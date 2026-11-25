> **Draft proposal. The changes proposed here require separate implementation and verification.** See the [current documentation guide](README.md) for active instructions.

# Opening star, terminal and reflective title

Feasible as a runtime scene, subject to a bank allocation and raster budget
check. This plan covers the opening brief through the cut to school. The
main-act strip is an independent decision covered by the companion plan.

1. **Pin a baseline.** Record the current source, numbered hardware XEX and
   size. Prerelease 178 is 1,044,435 bytes, leaving 4,141 bytes to the 1 MiB
   boundary. Treat this as file headroom only. Map runtime ownership of both
   framebuffers, the star tiles, display lists and memory under ROM. Keep the
   loader handoff and its raster sync. Reproduce the sync in the build path
   or apply the established packaging patch when preparing the candidate.
2. **Lay out the interlude.** Use the opening scene to re-render the loader
   mark from the same frame source as the loader and ending card. Start with
   the ending card's character tile approach, which avoids allocating a full
   bitmap for the star. Match the loader's scale, center, palette and apparent
   speed. Place a four-row ANTIC 4 strip at the regular footer position on
   black. Reuse the glyph source and typing rules. Audit the runtime star data
   and decoder's bank lifetime before committing to their reuse.
3. **Keep music and later cuts aligned.** Prototype the interlude in ticks
   0–1023, about 5.1 seconds, then use the existing city reveal window before
   the title cut at bar 4. Type both proposed pages within that budget and
   fade the star and text near the end. This consumes the opening part of the
   current artist card. If that card needs its original duration and the
   interlude must last 6–10 seconds, use a separate pre-song scene and start
   the music timeline at tick zero after the fade. Shifting all music cues
   would change the sync throughout the demo.
4. **Give the opening its own resident state.** Share glyph and typing logic
   at build time. Keep opening message records and the active screen outside
   swappable bank windows. The current ending resources are unpacked late by
   outro_loader.py. Do not call that preload at startup before checking all
   of its destinations and scratch addresses. Start with a single resident
   glyph set and a compact record stream if the allocation allows it.
   Prepare text and star data offscreen. Publish pointers in a bounded
   blanking window and leave a complete frame visible if preparation runs late.
5. **Add water below the city.** Preserve the 192 picture scanlines. Prototype
   in the existing 34-scanline blank tail before the last music DLI, using
   repeated groups of scanlines. Start with a mirrored selection of rows from
   the visible skyline buffer. Add a small phase-driven row offset through
   prepared reflected rows with safe edges. Use the existing title field
   mode and a lower luminance for the reflection; switch and restore the
   palette with bounded raster work. Gate the water on the city reveal so the
   quay and reflection resolve together. Avoid reflection frame banks.
6. **Check the handoffs.** Keep the four music DLIs at their existing lines
   in every opening list. Any extra palette DLI needs a distinct raster
   window and must leave the audio clock intact. Verify both framebuffer
   copies are restored for school, including mode, palette and list footer.
   Cover fresh boot and SELECT restart and confirm the title covers the
   screen cleanly after the loader relinquishes it.

Prototype in this order: star and blank strip, typing and fade, then static
reflection and ripple. At each step inspect the generated addresses and XEX
size, profile the longest frame and compare the POKEY write timing and stream
against the baseline. Check the sequence in Atari800, then record the exact
binary and result on AVG / 1088 Rambo. Emulator output alone does not prove
the raster timing on hardware.
