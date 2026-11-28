"""Keep write-only playfield inks available for the text raster split."""

from build_sequence import Code

INK_BASE = 0xd016
WRITERS = 0xdac0
WRITER_BYTES = 7
SHADOW = 0xdad5
RESTORE = 0xdad8
ROUTER = 0xdbc0


def emit(c, opcode, address):
    if opcode == 0x8d and INK_BASE <= address < INK_BASE+3:
        address = WRITERS + WRITER_BYTES*(address-INK_BASE)
        opcode = 0x20
    c.emit(opcode, address & 255, address >> 8)


def inserts(active_address, palette_address, water_address):
    from outro_palette import ENTRY
    from outro_text import TEXT_DLI_VCOUNT

    writers = bytearray()
    for pen in range(3):
        writers.extend((0x8d, (SHADOW+pen)&255, SHADOW>>8,
                        0x8d, (INK_BASE+pen)&255, INK_BASE>>8, 0x60))
    assert WRITERS + len(writers) == SHADOW
    writers.extend((0x0e, 0x0e, 0x82))  # Player power-on colors.
    assert WRITERS + len(writers) == RESTORE
    for pen in range(3):
        writers.extend((0xad, (SHADOW+pen)&255, SHADOW>>8,
                        0x8d, (INK_BASE+pen)&255, INK_BASE>>8))
    writers.append(0x60)
    assert WRITERS+len(writers) <= 0xdb00

    c = Code(ROUTER)

    def a(op, addr):
        c.emit(op,addr&255,addr>>8)

    a(0xad, active_address)
    c.branch(0xf0, 'no_caption')
    a(0xad, 0xd40b)
    c.emit(0xc9, 8)
    c.branch(0x90, 'restore')
    c.emit(0xc9, TEXT_DLI_VCOUNT)
    c.branch(0x90, 'music')
    c.emit(0xc9, TEXT_DLI_VCOUNT+2)
    c.branch(0xb0, 'music')
    a(0x4c, palette_address)
    c.label('restore')
    # The top blank DLI restores the picture inks before its first line.
    a(0x20, RESTORE)
    c.label('music')
    a(0x8d, 0xd40a)
    c.emit(0x60)
    c.label('no_caption')
    a(0xad, 0x83e0)
    c.emit(0xc9, 2)
    c.branch(0xb0, 'outro')
    a(0x4c, water_address)
    c.label('outro')
    a(0x4c, ENTRY)
    assert ROUTER+len(c.data) <= 0xdc00
    return [(WRITERS, bytes(writers)), (ROUTER, bytes(c.finish()))]
