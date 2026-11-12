# Repository Guidelines

## Project structure

Atari XE 1 MB stereo demo for “The Less I Know The Better”. `tools/` builds
6502 code and assets, `tests/` contains py65 checks, `assets/` holds source art,
and `releases/` preserves numbered stereo XEX files. The current release is
v330 / `releases/less-i-know-demo-release-058-stereo.xex`; current status is in
`docs/PLAN_STATUS.md`, current post-Trevor timeline in
`docs/AKTUALNY_MONTAZ_V330.md`. Vxxx notes are historical change records.

## Current constraints

- Build stereo only. Mono releases are retired.
- All 64 banks are allocated. Never assume historical recovered-space figures
  are still free; inspect the active allocator, overlap assertions and build JSON.
- Main code fills `$1400–$1DFF`; do not overlap the shared scanline pool at
  `$1E00`. Current v330 uses 298 shared rows. Check the generated JSON before
  changing code or row ownership.
- Preserve PORTB across NMI and banked callbacks. Verify bank ownership before
  changing memory use. Music remains on the original v035 player; preserve four
  evenly spaced music updates per PAL frame.
- Prepare inactive bitmap/PMG buffers and publish in an early bounded blanking
  window. A late `VCOUNT >= 124` check alone is not safe for long PMG writes.
- PMG spans are `$0980–$0BFF` and `$8980–$8BFF`; clear only those spans.
- Keep dance PMG double buffering, Trevor impact protections, and the tunnel
  renderer's own opaque hole coverage. See V135–V163 notes before altering them.
- Scene changes must follow player ticks. Current post-Trevor timing is in the
  montage document. Do not infer current story or memory layout from old V144,
  V244, or V256 audits.

## Build and verification

Install `requirements-dev.txt` in a virtual environment. `make all
PYTHON=/path/to/venv/bin/python` builds the replaceable dev pair;
`make check PYTHON=/path/to/venv/bin/python` runs all discovered tests.
`tools/check_playback.py` compares stereo POKEY output in Atari800. Current
v330 has 28 focused py65 checks recorded; full `make check` and physical Atari
playback have not been repeated for this release. State precisely what was run.

For hardware work, record PAL/NTSC, Atari model, memory expansion and stereo
configuration. py65 does not model ANTIC DMA or physical raster deadlines.

## Editing and release practice

Use `$` for hexadecimal addresses and retain Polish terminology in technical
specifications. Preserve numbered releases; create a new release filename for
each production build. Never overwrite a numbered release. Keep visual
prototypes separate from distribution XEX files and report SHA-256 for the
current release.

Commits should use concise imperative subjects. Release notes should identify
changed acts/memory regions and actual validation. Do not claim compo readiness,
real FPS, physical playback or audio/video verification without direct evidence.
