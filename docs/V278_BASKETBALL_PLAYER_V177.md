> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V278 — basketball player v177 in the dribble and the dunk

Six poses from the v177 RGBA layer are composited onto the existing ATARI ARENA
background. The dribble uses three full poses: starting position, second
position, crouch and return through the second position. The dunk gets the
crouch, two flight phases and a final pose. The timing of the shots and of the
ball does not change.

Version v177 used too small a patch for whole poses. In v278 the two additional
full frames (2 × 2240 B) occupy the previously empty `$4A00–$52BF` and
`$5300–$5BBF` in loader bank 0. The helper `$EC80–$ECDC` copies them into the
inactive buffer; it preserves and restores the bank. Separate patches for the
cracks in the table account for the character pixels. No bank was added. The
basketball player bank code occupies 2926 B (`$4000–$4B6D`), ending before the
data at `$4B80`.

[READ] The targeted tests cover all poses during the dribble, the dunk and
backboard frames, the invisible buffer, and music interrupts in the middle of
copying. Atari800 PAL/1088XE: 16 302 960 identical stereo POKEY bytes against
v035, the full track.
[READ] Full suite: 200/200 tests in 145.144 s. The additional test of interrupts
during a full copy also passed.

[LIMITATION] CPU/py65 does not model the ANTIC DMA load and is not an FPS
measurement. No listen or image evaluation was performed on physical Atari. The
buffer is larger than the old hand patch, so the actual smoothness should be
evaluated on the target hardware.
