> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V335 — static foot in the finale

The foot animation and the additional helper in the bank 49 gap were withdrawn.
The last scene returns to the static boy graphics from v330. The heart and panorama
fix from v333–v334 remains.

Stereo build: `build/visual-prototype-v335.xex`; SHA-256:
`7145dd1ec6b1bccc7c5121392bb11b0da9ea676877c89432b6fde44030873f5d`.
The build keeps 298 shared rows and 2560 B of code. No tests, emulator or Atari run
was performed; v330 remains the last hardware-confirmed version.

The foot movement did not consume a free bank: its 117 B lay in the gap of an already
allocated bank. It also should not affect the loader, because the helper is
called only in the finale. The production `loading_screen.py` shows a constant
`LOADING BANKS` caption; the animated dots are in a separate diagnostic tool
`build_init_trace_high.py`.
