# Technical and performance audit v126 — 2026-11-06

Scope: the current `lessIknow-thebetter` engine, the XEX generator, effects, banking, tests and the build process. The separate 3D engine from the parent directory and the `impala-lessIknow` music project are not covered by this measurement. Production code, scene boundaries and ticks were not changed.

Conclusion: the architecture protects the music and the active image, but the cost of graphics updates is high. The greatest potential lies in removing work performed repeatedly for unchanging data: display lists, portrait expansion, plasma composition and wide pos copies. There is no basis for stating that the whole meets the 50 Hz budget. Nor does exceeding a single frame automatically mean a fault: the animations have sparser phases, and the music runs independently.

## Verification

[READ] 80 tests in py65 1.2.0, 79 OK, 1 FAIL, time 79.768 s. The failure at `tests/test_mosaic.py:49–55`: the test expects the dance pos from `tick >> 5`, while the engine and the remaining tests use `tick >> 4`. First discrepancy: 5 instead of 3. This is an inconsistent test expectation, not evidence of a broken transition. Because the test stops at the first assertion, further transitions in that particular method are not verified.

[READ] A rebuild to `/tmp/atari-audit-v126.xex` identical to the supplied v126:
`06b97337f904bff25a271f299bb440ff645b092414a2395866683eaf69c04da1` (SHA-256).

[READ] `tools/check_playback.py --seconds 12`: PASS, 3,631,536 identical stereo POKEY bytes, about 1011.6 s of emulation, the whole track. Atari800, PAL, 1088XE, Altirra OS, started without screen and sound. This confirms that the register stream matches in this configuration; it is not a listening test or a measurement of interrupt regularity on physical hardware.

## Callback cost measurements

[READ] `tools/profile_engine.py`, data in `docs/AUDIT_V126_CYCLES.json`. 589 calls: successive ticks every 4 within each examined fragment, a fresh CPU at the start of the fragment. The cost includes the first fills and cache hits. The harness from `tests/test_sequence.py` sets a constant VCOUNT=124 and does not run DMA or NMI. The sampling does not reproduce the actual passage of time during rendering; it is not a full run of the track or an FPS measurement. The maxima apply only to those samples.

| Fragment, ticks (exclusive end) | Median cycles | Maximum | Calls >35,568 / samples |
|---|---:|---:|---:|
| Intro, 0–100 | 1,325 | 114,773 | 4/25 |
| Title, 1496–1596 | 1,089 | 120,904 | 4/25 |
| School, 2992–3092 | 649 | 17,416 | 0/25 |
| Parallax, 3553–3853 | 5,978 | 53,684 | 10/75 |
| Training, 6000–6100 | 594 | 93,168 | 1/25 |
| Solo dance, 9216–9472 | 1,157 | 92,904 | 16/64 |
| Mosaic, 12000–12300 | 8,038 | 73,698 | 19/75 |
| Portrait, 18000–18100 | 5,739 | 130,470 | 1/25 |
| Basketball player, 21000–21300 | 6,611 | 66,049 | 2/75 |
| Trevor, 27000–27300 | 7,816 | 55,496 | 15/75 |
| Late mosaic, 59000–59300 | 12,718 | 78,378 | 20/75 |

[CONCLUSION] 312 lines × 114 cycles = 35,568 cycles per PAL frame before DMA. A title update takes up to 3.4 such frames of CPU alone. The good medians result from the cache; they do not describe the cost of a phase change. What is needed is a measurement of the time from fetching a tick to displaying the image, and of the number of skipped phases. This table should not be converted directly into a real FPS.

## Most important improvements

### 1. Constant display lists are rebuilt — high priority

[READ] `mosaic.py:83–88`, `school_parallax.py:64–69`, `trevor_polished.py:190–195`, `basketball_hero.py:184–193`: when the image changes, the code rewrites the addresses for 192 lines. Each row additionally modifies the operands of two store instructions by adding 3 and handling the carry. The geometry is constant within a given scene mode.

