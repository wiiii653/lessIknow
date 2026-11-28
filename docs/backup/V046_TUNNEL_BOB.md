> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# v046 — ball sway in the tunnel

The ball at the end of the tunnel moves horizontally by at most five logical
pixels and vertically by at most four screen lines. Independent sine
trajectories create motion in different directions; four satellites move
together with it. Hardware players and missiles, rotation and rainbow colours
remain in use. The motion in the rotator and the transition moments remain
unchanged.

[READ] A 32-phase test checks every pixel of the tunnel's geometric hole
(`radius < 5` in texture space) for coverage by the masks of the four
players. The area is covered in all phases. 54 tests PASS:
`make check PYTHON=/tmp/tliktb-girl-venv/bin/python`.

[READ] Atari800 PAL 1088XE: 32 phase captures show the correct offsets
and the presence of the sprite and missile data. A stereo POKEY comparison
with the command
`APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v046.xex --seconds 12` gave 7 840 944 identical bytes
(~2184,2 s of emulation, the whole track). No separate listening test was
performed on hardware.
Preview: `build/v046-tunnel-bob.gif`, PAL colours approximated.

SHA256 XEX: `174064fc5525a5097869e609955467807532d647928245ce55ab57203d146bad`.
Previous XEX files preserved.
