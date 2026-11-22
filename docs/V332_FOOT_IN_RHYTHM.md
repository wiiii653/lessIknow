# V332 — foot movement in the finale

The lying boy moves the tip of his foot on every beat, in time with the player clock.
The sway shifts a small pixel slice up by one image row and
back. It works without copying a full frame, additional banks or timeline
changes. The finale controller is 698 B; the foot routine takes 117 B in a free
slot of bank 49 before the orbit tables.

Stereo build: `build/visual-prototype-v332.xex` and the JSON next to it. It has 298
shared rows and 2560 B of code. SHA-256: `be6837b553940ddb1d4a0826961c679f892ed4c12c2d15c1945d3d5b56f2a053`.
Package: `build/visual-prototype-v332-stereo.zip`.
No tests or emulator were run;
v332 was not checked on a physical Atari. The last hardware-confirmed
version remains v330.
