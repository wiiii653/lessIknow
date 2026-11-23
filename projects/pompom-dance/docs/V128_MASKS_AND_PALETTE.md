# V128 — character masks and dance palette

[READ] `build/visual-prototype-v128.xex`, identical to the working build.

- Cheerleaders: a one-pixel outline instead of the two-pixel expansion of the
  upper part of the figure. Small closed mask holes in the area of the face
  and costume are opaque; larger gaps between the arms remain
  open. The coloured pixels of the source are preserved.
- Dance-only palette: PF0=$5A, PF1=$AC, PF2=$2E — brighter pink,
  turquoise and a warm skin/floor colour. The four ANTIC E colours remain
  shared by the hall and the characters.
- Trevor: readjusted outlines of the head, hair, shoulders, sleeves,
  fists and the bottom edge of both poses. Removed fragments of the old hall,
  refined the gap between the lowered fist and the torso.
  Mirror reflections use the same masks as the source images.

[READ] The generated poses and the raster after executing the callback were
checked visually: solo, duet, trio and both sides of Trevor's impact with PMG.
Preview: `build/v128-live-preview.png`. The PNG palette is an approximation of PAL.

[READ] Stereo POKEY comparison in Atari800 PAL/1088XE: PASS,
3 626 640 identical bytes, about 1010.2 s of emulation, the whole track.

The v126 comparison test accounts for the intended mask and palette differences;
the other scenes are still compared pixel for pixel. The current character tests
compare the raster with the current generated poses.

[READ] `make check`: 83/83 tests OK, 95.529 s.
