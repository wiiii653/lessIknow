#!/usr/bin/env python3
"""Standalone clone of the TLIKTB loading screen and per-bank cycle.

The clone reproduces only what is visible while the demo loads:

- the text screen at `$3800`, display list at `$3880` and INIT at `$38A0`
  (taken from the hardware-confirmed release 058 reference);
- the animated finale star VBI at `$1100` and its delta stream at `$1400`;
- the progress-dot text rewritten by the `$3900` wrapper;
- the per-bank `$3A00` clear and the `$1000` 16 KiB copy, with the same
  timing as the real loader (about 4.6 + 6.4 PAL frames per bank).

It contains no demo scenes, no music player and no bank selectors. Bank
data is synthetic, so the file stays small and can be built in seconds.

Two modes:

- ``copy``   reproduces the current loader: clear staging, copy 16 KiB to
             `$4000` with NMI off (~6.4 frames of frozen animation).
- ``direct`` skips the copy, simulating a direct-to-bank load: only the
             clear runs, with NMI on.

This is a test harness for loader/flicker work, not a demo candidate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from build_sequence import Code  # noqa: E402
from build_visual_prototype import xex_segment  # noqa: E402
from extract_music import segments  # noqa: E402
import animated_loading  # noqa: E402

REFERENCE = ROOT / "releases" / "less-i-know-demo-release-058-stereo.xex"
SCREEN = 0x3800
DLIST = 0x3880
INIT38 = 0x38A0
WRAPPER = 0x3900
CLEAR = 0x3A00
COPY = 0x1000
MAIN = 0x3C00
DONE_TEXT = 0x3828
COUNTER = 0x3BF0


def reference_payload(address: int) -> bytes:
    for start, end, payload in segments(REFERENCE.read_bytes()):
        if start == address:
            return payload
    raise ValueError(f"reference has no segment at ${address:04X}")


def reference_wrapper() -> bytes:
    """Pick a release 058 wrapper that copies through $1000, not $20EA."""
    for start, end, payload in segments(REFERENCE.read_bytes()):
        if start == WRAPPER and b"\x20\x00\x10" in payload:
            return payload
    raise ValueError("reference has no $1000 wrapper")


def copy_routine() -> bytes:
    """16 KiB $8000 -> $4000 copy with the real loader's timing and NMI mask."""
    c = Code(COPY)

    def absolute(op: int, address: int) -> None:
        c.emit(op, address & 255, address >> 8)

    c.emit(0x08, 0x78)                     # PHP / SEI
    c.emit(0xa9, 0)                        # LDA #0
    absolute(0x8d, 0xd40e)                 # STA NMIEN
    absolute(0xad, 0xd301)                 # LDA PORTB
    c.emit(0x48)                           # PHA
    c.emit(0xa9, 0x80)                     # LDA #$80: bank 0
    absolute(0x8d, 0xd301)                 # STA PORTB
    reset_read = len(c.data) + 3           # operand of STA read+2
    c.emit(0xa9, 0x80, 0x8d, 0, 0)         # LDA #$80 / STA read+2
    reset_write = len(c.data) + 3          # operand of STA write+2
    c.emit(0xa9, 0x40, 0x8d, 0, 0)         # LDA #$40 / STA write+2
    c.emit(0xa2, 0x40, 0xa0, 0)            # LDX #$40 / LDY #0
    c.label("loop")
    c.label("read")
    c.emit(0xb9, 0, 0x80)                  # LDA $8000,Y
    c.label("write")
    c.emit(0x99, 0, 0x40)                  # STA $4000,Y
    c.emit(0xc8)                           # INY
    c.branch(0xd0, "loop")
    inc_read = len(c.data) + 1             # operand of INC read+2
    c.emit(0xee, 0, 0)
    inc_write = len(c.data) + 1            # operand of INC write+2
    c.emit(0xee, 0, 0)
    c.emit(0xca)                           # DEX
    c.branch(0xd0, "loop")
    c.emit(0x68)                           # PLA: restore PORTB
    absolute(0x8d, 0xd301)                 # STA PORTB
    c.emit(0xa9, 0x40)                     # LDA #$40
    absolute(0x8d, 0xd40e)                 # STA NMIEN
    c.emit(0x28, 0x60)                     # PLP / RTS
    data = bytearray(c.finish())
    for pos, label in ((reset_read, "read"), (reset_write, "write"),
                       (inc_read, "read"), (inc_write, "write")):
        addr = c.labels[label] + 2
        data[pos] = addr & 255
        data[pos + 1] = addr >> 8
    return bytes(data)


