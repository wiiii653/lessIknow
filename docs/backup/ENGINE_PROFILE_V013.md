> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# Engine v013 — cache, partial copies and PMG

## V1 — CPU and music

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 26 tests OK.
The py65 profile was saved in `build/engine-profile-v013.json`. Instruction
costs of the callback without ANTIC DMA, music NMI and vblank waits:

| Case | v011 | v013 |
| --- | ---: | ---: |
| Stationary title | 16166 | 403 |
| Stationary school | 16340 | 454 |
| Stationary training | 93424 | 434 |
| Solo pose change after buffers are filled | 93788 | 70272 |
| Duo pose change after buffers are filled | 93773 | 70213 |
| Trio pose change after buffers are filled | 93754 | 69785 |
| The same solo pose | 93788 | 984 |

[READ] The first buffer fill still costs about 93 thousand cycles.
Full copy: 7936 B, partial: 5376 B (pages 4–24). This is a conservative
change area, verified at build time for every pair of poses in a given group.
Content keys of both buffers prevent using diffs from the wrong frame.
It is not copying only individual changed bytes.

[READ] Full test in Atari800 PAL, expansion `-1088xe`, stereo POKEY:

```sh
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v013.xex --seconds 12
```

Result: 8 792 424 identical stereo POKEY bytes, about 2449.2 s of emulation.
One-time alignment of the recording start; the whole track is covered by the comparison.

[CONCLUSION] A typical pose change consumes about 25% fewer instruction cycles,
and stationary shots release almost the entire former renderer cost.
This does not establish a guaranteed free budget in every raster line.

## V2 / V3 — memory and interrupts

[READ] Each buffer has a separate content key. The image cache takes into account
the shot, the input offset and the kaleidoscope amplitude. A cache hit still
updates the palette and PMG in vblank. The music wrapper restores the foreground PORTB.
The interrupt-during-copy test and the original bank check pass.
The helpers occupy the ends of the buffers: `$AF00–$AFD5` and `$CF00–$CFC3`;
copying does not include them. Missiles `$0980–$09FF`, players `$0A00–$0BFF`.

## V6 — image and accents

[READ] On a real Atari800, 14 consecutive memory dumps were checked
after the callback: stationary training, three shots, filling both buffers,
partial copies of solo, duo and trio. Every raster matches pixel for pixel
with the source material. The py65 tests also check arbitrary pose order.

[READ] Four player stars and four missile dashes pulse above
the characters, for 24 ticks every ~93/94 ticks. The colors go from bright
warm through cyan to pink. The PMG data is preloaded; the callback changes
the registers. PMG DMA is disabled outside the active phase of the effect. Preview:
`build/v013-dance-pmg.png`.

[READ] Scene boundaries and tick thresholds remain as in v011.

[ASSUMPTION] No listening test on physical Atari was performed, nor a measurement of cycle
headroom in each line with PMG DMA. Full hardware validation of V1–V7 remains
a separate task; the POKEY comparison concerns the indicated emulator and configuration.
