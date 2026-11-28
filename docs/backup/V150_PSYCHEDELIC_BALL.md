> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V150 — psychedelic rotator and tunnel ball

## Image and animation

The ball has 16 distinct rotation phases instead of eight pulsing masks.
The silhouette remains a full sphere of constant size. The rotation happens
inside: a spherical projection with a tilted axis moves curved seams and colored
panels. A bright edge and a highlight in the upper part strengthen the reading
of a sphere. The seams change the panel color; they do not cut out
transparent pixels.

The four players have separate saturated hues, cyclically shifted around the
color wheel every 16 player ticks. Body/panel luminances are 8/10/14/12;
they distinguish the edge and the surface. The bright missile satellites keep
the previous two ellipses and positions. The new ball is shared by the banana
rotator and the tunnel, including their earlier range in act 2.
Music, trajectories, act boundaries and shot ticks are unchanged.

## Memory and update timing

[READ] Everything fits in the existing loader bank 2:

- `$7800–$7BFF`: code, palettes, coordinates, outlines and alignment.
- `$7C00–$7DFF`: 16×32 B of left-half panels.
- `$7E00–$7FFF`: 16×32 B of right-half panels.

Four PMG planes are prepared, but only two are stored.
The others are their complement inside a fixed silhouette mask (2×32 B).
The second half of the rotation switches the source page within the same bank.
Duplicated tables of satellites forming missile pairs were merged.

The helper is 2048 B instead of 2011 B, i.e. **+37 B**, with no new bank.
The total net recovery relative to v141 is **23 646 B = 23.09 KiB**.
Still 64 banks and 2515 B of main code (`$1400–$1DD2`).

The entry in the VCOUNT 124–127 window is preserved, the ball is not disabled
while waiting, and PORTB is restored. Clearing covers exactly 640 B of
PMG, in five runs of 128 B; duplicate writes of the shared range were removed.
As a result, the larger number of phases and the panel reconstruction do not
require a long rewrite of all four full masks from an additional bank.

[READ] py65, repeated callback 33024 → 33028: v149 8109 cycles,
v150 8211 cycles (+102). This is the CPU cost in this specific case,
without ANTIC DMA and without modeling real FPS.

## Validation

The tests check 16 distinct masks, a constant outline, full reconstruction of
all four planes from 6502 code, the colors, the motion, and the coverage of the
tunnel's central hole throughout the cycle. Regressions for late VCOUNT with an
artificial CPU halt, buffer handover and music NMI injection are preserved.

[READ] `make check`: **115 tests, 112 passed, 3 skipped**
(missing archival v126), 91.038 s.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **15 780 312
identical bytes** relative to v035; the comparison covers the whole track.
Without listening tests and verification on physical Atari. The CPU tests and
POKEY compatibility do not establish the real FPS or raster stability with DMA
on hardware.

## Release and previews

- `build/visual-prototype-v150.xex` and the corresponding JSON.
- `build/v150-ball-rotator.gif` — ball motion on the banana rotator.
- `build/v150-ball-tunnel.gif` — animation and colors in the tunnel.
- `build/v150-psychedelic-ball.png` — both effects side by side.
- `build/v150-ball-sheet.png` — 16 masks, a constant palette for comparing geometry.

The previews are produced after running the 6502 callback; colors and timing are
approximate. They are not an emulator recording or a smoothness measurement.

SHA-256 of the XEX: `0ec48a19fce0c8ec89909b30b7b18ec20e9046c37f86efeac56ac60f088b64ae`.
The numbered XEX/JSON files are identical to the working `visual-prototype-dev` files.
