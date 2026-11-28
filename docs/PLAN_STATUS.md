# Project Status

Reviewed 2026-11-28 against the development source and build artifacts.

## Current development baseline

Use source commit `a0278f2` and its build products for regression comparisons.
This baseline is ahead of numbered prerelease 183. Preserve its look and
timing when making unrelated changes.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `build/hardware-dev.xex` | 1,030,507 | `83ae3f77df0b00429b697c94947ec705f1687cc4db21130ea9ebb84e30075e08` |
| `build/visual-prototype-dev.xex` | 1,108,365 | `b7a9a5ed9bdaa1b76546e4b5092505badf4ee687c1cd56276604cb277b6417d6` |

The hardware package is 18,069 bytes below 1 MiB and contains 66 INIT
wrappers and 64 bank staging clears. The raw prototype and its companion
JSON describe the runtime, allocation and timing.

- **Loader and opening.** The loader uses the full-rate animated star,
  the **INSPIRED BY TAME IMPALA'S MUSIC VIDEO** credit and cycling dots.
  The silent cold-start terminal types two pages before the music.
  The scored title uses procedural plasma, one city panorama, rippling
  water and staggered PMG fireworks. Preserve the loader's raster sync,
  DMA shutdown, title dissolve and SELECT restart.
- **Main acts.** Ten fixed three-ink caption palettes keep their original
  hues with three fewer luminance steps. The cold-start opening and the
  credits sequence, including greetings, keep their own palettes.
  Practice uses the forward eight-phase ball stripe loop with its finger
  mask. The basketball hero uses the earlier cleaned artwork. The redrawn
  poses are preserved in [implemented-poses](../art-review/hero-basketball/implemented-poses/).
- **Music.** The hardware target uses release 122 music with the opening
  kick muted. Preserve the v035 player and its four evenly spaced
  updates per PAL frame. Release 133 audio is a separate packager option.
- **Memory.** The build JSON reports 64 allocated banks, 295 unique shared
  rows and 2,541 bytes of main code. The school panorama uses 18 frames
  in slots 33–37 and shares its renderer from slot 33. The run stub
  clears the second framebuffer at startup. The `bank_manifest` records
  logical slots, selector addresses and verified empty ranges with
  exclusive ends. Rebuild the JSON before budgeting memory for changes.

