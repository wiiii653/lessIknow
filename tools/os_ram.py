"""Load video assets under OS ROM, then run the standalone player with OS off."""

from build_sequence import Code
from build_visual_prototype import xex_segment

ROM_REGIONS = ((0xc000, 0xd000), (0xd800, 0x10000))
ROM_BYTES = 0x3800
RUN = 0x13e0
PLAYER_ENTRY = 0x2146


def loader(blob):
    if len(blob) != ROM_BYTES:
        raise ValueError('expected complete 14 KiB OS-RAM image')
    c = Code(0x1000)
    c.emit(0x08, 0x78, 0xa9, 0, 0x8d, 0x0e, 0xd4,
           0xad, 0x01, 0xd3, 0x48, 0x29, 0xfe, 0x8d, 0x01, 0xd3)
    source = 0x8000
    for block, (start, end) in enumerate(ROM_REGIONS):
        c.emit(0xa2, (end - start) >> 8, 0xa0, 0)
        c.label(f'copy{block}')
        read = c.origin + len(c.data)
        c.emit(0xb9, source & 255, source >> 8)
        write = c.origin + len(c.data)
        c.emit(0x99, start & 255, start >> 8, 0xc8)
        c.branch(0xd0, f'copy{block}')
        c.emit(0xee, (read + 2) & 255, (read + 2) >> 8,
               0xee, (write + 2) & 255, (write + 2) >> 8, 0xca)
        c.branch(0xd0, f'copy{block}')
        source += end - start
    # All runtime bank selections keep OS ROM disabled. The player's original
    # RUN loop has no OS calls; its DLI handler becomes the hardware NMI vector.
    c.emit(0xa2, 13)
    c.label('banks')
    c.emit(0xbd, 0xfc, 0x26, 0x29, 0xfe, 0x9d, 0xfc, 0x26, 0xca)
    c.branch(0x10, 'banks')
    c.emit(0x68, 0x8d, 0x01, 0xd3, 0xa9, 0x40, 0x8d, 0x0e, 0xd4, 0x28, 0x60)
    code = c.finish()
    return (xex_segment(0x8000, blob) + xex_segment(0x1000, code)
            + xex_segment(0x02e2, bytes((0, 0x10))))


def run_stub(entry=PLAYER_ENTRY):
    # Blank the loader's display as soon as the standalone player takes over.
    return bytes.fromhex(
        '78 a9 00 8d 0e d4 8d 00 d4 8d 1d d0 8d 1a d0 '
        'ad 01 d3 29 fe 8d 01 d3 4c'
    ) + entry.to_bytes(2, 'little')


def image(chunks):
    blob = bytearray(ROM_BYTES)
    for start, data in chunks:
        region = next(((lo, hi) for lo, hi in ROM_REGIONS
                       if lo <= start and start + len(data) <= hi), None)
        if region is None:
            raise ValueError('OS-RAM chunk outside usable RAM')
        offset = start - region[0] + (0x1000 if start >= 0xd800 else 0)
        blob[offset:offset + len(data)] = data
    # Direct NMI: original player pushes/pops all registers and ends with RTI.
    blob[-6:] = bytes((0x10, 0x22, 0x46, 0x21, 0x17, 0x23))
    return blob
