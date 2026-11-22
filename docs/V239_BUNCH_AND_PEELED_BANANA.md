# V239 — bunch and half-peeled banana, alternately

The bunch remains. Every other visible entry of the banana rotator shows
a single fruit peeled halfway: bright flesh, a yellow lower part and
three curled-back flaps of skin. The motif changes at the next entry,
without switching during rotation. Both variants keep **32 frames,
a full 360° and a clock of one frame per 16 ticks**. No dithering.

| Entry tick | Motif |
|---:|---|
| 12288 | Bunch |
| 14336 | Peeled |
| 32909 | Bunch — the whole section up to 35900 |
| 43008 | Peeled |
| 45056 | Bunch |
| 47104 | Peeled |
| 49152 | Bunch |
| 51200 | Peeled |
| 53248 | Bunch |

The variant follows from the position on the timeline, so seeking and re-entering
give the same image. There is no history-dependent entry counter. Throughout
32909–35900 the bunch is forced: the global time bit will not switch it
in the middle of the scene. Shot boundaries, tunnels, the ball and the satellites remain preserved.

## Memory

Both sets together are 64 bitmaps of 3840 B each, i.e. 245760 B unpacked.
They were placed in the **existing eight banana banks** (loader
3–10). Each bank contains four bunch phases and four corresponding
phases of the peeled fruit. No gaps were taken from other banks, nor the credits reserve.

- RLE graphics: **111114 B**.
- Code and tables: **1256 B per bank**, 10048 B in total.
- Total occupancy: **121162 B out of 131072 B**.
- **9910 B = 9.68 KiB** of scattered gaps remain in these banks.
- Relative to v236 a net recovery of 9902 B, despite adding a second full motif.
- Main code still 2521 B; the total number of banks does not increase.

The peeled variant starts in the opposite rotation and zoom phase, so that the large/dense
frames of both motifs do not fall in the same bank. This shifts the whole
cycle without shortening the number of frames or breaking its continuity.

## Decoder and buffers

The initial LZ in the working v237/v238 fit the graphics but exceeded
the existing CPU cost. In v239 a simpler RLE was used: literal bytes
and repetitions of a single byte. The decoder copies series from the end using
DEY/BPL; the lack of dependencies between bytes avoids the cost of testing
an additional counter. It uses neither the zero page nor the NMI scratch.
The packing chooses the repetition threshold within each bank's limit, allocating
free bytes to a faster stream for the most expensive frames.

The $7C00 entry was left for the main callback. The banana helper is at
$7840–$7BFE, the source copy/selection $7C80–$7C9B, the decoder $7D00–$7D90,
eight pairs of pointers $7F80–$7F8F. The data ends no later than $7840.
In bank 0 they fill this space exactly; an assert guards the code boundary.

The variant has a private key $0DDD and cache $0DDE. On exit the shared key
$83FA is invalidated, so it cannot masquerade as the school or ribbon frame
cache with the same values. Before skipping the copy, ownership of the active
display list is also checked. Only the inactive framebuffer is unpacked;
PORTB is still preserved by the existing NMI wrapper.

## Verification

[READ] New tests compare all 64 running frames with the generator,
enforce the 90000-cycle limit, the absence of writes to the front buffer, the alternation of entries,
the absence of a change in the middle of act 5, and jumps between motifs/school/ribbons.
Interrupts of the original music decoder are injected during unpacking;
after each one the same bank returns and the finished bitmap remains correct.

[READ] CPU measurement over 32 successive phases: the first two bunch frames
87875/88112 cycles; later max. 78748. The peeled variant max. 78599
after preparing the layout. This is CPU cost without ANTIC DMA, not an FPS measurement.

[READ] Eight banks of both tunnels byte-identical to v236.
Atari800 PAL/1088XE, stereo POKEY: **11 570 400 identical bytes**
relative to v035, the whole track. No test on physical Atari.

CPU/PMG previews: `build/banana-v239-variants.png`,
`build/banana-v239-bunch.gif` and `build/banana-v239-peeled.gif`.

[READ] Full regression: **181/181 tests**, no skips, 133.7 s.
The working build and v239 are identical. SHA-256:
`37cd975c936cadf7e1a4e6a3e4167af0441471d72f0324692335234a36a9c7dd`.
