"""Draw and publish the title's procedural reflection in title-owned RAM."""

import math

from build_sequence import Code

TEMPLATES = 0x4430
FOOTER_ENTRY = 0x5468
TABLES = 0x54b0
ENTRY = 0x6638
RIPPLE_MASKS = 0x7140  # Between firework code and anchor data.
EDGE_ENTRY = 0x71e0
RIPPLE_TABLES = 0x7f10  # Beyond the firework missile routine.
RETIRE_ENTRY = 0x3c80
RASTER_ENTRY = 0xe140  # Between the shared mosaic tables and the practice map.
STATE = 0x83e0
ROW_BYTES = 40
ROW_COUNT = 11
PIXELS_OFFSET = 0x0b00
TAIL_OFFSET = 0x0d00
FOOTER_OFFSET = 2 + 192 * 3
# The title draws into $9000 when the inactive display list is $8400.
BUFFER_PAIRS = ((0x8400, 0x9000), (0x8000, 0xb000))

# Sample the city near the quay and the live sky deeper into the reflection.
SOURCE_ROWS = (62, 61, 60, 57, 51, 45, 40, 33, 28, 24, 20)
SCANLINES = (2, 2, 3, 1, 4, 4, 4, 1, 4, 1, 3)
DEEP_ROW = 8
# Keep the last music DLI at relative line 234 while giving the water edge
# some clearance from the bottom of the picture.
BOTTOM_BLANK = 33 - sum(SCANLINES)
TAIL_SIZE = sum(SCANLINES)*3 + 5
WIDE_RIPPLE_ROW = 5
RIPPLE = tuple(tuple(round(amplitude*math.sin(math.tau*i/16)) for i in range(16))
               for amplitude in (1, 2))
# Interrupt the continuous reflection on just these single scanlines.
RIPPLE_LINES = (3, 7, 9)
# Spread each reveal step across the water.
COLUMNS = tuple(sorted(range(1, 39), key=lambda column: (column * 17) % 41))
MIDDLE_COLUMNS = tuple(sorted(range(1, 39), key=lambda column: (column * 13 + 5) % 43))
FIRST_FADE_OUT_PHASE = 39
LAST_FADE_OUT_PHASE = 46


def tail(display, framebuffer):
    data = bytearray()
    assert len(SCANLINES) == ROW_COUNT and 1 <= BOTTOM_BLANK <= 8
    for row, height in enumerate(SCANLINES):
        pixels = framebuffer + PIXELS_OFFSET + row * ROW_BYTES
        assert pixels // 0x1000 == (pixels + ROW_BYTES - 1) // 0x1000
        line = (0x4f, pixels & 255, pixels >> 8)
        if row in (0, DEEP_ROW):
            # Palette DLIs dim the waterline and the deeper bands.
            data.extend((0xcf, *line[1:]))
            height -= 1
        data.extend(line * height)
    data.extend(((BOTTOM_BLANK-1) << 4, 0x80, 0x41, display & 255, display >> 8))
    assert len(data) == TAIL_SIZE
    assert (framebuffer + TAIL_OFFSET) % 0x400 + len(data) <= 0x400
    return bytes(data)


def templates():
    return b''.join(tail(display, framebuffer) for display, framebuffer in BUFFER_PAIRS)


def tables():
    return bytes((*COLUMNS, 0, ROW_BYTES-1, *MIDDLE_COLUMNS, 0, ROW_BYTES-1))


def ripple_tables():
    return bytes((*(value & 255 for wave in RIPPLE for value in wave*2),
                  *(round(len(COLUMNS) * level / 8) for level in range(9))))


def ripple_masks():
    masks = bytearray()
    for row in RIPPLE_LINES:
        edge = 4 if row >= WIDE_RIPPLE_ROW else 2
        pixels = []
        for pixel in range(ROW_BYTES*2):
            phase = pixel*0.37 + row*1.3
            wave = math.sin(phase) + 0.35*math.sin(2*phase+pixel*0.12)
            pixels.append(15 if edge <= pixel < ROW_BYTES*2-edge and wave <= 0.4 else 0)
        masks.extend(left << 4 | right for left, right in zip(pixels[::2], pixels[1::2]))
    masks.extend(bytes([0, 0] + [255]*(ROW_BYTES-4) + [0, 0]))
    return bytes(masks)


