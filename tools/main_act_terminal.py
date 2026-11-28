"""Continuous four-row, one-bit ANTIC C terminal under the main-act bitmaps."""

from build_sequence import Code, DANCE_TICK
from music_timing import tick_at_bar
from outro_text import PREP_START as CREDITS_START, GLYPHS, TERMINAL_FONT
from outro_palette import EXIT
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

LIMIT = 0xe240
WIDTH = 40
ROW_COUNT = 4
GLYPH_ROWS = 7  # Each row starts with one blank scanline.
STRIDE = WIDTH // 2
ROW_BYTES = STRIDE * GLYPH_ROWS
# Two pages of four row slots. Each slot is within one 4 KiB ANTIC page.
BITMAP_ROWS = (0xd800, 0xda20, 0xdb20, *(0xdc00+n*ROW_BYTES for n in range(5)))
BEFORE = 0xd88c
ROW_ADDRESSES = 0xdaac
TAILS = (0xdf6d, 0xdaeb)
UPDATE = 0xdbac
PALETTE = 0xdbeb
ENABLED, PENDING, FRONT, LINE, COUNT, INK, NEXT_INK = range(0xdbf4, 0xdbfb)
COMMIT = 0xdebc
PATCH_ROWS = TAILS[0] + 1 + ROW_COUNT * 10 + 3
BANK_UPDATE = 0x5db0
GLYPHS_ENTRY = 0x6480
DRAW_ROW = 0x7000
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
        (SCHOOL_START, SCHOOL_PORTRAIT_TICK, 'ATARI ARENA. TRACKING ARRIVAL.'),
        (SCHOOL_PORTRAIT_TICK, SCHOOL_PORTRAIT_END, 'TRACKING HER IN CLOSE-UP.'),
        (SCHOOL_PORTRAIT_END, SCHOOL_PASS_START, 'BACK TO THE BOY.'),
        (SCHOOL_PASS_START, WHISTLE_START, 'SHE WALKS PAST.'),
        (WHISTLE_START, WHISTLE_END, 'THE BOY WHISTLES AS SHE WALKS AWAY.'),
        (WHISTLE_END, PRACTICE_CUTS[0], 'AT THE DOORWAY.'),
    ),
    (
        (PRACTICE_CUTS[0], PRACTICE_CUTS[1], 'CLOSE-UP. HE HOLDS THE BALL.'),
        (PRACTICE_CUTS[1], PRACTICE_CUTS[2], 'HE SHOOTS. TRACKING THE BALL.'),
        (PRACTICE_CUTS[2], DANCE_TICK, 'STRETCHING AT THE WALL BARS.'),
    ),
    (
        (DANCE_TICK, FIRST_ROTATOR, 'TRACKING A SINGLE DANCER.'),
        (tick_at_bar(27), FIRST_ROTATOR, 'RIBBONS IN PROFILE. COURT SCROLLS.'),
    ),
    (
        (FIRST_ROTATOR, tick_at_bar(33), 'SPIRAL TUNNEL.'),
        (tick_at_bar(33), tick_at_bar(34), 'ORGANIC TUNNEL.'),
        (tick_at_bar(34), tick_at_bar(35), 'SPIRAL REVERSES.'),
        (tick_at_bar(35), tick_at_bar(36), 'ORGANIC REVERSES.'),
        (tick_at_bar(36), tick_at_bar(37), 'BACK TO SPIRAL.'),
        (tick_at_bar(37), tick_at_bar(38), 'BACK TO ORGANIC.'),
        (tick_at_bar(38), RIBBON_CUTS[0], 'THE BALL KEEPS MOVING FORWARD.'),
    ),
    (
        (RIBBON_CUTS[0], RIBBON_CUTS[1], 'TWO DANCERS FLANK THE LEAD.'),
        (RIBBON_CUTS[1], RIBBON_CUTS[2], 'CUTTING TO THE LEAD DANCER ALONE.'),
        (RIBBON_CUTS[2], LAUNCH_PREP, 'THE TRIO RETURNS.'),
        (LAUNCH_PREP, KISS_START, 'LIFT.'),
        (KISS_START, hero.CUTAWAY_START, 'A KISS.'),
    ),
    (
        (hero.CUTAWAY_START, hero.START, 'BACK THROUGH THE TUNNEL TO THE COURT.'),
    ),
    (
        (hero.START, hero.DUNK, 'TRACKING THE DRIBBLE IN THE ARENA.'),
        (tick_at_bar(60), hero.DUNK, 'FOUR SATELLITES ORBIT THE BALL.'),
        (hero.DUNK, hero.SHATTER_START, 'TRACKING THE DUNK.'),
        (hero.SHATTER_START, hero.END, 'CRACK'),
    ),
    (
        (hero.END+48, TREVOR_CLOSE, 'TREVOR EMERGES FROM THE DARK.'),
        (TREVOR_CLOSE, FLIGHT_START, 'CHECKING TREVOR IN THE CLOSER SHOT.'),
        (TREVOR_HITS[0], MONTAGE_START, 'TRACKING EACH IMPACT AND REBOUND.'),
        (TREVOR_HITS[len(TREVOR_HITS)//2], MONTAGE_START, 'THE PUNCHES SWITCH HANDS.'),
    ),
    (
        (MONTAGE_START, tick_at_bar(84), 'THE BANANAS ROTATE INTO VIEW.'),
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
# One ink per act, with a ramp between acts.
PALETTES = (
    0x98,  # Atari Arena arrival
    0x48,  # Practice
    0x68,  # Trio
    0x28,  # First rotators
    0x58,  # Ribbons
    0x88,  # Tunnel cutaway
    0x38,  # Dunk
    0x28,  # Trevor
    0xa8,  # Late montage
    0x78,  # Eyes and final stretch
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
    shapes = [('000',)*GLYPH_ROWS]
    for char in charset:
        if char == '_':
            rows = ('000',)*6 + ('111',)
        elif char in TERMINAL_FONT:
            rows = TERMINAL_FONT[char].split()
        else:
            rows = [''.join(row[i] for i in (0, 2, 4)) for row in GLYPHS[char]]
        shapes.append(rows)
    glyphs = bytes(int(bits, 2) << 1 for row in zip(*shapes) for bits in row)
    assert all(len(line) < WIDTH for line in lines)
    return glyphs, codes, tuple(bytes(codes[char] for char in line) for line in lines)


def palette_steps():
    """Ease the text ink along the shorter GTIA hue arc between acts."""
    ramps = []
    for start, end in zip((PALETTES[0], *PALETTES), PALETTES):
        start_hue, end_hue = start >> 4, end >> 4
        assert start_hue and end_hue
        distance = (end_hue-start_hue+7)%15-7
        low, high = start & 14, end & 14
        for step in range(PALETTE_STEPS):
            fraction = step / (PALETTE_STEPS-1)
            weight = fraction*fraction*(3-2*fraction)
            hue = (start_hue-1+round(distance*weight))%15+1
            luma = 2*round((low+(high-low)*weight)/2)
            ramps.append(hue << 4 | luma)
    return tuple(ramps)


def absolute(c, opcode, address):
    c.emit(opcode, address & 255, address >> 8)


def check_window(c, outside):
    """Branch outside the main-act interval using the coherent 24-bit tick."""
    absolute(c, 0xad, TICK+2)
    c.branch(0xd0, outside)
    absolute(c, 0xac, TICK+1)
    c.emit(0xc0, SCHOOL_START >> 8)
    c.branch(0x90, outside)
    c.branch(0xd0, 'check_end')
    absolute(c, 0xad, TICK)
    c.emit(0xc9, SCHOOL_START & 255)
    c.branch(0x90, outside)
    c.label('check_end')
    c.emit(0xc0, CREDITS_START >> 8)
    c.branch(0x90, 'inside')
    c.branch(0xd0, outside)
    absolute(c, 0xad, TICK)
    c.emit(0xc9, CREDITS_START & 255)
    c.branch(0xb0, outside)
    c.label('inside')


def palette_helper(labels):
    c = Code(PALETTE_ENTRY)
    def a(op, addr): absolute(c, op, addr)

    assert PALETTE_STEPS == 16 and PALETTE_STEP_TICKS == 8
    c.emit(0x8a, 0x0a, 0x0a, 0x0a, 0x0a)
    c.jump(0x8d, 'ramp_base')
    c.emit(0x38)
    a(0xad, TICK); a(0xfd, labels['cue_lo']); c.emit(0xa8)
    a(0xad, TICK+1); a(0xfd, labels['cue_hi'])
    c.branch(0xd0, 'full')
    c.emit(0x98, 0x4a, 0x4a, 0x4a, 0xc9, PALETTE_STEPS-1)
    c.branch(0x90, 'step')
    c.label('full'); c.emit(0xa9, PALETTE_STEPS-1)
    c.label('step'); c.jump(0x0d, 'ramp_base')
    c.emit(0xaa); c.jump(0xbd, 'ramps'); a(0x8d, NEXT_INK); c.emit(0x60)
    c.label('ramp_base'); c.emit(0)
    c.label('ramps'); c.emit(*palette_steps())
    return bytes(c.finish())


def bank_update(records):
    starts = line_starts()
    c = Code(BANK_UPDATE)
    def a(op, addr): absolute(c, op, addr)

    a(0xad, PENDING)
    c.branch(0xf0, 'idle')
    c.emit(0x60)
    c.label('idle')
    check_window(c, 'outside')
    c.jump(0x4c, 'select_cue')
    c.label('outside'); c.emit(0x60)
    c.label('select_cue')
    # The active window guarantees a cue at or before the snapshot.
    c.emit(0xa2, len(CUES)-1)
    c.label('cue')
    a(0xad, TICK+1); c.jump(0xdd, 'cue_hi')
    c.branch(0x90, 'previous_cue')
    c.branch(0xd0, 'cue_found')
    a(0xad, TICK); c.jump(0xdd, 'cue_lo')
    c.branch(0xb0, 'cue_found')
    c.label('previous_cue'); c.emit(0xca); c.branch(0x10, 'cue')
    c.label('cue_found'); a(0x20, PALETTE_ENTRY)

    # Start at the last prepared line and walk only as far as the tick needs.
    a(0xae, LINE)
    c.label('advance')
    c.emit(0xe8, 0xe0, len(starts))
    c.branch(0xb0, 'previous_line')
    c.jump(0x20, 'line_started')
    c.branch(0xb0, 'advance')
    c.label('previous_line')
    c.emit(0xca)
    c.branch(0x30, 'line_found')
    c.jump(0x20, 'line_started')
    c.branch(0x90, 'previous_line')
    c.label('line_found')
    c.jump(0x8e, 'new_line')
    c.emit(0xa9, 0, 0xe0, 0xff)
    c.branch(0xf0, 'count_ready')
    assert TYPE_STEP == 16
    c.emit(0x38)
    a(0xad, TICK); c.jump(0xfd, 'start_lo'); c.emit(0xa8)
    a(0xad, TICK+1); c.jump(0xfd, 'start_hi')
    c.emit(0xc9, 3)
    c.branch(0xb0, 'full_line')
    c.emit(0x0a, 0x0a, 0x0a, 0x0a)
    c.jump(0x8d, 'new_count')
    c.emit(0x98, 0x4a, 0x4a, 0x4a, 0x4a)
    c.jump(0x0d, 'new_count'); c.jump(0xdd, 'line_len')
    c.branch(0x90, 'cursor')
    c.label('full_line'); c.jump(0xbd, 'line_len')
    c.label('cursor')
    a(0x2c, TICK); c.branch(0x70, 'count_ready')
    c.emit(0x09, 0x80)
    c.label('count_ready'); c.jump(0x8d, 'new_count')

    a(0xad, ENABLED); c.branch(0xf0, 'render')
    a(0xec, LINE); c.branch(0xd0, 'render')
    a(0xad, COUNT); c.jump(0xcd, 'new_count'); c.branch(0xd0, 'render')
    a(0xad, NEXT_INK); a(0xcd, INK); c.branch(0xf0, 'done')
    c.emit(0xa9, 2); a(0x8d, PENDING)
    c.label('done'); c.emit(0x60)

    c.label('render')
    c.jump(0xad, 'new_line'); a(0x8d, LINE)
    c.emit(0x38, 0xe9, ROW_COUNT-1); c.jump(0x8d, 'row_line')
    c.jump(0xad, 'new_count'); a(0x8d, COUNT)
    a(0xad, FRONT); c.emit(0x49, ROW_COUNT); c.jump(0x8d, 'back')
    c.label('row')
    # Each page is a four-slot ring. On Enter, the old rows remain in
    # their slots and publication rotates the order of their LMS addresses.
    c.jump(0xad, 'row_line')
    c.emit(0x29, ROW_COUNT-1); c.jump(0x0d, 'back'); c.emit(0xaa)
    c.jump(0xad, 'row_line'); a(0xcd, LINE)
    c.branch(0xf0, 'active_row')
    c.emit(0xa8)
    c.branch(0x30, 'empty_row')
    c.jump(0xb9, 'line_len'); c.emit(0xa8)
    c.branch(0x10, 'draw')
    c.label('empty_row'); c.emit(0xa0, 0); c.branch(0xf0, 'draw')
    c.label('active_row'); a(0xac, COUNT)
    c.label('draw'); c.jump(0xad, 'row_line'); a(0x20, DRAW_ROW)
    c.jump(0xad, 'row_line'); a(0xcd, LINE)
    c.branch(0xf0, 'ready')
    c.jump(0xee, 'row_line'); c.jump(0x4c, 'row')
    c.label('ready'); c.emit(0xa9, 1); a(0x8d, PENDING); c.emit(0x60)

    c.label('line_started')
    a(0xad, TICK+1); c.jump(0xdd, 'start_hi')
    c.branch(0xd0, 'line_started_done')
    a(0xad, TICK); c.jump(0xdd, 'start_lo')
    c.label('line_started_done'); c.emit(0x60)

    for name in ('new_line', 'new_count', 'row_line', 'back'):
        c.label(name); c.emit(0)
    addresses = []
    address = TEXT_ENTRY
    for record in records:
        addresses.append(address)
        address += len(record)
    assert address <= GLYPHS_ENTRY
    for name, data in (
        ('cue_lo', (tick & 255 for tick in CUES)),
        ('cue_hi', (tick >> 8 for tick in CUES)),
        ('start_hi', (tick >> 8 for tick in starts)),
        ('start_lo', (tick & 255 for tick in starts)),
        ('line_len', map(len, records)),
        ('line_lo', (addr & 255 for addr in addresses)),
        ('line_hi', (addr >> 8 for addr in addresses)),
    ):
        c.label(name); c.emit(*data)
    return bytes(c.finish()), c.labels


def draw_row(glyph_count, cursor, labels):
    """Update the changed pairs of glyphs in one inactive bitmap row."""
    c = Code(DRAW_ROW)
    def a(op, addr): absolute(c, op, addr)

    # A = transcript line (negative for blank), X = slot, Y = count and cursor.
    c.jump(0x8d, 'source_line'); c.jump(0x8e, 'slot'); c.jump(0x8c, 'count')
    c.jump(0xdd, 'slot_lines'); c.branch(0xd0, 'different_line')
    c.emit(0x98); c.jump(0xdd, 'slot_counts'); c.branch(0xd0, 'same_line')
    c.emit(0x60)
    c.label('same_line'); c.emit(0xa9, 1); c.branch(0xd0, 'range')
    c.label('different_line'); c.emit(0xa9, 0)
    c.label('range'); c.jump(0x8d, 'incremental')
    c.jump(0xad, 'source_line'); c.jump(0x9d, 'slot_lines')
    c.jump(0xbd, 'slot_counts'); c.emit(0x29, 0x7f)
    c.jump(0x8d, 'minimum')
    c.emit(0x98); c.jump(0x9d, 'slot_counts'); c.emit(0x29, 0x7f)
    c.jump(0x8d, 'length'); c.jump(0xcd, 'minimum')
    c.branch(0xb0, 'maximum')
    c.jump(0xae, 'minimum'); c.jump(0x8d, 'minimum'); c.emit(0x8a)
    c.label('maximum')
    c.emit(0x4a, 0x18, 0x69, 1)
    c.jump(0x8d, 'stop_pair')
    c.jump(0xad, 'incremental'); c.branch(0xf0, 'first_pair')
    c.jump(0xad, 'minimum'); c.emit(0x4a)
    c.label('first_pair'); c.jump(0x8d, 'pair')

    c.jump(0xae, 'source_line'); c.branch(0x30, 'no_source')
    a(0xbd, labels['line_lo']); c.jump(0x8d, 'read_lo')
    a(0xbd, labels['line_hi']); c.jump(0x8d, 'read_hi')
    c.label('no_source')
    c.jump(0xac, 'slot')
    a(0xb9, ROW_ADDRESSES); c.jump(0x8d, 'dst_lo')
    a(0xb9, ROW_ADDRESSES+len(BITMAP_ROWS)); c.jump(0x8d, 'dst_hi')
    c.emit(0xa2, 0)
    c.label('patch')
    # Each LDA/STA pair in the blit has six bytes. Advance the bitmap
    # address by one stride for the next scanline.
    c.jump(0xad, 'dst_lo'); c.jump(0x9d, 'store_lo')
    c.emit(0x18, 0x69, STRIDE); c.jump(0x8d, 'dst_lo')
    c.jump(0xad, 'dst_hi'); c.jump(0x9d, 'store_hi')
    c.emit(0x69, 0); c.jump(0x8d, 'dst_hi')
    c.emit(0x8a, 0x18, 0x69, 6, 0xaa, 0xe0, 6*GLYPH_ROWS)
    c.branch(0xd0, 'patch')

    c.label('draw_pair')
    c.jump(0xad, 'pair'); c.emit(0x0a, 0xa8)
    c.jump(0x20, 'character'); c.emit(0xaa, 0xc8)
    c.jump(0x20, 'character'); c.emit(0xa8)
    for row in range(GLYPH_ROWS):
        lookup = GLYPHS_ENTRY+row*glyph_count
        a(0xbd, lookup); c.emit(0x0a, 0x0a, 0x0a, 0x0a)
        a(0x19, lookup); c.jump(0x8d, f'pixels_{row}')
    c.jump(0xac, 'pair')
    for row in range(GLYPH_ROWS):
        c.jump(0xad, f'pixels_{row}')
        if row == 0:
            c.labels['store_lo'] = c.origin+len(c.data)+1
            c.labels['store_hi'] = c.origin+len(c.data)+2
        a(0x99, 0)
    c.jump(0xee, 'pair'); c.jump(0xad, 'pair'); c.jump(0xcd, 'stop_pair')
    c.branch(0xb0, 'finished'); c.jump(0x4c, 'draw_pair')
    c.label('finished'); c.emit(0x60)

    c.label('character')
    c.jump(0xcc, 'length'); c.branch(0x90, 'read_char')
    c.branch(0xd0, 'space')
    c.jump(0xad, 'count'); c.branch(0x10, 'space')
    c.emit(0xa9, cursor, 0x60)
    c.label('space'); c.emit(0xa9, 0, 0x60)
    c.label('read_char'); a(0xb9, 0); c.emit(0x60)
    c.labels['read_lo'] = c.labels['read_char']+1
    c.labels['read_hi'] = c.labels['read_char']+2
    for name in ('source_line', 'slot', 'count', 'length', 'minimum',
                 'incremental', 'pair', 'stop_pair', 'dst_lo', 'dst_hi',
                 *(f'pixels_{row}' for row in range(GLYPH_ROWS))):
        c.label(name); c.emit(0)
    c.label('slot_lines'); c.emit(*([0x80]*len(BITMAP_ROWS)))
    c.label('slot_counts'); c.emit(*bytes(len(BITMAP_ROWS)))
    return bytes(c.finish())


def bank_inserts():
    glyphs, codes, records = resources()
    update, labels = bank_update(records)
    palette = palette_helper(labels)
    blocks = (
        (BANK_UPDATE, update),
        (TEXT_ENTRY, b''.join(records)),
        (GLYPHS_ENTRY, glyphs),
        (PALETTE_ENTRY, palette),
        (DRAW_ROW, draw_row(len(codes)+1, codes['_'], labels)),
    )
    assert all(start+len(data) <= following for (start, data), (following, _) in zip(blocks, blocks[1:]))
    assert PALETTE_ENTRY+len(palette) <= 0x6800
    return blocks


def install_bank(bank):
    result = bytearray(bank)
    for address, payload in bank_inserts():
        start = address-0x4000
        end = start+len(payload)
        assert end <= len(result) and not any(result[start:end]), hex(address)
        result[start:end] = payload
    return bytes(result)


def retire():
    c = Code(BEFORE)
    def a(op, addr): absolute(c, op, addr)

    a(0xad, ENABLED); a(0x0d, PENDING)
    c.branch(0xf0, 'done')
    check_window(c, 'retire')
    c.emit(0x60)
    c.label('retire')
    c.emit(0xa2, 0); a(0x8e, PENDING)
    c.label('blank')
    a(0xad, 0xd40b); c.emit(0xc9, 124); c.branch(0x90, 'blank')
    c.emit(0xc9, 128); c.branch(0xb0, 'blank')
    c.emit(0xa9, 0x70)
    for base in DISPLAY_LISTS:
        for offset in range(3):
            a(0x8d, base+FOOTER_OFFSET+offset)
    a(0x8e, ENABLED)
    c.label('done'); c.emit(0x60)
    return bytes(c.finish())


def publish():
    c = Code(COMMIT)
    def a(op, addr): absolute(c, op, addr)

    # The last music DLI has already consumed this frame's footer. Only
    # make the prepared page visible in the same bounded blanking window.
    a(0xae, PENDING); c.branch(0xf0, 'done')
    a(0xad, 0xd40b); c.emit(0xc9, 121); c.branch(0x90, 'done')
    c.label('window')
    c.emit(0xc9, 128); c.branch(0xb0, 'done')
    c.emit(0xc9, 124); c.branch(0xb0, 'publish')
    a(0xad, 0xd40b); c.jump(0x4c, 'window')
    c.label('publish')
    c.emit(0xe0, 2); c.branch(0xf0, 'save')
    a(0xad, FRONT); c.emit(0x49, ROW_COUNT); a(0x8d, FRONT)
    a(0xad, LINE); c.emit(0x38, 0xe9, ROW_COUNT-1, 0x29, ROW_COUNT-1)
    a(0x0d, FRONT); c.emit(0xaa); a(0x20, PATCH_ROWS)
    a(0xad, ENABLED); c.branch(0xd0, 'save')
    for base, tail in zip(DISPLAY_LISTS, TAILS):
        for part in range(2):
            c.emit(0xa9, (tail >> (part*8)) & 255)
            a(0x8d, base+FOOTER_OFFSET+part+1)
    c.emit(0xa9, 1)
    for base in DISPLAY_LISTS:
        a(0x8d, base+FOOTER_OFFSET)
    a(0x8d, ENABLED)
    c.label('save')
    a(0xad, NEXT_INK); a(0x8d, INK)
    c.emit(0xa9, 0); a(0x8d, PENDING)
    c.label('done'); c.emit(0x60)
    return bytes(c.finish())


def patch_rows():
    c = Code(PATCH_ROWS)
    def a(op, addr): absolute(c, op, addr)

    c.emit(0xa0, 0)
    c.label('row')
    for part in range(2):
        a(0xbd, ROW_ADDRESSES+part*len(BITMAP_ROWS))
        for tail in TAILS:
            a(0x99, tail+3+part)
    # Four consecutive ring slots, starting at X on the selected page.
    c.emit(0xe8, 0x8a, 0x29, ROW_COUNT-1); a(0x0d, FRONT); c.emit(0xaa)
    c.emit(0x98, 0x18, 0x69, 10, 0xa8, 0xc0, 10*ROW_COUNT)
    c.branch(0x90, 'row'); c.emit(0x60)
    return bytes(c.finish())


def build():
    inserts = []
    for row in BITMAP_ROWS:
        assert row//0x1000 == (row+ROW_BYTES-1)//0x1000
        inserts.append((row, bytes(ROW_BYTES)))
    row_addresses = bytes(addr & 255 for addr in BITMAP_ROWS) + bytes(addr >> 8 for addr in BITMAP_ROWS)
    inserts.append((ROW_ADDRESSES, row_addresses))
    for base, tail in zip(DISPLAY_LISTS, TAILS):
        # Same raster height and DLI positions as the four ANTIC 4 rows.
        # Each glyph row starts with one blank scanline and fetches seven
        # packed 20-byte lines in ANTIC C.
        data = bytearray((0x90,))
        for row in range(ROW_COUNT):
            data.extend((0, 0x4c, 0, 0, *([0x0c]*(GLYPH_ROWS-1))))
        data[-1] |= 0x80
        data.extend((0x41, base & 255, base >> 8))
        assert tail//0x400 == (tail+len(data)-1)//0x400
        inserts.append((tail, data))

    trampoline = Code(UPDATE)
    trampoline.emit(0xad, 0x01, 0xd3, 0x48)  # Save the caller's PORTB.
    absolute(trampoline, 0xad, bank_value(PALETTE_BANK))
    trampoline.emit(0x8d, 0x01, 0xd3)
    absolute(trampoline, 0x20, BANK_UPDATE)
    trampoline.emit(0x68, 0x8d, 0x01, 0xd3, 0x60)
    palette = Code(PALETTE)
    absolute(palette, 0xad, INK)
    absolute(palette, 0x8d, 0xd016)
    absolute(palette, 0x4c, EXIT)
    assert PALETTE+len(palette.data) == ENABLED

    inserts.extend(((BEFORE, retire()), (UPDATE, bytes(trampoline.finish())),
                    (PALETTE, bytes(palette.finish())), (COMMIT, publish()),
                    (PATCH_ROWS, patch_rows()),
                    (ENABLED, bytes((0, 0, 0, 0xff, 0, 0, 0)))))
    return inserts, dict(before=BEFORE, update=UPDATE, commit=COMMIT,
                         enabled=ENABLED, palette=PALETTE)
