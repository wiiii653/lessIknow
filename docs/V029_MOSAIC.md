> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v029 — demoscene mosaic

Replaces the former static image with row shifting with two geometric
motifs: rotating tiles with zoom and a twisted tunnel of rings.
64 frames 160×96, double line repetition by ANTIC gives a 160×192 image.
Contours, bright edges and dark gaps remain legible in four colors.
Brightness pulses according to the player clock, modulo 187 ticks. Palettes change
over time. Frames are generated mathematically at build time, without new
AI images and without trigonometric computations on the Atari.

Scene boundaries remain unchanged: the effect is used by the existing mosaic
dispatch in ticks 11968–14959 and from 32912. Later acts still use
this placeholder dispatch; this version does not implement their separate dramaturgy.
The effect selects a frame every 16 ticks (~80 ms), not 50 new frames per second.
The GIF shows frames produced by the 6502 code, with an approximation of the PAL palette.

## Memory and execution

- 16 new banks of 16 KiB each; 33 banks / 528 KiB of expansion in total.
- Four frames of 3840 B in each new bank: `$4000`, `$4F00`, `$5E00`, `$6D00`.
- Identical renderer in each bank at `$7C00`, to the end of the bank `$8000`.
- New PORTB selectors: `$08C3–$08D2`; region `$08C0–$08FF` excluded from the graphics pool.
- The extended probe alias checks all previously loaded banks,
  uses two markers and restores the probed byte also for a rejected candidate.
- `$24B6` is the preserved probe byte, `$24B7` is the temporary probe selector.
- ANTIC reads only non-banked RAM. Copying goes to the inactive
  buffer `$9000` or `$B000`; the DL switches in vertical blank.
- An unchanged frame skips copying. The cache of other scenes is invalidated.
- The ball, pom-pom and Trevor PMG remain in previous scenes.
- Main code occupies 1782 B (limit up to `$1B00`); exact value in the release JSON.

## Validation V5–V7

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 45 tests PASS.
The new tests cover all 64 frames, no writes to the active buffer,
cache, scene transitions, restart and the last bank while preserving the 32 earlier ones.
The music interrupt test also covers the mosaic: the foreground bank returns after NMI,
and the pixels remain consistent with the source. Cost of a changed frame below 90000
instruction cycles in the tested phases (without DMA/WSYNC and interrupts).

[READ] Atari800, PAL, `-1088xe`, Altirra OS, stereo POKEY: 89 memory
dumps, including all mosaic frames and transitions from the school, hall, portraits
and Trevor. Images read from the active DL consistent with the source graphics.

[READ] Full music register comparison:

```sh
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py \
  --demo build/visual-prototype-v029.xex --seconds 12
```

7 904 232 identical stereo POKEY bytes, about 2201.8 s of emulation, the whole track.
Registration every 78 lines confirms the behavior of four updates per frame.
This tests the digital register stream; it is not a declaration of listening on hardware.

[CONCLUSION] Buffering and banking of the new effect do not disturb the flow of
music in the verified configuration. Physical Atari XE 1 MB and Altirra were not
tested separately in this iteration.

## Release

```sh
make build/visual-prototype-v029.xex
```

The builder preserves existing XEX files and refuses to overwrite. v027 and the intermediate
v028 were preserved.

SHA256 v029: `c8a509af600bafa2c16e198cf5c2f90ecf2afb9f1a33fee81dee8540107543f7`.
SHA256 of preserved v027: `43c4e5bb2120325b0947b6221487cff01ca5a46b38c29669ccc9a1ea42df704f`.

Preview: `build/v029-mosaic.gif`, sheet: `build/v029-mosaic-sheet.png`.
