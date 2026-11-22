# V055 — image effect phase

[READ] V055 retains the PAL bar mapping and scene thresholds from v053. For the
PMG accents in the dance and the mosaic palette changes it restores the phasing
used by v051. At the start of both mosaic shots the subtraction result is
clamped to zero when the scene begins before the effect's former start point.

[READ] As in v051, the mosaic pulse deliberately uses fixed 187-tick intervals
per half-bar. It therefore has a slight drift relative to the exact PAL grid:
about 3.2 ticks over 72 bars of the second mosaic, beyond the initial phase
offset. This does not change the player clock or the main scene thresholds.

[READ] In Atari800 7.2.1, PAL, 1088XE, Altirra OS, stereo, 14,958 frames were
compared up to tick 59832. The two previously examined palette pulses that in
v053 ran ahead of v051 again fell on the same frame samples as in v051 in v055:
ticks 12560 and 33128. Scene state and sampled POKEY registers agree between
versions on all compared frames.

| Fragment | v053 frame hash differences relative to v051 | V055 relative to v051 |
|---|---:|---:|
| Dance, 748 frames | 46 | 25 |
| First mosaic, 748 frames | 333 | 44 |
| Basketball, 748 frames | 190 | 190 |
| Second mosaic, 6731 frames | 3168 | 824 |

FNV-1a hashes identify potential image differences; they do not replace visual
assessment. An attempt to change the dribble phase in v054 increased the number
of differing basketball frames to 325, so it was reverted in v055. The
basketball animation remains as in v053.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python` passed 58 tests,
including the palette comparison with the retained v051.
Earlier v053 tests had six outdated expectations related to the frame phase
after the tick correction; they were fixed while keeping the image and
maintained-frame cost checks.

[READ] A full stereo POKEY comparison of v055 with the original v035 in Atari800
gave 7,762,320 identical bytes after a single alignment of the start. Listening
and a visual A/B comparison are still needed: equality of audio registers, or
agreement of two selected pulses, does not prove an ideal match to the audible
beat.

Release: `releases/visual-prototype-v055.xex`, SHA-256
`a327afb8c96b7638764e3159b196ff32bedece44907db6cb8b7c7be90c780d08`.