def dummy_copy() -> bytes:
    """Timing-only copy: ~6.9 PAL frames, no memory writes."""
    c = Code(COPY)

    def absolute(op: int, address: int) -> None:
        c.emit(op, address & 255, address >> 8)

    c.emit(0x08, 0x78)                     # PHP / SEI
    c.emit(0xa9, 0)
    absolute(0x8d, 0xd40e)                 # NMIEN=0
    c.emit(0xa2, 0xc0)                     # LDX #192 pages
    c.label("outer")
    c.emit(0xa0, 0)                        # LDY #0
    c.label("inner")
    c.emit(0x88)                           # DEY
    c.branch(0xd0, "inner")
    c.emit(0xca)                           # DEX
    c.branch(0xd0, "outer")
    c.emit(0xa9, 0x40)
    absolute(0x8d, 0xd40e)                 # NMIEN=$40
    c.emit(0x28, 0x60)                     # PLP / RTS
    return bytes(c.finish())


def no_op_copy(portb: bool = False) -> bytes:
    """`direct` mode: enable the loading VBI and return without a copy."""
    c = Code(COPY)
    if portb:
        # Mirror the copy's PORTB sequence without moving any bytes.
        c.emit(0xAD, 0x01, 0xD3)           # LDA $D301
        c.emit(0x48)                       # PHA
        c.emit(0xA9, 0x80)                 # LDA #$80
        c.emit(0x8D, 0x01, 0xD3)           # STA $D301
        c.emit(0x68)                       # PLA
        c.emit(0x8D, 0x01, 0xD3)           # STA $D301
    c.emit(0xA9, 0x40)                     # LDA #$40
    c.emit(0x8D, 0x0E, 0xD4)               # STA NMIEN (VBI keeps running)
    # Spend the copy's ~6.9 frames as a delay instead of a transfer, so the
    # bank cadence matches `copy` while the animation keeps running.
    c.emit(0xA2, 0x80)                     # LDX #128 pages (~copy cost)
    c.label("outer")
    c.emit(0xA0, 0)                        # LDY #0
    c.label("inner")
    c.emit(0x88)                           # DEY
    c.branch(0xD0, "inner")
    c.emit(0xCA)                           # DEX
    c.branch(0xD0, "outer")
    c.emit(0x60)                           # RTS
    return bytes(c.finish())


def main_loop(banks: int, mode: str, codes: dict[str, int], clear: bool | None = None) -> bytes:
    if clear is None:
        clear = mode == "copy"
    c = Code(MAIN)

    def absolute(op: int, address: int) -> None:
        c.emit(op, address & 255, address >> 8)

    def call(address: int) -> None:
        c.emit(0x20, address & 255, address >> 8)

    call(INIT38)                           # display init + install the VBI
    if mode != "copy":
        # The copy path enables NMIEN itself at the end of the 16 KiB copy.
        c.emit(0xa9, 0x40)                 # LDA #$40
        absolute(0x8d, 0xd40e)             # STA NMIEN: allow the VBI to fire
    c.emit(0xa9, banks & 255)              # bank counter lives outside X/Y
    absolute(0x8d, COUNTER)
    if banks > 255:
        raise ValueError("bank count must fit in one byte")
    c.label("bank")
    call(WRAPPER)                          # display, text, copy, display, text
    if clear:
        call(CLEAR)                        # zero the staging buffer
    absolute(0xce, COUNTER)                # DEC counter
    c.branch(0xd0, "bank")
    # Replace the loading line with DONE and hold it.
    line = "DONE".center(40)
    for index, ch in enumerate(line):
        c.emit(0xa9, codes[ch])
        absolute(0x8d, DONE_TEXT + index)
    c.emit(0xa9, 0)                        # LDA #0
    absolute(0x8d, 0xd40e)                 # NMIEN=0: stop the loading VBI
    c.label("hold")
    c.jump(0x4c, "hold")
    return bytes(c.finish())


def alphabet() -> dict[str, int]:
    title = "THE LESS I KNOW THE BETTER"
    credit = "A\\SLOP BY OGNJEN / SILLY VENTURE 2026 WE"
    source = "BASED ON TAME IMPALA'S MUSIC VIDEO"
    letters = " " + "".join(sorted(set(title + credit + source + "LOADING. ") - {" "}))
    return {ch: i for i, ch in enumerate(letters)}


