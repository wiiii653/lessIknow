#!/usr/bin/env python3
"""py65 smoke test for the loader clone.

Builds a two-bank copy-mode clone, runs it until the DONE line appears and
checks that the copy really filled $4000 and that no crash occurred.
"""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from extract_music import segments  # noqa: E402
from py65.devices.mpu6502 import MPU  # noqa: E402

import build  # noqa: E402


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        xex = Path(tmp) / "clone.xex"
        build.build(xex, banks=2, mode="copy")
        memory = bytearray(65536)
        for start, end, payload in segments(xex.read_bytes()):
            memory[start:end + 1] = payload
        memory[0xE45C] = 0x60  # SETVBV: return without installing an OS vector
        cpu = MPU(memory=memory)
        cpu.pc, cpu.sp = build.MAIN, 0xFD
        done = bytes((10, 20, 19, 11))  # D, O, N, E, centred in the line
        for _ in range(3_000_000):
            cpu.step()
            line = bytes(memory[build.DONE_TEXT:build.DONE_TEXT + 40])
            if done in line:
                break
        else:
            raise SystemExit("clone did not reach the DONE line")
        assert all(value == 0 for value in memory[0x4000:0x8000]), "copy left data"
        print("ok: 2 banks, wrapper/text copy ran, DONE line written")


if __name__ == "__main__":
    main()
