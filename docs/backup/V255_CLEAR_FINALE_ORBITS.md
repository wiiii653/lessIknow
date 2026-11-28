> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V255 — a distinct change of path above the boy

[READ] Successive terminal lines still choose the orbit target of the stars/notes.
The eight shapes now go from a tall, narrow ellipse (radii
9 × 30) to a wide, flat one (30 × 9), instead of similar ellipses differing
mainly in angle. The change happens smoothly by one degree every 8 ticks;
the revolution phase remains as before, every 16 ticks. Neighbouring shapes
change the sprite coordinate by at most 4 units. Text, timings,
colours and fade preserved.

[READ] The finale tests check the difference of the extreme orbits, successive targets,
smoothness, the active buffer, the return to the scene and the text. No visual evaluation
on physical Atari; CPU tests do not measure ANTIC DMA or FPS.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 266 664
bytes identical with v035; the comparison covers the whole track.

[READ] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 197/197
cases, no skips; 150.166 s.
