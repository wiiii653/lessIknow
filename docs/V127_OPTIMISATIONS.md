# V127 — copy, display list and PMG optimisation

[READ] Release: `build/visual-prototype-v127.xex`. SHA-256:
`7a344c4aa5afe7fe8f2acc15e7164498bb1ed20edfa6d8ac149d1da7b8370d5b`.
V126 remains preserved and unchanged. The working build `visual-prototype-dev.xex`
is byte-identical to v127. Scene boundaries, ticks and artwork were not changed.

## Engine changes

- The shared code outside the banking window copies five pages per index turn.
  Parallax and Trevor copy two such groups, the mosaic three. This replaces
  loops performing INY/BNE after every byte of a separate page.
- Two independent display list layout labels allow skipping the build of
  192 LMS addresses when the inactive DL already has the required layout. The mosaic,
  tripled-64 (parallax/Trevor), basketball player and portraits have separate keys.
  The plain-scene renderer invalidates both keys before changing addresses.
  The DL layout cache does not replace the framebuffer content cache.
- The mosaic colour phase uses division by decreasing multiples of 187:
  eight steps instead of a growing number of subtractions. The 11968/32912 bases,
  the palette shift and the pulse phase remain consistent with v126.
- PMG clearing in the basketball player, portraits and BANG uses five disjoint
  128 B segments. It removes duplicate writes to $0A00–$0A7F and reduces the
  iteration count from 256 to 128. The final data at $0980–$0BFF is identical.
- The basketball player copies the bitmap tail without JSR/RTS and without rewriting
  the operands for each of the 192 bytes.
- The emitter rejects duplicate labels instead of silently changing their addresses.

[READ] Reservation of $0C00–$0DFF for the copy helper, key checking and the keys
$0DFE/$0DFF. The packed-row pool starts at $0E00 in this fragment;
the collision check covers the helper. The main callback code grows from 1822 to
1830 B. The code still fits within the existing limits and the same banks.
The shared helper does not change PORTB; the NMI wrapper still restores the foreground bank.

## CPU results

[READ] The same set of 589 samples as in the v126 audit. Raw data:
`AUDIT_V126_CYCLES.json` and `V127_CYCLES.json`. The maximum concerns the examined
fragment, and the sum also covers cache hits and first fills.

| Fragment | v126 maximum | v127 maximum | Fewer maximum cycles | Fewer cycles over sample sum |
|---|---:|---:|---:|---:|
| Parallax | 53 684 | 43 511 | 19.0% | 21.1% |
| Mosaic | 73 698 | 58 255 | 21.0% | 25.8% |
| Portraits | 130 470 | 129 065 | 1.1% | 8.7% |
| Basketball player | 66 049 | 56 004 | 15.2% | 24.8% |
| Trevor | 55 496 | 44 046 | 20.6% | 31.5% |
| Late mosaic | 78 378 | 58 525 | 25.3% | 37.5% |

[READ] The number of calls over 35 568 cycles fell from 10 to 2 out of 75 parallax
samples and from 15 to 2 out of 75 Trevor samples. The remaining phases can still
exceed the one-frame budget. Intro/title/school/dance/training have up to
10 cycles of extra cost per DL rebuild due to key invalidation;
their main rendering loops were not accelerated. At the start of the mosaic,
bounded division may cost more than the short old loop (minimum
7842 instead of 7698); however, it removes the growing cost of the late part of the track.

[ASSUMPTION] These are measurements of CPU instructions in py65: without ANTIC DMA, music NMIs
and actual raster waiting. The sample sum is not a percentage of
whole-demo speed-up nor an FPS result. For comparison on an emulator
with hardware timing, presentation moments and skipped phases still need measuring.

## Verification

[READ] `make check PYTHON=/tmp/atari-audit-venv/bin/python`: **83 tests OK**,
88.662 s. It covers the existing pixel, active buffer, banking,
music interrupt tests and three new regression tests:

- raster, GTIA registers and PMG memory against archival v126 at scene
  boundaries, restarts and 40 deterministic random tick jumps;
- palette consistency at beat and pulse boundaries, for both colour phase bases;
- skipping LMS writes after both layouts have warmed up, and the drop in total update
  cost in the examined scenes.

The old expectation `tick >> 5` was corrected to `tick >> 4` only for the DANCE
section in the transitions test. Selection of the second half of the mosaic motif keeps `>>5`.

[READ] Atari800 PAL/1088XE, stereo POKEY, Altirra OS:
`tools/check_playback.py --seconds 12` — PASS, **3 637 368 identical bytes**,
about **1013.2 s** of emulation, the whole track. The final working build was tested,
identical to v127. This is register consistency, not a listening test on physical Atari.

## Building and repeating the measurement

`make` now generates an overwritable `visual-prototype-dev.xex` build together with JSON.
Both are a common Make target, dependent on the tools and all atlas files.
`make check` requires py65 instead of allowing the CPU tests to be skipped.
We create numbered releases with an explicit `--output` without `--replace`.

```sh
make all PYTHON=/tmp/atari-audit-venv/bin/python
make check PYTHON=/tmp/atari-audit-venv/bin/python
/tmp/atari-audit-venv/bin/python tools/profile_engine.py --xex build/visual-prototype-v126.xex --output /tmp/v126-cycles.json
/tmp/atari-audit-venv/bin/python tools/profile_engine.py --xex build/visual-prototype-v127.xex --output /tmp/v127-cycles.json
```

## Remaining potential

The largest further topics from the audit: preparing extended portraits before
the scene, smaller dance updates and limiting the passes of the plasma
composition. V127 does not implement these data format changes. The current stage removes the common
overhead and provides a verified basis for these more extensive optimisations.
