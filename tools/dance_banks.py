"""Complete gym/dancer frames in the six proven-unused v035 expansion banks."""

FRAME_BASES = (0x9000, 0xb000)
FRAME_BYTES = 0x2000


def frame_address(base, y):
    # 102 rows fit before the 4 KiB DMA boundary; leave a 16-byte gap.
    return base + (y * 40 if y < 102 else 0x1000 + (y - 102) * 40)


def frame_blob(rows):
    result = bytearray(FRAME_BYTES)
    for y, row in enumerate(rows):
        offset = frame_address(0, y)
        result[offset:offset + 40] = row
    return bytes(result)
