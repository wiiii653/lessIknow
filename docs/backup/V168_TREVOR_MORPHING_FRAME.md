> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V168 — morphing frame behind Trevor

The geometric tunnel bands behind Trevor smoothly change shape within the
existing 16 background phases. The square/rectangular perspective transitions
into an oval and returns to a rectangle at the cycle wrap. The morph is based
on interpolating the rectangular and the normalised elliptical norm. The motion
is only in the background: the character bitmap, its outline, the punches,
colours and ticks remain unchanged.

The change is in `tools/trevor_polished.py`, in the `tunnel_frames` generator.
It uses the already generated phase banks; it adds no data, runtime code or
banks.

## Release

The XEX was built with the command `python3 tools/build_bitmap_sequence.py --output
build/visual-prototype-v168.xex`. The build completed successfully; the main
callback is still 2546 B. No tests or video playback in the emulator were
performed in this change.

SHA-256: `cec65fb359440302247341403ba7f7bd9ce2eca8b58fa83c874b5815b320bcb5`.
