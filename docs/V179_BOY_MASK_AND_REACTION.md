# V179 — opaque silhouette and reaction after the transition

V179 completes the portrait mask in `arena_art.actor_mask()`: black pixels of the
hair and of the contour inside the silhouette guide mask are now preserved as
opaque. The coloured elements of the character still use selection of
coherent regions, which keeps the sign and background clean outside the boy.

In the first wide shot the boy remains in a neutral pose. When the
girl walks through the foreground, her subsequent shots are already combined
with the portrait in which the boy winks and purses his lips; that is also when
treble clefs and notes appear. The existing shots, ticks and scene boundaries were preserved.

- Preview of the composition frames: `build/v179-opening-frames.png` (this is not
  an emulator capture).
- XEX: `build/visual-prototype-v179.xex`.
- 286 shared rows, 11 034 B of row data, 2 552 B of code.
- SHA-256: `c6bde5abaaa7d5a472d975c811b2c2f82c61c9d212e3ef8a9772ff1a106fb101`.
- Build completed successfully. Neither tests nor emulator playback were
  run.
