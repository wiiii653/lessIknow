> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V160 — beating heart and hole masking by the active effect

At the user's request, the separate ball that in v158 constantly covered
the centre regardless of the effect shown was removed. Now **the current PMG object itself**
has a full silhouette over the hole. There is no extra ball and no shared mask
under the objects. All four players belong to the current effect.

Fireworks were removed from the post-Trevor cycle. The order:

1. Large rotating ball, again four colour planes.
2. Compact coloured ball.
3. Beating red-pink heart with shading and a bright highlight.
4. BANG/BAM on a full comic cloud.
5. Full cloud with spreading fragments.
6. Large star and orbiting smaller stars.
7. Compact gust of air with narrow streaks, without fireworks.
8. Full glass shard with colourful planes and flying fragments.

The heart has eight phases with two size pulses and a brightness change.
Its outline, top notch and highlight are drawn directly into the
16×32 masks. The minimal silhouette still covers the whole hole.

In the balls the hole is covered by the ball, in BANG/BAM by the cloud itself, in the stars
by the central star, and so on. Smaller particles may fly away, but the main object
does not uncover the hole. The fireworks of the earlier intro and of the throw are not
part of this change. Sashes are still excluded from the cycle.

Range 32909–59085, mode change every 512 ticks and a 4096-tick loop unchanged.
The v159 dithering, earlier scenes, the final boy and the music remain.

## Renderer, priority and memory

Player 0 no longer has a fixed mask, position or size. Each of the 64 frames
has its own 32-byte stream and metadata. The object type decides which
plane covers the centre. In the comic explosion and the glass the object's full background
is on P3, under the lettering/highlights on P1/P2. The actual GTIA priority order
is preserved. The layer composition order in the programmatic preview was also fixed,
so that P0 is above P1, and so on.

Loader bank 2:

- `$4000–$41F0`: helper, 497 B, +28 B.
- `$4400–$63FF`: P1/P2/P3 streams and missiles, 8192 B.
- `$6400–$693F`: existing metadata, 1344 B.
- `$6A00–$6AFF`: existing pointers, 256 B.
- `$6B00–$72FF`: dynamic P0 masks, 2048 B instead of the shared 16 B core.
- `$7300–$73BF`: P0 positions and sizes, 192 B.
- `$7400–$747F`: P0 pointers, 128 B.
- `$7800–$7FFF`: earlier-scene renderer, 2048 B.

[READ] Bank occupancy 14 705 B, +2380 B relative to v159; 1679 B of gaps remain.
Still 64 banks and 2546 B of main code with 14 B of headroom.
Net recovery relative to v141: 13 081 B (12.77 KiB).

The whole PMG is prepared in the inactive buffer, then committed
in a bounded window at the start of blanking. There is no moment with an empty cover
during the transition between modes.

## Validation

The test runs all 64 frames and checks:

- agreement of each of the four masks and its position with the active effect;
- coverage of every hole pixel by the sum of the effect's actual masks;
- absence of fireworks and presence of the heart and both of its pulses;
- priority of the lettering over the cloud in hardware and in the preview;
- no writes to the active buffer, returns to earlier scenes and the finale;
- decoder NMI interrupts and PORTB preservation and late VCOUNT.

[READ] `make check`: 124 tests, 121 passed, 3 skipped
(missing archival v126), 90.686 s.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
15 806 592 identical bytes relative to v035 across the whole track.

py65 does not model ANTIC DMA and does not determine the real FPS or raster
stability on physical Atari. No listening test and no hardware test were performed.

## Release and previews

`build/visual-prototype-v160.xex` and the corresponding JSON.
`build/v160-beating-heart.gif` — the heart; `build/v160-pmg-cycle.gif` — the full
cycle. `build/v160-active-objects.png` juxtaposes the ball, heart, lettering and glass.
Previews are produced after the 6502 callback; the palette and timing are approximate,
they are not an emulator recording.

SHA-256 XEX: `1f74fc2fb6533b216d2a18924ee83394fcff62b3009d2f3c2c6e4b043fbab3f5`.
The numbered XEX/JSON are identical to the working dev files.
