"""Small unbanked helper routines and preloaded PMG beat accents."""
from build_sequence import Code
from music_timing import tick_at_beat

COPY_ORIGIN = 0xcf00
EFFECT_ORIGIN = 0xaf00


def copy_helper():
    c = Code(COPY_ORIGIN)
    c.label('pixels')
    for page in range(31):
        if page == 4:
            c.label('dirty_pixels')
        c.emit(0xbd, 0, 0x40 + page, 0x9d, 0, 0x90 + page)
        if page == 24:
            c.label('gate')
            c.jump(0x4c, 'tail')
            c.label('tail')
    c.label('end')
    c.emit(0xe8)
    c.branch(0xf0, 'done')
    c.label('repeat')
    c.jump(0x4c, 'pixels')
    c.label('done')
    c.emit(0x60)
    data = c.finish()
    assert len(data) <= 256
    return data, c.labels


def effects_helper(state=0x83e0):
    c = Code(EFFECT_ORIGIN)
    def absop(op, address):
        c.emit(op, address & 255, address >> 8)
    # Called at vblank, even when the underlying picture remains unchanged.
    c.emit(0xa9, 0)
    absop(0x8d, 0xd01d)
    absop(0x8d, 0xd01b)
    c.emit(0xa9, 0x22)
    absop(0x8d, 0xd400)
    absop(0xad, state)
    c.emit(0xc9, 2)
    c.branch(0xb0, 'check_dance')
    c.emit(0x60)
    c.label('check_dance')
    c.emit(0xc9, 6)
    c.branch(0x90, 'check_slide')
    c.emit(0x60)
    c.label('check_slide')
    absop(0xad, state + 1)
    c.branch(0xf0, 'animate')
    c.emit(0x60)
    c.label('animate')
    c.emit(0xa2, 31)
    c.label('find_beat')
    absop(0xad, state + 3)
    c.jump(0xdd, 'beat_hi')
    c.branch(0x90, 'previous')
    c.branch(0xd0, 'found')
    absop(0xad, state + 2)
    c.jump(0xdd, 'beat_lo')
    c.branch(0xb0, 'found')
    c.label('previous')
    c.emit(0xca)
    c.branch(0x10, 'find_beat')
    c.emit(0x60)
    c.label('found')
    c.emit(0x38)
    absop(0xad, state + 2)
    c.jump(0xfd, 'beat_lo')
    c.emit(0xa8)
    absop(0xad, state + 3)
    c.jump(0xfd, 'beat_hi')
    c.branch(0xd0, 'done')
    c.emit(0xc0, 24)
    c.branch(0xb0, 'done')
    # Warm -> cyan -> pink decay, matching existing playfield colors.
    c.emit(0xa9, 0x2c, 0xc0, 8)
    c.branch(0x90, 'ink')
    c.emit(0xa9, 0x9a, 0xc0, 16)
    c.branch(0x90, 'ink')
    c.emit(0xa9, 0x48)
    c.label('ink')
    c.emit(0xa2, 3)
    c.label('set_ink')
    absop(0x9d, 0xd012)
    c.emit(0xca)
    c.branch(0x10, 'set_ink')
    c.emit(0xa2, 3)
    c.label('set_positions')
    c.jump(0xbd, 'positions')
    absop(0x9d, 0xd000)
    c.emit(0x18, 0x69, 9)
    absop(0x9d, 0xd004)
    c.emit(0xca)
    c.branch(0x10, 'set_positions')
    c.emit(0xa9, 0, 0xa2, 4)
    c.label('set_sizes')
    absop(0x9d, 0xd008)
    c.emit(0xca)
    c.branch(0x10, 'set_sizes')
    c.emit(0xa9, 8)
    absop(0x8d, 0xd407)
    c.emit(0xa9, 1)
    absop(0x8d, 0xd01b)
    c.emit(0xa9, 3)
    absop(0x8d, 0xd01d)
    c.emit(0xa9, 0x2e)
    absop(0x8d, 0xd400)
    c.label('done')
    c.emit(0x60)
    beats = [tick_at_beat(96 + i) for i in range(32)]
    c.label('positions'); c.emit(*(x + 48 for x in (20, 55, 99, 136)))
    c.label('beat_lo'); c.emit(*(t & 255 for t in beats))
    c.label('beat_hi'); c.emit(*(t >> 8 for t in beats))
    data = c.finish()
    assert len(data) <= 256, len(data)
    return data


def pmg_art():
    players = bytearray(512)
    missiles = bytearray(128)
    for i, row in enumerate((14, 10, 15, 11)):
        players[i*128+row:i*128+row+7] = bytes((0x10, 0x10, 0x38, 0xfe, 0x38, 0x10, 0x10))
        for y in range(row - 3, row):
            missiles[y] |= 3 << (2 * i)
    return bytes(missiles), bytes(players)