[ASSUMPTION] One-time initialisation of both DLs for a given layout and bases $9000/$B000 should remove from a dozen or so to about 20 thousand cycles per image change. This is an estimate from instruction counts, not a benchmark of the corrected version. A separate layout identifier should be stored for each DL, preserving the DLI, LMS and final jump bits. The list can be overwritten by another scene; initialising only once from program start would be wrong.

### 2. Portraits are expanded during playback — high priority

[READ] `crush_portraits.py:37–49`: for each source byte two reads are performed, nibble unpacking, an expansion lookup and updates of four operands of self-modifying code. Maximum of the whole callback: 130,470 cycles.

[CONCLUSION] Prepare the portraits in the final 160×52 format already during the build or INIT, then copy them as an ordinary block. Four images require 8320 B instead of 4160 B, that is an additional 4160 B. In the current location of the music bank one should not assume that they will fit: use a proven free area/bank or expand them before the scene. The gain requires a benchmark; adding RAM makes more sense here than micro-optimising a single shift.

### 3. Banked copies use a free byte loop — high priority

[READ] `mosaic.py:80–82`, `school_parallax.py:61–63`, `trevor_polished.py:187–189`: LDA abs,Y; STA abs,Y; INY; BNE, about 14 cycles/byte with no additional page crossings. The mosaic copy of 3840 B alone costs about 54 thousand cycles. Some frames start at non-zero low addresses, so there is an added cost of page crossings on reads.

[CONCLUSION] Use partially unrolled copies of several pages per index, analogously to `engine_effects.copy_helper`. The LDA/STA pair is 9 cycles/byte, and the loop cost can be amortised. Potential of about 30–35% of the copy itself, not of the whole callback. The code must execute outside the window being changed and must not overwrite the helpers at $AF00/$CF00. In addition, in `basketball_hero.py:166` the 192 B tail uses JSR/RTS for every byte: the overhead of those calls alone is 2304 cycles, which can be removed with a local inline loop.

### 4. The dance copies too wide an area — high priority

[READ] `build_bitmap_sequence.py:420–482`, `engine_effects.py:8–31`: after the buffers are warmed up, 5376 B (21 full pages) is still copied, also for solo. A full fill is 7936 B. There is a correct check of the contents of both buffers.

[CONCLUSION] Generate at build time lists of changed row segments, separately for solo/duo/trio and for each previous→new frame pair. Copy rectangles or runs instead of all the columns of the wide band. Keep the full path when entering from another scene. The difference must refer to the contents of the destination buffer, not to the last displayed frame. The gain depends on the number of runs and the overhead; it requires measurement, especially for trio.

### 5. The plasma performs several full passes — medium/high priority

[READ] `title_plasma.py:263–335`: when the mask changes it copies 2560 B to the cache, then composes 2560 B with the mask and colour. The fade adds another full read/mask/write. The cache and page unrolling already exist, so this is not a naive renderer without optimisation.

[CONCLUSION] First step: merge the fade with the composition so that the result is not read and written again, if the bank layout allows. Next, consider ready-made frames for the most expensive transitions and their exact phase combinations. Do not assume that all combinations of masks, plasma, colours and fade will fit in the 48,640 B freed as described in V120; a table of actually reachable states is needed. Merely moving successive instructions into tables without reducing the number of passes will have a smaller effect.

### 6. The mosaic computes an increasingly expensive modulo — medium priority

[READ] `mosaic.py:95–104`: determines the phase on every call by subtracting 187 until falling below 187. At tick 59000 this is about 139 iterations from the base of 32912. The cost grows as the scene progresses, also on an image cache hit. Samples: median about 8 thousand at the beginning and 12.7 thousand at the end (the difference also covers the remaining colour paths).

[CONCLUSION] Replace it with an algorithm with a bounded number of steps: beat-boundary search or binary division by a constant. In an incremental solution, handle restart, pause and large tick jumps. Preserve exactly the current phase of 187 and the colour base; changing to a different tempo would be an artistic change. The short contrast lookup can later be replaced by a flag table, but that has a lower priority.

