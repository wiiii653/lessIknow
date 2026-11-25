> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# Prerelease 170 audit — report only

**Status:** read-only audit of the current development tree and
`releases/less-i-know-demo-prerelease-170-stereo.xex`. No engine, tool or test
file was changed by this audit; this document is the only addition.

**Date:** 2026-11-23
**Baselines:** prerelease 170 (current candidate), release 133 / v390 (latest
approved), and a clean `HEAD` worktree build.

Terminology: **[READ]** = direct measurement, **[CONCLUSION]** = inference from
measurements, **[ASSUMPTION]** = assumption. No claim in this document is a
physical-hardware result.

## 1. Artifact identity

| Artifact | Size | SHA-256 |
|---|---:|---|
| `releases/less-i-know-demo-prerelease-170-stereo.xex` | 1,044,733 B | `f0f0f7c9ac6cbea629ad8e3247610f21a9ea8da9662ef25e434372a7b2597810` |
| `build/hardware-dev.xex` | 1,044,733 B | same |
| rebuild from current tree (`make hardware` flags) | 1,044,733 B | same |

[READ] Prerelease 170 is byte-identical to the hardware package rebuilt from
the current tree. The tree therefore reproduces 170 exactly.

[READ] The prototype source is `build/visual-prototype-dev.xex`, 1,116,327 B,
SHA-256 `71acc51a494dce5e3a6f5b822b2a6f964da077f907fc1d8a0e1d6040109c8282`,
295 shared rows, 2,541 code bytes.

[READ] A clean `HEAD` worktree builds a prototype with 295 shared rows and
2,497 code bytes, so the uncommitted working-tree edits add 44 bytes of
unbanked code.

**Documentation drift.** `docs/PLAN_STATUS.md` still names prerelease 165 as the
accepted final stereo prerelease. 166–170 exist; 170 is the newest. 170 is
untracked in git. If 170 is the current candidate, it should be recorded with
its SHA and committed or archived like a numbered release.

## 2. Packaging and the 1 MiB bound

[READ] `tools/build_hardware_xex.py` enforces `len(result) < 1024*1024`
(1,048,576 B).

| Build | Size | vs bound |
|---|---:|---:|
| release 133 (approved) | 952,239 B | 96,337 B free |
| prerelease 170 (shipped) | 1,044,733 B | **3,843 B free (0.37%)** |
| current `build()` default | 1,040,648 B | 7,928 B free |
| current `build(fast_clear=True)` | 1,051,848 B | **3,272 B over** |

[READ] The 4,085 B difference between `build()` and the shipped artifact is
`with_approved_music()` plus `animated_loading.install(full_rate=True)`.

[READ] Because the fast-clear variant exceeds the bound,
`test_hardware_loader.setUpClass` raises `ValueError: Hardware XEX exceeds the
established size bound`. The class contains 11 tests and none of them run.

[READ] `compact()` (`tools/build_compact_xex.py`) strips only runs of `0x00`,
never `0xFF`. On 170:

| Measurement | Value |
|---|---:|
| bank payload bytes | 993,657 B |
| `0xFF` bytes inside them | 55,387 B (5.6%) |
| `0xFF` runs ≥16 B | 69 |
| bank segments >16,000 B | 26 (release 133: 10) |

[CONCLUSION] Zero-run compaction is nearly exhausted; the remaining large
reclaimable block is the `0xFF` padding in the v035 music banks.

[CONCLUSION] Stripping `0xFF` runs requires a per-bank staging prefill change,
which touches the hardware-confirmed clear protocol. It must be validated on
physical hardware, not only in py65.

## 3. Test suite state

Command: `python -m unittest discover -s tests` from the repository root.
[READ] 212 tests, 13 failures, 1 error.

The packaged XEX cannot be used as a test target: the harness needs the
prototype format plus the `.json` sidecar (`callback`). Results below are from
the dev prototype, which reproduces 170 through `make hardware`.

