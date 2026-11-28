> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V271 — fixed early screen and bank diagnostics

## What was wrong

[READ] `tools/loading_screen.py` set `$D018=$00`. In ANTIC, the CHBASE field
then points to page `$0000`, and not to the font ROM at `$E000`. The ANTIC 2 screen
was therefore filled with empty characters: a black image without text.
The screen graphics, the display list and the INIT code were correct.

[READ] The same error is in `releases/avg-first-bank-diagnostic-001.xex`.
The black screen of that file is not a result of `BANK TEST FAILED`; it is the missing
visible font. One must not infer anything about the banks from it.

[READ] `less-i-know-release-v035.xex` and the Starfish remixes start on the
same Atari. This confirms the operation of the original player, its first
detection of 14 banks and the way AVG starts the XEX. It does not confirm
our additional loader of 50 video banks.

## The fix

`$D018=$E0` in `tools/loading_screen.py`. The rebuilt
`build/visual-prototype-dev.xex` differs from the previous one by **a single byte**
(`$00` → `$E0` at offset `$0D71`, INIT segment `$0780`). Full suite:
200/200 tests.

Release 011 (`releases/less-i-know-demo-release-011-avg-stereo.xex`) is created
from release 009 by `tools/build_avg_candidate.py` and contains the same fix.

## New diagnostic tools

- `tools/build_early_screen_diagnostic.py` →
  `releases/avg-early-screen-diagnostic-004.xex` (1.1 KiB). No banks and no
  player. If the Atari shows the text `EARLY SCREEN OK`, the early INIT, DMA
  and font ROM work in the AVG environment. The absence of the text points to the loading of
  INITs by AVG, not to the banks.
- `tools/build_first_bank_diagnostic_002.py` →
  `releases/avg-first-bank-diagnostic-004.xex` (2.7 KiB). It contains only
  the two original player segments (`$2000–$24B2`, `$24BD–$28BC`), without the music
  and graphics banks. It runs the original detection of 14 selectors and ends with
  the screen `BANK TEST PASSED` or `BANK TEST FAILED`. The screen and code lie
  at `$2B00–$2DFF`, outside all segments of this file.

Both screens set CHBASE=`$E0` and disable DMA only while writing.

## Limitations

- [READ] Copying version 1106 B instead of 2664 B to the card explains
  the earlier `EARLY SCREEN OK`; it is not a result of the bank test.
- [LIMITATION] No test was performed on AVG or on physical Rambo.
- [LIMITATION] The CHBASE error explains the black screen of the diagnostic, but does
  not prove the cause of the full demo not starting.
- [LIMITATION] Diagnostic 004 checks only the first 14 selectors.
  It does not test the 50 video banks or the copying of 16 KiB.
- A full start of the demo on the target machine remains unconfirmed.

## Test on Atari and the diagnostic conclusion

[READ] `avg-early-screen-diagnostic-004.xex` displayed `EARLY SCREEN OK`
on the target Atari. The early INIT, DMA and font ROM work in AVG.

[READ] `avg-first-bank-diagnostic-004.xex` showed `ORIGINAL V035 BANK
PROBE`, but without the result row. That variant did not contain the `$3300`
and `$3400` segments or the eight music banks, so it is not a reliable test of
the original detection; its missing result says nothing about the banks.

## New, standalone test of the 64-selector map

`tools/build_bank_map_diagnostic.py` →
`releases/avg-bank-map-diagnostic-001.xex` (473 B, 11 segments, without the player
and without banks). Each of the 64 selectors gets a unique marker in its bank
at `$4000`; the second loop checks whether no two selectors point to the same
bank. Result: `BANK MAP PASSED` or `BANK MAP FAILED`.

The 64 selectors in this test are **identical** to the set derived from
the working `rdc02-fws (2).xex`. The test does not depend on v035, the music or AVG.

- `PASSED`: the mapping of the 64 banks is available; look for the error in the copying
  and error handling of our loader, not in the selectors themselves.
- `FAILED`: one of the selectors points to the same bank; a hardware problem or
  a problem in the map assumptions.

[READ] py65 model: the map of 64 separate banks gives `PASSED`, and every
deliberate aliasing of two selectors gives `FAILED`. The first version of the test
had an error — the INIT page ended with a loop instead of `RTS`, so the probe did not
run; the fixed version is 466 B.

[READ] The next test on Atari: the INIT displayed `PROBING - PLEASE WAIT`, but
the result did not appear. `avg-first-bank-diagnostic-004` had the same symptom:
the INIT works, but the code under the RUN vector `$02E0` did not execute or crashed.

[READ] `releases/avg-bank-map-diagnostic-003.xex` (485 B) moves the WHOLE
probe into INIT — display, probing and result — so it does not depend on RUNAD.
It also does not read `$D301`; PORTB is write-only on real hardware, and reading
returns garbage. At the end it writes a constant `$FF` (the normal XL/XE state). py65
model: separate map → `BANK MAP PASSED`, alias → `BANK MAP FAILED`.

[CONCLUSION] If `003` shows a result and the full demo still does not start, the main
suspect becomes the RUN vector `$13E0` and its dependence on reading PORTB,
and not the bank map.

## Is the problem the too early use of ROM?

[CONCLUSION] No such error is visible. `less-i-know-release-v035.xex` reads the selector
table from `$2734/$2737`, but that is data from the XEX segment `$24BD–$28BC`
in RAM, not from ROM. The original detection sets `$D301=$FF` only in order
to restore the visibility of the OS, and it works on this Atari. Our additional loader
also keeps bit 0 of PORTB set during probing.

[CONCLUSION] In the `school_portrait_bank.loader()` code no error is visible in the selector
list: the 64 candidates are identical to those derived by the working
`rdc02-fws (2).xex`. Still open: the copying of 16 KiB, banks 0/1 counted
without verification and the silent `no_bank` loop (only a COLBK change, without text).
