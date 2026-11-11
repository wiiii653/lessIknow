#!/usr/bin/env python3
"""Self-contained 64-bank map probe that runs entirely inside INIT.

The previous version displayed "PROBING" from the INIT and then relied on the
$02E0 RUN vector to execute the probe. On the target AVG loader the RUN vector
never appeared to execute, so this build does everything from the INIT: display,
probe, result. No RUN vector is required.

Each candidate PORTB value gets a unique marker in its own bank at $4000; a
second pass verifies that no two selectors alias the same 16 KiB bank.
"""
from pathlib import Path

from build_sequence import Code
from build_visual_prototype import xex_segment

OUTPUT = Path('releases/avg-bank-map-diagnostic-003.xex')

SCREEN = 0x2B00
DLIST = 0x2C00
TITLE = 0x2C16
PROBING = 0x2C3E
PASSED = 0x2C66
FAILED = 0x2C8E
CODE = 0x2CC0
CANDIDATES = 0x2E00
INDEX = 0x2E40
COMPARE = 0x2E41
END = 0x2EFF

SELECTORS = [base + i + 1
             for base in (0x80, 0xA0, 0xC0, 0xE0, 0x00, 0x20, 0x40, 0x60)
             for i in range(0, 16, 2)]


def display_list():
    rows = bytearray((0x70, 0x70, 0x70))
    for row in range(5):
        rows.extend((0x42, (SCREEN + row * 40) & 255,
                     (SCREEN + row * 40) >> 8))
    rows.extend((0x41, DLIST & 255, DLIST >> 8))
    return bytes(rows)


def enc(text):
    return bytes((ord(ch) - 32) & 0x7F for ch in text[:40].ljust(40))


def copy_row(c, tag, source, row):
    target = SCREEN + row * 40
    c.emit(0xA0, 0)
    c.label(tag)
    c.emit(0xB9, source & 255, source >> 8, 0x99, target & 255, target >> 8)
    c.emit(0xC8, 0xC0, 40)
    c.branch(0xD0, tag)


def display_setup(c):
    def store(address, value):
        c.emit(0xA9, value, 0x8D, address & 255, address >> 8)

    for address, value in ((0x022F, 0x22), (0x0230, DLIST & 255),
                           (0x0231, DLIST >> 8), (0x02F4, 0xE0),
                           (0x02C5, 0x0E), (0x02C6, 0x00),
                           (0xD402, DLIST & 255), (0xD403, DLIST >> 8),
                           (0xD409, 0xE0), (0xD017, 0x0E),
                           (0xD018, 0xE0), (0xD400, 0x22)):
        store(address, value)


def build_code(origin):
    c = Code(origin)
    copy_row(c, 'title', TITLE, 0)
    copy_row(c, 'probing', PROBING, 2)
    display_setup(c)

    # Do NOT read $D301: PORTB is write-only on real hardware, so the value
    # read back is garbage. A fixed $FF restores the normal XL/XE default.

    # Pass 1: unique marker into every candidate bank.
    c.emit(0xA2, 0)
    c.label('write')
    c.emit(0x8E, INDEX & 255, INDEX >> 8)
    c.emit(0xBD, CANDIDATES & 255, CANDIDATES >> 8)
    c.emit(0x8D, 0x01, 0xD3)                # bit 0 stays set: OS ROM on
    c.emit(0xAD, INDEX & 255, INDEX >> 8)
    c.emit(0x18, 0x69, 0x01)                # marker = index + 1
    c.emit(0x8D, 0x00, 0x40)
    c.emit(0xAE, INDEX & 255, INDEX >> 8)
    c.emit(0xE8, 0xE0, 64)
    c.branch(0xD0, 'write')

    # Pass 2: read every marker back and compare.
    c.emit(0xA2, 0)
    c.label('read')
    c.emit(0x8E, INDEX & 255, INDEX >> 8)
    c.emit(0xBD, CANDIDATES & 255, CANDIDATES >> 8)
    c.emit(0x8D, 0x01, 0xD3)
    c.emit(0xAD, 0x00, 0x40, 0x8D, COMPARE & 255, COMPARE >> 8)
    c.emit(0xAD, INDEX & 255, INDEX >> 8)
    c.emit(0x18, 0x69, 0x01)
    c.emit(0xCD, COMPARE & 255, COMPARE >> 8)
    c.branch(0xD0, 'fail')
    c.emit(0xAE, INDEX & 255, INDEX >> 8)
    c.emit(0xE8, 0xE0, 64)
    c.branch(0xD0, 'read')

    c.emit(0xA9, 0xFF, 0x8D, 0x01, 0xD3)   # OS ROM + BASIC back on
    copy_row(c, 'passed', PASSED, 2)
    c.label('halt_pass')
    c.jump(0x4C, 'halt_pass')

    c.label('fail')
    c.emit(0xA9, 0xFF, 0x8D, 0x01, 0xD3)
    copy_row(c, 'failed', FAILED, 2)
    c.label('halt_fail')
    c.jump(0x4C, 'halt_fail')
    return bytes(c.finish())


def main():
    code = build_code(CODE)
    assert CODE + len(code) <= CANDIDATES, hex(CODE + len(code))
    print(f'code ${CODE:04X}-${CODE + len(code) - 1:04X} ({len(code)} B)')
    out = bytearray(b'\xff\xff')
    out.extend(xex_segment(DLIST, display_list()))
    out.extend(xex_segment(TITLE, enc('64 BANK SELECTORS')))
    out.extend(xex_segment(PROBING, enc('PROBING - PLEASE WAIT')))
    out.extend(xex_segment(PASSED, enc('BANK MAP PASSED')))
    out.extend(xex_segment(FAILED, enc('BANK MAP FAILED')))
    out.extend(xex_segment(CODE, code))
    out.extend(xex_segment(CANDIDATES, bytes(SELECTORS)))
    out.extend(xex_segment(INDEX, bytes(2)))
    out.extend(xex_segment(0x02E2, CODE.to_bytes(2, 'little')))
    # A halt loop as RUN target is harmless if a loader also honours $02E0.
    out.extend(xex_segment(0x02E0, CODE.to_bytes(2, 'little')))
    with OUTPUT.open('xb') as stream:
        stream.write(out)


if __name__ == '__main__':
    main()
