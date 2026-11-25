> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V173 — polish of the solo transitions

## Change

I reworked four poses that entered v171/v172 in the middle of the solo's final
phase. They now match a specific movement between the previous intermediate
frame and the next accent: the arm dropping, the torso turning, rising
from a squat, and opening crossed legs into a wide stance. The hand
positions are computed from the new graphics, so the colored ribbons still land
in the hands.

The new sheet contains nine poses; the first four are used by the scene.
The other scenes, the solo length, the ticks and the girl's launch are unchanged.
Each new bitmap still occupies one of the tails of banks 32–35, which contain
the proper decoder. Stream sizes: 983, 1006, 986 and 970 B.
Free gaps in the banks: 27 323 B.

- Graphics: `assets/art/source/act2_ribbon_inbetweens_v173.png`.
- Prompt: `assets/art/source/act2_ribbon_inbetweens_v173.prompt.txt`.
- Preview of the four transitions: `build/v173-solo-transition-contact.png`.
  It shows the bitmap compositions and an approximate palette; it is not an Atari
  screenshot or a recording of the 6502 callback execution.

## Release

`build/visual-prototype-v173.xex`, 309 shared rows, 2552 B of code.
SHA-256: `d113a29be0b2bf391ffe39aef4d9b31c0b9339af45efc66816da56048877e70c`.

I did not run the py65 tests or the emulator in this iteration; `py65` is not
installed in the environment. Playback of v173 still needs to be confirmed.
