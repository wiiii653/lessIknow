> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V100 — title typeface inspired by the original

The plasma lettering uses hand-built, thicker serif letters on
the GTIA 11 grid. Coloured faces and offset edges reference the colourful,
three-dimensional letters from the supplied image. They are an interpretation at Atari's
limited resolution, not an exact copy of the typeface. The letters remain part of
the plasma: no black panel was added, and the mask only changes the pixel shade.

TAME and IMPALA emerge in succession, but form a single line. An additional
raster phase lets successive words and lines emerge from the plasma gradually;
the performer's transition into the title and the constant plasma animation are preserved. The new
masks fit in the existing banks; the number of banks does not change.
Screen boundaries and music ticks remain the same.

[READ] 70 py65 tests passed, including comparison of the mask
of the coloured letters, partial emergence and plasma continuity between screens.
[READ] Atari800 PAL, 1088XE, Altirra OS, stereo: after a single start
alignment the POKEY register log was identical to v035 for 6 085 728 bytes;
the comparison covers the whole track. [CONCLUSION] The preview and the POKEY test do not replace
the evaluation of readability, smoothness and listening on real Atari.

`build/visual-prototype-v100-tytul.gif` is a programmatic preview with
approximate colours and timing. XEX: `build/visual-prototype-v100.xex`;
SHA-256 `d1aef662841f3dce0c66b07422214d44c4a273988a1084194679632da7a0551b`.
