> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# v042 — ball in the rotator and tunnel

The ball remains visible both in the tunnel and in the rotator. In the tunnel it
is in the centre. During the 1024-tick rotator phase it performs a full horizontal
swing: centre → right side → centre → left side → centre; the extreme deviation is
40 logical pixels. The movement and positions of the satellites are calculated relative to the ball.
At the boundary with the next tunnel it is back in the centre. The rotation, rainbow palette,
four players and four missiles are preserved; scene timings unchanged.

The table of 64 positions is indexed from the music clock, independent of the number of
renderer calls. The rotator bitmap frames and its existing colour sequence did not change.
The PMG routine in bank 17 is 1817 bytes and fits
within `$7800–$7FFF`. After leaving the scene, the dance
PMG graphics are restored.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 53 tests PASS,
including 64 fly-through phases, both extreme sides, the movement of all missiles with the ball,
the return to the centre, scene transitions and restoration of the dance sprites.

[READ] Atari800 PAL, 1088XE: 11 dumps covering the rotator
passage phases and the return to the tunnel, the positions and data of players and missiles.
Stereo POKEY comparison `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v042.xex --seconds 12`: 8 250 336 identical bytes,
about 2298.2 s of emulation and the whole track. Without a separate listening test on physical Atari.

Preview: `build/v042-rotator-ball.gif` (PAL colours approximate). XEX SHA256:
`70deb4337487574a6d40ce04535bf81e536abaa0cf3dd2550f2c3a0bab33581a`.
