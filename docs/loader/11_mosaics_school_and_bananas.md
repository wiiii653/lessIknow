> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# 11. Mosaics, school scene and bananas — analysis

Read-only analysis: no code, build or tools were changed.
Measurements: py65 on `build/visual-prototype-v294.xex`, callback invoked as
in `tests/test_sequence.py`, without modelling ANTIC DMA.

Legend: `[READ]`, `[CONCLUSION]`, `[ASSUMPTION]`, `[LIMITATION]`.

---

## 1. Important correction of scene names

`[READ]` Tick 8992 (bar 24) is **not the school scene**, only the start of the
side dance with ribbon (Act 2, 8975–11966). The earlier analysis
attributed its cost to the school scene.

`[READ]` Actual costs of the warm callback:

| Scene | Tick | Cycles | Frames (23 712) |
| --- | ---: | ---: | ---: |
| school shot (Act 1) | 4416 | **807** | 0.03 |
| practice | 6096 | **757** | 0.03 |
| side dance | 9496 | **69 302** | 2.92 |
| ribbons (typical) | 15008 | 44 469 | 1.88 |
| ribbons (accent) | 14992 | 91 376 | 3.85 |
| rotator | 32928 | 47 297 | 1.99 |
| tunnel | 35920 | 47 312 | 2.00 |
| title | 1504 | 11 997 | 0.51 |
| outro | 49868 | 10 915 | 0.46 |
| finale | 59104 | 10 203 | 0.43 |

`[CONCLUSION]` The school scene is **very cheap** (807 cycles) — there is
nothing to optimise there. The bottlenecks are the side dance, the ribbons and
the mosaics (rotator/tunnel).

---

## 2. Where exactly the time goes

`[READ]` Cycle breakdown by PC address (callback, cold start):

**Side dance (80 840 cycles):**

| Area | Cycles | Share |
| --- | ---: | ---: |
| `$0C00–$0F3F` — copying + compositor | 49 765 | 61 % |
| `$5400–$5CCF` — ribbon controller | 30 542 | 38 % |
| `$1400–$1DFF` — main code | 405 | 0.5 % |

**Rotator / tunnel (58 731 cycles):**

| Area | Cycles | Share |
| --- | ---: | ---: |
| `$0C00–$0F3F` — frame copying | 38 786 | 66 % |
| `$7C00–$7FFF` — mosaic helper (DL, palette, swap) | 11 984 | 20 % |
| `$7800–$7BFF` — ball/PMG helper | 7 314 | 12.5 % |

**Ribbons, peak (91 376 cycles):**

| Area | Cycles | Share |
| --- | ---: | ---: |
| `$5CD0–$5FFF` — finale/ribbon controller | 60 987 | 67 % |
| `$5400–$5CCF` — compositor | 29 523 | 32 % |

---

## 3. How copying works (the main source of cost)

`[READ]` `tools/engine_effects.py`, `runtime_helper()`:

- copies `5*X` pages of 256 B from the bank (`$4000+`) to the unbanked
  buffer (`$9000+`),
- in one loop iteration it copies **5 bytes in parallel** (one from each
  page), i.e. ~11 cycles per byte,
- `X=2` for the school/tango scene (2560 B), `X=3` for the mosaic (3840 B).

`[READ]` Why it is not possible to display directly from bank `$4000`:
the music NMI switches PORTB to the music bank four times per frame.
ANTIC then reads the same bank as the CPU, so an image from `$4000–$7FFF`
would flicker for the duration of each NMI. A buffer in unbanked RAM is
therefore **required**, not incidental.

`[CONCLUSION]` Copying can only be sped up within the same scheme — e.g. through
self-modifying `STA abs` (4 cycles instead of `STA abs,Y` 5 cycles) and greater
loop unrolling.

---

## 4. Proposals for the mosaics (rotator/tunnel)

| # | Change | Estimated gain | Risk |
| ---: | --- | ---: | --- |
| M1 | Self-modifying `STA abs` instead of `STA abs,Y` in the copy (−16 %) | ~6 200 cycles | low: code in `$0C00`, no data changes |
| M2 | Precompile DL entries for 192 rows per phase and swap the pointer | ~6 400 cycles | medium: table in bank, cache keys |
| M3 | Ball helper: update PMG only when the phase changes | ~3 000 cycles | low |
| M4 | Copy only rows changed between frames | 0–15 000 cycles | high: rotation changes the whole image |

`[CONCLUSION]` M1+M2+M3 give ~15 600 cycles, i.e. rotator/tunnel
from 47 297 → ~31 700 cycles (1.99 → 1.34 frames). Without changing the bank map.

---

## 5. Proposals for the side dance and ribbons

