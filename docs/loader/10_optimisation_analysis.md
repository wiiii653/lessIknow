# 10. Optimisation analysis (no code changes)

The document describes **possibilities** for optimising the current demo. It was
created in read-only mode: no production file, build or tool was changed. All
numbers come from measurements taken on the current build
(`build/visual-prototype-v294.xex`, `releases/less-i-know-demo-release-031-stereo.xex`).

Legend: `[READ]`, `[CONCLUSION]`, `[ASSUMPTION]`, `[LIMITATION]`.

## Quick clear in 100 and 101 · 2026-11-19

Optional releases were built from A2, preserving the whole 058 loading protocol
apart from the clear code at `$3A00`. A segment comparison showed exactly 64
replacements of the procedure. Each file is 960 077 B.

Atari800 PAL, emulated 1088 XE, Altirra OS. From entry into the `$38A0` loading
screen to the jump to the player at `$13E0`, 17.81 s elapsed in 098/099 and
14.53 s in 100/101, i.e. **3.28 s (18.4%)** less. The emulator ran 64 clears in
each file. 6 loader tests passed, and all 59 833 POKEY packet writes matched
098/099. The measurement covers a direct XEX start in the emulator. The trial
and measurement on physical AVG remain undone.

- [100 stereo](../../releases/less-i-know-demo-release-100-stereo.xex)
  · SHA-256 `4201e6a6c5faac3693a42faca8354a1ad3d9adfc8b6682ec99574a9d62379f24`
- [101 mono on a single POKEY](../../releases/less-i-know-demo-release-101-mono.xex)
  · SHA-256 `cecc647a0bd38ae990203ad5ec7d9ad16e16611f38bfff1e15d0a9adeec4407c`

The option is provided by `tools/build_hardware_xex.py` and
`tools/build_audio_revision.py` as `--fast-clear`.
[Loader contract and scope of the replacement](../HARDWARE_LOADER_CONTRACT.md).

## State before the trial, releases 098 and 099

Both files are 948 877 B each. The startup invariants, including the code at
`$3A00` and `$1000`, were checked against release 058. The A1–A3 speed-ups are
still proposals. The
[AVG / Rambo hardware contract](../HARDWARE_LOADER_CONTRACT.md) applies.

The A2 trial in py65 memory shortened the full `$8000–$BFFF` clear from 164 535
to 83 747 cycles per bank. That is 2.92 s less CPU work for 64 banks at the PAL
clock. The procedure preserved A, X, Y and the flags. The trial code grew from 37
to 212 B, so repeating it in the XEX adds the cost of transferring 11 200 B. The
trial did not include DMA, AVG work or a measurement of the whole startup.

The B1 simulation on 64 bank images from release 098 gives a XEX smaller by
20 537 B, but increases the number of bank data segments from 1 456 to 4 745.
The time gain depends on how AVG handles segments. The A1 and A2 estimates
concern the same clear, so they must not be added up directly. None of the trials
was introduced into the release files.

---

## 1. Input metrics

| Metric | Value |
| --- | ---: |
| Base of 64 banks (`visual-prototype-v294.xex`) | 1 111 760 B |
| Release 031 stereo | 941 515 B |
| Segments in release | 1 770 |
| Data in the bank window | 886 177 B |
| Remaining data (runtime) | 48 256 B |
| Segment headers (4 B × 1770) | 7 080 B |
| 16 KiB banks | 64 (1 048 576 B) |
| Zeros in banks | 335 472 B (32.0 %) |
| Unique banks | 64 of 64 (no duplicates) |
| Shared rows | 298 (`row_storage_bytes` 11 494 B) |
| Main code | 2 560 B (`$1400–$1DFF`) — no headroom |

`[READ]` INITs in release 031: `$38A0`×1, `$3900`×66, `$3A00`×64,
`$4800`×1; RUN `$13E0` (not used for startup).

---

## 2. CPU time budget

`[READ]` PAL frame: 312 lines × 76 cycles ≈ **23 712 cycles**.
With four callback invocations per frame the budget per call is **5 928 cycles**
(for 50 fps).

`[READ]` Measured callback costs (py65, no DMA, after cache warm-up; successive
ticks on the same CPU):

| Scene | Cycles | How many frames |
| --- | ---: | ---: |
| title | 11 997 | 0.51 |
| side dance (Act 2) | **69 302** | **2.92** |
| ribbons | 44 469 | 1.88 |
| Trevor | 443 | 0.02 |
| rotator | 47 297 | 1.99 |
| tunnel | 47 312 | 2.00 |
| outro | 10 915 | 0.46 |
| finale | 10 203 | 0.43 |
| school shot (Act 1) | 807 | 0.03 |
| practice | 757 | 0.03 |

`[READ]` Correction: in the first version of this document the scene called
"school" was tick 8992, which belongs to the side dance. The real Act 1 school
shots cost ~807 cycles and do not need optimisation. Details and address
profiles: [11_mosaics_school_and_bananas.md](11_mosaics_school_and_bananas.md).

