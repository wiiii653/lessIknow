> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V241 — fast bananas without decompression

## Cause and result

V239/v240 decompressed both RLE animations on every changed frame.
The cost of successive frames grew from about 47 thousand to 68–79 thousand CPU cycles.
The 90000 cycle limit alone did not guarantee keeping pace with ANTIC DMA.

V241 removes runtime RLE entirely. The bitmaps are copied directly
from the banks using the same procedure as the tunnels. Comparison with the same
callback invocation every 16 ticks:

| Motif | First two frames | Maximum of the next 30 |
|---|---:|---:|
| Bunch | 58644 / 58650 | 47300 |
| Peeled | 58682 / 58688 | 47375 |
| Tunnel | 58660 / 58671 | 47233 |

These are CPU instruction measurements without ANTIC DMA, not an FPS measurement. They do,
however, eliminate the extra cost that distinguished the bananas from the tunnels. Testing all
64 logical frames of both variants now requires fewer than 62000 cycles,
also on a cold entry; a separate test guards parity with the tunnel.

## Graphics layout and continuity

So that both variants fit without compression, the background composition was changed:
the source 128×128 tile contains two opposite copies of the same fruit,
with central symmetry. The drawing of the bunch and of a single peeled banana was kept,
but their placement is sparser and in pairs. The zoom repeats every half turn.

The layout after a 180° rotation is identical, therefore **16 unique
bitmaps per motif** are needed, replayed as **32 angular samples of a full rotation**.
These are not 32 unique bitmaps. The transitions 15→16 and 31→0 correspond to an ordinary
11.25° step, without a reset of the asymmetric bunch from the previous error.
The tests check the tile symmetry, the independent orientations of the four quarters
and the continuity of the seams. The alternation of entries and the ball PMG remain.

## Memory and code

Eight previous banks: four for the bunch and four for the peeled one.
Each holds four raw bitmaps (15360 B) and a 981 B helper. In total
**344 B of free gaps** remain, and not 9910 B as in v239. This is a deliberate cost
of restoring speed; no additional banks or gaps of other scenes were used.

Helper: $7C00–$7FD4. It has its own cache $0DDE and variant key $0DDD,
with invalidation of the shared key when switching to other renderers.
There is no decoder, no RLE streams and no use of zero page.

The variant selector $EBF0–$EC11 (34 B) and the bank selector $ED4D–$ED8F (67 B)
use the free tails of the existing intro reservations. Asserts protect the
typewriter and director boundaries. The row pool is still from $EDA0. Main 2518 B.

## Verification

21 targeted tests passed before the full regression. They cover
images, inactive buffer ownership, transitions, palettes, PMG and NMI.
Eight tunnel banks byte-identical with v240. The terminal and scene ticks
remain v240.

[READ] Atari800 PAL/1088XE, stereo POKEY: **11 610 936 identical
bytes** relative to v035, the whole piece. No attempt on physical Atari.

CPU/PMG previews: `build/banana-v241-variants.png`,
`build/banana-v241-bunch.gif`, `build/banana-v241-peeled.gif`.

[READ] Full regression: **184/184 tests**, no skips, 123.5 s.
The working build and v241 are identical; SHA-256:
`c17b9eb0d58fc9e35e84b159fa844a46d6c71f054afcd1fb10c54ff14a1de917`.
