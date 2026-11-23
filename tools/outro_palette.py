"""Animate the terminal font's three scanline inks with short ANTIC DLIs."""
from build_sequence import Code

ENTRY = 0x2451
EXIT = 0x2480
RASTER_ENTRY = 0xff94
BODY_ENTRY = 0xffb8
CARD_ENTRY = 0x3c00  # Late-loaded runtime, after the shared scanline pool.
CARD_FONT_ENTRY = 0x3d20
CARD_FADE = 0x0dd5
CARD_CLOCK_PENDING = 0x80  # Also maps to the zero fade row in the DLI.
CARD_DLI_VCOUNTS = (55,63,71)
CARD_RESTORE_VCOUNT = 79
CARD_RESTORE_COLORS = (0x0e,0x9a,0x2c)
# PAL GTIA colours in rainbow order, with a different dominant ink for
# each row. One phase swaps the bright and dim scanlines for the glitch.
INK_PHASES = (
    (0x9e, 0x5a, 0x7c),  # cyan, magenta, violet
    (0x4e, 0x6a, 0x9c),  # pink, purple, cyan
    (0x8e, 0x3a, 0x5c),  # blue, red-orange, magenta
    (0x2e, 0x3a, 0x0c),  # amber, red-orange, white
    (0xbe, 0xfa, 0x2c),  # lime, gold, amber
    (0xae, 0xca, 0xfc),  # mint, green, gold
    (0x76, 0xce, 0x4e),  # glitch: dim violet, bright green and pink
    (0x6e, 0x9a, 0x8c),  # purple, cyan, blue
)
GLYPH_INKS = (0,1,2,3,1,2,3,1)
ROW_DLI_STEP = 4  # VCOUNT counts pairs of raster lines.
TICKS_PER_PHASE = 4  # One palette step per PAL frame.
LIVE_TICK = 0x24a7


def helper():
    c = Code(ENTRY)
    def a(op,address):
        c.emit(op,address&255,address>>8)

    a(0xad,0x83e0);c.emit(0xc9,17);c.branch(0xd0,'music')
    a(0xad,0x0dd0);c.emit(0xc9,2);c.branch(0xd0,'card')
    from outro_text import TEXT_DLI_VCOUNT, BODY_DLI_VCOUNT
    a(0xad,0xd40b);c.emit(0xc9,TEXT_DLI_VCOUNT);c.branch(0x90,'top_music')
    c.emit(0xc9,BODY_DLI_VCOUNT);c.branch(0x90,'text')
    c.emit(0xc9,BODY_DLI_VCOUNT+3);c.branch(0xb0,'music')
    a(0x4c,BODY_ENTRY)
    # The foreground snapshot can hold while a new page is being typed.
    # Read the live clock, which stays constant across the text DLIs.
    c.label('text');a(0xad,LIVE_TICK);a(0x4c,RASTER_ENTRY)
    # Preserve the opening music DLI's WSYNC timing.
    c.label('top_music');c.emit(0xa0,4)
    c.label('top_delay');c.emit(0x88);c.branch(0xd0,'top_delay')
    c.label('music');a(0x8d,0xd40a);c.emit(0x60)
    assert c.origin+len(c.data)<=EXIT
    c.emit(*bytes(EXIT-c.origin-len(c.data)))
    # Discard the router's JSR return and restore NMI-saved Y/X/A.
    c.emit(0x68,0x68,0x68,0xa8,0x68,0xaa,0x68,0x40)
    c.label('card');a(0x4c,CARD_ENTRY)
    result = bytes(c.finish())
    assert ENTRY+len(result)<=0x249c
    return result


def card_inks(level, phase):
    return tuple(((ink&0xf0) | (2*round((ink&14)*level/14))) if level else 0
                 for ink in INK_PHASES[phase])


