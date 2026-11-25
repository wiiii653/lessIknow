> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V218 — motionless boy and terminal

From the first shot of the outro the boy remains in the same lower position.
After 59085 five lines of text get empty records; we do not restore the higher
framing. The same layout of 235 lines and the PMG offset of +32 lines apply until
the final fade. The full figure is preserved, without scaling. The upper horizontal
lines of the bitmap (source rows 5 and 9) were removed, leaving a black field.

Text: green phosphor (hue $C0, luminance $0E), dark background, 5×7 bitmap font
and `>` prompt characters. The headings were shortened to SONG / POKEY / MIDI, keeping the
names and authors. The text undulation remains. The terminal disappears with the fade;
there is no return of the figure upwards. The reset of the ordinary DL works only when leaving
the outro to an earlier scene, e.g. while scrolling back.

Ticks 53850 / 56842 / 59085 / 59833 and the four music interrupts remain
unchanged. No new banks were taken. Details of the base architecture and the
v216 verification: `V216_CREDITS_GREETZ.md`. CPU/ANTIC preview:
`build/outro-v218-preview.png` (reconstruction with an approximate PAL palette).

The first frame with the boy is not published in the old, higher layout.
Publication happens only after preparing a private DL at `$BC00`.
Packed data: 1752 B; loader: 362 B.

[READ] 40 tests of scenes, PMG, boundaries, budgets and regressions completed
successfully; after adding a check of the first publication, all 4 outro tests passed separately.
An earlier full run of v217 had one old assertion expecting `$8400` after the end of the credits;
it was adjusted to the constant `$BC00` and the retest passed within the set of 40 tests.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11,106,144 identical bytes
relative to v035, the whole track. The verification does not cover a physical Atari.
