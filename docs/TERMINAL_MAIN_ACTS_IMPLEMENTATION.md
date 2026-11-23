# Four-row terminal across the main acts

Feasible in principle. The existing ending proves that a 192-scanline
picture and four text rows fit together. Extending that geometry to every
main scene needs shared display-list ownership and a timing audit. This plan
follows TERMINAL_TEXT_PLAN.md: the strip starts at school, persists through
the main acts and hands off to the existing credits. The title and final card
keep their own layouts. This differs from the opening brief's initial scope,
so the two features can be implemented and evaluated independently.

1. **Measure the baseline.** Inventory both shared display lists, their
   footer owners, the private ending list and all writes to DLIST, CHBASE,
   PRIOR and playfield colors. Verify the layout during title-to-school,
   portrait, practice, dance, cutaway, dunk, Trevor, tunnel and eyes cuts.
   Cache keys must include any footer layout that can change while the
   picture mapping is held. Record the existing four music DLI positions,
   the baseline audio trace and available resident memory.
2. **Create one footer template.** Keep the existing 192 LMS entries and
   their offsets. On the shared lists, replace the 32 blank scanlines with
   four eight-scanline ANTIC 4 rows after the two-scanline gap. Follow the
   ending's geometry by putting the fourth music interrupt at the end of
   the fourth text row. Preserve that line even on blank pages. Keep the
   longer footer within the ANTIC list page and audit fixed-offset users
   such as the ending restore code. Build or patch the inactive list and
   publish it with the frame. Test a static page through several cuts
   before adding any typing.
3. **Bound the raster work.** On entry to the strip, establish text colors,
   black background and font independently of the scene's PMG settings.
   Restore the scene's palette and mode before its next picture. Preserve all
   four POKEY updates and their WSYNC timing. Start with stable text colors.
   Add per-row color changes only after the DLI cycle budget has been
   measured with character DMA and the busiest scene. Keep the credits' own
   palette path available.
4. **Allocate buffers and records.** Two text pages need 320 bytes at 4 × 40
   characters per page. Reserve these plus the active-page flag and typing
   state in audited RAM visible to ANTIC throughout bank switches. Account
   for the aligned font and compact page records separately. Do not assume
   the ending's fixed addresses can be reused. Its current code couples
   timing and length tables in the font region with a screen at $BF00.
   Factor the shared typing rules around separate opening/main/credits
   records and caller-supplied screen addresses, or keep a compact dedicated
   act-strip writer if generalizing the late engine costs more. Change text
   offscreen and publish it in bounded vertical blank.
5. **Drive pages from actual cuts.** Map pages 01–10 to the builder's scene
   constants and director cuts. Treat the brief's tick table as editorial
   guidance. Each page types from its act's first tick and holds until the
   next cue. If a page must land fully typed on its first beat, make that an
   explicit, separately authored cue for that page. Do not silently start
   typing the next caption over the previous act. Validate each line against
   the 37-character limit and the actual font, including brackets and the
   cursor glyph. Confirm the cutaway page completes before the dunk.
6. **Hand off to credits.** Retire the shared footer as the private credits
   list becomes active. Invalidate typing caches on entry and restart.
   Clear visible references to text RAM before the final card repurposes
   that RAM. Preserve the existing credits copy and final card.

The largest risks are resident RAM ownership and extra DLI work in the
busiest scenes. All banks are allocated, and the bytes below the 1 MiB XEX
limit do not establish free RAM. Require an allocation map and size check
before expanding beyond a single-act prototype. Verify geometry and the
four music interrupts at every cut, compare the full POKEY write stream,
then check visible tearing, colors, PMG effects and restart on emulator and
real hardware. The fallback if the timing budget fails is a fixed palette
and selected act captions. The transition to credits must still use the same
display geometry.