| # | Test | Message | Introduced by |
|---|---|---|---|
| 1 | `test_dunk_ball_follows_hand_until_release` | `7 not less than or equal to 1` | already at `HEAD` |
| 2 | `test_scene_handoffs_and_restart` | `14 != 6` at `CRUSH_START-1` | already at `HEAD` |
| 3 | `test_banana_impact_fades_shrinks_and_travels_safely` | `False is not true : 48` | already at `HEAD` |
| 4 | `test_both_late_banana_sections_include_word_and_satellites` | `[0,0,0,0] != [1,1,1,1]` | already at `HEAD` |
| 5 | `test_first_publication_is_already_the_lower_frame` | `(74,154,42) != (76,156,44)` | uncommitted edit |
| 6 | `test_four_satellites_orbit_…` | `[62,64,66] != [62,63,64]` | already red on v390 |
| 7 | `test_satellites_follow_airborne_ball_…` | `70 != 67` | already red on v390 |
| 8 | `test_dunk_keyframes_and_ball_match_the_archived_release` | PMG bytes differ | already red on v390 |
| 9 | `test_release001_poses_change_only_in_background_masks` | `3 != 1` | already red on v390 |
| 10 | `test_scene_boundaries_animation_and_bank_restoration` | `[246,186,154] != [246,186,46]` | already red on v390 |
| 11 | `test_front_solo_ribbons_have_independent_phases_…` | PMG mismatch at tick 17930 | already red on v390 |
| 12 | `test_midpoints_are_exactly_halfway_…` | `43 != 51` | already red on v390 |
| 13 | `test_v330_walk_with_only_four_profile_pixels_changed` | extra changed pixels at 4998, 5000, 5158… | already red on v390 |

Plus the `test_hardware_loader` `setUpClass` error from section 2.

### 3.1 Confirmed defects

**Dribble ball is 3 rows high.** All eight dunk keyframes were measured against
the expected hand positions:

```
v390 : ballY 51, error 1   (pose 2, dribble)
HEAD : ballY 48, error 7
dev  : ballY 48, error 7
```

Poses 3–5 are exact. In doubled PMG rows the dribble ball is about six raster
lines above the hand. Present in the committed `HEAD` tree.

**Portrait scene starts one tick early.**

```
tick 14958 (CRUSH_START-1) expected 6, got 14   (HEAD and dev)
tick 14959 (CRUSH_START)   expected 14, got 14
v390 at 14958: 6
```

A one-tick boundary error, also already committed.

### 3.2 Retiming, not lost sprites

The four-satellite formation still exists, but its visibility window moved:

```
all four players non-empty, ages after bar 108:
v390 : 48 .. 85  (38 ages)
HEAD : 96 .. 99  (4 ages)
dev  : 96 .. 99
```

Plane 3 is drawn in 1,274 of 1,496 sampled frames in every build, so the sprite
is not missing. Player sizes are `[1,1,1,1]` in 1,246 of 1,496 samples; the
failing assertion samples one of the boundary frames. Tests 3 and 4 encode the
old timing.

### 3.3 Uncommitted-only failure

Test 5 differs by exactly 2 on all three channels, consistent with the new
`PORTRAIT_LUMA` path in `tools/outro_palette.py` and `tools/final_boy.py`. This
looks like an intentional visual change; the test still asserts the old
constant.

## 4. Dead code and build-time waste

[READ] pyflakes reports 18 items in `tools/`:

- `build_bitmap_sequence.py`: unused imports `text_pixels`, `dance_pixels`,
  `dance_group_pixels`, `PALETTE`, `ROWS`, `gtia11_pixels`, `BALL_PATH`,
  `CRUSH_DATA`; unused locals `portrait_data` and `portrait_code` (two sites).
- `final_boy.py`: `outro_text.START`.
- `girl_eyes.py`: `math`.
- `gym_practice.py`: `gym_pixels`.
- `outro_text.py`: local `row`.
- `render_sequence_preview.py`: `video_memory`.
- `ribbon_dance.py`, `trevor_polished.py`: `clear_pmg`.
- `audit_tunnel_pmg.py`: `pathlib.Path`.

[READ] `crush_helper()` is built twice and `crush_packed()` once, and all three
results are discarded (`build_bitmap_sequence.py:95-96` and `:807`).
`crush_helper([])` also passes a list where an `eyes` argument is expected.

[READ] Zero-reference constants: `mosaic.TREVOR_START`,
`post_trevor_director.TIMELINE_ENTRY`, `basketball_hero.SHATTER_Y`,
`outro_text.STATE_PHASE`.