Use the [concise timeline](TIMELINE_MAP.md), [montage cut list](CURRENT_MONTAGE_V330.md)
and [screen text index](README.md#current-screen-text) when comparing scene
behavior. Keep numbered XEX files immutable. Use the baseline hashes to
identify the build under comparison and record new checks against the
exact artifact exercised.

## Releases and hardware evidence

| Artifact | Status |
|---|---|
| [Release 133 / v390](../releases/less-i-know-demo-release-133-stereo.xex) | Latest approved numbered release |
| [Prerelease 165](../releases/less-i-know-demo-prerelease-165-stereo.xex) | Earlier user-accepted prerelease |
| [Prerelease 180](../releases/less-i-know-demo-prerelease-180-stereo.xex) | Includes the experimental hero art and the forward stripe loop. |
| [Prerelease 181](../releases/less-i-know-demo-prerelease-181-stereo.xex) | Restores the earlier hero frames and retains the forward stripe loop. |
| [Prerelease 182](../releases/less-i-know-demo-prerelease-182-stereo.xex) | Earlier comparison build for the opening and caption work. Includes the PMBASE, title dissolve and loader handoff changes. |
| [Prerelease 183](../releases/less-i-know-demo-prerelease-183-stereo.xex) | Latest numbered prerelease. Includes the animated opening, title water, ten caption pages and the training bitmap fix. |
| [Release 058 / v330](../releases/less-i-know-demo-release-058-stereo.xex) | Documented full run from AVG on Atari 1088 Rambo and immutable loader reference |

The user also reported successful machine playback during later prerelease work.
The available record does not pin that report to an exact XEX hash and machine
configuration. Releases 059 and 060 failed on hardware.

### Prerelease validation history

Prerelease 181 is 1,044,667 bytes. SHA-256:
`2cc75d3444b7754fff7a8277db4314a07e545d14b238c510ef08146320fdc984`.
It restored the hero artwork in its existing bank layout at `$4B80` and
preserved prerelease 180's manually packaged loader raster sync helper.
The build record describes package checks. Playback of this exact build
was not recorded.

Prerelease 182 added the PMBASE shadow at `$0DFD`, the corrected title
dissolve handoff and full-rate loader raster sync in the regular build
recipe. Its final wrapper shuts DMA off before the loader display assets
are overwritten. The 1,044,790-byte package retains 66 INIT wrappers and
64 staging clears. The build and targeted py65 checks passed.

Prerelease 182 SHA-256:
`7e601c30c5558e9354827c83e48d7083b30c1328d373dcd10e71860d8957b369`.

Prerelease 183 is 1,044,796 bytes and matched the hardware development XEX
from commit `47d767e` when it was packaged. It uses the full-rate animated AVG loader. The opening
temporarily uses `$9000–$9BFF`. The act strip and restored training lookup
tables use RAM under ROM. The targeted py65 checks passed, including pixel
comparisons for all three training shots with captions active. The full
Atari800 stereo POKEY recording matched prerelease 182. During the caption
work, the Atari800 PAL 1088XE monitor recorded 185 first-dancer bitmap
publications and a maximum five-frame pose hold, matching prerelease 182.
It recorded 364 front-solo PMG publications versus 363 in prerelease 182.
Those results apply to the monitored prerelease work. Physical playback of
the identified 182, 183 and current development builds remains unverified.

Prerelease 183 SHA-256:
`91a27f7901b94ea678bb7e2fee9c5a037478a516dc34fefa527887a0b906619b`.

## Memory and loader constraints

- Treat release 058 as the immutable hardware loader reference.
- Use `make hardware` or `tools/build_hardware_xex.py` for hardware packaging;
  a raw `visual-prototype-*.xex` does not include the confirmed AVG protocol.
- Preserve the high-RAM loading screen, 66 INIT wrappers, 64 staging clears and
  compact bank payloads, deferred low-memory restore and final `$4800`
  bootstrap. INIT counts alone do not establish compatibility.
- Preserve PORTB around NMI and banked callbacks. Confirm ownership with the
  current allocator and generated build JSON before changing memory use.
- Prepare inactive bitmap and PMG buffers, then publish in an early bounded
  blanking window. A late `VCOUNT >= 124` check alone is unsafe for long PMG
  writes.
- PMG spans are `$0980–$0BFF` and `$8980–$8BFF`; clear only those spans.
- Preserve dance PMG double buffering, Trevor impact protections and the
  tunnel renderer's own opaque hole coverage.

## Build and evidence

```sh
make all PYTHON=/path/to/venv/bin/python
make check PYTHON=/path/to/venv/bin/python
```

Both development XEX files and the build JSON were reproduced byte for byte
from the baseline source. The full `make check` run on that baseline reported
**200 passes and 28 failures out of 228 tests**. The startup and framebuffer
clear, title water, main-act terminal and outro palette checks passed.
The failed checks by test module are recorded below for future comparisons.

| Test module | Failures |
|---|---:|
| `test_banana_cache` | 1 |
| `test_basketball_hero` | 3 |
| `test_basketball_v175_restore` | 2 |
| `test_final_pmg_publish` | 1 |
| `test_girl_eyes` | 1 |
| `test_hardware_loader` | 2 |
| `test_mosaic` | 1 |
| `test_outro_text` | 4 |
| `test_post_trevor_director` | 2 |
| `test_practice_pmg` | 1 |
| `test_ribbon_buffers` | 1 |
| `test_ribbon_inbetweens` | 1 |
| `test_sequence` | 1 |
| `test_story_finale` | 4 |
| `test_terminal_typing` | 3 |

`tools/check_playback.py` compares the stereo POKEY stream in Atari800.
py65 exercises 6502 code and does not model ANTIC DMA deadlines. A full
physical run is still needed for playback and raster evidence on this
development build. For hardware reports, record the XEX hash, PAL or NTSC,
Atari model, memory expansion, stereo configuration and loader setup.
