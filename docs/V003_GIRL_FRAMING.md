# Correction of the girl's first frame — v003

Date: 2026-11-04. Result: `build/visual-prototype-v003.xex`.

- [READ] First sprite setting: `(0, 0, 96, 128)` on a 160×64 canvas.
  The bottom edge shows the source down to row 31, that is, down to the waist.
- [READ] NORTH: 3×4 font, origin `(14, 15)` in a 48×64 source.
  The whole text rectangle fits inside the original turquoise jacket panel.
- [READ] 18 tests completed successfully, including 6502 callback execution,
  framing, the text, zooming out, memory under ROM and the original music banks.
- [READ] Preview made from the image list of the new XEX:
  `build/v003-school-girl-waist.png`.

## V6 — rhythm regression (without changing DLI spacing)

- [READ] Atari800, PAL, `-1088xe` (1088XE expansion), stereo POKEY,
  Altirra OS, headless. Comparison with the original v035: 10 478 232 identical
  bytes of stereo POKEY registers (~2918.8 s of emulation), covering the whole track.
  DLIs remain on lines 0, 78, 156, 234. No listening test or test
  on a physical Atari was performed. This is a regression test, not an experiment with changing V6 spacing.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v003.xex --seconds 15
```

## Preservation of previous files

[READ] SHA-256 after the change match the readings before the work:

- `build/visual-prototype.xex`: `41f1ef9bb4156d8466b32cce17f1d2ca132b3b443742654d16c841c0988802b9`
- `less-i-know-release-v035.xex`: `6d5d9cf3004f9003ede8d91aa4891a100f672c5a0e9429a6ecf20d1f5fef0ff0`

New XEX: `04a398c7b38497055827f229a5fb0550d0bedde5be61c56319a3b1ba2351650e`.
The generator refuses to write under an existing XEX name; the next version requires
a new path via `--output`. v002 is the preserved intermediate build of the correction.
