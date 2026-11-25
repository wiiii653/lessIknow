> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V053 — complete music clock correction

V053 keeps the bar mapping introduced in v052 and corrects the last threshold of
the Trevor shot: the pose change in the quiet passage of act 4. The threshold now
falls on the boundary of bar 68 (`tick_at_bar(68) = 25429`), instead of at
`start + 4 × 374`.

The shared function `tools/music_timing.py` sets all music boundaries from the
beginning of the track according to `ceil(n × 373.95555)`. It covers act
boundaries, cheerleader cutaways, training and basketball, Trevor's entrance and
strike, and beat accents. The mosaic rhythms the palettes at intervals of
186/187 ticks with the correct PAL phase.

| Boundary | Tick |
| ---: | ---: |
| Bar 24 — dance | 8975 |
| Bar 32 — kaleidoscope | 11967 |
| Bar 40 — portraits | 14959 |
| Bar 56 — basketball | 20942 |
| Bar 64 — Trevor's entrance | 23934 |
| Bar 68 — Trevor's pose change | 25429 |
| Bar 72 — strike | 26925 |
| Bar 88 — end of Trevor's scene | 32909 |
| Bar 160 — end of track | 59833 |

`make all` built `build/visual-prototype-v053.xex`. The release copy
`releases/visual-prototype-v053.xex` has the same SHA-256 sum:

`65d4f50caa0b5006be459a7a8db3118720ae665b64936ab04c70563cee19ce2d`

No automated tests and no full listening test on the emulator were performed in
this change.
