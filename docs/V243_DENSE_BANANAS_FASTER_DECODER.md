# V243 — dense bananas and a faster decoder

At the user's request, the image-symmetry saving from v241 was reverted.
Both graphics return exactly to v240: a dense 64×64 tile, uniform
direction of neighbouring fruit, the original zoom. Each variant has 32 distinct
frames of a full rotation. Ticks and phase-selection tempo were not changed.

## Speed-up

The new RLE separates input index Y and output index X. The stream is packed
with account for the source and framebuffer page boundaries, so the loops do not
have to recalculate two 16-bit pointers for each packet. Literals are copied two
bytes at a time, fills eight bytes at a time. Token 0 skips the padding to the
next input page; the end occurs after 15 bitmap pages.
The generator selects the packing threshold separately for frames within the
capacity of each bank, limiting the cost of the most expensive frame.

[READ] Callback with the ball and palette, after preparing both display lists:

| Motif | v240 max | v243 max | Less CPU |
|---|---:|---:|---:|
| Bunch | 78748 | 75139 | 4.6% |
| Peeled | 78599 | 72819 | 7.4% |

This is a CPU saving relative to the previous **dense** pattern, not relative to
the raw v241 symmetry. It still does not match the cost of raw copying.
The control tunnel keeps the v242 cost: 47233 cycles.
py65 does not model ANTIC DMA; the numbers above are not an FPS measurement.
First callbacks with DL building: bunch 87317/85847, peeled 70821/75345.

## Memory and isolation

- Eight existing loader banks 3–10; no gap from other scenes.
- Graphics 113,981 B; code and tables 1,667 B per bank; 3,755 B remain.
- Data $4000–$783F; helper $7840; entry $7C00; selector $7C80;
  decoder $7D00; fills $7E00; jump table $7F00;
  eight pointers $7F80–$7F8F.
- Scratch $0DC0–$0DC1 and $0DC4–$0DC6, private cache $0DDE, key $0DDD.
  No use of zero page or NMI scratch.
- Only the inactive framebuffer is unpacked. PORTB is protected by the
  existing music wrapper, and the shared cache $83FA is invalidated.

[READ] A comparison of loaded memory with v242: only banks
17–24 and 13 bytes of the selector $ED83–$ED8F differ. The other 56 banks are
identical, including the tunnels, the ball and the finale code.

## Verification

[READ] 9 targeted tests: all 64 frames decoded in agreement
with the generator and the v240 bitmaps, no writes to the front buffer, full rotation,
motif alternation, seeks and interrupts of the original player in the decoder.
The new cost regression requires max 76000/74000 cycles for the warmed-up motifs.

Preview: `build/banana-v243-variants.png`, animations
`build/banana-v243-bunch.gif` and `build/banana-v243-peeled.gif`.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **11376072
identical bytes** relative to v035, the whole song. No attempt on a physical Atari.
The working build and v243 have the same SHA-256:
`5c83f6d149be22dfa2cc778579f4d3c5dbd5cd71db135929fbb94e522df41785`.

[READ] `make check PYTHON=/tmp/finale197-venv/bin/python`: **186/186
tests**, no skips, 137.5 s. Whole Atari800 stereo song: 11376072
identical bytes relative to v035. The working build matches v243.
