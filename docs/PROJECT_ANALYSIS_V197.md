> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# Project analysis — anchored to v197 (report only)

**Status:** read-only analysis of `build/visual-prototype-v197.xex` with its
matching JSON. No repository file was changed by this analysis. Terminology:
[READ] = direct observation/measurement, [CONCLUSION] = inference from
observations, [ASSUMPTION] = assumption. All line references point at the
checkout as of 2026-11-08.

```
sha256sum build/visual-prototype-v197.xex
a9241df6fde777c27490d338645bdafe825dd4806cc95841278795c2a4bd7170
```

**v197 → v198 relation:** the two JSON sidecars are byte-identical; the XEX
files differ only in orbiting-glyph palette data (V198). Every structural
finding below therefore applies to v197 directly.

## 1. Engine and memory state (v197)

| Measurement | Value from v197 JSON | Location |
|---|---:|---|
| Main code | 2560 B | `$1400–$1DFF`, callback at `$1400` |
| Unique rows / row storage | 298 / 11 480 B | pool from `$1F00`, declared region capacity 12 384 B |
| Midpoint selector | 1370 B | `$4040` in loader index 2 |
| Final-boy controller | 809 B | `$5CD0` in loader index 49 |
| Music NMI entry | `$1BD4` | wrapper with `$D301` save/restore |
| Confirmed free bank gaps | **27 323 B** | incl. `$6E0F–$77FF` (2545 B) in index 2 |

- [READ] **Main code has zero headroom:** exactly 2560/2560 B; the budget
  assert (`tools/build_bitmap_sequence.py:760`) raises on +1 byte. Any future
  unbanked code requires refactoring first.
- [READ] **Documentation-vs-code drift in `AGENTS.md`
  ("Current Memory Ownership"):** hero helper measures **2892 B**
  (ends ~`$4B4C`), doc says 2859 B / ends `$4B2A`; Trevor helper measures
  **2500 B**, doc cites the historical 2466 B; final-boy controller measures
  809 B, doc says 812 B / ends `$5FFB`. Refresh the ownership section before
  the next banking changes.
- Largest confirmed free spaces inside allocated banks: `$6E0F–$77FF`
  (2545 B, index 2), 8 × 512 B at `$5200–$53FF` (indices 24–31), 7 × 372 B
  decoder-bank tails (indices 32–38), 9 × 512 B old ball slots
  (`$5E00–$5FFF`), six 1 KiB `$7C00–$7FFF` ribbon-bank tails (indices 8–13),
  ~112 B at the whistle bank 0 tail, 16 B deliberate gap in dance banks.

## 2. Test suite executed against v197

[READ] Full run with `ATARI_TEST_XEX=build/visual-prototype-v197.xex`:
**149 tests — 141 passing, 5 failures, 3 skipped, 106.7 s.**

| # | Failing test | Substance |
|---|---|---|
| 1 | `test_engine_cache.test_reclaimed_trevor_slots_hold_only_allocated_midpoint_data` | banks 32–38 hold nonzero bytes above the declared midpoint payload, before `$5400` (V173 solo-quarter streams) |
| 2 | `test_ribbon_inbetweens.test_all_fourteen_new_frames_decode_and_have_new_body_and_hand_shapes` | stream length mismatch `19888 != 19296` |
| 3 | `test_ribbon_inbetweens.test_live_solo_quarters_decode_from_banks_with_the_decoder_installed` | decoded frame `(32, 6)` differs from the Python-composed reference |
| 4 | `test_ribbon_inbetweens.test_midpoints_are_exactly_halfway_and_never_bridge_camera_cuts` | `frame_at(tick-1)` returns 51 instead of 4 at a camera-cut boundary |
| 5 | `test_sequence.test_live_scanlines_and_budget` | 22 298 py65 cycles exceed the 21 000-cycle ceiling (school ticks 4862/5236; raised since the v187 PMG melody) |

- **3 skips:** all of `tests/test_optimization.py` — the archived
  `build/visual-prototype-v126.xex` required for cross-release comparison is
  missing; the only inter-release regression net is dead.
- [CONCLUSION] The suite has not been green since V173/V187. These five failures
  also reproduce on the archived v196 XEX, so they are legacy red, **not** a
  v197 regression.

## 3. CPU cost and critical paths

- [READ] Profiles (`docs/ENGINE_PROFILE_V013.md`,
  `docs/V127_OPTIMISATIONS.md`, py65 without ANTIC DMA): worst scenes —
  portraits 129 065 cycles, mosaic 58 255, basketball 56 004, Trevor 44 046,
  parallax 43 511; latest ledger entry 91 282 (`build/v166-allocations.json`).
  PAL frame budget ≈ 35 568 cycles; one music tick ≈ a quarter frame.
- [READ] Bounded publication windows are in place and tested:
  PMG commit inside VCOUNT 124–127, framebuffer/DL publish at `VCOUNT ≥ $7C`
  (`tools/build_bitmap_sequence.py:577-586`), v188 style "keep front DMA until
  the back buffer is complete" in scenes 10–11
  (`tools/build_bitmap_sequence.py:607-618`).
