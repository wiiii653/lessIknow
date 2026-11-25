> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V091 — plasma color dithering

Transitions between the shades of the moving blobs use
an ordered Bayer 4×4 raster. The raster blends adjacent shades at their
boundaries, and its position is fixed relative to the screen. The effect is computed
at frame build time and uses the existing 16 frames and the same
banks; it does not increase processor work during playback. The dark
brightness, the raster reveal and fade, and the letter masks and their transition are preserved.

[READ] 69 py65 tests passed, including the raster distribution and
letter mask behavior test. [READ] A comparison of XEX v090 and v091 showed changes only in four
segments of the plasma frame banks; the remaining segments are identical.
[READ] Atari800 PAL, 1088XE, Altirra OS, stereo: the POKEY register recording was
identical to v035 for 6 047 640 bytes after a single alignment of the start;
the comparison covers the whole track. [CONCLUSION] This does not replace a listening test or an assessment
of the image on real Atari.

The programmatic preview `build/visual-prototype-v091-plazma.gif` has approximate
colors and pacing; it is not an emulator recording. XEX: `build/visual-prototype-v091.xex`;
SHA-256 `4de36c73b10fb178827663e93f740a3ec7fcb6a8bb10a38cb3b22553eeb3b2a7`.
