> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V052 — improved bar-to-tick mapping

## Change

The engine previously used an approximation of 374 ticks per bar. Since the
player clock runs at 199.44296 Hz, and a bar at 128 BPM lasts 1.875 s, the actual
average is 373.95555 ticks per bar. The error of the old conversion accumulated
to about 7 ticks (35.7 ms) at the end of the track.

`tools/music_timing.py` now determines the threshold of bar `n` as
`ceil(n × 37 395 555 / 100 000)`, always counted from the start of the track.
This means the first whole tick not earlier than the planned musical moment.
The act and cut boundaries as well as the dance accents use a shared function.
The mosaic shots change palette according to the rhythm of half-bars lasting
186 or 187 ticks.

| Boundary | V051 | V052 |
| ---: | ---: | ---: |
| Bar 24 — dance | 8976 | 8975 |
| Bar 32 — kaleidoscope | 11968 | 11967 |
| Bar 56 — basketball | 20944 | 20942 |
| Bar 64 — Trevor | 23936 | 23934 |
| Bar 72 — punch | 26928 | 26925 |
| Bar 88 — act change | 32912 | 32909 |
| Bar 160 — end | 59840 | 59833 |

## Build result

`make all` built `build/visual-prototype-v052.xex`. The release copy
`releases/visual-prototype-v052.xex` has the same SHA-256 sum:

`94fb15c9162f05a2b43587f0ec7eec79e07b52afcbd27e76c74cf82d2a23c008`

No automated tests and no full emulator listening test were performed in this
change.

In v052 the threshold of Trevor's internal pose change at bar 68 was still
present, based on the old addition of `4 × 374` to the act start. It was fixed
in v053; the release sum for v052 above refers to the version before this last
correction.
