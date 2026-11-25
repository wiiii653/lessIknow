> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V222 — typing terminal with cursor and Enters

Credits and greetz appear character by character. The green block cursor blinks
directly after the last typed character. After a short pause the next line
begins (`Enter`). Greetz scroll the history only after five lines are filled;
previous lines are not rewritten from the beginning. The cursor
stays on the last line until the next one begins. The text wave, the boy's fixed
lower position and the end of the captions at 59085 are preserved.

The timing of successive lines is stored in player ticks: a gap of 112 ticks
in the credits and 96 ticks in greetz. One character is typed every 2 ticks.
The credits headings remain in the windows 53850 / 54847 / 55844 / 56842.
Act and music boundaries were not shifted. No keyboard sounds were added.

## Memory and sources

- `tools/terminal_typing.py`: 156 B of code at `$EB44–$EBDF`, in the intro
  helper reserve enlarged by 32 B (1824 B). The existing intro effect code did
  not change; the shared row pool was shifted by 32 B.
- The 88 B schedule at `$23CE` and the 43 B lengths at `$2426` use the
  unused code of the old UI. Its entry `$23CD` now contains RTS.
  The main UI callback was already replaced in older releases.
- `$2D00–$2D26`, the old font initializer with the `$218F` call disabled,
  holds part of the packed stream. The old UI/font must not be re-enabled
  without restoring its code and changing the allocation.
- Terminal screen: `$BF00–$BFC7`, in the freed second bitmap buffer.
  Cursor `$A0` is inverse-space ANTIC 2, independent of the PMG around the head.
- `$0DD8`: working number of revealed characters. The code preserves X (line
  number) and passes the line address through the existing `$0DD3–$0DD4`.
- No new extension banks were used. Memory collision checks pass.

## Validation

[READ] V221: full set of 158 tests — OK, 113.2 s.
[READ] V222 after refining line lengths and the cursor: 44 tests of the terminal,
scenes, PMG, budgets and regressions — OK, 18.6 s.
[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 518 128
identical bytes relative to v035, the whole track. This is not a trial on
physical Atari.

Build: `build/visual-prototype-v222.xex`.
Animated CPU/ANTIC reconstruction preview: `build/terminal-v222.gif`.
Static preview: `build/terminal-v222-preview.png`.
