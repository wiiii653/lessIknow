# Protecting the baseline before the credits

- The allocation check now covers `$9000–$AEFF` and `$B000–$CEFF`.
  The static block below `$C000` is rejected before the file is created.
- The `quarter_at` model respects the half-step gate present in the working
  6502 selector. Neither the selector nor the playback timings in the XEX were
  changed. The previously reported "quarter" is selected from the half-step in
  the current playback; this describes the state, not a fix to the animation
  dynamics.
- The tests cover all streams sharing banks 32–35 and the actual placement of
  the additional four streams behind the data of those same banks.
- CPU regression limit for scenes 10–11: 25000 cycles against a measurement of
  23954. This is a CPU regression threshold with less than 5% headroom, not a
  guarantee of a frame with ANTIC DMA.
- Comparisons between releases rely on the available v198. They check
  bitmaps, both PMG buffers, GTIA registers, PORTB restores and callback cost.
- [READ] The build `/tmp/visual-prototype-memory-guard.xex` is byte-for-byte
  identical to the archived v198 (`cmp`).
- [READ] Two memory collision tests and three comparisons with v198 pass.

Credits/greetz are still not connected; do not release the experimental v199.
- [READ] Full run: 149 tests, zero failures, 3 historical skips of
  comparisons with v126 (106.5 s). After those comparisons were replaced with
  three v198 tests, their separate run also succeeded; the two new collision
  check tests passed separately.