def card_helper():
    c = Code(CARD_ENTRY)
    def a(op,address):
        c.emit(op,address&255,address>>8)

    c.emit(0xc9,3);c.branch(0xd0,'music')
    a(0xad,0xd40b);c.emit(0xc9,CARD_DLI_VCOUNTS[0]-1);c.branch(0x90,'music')
    c.emit(0xc9,CARD_RESTORE_VCOUNT+2);c.branch(0xb0,'music')
    c.emit(0xc9,CARD_RESTORE_VCOUNT-1);c.branch(0xb0,'restore')
    # The card counter keeps running after the final music packet.
    c.emit(0x4a,0x18);a(0x6d,0x24aa);c.emit(0x4a,0x4a,0x29,7)
    c.jump(0x8d,'phase')
    a(0xad,CARD_FADE);c.emit(0x0a,0x0a)
    c.label('combine');c.emit(0x09,0,0xaa)
    c.labels['phase']=c.labels['combine']+1
    for pen in range(3):
        c.jump(0xbd,f'card_ink{pen}');a(0x8d,0xd016+pen)
    a(0x4c,EXIT)
    c.label('restore')
    for pen,ink in enumerate(CARD_RESTORE_COLORS):
        c.emit(0xa9,ink);a(0x8d,0xd016+pen)
    a(0x4c,EXIT)
    c.label('music');a(0x8d,0xd40a);c.emit(0x60)

    palettes = [card_inks(level,phase) for level in range(8) for phase in range(8)]
    for pen in range(3):
        c.label(f'card_ink{pen}');c.emit(*(palette[pen] for palette in palettes))
    return bytes(c.finish())


def card_font_copy():
    from outro_text import COLOR_FONT, FONT

    c = Code(CARD_FONT_ENTRY)
    c.emit(0xa2,0)
    c.label('copy')
    for page in (1,2):
        c.emit(0xbd,0,(COLOR_FONT>>8)+page,0x9d,0,(FONT>>8)+page)
    c.emit(0xe8);c.branch(0xd0,'copy');c.emit(0x60)
    return bytes(c.finish())


def raster_helper():
    c = Code(RASTER_ENTRY)
    def a(op,address):
        c.emit(op,address&255,address>>8)

    # Add the music phase in VCOUNT units, then divide by the row height.
    assert TICKS_PER_PHASE == ROW_DLI_STEP
    c.emit(0x29,(len(INK_PHASES)-1)*TICKS_PER_PHASE,0x18)
    a(0x6d,0xd40b)
    c.emit(0x4a,0x4a,0x29,7,0xaa)
    # The first raster of each glyph is blank so this can run through the
    # row boundary without waiting on WSYNC during character DMA.
    for pen in range(3):
        c.jump(0xbd,f'ink{pen}');a(0x8d,0xd016+pen)
    a(0x4c,EXIT)
    assert c.origin+len(c.data)<=BODY_ENTRY
    c.emit(*bytes(BODY_ENTRY-c.origin-len(c.data)))

    from final_boy import PORTRAIT_LUMA
    a(0xad,PORTRAIT_LUMA);c.emit(0xea,0xaa);a(0x8d,0xd40a);c.branch(0xf0,'dark')
    c.emit(0x09,0x40);a(0x8d,0xd016)
    c.emit(0x8a,0x09,0x90);a(0x8d,0xd017)
    c.emit(0x8a,0x09,0x20);a(0x8d,0xd018);a(0x4c,EXIT)
    c.label('dark')
    for pen in range(3):
        a(0x8d,0xd016+pen)
    a(0x4c,EXIT)
    from outro_text import TEXT_DLI_VCOUNT
    # Rotate the lookup so the leading blank DLI selects the music phase.
    lead_offset = TEXT_DLI_VCOUNT // ROW_DLI_STEP
    indexed_phases = INK_PHASES[-lead_offset:] + INK_PHASES[:-lead_offset]
    for pen, phases in enumerate(zip(*indexed_phases)):
        c.label(f'ink{pen}')
        c.emit(*phases)
    result = bytes(c.finish())
    assert RASTER_ENTRY+len(result)<=0xfffa
    return result
