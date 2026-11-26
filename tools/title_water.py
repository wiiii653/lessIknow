"""Draw and publish the title's procedural reflection in title-owned RAM."""

from build_sequence import Code

TEMPLATES = 0x4430
FOOTER_ENTRY = 0x5468
TABLES = 0x54b0
ENTRY = 0x6638
RETIRE_ENTRY = 0x3c80
STATE = 0x83e0
ROW_BYTES = 40
ROW_COUNT = 11
PIXELS_OFFSET = 0x0b00
TAIL_OFFSET = 0x0d00
FOOTER_OFFSET = 2 + 192 * 3
# The title draws into $9000 when the inactive display list is $8400.
BUFFER_PAIRS = ((0x8400, 0x9000), (0x8000, 0xb000))
TAIL_SIZE = ROW_COUNT * 9 + 4

# Spread each new group of streaks across the width of the water.
COLUMNS = tuple(sorted(range(1, 39), key=lambda column: (column * 17) % 41))
MIDDLE_COLUMNS = tuple(sorted(range(1, 39), key=lambda column: (column * 13 + 5) % 43))
RIPPLE = (0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, -1, -1, -1, -1, -1)
GLINTS = {3: 0xf0, 7: 0x0f, 10: 0xf0}
FIRST_FADE_OUT_PHASE = 39
LAST_FADE_OUT_PHASE = 46


def tail(display, framebuffer):
    data = bytearray()
    for row in range(ROW_COUNT):
        pixels = framebuffer + PIXELS_OFFSET + row * ROW_BYTES
        assert pixels // 0x1000 == (pixels + ROW_BYTES - 1) // 0x1000
        sources = (pixels, pixels, pixels)
        if row < 2:
            # A thin echo of the facade catches the ripple beside the quay.
            sources = (pixels, framebuffer + (62-row) * ROW_BYTES, pixels)
        for source in sources:
            data.extend((0x4f, source & 255, source >> 8))
    data.extend((0x80, 0x41, display & 255, display >> 8))
    assert len(data) == TAIL_SIZE
    assert (framebuffer + TAIL_OFFSET) % 0x400 + len(data) <= 0x400
    return bytes(data)


def templates():
    return b''.join(tail(display, framebuffer) for display, framebuffer in BUFFER_PAIRS)


def tables():
    return bytes((*MIDDLE_COLUMNS, 0, ROW_BYTES-1,
                  *(value & 255 for value in RIPPLE + RIPPLE[:ROW_COUNT-1]),
                  *(round(len(COLUMNS) * level / 8) for level in range(9))))


def reflection(level, phase, plasma):
    """Reference for byte-packed mirror, ripple and dissolve."""
    result = bytearray()
    count = round(len(COLUMNS) * level / 8)
    for row in range(ROW_COUNT):
        order = MIDDLE_COLUMNS if 4 <= row < 8 else COLUMNS
        shown = set(order[:count])
        source = (63 - row) * ROW_BYTES
        shift = RIPPLE[(phase + row) & 15]
        ink = GLINTS.get(row, 0xff)
        interior = bytes(plasma[source + column + shift] & ink if column in shown else 0
                         for column in range(1, 39))
        result.extend(b'\0' + interior + b'\0')
    return bytes(result)


def renderer(reveal_start):
    c = Code(ENTRY)

    def a(op, address):
        c.emit(op, address & 255, address >> 8)

    ripple_table = TABLES + ROW_BYTES
    coverage_table = ripple_table + len(RIPPLE) + ROW_COUNT - 1
    # The skyline has yet to cover the plasma at the quay.
    assert reveal_start % 256 == 0
    a(0xad, STATE+3)
    c.emit(0xc9, reveal_start >> 8)
    c.branch(0xb0, 'visible')
    c.emit(0x60)
    c.label('visible')
    c.branch(0xd0, 'full')
    a(0xad, STATE+2)
    c.emit(0x4a, 0x4a, 0x4a, 0x4a, 0x4a, 0xaa, 0xe8)
    c.branch(0xd0, 'read_coverage')
    c.label('full')
    c.emit(0xa2, 8)
    a(0xad, STATE+11)
    c.emit(0xc9, FIRST_FADE_OUT_PHASE)
    c.branch(0x90, 'read_coverage')
    c.emit(0x49, 255, 0x18, 0x69, LAST_FADE_OUT_PHASE+1, 0xaa)
    c.label('read_coverage')
    a(0xbd, coverage_table)
    c.jump(0x8d, 'coverage_operand')

    a(0xad, STATE+12)
    c.emit(0x4a, 0x29, 15, 0xaa)
    for row in range(ROW_COUNT):
        source = (63 - row) * ROW_BYTES
        assert 0 < (source & 255) < 255
        a(0xbd, ripple_table + row)
        c.emit(0x18, 0x69, source & 255)
        c.jump(0x8d, f'read_lo{row}')

    # Patch the high bytes by page so the column loops stay small.
    for page in (8, 9, 11, 12):
        a(0xad, STATE+13)
        c.emit(0x09, page)
        for row in range(ROW_COUNT):
            if (63-row)*ROW_BYTES >> 8 == page:
                c.jump(0x8d, f'read_hi{row}')
            if (PIXELS_OFFSET+row*ROW_BYTES) >> 8 == page:
                for mode in ('dry', 'wet'):
                    c.jump(0x8d, f'{mode}_hi{row}')

    # The two edge columns always go through the zero-fill path, keeping
    # shifted reads inside the corresponding source row.
    c.emit(0xa2, ROW_BYTES-1)
    c.label('dry')
    c.label('dry_limit')
    c.emit(0xe0, 0)
    c.branch(0x90, 'wet')
    c.jump(0xbc, 'columns')
    c.emit(0xa9, 0)
    for row in range(ROW_COUNT):
        if row == 4:
            a(0xbc, TABLES)
        if row == 8:
            c.jump(0xbc, 'columns')
        c.labels[f'dry_hi{row}'] = c.origin + len(c.data)+2
        a(0x99, PIXELS_OFFSET+row*ROW_BYTES)
    c.emit(0xca)
    c.branch(0x10, 'dry')
    c.jump(0x4c, 'finished')

    c.label('wet')
    c.jump(0xbc, 'columns')
    for row in range(ROW_COUNT):
        if row == 4:
            a(0xbc, TABLES)
        if row == 8:
            c.jump(0xbc, 'columns')
        c.labels[f'read_lo{row}'] = c.origin + len(c.data)+1
        c.labels[f'read_hi{row}'] = c.origin + len(c.data)+2
        a(0xb9, 0x9000)
        if row in GLINTS:
            c.emit(0x29, GLINTS[row])
        c.labels[f'wet_hi{row}'] = c.origin + len(c.data)+2
        a(0x99, PIXELS_OFFSET+row*ROW_BYTES)
    c.emit(0xca)
    c.branch(0x10, 'wet')
    c.label('finished')
    a(0x4c, FOOTER_ENTRY)
    c.labels['coverage_operand'] = c.labels['dry_limit']+1
    c.label('columns')
    c.emit(*COLUMNS, 0, ROW_BYTES-1)
    return bytes(c.finish())


