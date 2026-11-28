# The Less I Know The Better — Atari XE Demo

A stereo Atari XL/XE demo for a 1 MB memory expansion. It uses the original
v035 POKEY player and an original tracker arrangement inspired by Tame Impala's
composition.

## Current builds

- [Release 133 / v390](releases/less-i-know-demo-release-133-stereo.xex) is the latest approved numbered release.
- [Prerelease 186](releases/less-i-know-demo-prerelease-186-stereo.xex) is the latest numbered test build in this workspace. It includes the shared montage tables and lighter terminal redraws.
- `make all` builds the current development snapshot with shot-synced captions, PAL-frame profile ribbons, and the credits shoe landing on every second kick.

See [Project Status](docs/PLAN_STATUS.md) for the current regression baseline,
build hashes and playback evidence. See [Final polish](docs/PLAN_STATUS.md#final-polish)
for the remaining graphics work and hardware validation.

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
- `docs/` — current technical and release references.
- `docs/backup/` — historical version notes, audits, and drafts.

Start with [`docs/README.md`](docs/README.md) for the documentation guide.
