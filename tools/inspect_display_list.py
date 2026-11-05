#!/usr/bin/env python3
"""Inspect the original player's ANTIC display list and DLI timing."""

import argparse
from pathlib import Path

from extract_music import segments


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xex", type=Path)
    parser.add_argument("--address", type=lambda n: int(n, 0), default=0x3300)
    args = parser.parse_args()
    memory = bytearray(65536)
    loaded = bytearray(65536)
    for start, end, data in segments(args.xex.read_bytes()):
        # Staging banks and INIT routines are not emulated here.
        memory[start:end + 1] = data
        loaded[start:end + 1] = b"\x01" * len(data)
    heights = (0, 0, 8, 10, 8, 16, 8, 16, 8, 4, 4, 2, 1, 2, 1, 1)
    pc, line = args.address, 0

    def fetch():
        nonlocal pc
        if not loaded[pc]:
            raise SystemExit(f"display list reaches unloaded address ${pc:04X}")
        value = memory[pc]
        pc = (pc & 0xfc00) | ((pc + 1) & 0x03ff)
        return value

    for _ in range(1024):
        address = pc
        op = fetch()
        mode = op & 15
        if mode == 1:
            target = fetch() | fetch() << 8
            print(f"${address:04X}: {'JVB' if op & 0x40 else 'JMP'} ${target:04X}")
            if op & 0x40:
                print(f"Total display-list scanlines: {line}")
                return
            pc = target
            continue
        height = ((op >> 4) & 7) + 1 if mode == 0 else heights[mode]
        if mode and op & 0x40:
            fetch()
            fetch()
        suffix = f" DLI on line {line + height - 1}" if op & 0x80 else ""
        print(f"${address:04X}: mode {mode:X}, lines {line}-{line + height - 1}{suffix}")
        line += height
    raise SystemExit("display list did not reach JVB")


if __name__ == "__main__":
    main()
