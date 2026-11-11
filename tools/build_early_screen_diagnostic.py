#!/usr/bin/env python3
"""Standalone AVG/OS-RAM test: show text from an early XEX INIT.

This artifact deliberately does not touch a bank. It isolates the early display
path from bank mapping: if the text is visible, early INIT and the ROM font are
working; if it is black, the problem is in the load/display environment.
"""
from pathlib import Path

from build_sequence import Code
from build_visual_prototype import xex_segment

SCREEN = 0x2900       # 5 rows x 40 bytes
DLIST = 0x2ac0        # inside the free $2900-$2BFF gap of the original player
ENTRY = 0x2b00
OUTPUT = Path('releases/avg-early-screen-diagnostic-004.xex')
LINES = ('EARLY SCREEN OK',
         'AVG / XEX INIT + ROM FONT',
         'IF VISIBLE: DISPLAY PATH WORKS',
         'BANK LOADING NOT TESTED',
         'READY')


def screen_code(origin):
    c = Code(origin)

    def store(address, value):
        c.emit(0xa9, value, 0x8d, address & 255, address >> 8)

    # OS shadows and hardware. $D018=$E0 selects the ROM character set at
    # $E000, unlike loading_screen's old $00 (which points CHBASE at page 0).
    for address, value in ((0x022f, 0x22), (0x0230, DLIST & 255),
                           (0x0231, DLIST >> 8), (0x02f4, 0xe0),
                           (0x02c5, 0x0e), (0x02c6, 0x00),
                           (0xd402, DLIST & 255), (0xd403, DLIST >> 8),
                           (0xd409, 0xe0), (0xd017, 0x0e),
                           (0xd018, 0xe0), (0xd400, 0x22)):
        store(address, value)
    # Copy the five ATASCII rows into screen memory (upper-case ATASCII - 32).
    for row, line in enumerate(LINES):
        for column in range(40):
            address = SCREEN + row * 40 + column
            value = ord(line[column]) - 32 if column < len(line) else 0
            c.emit(0xa9, value, 0x8d, address & 255, address >> 8)
    c.label('halt')
    c.jump(0x4c, 'halt')
    return bytes(c.finish())


def main():
    # ANTIC mode 2 rows, all LMS-pointed at SCREEN, then JVB.
    display = bytes((0x70, 0x70, 0x70,
                     0x42, SCREEN & 255, SCREEN >> 8,
                     0x42, (SCREEN + 40) & 255, (SCREEN + 40) >> 8,
                     0x42, (SCREEN + 80) & 255, (SCREEN + 80) >> 8,
                     0x42, (SCREEN + 120) & 255, (SCREEN + 120) >> 8,
                     0x42, (SCREEN + 160) & 255, (SCREEN + 160) >> 8,
                     0x41, DLIST & 255, DLIST >> 8))
    assert DLIST + len(display) <= 0x2b00
    out = bytearray(b'\xff\xff')
    out.extend(xex_segment(DLIST, display))
    out.extend(xex_segment(ENTRY, screen_code(ENTRY)))
    out.extend(xex_segment(0x02e2, ENTRY.to_bytes(2, 'little')))
    out.extend(xex_segment(0x02e0, ENTRY.to_bytes(2, 'little')))
    with OUTPUT.open('xb') as stream:
        stream.write(out)


if __name__ == '__main__':
    main()
