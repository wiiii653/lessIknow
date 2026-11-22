# The Less I Know The Better — Atari XE Demo

A stereo Atari XL/XE demo for a 1 MB memory expansion. It uses the original
v035 POKEY player and an original tracker arrangement based on Tame Impala's
composition.

## Current release and working tree

The latest approved stereo release is **release 133 / v390**:
[`releases/less-i-know-demo-release-133-stereo.xex`](releases/less-i-know-demo-release-133-stereo.xex).
The current source tree contains newer development edits and does not yet have
a numbered release. A development build is not hardware-confirmed.

Release 058 / v330 is the last full run confirmed on the user's Atari 1088
Rambo from AVG. The later hardware packaging path preserves that loader
contract; later candidates still require a real hardware run. See
[`docs/PLAN_STATUS.md`](docs/PLAN_STATUS.md) and
[`docs/HARDWARE_LOADER_CONTRACT.md`](docs/HARDWARE_LOADER_CONTRACT.md).

The source currently builds stereo only. All 64 expansion banks are allocated.
The music clock advances four evenly spaced updates per PAL frame. Scene
changes follow those player ticks.

## Build and checks

Install `requirements-dev.txt` in a virtual environment, then run:

```sh
make all PYTHON=/path/to/venv/bin/python
make check PYTHON=/path/to/venv/bin/python
```

This produces a replaceable development prototype and
`build/hardware-dev.xex`. The hardware package uses the approved release 133
music with the current earlier-percussion option. It does not create a numbered
release. To package a reviewed prototype as a new, uniquely named hardware
candidate, follow the release procedure in the hardware loader contract.

## Project map

- `tools/` — 6502 code generators, asset preparation and XEX packaging.
- `tests/` — py65 checks for generated code and timing/data invariants.
- `assets/` — source art, music and preserved reference assets.
- `releases/` — numbered XEX releases and historical artifacts.
- `docs/` — current technical references and the version history.

Start with [`docs/README.md`](docs/README.md) for the documentation guide.
