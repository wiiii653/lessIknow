"""Render the runtime opening in framebuffer RAM before entering the player."""

from build_sequence import Code
from dance_banks import FRAME_BASES
from final_boy import MARK_BANK, MARK_FRAMES, MARK_FRAMES_PER_BANK
from outro_text import (
    FINAL_MARK_FIRST_GLYPH, FINAL_MARK_PHASES, FINAL_MARK_ROWS, FINAL_MARK_WIDTH,
    color_font, final_mark,
)
from school_portrait_bank import bank_value
from outro_palette import fade_inks

FONT = FRAME_BASES[0]
SCREEN = FONT + 0x400
TEXT = SCREEN + FINAL_MARK_ROWS * 40
TEXT_BYTES = 4 * 40
PAGE_ADDRESS = FONT + 0x600
ENTRY = FONT + 0x800
CLEANUP = 0xfd92
PAGE_SWITCH = 144
FADE_START = 288
HOLD_FRAMES = 320
COLORS = (0x0e, 0x9a, 0x2c)
PAGE_INKS = ((0x9e, 0x7c, 0x4e), (0xae, 0x3c, 0x2e))
PAGES = (
    ('SYS.OPEN BEGIN.SYS [OK]', 'THE LESS I KNOW THE BETTER',
     'TAME IMPALA / ATARI XE 1 MB', 'LOADING TITLE...'),
    ('CITY PANORAMA', 'SILLY VENTURE 2026'),
)


def page_bytes(lines):
    rows = tuple('> ' + line for line in lines)
    assert len(rows) <= 4 and all(len(row) <= 39 for row in rows)
    return b''.join(row.encode('ascii').ljust(40) for row in
                    (*rows, *('',) * (4 - len(rows))))


def framebuffer(music_nmi):
    """Supply startup data inside the existing first framebuffer segment."""
    data = bytearray(0x1f00)
    font = color_font()
    for page in PAGES:
        for char in page_bytes(page):
            offset = (char - 32) * 8
            assert 32 <= char < 96 and (char == 32 or any(font[offset:offset+8]))
    data[0x100:0x100+len(font)] = font
    tiles, _ = final_mark(0)
    for row in range(FINAL_MARK_ROWS):
        start = SCREEN - FONT + row * 40 + (40 - FINAL_MARK_WIDTH) // 2
        data[start:start+FINAL_MARK_WIDTH] = bytes(
            tiles[row * FINAL_MARK_WIDTH:(row + 1) * FINAL_MARK_WIDTH])
    for index, page in enumerate(PAGES):
        offset = PAGE_ADDRESS - FONT + index * 256
        data[offset:offset+TEXT_BYTES] = page_bytes(page)
    code = helper(music_nmi)
    offset = ENTRY - FONT
    data[offset:offset+len(code)] = code
    return data


