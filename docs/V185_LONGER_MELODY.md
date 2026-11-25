> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V185 — earlier whistle and longer-visible notes

The whistle starts at tick 4862, after the shot of the boy passing in the
foreground (4488). The pose with the beak and the flying notes remain active in
scenes 10–12, until the start of the exercises at tick 5984. The whole melody is
visible for about 5.6 s, instead of 2.3 s in v184. The start falls about 3.3 s
earlier.

The girl still moves away along the path to the door in the existing scales.
Her last position again starts at the original tick 5610,
regardless of the start of the whistle. The boy first looks straight ahead,
at 4488 he looks back at her, and only at 4862 does he start whistling.

One flight phase now lasts eight ticks instead of four. A single note
rises for about 2.56 s. Over the whole shot the phase does not wrap the 8-bit
clock, so successive notes do not disappear when the emission delay is counted
again. PMG buffering and the missile trails are preserved.

## Build and verification

- `build/visual-prototype-v185.xex` and JSON; dev identical.
- SHA-256: `5df7b3c2d811ac8cd9c33da8737428269d1c524d78ba73fbe0b791382e56760d`.
- 316 rows, 12 174 B of row data, 2552 B of main code.
- PMG helper 839 B at $6A00–$6D46 of loader bank 0; no new banks.
- 14 tests passed: emission, flight time and direction, continuity in scenes
  10–12, behavior at the boundary of the former clock wrap, PMG buffers,
  disable at 5984, masks, v175 panorama, composition and ball regressions.
- `build/v185-whistle.gif` shows the whole melody after the 6502 callbacks have
  run. It does not model ANTIC DMA. No new emulator or hardware validation
  was performed.
