> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V164 — rainbow rockets from the bottom to the upper sky

## Effect

Both demo opening screens have four phase-shifted launches.
A rocket starts at the bottom edge of the active image (y=190), leaves
an intermittent tail and flies to the upper part of the frame. The four apexes lie
at y=44, 72, 56 and 36. At the apex there is a broad central flash,
a bloom of twelve rays, and then falling, thinning sparks.
Additional missile shards fly off to the sides beyond the outline of the main explosion.

[READ] The ascent lasts 64 player ticks (about 0.32 s); the whole cycle
256 ticks (about 1.28 s). The next rocket is shifted by 64 ticks.
The vertical anchors have 64 phases per cycle and change every 4 ticks, which is why
the flight is not limited to the four jumps stored in the shapes.
The shapes still have 16 phases, and the colours change every 8 ticks — also
during the bloom and decay. Each player and its missile have their own
rainbow palette phase; without enabling fifth player mode.

The texts keep the layout and order of the entries I KNOW → THE BETTER → THE LESS.
The historical Crane, the backgrounds, the borders of both screens, the fade and all scene ticks
remain as in v163. The full fireworks are on top of the letters, the building
and the plasma (`PRIOR=$C1`).

## Buffers and memory

Preparation still writes only to the inactive PMG range
`$0980–$0BFF` or `$8980–$8BFF`. Publication switches the complete buffer,
positions and colours within the limited VCOUNT 124–127 window. No new write
reads GTIA position registers. PORTB is restored by the
existing calling code. The music update was not changed.

[READ] In each of loader banks 40/41:

- controller: 1428 B, `$6C00–$7193`, publication still `$7000`;
- anchors: 257 B, `$7280–$7380` — four arrays of 64 and a fixed anchor
  for the 64-row missile plane in the upper part of the sky;
- shapes: still 3072 B, `$7400–$7FFF` — 4 × 16 × 32 player rows
  and 16 × 64 missile rows.

The installer checks the empty space and the separation of the controller, metadata
and shapes. The additional missile spread tables are part of the controller.
Cost relative to v163: **2 × (72 B of code/tables + 252 B of anchors) = 648 B**.
Net recovery relative to v141: **34 768 B = 33.95 KiB**. Still 64 banks,
main 2546 B and 14 B of headroom before `$1E00`.

[READ] The v163/dev comparison confirms that only loader banks 40/41 changed.
All remaining 62 banks and all non-banked RAM are
identical byte for byte.

## Validation

The tests run the 6502 callbacks and check the start of each of the four rockets
at the bottom edge, the successive decreasing y positions, the explosion high above
the city, the broad flash and twelve or more colours during the explosion.
They also check the lateral missile movement, the full shapes above the texts
and the Crane, the falling/fading of sparks, the inactive buffer, the restoration of
PORTB, GTIA mode 11, the text order and the publication at late VCOUNT.

[READ] Scene-only tests: 8 passed in 7.205 s.
[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 601 744 identical bytes relative to v035, about 4067.4 s of emulation,
covering the whole track. This is a comparison of register data, without listening.

Previews: `build/v164-title-fireworks.gif` and
`build/v164-launch-to-burst.png`. Made after the actual 6502 callbacks,
with an approximate palette and tempo; they are not an emulator recording.
[CONCLUSION] py65 does not model ANTIC DMA or the actual raster deadlines;
POKEY consistency is not an FPS measurement. Without a test on physical Atari.

[READ] Full `make check`: 124 tests, 121 passed,
3 skipped (missing archived v126), 95.022 s.

## Release

`build/visual-prototype-v164.xex` and the corresponding JSON are identical
to the tested dev working files. Previous releases preserved.
SHA-256 XEX: `3b81a480977e7bc0523cfe84165cb3c766c5c6b366c6d99c2ec645e149037370`.
