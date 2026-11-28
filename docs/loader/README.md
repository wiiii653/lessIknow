# Loader Documentation

Read the current [hardware loader contract](../HARDWARE_LOADER_CONTRACT.md)
before using any historical commands in this folder. `make hardware` builds
the replaceable AVG package `build/hardware-dev.xex`. The [project README](../../README.md)
describes the stereo build. The current package uses the full-rate star,
the updated loader credit and a bounded blanking wait for wrapper refreshes.
See the [loader text](../terminal_opening.md) and
[current development build](../PLAN_STATUS.md#current-development-build).

This folder documents the 64-bank XEX pipeline, loading screen, AVG startup,
runtime bank switching and diagnostic work. Detailed addresses and byte counts
in individual notes are snapshots from older releases. Verify them against
`tools/build_hardware_xex.py`, the current builders and the generated JSON
before making changes.

## Topics

| File | Topic |
|---|---|
| `01_build_pipeline.md` | Build pipeline |
| `02_xex_and_startup.md` | XEX format, INIT/RUNAD and startup |
| `03_loading_screen.md` | Loading screen and display list |
| `04_bank_switching.md` | PORTB, bank detection and copying |
| `05_compact_and_late_start.md` | Compact packaging and late startup |
| `06_memory_and_bank_map.md` | Memory map and bank allocation |
| `07_runtime_switching.md` | Runtime bank switching |
| `08_diagnostics.md` | Diagnostics and evidence |
| `09_playback_and_tests.md` | Reproduction and tests |
| `10_optimisation_analysis.md` | Optimization analysis |
| `11_mosaics_school_and_bananas.md` | Scene profiles and banked artwork |

## Fixed hardware layout

The current hardware packaging contract reserves the loading screen at
`$3800–$38FF`, INIT wrapper at `$3900`, bank clear routine at `$3A00`, deferred
low-memory buffer at `$4000–$47FF`, and final bootstrap at `$4800`. Bank data is
loaded through `$8000–$BFFF`. The exact code lengths can change only with a
loader-contract audit.

The reference is stereo release 058 / v330. See [Project Status](../PLAN_STATUS.md) for later hardware reports. py65 and Atari800 evidence must not be
described as AVG hardware confirmation.
