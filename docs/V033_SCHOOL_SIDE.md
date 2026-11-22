# v033 — side shot in front of the school

The cut in ticks 3553–4113 shows a blonde girl in profile, mid-step, in front of
the school. It is a static frame depicting motion, not a walking animation.
The original cut ended at tick 3927; extending it by 187 ticks (~0.94 s)
shortens the boy's shot after it. The girl enters the foreground at the
previous tick 4488, the remaining scene boundaries are unchanged.

Source: `assets/art/source/act1_girl_side_walking_v033.png`. Generated from the
existing school and girl illustrations, with a mid-step profile, in a European
comic style and a palette of black, cyan, pink and light peach. The frame is
rescaled to 160×64 and displayed by the existing renderer.

[READ] 48 tests PASS (`make check PYTHON=/tmp/tliktb-girl-venv/bin/python`),
including the cut boundaries and those of the adjacent shots. Atari800 PAL
1088XE, stereo POKEY: `tools/check_playback.py --demo build/visual-prototype-v033.xex --seconds 12`
with `APPIMAGE_EXTRACT_AND_RUN=1`: 8 606 664 identical register bytes,
~2397.5 s of emulation, the full track. No listening test on physical hardware
was performed.

Preview: `build/v033-girl-side.png`. XEX SHA256:
`3b47be7910e46ba2537ac0cee18a0eb91e0eaf066ed9f3bd1161c72de5725fd9`.
