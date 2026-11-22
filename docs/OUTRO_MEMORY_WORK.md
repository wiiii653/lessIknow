# Credits / greetz — memory reconnaissance

Historical status: preliminary reconnaissance. The implementation has been
connected since v216; current description: `V216_CREDITS_GREETZ.md`. Do not use
the experimental v199 as a release. v198 remains the reference point.

## Readings

- `$C000–$CEFF` belongs to the second bitmap buffer `$B000–$CEFF`.
  Static resources must not be installed there before the earlier scenes are
  replayed.
- Gaps identified outside the current scanline pool allocation and the v035
  segments: `$28BD–$28FF`, `$2940–$29FF`, `$2A65–$2BFF`, `$2C81–$2CFF`,
  `$2D27–$2DFF`, `$2F7F–$2FFF`, `$307F–$30FF`, `$3135–$317F`,
  `$31A4–$31EF`, `$31F1–$32FF`, `$3E58–$3FFF`.
  Total capacity: 2118 B.
- [READ] `audit_music_banks.trace` with the above ranges as
  `protected_ranges` performed decoder initialisation and the whole stream up
  to tick 59833. There was no music read or write in the protected ranges.
- This does not yet confirm the safety of all player start-up routines or
  visual operation on Atari.

## Further implementation

Verify the start-up routines and pack the text resources together with a small
loader into the verified gaps. After the scene of the lying boy begins, settle
the bitmap into one buffer; use the other for the unpacked font and the
captions. Earlier scenes must still have both full buffers. Preserve 53850 /
56842 / 59085 and the existing PMG. No reservations in extension banks have
been allocated.
