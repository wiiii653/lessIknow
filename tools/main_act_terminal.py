"""Four ANTIC 4 caption rows under the main act bitmaps."""

from build_sequence import Code, DANCE_TICK
from music_timing import tick_at_bar
from outro_text import START as CREDITS_START, GLYPHS, TERMINAL_FONT
from outro_palette import EXIT, GLYPH_INKS
from gym_practice import PRACTICE_TICK
from ribbon_dance import START as RIBBON_START
from basketball_hero import CUTAWAY_START, START as DUNK_START, END as TREVOR_START
from post_trevor_director import FIRST_ROTATOR, LATE_BANANA_START, START as MONTAGE_START

FONT = 0xd800
SCREENS = (0xda20, 0xdb20)
ENTRY = 0xdc00
LIMIT = 0xe240
WIDTH = 40
ROW_COUNT = 4
FOOTER_OFFSET = 2 + 192 * 3
DISPLAY_LISTS = (0x8000, 0x8400)
TICK = 0x83e2
SCHOOL_START = tick_at_bar(8)
CUES = (SCHOOL_START, PRACTICE_TICK, DANCE_TICK, FIRST_ROTATOR, RIBBON_START,
        CUTAWAY_START, DUNK_START, TREVOR_START, MONTAGE_START, LATE_BANANA_START)
CAPTIONS = (
    ('SCHOOL / ARRIVAL', 'SHE PASSES. HE WHISTLES.', 'THE LESS I KNOW THE BETTER'),
    ('PRACTICE / GYM', 'HE SHOOTS. HE MISSES.', 'THE BALL NEVER LIES.'),
    ('RIBBON DANCE / TRIO', 'THREE GIRLS. ONE BEAT.', 'HOLD THE POSE.'),
    ('BANANA ROTO-ZOOM', 'SPIRAL. ORGANIC. REPEAT.', 'THE FRUIT IS A PORTAL.'),
    ('RIBBON DANCE / SOLO', 'HALF-BEAT POSES', 'SMOOTH INBETWEENS'),
    ('TUNNEL / CUTAWAY', 'THE DIRECTOR CUTS.', 'NEXT: THE DUNK.'),
    ('HERO / DUNK', 'FOUR SATELLITES', 'GLASS ON FIRST CRACK'),
    ('TREVOR / 13 HITS', 'HE TAKES THE BALLS.', 'HE KEEPS COMING.'),
    ('BANANAS / TUNNELS', '32 PASSAGES', 'A CUT EACH BAR'),
    ("GIRL'S EYES", 'BANANAS BEFORE / AFTER', 'BUM / BAM'),
)
# Three fixed inks give every glyph the scanline stripes from the greetings.
# Keep one palette per caption so cuts within an act share the same colors.
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


def resources():
    pages = [(f'SYS.OPEN SCENE {i:02d} [OK]', *lines)
             for i, lines in enumerate(CAPTIONS, 1)]
    charset = sorted(set(''.join(line for page in pages for line in page) + '>'))
    assert len(charset) < 64
    codes = {char: index for index, char in enumerate(charset, 1)}
    # Match the scanline inks and leading blank raster of the credits font.
    glyphs = bytearray(8)
    for char in charset:
        if char in TERMINAL_FONT:
            rows = TERMINAL_FONT[char].split()
        else:
            rows = [''.join(row[i] for i in (0, 2, 4)) for row in GLYPHS[char]]
        for row, ink in enumerate(GLYPH_INKS):
            glyphs.append(sum(ink << (6 - 2 * i)
                              for i, bit in enumerate(rows[max(0, row-1)])
                              if bit == '1'))
    records = []
    for cue, end, page in zip(CUES, (*CUES[1:], CREDITS_START), pages):
        assert len(page) == ROW_COUNT and all(len(line) <= 37 for line in page)
        record = b''.join(bytes(codes[char] for char in '> ' + line) + b'\0'
                          for line in page)
        assert (len(record) - ROW_COUNT) * 4 < end - cue
        records.append(record)
    return bytes(glyphs), records