def helper(music_nmi):
    c = Code(ENTRY)

    def absolute(opcode, address):
        c.emit(opcode, address & 255, address >> 8)

    def set_byte(address, value):
        c.emit(0xa9, value)
        absolute(0x8d, address)

    set_byte(0xd409, FONT >> 8)
    c.jump(0xad, 'list_lo')
    absolute(0x8d, 0xd402)
    c.jump(0xad, 'list_hi')
    absolute(0x8d, 0xd403)
    for register, label in ((0xfffa, 'nmi_lo'), (0xfffb, 'nmi_hi')):
        c.jump(0xad, label)
        absolute(0x8d, register)

    c.label('frame')
    c.jump(0x20, 'next_blank')
    c.jump(0xad, 'frame_hi')
    c.branch(0xf0, 'first_256')
    c.jump(0xad, 'frame_lo')
    c.emit(0xc9, HOLD_FRAMES & 255)
    c.branch(0xf0, 'done')
    c.branch(0xd0, 'draw')
    c.label('first_256')
    c.jump(0xad, 'frame_lo')
    c.emit(0xc9, PAGE_SWITCH)
    c.branch(0xd0, 'draw')

    c.emit(0xa9, (PAGE_ADDRESS >> 8) + 1)
    c.jump(0x8d, 'read_page_hi')
    c.emit(0xa9, 0)
    c.jump(0x8d, 'text_index')
    c.emit(0xa2, TEXT_BYTES - 1)
    c.label('clear_text')
    absolute(0x9d, TEXT)
    c.emit(0xca, 0xe0, 0xff)
    c.branch(0xd0, 'clear_text')

    c.label('draw')
    c.jump(0x20, 'mark')
    c.jump(0x20, 'text')
    c.jump(0x20, 'palette')
    set_byte(0xd40e, 0x80)  # The opening has only palette NMIs.
    set_byte(0xd400, 0x22)
    c.jump(0xee, 'frame_lo')
    c.branch(0xd0, 'frame')
    c.jump(0xee, 'frame_hi')
    c.jump(0x4c, 'frame')
    c.label('done')
    set_byte(0xd40e, 0)
    set_byte(0xfffa, music_nmi & 255)
    set_byte(0xfffb, music_nmi >> 8)
    absolute(0x4c, CLEANUP)

    c.label('next_blank')
    absolute(0xad, 0xd40b)
    c.emit(0xc9, 124)
    c.branch(0xb0, 'next_blank')
    c.label('wait_blank')
    absolute(0xad, 0xd40b)
    c.emit(0xc9, 124)
    c.branch(0x90, 'wait_blank')
    c.emit(0x60)

    c.label('mark')
    absolute(0xad, 0xd301)
    c.emit(0x48)
    c.jump(0xad, 'frame_lo')
    c.emit(0x29, FINAL_MARK_PHASES - 1, 0xaa,
           0x29, MARK_FRAMES_PER_BANK - 1, 0x09, MARK_FRAMES >> 8)
    c.jump(0x8d, 'read_mark_hi')
    c.emit(0x8a, 0x4a, 0x4a, 0x4a, 0xaa)
    absolute(0xbd, bank_value(MARK_BANK))
    absolute(0x8d, 0xd301)
    c.emit(0xa2, FINAL_MARK_ROWS * FINAL_MARK_WIDTH * 8 - 1)
    c.label('copy_glyphs')
    c.label('read_mark')
    absolute(0xbd, MARK_FRAMES)
    absolute(0x9d, FONT + FINAL_MARK_FIRST_GLYPH * 8)
    c.emit(0xca, 0xe0, 0xff)
    c.branch(0xd0, 'copy_glyphs')
    c.emit(0x68)
    absolute(0x8d, 0xd301)
    c.emit(0x60)

    c.label('text')
    c.jump(0xae, 'text_index')
    c.emit(0xe0, TEXT_BYTES)
    c.branch(0xf0, 'text_done')
    c.emit(0xa0, 2)  # Two columns per frame, including the spaces at line ends.
    c.label('type_char')
    c.label('read_page')
    absolute(0xbd, PAGE_ADDRESS)
    absolute(0x9d, TEXT)
    c.emit(0xe8, 0x88)
    c.branch(0xd0, 'type_char')
    c.jump(0x8e, 'text_index')
    c.label('text_done')
    c.emit(0x60)

    c.label('palette')
    c.emit(0xa2, 0)
    c.jump(0xad, 'frame_hi')
    c.branch(0xf0, 'set_colors')
    c.jump(0xad, 'frame_lo')
    c.emit(0xc9, FADE_START & 255)
    c.branch(0x90, 'set_colors')
    c.emit(0xe9, FADE_START & 255, 0xaa)
    c.label('set_colors')
    for pen in range(3):
        c.jump(0xbd, f'color_{pen}')
        absolute(0x8d, 0xd016 + pen)
    # X holds the star fade step. The typed page selects a fixed ink set.
    c.emit(0x8a, 0x4a, 0x4a, 0x49, 7, 0xaa)
    c.jump(0xad, 'read_page_hi')
    c.emit(0xc9, PAGE_ADDRESS >> 8)
    c.branch(0xf0, 'first_inks')
    c.emit(0x8a, 0x09, 8)
    c.branch(0xd0, 'ink_index')
    c.label('first_inks')
    c.emit(0x8a)
    c.label('ink_index')
    c.jump(0x8d, 'text_ink_index')
    c.emit(0x60)

    c.label('text_nmi')
    c.emit(0x48, 0x8a, 0x48)
    c.jump(0xae, 'text_ink_index')
    for pen in range(3):
        c.jump(0xbd, f'text_inks{pen}')
        absolute(0x8d, 0xd016+pen)
    c.emit(0x68, 0xaa, 0x68, 0x40)

    c.labels['read_mark_hi'] = c.labels['read_mark'] + 2
    c.labels['read_page_hi'] = c.labels['read_page'] + 2
    for name in ('frame_lo', 'frame_hi', 'text_index', 'text_ink_index'):
        c.label(name)
        c.emit(0)
    for pen, color in enumerate(COLORS):
        c.label(f'color_{pen}')
        for step in range(HOLD_FRAMES - FADE_START):
            level = ((color & 14) // 2) * (31 - step) // 31
            c.emit((color & 0xf0) | (2 * level) if level else 0)
    palettes = [fade_inks(level, inks) for inks in PAGE_INKS for level in range(8)]
    for pen in range(3):
        c.label(f'text_inks{pen}')
        c.emit(*(inks[pen] for inks in palettes))
    c.label('nmi_lo')
    c.emit(c.labels['text_nmi'] & 255)
    c.label('nmi_hi')
    c.emit(c.labels['text_nmi'] >> 8)

    # Match the loader's mark position and the credits' terminal position.
    c.label('list_lo')
    c.emit((c.origin + len(c.data) + 2) & 255)
    c.label('list_hi')
    c.emit((c.origin + len(c.data) + 1) >> 8)
    display = c.origin + len(c.data)
    c.emit(0x70, 0x70, 0x70, 0x45, SCREEN & 255, SCREEN >> 8, 0x05, 0x05)
    c.emit(*([0x70] * 16), 0xa0)
    for row in range(4):
        address = TEXT + 40 * row
        c.emit(0x44, address & 255, address >> 8)
    c.emit(0x41, display & 255, display >> 8)
    assert c.origin // 0x400 == (c.origin + len(c.data) - 1) // 0x400
    return bytes(c.finish())


def cleanup(player_entry):
    """Blank the display and restore the framebuffer before music starts."""
    c = Code(CLEANUP)
    c.emit(0xa9, 0, 0x8d, 0x00, 0xd4, 0xa2, 0)
    c.label('clear')
    for address in range(FONT, ENTRY + 0x400, 256):
        c.emit(0x9d, 0, address >> 8)
    c.emit(0xe8)
    c.branch(0xd0, 'clear')
    # PF0 has the same color as on entry from the full-rate loader.
    c.emit(0xa9, COLORS[0], 0x8d, 0x16, 0xd0)
    c.emit(0x4c, player_entry & 255, player_entry >> 8)
    return bytes(c.finish())
