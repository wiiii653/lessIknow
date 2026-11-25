> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v051 — Trevor's comic BANG

In the energetic part of the scene, at the pose with the fist pointing forward,
the former small sparks give way for a moment to a comic effect. The flash
grows, a black BANG! lettering appears on a flashing bright background, and the
whole thing breaks apart into a splash. The remaining moments of the scene keep
the sparks. The animated tunnel, Trevor, the cuts and the act boundaries remain
unchanged.

Four sprites form the letters, and four wide missiles form the shape of the
burst in fifth-player mode; its colour changes with the music clock. The phases
of the effect are tied to the player clock: ticks 0–15 rise, 16–95 lettering,
96–127 splash. The effect appears at the punch pose, then the sparks return.
After leaving the scene the previous sprites and missiles are restored. The use
of the fifth player and the priorities is described in the
[Altirra Hardware Reference Manual](https://www.atari800xl.eu/docs/reference/altirra-hardware-reference-manual.pdf).

The software preview was corrected so that with `PRIOR=$11` it first draws the
fifth player and then the letters on the sprites. The PAL colours in the preview
are approximate.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 57 tests PASS.
The tests cover all phases, the BANG! glyphs, the missile data, the return of the
sparks and the restoration of the dance scene PMG. Atari800 PAL 1088XE: PMG data
dumps during the rise, the lettering and the splash, and at the scene boundaries.

[READ] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v051.xex --seconds 12`: 8 224 920 identical stereo POKEY
bytes, about 2291.1 s of emulation, the whole track. Without a separate listen
on physical Atari. Preview: `build/v051-trevor-bang.gif`.

XEX SHA256: `2e05ae19460fcb15921634fd2ae40671e6cbd2e8808c376334e59632e0e81733`.
Previous versions preserved.
