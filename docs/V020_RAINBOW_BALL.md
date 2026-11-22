# v020 — rainbow ball on PMG

[READ] The effect is active only in the throw shot: ticks 6981–7977.
The stationary ball was removed from the converted background. Four players
make up four bands of the ball; each has its own cyclically changed GTIA
colour. Four missiles form three coloured droplets each. Along an arc the ball
falls into the area of the hoop, drops and bounces. The sequence lasts 256 ticks
and repeats during the shot. Scene events remain unchanged.

## V1 / V2 / V3 — engine

[READ] The effect runs in vblank, also on a background cache hit.
A sample shot hold costs about 6100 py65 instruction cycles,
without DMA and NMI. There is no further bitmap copy or list building.
The additional bank 15 now has 16 KiB: the school portrait in the first 8 KiB,
the ball routine at `$6000`, PMG restore at `$6F00`.
The wrapper saves and restores PORTB; the NMI preserves the bank of the
interrupted code.
PMG uses `$0980–$0BFF`, double line height, four players
and four missiles. On leaving the shot the original dance-scene flash data
returns, also on a clock jump.

## V6 — verification

[READ] The 32 tests cover movement, four simultaneous colours, palette change,
four droplet streams, bitmap hold and restoration of the dance PMG.
In Atari800 PAL `-1088xe`, captures of several throw phases were checked, as
were neighbouring shots, the school cut-in and four later frames of the
performance.

[READ] The full stereo POKEY recording matches the original:
9 143 784 identical bytes, about 2547,1 s of emulation.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v020.xex --seconds 12
```

[ASSUMPTION] The GIF colours are an approximation of the PAL palette. Physical
hardware remains to be verified. Preview: `build/v020-rainbow-ball.gif`.
