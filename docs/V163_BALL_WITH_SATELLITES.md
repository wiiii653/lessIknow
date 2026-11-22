# V163 — Trevor bounces a finished ball with satellites

## Image and behaviour

Every third Trevor hit after the word releases a complete ball from the rotator:
16 rotation phases, the original four-colour cycle and both satellite orbits,
each from a pair of missiles. The whole effect shifts together towards the nearer edge.
The left hand (4) bounces left, the right (2) right; the direction follows from the pose,
not from alternating hit numbering.

[READ] BANG/BAM remain for the first 80 ticks. The flight takes the
unchanged age ticks 80–135. The remaining hits keep the spreading
clouds and debris. Hit ticks, scene boundaries and music were not changed.
The ball starts with its centre at x=48 or x=112 in the logical 160-pixel frame,
then moves by one pixel per tick. Rotation and satellites still
use the player tick. The earlier and later rotators/tunnels
keep their existing path and hole coverage, without a new PMG carousel.

## Shared renderer and hardware

No further masks were copied. The Trevor controller, through the existing
unbanked trampoline, calls an adapter in loader bank 2, which starts the
original `tunnel_ball` at `$7800`. The nested call restores PORTB,
and the controller restores the bank operand and the trampoline destination address.

The adapter preserves the pose, passes special pose 96 and a signed
x offset in `$83EA`. The original renderer adds this offset to the
ball and satellite positions before writing them to GTIA, in its
usual blanking window. On return the adapter restores Trevor's pose.

[READ] HPOS registers `$D000–$D007` are write-only; reading from those
addresses returns GTIA collision latches. An attempt to read positions
after publication was removed. The regression runs both directions with a model that rejects
every CPU read of those addresses. This prevents a situation where
a simple RAM model in py65 lets faulty hardware code through.

## Memory

[READ] Removed 16 copies of 512 B masks (`$5E00–$5FFF` of action banks
24–39): 8192 B recovered. Bank 49 remains untouched in this area,
because it holds the final boy's controller.

The Trevor controller shrank from 2557 to 2466 B: 91 B × 17 copies = 1547 B.
It ends at `$69A1`, leaving 94 B before `$6A00`.
The adapter in bank 2 takes 44 B (`$4000–$402B`). The free and zeroed
`$402C–$77FF` gives 14 292 B of contiguous area; the original renderer with its data
still takes 2048 B at `$7800–$7FFF`. The additional offset handling
fits within the existing alignment of this helper.

Additional net recovery relative to v162: **8192 + 1547 − 44 = 9695 B
(9.47 KiB)**. In total relative to v141: **35 416 B (34.59 KiB)**.
Still 64 banks; main still 2546 B, 14 B before `$1E00`.

## Verification

The tests compare all four planes of the finished ball with the rotator
masks, the positions and five-row masks of both satellites, the directions of both hands,
BANG/BAM and the clouds of the remaining hits. They check PORTB restoration,
the return through the music NMI, the absence of HPOS reads, tunnel hole coverage
and the PMG write executing in the window before the next satellites.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
13 910 544 identical bytes relative to v035, about 3874.9 s of emulation,
covering the whole track. This is a comparison of register data, without listening.

The previews `build/v163-rebound-left.gif`, `build/v163-rebound-right.gif`
and `build/v163-complete-rebounds.png` were made after the 6502 callbacks.
Their colours and pace are approximate; they are not an emulator recording.
[CONCLUSION] The py65 results and POKEY comparisons do not confirm the actual
FPS, ANTIC DMA deadlines or raster stability on physical Atari.
No test on physical hardware.

[READ] `make check`: 122 tests in 90.000 s, 119 passed,
3 skipped because of the missing archival v126. The map check confirms
the zeroing of 16 mask slots and of the free area in bank 2.

Release: `build/visual-prototype-v163.xex` and the corresponding JSON;
both are identical to the tested working dev files.
XEX SHA-256: `a670abbb762a11e11d8747c7bb42e86031a35d38389c090e3790cd5833b14db0`.
