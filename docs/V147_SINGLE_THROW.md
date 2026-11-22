# V147 — one wind-up and one throw

[READ] V146 used an eight-step sequence in the pre-flight wind-up, repeated
through most of the third shot. Despite a single final flight, this gave the
impression of repeatedly starting the throw.

[READ] It was replaced with a single run. After compression of the held frames,
the composition order is 8, 9, 35, 10, 11, 12, 13, 14, 15. No stage
appears again after moving on to the next. Position 35 is now
a small dip before the throw, instead of the large flight pose after which the
character returned to a smaller scale. The final close-up remains until the cut.

[READ] The shot still lasts from 17950 to 20942. The start of the flight and fireworks
remains at 20662; the earlier two shots and their dance are not changed.
The change concerns only the order table and the existing pose 35 bitmap.
The 6502 code, data sizes, 64 banks and the balance of 24 954 B recovered relative to
v141 remain unchanged.

The new test runs the actual 6502 controller through the whole third shot,
checks a single pass of all stages and the retention of the last frame.

Release: `build/visual-prototype-v147.xex` and JSON.
Preview: `build/v147-single-launch.gif`, played once.
The palette and pace of the preview are approximate; py65 does not model ANTIC DMA or
real presentation deadlines.

[READ] `make check`: 114 tests, **111 passed, 3 skipped**
(missing archival v126), 89,766 s. Atari800 PAL/1088XE, Altirra OS,
stereo POKEY: **14 837 040 identical bytes** relative to v035, the whole tune.
No trial and no listening on physical Atari.

[READ] The GIF does not contain a loop extension. The XEX is 1 109 034 B,
the same as v146. SHA-256:
`d4e3a7c3ab99de36c2c80703602d84e75f56f4354295a773514772ed097e85fc`.
The numbered release is identical byte for byte to the working build.
