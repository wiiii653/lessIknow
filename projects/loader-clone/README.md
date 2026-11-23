# Loader clone — standalone loading-screen harness

A small, separate project that reproduces **only the TLIKTB loading screen**:
the title and credits, the animated finale star, the progress dots, and the
per-bank clear/copy cycle. It contains no demo scenes, no music player and no
bank selectors, so it builds in seconds and can be flashed/tested without
touching the main demo.

Use it to iterate on loading-screen flicker and timing. It is not a demo
candidate and it does not replace a full hardware run.

## What it reproduces

| Part | Source |
|---|---|
| Text screen `$3800`, display list `$3880`, INIT `$38A0` | release 058 reference |
| Animated star VBI `$1100` + delta stream `$1400` | `tools/animated_loading.py` |
| Progress-dot text rewrites in the `$3900` wrapper | release 058 reference |
| `$3A00` 16 KiB staging clear (~4.6 PAL frames) | release 058 reference |
| `$1000` 16 KiB copy with NMI off (~6.4 PAL frames) | rebuilt, same timing |

The main loop calls the real `$3900` wrapper once per bank, so the display
refresh, both text rewrites and the copy happen in the same order as the demo.
At the end it writes `DONE` over the loading line and holds.

## What it does **not** reproduce

- No bank selectors and no `PORTB` switching: the copy goes to main RAM at
  `$4000-$7FFF`, not to an extended-RAM bank.
- No 1 MiB of bank data, so **load time is not reproduced**. Only the visual
  and per-bank CPU timing are.
- No music, no scenes, no low-RAM runtime, no bootstrap.

Those are deliberate. Test the loader's visible behaviour here, then port a
proven change to `tools/build_hardware_xex.py` and validate it on hardware.

## Current status (Atari800 + hardware, 2026-11-23)

| Variant | Result |
|---|---|
| `copy` (copy + clear) | animates, runs all 64 banks to `DONE` |
| `direct` (no copy, no clear) | animates, runs all 64 banks to `DONE` |
| `direct --no-vbi` | static by design: no star VBI |
| `direct --clear --no-init` | **animates, no blink** — identifies the per-bank `$38A0` refresh as the flicker source |

The loading VBI vector is installed by `$38A0`, but `NMIEN` is not enabled
there. In the demo the first `$1000`/`$20EA` copy sets `NMIEN=$40`, which is
why the animation starts. A no-op `$1000` therefore left `direct` static;
it now sets `NMIEN=$40` itself.

The `copy` variant pauses the animation for the 16 KiB copy (the stutter
under test); `direct` keeps it running.

## Build

Requires the parent repository (it imports `tools/` and reads the immutable
release 058 reference for the wrapper, clear and INIT bytes).

```sh
# current loader behaviour (clear + copy, NMI-off freeze)
python3 projects/loader-clone/build.py --output build/loader-clone-copy.xex

# simulate a direct-to-bank load: no copy, no NMI-off freeze
python3 projects/loader-clone/build.py --mode direct --output build/loader-clone-direct.xex

# short run for emulator checks
python3 projects/loader-clone/build.py --banks 8 --output build/loader-clone-8.xex
```

Each build also writes a `.json` sidecar with `callback`, `banks`, `mode`,
`size` and `sha256`.

## Run

PAL, Atari800 `1088XE` configuration, or Altirra 65XE/PAL with 1 MB:

```sh
atari800 -1088xe -pal -nobasic -run build/loader-clone-copy.xex
```

## What to look for

- The star animation runs from the first bank to the last.
- The dot count in the loading line advances once per bank.
- In `copy` mode the animation freezes for about 6 frames per bank; in
  `direct` mode it does not. That difference is the stutter under test.
- No colour flash, charset garbage or torn text at bank boundaries.

Altirra watchpoints: writes to `$D400`, `$D402/3`, `$D409`, `$D016-$D01A`.
Note that the `$38A0` refresh writes the *same* values every time; only a
changed value can produce a visible flash.

## Limits

py65 and Atari800 do not model ANTIC DMA or raster deadlines. A full run on
AVG + 1088 Rambo is the only acceptance for "works". Record the file name,
SHA-256, size and result.
