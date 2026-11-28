> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V216 — credits and greetz over the boy lying down

## Image and timeline

- 53850–56841: three credits screens, about five seconds each.
- 56842–59084: greetz, five visible lines; the text scrolls up and each
  line waves horizontally along a sine with an offset phase.
- From 59085: return of the full previous frame and the existing fade.
- The whole boy bitmap is preserved. In PAL, five ANTIC 2 rows replace
  the earlier top and bottom margins. The bitmap and PMG move down by
  32 lines for the duration of the captions, without scaling or cropping
  the character.
- ANTIC 2 gets white letters on a black background; before the bitmap the
  previous character palette returns. The palette change happens through
  VCOUNT/WSYNC in the foreground, without additional musical DLIs.
- The DLIs fall after lines 1, 79, 157, 235; the spacing stays equal at 78 lines.
- The content comes from `GREETZ_AND_CREDITS.md`, with shorter line breaks and
  ASCII spelling. Unfilled `[NAME]` placeholders and the proposed disclaimer
  before the intro were not shown.

## Memory ownership

- No gap in the expansion banks was occupied.
- 1738 B of packed resources in verified base-memory gaps indicated by
  `outro_loader.GAPS`; the tail of the data starts at `$3FC4`.
- Loader: 364 B, `$3E58–$3FC3`. Loader and data do not overlap.
- Finale controller in bank 49: 816 B, `$5CD0–$5FFF` — no further headroom.
- Caption variables: `$0DD0–$0DD7`, outside the scanline pool, the selector
  and its `$0DC0–$0DCF` space, and the DL keys `$0DFE–$0DFF`.
- Only after the boy lying down has been copied to `$9000` is the second
  buffer handed over to the captions: `$B000` — joined LZ stream, `$B800–$BAFF`
  — copy of the normal DL, `$BC00–$BE53` — separate caption DL,
  `$C000–$CEFF` — unpacked code, text and charset `$C800`.
  Earlier scenes still own both full buffers.
- Unpacking is a one-off multi-frame task. Music still runs through NMI. The
  210000-cycle threshold in the test refers to a cold entry, not FPS.
- At the end of greetz the normal DL is prepared in the inactive `$8400`
  and published in the VCOUNT 124–127 window.

## Verification

CPU/ANTIC preview: `build/outro-v216-preview.png` — credits, greetz and finale.
This is an image reconstruction, not a capture from physical Atari. The tests cover
unpacking, text pointers, the full bitmap, return to the finale, PMG, restart
and comparisons of earlier scenes with v198. [READ] Full run for v216: **154 tests, all passed,
no skips**, 114.3 s. Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
**9 791 424 identical bytes** against the original v035; the whole track.
A rebuild from the current sources is byte-for-byte identical to v216 (`cmp`).
All 64 bank blocks are preserved; only block 63 changed,
that is loader index 49 with the finale controller. The remaining 63 bank blocks
are identical to v198.

Preview reconstruction generator: `tools/preview_outro.py`. The CPU tests
are not a measurement of ANTIC DMA nor confirmation of operation on physical Atari.

Working versions v199–v215 are not presentation versions.
