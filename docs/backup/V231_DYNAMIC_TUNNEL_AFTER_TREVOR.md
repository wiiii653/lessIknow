> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V231 — dynamic tunnel after Trevor

## Edit

The segment from tick 41984 to 53849 is now driven by musical phrases.
The segment length and the entry of the lying boy at 53850 remain preserved.
The change applies only to the tunnel windows inside the existing cycle.

- The existing spiral "fan" interleaves with the organic tunnel.
- Successive accents change the animation direction and the 1×/2× speed.
- The base rhythm of changes is a half bar (about 0.94 s), with a shorter quarter-bar
  accent at the end of each four-bar phrase.
- The table has 72 entries; in the banana windows it is deliberately skipped.
- The ball, its colours and satellites still work according to the existing effect.
  The tunnel variant is also passed to the ball controller, so the mask
  remains matched to the current frame and covers the central hole.

No bitmaps or new PMG effects were added. The graphics of both tunnels and of the bananas,
the earlier occurrences of these effects and the act boundaries are preserved.
The previously reported issue of incomplete banana rotation is not the subject of
this change.

## Code and memory

`tools/post_trevor_director.py` generates the frame selection procedure and
the table of musical cue points. It replaces the global frame computation in the main
callback; outside the target segment it reproduces the original result.

- Procedure together with the tables: 337 B, $EC20–$ED70.
- Reserve: 384 B, up to $ED9F; the shared static rows start at $EDA0.
- The intro helper reserve grew from 1888 to 2272 B; the intro and terminal code itself
  keeps its addresses.
- Main callback: 2524 B, 36 B less than in v230.
- Scratch: $0DDA. No new extension banks and no use of their gaps.

## Verification

[READ] 38 targeted tests passed: scene clock, edit boundaries,
two motifs, PORTB restoration, PMG and coverage of every hole pixel around
the cut points. The tests also check the unchanged banana clock and earlier
shots.

[READ] Atari800 PAL/1088XE, stereo POKEY: 10 104 192 bytes identical
to v035; the comparison covered the whole track. The four musical updates per frame
and the NMI procedures were not changed.

[READ] Full run: 168 tests in 115.9 s; 167 passed, one
compared frames with the old edit clock. The tick selection in that test was updated,
keeping the check of all 64 bitmaps and of the inactive-buffer
properties. Re-running the module: 4/4 passed. The XEX code did not
require changes after that; in total all 168 cases were verified.

[READ] The cost of the director alone at the table points: 85–1348 NMOS
6502 cycles. This is a CPU measurement without ANTIC DMA and musical NMIs, not an FPS measurement.

CPU/PMG reconstruction preview: `build/post-trevor-v231.gif`.
This is a reconstruction of frames, not an FPS measurement or a recording from physical Atari.
