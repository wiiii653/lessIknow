> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V198 — rainbow object colours in the finale

The stars, notes and treble clef orbiting around the head get a vivid, cyclic
palette of 19 GTIA colours. The four objects have shifted phases, so the colours
flow independently through the full spectrum. The palette works together with the existing
fade-out.

Only the palette bytes changed: 19 B in the data of bank 49. The orbit, the rhythm
of toggling the stars and notes, the PMG masks, the bitmap, the fade-out and the code remain
as in v197. Build: `build/visual-prototype-v198.xex`, the dev pair updated.

[READ] Ten finale tests pass. The palette test checks the full 19
colours, at least 16 shades and correct brightness for applying the fade.
