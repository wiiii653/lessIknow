> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V149 — compact Crane and fireworks in front of the image

## Change

At the user's request, the left tower of the historic Crane is connected
to the body with a continuous gate wall. The gap with moving plasma was
eliminated. The whole silhouette was reduced from 40×32 to 36×29 source pixels
on an 80×64 grid; position (22,35) preserves the centring and the quay at the
bottom. Two masonry towers, the roofs, the wooden jib and the contrast of the
cool wall with the warm roofs and the outline remain.

The fireworks of both intro screens now have four phase-shifted cycles:
rocket ascent with a tail, a central flash, a radial bloom, falling and fading
fragments. The missiles have a longer vertical trail range. The colours still
change cyclically and are subject to the screen fade-out.

Clipping of the shapes to the captions, their shadows and the Crane silhouette
was removed. Complete players and missiles are in front of the plasma, the
letters and the building, with `PRIOR=$C1`, without fifth player mode. This
deliberately replaces the caption and building protection from v140/v144. The
order of entries I KNOW → THE BETTER → THE LESS, the final text layout and all
scene ticks remain unchanged.

## Memory and code

[READ] Loader banks 40 and 41 have the same controller and shapes:

- Code 1356 B: `$6C00–$714B`, publication entry `$7000`.
- Vertical anchors: `$73F8–$73FC` (5 B), moved before the old end of data.
- Shapes: `$7400–$7FFF` (3072 B). Four players with 16×32 rows each;
  a shared missiles plane of 16×64 rows, with a separate address table.
- The installer checks the separation of code, anchors and data and the empty
  target space. The new shapes add nothing beyond the end of the bank.

[READ] Cost relative to v148: 2×(512 B of shapes + 32 B of tables) = 1088 B.
Still 64 banks. The net recovery relative to v141 is **23 683 B = 23.13 KiB**.
The Crane graphic fits within the existing plasma frames. The main code is still
2515 B (`$1400–$1DD2`), with 45 B before the pool from `$1E00`.

Preparation of the effect keeps the inactive PMG buffer, and publication takes
place in a bounded VCOUNT 124–127 window. Four music updates per
PAL frame and PORTB restoration are preserved.

## Validation

[READ] The intro tests check the continuity of the left tower connection,
the size of the building, the preserved caption order, complete shapes in both
banks, the overlaying on the letters and the Crane, the falling/shrinking of
late sparks, the ownership of the PMG buffers, PORTB and the publication under
a moving VCOUNT.

[READ] `make check`: **115 tests, 112 passed, 3 skipped**
(missing archival v126), 90.781 s.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **15 348 384
identical bytes** relative to v035; the whole track covered.

Previews after the execution of the 6502 callback: `build/v149-intro.gif` (both
captions, a single replay) and `build/v149-zuraw-fireworks.png`. The palette and
tempo of the previews are approximate. This is not an emulator recording, an FPS
measurement or a raster check on physical Atari. The POKEY comparison does not
replace listening.

## Release

`build/visual-prototype-v149.xex` with the corresponding JSON; identical
to the `visual-prototype-dev` working files.

SHA-256 XEX: `f57e236d15a2fd910c84a4a50ef1d6b5a1391ea63bb1fb2c4f43737ab9f35465`.
