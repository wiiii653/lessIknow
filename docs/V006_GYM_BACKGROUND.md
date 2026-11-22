# Gym behind the cheerleaders — v006

Date: 2026-11-04. File: `build/visual-prototype-v006.xex`.

- [READ] Background in four colours: tall windows, roof structure,
  a basketball backboard with hoop and net, navy walls and a court floor
  with field lines. Geometry source: `tools/gym_background.py`.
- [READ] All non-zero pixels of the four poses are retained, and successive
  dancers appear at the original ticks. The PMG masks take the wall colour
  and cover only the dancers' area; they do not obscure the windows or the floor.
- [READ] Previews from executing the 6502 callback and reading the ANTIC lists:
  `build/v006-gym-solo.png`, `build/v006-gym-duo.png`, `build/v006-gym-trio.png`.
  The RGB colours are an approximation of the hardware palette.
- [READ] 19 tests passed, including scene transitions, full scanlines,
  DMA boundaries, no segment overlap, NORTH and memory below ROM.

## Memory and V2/V3 — player access control

- [READ] 835 unique rows, 31 173 B of data with alignment. Merging rows by
  shared endings/beginnings is lossless. The callback is 1135 B; the row tables
  take 3264 B.
- [READ] Additionally used: `$0600–$07FF`, `$08C0–$09FF`
  and `$1880–$18FF`. The divide-by-2 table is replaced by an LSR instruction.
  The music banks and the `$4000–$7FFF` window remain outside the image data.
- [READ] The original restart, decoder and DLI were run in py65 through
  59 833 updates to the end of the track, with reads and writes
  to the new regions forbidden: no access to those regions.
  Mechanism: `audit_music_banks.trace(..., protected_ranges=...)`.
  This is not a full verification of all PORTB behaviours from V2.

## V6 — playback regression

- [READ] Atari800, PAL, `-1088xe` extension, Altirra OS,
  stereo POKEY, headless. DLI still in lines 0, 78, 156, 234.
- [READ] Comparison of v006 with v035: **7 183 296 identical bytes** of
  stereo POKEY registers, about 2001.0 s of emulation, the whole track covered by the test.
  The initial silence was aligned once. No listening test or test
  on physical Atari was performed; DLI spacings were not changed in the V6 experiment.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v006.xex --seconds 10
```

## Preserved versions

- [READ] v035, the original prototype and v003 kept their previous SHA-256.
- [READ] SHA-256 of v006: `f261c0128dec5760c016c0fdd4553ebf3eb6701d11395fde3e03a224c9effbd5`.
- [READ] v004 and v005 are preserved intermediate builds of this change.
