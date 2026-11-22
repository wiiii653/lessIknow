# V146 — readable throw and fireworks

[READ] At the user's request, the grid, the pitch rectangle and its lines were
removed from the entire third dance shot. The girl and the two bases are now on
a calm black background. The overhead perspective, the enlargement of the
heroine and the receding of the other girls remain in the existing phases.

[READ] In the preparation for the throw there are no animated ribbons.
In the first stage of flight, tick 20662, the fireworks begin: rockets, the
bloom of radial shapes and scattered points on the players, with small sparks
on the missiles. These are eight phases of 16 ticks, four blooms offset in
phase. The effect lasts until the end of this shot, at 20942.

[READ] The players are twice wide (16 logical pixels) instead of the
four-times-wide ribbon loops. The left pair fits in columns 10–25, the right
pair in 134–149 of the 160-pixel image. The centres of the blooms are at
(18,42), (18,132), (142,54), (142,147) in logical pixels/raster lines.
The large masks do not cover the central band of the face. The existing colour
cycles after the musical DLIs also cover the new fireworks.

[READ] The earlier side dance, the group and the solo keep the previous
ribbons and sparks. Also the repeated jumps between these shots restore the
appropriate width and PMG masks. Throughout the scene the preparation of the
inactive PMG/bitmap and the limited publication window VCOUNT 124–127 are
preserved. The stages of the throw, the shots, the acts and the music ticks were
not shifted.

## Memory

[READ] The eight firework shapes occupy 128 B. Together with the new effect
selection and copying, the cost increases by 349 B: the controller in loader
bank 49 now has 2203 B and occupies `$5400–$5C9A`. The bitmaps and existing
ribbon streams keep their sizes. Still 36 compositions and 64 banks.

[READ] To keep the code disjoint, the final boy's controller was moved from
`$5B80` to `$5CC0–$5FEB` (still 812 B). Between the controllers 37 B remain,
and before Trevor's code from `$6000` only 20 B. The installers reject
collisions. The main code still has 2494 B, and the finale bitmap and music keep
their existing places.

[READ] Current net recovery relative to v141: **24 954 B = 24.37 KiB**.
This does not mean freeing whole banks or lowering the hardware requirements.

## Previews

- `build/v146-launch-fireworks.gif`: the whole third shot, callback every 12 ticks.
- `build/v146-flight-fireworks.gif`: a short preview of the final flight itself.
- `build/v146-launch-storyboard.png`: the preparation, the start of the flight and the close-up.
- `build/visual-prototype-v146.xex` and JSON: the numbered release.

The shapes and effects are produced in `tools/ribbon_dance.py`. No new source
illustrations were generated. The GIF has an approximate palette and tempo; the
py65 execution does not model ANTIC DMA or actual presentation timings.

## Validation

[READ] `make check`: **113 tests, 110 passed, 3 skipped**
(missing archival v126), 89.829 s. The new tests check the removal of the lines,
zero ribbon masks in the preparation, eight different bloom phases, effect
columns outside the face, player sizes, missile sparks, the return to the
earlier ribbons and writes only to the inactive PMG. The existing NMI test now
also covers the start of the fireworks; the moving VCOUNT test checks
both the ribbons and the new blooms.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **14 751 288 identical
bytes** relative to v035 throughout the whole track. The final boy, the
fade and the returns between scenes also pass the tests after the code
relocation. Without a listening test and a run on physical Atari; register
agreement is not a measurement of actual image smoothness.

[READ] XEX: 1 109 034 B, with no change in size relative to v145.
SHA-256: `7b0184401c7dfcc1a85b51d199671ce2e9731b71f9297b8086e3c168783624d9`.
The numbered release and the verified working build are identical byte for byte.
