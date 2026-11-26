# Current Demo Timeline

This concise map reflects the current source tree as reviewed on 2026-11-25.
Exact tick boundaries are generated from the music clock; after timing edits,
use `build/visual-prototype-dev.json` as the build-specific source of truth.
The clock runs at about 199.44 updates per second on PAL, with roughly 373.956
ticks per 128 BPM bar.

## Opening

| Player ticks | Approx. time | Image |
|---:|---:|---|
| 0–1,023 | 0:00–0:05.14 | Procedural plasma. Fireworks begin at tick 768. |
| 1,024–1,495 | 0:05.14–0:07.50 | City panorama and plasma reflection reveal together |
| 1,496–2,991 | 0:07.50–0:15.00 | The song title replaces “TAME IMPALA” over rippling water as fireworks build |
| 2,992 onward | 0:15.00 onward | School / arena sequence |

The opening is generated from a single panorama and procedural plasma rather
than a stack of full-screen animated city frames. The title and fireworks are
also built at runtime. The opening source changes after the approved release
have not yet been verified in a full hardware run.

## Main acts

| Player ticks | Approx. time | Act |
|---:|---:|---|
| 2,992–5,984 | 0:15–0:30 | School arrival, girl passes, boy whistles |
| 5,984–8,975 | 0:30–0:45 | Basketball practice build-up |
| 8,975–11,967 | 0:45–1:00 | First side-dancer sequence |
| 11,967–14,958 | 1:00–1:15 | Banana roto-zoom and tunnel transition |
| 14,959–20,941 | 1:15–1:45 | Ribbon dance and performance |
| 20,942–21,689 | 1:45–1:49 | Tunnel cutaway before the dunk |
| 21,690–23,933 | 1:49–2:00 | Basketball hero sequence and dunk |
| 23,934–29,655 | 2:00–2:29 | Trevor fight with 13 hits |
| 29,656–41,883 | 2:29–3:30 | Post-Trevor montage: bananas, tunnels and girl's eyes |
| 41,884–51,231 | 3:30–4:17 | Terminal credits and greetz below the boy's still portrait |
| 51,232–51,979 | 4:17–4:21 | Final shot, orbiting sprites and fade |
| 51,980 onward | 4:21–5:00 | Final card and orbit; music continues to five minutes |

The post-Trevor cuts are listed in detail in
[`CURRENT_MONTAGE_V330.md`](CURRENT_MONTAGE_V330.md). The table above is a
rounded overview, not a substitute for the generated build JSON.

In the ribbon-dance section, the front solo uses the same half-beat pose-change
cadence as the preceding trio. Smooth half-beat inbetweens are retained, but
extra quarter-beat subdivisions are suppressed during the solo so it does not
run faster than the three-dancer passage. The built stereo prerelease has not
been confirmed on physical hardware.

## Timing and validation

Scene changes follow the v035 player update counter, not a separate VBI timer.
The current source computes PAL tick positions in `tools/music_timing.py`.
Emulator POKEY comparisons check the audio register stream; they do not verify
visual synchronization on a physical Atari. See [Project Status](PLAN_STATUS.md) for hardware evidence.
