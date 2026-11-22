# v040 — hair strands

The shifting of a large rectangular hair fragment, which tore the image, was
removed. The original silhouette and hair remain motionless relative to the
head; three narrow strands are anchored on existing pixels and have tips moving
independently in the vertical direction, with different phases. The shot is
still prepared as 18 frames: background and character motion, framing and scene
boundaries unchanged.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 51 tests PASS.
The tests cover fixed roots on the original pixels, strand continuity, three
tip positions for each strand, different phases and all frames of the shot.
Atari800 PAL 1088XE: 18 screenshots consistent with the generated frames.

[READ] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v040.xex --seconds 12`: 8 747 712 identical stereo POKEY
bytes, about 2436.7 s of emulation and the whole piece. Without a separate
listening session on a physical Atari. Preview: `build/v040-school-hair.gif`.

SHA256: `fb7487dc9731923fd51dd7b283c4210b689da7a1ed7acb99f4f035b1045da3f4`.
