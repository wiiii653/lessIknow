# Project Status

Reviewed 2026-11-28 against the development source and build artifacts.

## Final polish

- Prerelease 187 is byte-identical to the RUNAD package the user reported
  working on Atari 1088 Rambo with AVGCart. A detailed physical timing and
  cadence report should record the machine, video standard and stereo
  setup with the exact XEX hash.
- Graphics fixes and polish remain pending. The poses and keyframes are
  approved. The remaining scope is the appearance and visual quality of the
  existing artwork.

## Current development build

The current runtime is packaged in numbered prerelease 187. It includes the
revised opening, main-act and credits transcripts, PAL-frame profile ribbons, a
tapered title reflection, the ending card on bitmap resolutions and scanline
repetition, the shoe landing on every second kick during the credits, and
the Atari Arena captions.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| [Prerelease 187](../releases/less-i-know-demo-prerelease-187-stereo.xex) | 1,031,138 | `89af0d1babcc4d5f820f2cdf5a999c67be152f31c1ff9d4bf1868fa0c5bb39d3` |
| `build/hardware-dev.xex` | 1,031,120 | `6da09689335d59c841c1856cec53cac523f227b1efdc107783ac8a231115a5be` |
| `build/visual-prototype-dev.xex` | 1,107,949 | `7f5d26d4c7993750c4c0a307b297fe9f77f852fffd3292659a9d16d8c92f6e5c` |

The main-act terminal uses a one-color ANTIC C bitmap. Four rows keep the
same placement and timing. Two pages of four row slots use 1,120 bytes of
unbanked bitmap storage. The writer only redraws affected character pairs,
and scrolling rotates the row pointers. All 42 captions completed within
their cue windows in Atari800. The stereo POKEY stream matched the
preceding build over the full track.

Atari800 7.2.1 on PAL 1088XE recorded 174 tunnel bitmap updates and 355
ball updates over the first 744-frame tunnel sequence, up from 158 and
315. In the dunk cutaway, the bitmap increased from 38 to 43 updates over
187 frames, and the ball increased from 78 to 90. The longest ball hold
there dropped from seven to four frames. Party build 058 recorded 121 ball
updates in the same cutaway.

The banana bitmap copy processes all 15 aligned pages in one indexed loop.
The routine uses 138 bytes at `$7F40–$7FC9` in each of the 16 banana banks.
The late BUM/BAM overlay uses the existing shared copy to retain its raster
timing. All 64 banana bitmaps and the profile ribbon midpoint data were
verified byte for byte. The copy saves 2,384 cycles when the overlay is
inactive. The highest warm callback cost across all 64 views fell from
49,020 to 47,518 cycles.

Before the bitmap terminal change, the faster copy increased bitmap
updates from 86 to 91 in the first banana pass and from 73 to 80 in the
second. With the bitmap terminal, those passes recorded 108 and 93
updates across the same 440 and 374 PAL frames. The two later banana
passes increased from 34 to 39 and from 54 to 62 updates. Their longest
holds were six and seven PAL frames.

The full py65 suite rerun for prerelease 187 passed 211 of 232 checks.
The banana cycle-budget check passed, and the other 21 checks failed
in the prior run on the one-color terminal build as well.

Removing the unreachable montage dispatch and its tick check freed 125
bytes in main code, bringing its free space to 135 bytes. In 465 py65
samples from tunnels and the montage, the display lists, bitmap and
PMG bytes, GTIA registers, and PORTB matched the previous build. The
loader star test finds its data by load address and verifies all 32 phases
and the wrap.

The previous build
`64990331f51b176f93c2ee267e98f531d8b05c830dc1e747ac11e438c5c99e59`
passed seven focused terminal checks. An Atari800 PAL
1088XE trace recorded all 42 main-act captions fully typed before the end
of their action windows. Stereo POKEY output matched the preceding build
over the full track.

The preceding development build
`db47674722040d579d6ea57b6ceb1e05b388f3371cd5eaabda0d16ea2fc0c598`
verified 36 unique scrolling credits and greetings. The event credit
occupies 31 of 40 columns including the prompt.

On the profile-ribbon build
`4d41ffec79cb189834b2f0f598c3ac7558ab30af644a2991b207a1a12f97b471`,
Atari800 7.2.1 on PAL 1088XE with stereo POKEY recorded 741 consecutive
profile frames from the dancer's first bitmap through the end of the shot.
The ribbons and sparks advanced one phase per frame. The bitmap, ribbon
masks, sparks and horizontal positions matched the reference for every
frame. The profile bitmap changed 181 times after tick 9,008, compared
with 184 changes before the ribbon work. The stereo POKEY recording
matched the previous build byte for byte over the full track.
The py65 suite passed 209 of 232 checks. All 23 failures also occurred on
the previous development build, which skipped the two new profile-ribbon
checks.

The previous development build
`63a18c4615084ef9af9f5ecb46b7381829dbc0bbbac0b139188ba2afe9c4416a`
passed 17 targeted checks covering the title, scanline budget and main-act
terminal. Atari800 showed the shorter, darker lower water bands and the
clearance below them. Its stereo POKEY recording matched the build
`5818ac9a029dcca6c01da6a429712cffd1fc09d7e0681bf5736b5b923b3901b7`
over the full track. That build passed six targeted outro checks. Live
display-list checks confirmed the doubled and tripled rows, and all six
ending cards were verified through a carousel wrap. The earlier development build
`2f3913eb9ff7f95d92c864d7158973ae4855988475093023a37bef31d25a0105`
passed seven targeted checks. Atari800 confirmed its first two shoe landings
and produced stereo POKEY output identical to prerelease 186. An earlier
full-suite run on build
`caf644bade27a064f79f09bdfb835535b1a4d8471711f3ff856670697b2f7710`
reported 207 passes and the same 23 failures as prerelease 186.

