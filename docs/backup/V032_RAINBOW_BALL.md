> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# v032 — rainbow ball and satellites

The ball in the tunnel has two bright, contrasting halves. Eight sets pass
through pink, purple, blue, turquoise, green, yellow, orange and red. The
satellites have a third shade, different from both halves. Ball luminance 14/12,
satellites 14; seams and outline black. The colours change every 32 player ticks.

The missiles are twice as wide (SIZEM `$FF`) and have more distinct tails.
Still four ball sprites, four missiles and a shared satellite colour in
fifth-player mode. The code in bank 17 at `$7800` occupies 1690 B, fitting within
the reserved 2048 B. No banks were added and scene boundaries were not changed.

## V5–V7 validation

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 48 tests PASS.
The palette test covers all eight sets, three distinct shades, minimum luminance
12, black seams and missile width. The remaining tests check masks,
transitions, the cache and bank behaviour during music interrupts.

[READ] Atari800 PAL, `-1088xe`, stereo POKEY, Altirra OS:

```sh
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py \
  --demo build/visual-prototype-v032.xex --seconds 12
```

8 417 160 identical stereo POKEY bytes, about 2344.7 s of emulation.
The entire track is covered by the comparison with the original. No separate
hardware test. The preview runs 6502 code; PAL colours are approximate.

- `build/visual-prototype-v032.xex`
- `build/v032-rainbow-ball.gif`
- `build/v032-rainbow-ball-sheet.png`

SHA256 v032: `43ce5f8cf4439c5f00d8c1907281d13b5d648cda6df56470dc154f973ac4791e`.
Preserved v031: `db98f9398570e10238a6a411734d7cb1ac9b52fac9cfef3c4885954c7913ade8`.
