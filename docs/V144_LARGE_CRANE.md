> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V144 — large historic Crane in the intro

[READ] The Crane is 40×32 GTIA pixels on an 80×64 grid; it starts at (20,32).
Its area is half the width and half the height of the active image
(a quarter of the area), instead of the former 13×15. Both screens have the same
silhouette: two rounded, brick towers, steep roofs, a tall wooden section
with an upper and a lower projecting eave, a water gate, a rope and a quay.

[READ] The drawing is defined by hand in `tools/title_plasma.py`,
without copying a photograph into the bitmap. References for the structure:

- [National Maritime Museum — historic photographs and description of the structure](https://nmm.pl/2022/04/04/gdanski-zuraw-na-czarno-bialych-zdjeciach-nielatwy-los-zabytkowego-dzwigu-portowego/).
- [Visit Gdansk — photograph from the Motlawa](https://kartaturysty.visitgdansk.com/res/10002/10019/fotka.jpg).

[READ] The colours are stage-like: turquoise/cyan towers with a brick rhythm,
warm red-orange roof tiles, dark wood with golden edges and a black outline.
The cool towers stand out against the plasma in the hue 2–7 range. GTIA 11
keeps the shared existing luminance and its fade; no raster brightness changes
or musical DLIs were added.

[READ] The titles occupy the upper half. TAME/IMPALA start at raster lines
0/48 and keep the doubled glyph rows. The title has a single glyph row
height: THE LESS / I KNOW / THE BETTER start at 0/33/66.
The letters and shadows end before source row 32. The order of entries
I KNOW → THE BETTER → THE LESS and the timings of reveal, crossfade and end
of the screens remain unchanged. No act boundaries were changed.

[READ] The firework masks take the whole Crane outline into account, including
the black wood and the black edges. Sprites and missiles do not cut through the
building. This is a change to host-generated data; the 6502 code and buffers
remain unchanged. Everything fits within the existing 16 plasma frames,
the existing title masks and PMG streams. Still 64 banks,
29 901 B of net recovery relative to v141 and 2560 B of main code.

Release: `build/visual-prototype-v144.xex` and JSON.
Previews: `build/v144-duzy-zuraw.gif`, `build/v144-zuraw-cards.png`.
The GIF runs successive py65 callbacks every 24 ticks. The palette and pace are
approximate; it is not an emulator recording or an ANTIC DMA FPS measurement.

## Validation

[READ] Final `make check`: 101 tests, 98 passed, 3 skipped
(missing archival v126), 81,864 s. The tests check the new building area,
no collision with the titles, protection of the silhouette against all PMG
phases, the order of word entries, safe buffers and the transition to further
scenes.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 12 213 216
identical bytes relative to v035, the whole tune. No listening and no test
on physical Atari. The v143/v144 comparison confirms a change in only seven
plasma/mask data banks (loader indices 40–44, 47–48); the remaining banks,
non-banked RAM and the code are identical.

[READ] The XEX is 1 109 100 B, the same as v143. SHA-256:
`8db4ca4de50c7db85d02732e416a9734b1ceab91a9e9e999c59e0e32fc828f21`.
The numbered release and the verified working build are identical byte for byte.