def retire(reveal_start, school_start):
    """Remove water jumps while ANTIC is between frames."""
    c = Code(RETIRE_ENTRY)

    def a(op, address):
        c.emit(op, address & 255, address >> 8)

    c.label('check_water')
    a(0xad, STATE+4)
    c.branch(0xd0, 'check_tails')
    a(0xad, STATE+3)
    c.emit(0xc9, reveal_start >> 8)
    c.branch(0x90, 'check_tails')
    c.emit(0xc9, school_start >> 8)
    c.branch(0x90, 'water_done')
    c.branch(0xd0, 'check_tails')
    a(0xad, STATE+2)
    c.emit(0xc9, school_start & 255)
    c.branch(0x90, 'water_done')
    c.label('check_tails')
    for display, framebuffer in BUFFER_PAIRS:
        a(0xad, display+FOOTER_OFFSET+2)
        c.emit(0xc9, (framebuffer+TAIL_OFFSET) >> 8)
        c.branch(0xf0, 'retire_water')
    c.label('water_done')
    c.emit(0x60)

    c.label('retire_water')
    a(0xad, 0xd40b)
    c.emit(0xc9, 124)
    c.branch(0x90, 'retire_water')
    c.emit(0xc9, 132)
    c.branch(0xb0, 'retire_water')
    for index, (display, framebuffer) in enumerate(BUFFER_PAIRS):
        a(0xad, display+FOOTER_OFFSET+2)
        c.emit(0xc9, (framebuffer+TAIL_OFFSET) >> 8)
        c.branch(0xd0, f'water_reset{index}')
        c.emit(0xa9, 0x70)
        for offset in range(3):
            a(0x8d, display+FOOTER_OFFSET+offset)
        c.label(f'water_reset{index}')
    c.emit(0x60)
    return bytes(c.finish())


def footer():
    """Patch and initialize the inactive list's water tail on first use."""
    c = Code(FOOTER_ENTRY)

    def a(op, address):
        c.emit(op, address & 255, address >> 8)

    a(0xad, STATE+6)
    c.emit(0x09, FOOTER_OFFSET >> 8)
    for operand in ('read_hi', 'jump_hi', 'low_hi', 'high_hi'):
        c.jump(0x8d, operand)
    c.label('read')
    a(0xad, FOOTER_OFFSET)
    c.emit(0xc9, 1)
    c.branch(0xd0, 'initialize')
    c.emit(0x60)
    c.label('initialize')
    a(0xad, STATE+13)
    c.emit(0x09, TAIL_OFFSET >> 8)
    c.jump(0x8d, 'write_hi')
    c.label('high')
    a(0x8d, FOOTER_OFFSET+2)
    c.emit(0xa9, TAIL_OFFSET & 255)
    c.label('low')
    a(0x8d, FOOTER_OFFSET+1)
    c.emit(0xa2, 0)
    a(0xad, STATE+13)
    c.emit(0xc9, 0x90)
    c.branch(0xf0, 'source_ready')
    c.emit(0xa2, TAIL_SIZE)
    c.label('source_ready')
    c.emit(0xa0, 0)
    c.label('copy')
    a(0xbd, TEMPLATES)
    c.label('write')
    a(0x99, TAIL_OFFSET)
    c.emit(0xe8, 0xc8, 0xc0, TAIL_SIZE)
    c.branch(0xd0, 'copy')
    c.emit(0xa9, 1)
    c.label('jump')
    a(0x8d, FOOTER_OFFSET)
    c.emit(0x60)
    for name in ('read', 'jump', 'low', 'high', 'write'):
        c.labels[name+'_hi'] = c.labels[name]+2
    return bytes(c.finish())
