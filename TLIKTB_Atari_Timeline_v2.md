> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](docs/README.md) for active instructions.

# Original Demo Timeline Draft (v2)

Historical planning document. Current scene timing is maintained in
[`docs/TIMELINE_MAP.md`](docs/TIMELINE_MAP.md) and
[`docs/CURRENT_MONTAGE_V330.md`](docs/CURRENT_MONTAGE_V330.md). Do not use this
draft as the active cut list.

## Original timing assumptions

- PAL vertical refresh: approximately 49.86 Hz.
- Music tempo: 128 BPM; a bar lasts 1.875 seconds.
- The player advances four POKEY updates per PAL frame, about 199.44 updates
  per second.
- The original five-minute track contains 160 bars.
- A bar is approximately 373.956 player updates. Bar boundaries are rounded up
  to the first whole update at or after the requested position.

The current implementation derives time from the v035 player tick counter,
not from an independent frame timer. See `tools/music_timing.py`.
