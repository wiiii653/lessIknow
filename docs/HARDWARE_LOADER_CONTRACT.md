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

The user reported flawless operation of `build/hardware-runad-compat-test.xex`
on their AVG/Rambo setup. [Numbered prerelease 187](../releases/less-i-know-demo-prerelease-187-stereo.xex)
is byte-identical to that file. It is 1,031,138 bytes, with SHA-256
`89af0d1babcc4d5f820f2cdf5a999c67be152f31c1ff9d4bf1868fa0c5bb39d3`.
It uses an unbanked `RUNAD` stub at `$3FB0` to select base RAM and invoke
the existing `$4800` bootstrap. The firmware version and exact
launch-to-opening time were unrecorded.

## Prerelease 187 packaging

The packager's `--runad-handoff` option reproduces the handoff used in
prerelease 187. It replaces the last two XEX records, `INITAD=$4800` and
`RUNAD=$13E0`, with a stub at `$3FB0–$3FC3` and `RUNAD=$3FB0`. The stub
disables IRQ, NMI and display DMA, selects base RAM with `PORTB=$FF` and
jumps to `$4800`. Its payload is
`78 A9 00 8D 0E D4 8D 00 D4 8D 2F 02 A9 FF 8D 01 D3 4C 00 48`.
All preceding XEX records match the INIT package. The current `make hardware`
output compares byte for byte with the archived prerelease 187. The two
loading-speed experiments below are closed and their changes are absent
from prerelease 187.

## Selective clear test

`build/hardware-fast-load-test.xex` is a separate 1,032,272-byte test file,
with SHA-256
`ffc03e7b1f70fd25d15f73b53e2c3370a342107f6ddaccdbde0c92b2a97ece68`.
Its only changes from the hardware-tested RUNAD file are the 64 routines at
`$3A00`. Each routine clears the pages with gaps in the following XEX
segments. All 64 staging images reconstructed byte for byte from poisoned
RAM in py65. The final runtime overwrites the loader scratch area.

On Atari800 7.2.1, PAL 1088XE with Altirra OS, the time from the loading
screen to the silent opening fell from 1,169 to 809 PAL frames, about 23.45
to 16.23 seconds. The silent opening lasted 930 frames in both runs, and
full-track stereo POKEY output matched. On physical AVGCart, the user
reported the same loading time for the selective clear and RUNAD control.
Exact stopwatch times were unrecorded.

## Compressed transfer test

`build/hardware-compact-transfer-test.xex` is a 703,798-byte diagnostic
package derived from the 1,031,138-byte RUNAD control, a 31.7% reduction.
Its SHA-256 is
`f1346b7f3dd38e1028ba598f41ceb526039bb7b24fcb82eff46a4f5119f6193e`.
It uses the existing LZ decoder to unpack 49 video banks directly into
their original extended RAM destinations. Those banks use a compressed
payload and decode in place of the normal staging clear and copy.
The 14 music banks, remaining video bank, INIT wrappers and bootstrap
are unchanged. The decoder uses loader scratch RAM. All 49 outputs
matched the control images byte for byte in py65.

On Atari800 7.2.1 with the same PAL 1088XE and Altirra OS settings, the
loading screen to silent opening took 1,194 PAL frames, versus 1,169 for
the RUNAD control. All 64 extended RAM banks matched byte for byte at
the start of the silent opening. The opening lasted 930 PAL frames,
and the full-track stereo POKEY traces matched. The package changes XEX
segment count and CPU work as well as file size. On physical AVGCart,
the user reported approximately the same load time as the RUNAD control,
possibly about two seconds longer. Exact times and firmware version were
unrecorded. This test showed no speedup on that setup. The default
hardware build still uses the required packaging below.

In the Atari800 RUNAD control, frame-boundary CPU samples landed mainly
in the staging clear and bank copy loops. The raster synchronization
wait appeared in 19 of 1,169 samples. This profile covers emulated
execution and gives no measurement of AVGCart transfer time.

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
  bootstrap in the legacy INIT package. For the RUNAD package, the
  stub explicitly selects the same base RAM that holds the deferred data.
  In either package, the `$4800` bootstrap disables IRQ/NMI, restores low
  RAM and jumps directly to `$13E0`.
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
python3 tools/build_hardware_xex.py build/visual-prototype-dev.xex /path/to/new-stereo-candidate.xex --approved-music --release-122-music --full-rate-loading --runad-handoff
```

The development target enables the full-rate animated loader and the RUNAD
handoff. The command-line packager retains the INIT handoff when invoked
without `--runad-handoff`. Wrapper refreshes use the bounded
`124 <= VCOUNT < 128` blanking window inherited
from prerelease 181. The final wrapper restores the OS VBI and disables
both the DMA shadow and ANTIC DMA before late segments overwrite the loader
display. See [Project Status](PLAN_STATUS.md#current-development-build)
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
