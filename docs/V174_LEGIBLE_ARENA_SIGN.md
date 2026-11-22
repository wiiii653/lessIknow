# V174 — legible ATARI ARENA sign

The first shot of the boy in front of the arena had black blotches and
transparent fragments on the lettering. The source of the bug was a wide portrait
mask: it treated the black background of the source image as part of the boy and
overwrote the sign with it.

The mask now selects the coloured components of the figure and their black
outline, instead of filling the whole background polygon. The treble clefs and
notes were moved above the lettering so they do not darken the ATARI ARENA
letters.

- Preview of the composed frame: `build/v174-arena-sign-preview.png`.
- XEX: `build/visual-prototype-v174.xex`.
- 307 shared rows (limit 309), 2552 B of code.
- SHA-256: `f9576e668282b94ec598de5c04f55a0e50e578014c07fb09af471bb282979b12`.
- Ticks, scene boundaries and banked memory allocation unchanged.
- Built; no tests or emulator playback were run.
