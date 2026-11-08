#!/usr/bin/env python3
"""Extract the staged music banks from an Atari DOS binary (XEX)."""

import argparse
import hashlib
import json
from pathlib import Path


def segments(data):
    if not data.startswith(b"\xff\xff"):
        raise ValueError("missing XEX header")
    pos = 2
    while pos < len(data):
        if pos + 2 > len(data):
            raise ValueError(f"truncated segment header at {pos:#x}")
        start = int.from_bytes(data[pos:pos + 2], "little")
        pos += 2
        if start == 0xffff:
            continue
        if pos + 2 > len(data):
            raise ValueError(f"truncated segment end at {pos:#x}")
        end = int.from_bytes(data[pos:pos + 2], "little")
        pos += 2
        size = end - start + 1
        if size <= 0 or pos + size > len(data):
            raise ValueError(f"invalid segment ${start:04X}-${end:04X}")
        yield start, end, data[pos:pos + size]
        pos += size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xex", type=Path, help="original player XEX")
    parser.add_argument("output", type=Path, help="new output directory")
    args = parser.parse_args()
    data = args.xex.read_bytes()
    entries = list(segments(data))
    banks = [payload for start, end, payload in entries
             if (start, end) == (0x8000, 0xbfff)]
    if not banks:
        parser.error("no 16 KiB staging banks found at $8000-$BFFF")
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {"source": args.xex.name, "source_sha256": hashlib.sha256(data).hexdigest(),
                "bank_size": 16384, "banks": []}
    for index, bank in enumerate(banks, 1):
        name = f"bank_{index:02d}.bin"
        (args.output / name).write_bytes(bank)
        manifest["banks"].append({"file": name, "sha256": hashlib.sha256(bank).hexdigest(),
                                  "all_ff": all(byte == 0xff for byte in bank)})
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Extracted {len(banks)} staging banks to {args.output}")


if __name__ == "__main__":
    main()
