"""Keep the write-only PF0 ink available for the text raster split."""

from build_sequence import Code

INK_BASE = 0xd016
WRITERS = 0xdac0
SHADOW = 0xdad5
RESTORE = 0xdad8
ROUTER = 0xdbc0


def emit(c, opcode, address):
    if opcode == 0x8d and address == INK_BASE:
        address = WRITERS
        opcode = 0x20
    c.emit(opcode, address & 255, address >> 8)


def inserts(active_address, palette_address, water_address):
    from outro_palette import ENTRY
    from outro_text import TEXT_DLI_VCOUNT

    write = bytes((0x8d, SHADOW&255, SHADOW>>8, 0x8d, INK_BASE&255, INK_BASE>>8, 0x60))
    restore = bytes((0xad, SHADOW&255, SHADOW>>8, 0x8d, INK_BASE&255, INK_BASE>>8, 0x60))

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
    return [(WRITERS, write), (SHADOW, b'\x0e'), (RESTORE, restore), (ROUTER, bytes(c.finish()))]
