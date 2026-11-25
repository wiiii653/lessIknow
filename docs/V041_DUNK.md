> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v041 — dunk pacing and hand tracking

The dunk shot keeps ticks 22440–23935. The preparation lasts 752 ticks,
the next two in-flight poses 224 ticks each, and the final pose 296 ticks. Pose
changes are synchronised with the existing music clock. These are four
illustrations; the acceleration of the action was achieved by cutting them together,
without additional drawing frames.

The centre of the PMG ball is pinned to the hand separately in each of the four poses:
(85,102), (99,28), (115,18), (124,32), in logical 160×192 coordinates.
After the hold at the rim the ball falls; the flash occurs on release.
The ball keeps the coloured sprites and missiles.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 52 tests PASS,
including the ball positions at pose boundaries, the release moment, a single fall,
scene transitions and PMG playback after a restart.

[READ] Atari800 PAL 1088XE: 11 screenshots of the dunk phases, correct poses,
ball coordinates and PMG data. `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py
--demo build/visual-prototype-v041.xex --seconds 12`: 9 203 904 identical
stereo POKEY bytes, about 2563.8 s of emulation, the full track. No separate
listening test on a physical Atari was performed.

Preview: `build/v041-dunk.gif`. XEX SHA256:
`6728426166c4151323cb9ccd4def6a81cd00c2d15599eab12a1991d04bc541ee`.
