> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V141 — taller text and the Gdansk Crane

[READ] Both sets of text have been raised. TAME/IMPALA start on lines
18 and 84 of the visible image. The three title rows start at 0, 48 and 96;
their faces and the extruded shadow end on source row 47.
The order of entries remains I KNOW → THE BETTER → THE LESS, and the final layout
is THE LESS / I KNOW / THE BETTER. The clock and the reveal moments were not changed.

[READ] The Crane is hand-drawn 13×15 GTIA-pixel artwork, starting at
column 34 and row 49 of an 80×64 source. Two towers, roofs, the central tall
timber section and the projecting crane housings stand out from their surroundings.
The night palette separates the cool towers, the warm timber structure and the windows.
The surrounding panorama was raised slightly; the text does not cover the top of the monument.

References: [National Maritime Museum — history of the Crane](https://nmm.pl/zuraw/historia-zurawia/),
[photo from the Motlawa side](https://www.earthtrekkers.com/wp-content/uploads/2018/07/Zuraw.jpg.optimal.jpg).
The photo was not copied into the bitmap — the drawing is produced in `tools/title_plasma.py`.

[READ] The city is part of the existing 16 plasma frames. Letter masks,
dissolve masks and PMG protection masks are regenerated for the taller layout. The number
of frames, table sizes and the allocation of 64 banks remain unchanged;
the change does not increase the Atari's memory requirements.

The tests check the order of entries in the raised layout, the separation of text
and shadows from the panorama, letter protection during dissolve, the inactive PMG buffer,
restart and the transition to school. The preview `build/v141-gdansk-intro.gif` comes
from sequential py65 callbacks; colour and pacing are approximate, without ANTIC DMA.

Release: `build/visual-prototype-v141.xex`.

[READ] Full `make check`: 100 tests, 97 passed, 3 skipped
due to the missing archival v126; 85.797 s. Atari800 PAL/1088XE,
Altirra OS, stereo POKEY: 14 639 760 identical bytes relative to v035,
the whole track. This is not a listening test on a physical Atari.

[READ] The XEX has the same number of bytes as v140: 1 109 022 B. The working build is
identical to v141. SHA-256:
`cbde55ed1cb77faf55cd54043119bdc7cfcba06cd14dedc806196927e124dba6`.
