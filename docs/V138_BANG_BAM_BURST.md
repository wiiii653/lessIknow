# V138 — BANG/BAM and colourful cloud burst

## Hit effect

[READ] Successive hits alternate BANG and BAM. The shorter word is centred
in a shared cloud. The font stays black during the legible-word phase,
and the missiles background cycles through bright hues.

| Age since hit, ticks | Phase |
| --- | --- |
| 0–7 | Flash and unfolding of the cloud |
| 8–79 | Legible BANG or BAM |
| 80–103 | Letters disappear; four coloured player fragments break away from the centre |
| 104–119 | The cloud spreads to the sides; four missiles form separated debris |
| 120–135 | Shrunken players and missiles, small separate fragments with gaps |
| from 136 | The effect fades before the next hit |

[READ] `HITS`, the hand sequence, scene boundaries and music ticks were not changed.
The existing splash ending can still be running during the next swing.
The fragment palette uses a 16-shade cycle and shifts between the four players.
In the initial cloud the missiles act as a fifth player; after the burst they
receive four colours matching the players. Colours change on PMG,
without repainting Trevor or his background. No DLI was added.

## Memory and raster

[READ] The Trevor helper grew from 1748 to 2395 B and still fits in its
slot `$6000–$69FF`. 165 B remain before the `$6A00` boundary, where the streamers
start in bank 49. The code is duplicated in 16 action banks and the entrance bank:
the increase in occupied data is 17 × 647 B = 10 999 B, within the existing banks.
No banks or source images were added. All 64 banks are still in use.

[READ] The effect uses the already separated PMG buffers `$0980–$0BFF` and
`$8980–$8BFF`. Write operands are directed to the inactive buffer;
positions, sizes, palette and PMBASE are committed in the start-of-blanking window.
The previous PMG image is not erased while the next one is being prepared.
Outside the active effect PMG can be disabled, in line with the existing scene.

## Documentation and sources

Updated `AGENTS.md`, `README.md`, `docs/PLAN_STATUS.md`, the timeline
and the technical limitations. The current map distinguishes loader indexes from PORTB,
marks the V120 slots as already taken, describes the double PMG, the block on the old V7
and the missing acts 5–8. Historical release notes remain preserved.

Code: `tools/trevor_polished.py`. New tests check both words, both hit
directions, separation/shrinking and fragment colours, the absence of writes to the active PMG,
late raster positions, decoder interrupts with PORTB restoration and the return to the dance.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 283 288
identical bytes with v035, the whole track. This is not a listening test on physical Atari.
The moving-VCOUNT tests do not model ANTIC DMA or real GTIA fetches.

Preview: `build/v138-bang-bam.gif`, sequential callbacks every 4 ticks,
approximate palette and pace; this is not a recording of the full emulator.
Release: `build/visual-prototype-v138.xex`.

[READ] Final `make check`: 94 tests, 91 passed, 3 skipped
because of the missing archival v126; 84.481 s. The test of real decoder NMIs
confirms an identical finished PMG and registers after interrupted rendering.
The working XEX is identical to v138.
SHA-256: `0f37cc4d8edab22027ee34a9c248cf68f91b22989f04dec40615805287dd83e1`.
