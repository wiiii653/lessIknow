> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V159 — subtle dithering of the bananas and the tunnel fan

The bananas receive a sparse golden raster on the transition between the shadow
and the yellow surface. The 4×4 pattern is assigned to texture coordinates, so
it rotates together with the fruit. The black outlines and the crown of the
bunch are not changed.

The tunnel has a light raster blending two colours on a narrow band at the edge
of the fan arms. The threshold covers 3 of the 16 positions of the Bayer matrix
only in that band, not the entire surface. The pattern is fixed in screen space,
without randomness or alternating raster toggling between frames. The white
ridges, black gaps and the central hole are preserved.

## Scope and memory

[READ] Comparison of all 64 packed v158/v159 frames:

- Rotator: 8920 of 491 520 pixels changed, **1.81%**. Only yellow → gold; no
  black pixel is changed.
- Tunnel: 9796 of 491 520 pixels changed, **1.99%**. Only the blending of two
  colour fields; no black pixel or white ridge pixel is changed.

The bitmap/bank sizes and the Atari code remain identical. No additional RAM,
new banks, CPU cost of rasterisation or timeline changes. The PMG cycle of v158
and the opaque ball covering the centre are unchanged. The memory map and the
v158 balance remain current.

## Validation and release

`build/visual-prototype-v159.xex` and the corresponding JSON.
`build/v159-subtle-dither.png` shows both effects after the 6502 callback, with
an approximate palette; it is not an emulator recording.

[READ] `make check`: 122 tests, 119 passed, 3 skipped (missing archived v126),
90.768 s.
[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 9 833 112 identical bytes
relative to v035 over the entire track.

The py65 tests do not model ANTIC DMA or the actual FPS. Without a listening
test and a test on physical Atari; the absence of a random raster is not a
measurement of flicker on the target screen.

XEX SHA-256: `5f42b0f3d11381ed8e2193544f46fe9ea07315350cd253f88ce7ae4eec565997`.
The numbered XEX/JSON files are identical to the working dev ones.
