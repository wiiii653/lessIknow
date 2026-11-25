> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V162 — withdrawal of the new cycle and two existing Trevor balls

## Rotator and tunnel

At the user's request, the new v158–v160 PMG set was withdrawn: the cycle, heart,
new stars, puffs and duplicated masks. The rotator/tunnel in all of its ranges
again call the same original `tunnel_ball` from earlier scenes: a spinning
colourful ball and missile satellites. This ball covers the tunnel opening.
There is no additional obscuring object and no new carousel.
The background graphics remain without dithering, in line with v161.

The code and tests of the withdrawn experiment are preserved only in
`docs/archive/pmg_showcase_v160.py` and `docs/archive/test_pmg_showcase_v160.py`.
They are not imported by the builder and are not discovered by the production tests.
They do not occupy Atari memory. The older numbered XEX files remain preserved.

## Trevor's fight

BANG/BAM, the clouds and the shard splash are preserved. Every third blow, after
the text, releases alternately:

- the large tunnel ball — to the left;
- the compact throw ball — to the right.

Both use the existing masks. The same 512-byte slot `$5E00–$5FFF`
in every action bank contains two phases of the large ball and two of the compact one.
No further ball bitmaps were added. The large one uses two pairs of spaced
players; the compact one overlays four colour planes in one place.
The preserved missiles still supply the spreading shards.

Effect duration 80–135 ticks from the blow, the texts and the blow ticks themselves are unchanged.
The timeline and Trevor's illustration sources were not changed.

## Memory recovery

[READ] Loader bank 2 now has the entire `$4000–$77FF` free/zeroed:
**14 KiB of continuous area**. The only remaining payload is the previous
ball renderer with data at `$7800–$7FFF`, 2048 B.

The 12 657 B occupied by the new cycle were removed. Trevor's controller grew from 2556
to 2557 B, which across 17 copies occupies 17 B. After removing the duplicated
palette entries, the redundant state byte and replacing the phase table with a
calculation, the consistent BANG/BAM animation was preserved and both directions fit in the same
slot.

Net recovery relative to v161: **12 640 B = 12.34 KiB**.
In total relative to v141: **25 721 B = 25.12 KiB**. Still 64 banks.
The main code remains 2546 B. Trevor ends at `$69FC`, with 3 B of headroom
before the data from `$6A00`.

## Validation and release

The tests check the zeroed 14 KiB, the opening being covered by the original ball,
both types and all four planes of the fight balls, the opposite directions,
BANG/BAM, the shards, the inactive PMG buffer, NMI and PORTB. The late VCOUNT test
again matches the earlier ball renderer updated in the blanking.

[READ] `make check`: 121 tests, 118 passed, 3 skipped
(missing archived v126), 90.643 s.
[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
15 383 304 identical bytes relative to v035 across the whole track.

`build/visual-prototype-v162.xex` and the corresponding JSON.
Previews: `build/v162-large-left.gif`, `build/v162-small-right.gif`.
The palette and tempo of the previews after the 6502 callback are approximate; this is not an
emulator recording or an FPS measurement. py65 does not model ANTIC DMA.
Without listening and without a test on physical Atari.

SHA-256 XEX: `26349e9efc35072d335d1f96cf5f54a770e2a5089727fc0b4c982179d1a80dd6`.
The numbered XEX/JSON are identical to the dev working files.
