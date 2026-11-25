# The Less I Know The Better — Atari XE Demo

A stereo Atari XL/XE demo for a 1 MB memory expansion. It uses the original
v035 POKEY player and an original tracker arrangement based on Tame Impala's
composition.

The project is nearly finished. The remaining work is focused on graphics
improvements only. The accepted final prerelease is
[`releases/less-i-know-demo-prerelease-165-stereo.xex`](releases/less-i-know-demo-prerelease-165-stereo.xex).

## Current release and working tree

The latest approved stereo release is **release 133 / v390**:
[`releases/less-i-know-demo-release-133-stereo.xex`](releases/less-i-know-demo-release-133-stereo.xex).
For the current working tree, prerelease history and hardware evidence, see
[Project Status](docs/PLAN_STATUS.md). Use the release above for the approved
build. The development build includes the restored basketball hero frames.

The source currently builds stereo only. All 64 expansion banks are allocated.
The music clock advances four evenly spaced updates per PAL frame. Scene
changes follow those player ticks.

## Build and checks

Install `requirements-dev.txt` in a virtual environment, then run:

```sh
make all PYTHON=/path/to/venv/bin/python
make check PYTHON=/path/to/venv/bin/python
```

This produces the replaceable raw prototype, its build JSON and
`build/hardware-dev.xex`. The hardware target uses release 122 music with
the opening kick muted and enables the animated loader. For numbered candidates,
use the [hardware packaging procedure](docs/HARDWARE_LOADER_CONTRACT.md).

## Project map

- `tools/` — 6502 code generators, asset preparation and XEX packaging.
- `tests/` — py65 checks for generated code and timing/data invariants.
- `assets/` — source art, music and preserved reference assets.
- `releases/` — numbered XEX releases and historical artifacts.
- `docs/` — current technical references and the version history.

Start with [`docs/README.md`](docs/README.md) for the documentation guide.
