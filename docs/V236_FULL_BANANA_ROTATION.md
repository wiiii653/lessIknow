> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V236 — full, continuous banana rotation

## Causes

1. `mosaic.pixels()` computed a 0–2π phase, but divided the rotation angle by 4.
   All 32 bitmaps therefore covered only 90°. The 31 → 0 wrap
   jumped from 87,1875° to 0°, instead of continuing the motion. The asymmetric
   bunch tile has no quarter-turn symmetry, so the jump was visible.
2. The act 5 dispatcher masked the phase with 15, looping 0–15 separately
   and, after tick 34404, appending bit 16 and looping 16–31. This meant a reset
   every 16 frames plus an additional jump at the bar 92 boundary. Fixing the
   angle in the artwork alone would not remove these resets.

## Fix

The angle is now the full phase, without dividing by 4. The existing 32 frames
cover 360° in 11,25° steps; the 31 → 0 wrap is the same angular step as the
others. The zoom keeps the previous sine.

Act 5 takes all five phase bits (`AND $1F`) and there is no splitting of the
animation at bar 92. At 34403 and 34404 it displays the same phase 6, instead
of a jump 6 → 22. The next phase 7 appears normally at 34416.

Scene boundaries, rotator placements and the v231 tunnel montage were not
changed. The bunch tile, the gold/yellow palette, the absence of dithering and
the ball graphics remain. The eight banks with both tunnel textures are
identical to v235. The banked banana helpers also remain identical; only their
bitmaps and the main phase selection in act 5 changed.

## Memory

Still 32 banana frames and the same bank allocation. No PMG data or tables were
added. Removing the half-cycle logic shortens the main code by **30 B**:
now 2521 B, i.e. 39 B of headroom before $1E00.

## Verification

[READ] 44 targeted tests passed. The new regressions check the
0/90/180/270° orientations, continuous visiting of all 32 phases in act 5,
the absence of a reset at mid-rotation and at tick 34404, and the natural wrap
of the last frame. The comparison test against v198 retains the PMG and banana
palette check wherever the old and the new clock select the same phase.

[READ] The eight tunnel banks and the helpers of the eight banana banks were
compared directly with v235 — byte-identical.

[READ] Atari800 PAL/1088XE, stereo POKEY: **11 186 424 bytes identical
to v035**, the whole track. No test on physical Atari.

[READ] The full run passed the 174 existing tests (117,8 s).
The new module had an import-order bug during discovery without PYTHONPATH;
after fixing the import of `test_sequence` before `mosaic`, separate discovery
passes 3/3 new regressions (2,6 s). In total all 177 cases were verified. The
XEX required no changes afterwards. The working build is identical
to v236; SHA-256:
`63bce85afb9d3b1e792c29fb308e969b7a5e36b9f59e1bbee37addf0400ce764`.

CPU/PMG previews: `build/bananas-v236.gif` (two full rotations, including
the 31 → 0 transition) and `build/bananas-v236-cardinals.png` (four orientations).
