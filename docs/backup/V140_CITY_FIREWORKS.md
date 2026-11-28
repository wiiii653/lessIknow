> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V140 — city fireworks and title entrance order

[READ] The final layout of the second board remained unchanged: THE LESS at the
top, I KNOW in the middle, THE BETTER at the bottom. As clarified by the user,
only the order of entrances was changed: I KNOW, THE BETTER, THE LESS. The
existing mask trigger moments and transitions between boards remain unchanged.

[READ] Both boards have a city silhouette at the bottom of the plasma and
fireworks: a rocket, a bloom, expanding arms and falling sparks. Four players
and four missiles use normal colours above GTIA 11 (`PRIOR=$C1`, without a
fifth player). The PMG masks account for the sum of both complete letter boards
and their shadows. Thanks to this they also do not obscure the text bleeding
between cards. PMG brightness follows the board fade.

## Memory and raster

[READ] No new banks and no new full bitmaps. The existing 16 background frames
were changed by adding a low city silhouette. The fireworks occupy the former
empty bank tails of plasma banks 40–41 (loader indices): the controller `$6C00`,
a separate commit entry `$7000`, 16 × 5 × 32 B of masks `$7400–$7DFF`, five
vertical anchors `$7E00–$7E04`. The controller is 1324 B including padding up to
the fixed entry; with data and anchors it is 3889 B per bank. Non-banked code
grew by 70 B relative to v138. The same 64 banks are still allocated.

[READ] The PMG calculations and writes go to one of the existing inactive
buffers `$0980–$0BFF` / `$8980–$8BFF`, before the plasma composition. At
presentation time the switching of PMBASE and the registers remains within a
bounded blanking window. No DLI or music ticks were added. The colours of the
letters themselves still change according to the existing beat phase.

[READ] Instruction measurement on the first implementation: PMG preparation
added about 9.6 thousand cycles. For this reason preparation was separated from
publication so that the long copy does not happen after waiting for blanking.
The regression CPU limit for the intro samples was changed from 140 thousand to
150 thousand cycles; this is not the deadline of one PAL frame. The earlier
plasma composition alone already exceeded a single frame; we do not claim 50
new frames/s.

## Verification

Tests cover the order and behaviour of the word positions, all mask phases,
protection of letters/shadows, the actual PMG state during board bleeding, no
writes to the active PMG, late raster entries, restart, and the return to
ANTIC E in the school scene. The preview `build/v140-city-fireworks.gif` comes
from 187 successive callback runs every 16 ticks; colours and timing are
approximate, and the model does not include ANTIC DMA or real hardware
deadlines.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 714 136 identical
bytes relative to v035, the whole track. This is not a hardware listening test.

Sources: `tools/title_plasma.py`, `tools/title_fireworks.py`.
Release: `build/visual-prototype-v140.xex`.

[READ] Final `make check`: 99 tests, 96 passed, 3 skipped due to the missing
archival v126; 85.614 s. Working XEX identical to v140.
SHA-256: `089c298b9a098d686fe069b69e0cca397d456bb5a4ec775453d3d63a4f9a976e`.
