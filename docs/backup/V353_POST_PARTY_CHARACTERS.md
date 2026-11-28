> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# Hardware note — 2026-11-17
The user confirmed the failure of the raw v353 prototype on a physical Atari.
For the next attempt `releases/less-i-know-demo-release-062-stereo.xex`
was prepared with the loader of working 058. Rules and actual validation:
[loader contract](../HARDWARE_LOADER_CONTRACT.md). The prototype below is not itself a
distribution file for AVG.

# V353 — first character polish after the party

Stereo prototype for graphics assessment. It keeps the v352 montage and its player ticks.
It is not a new production release nor a Pouët package.

## Image changes

- Opening: a hand-defined girl character on a 48×64 grid,
  a separate opacity mask and a deliberately drawn far 12×16 variant.
  The black contour pixel remains opaque; the spaces
  between the legs show the background. Positions, shot scale and the Fuji on the jacket
  were preserved.
- Walk before the arena: head, profile and hair replace the noisy frame
  fragment in the 18 existing frames. Around the new silhouette a
  clean arena plate is reproduced with the existing parallax offset. The torso,
  arms, legs, ticks and direction of motion remain from the preserved frames.
- Basketball player: selected, explicitly indicated gaps inside the material and skin
  in five source frames; the dribbling patches inherit the fixes.
  No filter was applied to the whole character. The backboard and glass patches,
  contours, poses, ball trajectories and the PMG renderer were preserved.

## Memory and artifacts

The main code still occupies 2542 B from `$1400`, before the pool below `$1E00`.
Pool: 297 rows and 11 486 B (v352: 298 and 11 527 B). The
addresses of some shared rows change. All
64 banks are still allocated; bank content changes concern loader index 15
(basketball player graphics from `$4B80`) and 33–37 (walk frames).
The 6502 code logic, bank ownership, PMG ranges and NMI were not changed.
The generator and memory tests checked data overlap.

- XEX: `build/visual-prototype-v353.xex`, JSON next to it.
- SHA-256: `d002ff99361640ac1bfe38c903e91e2e1a6945b0655fa8111024a061bd87dfb4`.
- Comparison: `build/polish-audit/v353-review.png`; extended frames:
  `build/polish-audit/before-after.png`. The images were reproduced from bitmaps
  after the 6502 callbacks for both XEX. Approximate colours, without PMG overlays
  and raster simulation; they are not screenshots from a physical Atari.

## Validation performed

`make all PYTHON=/tmp/lessiknow-polish-venv/bin/python` and a separate build of the
numbered prototype passed; dev and v353 have an identical SHA-256.

34 focused tests passed: `test_girl_back_art`,
`test_school_parallax`, `test_basketball_hero`,
`test_basketball_v175_restore`, `test_memory_allocations`,
`test_display_lists`, `test_post_trevor_director`.

Full `make check`: 200 tests, 32 failures and 1 error. Separately the
unchanged `tools/` and `tests/` from HEAD were exported to `/tmp` and run with the
v352 XEX/JSON: 198 tests, the same 32 failures and 1 error. The list of all 33 entries,
including the raster subcases, is identical. They cover bananas/cache,
loader, Trevor palette, finale and tunnel ball/raster. The result does not mean
that the defects are insignificant; they were neither removed nor were their assertions
loosened.
Report: `build/polish-audit/validation-v353.json`.

Atari800: PAL, emulated 1088 XE, two POKEYs, Altirra OS, turbo,
no window or sound, stereo logging every 78 lines. Command:

```sh
/tmp/lessiknow-polish-venv/bin/python tools/check_playback.py --seconds 15 --demo build/visual-prototype-v353.xex --reference build/visual-prototype-v352.xex --minimum-seconds 270
```

Result: **10 721 808 identical stereo bytes**, about 2986.6 s
emulated, which covers the full run and the period after the montage ends.
The new `--reference` and `--minimum-seconds` options allow checking regression
against a saved demo; the default reference is still player v035.
Separate comparisons of v353 and v352 with v035 gave the same first difference
at byte 935 784 (about 260.7 s, at the end of the montage).
The cause of this difference was not established here and we do not declare full consistency
with v035.

No full visual playback, listening session or physical attempt was performed.
py65 does not model ANTIC DMA and physical raster deadlines. The existing
feed backboard artifact from the v347 audit remains for a separate fix.
The last hardware-confirmed release is still release 058 / v330;
production release files were not changed.
