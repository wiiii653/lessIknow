# Repository Guidelines

## Project structure and current state

This repository builds a stereo Atari XL/XE demo for “The Less I Know The
Better”. `tools/` contains 6502 code and asset builders, `tests/` contains
py65 checks, `assets/` holds source art and music, and `releases/` preserves
numbered XEX files.

See `docs/PLAN_STATUS.md` for the latest approved release, numbered
prereleases and the current regression baseline. Release 058 / v330 is
the documented full run and loader reference for Atari 1088 Rambo using AVG.
See `docs/TIMELINE_MAP.md` and `docs/CURRENT_MONTAGE_V330.md` for current timing.

## Hardware loader contract

Read `docs/HARDWARE_LOADER_CONTRACT.md` before changing bank loading or XEX
packaging. Hardware-confirmed reference: stereo release 058 / v330, AVG,
Atari 1088 Rambo. Raw `visual-prototype-*.xex` files omit this loading
protocol. Use `make hardware` or `tools/build_hardware_xex.py` for a hardware
candidate. Preserve the high-RAM loading screen, 66 INIT wrappers, 64 staging
clears and compact bank payloads, deferred low RAM, and final `$4800`
bootstrap. INIT counts alone do not establish compatibility. Releases 059/060
failed on hardware. Record the exact XEX hash and machine setup for later
hardware reports. See `docs/PLAN_STATUS.md` for evidence.

## Memory and runtime constraints

- Build stereo only; mono releases are retired.
- All 64 banks are allocated. Check the current allocator, overlap assertions
  and generated build JSON before changing memory use.
- Main code occupies `$1400–$1DFF`. The shared scanline pool starts at `$1E00`.
  Read `unique_rows` in the generated build JSON for the active count.
- Preserve PORTB across music NMI and banked callbacks. Music remains on the
  original v035 player with four evenly spaced updates per PAL frame.
- Prepare inactive bitmap and PMG buffers, then publish in an early bounded
  blanking window. A late `VCOUNT >= 124` check alone is not safe for long PMG
  writes.
- PMG spans are `$0980–$0BFF` and `$8980–$8BFF`; clear only those spans.
- Preserve dance PMG double buffering, Trevor impact protections and the
  tunnel renderer's opaque hole coverage.
- Drive scene changes from player ticks. Do not infer current timing or memory
  ownership from historical Vxxx notes.

## Build and verification

Install `requirements-dev.txt` in a virtual environment:

```sh
make all PYTHON=/path/to/venv/bin/python
make check PYTHON=/path/to/venv/bin/python
```

`make all` builds the replaceable development prototype and hardware package.
`make check` runs the discovered test suite. `tools/check_playback.py` compares
stereo POKEY output in Atari800. py65 does not model ANTIC DMA or physical
raster deadlines. Record PAL/NTSC, Atari model, memory expansion and stereo
configuration for hardware checks.

Do not claim physical playback, full visual verification, real frame rate or
compo readiness without direct evidence.

## Documentation and releases

Write and maintain project documentation in English. Keep numbered releases
immutable; use a new filename for each production build. Keep visual prototypes
separate from distribution XEX files. Release notes should identify changed
acts and memory regions and state the validation actually performed.
