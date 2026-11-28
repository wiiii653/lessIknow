> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V157 — continuous ribbons in all shots

## Cause

The `ribbon_streams()` generator marked only the rounded points of the sampled
curve. At the highest vertical speed successive points differed
by two rows, leaving an empty row in between. The gaps were therefore
stored in the masks themselves, used by all ribbon shots.
Example: player 0, phase 0 had empty local rows 26 and 38.

## Fix

Successive samples are joined with rasterised segments that fill
every skipped row and preserve a continuous path. The change covers all
four players and 16 phases, i.e. 64 masks. The loop shapes, hand
anchors, character motion, rainbow bands, sizes and timing were preserved.

Missile sparks, ejection fireworks and wind streaks are separate shapes;
their intentional gaps were not filled.

[READ] Still 5120 B of data in bank 49, `$6A00–$7DFF`.
No increase in RAM, code or the number of banks. The PMG double buffering
mechanism, image publication and music and scene ticks were not changed.
The memory map and v156 balance remain current.

## Validation

The regression covers all 64 masks: every row between the extreme
points is occupied, and all pixels belong to a single path
under eight-direction neighbourhood. The existing tests of the inactive buffer,
moving VCOUNT and music NMI were preserved.

[READ] `make check`: 119 tests, 116 passed, 3 skipped
(no archival v126), 89.045 s.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 720 904 identical bytes relative to v035 through the whole piece.
No listening session or physical Atari test was performed; py65 does not model
ANTIC DMA and does not determine the real FPS.

## Release and previews

`build/visual-prototype-v157.xex` and JSON.
`build/v157-connected-ribbons.gif` shows the side shot, the group and the solo;
`build/v157-connected-ribbons.png` juxtaposes these three shots.
After the 6502 callback is executed the previews have an approximate palette and timing,
they are not an emulator recording.

SHA-256 XEX: `4b2efb01129cabacb5be767dcfaec1132d409c803b21df6bc3654fd105213235`.
The numbered XEX/JSON are identical to the dev working files.
