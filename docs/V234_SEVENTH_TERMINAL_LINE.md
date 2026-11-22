# V234 — seventh terminal line

The terminal now has **7 rows: the status and 6 rows of typed text**.
The greetz stay on screen one line longer before
scrolling. The existing credits, greetz, typing, Enters, cursor
and subtle glitch remain. The content and the ticks of their typing were not changed.

## Frame and raster

Previously, six rows of text replaced the top margin and the first
8 black lines of the bitmap. The seventh replaces the next 8: bitmap
lines 16–191 are displayed. The first non-black pixel of the character is only
in source row 9, i.e. bitmap line 27; nothing of the character disappears.
Every visible pixel of the boy and of the PMG keeps its physical height.

The private display list $BC00 has 554 B: the bitmap starts at $BC16,
has 176 lines, the footer lies below $BE26. The whole image still has 235 lines.
The DLIs fall at 1/57/79/157/235; the additional 57 is only a palette
change, recognised at VCOUNT 32. The music remains every 78 lines.
The letters are still green, the background black, the body palette restored after the text.

## Memory

- History screen: 240 B, $BF00–$BFEF, still in the same RAM page.
- Typewriter: 195 B, $EB44–$EC06, +1 B; its reserve unchanged.
- Timing table: 48 entries, 96 B, $23CE–$242D.
- Lengths of 47 logical rows: $C828–$C856, in unused control
  glyphs of the font. Loaded only with the finale resources, not statically
  into the bitmap buffer. The remaining characters and the status do not use these glyphs.
- Outro resources after compression: 1743 B, +52 B; the audited gaps have 1783 B.
- Loader: 373 B, $3E58–$3FCC, before the resource tail beginning at $3FCE.
  Only one byte of slack is left, so it must not be enlarged without relocation.
- Main code: still 2551 B. No extension bank gap is occupied.

## Verification

[READ] 46 targeted tests passed: the text and cursor in all
six history rows, the scroll, the final clearing, the fixed bitmap map,
the PMG and the return beyond the finale. A new regression checks the simultaneous visibility
of `ATARIONLINE.PL / PTODT` in the first and `PERSONALLY` in the sixth greetz row.

[READ] Atari800 PAL/1088XE, stereo POKEY: **6 749 784 bytes identical
to v035**, the whole track. Without a test on physical Atari.

[READ] Full regression: **173/173 tests**, no skips, 119.4 s.
XEX v234 and the working `visual-prototype-dev` are identical.
SHA-256: `9fedec90111c52c56d2a184cd12390ff382b613d858db3cfd13f589807d910b2`.

CPU/ANTIC/PMG preview: `build/terminal-v234.png` (approximate PAL palette).
