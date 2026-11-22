# V183 — notes flying out of the mouth on PMG

The marks that looked like eyes above the entrance were treble clefs from the bitmap.
They were drawn for 192 lines, after which the school display list fetched only every
third line. That removed most of the shape. The bitmap melody was removed.

From tick 5610, when the girl reaches the door, four players display
notes, a pair of notes and a treble clef. They are emitted in turn from in front of the
boy's mouth, rise up and to the left, sway slightly and change colours. Four
missiles form short detached trails under the marks. The meeting frames and the
v175 panorama and the rhythm of later scenes remain preserved.

The code is generated in `tools/whistle_pmg.py`. It occupies 835 B in the previously free
gap of loader bank 0, $6A00–$6D42. The call adds 10 B to the banked effect
dispatcher. No bank or main code was added. The renderer builds an inactive
PMG buffer and publishes it in the lower blanking; it switches the existing buffering
$0980–$0BFF / $8980–$8BFF. The notes are turned off in the next shot (5984).

## Result

- `build/visual-prototype-v183.xex` and JSON; dev is identical.
- SHA-256: `c98aad7de93b23c7cb8456bf89c7698ee3cc7cef53f6024b726930438ddb3ad5`.
- 316 shared rows, 12 158 B of row data, 2552 B of main code.
- Bank comparison with v182: only loader bank 0 changed; the remaining
  63 banks are identical byte for byte.
- 13 CPU/rendering tests passed: emission at the mouth, upward motion,
  missile trails, alternating buffers and preservation of the previous image,
  no bitmap notes on the building, effect disabled after the cut, the boy's
  reaction, masks, v175 panorama accuracy and ball regressions.
- `build/v183-whistle.gif` and `build/v183-whistle-preview.png`: previews
  after executing the 6502 code, with PMG overlaid. They do not model ANTIC DMA or FPS.
- The emulator was not run again; the Atari800 installation has a known
  FUSE obstacle described with v181. No new hardware validation.
