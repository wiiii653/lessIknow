# Preserved v175 Frames

Extracted from `build/visual-prototype-v175.xex`, SHA-256:
`acb1f03deea22c6c747b5438b4dd75ad214ad834ca67be3365acbfcea0157675`.

- `arena-pan.bin`: 18 consecutive 160×64 frames, 2 bits per pixel, 2,560 B per
  frame. Extracted from loader banks 19–23 without controller code. The current
  build uses them to preserve the exact v175 walk cycle.
- `encounter.bin`: six encounter frames, 160×192, one colour index (0–3) per
  pixel. Reconstructed from row-address tables in the build JSON and XEX
  segments. This is a composition reference; the current build regenerates the
  frames with refined masks and the girl's path toward the door.
- `basketball.bin`: 12,988 B from loader bank 1, `$4B80–$7E3B`. Contains five
  full 160×56 frames (2 bits per pixel), three 44×28 dribble patches and three
  48×24 backboard-break patches. It reconstructs eight character poses and
  three glass-break phases. SHA-256:
  `c55b76ee9af23689177155f1ebc3aea84866f2733a47c82394ab17f2c009e09b`.
