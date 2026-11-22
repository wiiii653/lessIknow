# Dunk payload artefact audit — v347

The graphics and bank code of the dunk payload in v347 are identical to v330. In a comparison of 94 py65 phases it rendered the same pixels and PMG. This does not settle ANTIC behaviour on physical Atari.

A potential hardware cause was identified: `basketball_hero.helper` clears and refills the active PMG after waiting for `$D40B >= 124`. In py65, for phases 60, 75 and 82, 4959, 4898 and 4870 CPU cycles respectively elapse from the first to the last PMG write (about 43 lines of 114 cycles); this covers the `$0980–$0BFF` range. It cannot be ruled out that the update happens while the upper part of the image is being displayed. py65 does not model ANTIC DMA, and the measurement is not proof of the artefact's cause.

A safe fix requires preparing the inactive PMG and the positions/colours, then publishing them in a bounded blanking window. In the dunk bank 52 B remain before the `$4B80` data and 192 B below `$7F40–$7FFF`; before any modification the ownership of these areas, the NMI, the sprites of both buffers and the publication timing must be taken into account. No code changes were made and no new XEX was built.
