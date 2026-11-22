# V135 — stable ball and satellite PMG

[READ] PMG blanking and DMA disabling were removed from the mosaic/tunnel
renderer. The previous ball also remains visible while waiting for a new
update window. The ball helper allows a write to start only
at VCOUNT 124–127 (lines 248–255 PAL). A late call waits for
the next window, keeping the existing PMG. Scene boundaries,
music ticks and the ball/star masks were not changed.

[READ] The new test `tests/test_tunnel_raster.py` uses a moving
VCOUNT and checks 4 phases × 11 initial raster positions × 2 variants
of the delay. An additional variant stops the CPU for 3500 cycles after the first
PMG write. All memory and register writes finish before line 48
of the next frame; PMG/DMA are not blanked. The test detects the fault on archival
v134 and passes on v135. This is a model of instruction cycles with a synthetic
delay, not full ANTIC emulation or a hardware measurement.

[READ] Atari800 PAL/1088XE: 14,967,504 identical stereo POKEY bytes
relative to v035; the whole track. Preview of the finished callback raster:
`build/v135-pmg-preview.png` (approximate PAL colours). It is not a recording
of the raster trace in the emulator.

XEX: `build/visual-prototype-v135.xex`, identical to the working build.
SHA-256: `a797a26fc7cae52da34e7e5df5ab2c81494002d362219f2a9dcb05a527f15f65`.

[READ] Full `make check`: 87 tests, 84 passed, 3 skipped
due to the absence of archival v126; 77.469 s.
