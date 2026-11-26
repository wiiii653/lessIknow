> **Draft implementation plan.** Reviewed against prerelease 182 and commit
> `2d523ff`. See the [opening brief](TERMINAL_OPENING_BRIEF.md) for the copy
> and visual direction, and [Project Status](PLAN_STATUS.md) for release
> evidence.

# Opening star, terminal and water reflection

Show the familiar animated star above four terminal rows when the demo takes
over from the loader. Fade to the existing plasma and title sequence, then
reveal a reflection below the city quay. The title uses that space for water.
The [main-act strip](TERMINAL_MAIN_ACTS_IMPLEMENTATION.md) can be implemented
independently.

Start from the current source with commit `2d523ff` as the minimum baseline
and compare candidates against the immutable prerelease 182 XEX. Preserve
its full-rate animated loader, raster sync and DMA shutdown, RAM-shadowed
PMG buffering, corrected title dissolve, stereo mix and SELECT restart.
Treat changes to these behaviors outside the planned opening as regressions.
Use the current source and build map wherever the older brief differs.

## 1. Start the interlude in the runtime

Use a dedicated runtime display list after the `$4800` bootstrap hands off
to `$13E0`. Prerelease 182 restores the OS VBI and shuts off ANTIC DMA before
the final segments overwrite the loader font, list and animation data.
Recreate the image from the same assets in the runtime. Keep the packaging
protocol in the [hardware loader contract](HARDWARE_LOADER_CONTRACT.md).

Start with the same scale, screen position, palette and nominal PAL frame
cadence as the loader. `outro_text.final_mark()` yields 32 phases of 168
glyph bytes each, and `final_boy.install_mark_frames()` already installs
those phases at `$6800` in loader banks 20–23. Prototype reading those
existing tables with a small runtime routine that restores PORTB. The finale
animator assumes its own font destination and palette, so use its addressing
as a reference when factoring a shared copy routine. A duplicate raw phase
table alone would cost 5,376 bytes. Keep the mark's three ANTIC 5 rows and the
terminal's four ANTIC 4 rows in separate bands with matching fonts and a
black terminal background.

## 2. Give the text time and preserve the scored opening

Start with a silent runtime interlude of **320 PAL frames** (about 6.4 s).
Use a frame count tied to the first of the four scheduled raster events
while the music clock is held at zero. Keep NMI scheduling alive and gate
packet consumption until the title's first frame is ready. Place the
opening list's mark rows and blank spacers so the fourth text row ends at
line 234 and the other clock slots stay on relative lines 0, 78 and 156.
Use `stereo_playback.py` to trace SELECT restart and first packet handling.
After the fade, publish the initial title list in blanking and release the
player on the corresponding first music DLI. Verify both POKEYs start
together and tick zero runs once. Start the silent interlude again on
SELECT, including a SELECT from the credits and the final card.

Use the two pages in the opening brief as draft copy. A workable first pass
is frames 0–143 for page one, 144–287 for page two, and 288–319 for the fade
and handoff. At the existing terminal's nominal character cadence, the pages
take about 124 and 72 music-tick equivalents to type (roughly 0.62 and 0.36 s).
Drive that cadence from interlude time while the player is held. Keep the
complete pages visible for the rest of their windows. Apply the same
brightness envelope to both the star and text, and hold a finished frame if
the initial plasma buffer misses its publication window.

An interlude over player ticks 0–1023 would be about 5.1 s. That version
changes the visible artist cues from tick 512 and the fireworks from tick
768. Use it only if an interlude over the music is an explicit editorial
choice. The silent version keeps the city reveal at 1024, the card change
at 1496 and the school entry at 2992 on the existing track clock.

## 3. Prove the storage budget

Reserve the opening display list, text pages, glyph destinations, message
records and phase state in the current allocator. The later terminal
unpacks into `$C000–$CEFF`, using the second framebuffer for staging.
Reuse its glyph shapes and typing rules at build time. Any runtime reuse
needs separate addresses and an audit of the live display list, records and
scratch memory. Generate the opening font for the characters actually used
in the two pages. Verify bracket glyphs and the synthetic cursor. Check that
mark glyphs and text glyphs can coexist before assigning separate aligned
font pages. The mark, four text rows and associated pointers must be safe
across music bank switches and restart.

Prerelease 182 is 1,044,790 bytes, leaving 3,786 bytes to the 1 MiB boundary.
That number applies to the packaged file. The build JSON reports 295 shared
scanline rows and 2,541 of 2,560 bytes of main code. Budget against the
current generated allocation, including packed row spans, PMG pages and
RAM under ROM. Reject overlaps at build time and measure the final package
with the normal full-rate loader enabled.

## 4. Add the reflection in the title tail

The existing title displays an 80×64 GTIA 11 field on 192 scanlines, with
the city anchored at its bottom. Preserve those rows. Relative to the list
start, the picture is on lines 9–200 and the fourth music DLI is on line 234.
Prototype 33 water scanlines on lines 201–233 and keep a final one-line
music marker at line 234. Check that this band is visible on the target
display before committing to its depth.

Mirror eleven source rows around a fixed waterline, starting from the
bottom of the composed city and plasma. Repeat each reflected source row
three times. Sample before title lettering is composited, and treat PMG
fireworks as a separate effect. Gate the band and its source pixels on the
same reveal stage as the city. For the first version use a subtle texture
at the existing title luminance. Then add slow horizontal offsets with
edge fill so a displaced read never wraps into an adjacent source row.
GTIA 11 shares luminance through COLBK. A dimmer band needs a timed
luminance change and restore, so profile that as a separate step.

A first RAM estimate is 440 bytes per buffer for eleven 40-byte rows.
Repeating them with an LMS on each of 33 lines yields a 103-byte tail
including the music marker and JVB. That tail cannot grow into the packed
rows that start after the ordinary list. Evaluate a separate tail or a
dedicated title list as part of the allocation. One alternative is 1,320
bytes per buffer for 33 contiguous rows and a 39-byte tail, trading LMS
overhead for more pixel writes. The unused part of the title's framebuffer
span is a candidate while the title owns it. Check actual writes, ANTIC
fetch boundaries and both buffer lifetimes. Measure the 6502 work before
choosing. Build the reflection and its LMS pointers with the
inactive title frame and publish them together. Restore the ordinary
ANTIC E list, palette and pointers for school and invalidate both layout
caches on restart.

## 5. Implementation and acceptance order

1. Show the static mark and blank strip after the loader. Check the raster
   positions, buffer ownership and the handoff to an unmodified title.
2. Animate the mark, then add typing and fade. Exercise cold boot, player
   start and SELECT from different acts. Compare the full stereo POKEY
   stream to prerelease 182 after a single alignment at playback start,
   and check the four music DLI positions separately.
3. Add the static reflection, then ripple. Measure the worst case with the
   city reveal, title dissolve and fireworks active. If ripple or a
   luminance split misses the budget, keep the static reflection while
   profiling those additions.
4. Package the hardware XEX and record its size, SHA-256, AVG loading
   setup if applicable, Atari model, memory expansion, stereo configuration
   and PAL/NTSC setting. Use emulator captures for raster checks and a
   physical AVG / 1088 Rambo run for hardware evidence.
