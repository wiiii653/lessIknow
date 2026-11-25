> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V249 — two balls with satellites on hits

Each of the 13 retained hits begins with the arrival of the full rotator ball
with two pairs of orbiting stars. After the existing BUM/BAM, a
smaller dunk ball flies away with four independent orbits. The exact
masks, phases, satellite shapes and palettes of the original effects were used. Thirteen
different arrival vectors and thirteen other departure vectors cover the sides,
top and bottom; the path heads towards the existing fist. The timing of the hits, Trevor's
bitmaps, the BUM/BAM length and the v248 scene boundaries remain.

## Memory and validation

The new 1853 B renderer fits in loader bank 19 `$6800–$6F3C`, after the
school-walk image data and before its code `$7000`. In the same bank the large-ball
masks occupy `$7300–$7AFF`, the small-ball ones `$7B00–$7CFF`, the orbit tables
`$7D00–$7E7F`, and the offset tables `$7F00–$7FE6`. The installer checks the zeroed
area before use. The v247 flight helper was removed from bank 2; the remaining
use of that bank follows v248 unchanged. Still 64 banks and 2560 B main.

Masks and satellites are prepared in the inactive PMG, and the registers are published
in an early blanking window. The tests check the actual masks of both balls,
the original orbits and colours, unique vectors, the inactive buffer, the moving raster,
music NMI and the absence of HPOS register reads. The v248 boundaries remain.

[READ] Atari800 PAL/1088XE, stereo POKEY: 15 917 976 bytes identical
to v035 over the whole tune. Without listening, DMA FPS measurement and a test on physical Atari.
The preview `build/v249-flight-preview.png` shows selected frames generated
after the 6502 callbacks, with an approximate PAL palette; it is not an emulator recording.

[READ] Full `make check`: 190/190 tests, 145.141 s.