def build():
    glyphs, records = resources()
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
    c.jump(0x8d, 'shown_page')
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
    c.jump(0x8e, 'next_page')
    c.emit(0x38)
    a(0xad, TICK)
    c.jump(0xfd, 'cue_lo')
    c.emit(0xa8)
    a(0xad, TICK+1)
    c.jump(0xfd, 'cue_hi')
    c.branch(0xd0, 'full')
    c.emit(0x98, 0x4a, 0x4a, 0x18, 0x69, 1)
    c.jump(0x4c, 'count')
    c.label('full')
    c.emit(0xa9, 0xff)
    c.label('count')
    c.jump(0xdd, 'page_len')
    c.branch(0x90, 'count_ok')
    c.jump(0xbd, 'page_len')
    c.label('count_ok')
    c.jump(0x8d, 'count_next')
    c.jump(0x8d, 'count_copy')
    c.jump(0xec, 'shown_page')
    c.branch(0xd0, 'changed')
    c.jump(0xcd, 'shown_count')
    c.branch(0xd0, 'changed')
    c.emit(0x60)
    c.label('changed')
    c.jump(0xbd, 'page_lo')
    c.jump(0x8d, 'read_char_lo')
    c.jump(0xbd, 'page_hi')
    c.jump(0x8d, 'read_char_hi')
    c.jump(0xad, 'front_hi')
    c.emit(0x49, 1)
    for operand in ('clear_hi', 'write_char_hi'):
        c.jump(0x8d, operand)
    c.emit(0xa9, 0, 0xa2, WIDTH*ROW_COUNT-1)
    c.label('clear')
    a(0x9d, SCREENS[0])
    c.emit(0xca, 0xe0, 0xff)
    c.branch(0xd0, 'clear')
    c.emit(0xa2, 0, 0xa0, 0, 0xa9, 0)
    c.jump(0x8d, 'row')
    c.label('load_char')
    c.label('read_char')
    a(0xbd, 0)
    c.branch(0xf0, 'next_row')
    c.label('write_char')
    a(0x99, SCREENS[0])
    c.emit(0xc8, 0xe8)
    c.jump(0xce, 'count_next')
    c.branch(0xd0, 'load_char')
    c.branch(0xf0, 'ready')
    c.label('next_row')
    c.emit(0xe8)
    c.jump(0xee, 'row')
    c.jump(0xac, 'row')
    c.jump(0xb9, 'row_offset')
    c.emit(0xa8)
    c.jump(0x4c, 'load_char')

    c.label('ready')
    c.jump(0xee, 'pending')
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
    c.jump(0xad, 'next_page')
    c.jump(0x8d, 'shown_page')
    c.jump(0xad, 'count_copy')
    c.jump(0x8d, 'shown_count')
    c.emit(0xa9, 0)
    c.jump(0x8d, 'pending')
    c.label('commit_done')
    c.emit(0x60)

    # The blank line before the strip establishes its three inks once per
    # frame. The published page determines the palette for every text row.
    c.label('palette')
    c.jump(0xae, 'shown_page')
    for pen in range(3):
        c.jump(0xbd, f'ink_{pen}')
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
    c.label('blank')
    a(0xad, 0xd40b)
    c.emit(0xc9, 124)
    c.branch(0x90, 'blank')
    c.emit(0xc9, 128)
    c.branch(0xb0, 'blank')
    c.emit(0x60)

    for label, address in (('read_char_lo', 'read_char'), ('read_char_hi', 'read_char'),
                           ('write_char_hi', 'write_char'), ('clear_hi', 'clear')):
        c.labels[label] = c.labels[address] + (1 if label.endswith('lo') else 2)
    for label, value in (('enabled', 0), ('front_hi', SCREENS[0] >> 8),
                         ('shown_page', 0xff), ('shown_count', 0),
                         ('next_page', 0), ('count_next', 0), ('count_copy', 0),
                         ('row', 0), ('pending', 0)):
        c.label(label)
        c.emit(value)
    for index, base in enumerate(DISPLAY_LISTS):
        tail = c.origin + len(c.data)
        c.data[c.labels[f'tail_{index}_0']] = tail & 255
        c.data[c.labels[f'tail_{index}_1']] = tail >> 8
        c.emit(0x90, 0x44, SCREENS[0] & 255)
        c.label(f'text_hi_{index}')
        c.emit(0, 0x04, 0x04, 0x84, 0x41, base & 255, base >> 8)
        assert (tail & 0x3ff) + 10 <= 0x400
    for pen, inks in enumerate(zip(*PALETTES)):
        c.label(f'ink_{pen}')
        c.emit(*inks)
    c.label('row_offset')
    c.emit(*(row * WIDTH for row in range(ROW_COUNT)))
    for name, values in (('cue_lo', (tick & 255 for tick in CUES)),
                         ('cue_hi', (tick >> 8 for tick in CUES)),
                         ('page_len', (len(record)-ROW_COUNT for record in records))):
        c.label(name)
        c.emit(*values)
    for part in ('lo', 'hi'):
        c.label('page_' + part)
        for index in range(len(records)):
            c.emit(0)
    for index, record in enumerate(records):
        address = c.origin + len(c.data)
        c.data[c.labels['page_lo']-c.origin+index] = address & 255
        c.data[c.labels['page_hi']-c.origin+index] = address >> 8
        c.emit(*record)

    code = bytes(c.finish())
    assert FONT + len(glyphs) <= SCREENS[0]
    assert ENTRY + len(code) <= LIMIT, hex(ENTRY + len(code))
    return [(FONT, glyphs), *((screen, bytes(WIDTH*ROW_COUNT)) for screen in SCREENS),
            (ENTRY, code)], c.labels
