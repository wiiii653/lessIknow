# V192 — U from an inverted A

The U glyph in BUM is computed from the actual A used in BAM:
vertical inversion and replacement of the crossbar row with side strokes.
U logical rows: CC CC CC CC CC CC 78. The PMG row doubling,
cell width and title position remain as in v191.

- `build/visual-prototype-v192.xex` and JSON; dev identical.
- SHA-256: `c6e8921b7fc3f12ec7a92c380da8e48e9371e7eb668b3c41b30e377783cb1cfa`.
- 12 tests passed: inversion of A and absence of the crossbar also in the actual
  PMG data, BUM/BAM centring, scatter at the fists and bubble animation.
  Log: `build/v192-focused-check.log`.
- No change to Atari code, bank allocation or synchronisation. No new
  music comparison or full suite was run after changing a single glyph.
