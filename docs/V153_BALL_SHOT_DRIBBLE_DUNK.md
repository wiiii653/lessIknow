# V153 — shared neon ball for shot, dribble and dunk

Instead of the former stripes and transparent gaps, all three shots
use a full sphere: eight distinct rotation phases, curved coloured
panels, bright seams and a highlight, plus a darker edge. The look refers
to the larger v150 ball from the tunnel; the compact version keeps the size
needed for contact with the hand. The geometry does not pulse and does not
reveal the background.

Four co-located players have brightnesses 6/10/12/14. The colours cycle
through the Atari palette. The shot and bounce trajectories, hand anchors,
ball release, backboard shatter and the entire v151 timeline are preserved.

## Memory

[READ] The new masks are still **8 × 4 × 16 = 512 B**, exactly as much
as before. Both the throw helper (2235 B) and the hero (2652 B)
have unchanged length. It is the mask data and colour values that changed;
**the cost of additional RAM and new banks is 0 B / 0 banks**.

[READ] Still 64 banks, main code 2546 B, only 14 B before `$1E00`.
Net recovery relative to v141 is still 23 671 B (23.12 KiB). There is no need
to switch to the large-ball bank during the shot or the dunk.

## Validation

The tests check the eight distinct masks, the shared full silhouette,
non-overlapping planes, preservation of motion and colours, hand anchors,
all dunk and backboard shatter phases, mask restoration and PORTB.

[READ] `make check`: 116 tests, 113 passed, 3 skipped
(missing archival v126), 87.461 s.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
15 373 584 identical bytes relative to v035 across the whole track.
Without listening and without a test on a physical Atari.

The py65 tests do not model ANTIC DMA or the real FPS. The POKEY comparison
does not replace listening and image checks on a physical Atari.

## Release

- `build/visual-prototype-v153.xex` and JSON; identical to the working dev build.
- `build/v153-ball-shot.gif` — the shot.
- `build/v153-ball-dribble.gif` — the dribble.
- `build/v153-ball-dunk.gif` — the dunk.

The GIFs show the 6502 callback, with an approximate palette and timing.
The earlier v152 candidate is preserved; v153 removes the half-phase repeats.

SHA-256: `784b75809316314ba8e897736083bebb9c417a9e41875519b577f15f18c44a0b`.
