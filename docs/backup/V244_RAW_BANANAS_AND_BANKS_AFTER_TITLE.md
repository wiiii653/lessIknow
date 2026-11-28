> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V244 — raw bananas and bank reuse after the title

The actual playback of both bananas now uses raw bitmaps,
just like the tunnels. The RLE cost was removed from the critical animation path
without changing the 64 images, pattern density, orientation, zoom, palettes, PMG
or timeline.

## Why memory is sufficient

All 64 banks were allocated, but the nine title banks 40–48
no longer have work after tick 2992. Reusing them gives 144 KiB
of scene memory. Eight hold additional raw frames, the ninth serves
as staging. No scattered gaps from other scenes and credits were taken.

| Owner | Before the title / during the title | After preparation |
|---|---|---|
| Loader 3–10 | 64 packed frames of both bananas | 32 raw frames of the bunch |
| Loader 40–47 | Plasma, masks, transitions and title fireworks | 32 raw frames of the peeled banana |
| Loader 48 | The last transition and title masks | Frame staging + helper templates |
| `$E580–$E956` | Part of the title code inactive later | Worker cache |
| `$EA00–$EAFF` | Title data inactive later | 256 B of scratch |
| `$EB00–$EB1F` | Title data inactive later | Private worker state |

Bank 46 stores the templates and bootstrap in the unused end of the fade:
$5400–$5BFF templates, $6000–$63D6 worker, $6800–$6845 bootstrap. Before
bank 46 is overwritten, the templates are copied to bank 48 under
$6000–$67FF. The staging in bank 48 is $4000–$4EFF. The raw banks contain
4 × 3840 B bitmaps plus a 981 B helper at $7C00; 43 B remain each.
In total 245760 B of images and 15696 B of helpers in 16 banks; 688 B of their
combined tails. This is the runtime budget, separate from the packed startup data.

## Background preparation

The bootstrap arms itself during the actual passage through ticks
3072–3327. The main callback gives the worker one task per call up to
11775. Each task processes one 256 B page. First the four frames of the peeled
banana are produced in the new bank, then the bunch in its own bank,
from frame 3 down to 0. If the destination write could cut across the source of
the current frame, the worker unpacks it into bank 48 and only then copies it back.
The source pointers and the helper are overwritten only after use.

FLAG $0DDF: 0 = original data, 1 = preparation, 2 = full raw.
Preparation needs 1261 small tasks. The worker does not use the music scratch
or the zero page, preserves PORTB, and does not touch the framebuffers,
PMG or image publication registers. The cache and the terminal font have
disjoint ranges; typewriter $EB44 and director $EC20 remain.

[READ] Atari800 PAL/1088XE, Altirra OS: the worker completion breakpoint
falls at tick **8609**. The Act 2B window boundary is at tick **11968**
(bar 32, scene threshold); the first rotator/tunnel selection observed in the
Atari800 callback occurs at tick **11976** and reads FLAG=2. These are two
different points: the timeline threshold and the first measured renderer
selection. The margin to the start of the window is about **17 seconds**,
and to the first bananas 12288 about 18 seconds. This is a reading from an
emulator modeling ANTIC, not a conclusion from the py65 budget alone.

## Smoothness

| Theme | Max. callback after warm-up |
|---|---:|
| Bunch | 47323 CPU cycles |
| Peeled | 47402 CPU cycles |
| Tunnel | 47245 CPU cycles |

[READ] Trace of successive renderer calls in Atari800: the bunch at ticks
12288–13300 performs 63 phase changes, always by one modulo 32 — two full
cycles without a skipped frame. The peeled at 14336–14944 performs 38 such
changes, also without skips, and shows all 32 phases. The shot lengths are
preserved. The py65 instruction measurement alone is not FPS, which is why this
trace was checked separately.

## Tests and tooling limitations

The new tests perform full preparation with 1122 injected interrupts of the
original player. All 64 raw bitmaps match the generator.
Physical banks, PORTB, the absence of writes to the image/PMG and the cost of both
themes below 48000 cycles after warm-up are checked. The most expensive task with
NMI: 11462 cycles; without NMI 10161 cycles. The remaining banks are not changed
by the cache.

This is an overlay for normal forward playback. Once the title
banks have been used, going back to the title requires reloading the XEX. A large
seek from a fresh XEX outside the bootstrap window keeps the title code and uses
the previous RLE; such a seek does not measure the cost of prepared playback.

[READ] Whole track Atari800 stereo: **10589472 bytes identical to v035**.
No attempt on physical Atari. XEX v244 and the verified cache-work identical:
`4f6ab57d3919ce7bf0119607910a6a8dd931870beb2887898850925bc6e4eb5a`.
Main 2557 B ($1400–$1DFC), 3 B remain before the row pool $1E00.

[READ] `make check PYTHON=/tmp/finale197-venv/bin/python`: **189/189
tests**, no skips, 151.2 s. Working build and v244 identical.
