# V189 — restored basketball and backboard from v175

## Restored shots

The whole set of dribbling, feed and backboard-smash graphics was reproduced
directly from the preserved v175 XEX. The source of the current build is
`assets/art/reference/v175/basketball.bin`: 12 988 B from loader bank 1,
$4B80–$7E3B. That is five full 160×56 frames, three 44×28 arm patches
and three 48×24 smashable backboard patches.

The set reproduces eight original poses: four different hand phases during
dribbling, plus the preparation, jump, flight to the basket and dunk. The restored
backboard has the drawing, size and position of v175. The first crack,
the falling out of larger fragments and the shattering of the glass are exactly original.
The ball, its satellites, the moment the satellites turn into shards and the flash also
remain consistent with v175. The background comes from the same ATARI ARENA hall sequence.

Version v177 replaced the images without changing the mechanism for updating the small
arm area and without rearranging the glass patches. The new poses extended beyond
that area, two arm phases duplicated others, and the new smaller backboard
did not match the crack area. Reproducing the whole consistent set
removes these discrepancies; four previously failing basketball tests
now pass.

## Memory and smoothness

The restored four distinct arm phases improve motion legibility
without adding new data. The v175 tempo and key frames were preserved.
No new full frames were added: one costs 2240 B, and in the bank
there remain 85 B between code and DATA, 4 B before the orbits and 192 B at the end.

The change concerns only loader bank 1; the remaining 63 banks are identical
byte for byte to v188. The main code still occupies 2560 B, shared row data
11 480 B / 298 rows. No bank or decompression cost was added.
The v188 note-continuity fix and further scenes remain active.

## Build and check

- `build/visual-prototype-v189.xex` and JSON; dev identical.
- SHA-256: `5e597f13563f7b63657a2da29f92bbad4da87a3d981e7ee30ad427db896e8c05`.
- 23 focused tests passed: eight poses, both dribbling series,
  the dunk, all glass and shard phases, the finale, PMG continuity, comparison
  of raw data and of the running frames, ball and satellites with v175.
  Log: `build/v189-focused-check.log`.
- `make check`: 144 tests, 135 passed, 6 failed,
  3 skipped (missing v126). The four basketball errors from v188 disappeared;
  the rest concern the previously described ribbon/memory tests (4),
  the old act 5 threshold (1) and the CPU limit (1).
  Log: `build/v189-check.log`.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 992 848 identical
  bytes with v035; the whole piece. Log: `build/v189-playback-check.log`.
- Previews after 6502 callbacks: `build/v189-basketball.gif` and
  `build/v189-basketball-preview.png`. They do not model ANTIC DMA or the real
  FPS; no new assessment on a physical Atari was performed.