| # | Change | Estimated gain | Risk |
| ---: | --- | ---: | --- |
| T1 | Copying as in M1 (2560 B → −16 %) | ~4 500 cycles | low |
| T2 | Actor overlay: merge pixel+mask into a single byte with a transparency bit (2 operations instead of 4) | ~10 000 cycles | medium: new data format in banks 24–39 |
| T3 | Limit the overlay to the actual bounding box of the pose | ~5 000 cycles | medium: pose metadata |
| T4 | Ribbon controller: skip the rebuild when the phase has not changed | ~5 000 cycles | low |

`[CONCLUSION]` T1+T2 give ~14 500 cycles: side dance 69 302 → ~55 000
(2.92 → 2.3 frames), and the ribbon peaks from 91 376 → ~77 000.

---

## 6. School scene — no need for optimisation

`[READ]` 807 cycles warm, 17 500 cold. That is 3 % of the frame budget.
`[CONCLUSION]` Nothing is worth changing here; the risk of visual regression
would be greater than the gain.

---

## 7. Bananas: alternating rotation at the end of the demo

### 7.1. How it works now

`[READ]` `tools/post_trevor_director.py`:

- montage clock = `tick + 4000` (no offset outside the montage),
- motif: clock bit 10 (`(clock>>5)&32`) — 0 = bananas, 1 = tunnel,
  alternating every 1024 ticks,
- banana phase: `(clock>>4)&31` — 32 phases, step 16 ticks, **always in one
  direction**,
- variant (bunch/peeled banana): `banana_variants.variant_at()` — clock bit 11,
  changes every 2048 ticks.

`[READ]` After `CYCLE_START` (the last third of the montage) the bananas use the
full 32 phases (0–31); earlier, some of the peeled frames use 16 phases.

### 7.2. What I propose

`[CONCLUSION]` Clock bit 11 changes at **every successive** banana window
anyway (windows every 2048 ticks), so it can be used as a direction switch
without an extra counter:

```
phase = (clock >> 4) & 31
if clock >= PROG and ((clock >> 11) & 1):
    phase = 31 - phase        ; mirror = rotation in the opposite direction
```

where `PROG` is e.g. `CYCLE_START` (37984 in the montage clock, i.e. the last
third) or `tick_at_bar(112)`.

`[CONCLUSION]` Effect: the bunch rotates one way, the peeled banana the other,
alternating with each appearance of the fruit. The switch happens at
the moment the banana disappears (the motif changes to the tunnel), so **no
phase jump is visible**.

### 7.3. Cost and implementation

| Element | Cost |
| --- | --- |
| Code in bank 2 (`bank_helper`) | ~15–20 B |
| RAM | 0 B (no new state) |
| Banks | 0 |
| CPU per frame | ~30 cycles |
| Cache keys `$83fa` | unchanged (frame IDs 0–31) |

`[READ]` There is room: the director helper ends before `$7250`
(assertion `BANK_ENTRY+len(data)<=0x7250`), and bank 2 has free areas.

### 7.4. Variant with phase continuity

`[ASSUMPTION]` If mirroring turns out too “jumpy” with longer windows, a window
counter and a phase base can be added (as for tunnels in
`timeline()`): `faza = (base + dir*elapsed) mod 32`. Cost: +1 byte of state
and ~20 B of code. Visual gain: motion starts where it previously
ended.

### 7.5. What not to touch

- `frame_at()` (Python, previews) and `bank_helper()` (6502) must compute the
  phase **identically**, otherwise the previews and the build will diverge.
- IDs 32–59 (tunnel/organic) and 60–63 (eyes) remain unchanged.
- Banana variants (banks 40–48, resources 46/48) and the `$83fa` key unchanged.
- `banana_variants.variant_at()` selects the variant bank independently of the
  phase — mirroring must not change the variant choice.

---

## 8. Order of work and verification

1. **M1 + T1** (faster copying) — lowest risk, ~10 000 cycles.
2. **M2** (precompiled DL) — medium risk, ~6 400 cycles.
3. **T2/T3** (overlay) — larger data change, ~15 000 cycles.
4. **Bananas** (alternating rotation) — independent of the above.

Verification after each change:

```sh
PYTHONPATH=tests:tools /tmp/opencode/tliktb-venv/bin/python -m unittest discover -s tests
ATARI_TEST_XEX=build/visual-prototype-v294.xex PYTHONPATH=tests:tools \
  /tmp/opencode/tliktb-venv/bin/python -c "from test_sequence import execute; \
  print(execute(32928).processorCycles)"
```

`[LIMITATION]` py65 measurements do not model ANTIC DMA; the real gain on
hardware may differ. Changes in copying require frame-by-frame image
comparison with the current build.
