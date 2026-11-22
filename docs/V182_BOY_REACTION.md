# V182 — look, turn and whistle

The boy's reaction is divided into three separate poses, while preserving
the framing and the girl's path from v181:

| Tick | Reaction |
|---|---|
| 2992, 4114 | Looks straight ahead; source `act1_boy_front.png`. |
| 4488 | Turns to look while passing in the foreground. |
| 4862, 5236 | Still looking after the departing girl. |
| 5610 | The girl is at the door: pout, wink and musical notes. |

The calm turned pose uses `act1_school_court_boy.png`, and the whistle
`act1_boy_front_v170.png`. All portraits go through the current
mask protecting the hair and jacket and the arena sign. Notes are added only
to the last pose. The side walk still matches v175 exactly.

- XEX: `build/visual-prototype-v182.xex`; the dev pair is identical.
- SHA-256: `6675f18047cd8e8c4e6b2dca97b80d1acce8da9a7202ab4e1a7a1544385e7d6f`.
- 316 shared rows, 12 153 B of row data, 2552 B of code.
  The generator completed allocation within existing regions. No banks were added.
- Seven CPU/rendering tests passed: the order of the three poses and the notes,
  the hair/jacket coverage, the accuracy of the v175 panorama and its clock, the composition,
  the foreground and the path to the door.
- Preview after the 6502 callbacks: `build/v182-boy-reaction-preview.png`.
  Does not model ANTIC DMA. No new playback was performed in the emulator;
  the Atari800 installation has a known FUSE obstacle described with v181.
- The ticks and shot boundaries and the further acts remain unchanged.
