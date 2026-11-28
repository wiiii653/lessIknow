> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V167 — rainbow cycle of tunnel reflections

After the Trevor scene, the colour of the bright tunnel reflections changes with each
new animation phase. The colour register `$D018` passes through 16 successive
colours from the existing palette, maintaining high brightness. The phase changes every
16 player ticks. The short tunnel flashback in act 3 still has a white flash;
the yellow colour of the banana bunch before the tunnel remains constant. Scenes,
ticks, image animation and memory allocation were not changed.

The change is in `tools/mosaic.py`. The expectation in the existing rotator
and tunnel colour test was updated in `tests/test_mosaic.py`; the tests were not run
in this change.

## Release

The XEX was built with the command `python3 tools/build_bitmap_sequence.py --output
build/visual-prototype-v167.xex`. The build completed successfully; the main
callback still has 2546 B. Playback on Atari800/Altirra and listening were not
verified in this change.

SHA-256: `fe7e0408d324f57649d0a2d0e796dcb1dc58242177b646ad194d07ba8d5fe4d0`.