def skeleton(mode: str, banks: int, clear: bool | None = None,
             dummy: bool = False, portb: bool = False) -> bytes:
    out = bytearray(b"\xff\xff")
    out.extend(xex_segment(SCREEN, bytes(120)))
    out.extend(xex_segment(DLIST, bytes(28)))
    out.extend(xex_segment(INIT38, reference_payload(INIT38)))
    out.extend(xex_segment(WRAPPER, reference_wrapper()))
    out.extend(xex_segment(CLEAR, reference_payload(CLEAR)))
    out.extend(xex_segment(COPY, dummy_copy() if dummy else (copy_routine() if mode == "copy" else no_op_copy(portb))))
    # The OS calls INIT immediately after the $02E2 segment, so every target
    # (the main loop included) must already be loaded. $02E0 stays last.
    out.extend(xex_segment(MAIN, main_loop(banks, mode, alphabet(), clear)))
    out.extend(xex_segment(0x02E2, INIT38.to_bytes(2, "little")))
    out.extend(xex_segment(0x02E0, MAIN.to_bytes(2, "little")))
    return bytes(out)


def keep_animation(xex: bytes) -> bytes:
    """install() points the last wrapper's second refresh at `stop`; undo it."""
    out = bytearray(b"\xff\xff")
    for start, end, payload in segments(xex):
        if start == WRAPPER:
            stop = bytes((0x20, 0x20, 0x11))
            assert payload.count(stop) == 1, "unexpected wrapper patch"
            payload = payload.replace(stop, bytes((0x20, 0xa0, 0x38)))
        out.extend(xex_segment(start, payload))
    return bytes(out)


def without_init(xex: bytes) -> bytes:
    """Remove the wrapper's two per-bank $38A0 display refreshes."""
    out = bytearray(b"\xff\xff")
    for start, end, payload in segments(xex):
        if start == WRAPPER:
            assert payload.count(bytes.fromhex("20a038")) == 2, "unexpected wrapper calls"
            payload = payload.replace(bytes.fromhex("20a038"), bytes.fromhex("eaeaea"))
        out.extend(xex_segment(start, payload))
    return bytes(out)


def without_vbi(xex: bytes) -> bytes:
    """Static-screen variant: $38A0 returns instead of installing the VBI."""
    out = bytearray(b"\xff\xff")
    for start, end, payload in segments(xex):
        if start == INIT38:
            assert payload[-3:] == bytes.fromhex("4c0011"), "unexpected $38A0 tail"
            payload = payload[:-3] + bytes.fromhex("60eaea")
        out.extend(xex_segment(start, payload))
    return bytes(out)


def build(output: Path, banks: int, mode: str, no_vbi: bool = False, clear: bool | None = None, dummy: bool = False, portb: bool = False, no_init: bool = False) -> Path:
    data = animated_loading.install(skeleton(mode, banks, clear, dummy, portb), full_rate=True)
    data = keep_animation(data)
    if no_init:
        data = without_init(data)
    if no_vbi:
        data = without_vbi(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    meta = {
        "callback": MAIN,
        "banks": banks,
        "mode": mode,
        "vbi": not no_vbi,
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    output.with_suffix(".json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{output}: {len(data)} B; {banks} banks; mode={mode}")
    print(f"SHA-256 {meta['sha256']}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parent / "build" / "loader-clone-dev.xex")
    parser.add_argument("--banks", type=int, default=64)
    parser.add_argument("--mode", choices=("copy", "direct"), default="copy")
    parser.add_argument("--no-vbi", action="store_true",
                        help="skip the animated star VBI (static screen)")
    parser.add_argument("--clear", dest="clear", action="store_true", default=None,
                        help="force the $3A00 staging clear")
    parser.add_argument("--no-clear", dest="clear", action="store_false",
                        help="skip the $3A00 staging clear")
    parser.add_argument("--dummy-copy", action="store_true",
                        help="replace the 16 KiB copy with a timing-only delay")
    parser.add_argument("--portb", action="store_true",
                        help="direct mode: mirror the copy's PORTB sequence")
    parser.add_argument("--no-init", action="store_true",
                        help="skip the wrapper's per-bank $38A0 display refresh")
    args = parser.parse_args()
    if not 1 <= args.banks <= 255:
        parser.error("--banks must be 1..255")
    build(args.output, args.banks, args.mode, no_vbi=args.no_vbi, clear=args.clear, dummy=args.dummy_copy, portb=args.portb, no_init=args.no_init)


if __name__ == "__main__":
    main()