def mask_offset(row):
    if row in RIPPLE_LINES:
        return RIPPLE_LINES.index(row)*ROW_BYTES
    if row >= WIDE_RIPPLE_ROW:
        return len(RIPPLE_LINES)*ROW_BYTES
    return None


def raster(published_light):
    """Dim the two water bands and preserve the title's four music DLIs."""
    from outro_palette import EXIT

    c = Code(RASTER_ENTRY)

    def a(op, address):
        c.emit(op, address & 255, address >> 8)

    # Palette-only DLIs lie at relative lines 201 and 222. The event
    # at 234 restores the sky and continues through the music player.
    a(0xad, 0xd40b); c.emit(0xc9, 96); c.branch(0x90, 'music')
    c.emit(0xc9, 113); c.branch(0x90, 'surface')
    c.emit(0xc9, 120); c.branch(0xb0, 'restore')
    c.emit(0xa2, 2); c.branch(0xd0, 'water')
    c.label('surface'); c.emit(0xa2, 1)
    c.label('water')
    a(0xad, published_light)
    c.label('dim')
    c.emit(0xc9, 2); c.branch(0x90, 'water_light')
    c.emit(0xe9, 2, 0xca); c.branch(0xd0, 'dim')
    c.label('water_light')
    a(0x8d, 0xd01a); a(0x4c, EXIT)
    c.label('restore')
    a(0xad, published_light); a(0x8d, 0xd01a)
    c.label('music')
    a(0x8d, 0xd40a); c.emit(0x60)
    result = bytes(c.finish())
    assert RASTER_ENTRY + len(result) <= 0xe180
    return result


def reflection(level, phase, scene):
    """Reference for byte-packed mirror, ripple and dissolve."""
    result = bytearray()
    masks = ripple_masks()
    count = round(len(COLUMNS) * level / 8)
    for row, source_row in enumerate(SOURCE_ROWS):
        order = MIDDLE_COLUMNS if 4 <= row < 8 else COLUMNS
        shown = set(order[:count])
        source = source_row * ROW_BYTES
        wave = RIPPLE[row >= WIDE_RIPPLE_ROW]
        shift = wave[(phase + 2*row) & 15]
        offset = mask_offset(row)
        mask = bytes([255])*ROW_BYTES if offset is None else masks[offset:offset+ROW_BYTES]
        pixels = bytearray(ROW_BYTES)
        for column in shown:
            pixels[column] = scene[source + column + shift] & mask[column]
        edge = 2 if row >= WIDE_RIPPLE_ROW else 1
        pixels[:edge] = bytes([(pixels[edge] >> 4)*17])*edge
        pixels[-edge:] = bytes([(pixels[-edge-1] & 15)*17])*edge
        result.extend(pixels)
    return bytes(result)


