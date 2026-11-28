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
ROW_BYTES = 40
TEXT_BYTES = 4 * ROW_BYTES
TYPING_ROW = TEXT + TEXT_BYTES - ROW_BYTES
SCRIPT_ADDRESS = FONT + 0x600
ENTRY = FONT + 0x800
CLEANUP = 0xfd92
TYPE_STEP = 4
FADE_START = 896
HOLD_FRAMES = 928
COLORS = (0x0e, 0x9a, 0x2c)
TEXT_INKS = (0x9e, 0x7c, 0x4e)
ENTER = 1
CURSOR = ord('_')
AUDF1, AUDC1 = 0xd200, 0xd201
KEY_TONE = 0xa2
KEY_DIVISOR = 26
TRANSCRIPT = (
    (12, 'TWO WEEKS PASSED AND THINGS HAVE'),
    (160, 'CHANGED. THIS IS THE FINAL RELEASE'),
    (320, 'OF THE DEMO.'),
    (444, '> REVIEW THE FINAL BUILD'),
    (584, 'AGENT: CHECKING SCENE CUES.'),
    (724, 'I WILL TRACE THE FRAME HANDOFFS.'),
)


def typing_script():
    assert HOLD_FRAMES % TYPE_STEP == 0 and HOLD_FRAMES//TYPE_STEP <= 256
    script = bytearray(HOLD_FRAMES//TYPE_STEP)
    starts = tuple(frame for frame, _ in TRANSCRIPT)
    for (start, line), end in zip(TRANSCRIPT, (*starts[1:], FADE_START)):
        glyphs = line.encode('ascii')
        assert start % TYPE_STEP == 0 and len(glyphs) < ROW_BYTES
        assert start + TYPE_STEP*(len(glyphs)+1) < end
        slot = start//TYPE_STEP
        script[slot] = ENTER
        script[slot+1:slot+1+len(glyphs)] = glyphs
    assert SCRIPT_ADDRESS + len(script) <= ENTRY
    return script


def framebuffer(music_nmi):
    """Supply startup data inside the existing first framebuffer segment."""
    data = bytearray(0x1f00)
    font = color_font()
    script = typing_script()
    for char in ({code for code in script if code > ENTER} | {CURSOR}) - {32}:
        offset = (char - 32) * 8
        assert 32 <= char < 96 and any(font[offset:offset+8])
    data[TEXT-FONT:TEXT-FONT+TEXT_BYTES] = b' ' * TEXT_BYTES
    data[0x100:0x100+len(font)] = font
    tiles, _ = final_mark(0)
    for row in range(FINAL_MARK_ROWS):
        start = SCREEN - FONT + row * 40 + (40 - FINAL_MARK_WIDTH) // 2
        data[start:start+FINAL_MARK_WIDTH] = bytes(
            tiles[row * FINAL_MARK_WIDTH:(row + 1) * FINAL_MARK_WIDTH])
    offset = SCRIPT_ADDRESS - FONT
    data[offset:offset+len(script)] = script
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
    set_byte(AUDF1, KEY_DIVISOR)
    set_byte(AUDC1, 0)

    c.label('frame')
    c.jump(0x20, 'next_blank')
    c.jump(0xad, 'frame_hi')
    c.emit(0xc9,HOLD_FRAMES >> 8)
    c.branch(0xd0, 'draw')
    c.jump(0xad, 'frame_lo')
    c.emit(0xc9, HOLD_FRAMES & 255)
    c.branch(0xf0, 'done')

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
    set_byte(AUDC1, 0)
    set_byte(AUDF1, 0)
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
    # Erase the old cursor before a keystroke or the Enter scroll.
    c.jump(0xae, 'column')
    c.emit(0xa9, 32);absolute(0x9d, TYPING_ROW)
    assert TYPE_STEP == 4
    c.jump(0xad, 'frame_lo');c.emit(0x29, TYPE_STEP-1);c.branch(0xd0, 'cursor')
    # Divide the frame counter by four to address the compact script page.
    c.jump(0xad, 'frame_hi');c.emit(*([0x0a]*6));c.jump(0x8d, 'slot_high')
    c.jump(0xad, 'frame_lo');c.emit(0x4a,0x4a);c.jump(0x0d, 'slot_high');c.emit(0xa8)
    absolute(0xb9, SCRIPT_ADDRESS)
    c.branch(0xf0, 'cursor')
    c.emit(0xc9, ENTER);c.branch(0xd0, 'type_char')
    c.emit(0xa2, 0)
    c.label('scroll')
    absolute(0xbd, TEXT+ROW_BYTES);absolute(0x9d, TEXT)
    c.emit(0xe8, 0xe0, TEXT_BYTES-ROW_BYTES);c.branch(0xd0, 'scroll')
    c.emit(0xa2, ROW_BYTES-1, 0xa9, 32)
    c.label('clear_row');absolute(0x9d, TYPING_ROW)
    c.emit(0xca);c.branch(0x10, 'clear_row')
    c.emit(0xa2, 0);c.jump(0x8e, 'column')
    c.emit(0xe8);c.jump(0x8e, 'started')
    c.jump(0x4c, 'cursor')
    c.label('type_char')
    absolute(0x9d, TYPING_ROW)
    c.emit(0xe8);c.jump(0x8e, 'column')
    set_byte(AUDC1, KEY_TONE)
    c.label('cursor')
    c.jump(0xad, 'started');c.branch(0xf0, 'text_done')
    c.jump(0xad, 'frame_lo');c.emit(0x29, 16);c.branch(0xd0, 'text_done')
    c.jump(0xae, 'column')
    c.emit(0xa9, CURSOR);absolute(0x9d, TYPING_ROW)
    c.label('text_done')
    c.emit(0x60)

    c.label('palette')
    c.emit(0xa2, 0)
    c.jump(0xad, 'frame_hi')
    c.emit(0xc9, FADE_START >> 8)
    c.branch(0xd0, 'set_colors')
    c.jump(0xad, 'frame_lo')
    c.emit(0xc9, FADE_START & 255)
    c.branch(0x90, 'set_colors')
    c.emit(0xe9, FADE_START & 255, 0xaa)
    c.label('set_colors')
    for pen in range(3):
        c.jump(0xbd, f'color_{pen}')
        absolute(0x8d, 0xd016 + pen)
    # X holds the star fade step. Text fades on the same envelope.
    c.emit(0x8a, 0x4a, 0x4a, 0x49, 7)
    c.jump(0x8d, 'text_ink_index')
    c.emit(0x60)

    c.label('text_nmi')
    c.emit(0x48, 0x8a, 0x48)
    c.jump(0xae, 'text_ink_index')
    for pen in range(3):
        c.jump(0xbd, f'text_inks{pen}')
        absolute(0x8d, 0xd016+pen)
    # End the key pulse before displaying the text. The music NMI takes
    # over only after the opener has explicitly muted this channel.
    set_byte(AUDC1, 0)
    c.emit(0x68, 0xaa, 0x68, 0x40)

    c.labels['read_mark_hi'] = c.labels['read_mark'] + 2
    for name in ('frame_lo', 'frame_hi', 'column', 'started', 'slot_high', 'text_ink_index'):
        c.label(name)
        c.emit(0)
    for pen, color in enumerate(COLORS):
        c.label(f'color_{pen}')
        for step in range(HOLD_FRAMES - FADE_START):
            level = ((color & 14) // 2) * (31 - step) // 31
            c.emit((color & 0xf0) | (2 * level) if level else 0)
    palettes = [fade_inks(level, TEXT_INKS) for level in range(8)]
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
