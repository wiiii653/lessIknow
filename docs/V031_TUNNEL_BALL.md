# v031 — ball deep inside the tunnel

At the tunnel's vanishing point sits an orange-gold basketball.
Eight masks rotate the curved seams and slightly change the radius. A dark outline
separates the ball from the mosaic. Four missiles orbit it with short tails;
the spark colour passes through the Atari palette. The ball appears only in the
tunnel motif, not in the rotating tiles. Scene boundaries and the music clock unchanged.

## Hardware and memory

- P0/P1: two halves of the orange-gold ball; P2/P3: seams and outline.
- Mask resolution 16×32, double player width and double DMA lines:
  a 32×64 area in logical screen coordinates (a circle at the Atari pixel aspect ratio).
- M0–M3: independent positions of the four sparks; fifth player mode, colour `$D019`.
- PRIOR `$11`, DMACTL `$2E`, GRACTL `$03`. The tiles motif disables PMG.
- Code and tables 1595 B in the free tail of bank 17, `$7800–$7E3A`.
  No new banks: still 33 banks.
- The unbanked RAM wrapper switches bank 17 after the mosaic renderer,
  calls the effect and restores PORTB. The NMI wrapper remains unchanged.
- Main callback 1783 B; unused branches of the old kaleidoscope were removed.
- Exiting the mosaic restores the dance PMG graphics. No change to the tunnel bitmap.

## V5–V7: results

[READ] 47 tests PASS:

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
```

The tests cover eight rotations, disjoint colour and seam masks, all four
missiles, motion with a static bitmap, disabling on transition to the tiles,
restoring the dance stars and bank behaviour during music interrupts.
Updating on a held tunnel frame costs fewer than 14000 instruction cycles
in the test (without DMA, NMI and raster waiting).

[READ] Atari800 PAL, `-1088xe`, Altirra OS: 89 memory dumps covering
all mosaic frames, earlier scenes and transitions. Bitmap pixels
match the source; the four PMG planes of the ball match the rotation masks,
the missiles are present in the tunnel motif.

[READ] Full digital stereo POKEY comparison, sampled every 78 lines:

```sh
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py \
  --demo build/visual-prototype-v031.xex --seconds 12
```

8 265 816 identical bytes, about 2302.5 s of emulation; the whole track covered.
No separate listening test on physical Atari or test in Altirra was performed.

## Files

- `build/visual-prototype-v031.xex`
- `build/v031-tunnel-ball.gif` — 6502 code samples every 8 ticks; PAL colours approximated,
  the preview is not a measurement of the frame count achieved by the emulator.
- `build/v031-tunnel-ball-sheet.png`

SHA256 v031: `db98f9398570e10238a6a411734d7cb1ac9b52fac9cfef3c4885954c7913ade8`.
v029 was preserved (`c8a509af600bafa2c16e198cf5c2f90ecf2afb9f1a33fee81dee8540107543f7`)
and the intermediate v030. The builder refuses to overwrite an existing XEX.
