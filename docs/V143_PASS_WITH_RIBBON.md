> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V143 — the girl and the ribbons crossing the frame

[READ] In the side shot 8975–11967 the girl moves from x=40
to x=128. The eight body positions and hall phases keep the existing animation.
The background still scrolls to the left; the character and her four players
and four missiles move to the right. The shift is 4 pixels every 128 ticks,
limited to 22 steps, with no wrap to the left edge at the end.
Scene boundaries and music ticks were not changed.

[READ] The banked side frames now contain only the background. The independent
masked characters are composed into the inactive bitmap by the unbanked
helper at `$0E00`. The eight actors have 2048 B each: pixels and a mask
preserving the background, cropping 68×56 from x=4/y=8, 17 bytes per row.
The data occupy `$4A00–$51FF` in loader banks 24–31. In those banks 512 B
of free slot remain; banks 32–39 keep the entire `$4A00–$53FF` free.

[READ] The cache also takes position into account. A shift with an unchanged
pose forces re-rendering of the background and the character; an HPOS change
is published with the complete bitmap/PMG in a bounded blanking window. PORTB
is restored by the NMI wrapper and the copy trampoline. The new helper does not
clear the active PMG.

[READ] Relative to v142: +16,384 B of character data, +256 B of runtime
reservation (`$0C00–$0EFF` instead of the end at `$0DFF`) and +92 B of controller
(1854 instead of 1762 B). The main code is still 2560 B. Net recovery remaining
relative to v141: **29,901 B = 29.20 KiB**. Still 64 banks. The separate
pom-pom project and earlier releases remain preserved.

[READ] `make check`: 101 tests in 84.063 s, 98 passed, 3 skipped
due to the absence of v126. The new test checks pixels at the beginning, middle
and end of the crossing, the consistency of all four anchors and the common
movement of the eight HPOS at the same animation phase. The tests also cover
writes only to inactive buffers and the music NMI during masked composition.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15,040,296
identical bytes relative to v035, the whole track. Py65: cold entry to the side
shot 80,681 cycles, position change 80,643; these are instruction costs without
ANTIC DMA, not an FPS measurement. No listening test or trial on a physical
Atari.

Release: `build/visual-prototype-v143.xex` with JSON.
SHA-256: `cd24ccf06843bc1ba833d8b4cf7380b1d0c89e286186a8c095fd422bc5759f22`.
The release and the verified working build are identical byte for byte.
Preview: `build/v143-side-crossing.gif` and `build/v143-side-crossing.png`.
The preview comes from successive 6502 callbacks every 16 ticks; the tempo and
palette are approximate, without modelling the copy time and DMA.
