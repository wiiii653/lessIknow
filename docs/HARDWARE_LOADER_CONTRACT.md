# AVG / 1088 Rambo Hardware Loader Contract

Read this document before changing bank loading or packaging an XEX.

## Reference and confirmed evidence

The documented reference run on physical hardware was v330 / stereo
release 058, loaded from AVG on an Atari 1088 Rambo. The user did not specify
PAL/NTSC or the exact second-POKEY setup for that report. Do not add those as
confirmed facts.

Reference file: `releases/less-i-know-demo-release-058-stereo.xex`, 936,240 B.
SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`.
Never overwrite this file or any numbered release.

Releases 059 and 060 failed to start on the user's hardware. Release 061 has
the same 51 `$1000` procedures as 058 (50 video banks plus the RAM-under-ROM
copy), the same loading screen, 66 wrappers, clear code and bootstrap. Those
procedures alone therefore do not explain the failure. A later failure was
reported for prototype v353, which used a different loading path. The exact
hardware failure cause remains unresolved.

## Required packaging behavior

- Loading screen: text at `$3800`, ANTIC display list at `$3880`, INIT at
  `$38A0`.
- Preserve the original v035 bank detection and the 50 additional video-bank
  selectors. Do not change the map or order based only on emulator results.
- Run all 66 INITs through the `$3900` wrapper in release 058 order. The wrapper
  preserves registers and flags around loading-screen refreshes.
- Before loading each of the 64 bank images, clear `$8000–$BFFF` via INIT
  `$3A00`. Then load nonzero fragments. Reconstructed images must match the raw
  prototype byte for byte, including the RAM-under-ROM image.
- Do not load final runtime data for `$0400–$0BFF` into loader work areas during
  loading. Defer it to `$4000–$47FF` and restore it at the end.
- Preserve the release 058 restore ranges: `$0400–$07DF`, `$0800–$08BF`,
  `$0900–$0976`, `$0980–$09FF`, `$0A00–$0BFF`. Audit any increase; do not
  silently change the bootstrap.
- Keep PORTB unchanged between loading the `$4000` buffer and executing the
  bootstrap. The `$4800` bootstrap disables IRQ/NMI, restores low RAM, then
  jumps to `$13E0`. It does not return to the loader or rely on RUNAD handling.
- Keep the packaged file below 1 MiB to remain within the known-compatible
  loading path. This size limit is a compatibility condition, not a proven
  explanation for previous failures.
- Do not move progress dots into low RAM in the hardware loader. Comparing
  addresses or INIT counts alone is insufficient.

## Build and verification

`make all PYTHON=/path/to/python` builds the raw prototype and
`build/hardware-dev.xex`. `make hardware PYTHON=/path/to/python` refreshes the
hardware target and its dependencies. To make a numbered candidate, choose a
new filename:

```sh
python3 tools/build_hardware_xex.py build/visual-prototype-dev.xex /path/to/new-stereo-candidate.xex --approved-music --release-122-music --full-rate-loading
```

The development target enables the full-rate animated loader. Wrapper
refreshes use the bounded `124 <= VCOUNT < 128` blanking window inherited
from prerelease 181. The final wrapper restores the OS VBI and disables
both the DMA shadow and ANTIC DMA before late segments overwrite the loader
display. See [Project Status](PLAN_STATUS.md#current-development-baseline)
for the development package hash and [loader text](terminal_opening.md)
for the current screen copy.

The packager refuses to overwrite numbered files, verifies the release 058
SHA-256, rejects unknown changes to bank procedures and compares the base
package against the reference before installing the optional animated
loading screen. Packaging preserves the runtime graphics, scene timing,
64-bank allocation and player code.

py65 checks can verify reconstructed images, wrapper behavior and the bootstrap
handoff, but they do not model ANTIC DMA or physical raster deadlines. Atari800
confirmation does not replace a full AVG / 1088 Rambo test.
