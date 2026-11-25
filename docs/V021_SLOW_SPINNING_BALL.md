> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v021 — one slow ball flight and spin

[READ] The shot still runs from tick 6981 to 7978. The flight uses the
full 16-bit time from the start of the shot: phase = (tick − 6981) >> 3,
0–124. The ball flies once, from the hand to the hoop, over about five seconds.
There is no repetition, no falling and no second bounce in this shot.

[READ] The size grew from 8×16 to 16×32 logical pixels:
the players are double width, and the mask has 16 double lines.
Eight frames change the position of the curved seam, the equatorial seam
and the coloured panels. The mask geometry rotates, alongside an independent
change of the four GTIA colours. The missiles still draw coloured droplets.

## V1 / V6 — verification

[READ] 34 tests OK: movement throughout the shot, no restart after 256,
512 and 768 ticks, the new size, and eight different rotation masks.
Background behaviour and the recreation of the dance scene PMG were also
checked. In Atari800 PAL `-1088xe`, nine phases were verified from the start
to the last tick of the shot, plus the next shot and the return to the dance.
The phases in the screenshots agree with the full time from the start of the throw.

[READ] Full stereo POKEY comparison with the original:
8 980 704 identical bytes, about 2501.6 s of emulation.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v021.xex --seconds 12
```

[ASSUMPTION] Verification on physical Atari remains. The GIF approximates PAL
colours and pixel proportions: `build/v021-slow-spinning-ball.gif`.
Earlier XEX files were kept.