[READ] `sample_rows` (`build_bitmap_sequence.py:100-102`) has two identical
branches: `frame < 2` and `frame < 6` both return all 192 rows.

[READ] `build/visual-prototype-dev.json` writes `crush_entry` from
`ribbon_dance.ENTRY` (21504), not `crush_portraits.ENTRY` (0x4B10). The key name
is misleading for any tooling that reads it.

## 5. Memory

[READ] Main code: 2,541 B at `$1400–$1DEC`.
[READ] Shared rows: 295, 11,548 B stored (11,800 B unpacked).
[READ] LMS table: `$D800`, 3,264 B; plasma 2,272 B ends at `$EDA0`.
[READ] `$EDA0–$FE87` (4,328 B) is unallocated. It lies under OS ROM, so it is
usable only with the OS disabled.

[READ] Bank 8 retired-portrait gap: 5,360 B (`$4B10–$5FFF`). The new practice
overlay uses 568 B of note data at `$4B10–$4D47` and a 4,096 B code page at
`$5000–$5FFF`; about 696 B remains zero. This gap is now mostly reclaimed.

## 6. Duplication

- **Eight copies of the 192-row LMS display-list builder**: `basketball_hero`,
  `crush_portraits`, `final_boy`, `mosaic`, `ribbon_dance`, `school_parallax`,
  `trevor_awakens`, `trevor_polished`. `engine_effects.py` already hosts
  `cached_display_list` and `clear_pmg`, so the row loop belongs there too.
  Each copy lives in a different bank, so the cost is maintenance risk rather
  than low-RAM pressure.
- **Eight copies of the palette quantizer** (`min(range(4), key=lambda …)`):
  `build_sequence`, `gym_background`, `crush_portraits`, `gym_practice`,
  `trevor_awakens`, `school_story`, `prepare_production_art`,
  `trevor_polished`.
- **Three copies of XEX segment parsing**: `dump_bitmap_assets.py`,
  `dump_runtime_planes.py`, `extract_music.py`.
- **Shared scratch map `$83E0–$83FF`**: 31 addresses used by about 20 modules
  with no central definition. `$83EF` is now both Trevor impact Y and
  `final_boy.PORTRAIT_LUMA`; `$83ED` means scene id, ribbon frame, banana phase
  or tunnel rotation depending on the module. This is the highest structural
  risk in the tree.

## 7. Recommended order

1. Decide whether prerelease 170 is the current candidate; record its SHA in
   `docs/PLAN_STATUS.md` and commit or archive it.
2. Fix the dribble ball Y and the one-tick-early portrait boundary.
3. Confirm whether the satellite retiming is intended; update tests 3 and 4 if
   it is.
4. Update test 5 to the new portrait luma, or revert the luma change.
5. Decide on `0xFF` stripping for bank payloads. It recovers about 55 KB but
   requires hardware validation.
6. Clean up dead build calls, unused imports and the eight duplicated row
   builders.
7. Triage the eight failures that are already red on v390; they do not describe
   170 but they hide future regressions.

## 8. What looks sound

- The allocator asserts overlap, ANTIC page crossings and region spans.
- The hardware loader re-validates INIT order, INIT count and bootstrap spans.
- PORTB is saved and restored around banked calls.
- The practice overlay clears PMG before the VCOUNT window, as the loader
  contract requires.
- Bank 8 reuses the retired portrait gap instead of leaving it empty.

## Appendix — reproduction

```sh
# hardware package identity
sha256sum releases/less-i-know-demo-prerelease-170-stereo.xex build/hardware-dev.xex

# prototype
python tools/build_bitmap_sequence.py --replace

# hardware package (same flags as the Makefile)
python tools/build_hardware_xex.py build/visual-prototype-dev.xex \
    /tmp/opencode/hw.xex --approved-music --release-122-music --full-rate-loading

# tests (cwd must be the repository root)
python -m unittest discover -s tests

# clean HEAD comparison
git worktree add /tmp/opencode/head-wt HEAD
cd /tmp/opencode/head-wt && python tools/build_bitmap_sequence.py --output /tmp/opencode/head.xex
```

**Limits.** py65 does not model ANTIC DMA or physical raster deadlines. No
result here is a playback, visual or compo-readiness confirmation. The last
full playback confirmed by the user remains stereo release 058 / v330 on an
Atari 1088 Rambo via AVG.
