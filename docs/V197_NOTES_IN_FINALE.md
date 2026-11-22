# V197 — little notes around the head in the finale

For the lying boy, four stars and four
melody symbols spin alternately around his head: notes and a treble clef from the initial whistling.
The change occurs every 256 player ticks (about 1.28 s). The orbit,
colour changes, preparation of the masks in the inactive PMG buffer and the final
fade-out are preserved. The melody shapes keep their original silhouettes; for the smaller
finale frame they use single rows and ordinary PMG width.

Build: `build/visual-prototype-v197.xex` and the corresponding JSON; the dev pair
updated. Scene boundaries unchanged. Main code still 2560 B.
Finale controller: 809 B at $5CD0; data 48 B at $69C4 and 95 B at
$7FA0 in the existing bank 49. The installer checks that all occupied
places were empty. In total 952 B versus 812 B in v196: an additional 140 B.

[READ] Nine `test_story_finale.py` tests passed: the masks of all
four objects through four switches, no residue in the buffers,
the orbit, the raster, the NMI and PORTB behaviour and the permanent black after the end.
[READ] Atari800 PAL / 1088XE / stereo POKEY: 6 125 832 identical bytes
compared with v035; the comparison covers the whole track.
[CONCLUSION] The CPU tests confirm the masks and the moment of register publication;
they are not an assessment of the appearance on physical Atari.

[READ] The full `make check` reports earlier test failures concerning
Trevor's recovered slots, the intermediate ribbon frames and the raster budget.
The five reported tests were run separately on the archived XEX v196:
all five also fail. They do not result from the finale masks.
Full result: 148 tests, 5 failures also confirmed on v196,
3 skipped. The nine finale tests also pass in the full set.
