> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V187 — large, clear PMG notes

Previous glyphs were only 8 logical pixels wide, and their
brightness decreased over a significant part of the flight. On the colorful arena they were too small
and not legible enough.

V187 doubles both dimensions: the players are 16 logical pixels wide,
and the glyphs are drawn in 24 double PMG rows, up to 48 screen lines.
That is four times the glyph area. Brightness 14 is maintained through
33 of the 36 flight phases; only the last three phases dim the glyph. The rainbow
colors are interleaved with white flashes. SIZEM=$55 widens the detached missile trails.

The larger notes move away from the face faster, and the four arcs spread wider
across the sky. The start of the path was corrected so that the enlarged
glyph emerges from in front of the lips instead of covering the face. The beak and the first note
still start at 4862, and the whole thing ends when the girl reaches the door
at 5610. Frames, characters, scales and the girl's path remain from v186.

## Result and verification

- `build/visual-prototype-v187.xex` and JSON; dev identical.
- SHA-256: `1491ff54537d31dfdd8b6999269cd850d3c0321f393827ac8de2a30d7b221a27`.
- PMG helper 1167 B at $6A00–$6E8E of loader bank 0; 113 B remains
  to cleanup $6F00. No new bank; main 2552 B, 298 rows / 11 480 B.
- 16 CPU/graphics tests passed. The new regression checks the hardware
  width doubling, the actual number of lit rows, brightness 14
  and the widened missiles; the others check synchronization, paths,
  fading at the door, buffers, masks and the unchanged v175 walk.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 221 456 identical
  bytes relative to v035; the whole track. AppImage mode
  `APPIMAGE_EXTRACT_AND_RUN=1`, after 20 s of host time for the recording.
- Only loader bank 0 changed; the remaining 63 banks are identical
  byte for byte with v186.
- `build/v187-whistle.gif` and `build/v187-whistle-preview.png`: previews
  after executing the 6502 callbacks, with PMG, without ANTIC DMA modeling.
- The full suite was not repeated after this size and color change.
  The last result (v186) and the 10 earlier failing tests are
  described in `V186_CLOSED_MEETING_SCENE.md`.
