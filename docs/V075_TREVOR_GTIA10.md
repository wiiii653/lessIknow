> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v075 — Trevor in GTIA 10

[READ] The Trevor scene uses ANTIC F / GTIA 10 (80 × 192). The four original frames and the animated tunnel were converted to a palette with independent hues and luminances. The number of colours used depends on the shot. During a punch the image reserves the sprite colour registers for black letters and particles; the speech-bubble colour is shared with the GTIA 10 background register. The first PM colour is black to avoid a changing border colour, so the first projectile is dark. Scene timing and BANG behaviour are preserved.

[READ] Before a shot is displayed, its inactive display list gets mode F; the mosaic restores E. Trevor's and the mosaic's cache identifiers were separated so that the mode change happens on transition. The test covers a direct transition at the scene boundary and the behaviour of the musical DLIs.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 63 tests OK. `tools/check_playback.py --demo build/visual-prototype-v075.xex --seconds 12`: 8 371 872 identical stereo POKEY bytes; the whole track. The GIF preview comes from Atari800 7.2.1 (PAL, 1088XE, Altirra OS, turbo, no audio monitoring). Not tested on physical Atari.

[READ] `releases/visual-prototype-v075.xex`, SHA-256 `081fa9c9db74224164305cf1b2895c09efde5b992897ace1155bcc25a904a7d4`.
