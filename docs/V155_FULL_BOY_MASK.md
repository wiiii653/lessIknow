> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V155 — full boy mask in front of the arena

## Cause and fix

The environment swap in v151 determined the boy mask by selecting connected
colour regions. The black interior of the hair was not correctly closed by the mask,
and the magenta of the jacket could belong to the same component as the old court.
The rejected regions were replaced with arena graphics, producing transparency.

`arena_art.portrait()` now uses the full silhouette mask, independent of
pixel colour. The black of the hair and the magenta of the jacket remain opaque. The mask
also covers the cut-off right edge of the character on screen. The fix applies to
both of the boy's poses and to the scenes with the girl walking away. The masking of
the basket, the player inside, the girl and any ticks were not changed.

## Memory

[READ] The change concerns asset composition during the build. No new Atari
code and no additional banks. Still main 2546 B, hero 2652 B,
64 banks. The packed rows occupy 10 764 B instead of 10 927 B in v153,
i.e. 163 B less. Recovery relative to v141: 23 834 B (23.28 KiB).

## Validation

The new regression executes the callback of both poses and compares the hair and
jacket regions, including the black and the right edge, with the original pixels.
Preview after the callback: `build/v155-opaque-boy.png`.
The preview palette is approximate; this is not an emulator capture.
The CPU tests do not model ANTIC DMA or the real FPS. No listening test
or test on physical Atari was performed.

[READ] `make check`: 117 tests, 114 passed, 3 skipped
(no archived v126), 87.656 s.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 573 016 identical bytes relative to v035 across the whole track.

## Release

`build/visual-prototype-v155.xex` and JSON; identical to the dev working files.
The working numbered v154 remains preserved; v155 also covers the full right
edge of the silhouette.

SHA-256: `faa9c90b7bf141f96a9ba342d246c025562a8d5855a91b384c2c53b5a5578b91`.
