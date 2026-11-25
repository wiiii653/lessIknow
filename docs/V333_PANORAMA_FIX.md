> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V333 — first scene panorama fix

Removed the extra shifting of the top ten rows of the arena panorama.
The shift covered the whole frame, so it detached the top of the head of the girl
walking in from the side. Panoramic frames again keep a consistent character position.

Stereo build: `build/visual-prototype-v333.xex` and the JSON next to it. Built 298
shared rows and 2560 B of code. No tests, emulator or
Atari were run; v330 remains the last hardware-confirmed release.
