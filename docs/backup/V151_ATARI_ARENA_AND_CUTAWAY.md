> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V151 — ATARI ARENA, cutaway and quick dunk

## Approved edit

The user asked for a short cutaway of the tunnel with the ball after the
launch, preserving the launch length, and for shortening the stretched dunk scene.
The interior of act 3 was rebuilt without shifting Trevor's entrance or the music:

| Ticks (exclusive end) | Bars | Nominal length | Image |
|---|---|---|---|
| 17950–20942 | 48–56 | 15 s | Previous dance and single launch; no change to length or flight phases |
| 20942–21690 | 56–58 | 3.75 s | Cutaway of the spiral tunnel with the v150 neon ball |
| 21690–23186 | 58–62 | 7.5 s | Dribbling inside ATARI ARENA |
| 23186–23934 | 62–64 | 3.75 s | Single dunk, crack and shattering of the backboard |
| from 23934 | from 64 | unchanged | Trevor's silent entrance |

The dunk lasts half as long: its phase advances every 8 ticks, formerly every 16.
The sequence remains complete: preparation, two flight stages, contact,
crack, shatter and the ball falling. The end of the backboard breaking was not cut.
The cutaway uses all 32 phases of the existing tunnel and the v150 ball;
it does not take new banks for additional bitmaps.

## Art and logo

The fictional ATARI ARENA replaces the school in the existing exterior shots
2992–5984. The façade is inspired by the oval form of ERGO ARENA, with bands of glass,
a low roof, a large lettering and Fuji above the entrance. The boy, the girl's movement,
the scrolling of planes and walking into the depth retain the existing choreography.
On the girl's back, the large Fuji replaces NORTH; a smaller sign is also
on the jacket in the side shot.

In act 3 the new interior has large stands, a roof truss and a suspended
ATARI ARENA screen. Further rows of the audience are calmed during reduction to the Atari palette,
so that the character remains legible. The player and the basket come from the existing
illustrations, with separate masks; the animated arm still uses the same
small patch. After the backboard is smashed, the actual arena background is revealed.

Architecture sources: the official [ERGO ARENA façade](https://ergoarena.pl/wp-content/uploads/2024/07/Rectangle-14.jpg)
and [interior during basketball](https://ergoarena.pl/wp-content/uploads/2024/09/Arena-Glowna5.jpg).
This is an illustration inspiration, not a documentary reconstruction of the venue.

Both illustrations were made with the built-in `image_gen.imagegen`:

- [Façade](../../assets/art/source/act1_atari_arena_exterior_v151.png),
  [full prompt and references](../../assets/art/source/act1_atari_arena_exterior_v151.prompt.txt).
- [Interior](../../assets/art/source/act3_atari_arena_interior_v151.png),
  [full prompt and references](../../assets/art/source/act3_atari_arena_interior_v151.prompt.txt).

The sources remain in the repository, the old illustrations are preserved.
`tools/arena_art.py` performs the target quantisation, compositing and overlaying
of the small Fuji signs. The Makefile prepares two raw RGB inputs.

## Memory and code

[READ] Still 64 banks. The arena bitmaps replace the existing data
within the existing structures, and the cutaway shares the tunnel and ball banks.

- Main code: 2546 B (`$1400–$1DF1`), +31 B; **14 B** before the `$1E00` pool.
- Hero helper in loader bank 1: 2652 B (`$4000–$4A5B`), +15 B.
  292 B remain before the data from `$4B80`. The data and three backboard shatter patches
  still end at `$7E3B`.
- Shared rows: 279 instead of 277; packed they occupy **10 927 B** instead of
  10 998 B, i.e. saving 71 B. The number of scene table entries does not grow.
- Net change relative to v150: +31 +15 −71 = **−25 B of occupancy**.
  Recovery relative to v141: **23 671 B = 23.12 KiB**. This does not mean a free bank.

The banked hero passes the initial two bars to the unbanked trampoline,
which starts the normal tunnel renderer. Nested returns restore
PORTB. The phase selection takes both tick bytes into account, including the crossing of `$xxFF`.
The four music updates per PAL frame and the DLI layout are preserved.

## Validation

[READ] `make check`: **116 tests, 113 passed, 3 skipped**
(missing archived v126), 86.535 s. The tests cover the unchanged end of the
launch, the cutaway/dribbling/dunk boundaries, all poses and phases
of the backboard shatter, buffer consistency with the graphics, the large Fuji, PORTB,
NMI injection and the ball's late VCOUNT.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
**15 154 704 identical bytes** relative to v035; the whole track is covered.
The final rebuild is identical to the binary file covered by the comparison.
No listening test or test on physical Atari was performed. The py65 tests do not model
ANTIC DMA and do not determine the real FPS or raster stability on hardware.

## Release and previews

- `build/visual-prototype-v151.xex` with the corresponding JSON.
- `build/v151-arena-exterior.gif` — the whole section in front of the arena.
- `build/v151-launch-tunnel-dunk.gif` — end of the launch, cutaway and act 3.
- `build/v151-atari-arena.png` — façade, large Fuji and interior.

The GIFs play once; they are generated from the 6502 callback with a 16-tick
step. Colours and tempo are approximate; this is not an emulator recording.

XEX SHA-256: `52c99b69e13b70fc8b3d8af9d591b8aa34ce4de68b6fba956ee4f5325a0bf52f`.
The numbered XEX/JSON are identical to the working `visual-prototype-dev` files.
