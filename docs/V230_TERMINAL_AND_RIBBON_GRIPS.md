> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V230 — four final notes: terminal, ribbons, brightness and the sixth row

## Terminal

- The prompt `XE:> ` and all letters are aligned to fixed columns.
  There is no horizontal wobble. Typing, the pause before entry, Enter and the
  block cursor work as in a terminal session; while typing the cursor is full,
  before/after it blinks. The SYS.OPEN / UPLINK headers and all credits are
  preserved.
- A sixth row was added — the status `[XE-OS] LINK:ONLINE // SV2026 [OK]`.
  The remaining five rows are the scrolling history with prompts.
- So as not to disturb the boy, the extra row replaces the first eight black
  lines of the bitmap. The display list shows the remaining 184 lines at the
  same physical positions. No pixel of the character is clipped or scaled.
- The green letters now have luminance $0E instead of $0C. About once every
  1.28 s there is a single-frame change of green to white and a single artifact
  in the status. The letter positions and skin colour remain constant; the
  background is black.
- The regular music DLI remain after lines 1/79/157/235. The additional palette
  split falls after 49, is recognised at VCOUNT 28 and does not decode music.

## Ribbon grips

The audit found incorrect nominal hands in base pose 3 and the use of points
from the old sheet for four quarter frames. The visible hand of pose 3 was
corrected and separate QUARTER_HANDS were added for the new sheet. Because pose 3
has one visible hand, both streams of the middle character originate from that
hand. No other silhouette was drawn.

After converting the coordinates, the grip point is pulled to within at most
4 pixels of that specific character's skin (not the floor or a neighbour).
Missing such a point aborts the build. This applies to front, solo,
three-character shots and intermediate frames. The side shot keeps its existing
anchors.

At the base of each ribbon a continuous grip was added in the two middle columns
and three PMG rows. This offsets the difference between the centre 3.5 and
rounding to pixel 4 and prevents the ribbon end from moving away from the hand
in some phases. The ribbon controller now uses the PMBASE shadow in RAM instead
of reading $D407. The metadata and PMG changed; the dancer bitmaps themselves
remain preserved.

## Memory and safety

The intro helper reserve is 1888 B. Typewriter: 194 B from $EB44 to $EC05,
the scanline pool starts at $EC20. No new extension banks.
The status fits in unused font control characters $C800 (row ASCII,
not used glyph data). The private DL $BC00 is 575 B.

The palette router is 74 B and ends at $249A. **$249C–$24A4 are live player
and memory-detection variables**, not free space after the UI. An assert in the
generator guards this boundary. The larger router from working v229 was rejected
after a real emulator start attempt; do not use that release for a show.

## Verification

The tests cover the hands of all base frames and 18 additional frames, the grip
in all 16 phases of each ribbon, data decoding, callbacks, NMI, a stable frame
and the unchanged four music updates per frame.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 297 880 identical bytes
against v035, the entire track. No test on physical Atari.

CPU/ANTIC reconstruction previews: `build/terminal-v230.gif`,
`build/terminal-v230-preview.png`, `build/ribbon-v230-grips.png`.

[READ] Full suite for v230: **165/165 tests, no skips**, 113.7 s.
