# Gym hall rebuild — v009

Date: 2026-11-04. Result: `build/visual-prototype-v009.xex`.

## Image

- [READ] The hall fills the entire frame: beams and walls in perspective, tall
  windows, banners, side stands, doors, a basket backboard and a large floor.
  The characters have dark outlines and contact shadows. The geometry is stored
  in `tools/gym_background.py`, the composition in `tools/build_sequence.py`.
- [READ] Full images for solo, duo and trio replace the rectangular PMG masks.
  The background is also present behind the dancers, and the source colour
  pixels of all four poses remain preserved.
- [READ] The `build/v009-gym-{solo,duo,trio}.png` previews were reproduced from
  the RAM of a real Atari800, after the loader started and the callback ran with
  interrupts active. The RGB colours are approximate. The images have the
  aspect ratio of wide ANTIC E pixels: 160×192 logically corresponds to 320×192.

## V2 — PORTB ownership

- [READ] The NMI wrapper at `$1963` preserves registers like the original
  player, executes WSYNC, writes PORTB and selects the decoder bank from `$24A5`
  and the `$26FC` table. It enters the original handler at `$2218`.
- [READ] The epilogue at `$2312` jumps to a wrapper that restores the previous
  PORTB before restoring registers and RTI. Music can interrupt the copying of
  any of the six graphics banks.
- [READ] A py65 test injects a real NMI during copying in every bank: correct
  return, preserved PORTB and a pixel-identical resulting image.

## V3 — banks and main memory

- [READ] Six banks 9–14 were used, previously examined as never read by the
  v035 decoder. Each contains two 8 KiB frames: four poses × three dancer counts
  in total. Music banks 1–8 are byte-identical to the original. The end-of-music
  marker in bank 8 was not removed.
- [READ] RAM `$9000–$AFFF` and `$B000–$CFFF` are two image buffers. The CPU
  copies into the inactive buffer with NMIs active; ANTIC reads the existing
  buffer. The list is switched during vertical blanking. Every row stays within
  a 4 KiB DMA page.
- [READ] `$3300–$3BFF` holds static bitmaps. The old indicator visualisation and
  font initialisation were disabled. The five digits of the old clock were moved
  from `$34DA–$34DE` to `$83F0–$83F4` in the restart and countdown code; the
  instructions keep their types and execution time.
- [READ] A full decoder and restart run over 59 833 updates with `$3300–$3BFF`
  and `$9000–$CFFF` protection showed no access to those regions. In this
  isolated test the original RTI epilogue was reproduced, because the tracer
  calls `$2210` directly. The wrapper separately covers the interrupt test.
- [READ] 425 static rows occupy 16 515 B after sharing; the callback with the
  wrapper: 1417 B; row tables: 3264 B.

## V6 — music and timing regression

- [READ] Atari800, PAL, `-1088xe`, Altirra OS, stereo POKEY, headless.
  DLI remain on lines 0, 78, 156 and 234. Scene boundaries and the solo, duo and
  trio thresholds keep the previous music counter values.
- [READ] Comparison of v009 with v035: **6 620 400 identical stereo POKEY
  bytes**, about 1844.2 s of emulation, covering the entire track. The initial
  silence was aligned only once; no samples were shifted or skipped in between.
- [READ] Actual gaps between dance callbacks in Atari800: 16–20 ticks, about
  10–12.5 frames/s. All four poses appeared within 16 consecutive frames, with
  an occasional pose skip during longer copying. The music tick runs
  independently and does not lose updates.
- [READ] No listening test or test on physical Atari was performed. This test
  does not change the DLI spacing within the V6 experiment.

## Verification and reproduction

- [READ] 20 tests completed successfully.
- [READ] In addition, the entire raster was compared with the RAM of a real
  Atari800 for the title, the girl's first frame, solo, duo and trio: every
  image matched pixel by pixel against the reference, without corruption of
  static data.
- [READ] The Atari800 monitor was stopped at `$220D`, after the callback
  returned; dumps of `$0000–$CFFF` and `$D800–$FFFF` contained the ANTIC lists
  and image data. The counter `$24A7–$24A9` was changed only in the image tests,
  to check specific scenes quickly. The music comparison ran without such a
  change.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v009.xex --seconds 10
```

[READ] Previous XEX files were preserved; v008 is an intermediate build of the
rebuild.
SHA-256 v009: `258d94eb37b9efb080438c15276bea685dfd9ef3859a7bb9e5507e95361c2ed6`.
SHA-256 v007 remains `60fe082a4fd87b1529ede5d0349adde5a48bb57861a32dd93e9512a12a1f022d`.
