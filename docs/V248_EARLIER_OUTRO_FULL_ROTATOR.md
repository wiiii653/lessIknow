> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V248 — full montage, earlier outro

At the user's request, 2000 ticks of montage lost in v240 were restored
and the whole montage was shifted 4000 ticks earlier. Trevor now ends
at 28909 instead of 32909, and the frame of the boy with the terminal starts at 49850
instead of 51850 (2000 ticks earlier, about 10.0 s earlier). The end of the text
at 59085, the fade and the black at 59833 remain. The last of the 13 preserved punches has
time for the whole BUM/BAM and the ball's departure; none is cut at a boundary.

The montage's virtual clock is the actual tick +4000. The sequence of phases,
motifs, palettes, ball and satellites replays the former
32909–53849 in the same order; the fragment corresponding to 51850–53849 was restored from v239.
The music is not shifted, so the visual events occur 4000 ticks
earlier relative to it. The earlier rotator shots keep the real clock.
All credits/greetz boards and their final tick remain; the earlier
entry extends the time available for reading.

## Memory and validation

The main code occupies 2560 B `$1400–$1DFF`: no headroom to the `$1E00` pool.
In loader bank 2, the Trevor flight helper occupies `$6E10–$71BE`, the director
`$7250–$73D6`, the selector `$7400–$744B` and the ball clock `$7480–$74B4`.
The existing masks and the ball helper `$7800–$7FFF` remain; still 64 banks.
Bank switches preserve PORTB, and the auxiliary clock `$0DD3–$0DD4`
is used before the terminal entry.

[READ] The test compares bitmaps, phases, PMG positions and palettes of montage samples
with v247 and of the restored ending with v239. Atari800 PAL/1088XE stereo POKEY:
11 118 384 bytes identical to v035, the full track. This is not a listening test nor
an FPS measurement from ANTIC DMA; there is no test on a physical Atari.

[READ] Full `make check`: 190/190 tests, 146.748 s.
