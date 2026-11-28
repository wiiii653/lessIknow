"""Continuous four-row ANTIC 4 terminal under the main-act bitmaps."""

from build_sequence import Code, DANCE_TICK
from music_timing import tick_at_bar
from outro_text import START as CREDITS_START, GLYPHS, TERMINAL_FONT
from outro_palette import EXIT, GLYPH_INKS
import basketball_hero as hero
import girl_eyes
from gym_practice import PRACTICE_CUTS
from launch_kiss import START as KISS_START
from ribbon_dance import CUTS as RIBBON_CUTS, LAUNCH_PREP
from post_trevor_director import FIRST_ROTATOR, LATE_BANANA_START, START as MONTAGE_START
from school_parallax import BANK_INDEX, FRAME_COUNT, FRAMES_PER_BANK
from school_portrait_bank import bank_value
from school_story import (
    SCHOOL_PORTRAIT_TICK, SCHOOL_PORTRAIT_END, SCHOOL_PASS_START, WHISTLE_START, WHISTLE_END,
)
from trevor_awakens import MIDPOINT as TREVOR_CLOSE, FLIGHT_START
from trevor_polished import HITS as TREVOR_HITS

FONT = 0xd800
SCREENS = (0xda20, 0xdb20)
ENTRY = 0xdc00
CODE_LIMIT = 0xe180  # The practice framebuffer high-byte table follows.
LIMIT = 0xe240
FONT_LIMIT = 0xd960
PALETTE_TAIL = 0xdaeb
ROUTER_TAIL = 0xdbeb
WIDTH = 40
ROW_COUNT = 4
TYPE_STEP = 16  # Four PAL frames, matching the opening terminal.
LINE_HOLD = 48
LOG_DELAY = 12  # Give the scene three PAL frames to publish its new picture.
PALETTE_STEPS = 16
PALETTE_STEP_TICKS = 8
PALETTE_RESERVATION = 576
PALETTE_BANK = BANK_INDEX + FRAME_COUNT//FRAMES_PER_BANK
PALETTE_ENTRY = 0x6800 - PALETTE_RESERVATION
TEXT_ENTRY = 0x6000  # Free space before the palette ramps in the same bank.
FOOTER_OFFSET = 2 + 192 * 3
DISPLAY_LISTS = (0x8000, 0x8400)
TICK = 0x83e2
SCHOOL_START = tick_at_bar(8)
CUES = (SCHOOL_START, PRACTICE_CUTS[0], DANCE_TICK, FIRST_ROTATOR, RIBBON_CUTS[0],
        hero.CUTAWAY_START, hero.START, hero.END, MONTAGE_START, LATE_BANANA_START)
