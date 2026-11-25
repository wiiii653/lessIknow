> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v347 — bubbles and pitch control

The side bubbles from v340 were restored, after being disabled by mistake in v346. The PMG render in py65 shows four bubbles at an age of 56 and 72 ticks; in the eyes shot the ball is selected. The appearance on hardware has not been verified.

The layup bank in v347 is identical byte for byte with v330. A py65 comparison of all 94 layup phases, with PMG, showed no pixel differences relative to v330. The cause of the reported artefacts on the pitch was not identified this way; an image of the problem is needed. Two layup scene tests passed. The director test requires the centre of the tunnel to be constantly covered also in the eyes shot, where the ball deliberately moves, and it reported an error there; the other three tests passed.

Stereo build `build/visual-prototype-v347.xex`; SHA-256 `51be93153eb50a50ac6c2dab90e9dc3555c523d6c093c9d46cc1db60cfc99641`. Generator: 298 shared rows and 2560 B of code. Neither the emulator nor physical Atari was run.