### 7. PMG is cleared over a wide area even for similar frames — medium priority

[READ] `basketball_hero.py:198–202`, `crush_portraits.py:69–73`, `trevor_polished.py:222–225`: three indexed stores for each of 256 indices. That is 768 store operations and about 5.1 thousand cycles of the loop. The ranges partially overlap: $0980–$0A7F and $0A00–$0AFF.

[CONCLUSION] Clear the previously occupied PMG ranges and leave a full clear for a change of owner/scene. Overlapping stores can also be eliminated. Check the old ball positions, BANG and eyes after transitions; disabling GRACTL alone does not remove old data.

## Technical risks and the build process

**Raster synchronisation: requires measurement.** The `VCOUNT >=124` loops in many effects wait for a window, not for the start of a new frame. Two calls can pass in the same window, and an NMI can delay further writes. PMG is sometimes cleared only after that wait. No tearing has been demonstrated, but a constant VCOUNT=124 in the tests cannot rule it out. An emulator trace with DMA is needed: entry line, rendering time, DL switch line, last PMG write, spacing of the four music ticks. Before changing the synchronisation scheme, check the impact on the original DLI.

**The snapshot is not the presentation time.** `build_bitmap_sequence.py:224–233` correctly fetches a consistent multi-byte tick, but after 90–130 thousand cycles it displays a state already several frames old. This is image delay, not a slowdown of the music clock. The tests should measure skipped phases and the delay of important beats instead of merely requiring the cost to be below 110/140 thousand cycles.

**Incremental make is inconsistent with release protection.** `Makefile:37–38` tries to regenerate the same v126 after a dependency change, while `build_bitmap_sequence.py:48–49` refuses to overwrite an existing XEX. A rebuild after editing sources will fail. Keep archival releases, but provide a separate overwritable working target or explicit target versioning. `make clean` removes the current XEX, so it is not a good way around release protection.

**Incomplete asset dependencies.** The generator reads, among others, all four `trevor-polished-*.rgb` files, but the main target declares only `-0.rgb`. Similarly for the dance/trevor sets. Changing or deleting a single remaining file does not necessarily rebuild the XEX. Declare all actual inputs and the JSON artefact used by the tests; the tests should be certain that they examine the current build.

**False green without py65.** `requirements-dev.txt` calls py65 optional; CPU tests can be skipped and unittest will still return success. In the required release check the dependency must be mandatory. The current audit installed py65 and does not rely on skipped tests.

**Code maintenance.** The repeated DL/copy/PMG emitter in several files makes uniform fixes difficult. Extract parameterised sequence generators, without adding 6502 call overhead. Add rejection of a duplicate label in `Code.label`, which currently overwrites the symbol silently. `AGENTS.md` describes missing sources and tests even though both exist; the document is out of date.

## What is done well

- Drawing to the inactive buffer and separate keys for its contents; the tests check writes to the active image.
- The music wrapper preserves registers and PORTB; the video banks do not replace the required decoder banks.
- Checks of segment collisions and memory limits, bank alias probing and tests of the original pixels.
- Synchronisation of scenes with the player clock rather than with the number of callbacks; the music passes a full comparison in the emulator.
- A build from the current inputs reproduces the supplied XEX byte for byte.

## Recommended order

1. Fix the outdated test and the working rebuild process; enable the required CPU tests.
2. Add measurement of actual frames with DMA/NMI and presentation deadlines.
3. Remove the rebuilding of constant DLs and speed up the shared copies; compare pixels, buffer ownership and POKEY.
4. Prepare the portraits in advance and introduce smaller dance updates.
5. Remove the growing modulo, limit PMG clearing and optimise the plasma passes.

No percentage speed-up of the whole demo is given: the measurements so far show the cost of the current code, and the stated savings of individual loops are estimates. The release after the changes should pass tests of the image, banking, full POKEY and actual presentation time.