# Each entry has a window in which the action it describes is on screen.
CAPTIONS = (
    (
        (SCHOOL_START, SCHOOL_PORTRAIT_TICK, 'TRACKING THE SCHOOL ARRIVAL.'),
        (SCHOOL_PORTRAIT_TICK, SCHOOL_PORTRAIT_END, 'CUT TO THE GIRL IN CLOSE-UP.'),
        (SCHOOL_PORTRAIT_END, SCHOOL_PASS_START, 'BACK OUTSIDE.'),
        (SCHOOL_PASS_START, WHISTLE_START, 'SHE WALKS PAST.'),
        (WHISTLE_START, WHISTLE_END, 'THE BOY WHISTLES AS SHE WALKS AWAY.'),
        (WHISTLE_END, PRACTICE_CUTS[0], 'AT THE DOORWAY.'),
    ),
    (
        (PRACTICE_CUTS[0], PRACTICE_CUTS[1], 'TRACKING THE WIDE PRACTICE SHOT.'),
        (PRACTICE_CUTS[1], PRACTICE_CUTS[2], 'CHECKING THE BALL AGAINST THE HAND.'),
        (PRACTICE_CUTS[2], DANCE_TICK, 'STRETCHING AT THE WALL BARS.'),
    ),
    (
        (DANCE_TICK, FIRST_ROTATOR, 'TRACKING A SINGLE DANCER.'),
        (tick_at_bar(26), FIRST_ROTATOR, 'THE GYM SCROLLS BEHIND HER.'),
        (tick_at_bar(29), FIRST_ROTATOR, 'FOLLOWING HER RIBBONS IN PROFILE.'),
    ),
    (
        (FIRST_ROTATOR, tick_at_bar(33), 'SPIRAL TUNNEL.'),
        (tick_at_bar(33), tick_at_bar(34), 'ORGANIC TUNNEL.'),
        (tick_at_bar(34), tick_at_bar(36), 'TUNNEL REVERSES. BALL MOVES ON.'),
        (tick_at_bar(36), RIBBON_CUTS[0], 'TRACING THE BALL THROUGH THE CUTS.'),
    ),
    (
        (RIBBON_CUTS[0], RIBBON_CUTS[1], 'TWO DANCERS FLANK THE LEAD.'),
        (tick_at_bar(42), RIBBON_CUTS[1], 'THE TRIO MOVES THROUGH THE POSES.'),
        (RIBBON_CUTS[1], RIBBON_CUTS[2], 'CUTTING TO THE LEAD DANCER ALONE.'),
        (RIBBON_CUTS[2], LAUNCH_PREP, 'THE TRIO RETURNS FOR THE LIFT.'),
        (tick_at_bar(52), LAUNCH_PREP, 'TRACKING THE RIBBON BETWEEN POSES.'),
        (KISS_START, hero.CUTAWAY_START, 'A KISS.'),
    ),
    (
        (hero.CUTAWAY_START, hero.START, 'BACK THROUGH THE TUNNEL TO THE COURT.'),
    ),
    (
        (hero.START, hero.DUNK, 'TRACKING THE DRIBBLE IN THE ARENA.'),
        (tick_at_bar(60), hero.DUNK, 'FOUR SATELLITES ORBIT THE BALL.'),
        (hero.DUNK, hero.SHATTER_START, 'TRACKING THE WIND-UP AND LEAP.'),
        (hero.SHATTER_START, hero.END, 'CRACK.'),
    ),
    (
        (hero.END+48, TREVOR_CLOSE, 'TREVOR EMERGES IN THE DARK GYM.'),
        (TREVOR_CLOSE, FLIGHT_START, 'CHECKING TREVOR IN THE CLOSER SHOT.'),
        (TREVOR_HITS[0], MONTAGE_START, 'TRACKING EACH IMPACT AND REBOUND.'),
        (TREVOR_HITS[len(TREVOR_HITS)//2], MONTAGE_START, 'THE PUNCHES SWITCH HANDS.'),
    ),
    (
        (MONTAGE_START, tick_at_bar(84), 'THE BANANAS ROTATE INTO VIEW.'),
        (tick_at_bar(82), tick_at_bar(84), 'COMPARING THE BANANA ROTATIONS.'),
        (tick_at_bar(84), tick_at_bar(88), 'FOLLOWING THE RETURN TO THE SPIRAL.'),
        (tick_at_bar(88), tick_at_bar(92), 'THE TUNNEL SWITCHES TO ORGANIC.'),
        (tick_at_bar(92), tick_at_bar(96), 'THE BANANAS RETURN TO THE BEAT.'),
        (tick_at_bar(96), tick_at_bar(100), 'SPIRAL AGAIN. BALL STILL MOVING.'),
        (tick_at_bar(100), LATE_BANANA_START, 'WATCHING THE ORGANIC TUNNEL TURN.'),
    ),
    (
        (LATE_BANANA_START, girl_eyes.START, 'THE BANANAS FILL THE FRAME AGAIN.'),
        (girl_eyes.START, girl_eyes.END, 'HOLDING THE CLOSE-UP ON HER EYES.'),
        (girl_eyes.END, tick_at_bar(110), 'FOLLOWING THE LAST BANANA PASS.'),
        (tick_at_bar(110), CREDITS_START, 'ONE LAST SPIRAL BEFORE THE CREDITS.'),
    ),
)
# Three fixed inks give every glyph the scanline stripes from the greetings.
# Keep one palette per act so cuts within an act share the same colors.
PALETTES = (
    (0x98, 0x76, 0x56),  # School
    (0x48, 0x34, 0x26),  # Practice
    (0x68, 0x96, 0x46),  # Trio
    (0x28, 0xb4, 0xf6),  # First rotators
    (0x58, 0x86, 0x98),  # Ribbons
    (0x88, 0x94, 0xa6),  # Tunnel cutaway
    (0x38, 0x44, 0x56),  # Dunk
    (0x28, 0x44, 0x66),  # Trevor
    (0xa8, 0x84, 0x66),  # Late montage
    (0x78, 0x54, 0x36),  # Eyes and final stretch
)
assert len(PALETTES) == len(CUES) == len(CAPTIONS)


def typing_lines():
    return tuple('> '+line for scene in CAPTIONS for _, _, line in scene)


def line_starts():
    """Start on PAL frames and reject text that would spill past its action."""
    starts = []
    ready = SCHOOL_START
    lines = iter(typing_lines())
    for scene, cue, end in zip(CAPTIONS, CUES, (*CUES[1:], CREDITS_START)):
        for action, cut, _ in scene:
            line = next(lines)
            start = (action+LOG_DELAY+3) & ~3
            finished = start + TYPE_STEP*len(line)
            assert cue <= action < cut <= end, (line, cue, action, cut, end)
            assert start >= ready, (line, start, ready)
            assert finished < cut, (line, finished, cut)
            starts.append(start)
            ready = finished + LINE_HOLD
    return tuple(starts)


def resources():
    lines = typing_lines()
    charset = sorted(set(''.join(lines) + '_'))
    assert len(charset) < 64
    codes = {char: index for index, char in enumerate(charset, 1)}
    # Match the scanline inks and leading blank raster of the credits font.
    glyphs = bytearray(8)
    for char in charset:
        if char == '_':
            rows = ('000',)*6 + ('111',)
        elif char in TERMINAL_FONT:
            rows = TERMINAL_FONT[char].split()
        else:
            rows = [''.join(row[i] for i in (0, 2, 4)) for row in GLYPHS[char]]
        for row, ink in enumerate(GLYPH_INKS):
            glyphs.append(sum(ink << (6 - 2 * i)
                              for i, bit in enumerate(rows[max(0, row-1)])
                              if bit == '1'))
    assert all(len(line) < WIDTH for line in lines)
    return bytes(glyphs), codes, tuple(bytes(codes[char] for char in line) for line in lines)


def palette_steps():
    """Ease each ink along the shorter GTIA hue arc toward the next palette."""
    ramps = []
    for previous, target in zip((PALETTES[0], *PALETTES), PALETTES):
        for step in range(PALETTE_STEPS):
            fraction = step / (PALETTE_STEPS-1)
            weight = fraction*fraction*(3-2*fraction)
            inks = []
            for start, end in zip(previous, target):
                start_hue, end_hue = start >> 4, end >> 4
                assert start_hue and end_hue
                distance = (end_hue-start_hue+7)%15-7
                hue = (start_hue-1+round(distance*weight))%15+1
                low, high = start & 14, end & 14
                luma = 2*round((low+(high-low)*weight)/2)
                inks.append(hue << 4 | luma)
            ramps.append(tuple(inks))
    return tuple(ramps)


def install_bank(bank, labels):
    c = Code(PALETTE_ENTRY)

    def a(opcode, address):
        c.emit(opcode, address & 255, address >> 8)

    # X selects the current act. Stage its current inks in unbanked RAM
    # so the palette DLI never needs to switch banks.
    assert PALETTE_STEPS == 16 and PALETTE_STEP_TICKS == 8
    c.emit(0x8a,0x0a,0x0a,0x0a,0x0a)
    c.jump(0x8d,'ramp_base')
    c.emit(0x38)
    a(0xad,TICK);a(0xfd,labels['cue_lo']);c.emit(0xa8)
    a(0xad,TICK+1);a(0xfd,labels['cue_hi'])
    c.branch(0xd0,'full')
    c.emit(0x98,0x4a,0x4a,0x4a,0xc9,PALETTE_STEPS-1)
    c.branch(0x90,'step')
    c.label('full');c.emit(0xa9,PALETTE_STEPS-1)
    c.label('step');c.jump(0x0d,'ramp_base')
    a(0x8d,labels['next_palette'])
    a(0xcd,labels['shown_palette'])
    c.branch(0xf0,'ready')
    c.emit(0xaa)
    for pen in range(3):
        c.jump(0xbd,f'ink_{pen}');a(0x8d,labels['next_inks']+pen)
    c.label('ready');c.emit(0x60)
    c.label('ramp_base');c.emit(0)
    for pen, inks in enumerate(zip(*palette_steps())):
        c.label(f'ink_{pen}')
        c.emit(*inks)
    data = bytes(c.finish())
    assert len(data) <= PALETTE_RESERVATION
    _, _, records = resources()
    transcript = b''.join(records)
    assert TEXT_ENTRY + len(transcript) <= PALETTE_ENTRY
    result = bytearray(bank)
    for address, payload in ((TEXT_ENTRY, transcript), (PALETTE_ENTRY, data)):
        start = address - 0x4000
        end = start + len(payload)
        assert not any(result[start:end])
        result[start:end] = payload
    return bytes(result)


def build():
    glyphs, codes, records = resources()
    starts = line_starts()
    c = Code(ENTRY)

    def a(opcode, address):
        c.emit(opcode, address & 255, address >> 8)

    # Called with a coherent tick snapshot before the scene renderer. Restore
    # plain tails before the outro saves a list and before restart primes title.
    c.label('before')
    c.jump(0xad, 'enabled')
    c.jump(0x0d, 'pending')
    c.branch(0xf0, 'before_done')
    c.jump(0x20, 'select_page')
    c.branch(0xb0, 'before_done')
    c.emit(0xa9, 0)
    c.jump(0x8d, 'pending')
    c.jump(0x20, 'blank')
    c.emit(0xa9, 0x70)
    for base in DISPLAY_LISTS:
        for offset in range(3):
            a(0x8d, base + FOOTER_OFFSET + offset)
    c.emit(0xa9, 0)
    c.jump(0x8d, 'enabled')
    c.emit(0xa9, 0xff)
    c.jump(0x8d, 'shown_line')
    c.label('before_done')
    c.emit(0x60)

    # Called after rendering, including when the bitmap renderer kept its
    # old frame. Prepare an inactive text screen and publish only its LMS.
    c.label('update')
    c.jump(0xad, 'pending')
    c.branch(0xd0, 'update_done')
    c.jump(0x20, 'select_page')
    c.branch(0xb0, 'prepare')
    c.label('update_done')
    c.emit(0x60)
    c.label('prepare')
    a(0xad,0xd301);c.emit(0x48)
    a(0xad,bank_value(PALETTE_BANK));a(0x8d,0xd301)
    a(0x20,PALETTE_ENTRY)
    # The current transcript and palette live in the same bank. Keep it
    # selected until the inactive text screen has been prepared.
    c.jump(0x20, 'select_line')
    c.jump(0x8e, 'next_line')
    c.emit(0xa9, 0, 0xe0, 0xff)
    c.branch(0xf0, 'save_count')
    assert TYPE_STEP == 16
    c.emit(0x38)
    a(0xad, TICK)
    c.jump(0xfd, 'start_lo')
    c.emit(0xa8)
    a(0xad, TICK+1)
    c.jump(0xfd, 'start_hi')
    c.emit(0xc9, 3)
    c.branch(0xb0, 'full')
    c.emit(0x0a, 0x0a, 0x0a, 0x0a)
    c.jump(0x8d, 'count_copy')
    c.emit(0x98, 0x4a, 0x4a, 0x4a, 0x4a)
    c.jump(0x0d, 'count_copy')
    c.jump(0xdd, 'line_len')
    c.branch(0x90, 'blink')
    c.label('full')
    c.jump(0xbd, 'line_len')
    c.label('blink')
    # Bit 7 of the count represents the cursor, including while holding a line.
    a(0x2c, TICK)
    c.branch(0x70, 'save_count')
    c.emit(0x09, 0x80)
    c.label('save_count')
    c.jump(0x8d, 'next_count')
    c.jump(0xad, 'enabled')
    c.branch(0xf0, 'changed')
    c.jump(0xec, 'shown_line')
    c.branch(0xd0, 'changed')
    c.jump(0xad, 'next_count')
    c.jump(0xcd, 'shown_count')
    c.branch(0xd0, 'changed')
    c.jump(0xad, 'next_palette')
    c.jump(0xcd, 'shown_palette')
    c.branch(0xf0, 'no_change')
    c.emit(0xa9, 2)
    c.jump(0x8d, 'pending')
    c.label('no_change')
    c.jump(0x4c, 'restore_bank')
    c.label('changed')
    c.jump(0xad, 'front_hi')
    c.emit(0x49, 1)
    for operand in ('clear_hi', 'write_char_hi', 'cursor_hi'):
        c.jump(0x8d, operand)
    c.emit(0xa9, 0, 0xa2, WIDTH*ROW_COUNT-1)
    c.label('clear')
    a(0x9d, SCREENS[0])
    c.emit(0xca, 0xe0, 0xff)
    c.branch(0xd0, 'clear')
    c.jump(0xad, 'next_line')
    c.emit(0x38, 0xe9, ROW_COUNT-1)
    c.jump(0x8d, 'row_line')
    c.emit(0xa2, 0)
    c.label('write_row')
    c.jump(0x8e, 'row')
    c.jump(0xbc, 'row_offset')
    c.jump(0xae, 'row_line')
    c.branch(0x30, 'next_row')
    c.jump(0xbd, 'line_lo')
    c.jump(0x8d, 'read_char_lo')
    c.jump(0xbd, 'line_hi')
    c.jump(0x8d, 'read_char_hi')
    c.jump(0xad, 'row')
    c.emit(0xc9, ROW_COUNT-1)
    c.branch(0xf0, 'active_count')
    c.jump(0xae, 'row_line')
    c.jump(0xbd, 'line_len')
    c.branch(0xd0, 'copy_count')
    c.label('active_count')
    c.jump(0xad, 'next_count')
    c.emit(0x29, 0x7f)
    c.branch(0xf0, 'draw_cursor')
    c.label('copy_count')
    c.jump(0x8d, 'count_copy')
    c.emit(0xa2, 0)
    c.label('load_char')
    c.label('read_char')
    a(0xbd, 0)
    c.label('write_char')
    a(0x99, SCREENS[0])
    c.emit(0xc8, 0xe8)
    c.jump(0xce, 'count_copy')
    c.branch(0xd0, 'load_char')
    c.label('draw_cursor')
    c.jump(0xad, 'row')
    c.emit(0xc9, ROW_COUNT-1)
    c.branch(0xd0, 'next_row')
    c.jump(0xad, 'next_count')
    c.branch(0x10, 'next_row')
    c.emit(0xa9, codes['_'])
    c.label('cursor')
    a(0x99, SCREENS[0])
    c.label('next_row')
    c.jump(0xee, 'row_line')
    c.jump(0xae, 'row')
    c.emit(0xe8, 0xe0, ROW_COUNT)
    c.branch(0xd0, 'write_row')

    c.label('ready')
    c.jump(0xee, 'pending')
    c.label('restore_bank')
    c.emit(0x68);a(0x8d,0xd301)
    c.emit(0x60)

    # The last music DLI has already consumed the current list's footer.
    # Only enter the wait from the end of this frame, never from another DLI.
    c.label('commit')
    c.jump(0xad, 'pending')
    c.branch(0xf0, 'commit_done')
    a(0xad, 0xd40b)
    c.emit(0xc9, 121)
    c.branch(0x90, 'commit_done')
    c.label('publish_window')
    c.emit(0xc9, 128)
    c.branch(0xb0, 'commit_done')
    c.emit(0xc9, 124)
    c.branch(0xb0, 'publish')
    a(0xad, 0xd40b)
    c.jump(0x4c, 'publish_window')
    c.label('publish')
    c.jump(0xad, 'pending')
    c.emit(0xc9, 2)
    c.branch(0xf0, 'save')
    c.jump(0xad, 'front_hi')
    c.emit(0x49, 1)
    c.jump(0x8d, 'front_hi')
    for index in range(len(DISPLAY_LISTS)):
        c.jump(0x8d, f'text_hi_{index}')
    c.jump(0xad, 'enabled')
    c.branch(0xd0, 'save')
    c.emit(0xa9, FONT >> 8)
    a(0x8d, 0xd409)
    for index, base in enumerate(DISPLAY_LISTS):
        for part in range(2):
            c.emit(0xa9, 0)
            c.labels[f'tail_{index}_{part}'] = len(c.data)-1
            a(0x8d, base + FOOTER_OFFSET + part + 1)
        c.emit(0xa9, 1)  # ANTIC JMP to the separate tail.
        a(0x8d, base + FOOTER_OFFSET)
    c.jump(0x8d, 'enabled')
    c.label('save')
    c.jump(0xad, 'next_palette')
    c.jump(0x8d, 'shown_palette')
    c.emit(0xa2,2)
    c.label('copy_inks')
    c.jump(0xbd,'next_inks');c.jump(0x9d,'shown_inks')
    c.emit(0xca);c.branch(0x10,'copy_inks')
    c.jump(0xad, 'next_line')
    c.jump(0x8d, 'shown_line')
    c.jump(0xad, 'next_count')
    c.jump(0x8d, 'shown_count')
    c.emit(0xa9, 0)
    c.jump(0x8d, 'pending')
    c.label('commit_done')
    c.emit(0x60)

    # The blank line before the strip establishes its three inks once per
    # frame. Palette selection is independent of the typed line.
    c.label('palette')
    for pen in range(3):
        c.jump(0xad, f'shown_ink_{pen}')
        a(0x8d, 0xd016+pen)
    a(0x4c, EXIT)

    c.label('select_page')
    # Compare the 24-bit music clock against the upper bound, then find the
    # latest cue. Carry signals an active caption.
    a(0xad, TICK+2)
    c.branch(0xd0, 'outside')
    a(0xad, TICK+1)
    c.emit(0xc9, CREDITS_START >> 8)
    c.branch(0x90, 'scan_start')
    c.branch(0xd0, 'outside')
    a(0xad, TICK)
    c.emit(0xc9, CREDITS_START & 255)
    c.branch(0xb0, 'outside')
    c.label('scan_start')
    c.emit(0xa2, len(CUES)-1)
    c.label('scan')
    a(0xad, TICK+1)
    c.jump(0xdd, 'cue_hi')
    c.branch(0x90, 'previous')
    c.branch(0xd0, 'found')
    a(0xad, TICK)
    c.jump(0xdd, 'cue_lo')
    c.branch(0xb0, 'found')
    c.label('previous')
    c.emit(0xca)
    c.branch(0x10, 'scan')
    c.label('outside')
    c.emit(0x18, 0x60)
    c.label('found')
    c.emit(0x38, 0x60)

    # In order playback normally needs only the current and next cue.
    # Seek in either direction when the foreground has skipped a line.
    c.label('select_line')
    c.jump(0xae, 'shown_line')
    c.label('advance')
    c.emit(0xe8, 0xe0, len(starts))
    c.branch(0xb0, 'use_previous')
    c.jump(0x20, 'line_has_started')
    c.branch(0xb0, 'advance')
    c.label('use_previous')
    c.emit(0xca)
    c.branch(0x30, 'line_found')
    c.jump(0x20, 'line_has_started')
    c.branch(0x90, 'use_previous')
    c.label('line_found')
    c.emit(0x60)
    c.label('line_has_started')
    a(0xad, TICK+1)
    c.jump(0xdd, 'start_hi')
    c.branch(0xd0, 'line_found')
    a(0xad, TICK)
    c.jump(0xdd, 'start_lo')
    c.emit(0x60)
    c.label('blank')
    a(0xad, 0xd40b)
    c.emit(0xc9, 124)
    c.branch(0x90, 'blank')
    c.emit(0xc9, 128)
    c.branch(0xb0, 'blank')
    c.emit(0x60)

    for label, address in (('read_char_lo', 'read_char'), ('read_char_hi', 'read_char'),
                           ('write_char_hi', 'write_char'), ('clear_hi', 'clear'),
                           ('cursor_hi', 'cursor')):
        c.labels[label] = c.labels[address] + (1 if label.endswith('lo') else 2)
    for label, value in (('enabled', 0), ('front_hi', SCREENS[0] >> 8),
                         ('shown_palette', 0xff), ('shown_line', 0xff), ('shown_count', 0),
                         ('next_palette', 0), ('next_line', 0xff), ('next_count', 0),
                         ('count_copy', 0), ('row', 0), ('row_line', 0), ('pending', 0)):
        c.label(label)
        c.emit(value)
    c.label('next_inks');c.emit(0,0,0)
    c.label('shown_inks')
    for pen in range(3):
        c.label(f'shown_ink_{pen}');c.emit(0)
    for index, base in enumerate(DISPLAY_LISTS):
        tail = c.origin + len(c.data)
        c.data[c.labels[f'tail_{index}_0']] = tail & 255
        c.data[c.labels[f'tail_{index}_1']] = tail >> 8
        c.emit(0x90, 0x44, SCREENS[0] & 255)
        c.label(f'text_hi_{index}')
        c.emit(0, 0x04, 0x04, 0x84, 0x41, base & 255, base >> 8)
        assert (tail & 0x3ff) + 10 <= 0x400
    # Use the space between existing tables and the two text buffers so the
    # renderer still fits ahead of the practice framebuffer map.
    auxiliary = []
    for address, limit, tables in (
        (PALETTE_TAIL, SCREENS[1], (('start_lo', (tick & 255 for tick in starts)),)),
        (ROUTER_TAIL, ENTRY, (('cue_lo', (tick & 255 for tick in CUES)),
                              ('cue_hi', (tick >> 8 for tick in CUES)))),
    ):
        data = bytearray()
        for name, values in tables:
            c.labels[name] = address+len(data)
            data.extend(values)
        assert address+len(data) <= limit
        auxiliary.append((address, bytes(data)))
    for name, values in (('row_offset', (row*WIDTH for row in range(ROW_COUNT))),
                         ('start_hi', (tick >> 8 for tick in starts)), ('line_len', map(len, records))):
        c.label(name)
        c.emit(*values)
    for part in ('lo', 'hi'):
        c.label('line_' + part)
        for index in range(len(records)):
            c.emit(0)
    address = TEXT_ENTRY
    for index, record in enumerate(records):
        c.data[c.labels['line_lo']-c.origin+index] = address & 255
        c.data[c.labels['line_hi']-c.origin+index] = address >> 8
        address += len(record)
    assert address <= PALETTE_ENTRY

    code = bytes(c.finish())
    assert FONT + len(glyphs) <= FONT_LIMIT
    assert ENTRY + len(code) <= CODE_LIMIT, hex(ENTRY + len(code))
    return [(FONT, glyphs), *auxiliary, *((screen, bytes(WIDTH*ROW_COUNT)) for screen in SCREENS),
            (ENTRY, code)], c.labels