- [CONCLUSION] Remaining CPU is dominated by full-span PMG clears and untracked
  republishing — both are candidates listed in §6; py65 numbers are CPU-only
  and never establish FPS or real raster deadlines.

## 4. Build pipeline

[READ] Highest-leverage observations, each with a reference:

- `tools/build_bitmap_sequence.py::build()` is **868 lines** (53–920): row
  chaining (94–163), scene dispatch (236–377), display list (515–575), v035
  binary patching (787–838), bank loaders (839–866), JSON writer (871–919)
  all inline. Natural seams already exist for a staged refactor.
- Duplicated emission blocks: 8 near-identical `dl1/dl2` row loops;
  **17 copies** of the `VCOUNT=124` blanking wait; 6 inline PMG clear loops
  despite existing `engine_effects.clear_pmg()` (already divergent in
  `ribbon_dance.py:510`); 10 copies of 2-bit packing; 8 copies of palette
  quantization; 4 BFS flood fills; ~15 `_lo/_hi` label patch idioms.
- Generators executed twice per build for JSON stats:
  `ribbon_dance.helper()` (858/887), `final_boy.helper()` (859/902),
  `crush_helper` (77/754); `ribbon_dance.metadata()` reads `artwork(f)` 8×
  per frame; `metadata()` itself runs twice (~2.4 s duplicated).
- Python regeneration cost per full build ≈ 10–20 s; caching is in-process
  only (`lru_cache`), no disk cache; any `tools/*.py` edit forces a full
  rebuild (`Makefile:36`).
- Orphan script: `tools/prepare_school_pan.py` (no consumers); `make clean`
  removes only 6 of dozens of accumulated `build/` artifacts; import cycle
  `arena_art` ↔ `school_story` resolved by local imports in 8+ modules.
- Safety net is Python `assert` only (stripped silently under
  `PYTHONOPTIMIZE`); JSON has no timestamp/hash/version (contrast
  `extract_music.py:44`); the two 7936-byte framebuffer clears are appended
  **after** the global overlap check (`build_bitmap_sequence.py:778-781` vs
  `:786`) and are safe only by the row allocator's region ceilings.

## 5. Formal risk register

1. **Bank 49 is triple-reserved and order-sensitive:** ribbon controller from
   `$5400`, final-boy controller `$5CD0–$5FFB`, Trevor engine from `$6000`;
   inter-controller gaps are 10 B and 4 B. Only install order (not local
   checks) keeps them separated. [READ]
2. **`$0DC0–$0DCF` workspace is load-bearing** for the midpoint selector; any
   stray write silently corrupts stepping (`tools/ribbon_inbetweens.py`).
3. **Scene numbers are bare literals** in behavior branches:
   `CMP #2/#10/#12` chains in `build_bitmap_sequence.py:609-618` and
   `engine_effects.py:41-52`; `CMP #14` for the ribbon NMI work. Renumbering
   scenes silently changes behavior.
4. **v035 magic anchors** (`0x21bc`, `0x220a`, `0x218f`, `0x2312`, countdown
   operands `$34DA–$34DE`) fail loudly on mismatch but are undocumented; PORTB
   immediates in scene code have no build-time cross-check against
   `bank_value()`.
5. **STATE byte map `$83E0–$83FF`** is convention only; collisions of a
   new-byte assignment are undetectable at build time.

## 6. Recommended action list (not executed)

In order, cheapest first where applicable:

1. **Green the suite.** Fix the five legacy failures: reconcile declared
   payload lengths vs banked V173 streams, the inbetween frame numbering at
   camera cuts, and either raise or re-justify the 21 000-cycle school-scene
   ceiling (actual measured 22 298; documented growth since v187).
2. **Restore inter-release regression:** base the comparison on a recent
   archived XEX (v197 itself is available) instead of the lost v126.
3. **Refactor `build()` into named stages** and hoist the DL/blanking/clear
   emissions into `engine_effects.py`. Regression gate: byte-identical
   generated XEX vs `build/visual-prototype-v197.xex`.
4. **Central `memory_map.py`:** unique STATE-byte and PORTB assignments plus
   the confirmed free-gap ledger; regenerate an allocations JSON for the
   current release.
5. **Refresh `AGENTS.md` ownership numbers** (hero 2892 B, Trevor 2500 B,
   finale 809 B, gaps 27 323 B) and drop the orphan script.
6. **Then runtime optimizations:** dirty-row PMG tracking instead of full
   5 × 128 B clears per publish, scene-flag bit table replacing
   compare-chains, LZ match-length ≥6 for the four solo-quarter streams
   (currently ≥8).

## 7. Summary verdict

[CONCLUSION] v197 is a solid anchor for further production: the identified bank
gaps and the engine's bounded-publication discipline support the remaining
ambitions (credits/greetz windows at ticks 53850–56842 and 56842–59085, Acts
5C/5D and 6–7). The real blockers are not on the hardware side: a red test
suite, zero main-code headroom, and the monolithic builder slow every future
scene. Clean those first; new features afterwards will then ride on a green,
regression-protected base.
