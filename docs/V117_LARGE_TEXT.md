> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V117 — larger, high-contrast lettering on the plasma

TAME and IMPALA occupy two centred rows. The performer letters are twice as
wide and tall as in the single-row variant. The track title also has a greater
height. Letter fills are now uniform and differently coloured, regardless
of the plasma detail; narrow shifted edges have a separate colour.
Transparent pixels do not change the background, and the phases of raster reveal,
lettering swap and fade-out remain preserved.

The composition uses two 256-byte tables: the background-preserving mask and the
letter colours. The code reserve under the system ROM grew to `$E4C0–$ECBF`; the code and
its data end below `$EB9F`. No extension banks were added.
[READ] In isolated py65 a fresh title frame costs about 98–157 thousand
cycles depending on the fade mask. [CONCLUSION] The heavier phases may skip
animation steps on hardware; they require an evaluation of smoothness on the Atari.

[READ] 78 tests completed successfully, including the test of constant letter
colours over all plasma shades, of the two large rows and of the transitions.
[READ] Atari800 PAL, 1088XE, Altirra OS, stereo: after a single alignment of the
start, 6 131 448 POKEY bytes were identical to v035; this covers the whole track.

`build/visual-prototype-v117-tytul.gif` is a preview of sequential py65
execution with approximate colours and pace. XEX: `build/visual-prototype-v117.xex`;
SHA-256 `f03f4b1b340032e860298aa7e8c9d2607eb585482fc278daa3469782d2526622`.
