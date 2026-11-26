"""Align the two POKEYs at playback start and at scored bass attacks."""

from pathlib import Path
from build_sequence import Code, DANCE_TICK
from school_portrait_bank import bank_value

ATTACK_SCORE = Path(__file__).resolve().parents[1] / 'assets/music/v035-bass-attacks.txt'
ATTACK_TABLE = 0x4e00  # Bank 0, after the card pages and before the scene helpers.


def install_attacks(bank):
    ticks = [int(tick) for tick in ATTACK_SCORE.read_text().partition('\n')[2].split()]
    if not ticks or ticks != sorted(set(ticks)) or not (ticks[0] == 0 < ticks[-1] < 59833):
        raise ValueError('invalid v035 bass attack schedule')
    # The development mix adds an attack two updates ahead of the dancer.
    attacks = sorted({*ticks[1:], DANCE_TICK - 2})
    data = b''.join(tick.to_bytes(2, 'little') for tick in (*attacks, 0xffff))
    offset = ATTACK_TABLE - 0x4000
    if len(data) > 0x400 or any(bank[offset:offset+len(data)]):
        raise ValueError('v035 bass attack table overlaps bank 0 artwork')
    return bank[:offset] + data + bank[offset+len(data):]


def start_gate(origin, callback, *, after_video=None):
    c = Code(origin)

    def absolute(opcode, address):
        c.emit(opcode, address & 255, address >> 8)

    for opcode, address in ((0xad, 0x24a7), (0x0d, 0x24a8), (0x0d, 0x24a9)):
        absolute(opcode, address)
    c.branch(0xd0, 'writer')
    c.emit(0xa9, ATTACK_TABLE & 255); c.jump(0x8d, 'attack_ptr')
    c.emit(0xa9, ATTACK_TABLE >> 8); c.jump(0x8d, 'attack_ptr_hi')
    c.jump(0x20, 'next_attack')

    # Stop the low frequency clocks and reset the noise generators. Load the
    # first packet under reset, then reload the timers and release both chips.
    c.emit(0xa9, 0)
    for address in (0xd20f, 0xd21f):
        absolute(0x8d, address)
    c.emit(0xa2, 8)
    c.label('load')
    for shadow, chip in ((0x2900, 0xd200), (0x2909, 0xd210)):
        absolute(0xbd, shadow)
        absolute(0x9d, chip)
    c.emit(0xca)
    c.branch(0x10, 'load')
    c.jump(0x20, 'sync_timers')
    c.emit(0xa9, 3)
    absolute(0x8d, 0xd20f)
    absolute(0x8d, 0xd21f)
    absolute(0x4c, 0x2c6c)

    c.label('writer')
    # Interleave writes to the two chips so each pair arrives together.
    for register in (8, 0, 2, 4, 6, 1, 3, 5, 7):
        for shadow, chip in ((0x2900, 0xd200), (0x2909, 0xd210)):
            absolute(0xad, shadow + register)
            absolute(0x8d, chip + register)

    absolute(0xad, 0x24a7)
    c.label('compare_lo'); c.emit(0xc9, 0xff)
    c.branch(0xd0, 'meters')
    absolute(0xad, 0x24a8)
    c.label('compare_hi'); c.emit(0xc9, 0xff)
    c.branch(0xd0, 'meters')
    c.jump(0x20, 'sync_timers')
    c.jump(0x20, 'next_attack')
    c.label('meters')
    absolute(0x4c, 0x2c6c)  # Original visual meters and tick handler.

    c.label('sync_timers')
    for address in (0xd40a, 0xd209, 0xd219):
        absolute(0x8d, address)
    c.emit(0x60)

    c.label('next_attack')
    absolute(0xad, 0xd301)
    c.emit(0x48)
    absolute(0xad, bank_value(0))
    absolute(0x8d, 0xd301)
    c.emit(0xa2, 0)
    c.label('read_attack'); absolute(0xbd, ATTACK_TABLE)
    c.jump(0x9d, 'attack_scratch')
    c.emit(0xe8, 0xe0, 2); c.branch(0xd0, 'read_attack')
    c.emit(0x68); absolute(0x8d, 0xd301)
    for i, label in enumerate(('compare_lo', 'compare_hi')):
        c.jump(0xad, 'attack_byte' + str(i))
        c.jump(0x8d, label + '_operand')
        c.labels[label + '_operand'] = c.labels[label] + 1
    c.emit(0x18); c.jump(0xad, 'attack_ptr')
    c.emit(0x69, 2); c.jump(0x8d, 'attack_ptr')
    c.branch(0x90, 'attack_ready')
    c.jump(0xee, 'attack_ptr_hi')
    c.label('attack_ready'); c.emit(0x60)
    c.label('attack_scratch'); c.label('attack_byte0'); c.emit(0)
    c.label('attack_byte1'); c.emit(0)
    c.labels['attack_ptr'] = c.labels['read_attack'] + 1
    c.labels['attack_ptr_hi'] = c.labels['read_attack'] + 2

    # The keyboard sets the request in the main loop. Drain it on the first
    # music interrupt of a frame. The video callback then draws the opening
    # frame while the music clock is held at zero.
    c.label('restart_request')
    absolute(0xad, 0x24a2)
    c.branch(0xf0, 'no_restart')
    absolute(0xad, 0xd40b)
    c.emit(0xc9, 32)
    c.branch(0xb0, 'defer_restart')
    c.emit(0xa9, 1)
    c.jump(0x8d, 'restart_stage')
    c.emit(0x60)
    c.label('defer_restart')
    c.emit(0xa9, 0)
    c.label('no_restart')
    c.emit(0x60)

    c.label('play_gate')
    c.jump(0xad, 'restart_stage')
    c.branch(0xf0, 'track_end')
    c.emit(0xc9, 3)
    c.branch(0xd0, 'hold_playback')
    absolute(0xad, 0xd40b)
    c.emit(0xc9, 32)
    c.branch(0xb0, 'hold_playback')
    c.emit(0xa9, 0)
    c.jump(0x8d, 'restart_stage')
    for address in (0x24aa, 0x24ab, 0x24ac):
        absolute(0x8d, address)
    c.label('track_end')
    absolute(0xad, 0x24c8)
    c.emit(0x60)
    c.label('hold_playback')
    c.emit(0xa9, 1, 0x60)

    # Prime both display lists with the opening scene, then start from a
    # fixed front buffer regardless of which page the previous scene used.
    c.label('video_callback')
    absolute(0xad, 0x24a2)
    c.branch(0xd0, 'video_wait')
    c.jump(0xad, 'restart_stage')
    c.branch(0xd0, 'prepare_intro')
    if after_video is None:
        absolute(0x4c, callback)
    else:
        absolute(0x20, callback)
        absolute(0x4c, after_video)
    c.label('prepare_intro')
    c.emit(0xc9, 3)
    c.branch(0xf0, 'video_wait')
    c.emit(0xa9, 0xff)
    absolute(0x8d, 0x83fa)  # Invalidate the scene cache to render this page.
    absolute(0x20, callback)
    c.jump(0xad, 'restart_stage')
    c.emit(0xc9, 1)
    c.branch(0xf0, 'advance_restart')
    absolute(0xad, 0x83e6)
    c.emit(0xc9, 0x80)
    c.branch(0xd0, 'video_wait')
    c.label('advance_restart')
    c.jump(0xee, 'restart_stage')
    c.label('video_wait')
    c.emit(0x60)
    c.label('restart_stage')
    c.emit(0)
    return bytes(c.finish()), c.labels