def renderer(reveal_start):
    c = Code(ENTRY)

    def a(op, address):
        c.emit(op, address & 255, address >> 8)

    coverage_table = RIPPLE_TABLES + 2*sum(map(len,RIPPLE))
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
    for row, source_row in enumerate(SOURCE_ROWS):
        source = source_row * ROW_BYTES
        wide = row >= WIDE_RIPPLE_ROW
        assert 2 <= (source & 255) <= 253
        a(0xbd, RIPPLE_TABLES + (2*len(RIPPLE[0]) if wide else 0) + (2*row & 15))
        c.emit(0x18, 0x69, source & 255)
        c.jump(0x8d, f'read_lo{row}')

    # Patch the high bytes by page so the column loops stay small.
    pages = {source*ROW_BYTES >> 8 for source in SOURCE_ROWS}
    pages.update((PIXELS_OFFSET+row*ROW_BYTES) >> 8 for row in range(ROW_COUNT))
    for page in sorted(pages):
        a(0xad, STATE+13)
        c.emit(0x09, page)
        for row, source_row in enumerate(SOURCE_ROWS):
            if source_row*ROW_BYTES >> 8 == page:
                c.jump(0x8d, f'read_hi{row}')
            if (PIXELS_OFFSET+row*ROW_BYTES) >> 8 == page:
                for mode in ('dry', 'wet'):
                    c.jump(0x8d, f'{mode}_hi{row}')

    # Keep shifted reads away from the edges, then extend the nearest
    # reflected pixels into the guard columns.
    c.emit(0xa2, ROW_BYTES-1)
    c.label('dry')
    c.label('dry_limit')
    c.emit(0xe0, 0)
    c.branch(0x90, 'wet')
    a(0xbc, TABLES)
    c.emit(0xa9, 0)
    for row in range(ROW_COUNT):
        if row == 4:
            a(0xbc, TABLES+ROW_BYTES)
        if row == 8:
            a(0xbc, TABLES)
        c.labels[f'dry_hi{row}'] = c.origin + len(c.data)+2
        a(0x99, PIXELS_OFFSET+row*ROW_BYTES)
    c.emit(0xca)
    c.branch(0x10, 'dry')
    c.jump(0x4c, 'finished')

    c.label('wet')
    a(0xbc, TABLES)
    for row in range(ROW_COUNT):
        if row == 4:
            a(0xbc, TABLES+ROW_BYTES)
        if row == 8:
            a(0xbc, TABLES)
        c.labels[f'read_lo{row}'] = c.origin + len(c.data)+1
        c.labels[f'read_hi{row}'] = c.origin + len(c.data)+2
        a(0xb9, 0x9000)
        offset = mask_offset(row)
        if offset is not None:
            a(0x39, RIPPLE_MASKS+offset)
        c.labels[f'wet_hi{row}'] = c.origin + len(c.data)+2
        a(0x99, PIXELS_OFFSET+row*ROW_BYTES)
    c.emit(0xca)
    c.branch(0x10, 'wet')
    c.label('finished')
    a(0x4c, EDGE_ENTRY)
    c.labels['coverage_operand'] = c.labels['dry_limit']+1
    return bytes(c.finish())


def edge_filler():
    """Extend each row's outermost safe reflected pixels to the edges."""
    c = Code(EDGE_ENTRY)

    def a(op, address):
        c.emit(op, address & 255, address >> 8)

    operands = ('read_left', 'write_left', 'read_right', 'write_right')
    # Use the same patched row base for the reads and the writes.
    c.emit(0xa2,0,0xa9,PIXELS_OFFSET & 255)
    c.jump(0x8d,'row_lo')
    a(0xad,STATE+13);c.emit(0x09,PIXELS_OFFSET >> 8)
    c.jump(0x8d,'row_hi')
    c.label('row')
    c.jump(0xad,'row_lo')
    for name in operands:
        c.jump(0x8d,name+'_lo')
    c.jump(0xad,'row_hi')
    for name in operands:
        c.jump(0x8d,name+'_hi')
    c.emit(0xa0,1,0xe0,WIDE_RIPPLE_ROW);c.branch(0x90,'read_left');c.emit(0xc8)
    c.label('read_left');a(0xb9,0)
    c.emit(0x4a,0x4a,0x4a,0x4a)
    c.jump(0x20,'repeat_nibble')
    c.label('left');c.emit(0x88)
    c.label('write_left');a(0x99,0);c.branch(0xd0,'left')
    c.emit(0xa0,ROW_BYTES-2,0xe0,WIDE_RIPPLE_ROW)
    c.branch(0x90,'read_right');c.emit(0x88)
    c.label('read_right');a(0xb9,0)
    c.jump(0x20,'repeat_nibble')
    c.label('right');c.emit(0xc8)
    c.label('write_right');a(0x99,0)
    c.emit(0xc0,ROW_BYTES-1);c.branch(0x90,'right')
    c.jump(0xad,'row_lo');c.emit(0x18,0x69,ROW_BYTES)
    c.jump(0x8d,'row_lo');c.branch(0x90,'next')
    c.jump(0xee,'row_hi')
    c.label('next');c.emit(0xe8,0xe0,ROW_COUNT);c.branch(0xd0,'row')
    a(0x4c, FOOTER_ENTRY)
    c.label('repeat_nibble');c.emit(0x29,15)
    c.jump(0x8d,'outer_pixel')
    c.emit(0x0a,0x0a,0x0a,0x0a);c.jump(0x0d,'outer_pixel');c.emit(0x60)
    for name in operands:
        c.labels[name+'_lo'] = c.labels[name]+1
        c.labels[name+'_hi'] = c.labels[name]+2
    for name in ('row_lo', 'row_hi', 'outer_pixel'):
        c.label(name);c.emit(0)
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
