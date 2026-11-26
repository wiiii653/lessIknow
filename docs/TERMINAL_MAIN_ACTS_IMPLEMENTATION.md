> **Draft implementation plan.** Reviewed against prerelease 182 and commit
> `2d523ff`. The [main-act text draft](TERMINAL_TEXT_PLAN.md) supplies the ten
> pages. [Project Status](PLAN_STATUS.md) records release evidence.

# Four-row terminal across the main acts

Keep a 40-column, four-row strip below the full 192-scanline picture from
school through the post-Trevor montage. At the credits cue, hand off to the
existing terminal at the same screen position. The title and final card
use their own layouts. See the [opening plan](TERMINAL_OPENING_IMPLEMENTATION.md)
for the separate star interlude and water reflection.

Start from the current source with commit `2d523ff` as the minimum baseline
and compare candidates against the immutable prerelease 182 XEX. Preserve
its animated loader and DMA handoff, four stereo music updates per PAL
frame, scene cuts, title dissolve, PMG buffering and SELECT restart.
Treat changes outside the strip and its display handoffs as regressions.
Use the current source and build map wherever the older text draft differs.

The implementation on `feature/terminal-opening` types all ten pages at
their act cues and holds each finished page until the next cue. The ordinary
display lists jump to separate tails while the strip is active and recover
their original tails at credits or restart. The font, two text screens,
and writer use reclaimed LMS table space at `$D800–$E23F`. Training still
needs the framebuffer maps at descriptor indices 2 and 3. Their shared low
bytes are at `$D960`, with high bytes at `$E180` and `$FDC8`. The allocator
checks all three ranges. Picture rows and active school table addresses stay
in place.

Text uses the credits' striped glyphs with a fixed three-ink palette for each
caption. The foreground prepares the inactive screen and the last music
interrupt publishes it in early blanking. A single interrupt in the gap
applies the caption palette, and the top blank restores the scene inks
from RAM. The final-boy greetings retain the animated row-by-row rainbow.
If the last music interrupt runs past the publication window, the ready
caption stays queued for the next frame.
The py65 check covers all ten cues, double buffering, all three training
bitmaps with the active strip, and the credits handoff.
The Atari800 monitor confirmed the first live publication with the
expected font in early blanking. The dance renderer copies each ribbon
plane without a per-byte subroutine call and can start publishing its
prepared buffers on PAL scanlines 248–263. In Atari800 PAL 1088XE with
the strip visible, the first dancer published 185 bitmaps and held a pose
for at most five PAL frames. The front solo published 364 PMG buffers.
Prerelease 182 recorded 185, five, and 363 respectively. The full stereo
POKEY stream matched prerelease 183. Physical playback and screen framing
on a real display remain to be verified.

## 1. Reserve the display list space first

The ordinary lists at `$8000` and `$8400` start with two bytes of blank
instructions, then have 192 three-byte LMS entries and an eight-byte
footer. The credits layout at `$BC00` proves the vertical geometry.
The proposed main-act footer is 16 bytes: a two-scanline gap, four
three-byte ANTIC 4 LMS instructions, and a three-byte JVB. Within the
list, this gives the following geometry.

| Relative scanlines | Role |
|---|---|
| 0–8 | Existing top blank, with music on line 0 |
| 9–200 | Unchanged picture, with music on lines 78 and 156 |
| 201–202 | Gap. Set up the strip palette here when enabled. |
| 203–234 | Four eight-scanline text rows. The last row supplies the music DLI on 234. |

The eight additional bytes per list would collide with packed scanlines
starting at `$824A` and `$864A`. Reserve the larger spans before packing
rows and regenerate the lookup tables. Update the allocator, list
builders and shape assertions together. If repacking cannot fit, evaluate
an ANTIC jump to a separately allocated footer and audit fetch timing
there. Check all layouts against the 1 KiB display list boundary. Update
fixed-offset users, especially `title_plasma.py` and
`outro_text.BITMAP_JVB_HIGH`, before testing any return to the title.

Implement the school-only prototype with a static strip, then exercise a
scene whose renderer keeps the same list while updating PMG. Inventory
ordinary list publication in `build_bitmap_sequence.py` and banked
publishers in school parallax, practice, both dances, hero, Trevor, mosaic
and eyes. Also check the private final-shot and final-card lists. Keep
the 192 picture LMS entries in place so these renderers retain their
existing row addresses.

## 2. Keep the music and picture palette stable

Start with one palette for all four text rows. Use a non-music DLI on the
two-line gap, with the three intermediate text rows free of DLIs. Route the
fourth music DLI through the existing WSYNC/player entry and bound the new
gap handler. Route by the **published** list layout and raster position.
The next scene can be prepared while the previous list is visible, and
scene 14 is shared by the school portrait and ribbon dance.

