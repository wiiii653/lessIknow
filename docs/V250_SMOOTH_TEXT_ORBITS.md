> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V250 — smooth orbits on new terminal lines

Each of the 34 printed credits/greetz lines chooses a new orbit shape for the
stars and notes. The target differs both from the current shape and from
the previous target. The horizontal and vertical radii change by one degree every
16 ticks, without a jump in position. A repeated callback in the same
tick does not accelerate the change. After the last line the orbits still circle; fade,
colours, the boy's bitmap, the content and all scene boundaries are preserved.

## Memory and verification

The helper, the timings of the 34 lines and the tables of eight shapes take 600 B in bank 49
`$66A0–$68F7`, after the Trevor helper ending at `$6697`. The current positions
and state are in `$69B8–$69C3`, before the existing data `$69C4`. The installer
checks both areas. The helper uses `$0DD8–$0DD9` as scratch before a separate
terminal call, which then uses the same bytes. The finale controller has 700 B, still fits within its
existing range; main remains 2560 B, the number of banks 64. PMG data
is prepared in the inactive buffer and published in the blanking window.

[READ] The test models all texts, the rate of change, repeated callbacks,
the return to the scene and the positions of the four sprites. The other tests cover PMG
shapes, fade, the exit to black, VCOUNT and the music NMIs.

[READ] In 128 callbacks from the finale entry, after discarding initialisation,
the average cost rose from 10 295 to 10 978 py65 cycles; the maximum from 10 371 to
11 054. This is CPU cost without ANTIC DMA, not an FPS measurement.

[READ] Atari800 PAL/1088XE stereo POKEY: 16 306 560 bytes identical
with v035 throughout the whole track. Without listening or testing on physical Atari.

[READ] Full `make check`: 192/192 tests, 151.229 s. The additional test of the
maximum shift between neighbouring shapes passed separately.
