# Project Status

The project is nearly finished. Further development is focused on graphics
improvements only.

Reviewed 2026-11-25 against the working tree and existing build artifacts.

## Releases and hardware evidence

| Artifact | Status |
|---|---|
| [Release 133 / v390](../releases/less-i-know-demo-release-133-stereo.xex) | Latest approved numbered release |
| [Prerelease 165](../releases/less-i-know-demo-prerelease-165-stereo.xex) | User accepted this prerelease |
| [Prerelease 180](../releases/less-i-know-demo-prerelease-180-stereo.xex) | Includes the experimental hero art and the forward stripe loop. |
| [Prerelease 181](../releases/less-i-know-demo-prerelease-181-stereo.xex) | Restores the earlier hero frames and retains the forward stripe loop. |
| [Prerelease 182](../releases/less-i-know-demo-prerelease-182-stereo.xex) | Regression baseline. Includes the PMBASE, title dissolve and loader handoff changes. |
| [Prerelease 183](../releases/less-i-know-demo-prerelease-183-stereo.xex) | Candidate on `feature/terminal-opening` for a physical Atari run. Includes the animated opening, ten caption pages and the training bitmap fix. |
| [Release 058 / v330](../releases/less-i-know-demo-release-058-stereo.xex) | Documented full run from AVG on Atari 1088 Rambo and immutable loader reference |

The user also reported successful machine playback during later prerelease work.
The available record does not pin that report to an exact XEX hash and machine
configuration. Releases 059 and 060 failed on hardware.

Prerelease 181 is 1,044,667 bytes. SHA-256:
`2cc75d3444b7754fff7a8277db4314a07e545d14b238c510ef08146320fdc984`.

The build completed via `make all`. Act 3 uses the restored artwork in its
existing bank layout starting at `$4B80`. The build JSON reports 295 shared
rows and 2,541 main code bytes. The numbered package preserves prerelease
180's additional loader raster sync: prepend its `$3B80–$3B8D` helper and
route the 131 refresh calls in the 66 INIT wrappers through it. Packaging
checked that the helper survives through the last wrapper and that the file
fits below 1 MiB. This post-build step sits outside Make. Prerelease 181
has no playback validation in this build record.

## Current development tree

- **Opening:** procedural plasma, one city panorama, moving water under the
  quay, title text and staggered PMG fireworks. The city and reflection
  begin revealing at tick 1024.
- **Loader:** the hardware target enables the animated ending star, static
  rainbow text and animated dots after the centered LOADING word.
- **Music:** the hardware target uses release 122 data with the opening kick
  muted. Keep the v035 player and its four evenly spaced updates per PAL frame.
  Release 133 audio remains available as a distinct packager option.
- **Practice:** the close-up ball overlay uses a forward eight-phase stripe
  loop. The finger mask and PMG buffer publication are separate from the
  basketball hero artwork.
- **Basketball hero:** the dribble and dunk use the earlier cleaned artwork
  sourced by `tools/basketball_hero.py`. The redrawn poses and their masks are
  backed up under [implemented-poses](../art-review/hero-basketball/implemented-poses/).
- **Terminal and ending:** the opening and main-act strips use fixed striped
  text palettes. The final-boy greetings use the animated rainbow DLI glitch.
  The ending cards use fixed inks with fades and credit dual POKEY playback
  and its four updates per PAL frame.
- **Memory:** all 64 banks are allocated. The existing development JSON
  reports 295 unique shared scanlines. Regenerate it before budgeting memory
  for a change.

The development tree after prerelease 181 shadows PMBASE at `$0DFD`
for title fireworks, whistle PMG, and the two Trevor renderers. Sprite
publishers keep that byte in sync with ANTIC. The title reveal stops selecting
dissolve frames once the final text stage has elapsed. The full-rate loader
now includes the early blanking sync in its build recipe and disables DMA
before late payloads replace the loader display assets. These changes are in prerelease 182. The numbered file matches the hardware
development build byte for byte. It is 1,044,790 bytes and retains 66 INIT
wrappers and 64 staging clears. The build and targeted py65 checks passed.
Physical Atari playback remains unverified.

Prerelease 182 SHA-256:
`7e601c30c5558e9354827c83e48d7083b30c1328d373dcd10e71860d8957b369`.

Prerelease 183 is 1,044,796 bytes and matches the branch's hardware development
XEX byte for byte. It uses the full-rate animated AVG loader. The opening
temporarily uses `$9000–$9BFF`. The act strip and restored training lookup
tables use RAM under ROM. The targeted py65 checks passed, including pixel
comparisons for all three training shots with captions active. The full
Atari800 stereo POKEY recording matched prerelease 182. Physical playback
of 183 remains pending.

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

`make all` builds the development prototype and hardware-packaged development
pair. `make check` runs the discovered py65 suite. `tools/check_playback.py`
compares POKEY output in Atari800; it does not establish visual correctness,
physical playback or raster deadlines. For every hardware report, record PAL or
NTSC, Atari model, memory expansion and stereo configuration.

## Current scene timing

See [`TIMELINE_MAP.md`](TIMELINE_MAP.md) for the concise current timeline and
[`CURRENT_MONTAGE_V330.md`](CURRENT_MONTAGE_V330.md) for post-Trevor cuts.
Both documents are maintained in English. Historical Vxxx records are
archival change notes and may describe superseded states; use this status page
and the current source as authority.
