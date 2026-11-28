> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V169 — new tunnel texture in act 5

## Change

In 5B the tunnel uses spiral bands from tick 38892. Exactly at tick
40388, in bar 108, it changes into a radial grid of stars with eight
spinning rays and concentric rings. The change applies
until the end of the 5B range at tick 41884. Shot boundaries, animation tempo and the ball
obscuring the centre of the tunnel remain unchanged.

Both variants share the existing 32 tunnel frames: 32–47 store the
spiral, 48–63 the new grid. They are selected by a compact 16-bit tick
dispatcher. In the generator `tools/mosaic.py` the patterns are computed for
the same four-colour bitmaps; no frames or bank allocations were added.

## Memory and validation

- All 64 banks still allocated; entirely free banks: 0.
- Confirmed gaps in the used banks: still 31,623 B according to the v166 map.
- Main code: 2552 B of 2560 B available before `$1E00`; 8 B spare.
- The build of `build/visual-prototype-v169.xex` completed correctly.
- No py65 tests, music comparisons or playback in Atari800/Altirra were
  performed in this change.

SHA-256 of the XEX: `05f1c69517d4b1f459fec5b4183e59266392d9e169c72f4b6f4b3e35b9939b8e`.

Detailed map of allocations and fragmented gaps: `MEMORY_MAP_V168.md`.