### PMG cadence in the current build

Atari800 sampled active sprite masks and horizontal positions once per PAL
frame. A change can come from a moving player or missile. Counts use pairs
of consecutive frames with PMG DMA and GTIA graphics enabled.

| Effect | Sampled player ticks | Frames with changed sprite data |
|---|---:|---:|
| Title fireworks | 768–2,919 | 86 of 537 |
| Atari Arena whistle notes | 4,864–5,609 | 145 of 184 |
| Practice ball and accents | 5,992–8,971 | 642 of 738 |
| Profile ribbons and sparks | 9,004–11,966 | 740 of 740 |
| First spiral and organic tunnels | 11,992–14,943 | 353 of 737 |
| Trio, front solo and trio reprise | 15,000–20,399 | 616 of 1,349 |
| Lift and launch fireworks | 20,400–20,941 | 112 of 135 |
| Tunnel cutaway | 20,972–21,671 | 84 of 174 |
| Basketball hero ball and accents | 21,720–23,889 | 464 of 542 |
| Trevor impacts and ball | 26,936–29,643 | 225 of 669 |
| Banana bunch | 29,932–30,275 | 46 of 85 |
| Peeled banana | 30,304–30,651 | 50 of 86 |
| Montage spiral | 31,440–31,735 | 34 of 73 |
| Montage organic | 31,792–32,135 | 42 of 85 |
| Eye-shot ball | 39,384–40,128 | 139 of 186 |
| Credits orbit | 41,904–51,199 | 2,271 of 2,323 |
| Finale orbit | 51,420–51,779 | 88 of 89 |

The title, Trevor impacts and scene transitions include held graphics. The
tunnel overlays commonly held three or four frames between changes.
Front ribbons commonly held two to five frames. Credits and finale orbits
changed almost every frame during the sampled passages.

## Earlier regression baseline

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
  rows and 2,541 bytes of main code. The Atari Arena panorama uses 18 frames
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
| [Prerelease 183](../releases/less-i-know-demo-prerelease-183-stereo.xex) | Includes the animated opening, title water, ten caption pages and the training bitmap fix. |
| [Prerelease 184](../releases/less-i-know-demo-prerelease-184-stereo.xex) | Audited build with the synced main-act terminal. The user reported clean physical playback. Machine and loader details for this run were not recorded. |
| [Prerelease 185](../releases/less-i-know-demo-prerelease-185-stereo.xex) | Adds the credits foot tap on alternate kicks. |
| [Prerelease 186](../releases/less-i-know-demo-prerelease-186-stereo.xex) | Hardware test candidate with a bounded montage swap, shared montage tables and lighter terminal redraws. Retains the credits foot tap. |
| [Prerelease 187](../releases/less-i-know-demo-prerelease-187-stereo.xex) | Current runtime with the one-color main-act terminal and the AVG-tested RUNAD handoff. |
| [Release 058 / v330](../releases/less-i-know-demo-release-058-stereo.xex) | Documented full run from AVG on Atari 1088 Rambo and immutable loader reference |

The user also reported successful machine playback during later prerelease work.
The available record does not pin that report to an exact XEX hash and machine
configuration. Releases 059 and 060 failed on hardware.

### Prerelease validation history

Prerelease 187 includes the current opening, title reflection, caption timing,
profile ribbons, banana playback and ending changes. Its main-act terminal uses
1,120 bytes in RAM under ROM for the double-buffered text rows. The build JSON
reports 64 allocated banks, 295 shared scanline rows and 2,425 bytes of main
code. The numbered package preserves all 66 INIT wrappers, 64 staging clears,
the deferred low RAM at `$4000–$47FF` and the `$4800` bootstrap. The final
RUNAD stub uses `$3FB0–$3FC3`. py65 verified the handoff and all five
low-RAM restore spans. Atari800 7.2.1 on PAL 1088XE recorded identical
stereo POKEY output to the standard development XEX over the full track.
See the [loader contract](HARDWARE_LOADER_CONTRACT.md) for the exact package
difference and the AVG results.

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
the identified 182 and 183 packages remains unverified.

Prerelease 183 SHA-256:
`91a27f7901b94ea678bb7e2fee9c5a037478a516dc34fefa527887a0b906619b`.

Prerelease 184 SHA-256:
`35eaab64e2b306e55b9ff1da51ce13abcbb96e6e798fbb2fbbfb8dd4bc03baa9`.
Prerelease 185 SHA-256:
`369c187aa71b2b0f0e07165fc9ee6de6185616bef4c7b54ccff4020325abc689`.

Prerelease 186 is 1,020,514 bytes. SHA-256:
`9e0fc6c67a771ba80dd1d3d021c4c8cb948995684c650f7b1949e55431104c21`.
It frees 12,456 bytes across montage bank tails and uses 381 bytes of
unbanked RAM at `$DFC0–$E13C` for the shared tables. The terminal writer
and screen cache remain in their existing RAM-under-ROM window at `$DC00`.
Atari800 stereo POKEY output matched prerelease 185 byte for byte. The
physical playback result is pending.

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
