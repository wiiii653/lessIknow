# V137 — rainbow ribbons and flying sparks

[READ] Four players change colours in a cycle of 16 shades. The existing four
music DLIs additionally call an unbanked palette helper **after** the decoder
tick has finished, only in scene 14. This gives wide rainbow bands along the
ribbons as well as changing hues over time. No DLIs or music ticks were added;
no scenes were shifted. The palette helper uses only the stack as temporary
memory and can be interrupted by the NMI without losing context.

[READ] Four missiles were already in use in v136. Their oscillating accents were
replaced with a stream of sparks: four phase-shifted births, upward motion with
deceleration, horizontal scatter and a short fading tail. The fifth player
colour also takes part in the cycle, at high brightness.

[READ] The choreography bitmaps and the size of the PMG tables did not change.
The double buffers of the PMG and bitmaps still protect the active image. 64
banks are preserved; the extra memory is code and small tables, with no
additional frames.

## Verification

[READ] The palette tests run the 6502 code for four bands and four clock phases,
with a selected video bank: they check all five colours, bank and stack
behaviour and the absence of writes to the image buffers. The spark test checks
the mask and position change with the dancer's pose stopped. The buffer
protection tests, the late raster and the music NMI also pass.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 113 088 identical bytes
against v035; the whole track. This is not a hardware listen nor a measurement
of the exact palette transition lines.

The preview `build/v137-rainbow-dance.gif` is a sequential execution of the
callback in py65 with an approximate palette and ideal DLI band positions. In
the emulator the band boundaries take the music decoder time into account; the
GIF does not model that latency, the DMA or the missed phases. The pose graphics
come from v136, with no new AI generation.

XEX: `build/visual-prototype-v137.xex`.

[READ] Full `make check`: 92 tests, 89 passed, 3 skipped because the archived
v126 is missing; 81.817 s. The working build is identical to v137. SHA-256:
`0b6a15875e0933d5cbc049058dcc86d9b285be0501c918e2e386e90c0e17324e`.
The additional code and tables occupy 496 B against v136 (381 B of unbanked
code/tables and 115 B in the scene controller).
