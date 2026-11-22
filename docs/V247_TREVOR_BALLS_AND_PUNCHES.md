# V247 — Trevor's balls and punches

Each of the 40 existing punches keeps its tick, drawing, pose and
alternating BUM/BAM caption. A small ball from the basketball insert masks
flies in from the side of the proper fist in the last 32 ticks before the
punch. Then the full impact effect lasts 80 ticks, after which the ball flies
away towards the same edge in ticks 80–105. Some punches are 140
ticks apart: the flights and the caption must fit into this existing rhythm.
The previous clouds and the large ball with satellites are not called in this
scene.

## Memory and verification

The new helper and eight sets of four masks occupy 1078 B in loader
bank 2, `$6E10–$7245`. The installer checks that the area is empty;
the end of the free gap after this helper is `$7246–$77FF`. Trevor's code is now
1823 B, with no changes to his bitmap data and no change to the bank count. PMG
preparation happens in the inactive buffer, publication in the early
blanking; the banked call preserves the foreground bank and does not read HPOS.

[READ] The py65 tests check all 40 arrivals and departures, the ball
masks, poses, BUM/BAM, the inactive buffer, the moving VCOUNT and the musical
NMIs. Comparison of representative Trevor bitmaps with v246 showed no changes.
Atari800 PAL/1088XE, stereo POKEY: 16 392 024 bytes identical to v035,
the full track. The AppImage was run after extracting to `/tmp`, without FUSE.
This is not a listening test nor an FPS measurement with ANTIC DMA; there is no test on physical Atari.

[READ] Full `make check` for v247: 188/188 tests, 148.501 s.