Audit CHBASE, PRIOR, COLBK, playfield colors and sprite coverage at the
strip boundary. Restore the picture settings before the next picture
fetch, including on held frames and effects that rewrite colors in the
music interrupt. Capture or track the actual colors used by each scene
rather than adding a generic restore palette. Preserve PORTB, the NMI
stack and the PMBASE shadow. Check that active missiles or players do
not spill into the footer and keep both PMG buffer spans intact.

Measure the raster with character DMA, the stereo player's longest
updates and the busiest scene callbacks. Verify music lines and POKEY
write timing before adding rainbow or per-row effects. Add those
effects only where the non-music DLIs have measured headroom. Keep the
credits' existing router and palette path as a separate layout.

## 3. Allocate the writer and publish complete pages

Budget 320 bytes for two 4×40 screen pages, up to 1,024 bytes for an
aligned font, and separate allocations for the compact text records,
typing state and code. Use the current build map and bank ownership to
place them. ANTIC must see the text screens and font while music banks
are switched. Immutable text records can be banked if the foreground
reader restores PORTB and its read is safe across an NMI. Prerelease
182 has 3,786 bytes to the packaged 1 MiB boundary. The build's main
code has 19 bytes to its allocation limit. Place new helpers in audited
space and charge the whole feature to the hardware package.

Reuse the ending glyphs and typing rules. Its active color font at
`$B400` and text screen at `$BF00` are inside the live
`$B000–$CEFF` framebuffer span during the main acts. The late engine
also relies on `$C000–$CEFF`, and its scratch near
`$0DD0` overlaps the montage director's state. Give the main strip
its own font, screens and state. A compact foreground writer with
page-relative line offsets is a good first implementation. Consider
sharing code with the opening interlude once both lifetimes are mapped.

Prepare changed rows and their LMS operands before blanking. Publish
the ready list, matching text page and raster mode together in the early
blanking window. Internally keep picture row cache, footer layout and
text page identity distinct. When a renderer holds its bitmap or
regenerates list entries, the strip still needs to advance. Prototype a
text-only pointer commit in blanking, with all four operands ready and
the window checked, or a list swap with the current picture mapping.
Measure it through a held practice shot. Allow the previous complete
page or typing state to remain visible if the next commit misses its
window.

## 4. Generate cues from the scene timeline

Use the music tick snapshot from the foreground director. Generate the
ten page starts from the same constants that drive the visible cuts,
including the nominal dance entrances where the renderer starts
preparation early. Use these values as a prerelease 182 cross-check.
Intervals end at the next cue.

| Page | Tick | Act |
|---|---:|---|
| 01 | 2992 | School arrival |
| 02 | 5984 | Basketball practice |
| 03 | 8975 | First side-dancer |
| 04 | 11967 | Early tunnel and rotator sequence |
| 05 | 14959 | Ribbon dance |
| 06 | 20942 | Tunnel cutaway |
| 07 | 21690 | Basketball hero |
| 08 | 23934 | Trevor fight |
| 09 | 29656 | Post-Trevor montage |
| 10 | 38705 | Bananas before the eyes and the late montage |
| Credits | 41884 | Existing boy terminal |

Page 10 covers the lead into the eyes. The eyes themselves start at
39379. Keep that grouping if the copy introduces the sequence, or move
the eye caption to the actual eye cue. Type each page from its own cue
and hold it through the act. Any caption that must already be complete
at the cut can be prepared invisibly. Validate the 37-character
editorial limit, prompt, cursor, brackets, font coverage and reading
time at build time. The shortest planned page has 748 ticks
(about 3.75 s), enough for the existing typing cadence. Test a skipped
tick and cut entry with the old page still on screen.

On the credits cut, keep the strip position and retire its raster mode
as the private credits list is published. Audit the order of the final
portrait setup, outro staging and takeover so no frame points at text
or font data being overwritten. Invalidate both layout and text caches
on SELECT. Confirm that the final card takes over its own buffers and
that restart rebuilds the opening and school lists.

## 5. Roll out and measure

1. Fit the footer and a static school page. Check all 192 picture rows,
   the POKEY stream and the four clock positions against prerelease 182.
2. Add the typed writer and the text-only commit. Test school, practice,
   the school-to-practice cut and SELECT before enabling all pages.
3. Enable pages through the rest of the director. Inspect the dance
   entrances and launch, hero and Trevor impacts, the tunnel hole,
   the eyes, and the credits takeover. Capture near each cut and at a
   held picture. Compare raster timing separately from the sampled
   stereo stream. Spot-check the footer on a real display for overscan.
4. Compare the fixed-palette strip and the animated greeting design at
   matched music ticks to check how often each effect presents a new pose.
5. Build with the normal full-rate hardware loader. Record the
   allocation, final size and SHA-256. Compare test failures against
   the baseline and record the exact emulator and physical Atari
   configurations with their results.
