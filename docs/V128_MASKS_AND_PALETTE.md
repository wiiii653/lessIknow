# V128 — character masks and dance palette

[READ] `build/visual-prototype-v128.xex`, identical to the working build.

- Cheerleaders: one-pixel outline instead of a two-pixel extension
  of the upper part of the silhouette. Small closed mask holes in the face
  and costume area are opaque; larger gaps between the arms remain
  open. Colored source pixels are preserved.
- Dance-only palette: PF0=$5A, PF1=$AC, PF2=$2E — lighter pink,
  turquoise and a warm skin/floor color. The four ANTIC E colors remain
  shared by the hall and the characters.
- Trevor: re-fitted outlines of the head, hair, shoulders, sleeves,
  fists and the lower edge of both poses. Removed fragments of the old hall,
  refined the gap between the lowered fist and the torso.
  Mirror reflections use the same masks as the source images.

[READ] Visually checked the generated poses and the raster after executing the
callback: solo, duet, trio and both sides of Trevor's hit with PMG.
Preview: `build/v128-live-preview.png`. The PNG palette is an approximation of PAL.

[READ] Stereo POKEY comparison in Atari800 PAL/1088XE: PASS,
3 626 640 identical bytes, about 1010.2 s of emulation, the whole track.

The v126 comparison test takes into account the intended mask and palette
differences; the remaining scenes are still compared pixel for pixel. The current character
tests compare the raster with the currently generated poses.

[READ] `make check`: 83/83 tests OK, 95.529 s.
