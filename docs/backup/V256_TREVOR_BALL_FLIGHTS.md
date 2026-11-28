> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V256 — Trevor's ball flights

[READ] Two visible problems in the ball arrival and departure were fixed:
the paths no longer reach the vertical limiter and do not slide
for several steps along its edge. At the start of the arrival and the end of the departure
the brightness of the balls and their satellites gradually fades, instead of appearing or
disappearing at full brightness on screen. For all 13 punches, separate directions were kept
in each phase; the arrival and departure directions may
repeat between phases. The geometry of the balls and satellites, the anchors, the positions
of the punches, BUM/BAM and their ticks remain unchanged.

[READ] The change is limited to loader bank 19. The helper is 1931 B
(`$6800–$6F8A`), leaving 117 B before `$7000`. The tests cover all
punches, the absence of reaching the limiters, brightness at the boundaries, the inactive buffer,
blanking and music NMI in both flights. The rendered py65 preview does not model
ANTIC DMA; no visual listening/viewing or hardware test was performed.

[READ] Preview of selected 6502 callback frames with an approximate palette:
`build/v256-trevor-flight-preview.png` (it is not an emulator capture).
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 322 616 bytes
identical to v035; the comparison covers the whole track.

[READ] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 199/199
tests, no skips; 152.424 s.
