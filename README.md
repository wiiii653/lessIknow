# The Less I Know The Better — Atari XE Demo

A stereo Atari XL/XE demo for a 1 MB memory expansion. It uses the original
v035 POKEY player and an original tracker arrangement based on Tame Impala's
composition.

## Current builds

- [Release 133 / v390](releases/less-i-know-demo-release-133-stereo.xex) is the latest approved numbered release.
- [Prerelease 183](releases/less-i-know-demo-prerelease-183-stereo.xex) is the latest numbered development snapshot. It includes the opening terminal, title reflection and ten main-act captions.
- `make all` builds the current development snapshot. It also includes the consolidated school panorama banks, the updated **INSPIRED BY** loader credit and dimmer main-act captions. The opening terminal and the credits sequence keep their original palettes.

See [Project Status](docs/PLAN_STATUS.md) for the current regression baseline,
build hashes and playback evidence.

The source currently builds stereo only. All 64 expansion banks are allocated.
The music clock advances four evenly spaced updates per PAL frame. Scene
changes follow those player ticks.

## Build and checks

Install `requirements-dev.txt` in a virtual environment, then run:

```sh
make all PYTHON=/path/to/venv/bin/python
make check PYTHON=/path/to/venv/bin/python
```

`make all` produces the replaceable raw prototype `build/visual-prototype-dev.xex`,
its layout and timing JSON, and the AVG-packaged `build/hardware-dev.xex`.
The hardware target uses release 122 music with the opening kick muted and
enables the full-rate animated loader. `make check` runs the discovered test
suite against the raw prototype and also exercises the packager. For numbered candidates,
use the [hardware packaging procedure](docs/HARDWARE_LOADER_CONTRACT.md).

## Project map

- `tools/` — 6502 code generators, asset preparation and XEX packaging.
- `tests/` — py65 checks for generated code and timing/data invariants.
- `assets/` — source art, music and preserved reference assets.
- `releases/` — numbered XEX releases and historical artifacts.
- `docs/` — current technical references and the version history.

Start with [`docs/README.md`](docs/README.md) for the documentation guide.
