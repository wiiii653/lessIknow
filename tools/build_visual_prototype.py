#!/usr/bin/env python3
"""Build an experimental music + ANTIC E image from the original v035 XEX."""

import argparse
import math
from pathlib import Path

from extract_music import segments


def xex_segment(address, payload):
    end = address + len(payload) - 1
    if not payload or end > 0xffff:
        raise ValueError("invalid segment size")
    return address.to_bytes(2, "little") + end.to_bytes(2, "little") + payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("player", type=Path)
    parser.add_argument("gray", type=Path, help="160x192 8-bit grayscale image")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    gray = args.gray.read_bytes()
    if len(gray) != 160 * 192:
        parser.error("image must contain exactly 160x192 grayscale bytes")
    image = bytearray()
    for i in range(0, len(gray), 4):
        byte = 0
        for pixel in gray[i:i + 4]:
            # Avoid PF0, whose color the player does not initialize.
            value = 0 if pixel < 48 else 2 if pixel < 155 else 3
            byte = (byte << 2) | value
        image.append(byte)

    # Original list begins with a DLI at line 0, then 8 blank lines.
    display = bytearray((0x80, 0x70))
    for row in range(192):
        line = row + 9
        op = 0x0e | (0x80 if line in (78, 156) else 0)
        if row in (0, 102):
            address = 0x9000 if row == 0 else 0xa000
            display.extend((op | 0x40, address & 255, address >> 8))
        else:
            display.append(op)
    # Finish with the fourth DLI at line 234, then wait for vertical blank.
    display.extend((0x70, 0x70, 0x70, 0x70, 0x90, 0x41, 0x00, 0x80))

    # Four row-remapped display lists produce a breathing/rippling image.
    # Every row has an LMS, so no bitmap copying is needed at runtime.
    animated_lists = bytearray()
    list_addresses = []
    for phase in range(4):
        # ANTIC wraps its display-list counter within a 1 KiB page. A list
        # must not straddle that boundary without an explicit JMP.
        animated_lists.extend(bytes((-len(animated_lists)) % 0x400))
        base = 0xb000 + len(animated_lists)
        list_addresses.append(base)
        frame = bytearray((0x80, 0x70))
        for row in range(192):
            shift = round(phase * 3 * math.sin((row - 95.5) * math.pi / 96))
            source_row = max(0, min(191, row + shift))
            address = (0x9000 + source_row * 40 if source_row < 102
                       else 0xa000 + (source_row - 102) * 40)
            frame.extend((0x4e | (0x80 if row + 9 in (78, 156) else 0),
                          address & 255, address >> 8))
        frame.extend((0x70, 0x70, 0x70, 0x70, 0x90, 0x41, base & 255, base >> 8))
        if (base & 0x3ff) + len(frame) > 0x400:
            raise ValueError('display list crosses an ANTIC 1 KiB boundary')
        animated_lists.extend(frame)
    assert 0xb000 + len(animated_lists) <= 0xc000
    sequence = [list_addresses[i] for i in (0, 1, 2, 3, 3, 2, 1, 0)]
    # Called once per four DLIs by the original main loop. Use playback ticks
    # (not VBI), so pause also pauses the animation. Wait for vertical blank
    # before changing the two display-list pointer bytes.
    animation = bytes.fromhex(
        'ad a7 24 4a 4a 4a 29 07 aa '
        'ad 0b d4 c9 7c 90 f9 '
        'bd 40 81 8d 02 d4 bd 48 81 8d 03 d4 '
        'ad a7 24 29 f0 09 0e 8d 17 d0 49 80 8d 18 d0 20 cd 23 60')
    animation += bytes(0x40 - len(animation))
    animation += bytes(a & 255 for a in sequence) + bytes(a >> 8 for a in sequence)

    output = bytearray(b"\xff\xff")
    patched = False
    inserted = False
    for start, end, payload in segments(args.player.read_bytes()):
        if start == 0x2000 and end == 0x24b2:
            payload = bytearray(payload)
            # RUN sets DLISTL/H with these immediate loads.
            offset = 0x21bc - start
            expected = bytes.fromhex("a9 00 8d 02 d4 a9 33 8d 03 d4")
            if payload[offset:offset + len(expected)] != expected:
                raise ValueError("unexpected v035 display setup; refusing to patch")
            payload[offset + 6] = 0x80
            ui = 0x220a - start
            if payload[ui:ui + 3] != bytes.fromhex('20 cd 23'):
                raise ValueError('unexpected main-loop UI call')
            payload[ui:ui + 3] = bytes.fromhex('20 00 81')
            patched = True
        if (start, end) == (0x02e0, 0x02e1):
            output.extend(xex_segment(0x8000, display))
            output.extend(xex_segment(0x8100, animation))
            output.extend(xex_segment(0xb000, animated_lists))
            output.extend(xex_segment(0x9000, image[:102 * 40]))
            output.extend(xex_segment(0xa000, image[102 * 40:]))
            inserted = True
        output.extend(xex_segment(start, payload))
    if not patched or not inserted:
        raise ValueError("expected v035 code and RUN vector not found")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output)
    print(f"Wrote {args.output} ({len(output)} bytes)")


if __name__ == "__main__":
    main()
