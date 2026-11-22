# V087 — dark plasma and raster title swap

The plasma has a maximum GTIA 11 brightness of 8. At the start it emerges from
the darkness with a spatial mask using ordered dithering. The smooth background
runs without interruption from the beginning to the end of the title screen, and
its phase is computed from the absolute music tick. Only just before the next
scene enters does the plasma fade out.

In the interval of 256 ticks around the boundary between the performer and the
title, eight masks swap the pixels of the letters TAME IMPALA for THE LESS in
raster fashion. The letters still differ from the background only in colour,
with no rectangular backing. Then the remaining lines of the title appear. Scene
boundary 1496 and school entry 2992 remain unchanged.

[READ] The py65 tests compare the resulting frames with the masks, examine PORTB
behaviour, the return from other scenes and the continuity of the background
pixels and brightness directly across the 1495/1496 boundary. [READ] Atari800
PAL, 1088XE, Altirra OS, stereo: the POKEY register dump was identical to v035
for 6 151 248 bytes after a single alignment of the start; the comparison covers
the whole track. [READ] In isolated py65 the frame rebuild takes about 53–130
thousand cycles, depending on the mask. [CONCLUSION] Longer rebuilds may miss
display phases; they require an evaluation of smoothness and a listen on Atari.
The effect uses 63 of the 64 banks of the 1 MB configuration.

The preview `build/visual-prototype-v087-preview.gif` reproduces the display list
with approximate colours and an assumed tempo; it is not an emulator recording.
XEX: `build/visual-prototype-v087.xex`; SHA-256
`1a6d43a84548950af90933327f2eb3935f6b9abf5bc69f9e158f60c48ccb9424`.
