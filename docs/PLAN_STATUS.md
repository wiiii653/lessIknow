# Project Status

Status reviewed on 2026-11-22. The numbered release and the source working
tree are separate states; do not describe a development build as an approved
release.

## Release state

- Latest approved stereo release: **release 133 / v390**.
- Approved file: `releases/less-i-know-demo-release-133-stereo.xex`.
- Approved music is embedded in that release. The development hardware build
  derives its music from this file and can apply the earlier-percussion option.
- Last full playback confirmed by the user on physical hardware: stereo release
  058 / v330, loaded from AVG on an Atari 1088 Rambo.
- Releases 059 and 060 failed on hardware. Release 061 and later releases have
  no user-confirmed full hardware playback. Emulator tests do not change this.

## Current development tree

The current tree includes source edits made after release 133, including the
opening reveal/fireworks work and refinements to the arena character masks.
These edits have not been cut as a new numbered release. Do not overwrite any
numbered release when building or packaging them.

The opening now uses procedural plasma, a staged city reveal and progressively
building PMG fireworks. The title animation code stores one city panorama and
derives the plasma/reveal frames procedurally. The boy's arena silhouette mask
has been refined around the hair and arena edge. These latest edits have passed
their targeted source-level checks where recorded, but this document does not
claim a full current playback or a real-hardware visual check.

The ribbon-dance front solo now follows the same half-beat pose cadence as the
preceding three-dancer section. Its inbetween poses remain enabled for smooth
transitions, while quarter-beat subdivisions are disabled in this solo passage
to keep its speed aligned with the trio. A stereo prerelease was built for
listening; it has not been confirmed on physical hardware.

The demo is stereo-only. The v035 player remains the music engine and runs four
evenly spaced updates per PAL frame. Scene timing is driven by its update
counter. The active allocator uses all 64 banks; there is no assumed free bank.
The shared scanline pool currently contains 298 rows, with its base at `$1E00`.

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