`[CONCLUSION]` The side dance, rotator, tunnel and ribbon scenes exceed the
one-frame budget several times over. The music stays in time because the NMI
runs independently, but the image refresh in these scenes is CPU-limited.
`[LIMITATION]` py65 does not model ANTIC DMA or real raster deadlines; on
hardware the cost will be even higher.

`[READ]` The "cold" cost (fresh CPU, empty caches) is much larger: title 131 812,
side dance 81 018, outro 192 825 cycles. This explains why the first call after a
scene change is expensive.

---

## 3. Loader cost (loading time)

`[READ]` Measured by emulating code fragments from the release:

| Stage | Cycles | For 64 banks |
| --- | ---: | ---: |
| Bank clear (`$3A00`) | 164 535 | **5.94 s** |
| Copying 16 KiB (`$1000`) | 230 409 | **8.30 s** |
| Probing and bank selection | ~30 thousand/bank | ~1.9 s `[ASSUMPTION]` |
| **Total loader CPU overhead** | | **~16 s** |

`[CONCLUSION]` About 16 s of loading is pure 6502 work, independent of SIO.
Clearing and copying are 86 % of that time.

`[READ]` The clear runs under `SEI`; a single bank is a ~93 ms block without
interrupts. It does not affect the music (which is not playing yet), but it
lengthens the load.

---

## 4. File size analysis

`[READ]` Zeros make up 32 % of the bank data. The current zero-run skip threshold
in `tools/build_compact_xex.py` is **16 B**. Simulation for the current bank set
(including headers and clear code):

| Threshold | Bank + clear size | Saving vs 16 B | Data segments |
| ---: | ---: | ---: | ---: |
| 4 B | 838 734 B | +30 137 B | 14 235 |
| 8 B | 848 405 B | +20 466 B | 4 675 |
| **16 B (current)** | **868 871 B** | — | 1 401 |
| 32 B | 883 744 B | −14 873 B | 532 |

`[CONCLUSION]` Dropping to the 8 B threshold gives **~20 KB less** at +3 274
segments. The 4 B threshold gives a further ~10 KB, but the number of segments
grows to 14 235, which lengthens the handling of the file by the file loader.

`[READ]` No duplicate banks — deduplication would gain nothing.
`[READ]` No bank fits in the first 8 KiB (the last non-zero byte ≥ `$27FF`), so
shortening a bank to 8 KiB is not possible without redesigning the layout.

`[READ]` The runtime data is only 48 KB — compressing this part would gain at
most a few KB and complicates startup.

---

## 5. Optimisation candidates

### A. Loading time — the biggest potential

| # | Idea | Gain | Risk | Dependencies |
| ---: | --- | ---: | --- | --- |
| A1 | Clearing only the skipped ranges (not whole 16 KiB) | ~4.0 s | medium | new range code/table; `$3A00` and its self-mod `$3A14` |
| A2 | Unrolled `STA abs` instead of a `STA abs,Y` loop | ~2.5 s | low | clear code size; A/X/Y/flags preservation |
| A3 | Unrolled copy (`LDA abs,Y` × N / `STA abs,Y` × N) | ~1.7 s | low | `school_portrait_bank.loader`, INIT code length |
| A4 | Loading banks directly into `$4000` (as in another 1 MB demo) | ~8.3 s + 2 KiB RAM | high | the whole XEX structure, compact pass, no `$8000` buffer |
| A5 | Probing banks only once and writing the table permanently into the build | ~1.9 s | high | portability between clones; test `avg-bank-map-diagnostic-003` |

`[CONCLUSION]` A1–A3 do not change the file format and can give **~8 s** shorter
loading in total while preserving all invariants.
A4 is the biggest gain, but it requires rewriting the loader and revalidating the
whole startup.

### B. File size

| # | Idea | Gain | Risk |
| ---: | --- | ---: | --- |
| B1 | Zero threshold 16 → 8 B | ~20 KB | low |
| B2 | Zero threshold 8 → 4 B | ~10 KB | medium (14 thousand segments) |
| B3 | Runtime data compression | ~2–5 KB | high (decoder, RAM) |
| B4 | Bank deduplication | 0 B | — |

`[READ]` B1 requires no changes to the 6502 code — only to the compacting tool.
`[LIMITATION]` Changing the threshold changes the number of segments and the file
handling times; the POKEY comparison and the startup test must be repeated.

### C. CPU during playback

| Scene | Cost | Proposal |
| --- | ---: | --- |
| side dance | 69 302 | faster copying (M1/T1); actor overlay (T2/T3) |
| rotator/tunnel | ~47 300 | limit copying to dirty pages (already 5 376 B of 7 936 B); consider double buffering and LMS swapping |
| ribbons | 44 469 | composite only the actor area; limit PMG clearing to the active ranges |
| title | 11 997 | cache the plasma composite; refresh only the changed rows |
| outro/finale | ~10 200 | cheap so far; not a priority |

`[CONCLUSION]` Cutting the school cost in half would give ~1.5 frames of headroom
and would improve smoothness the most. That is, however, a change in the scene
generators, not in the loader.

### D. Memory and main code

- `[READ]` Main code 2 560 B in `$1400–$1DFF` — **zero headroom**.
  Freeing space requires merging the `compare_tick`/`compare_tick16` trampolines
  or moving part of the logic into a bank.
- `[READ]` The 298-row / 11 494 B pool is already deduplicated.
  Further gain only by sharing rows between scenes
  (requires changing the cache keys).
- `[ASSUMPTION]` Checking which rows are used in only one scene
  could point to candidates for removal after artistic changes.

---

## 6. Loader dependencies — what must not be touched

`[READ]` The following elements are coupled together; changing one requires
checking the others.

### 6.1. Fixed addresses

| Address | Role | Note |
| --- | --- | --- |
| `$3800–$3877` | loading screen | must not collide with runtime segments |
| `$3880–$388A` | display list | must lie within a single 1 KiB page |
| `$38A0–$38DC` | screen INIT | sets CHBASE `$D409` and the colours |
| `$3900–$398B` | INIT wrapper (diagnostics) | optional; removed by skipping stage 2 |
| `$3A00–$3A24` | bank clear | **self-mod at `$3A14`** |
| `$4000–$47FF` | low memory buffer | inside the bank window |
| `$4800–$4873` | bootstrap + `JMP $13E0` | must be the last INIT |

### 6.2. Invariants

1. Between the `$4000–$47FF` segment and the `$4800` INIT, **PORTB must not be
   changed** — the bootstrap reads the same bank.
2. `LOW` in `build_avg_late_lowram.py` must correspond to the actual
   low memory segments; adding a range requires a new copy loop.
3. Selector tables: `$24B3–$24B5` and `$08C3–$08F1`; `bank_value()` must
   agree with the loader and all consumers.
4. Exactly 64 banks; banks 0/1 are computed arithmetically without verification.
5. Bank 39 holds the finale bitmap and the side actor; bank 49 the controllers.
6. Banks 40–48 act as the overlay (plasma, fireworks, bananas 46/48).
7. INIT order: screen → 14 v035 banks → 50 video banks → runtime
   segments → `$4000` buffer → bootstrap.
8. Start: `JMP $13E0` from the bootstrap; RUNAD exists but is not used.
9. The clear code assumes that the whole `$8000–$BFFF` is zeroed before the
   bank data — changing the zero threshold in the compactor must not break this.
10. `SEI` in the clear: do not add NMI-dependent code there.

### 6.3. Places reading `$D301`

`[READ]` `run_stub`, `school_portrait_bank.loader`, `banana_cache`,
`banked_effects`, `ribbon_copy`. On the tested hardware the read works,
but it is not portable. Any optimisation of these blocks should either
preserve the `PHA/PLA` pattern or introduce a shadow in RAM.

---

## 7. Priorities

| Priority | Change | Gain | Risk | Impact on the loader |
| ---: | --- | ---: | --- | --- |
| 1 | A1 + A2 (clear) | ~6 s | medium | `$3A00` code, self-mod `$3A14` |
| 2 | A3 (copy) | ~1.7 s | low | `school_bank_loader`, INIT length |
| 3 | B1 (8 B zero threshold) | ~20 KB | low | compact pass, segment count |
| 4 | C side dance | ~0.6 frame | medium | composer, cache |
| 5 | C rotator/tunnel | ~1 frame | medium | mosaic renderers |
| 6 | A4 (loading into banks) | ~8 s | high | the whole XEX structure |

`[CONCLUSION]` Best gain-to-risk ratio: **A2 + A3 + B1**.
They do not touch the bank map, the INIT order or the startup.

---

## 8. What cannot be improved cheaply

- `[READ]` Bank deduplication — no duplicates.
- `[READ]` Shortening banks to 8 KiB — the data reaches the end of the 16 KiB.
- `[READ]` Runtime compression — only 48 KB, the gain is disproportionate
  to the risk of a decoder in base memory.
- `[LIMITATION]` Shrinking the main code without a refactor — 2 560 B
  is exactly filled.

---

## 9. How to verify changes

1. `make check` — 200/200.
2. XEX structure comparison: 64 banks, INITs `$38A0/$3900/$3A00/$4800`.
3. Repeat the stereo POKEY comparison in Atari800 1088XE against v035.
4. Startup test on physical Atari (AVG, Rambo 1 MB).
5. Loading time measurement on hardware (stopwatch) before and after.
6. Measurement of warm callback cycles in py65 for the scenes: side dance, rotator, tunnel.

`[LIMITATION]` Points 1–3 and 6 do not confirm smoothness or the behaviour of the
physical AVG loader.
