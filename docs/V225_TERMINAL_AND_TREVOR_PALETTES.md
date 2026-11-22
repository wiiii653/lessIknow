# V225 — terminal palette with DLI and Trevor's entrance

## Terminal

The cause of the flicker was COLPF2 writes by the foreground, dependent on the
drawing time of the text and PMG. ANTIC 2 shared the background/character hue
with the skin color of the bitmap. VCOUNT/WSYNC polling was removed from the
text renderer.

The terminal now uses ANTIC 4: letters are drawn in the COLPF0 color, and empty
pixels and the surroundings have a true COLBK `$00`. The new 3×7 terminal font
fits 40 columns. The cursor `$5F` is a full block in the same green
color. There is no green background/band or green frame.

The display list marks the last text row as `$C4`, adding a DLI after
line 41. The NMI router `$2451–$248F` (63 B) sets the green
letters at the first DLI and restores the bitmap color at the additional DLI.
The additional DLI does not start the music decoder: it pops the JSR return
address, restores Y/X/A and executes RTI. It does not switch banks. The four
music DLIs remain at lines 1/79/157/235, i.e. every 78 lines. COLPF1 and COLPF2
are not changed by the terminal; the skin color remains under the control of the
character renderer.

The router occupies the further part of the disabled old UI/font code. The old
UI/font must not be restored without changing its memory ownership. Text
package: 1691 B, loader: 351 B. No new banks.

## Trevor

Both entrance shots have the basic palette from the beating:
COLPF0 `$48`, COLPF1 `$68`, skin `$2A`. The dimming of the first
shot and the different skin hue of the second shot were removed. The animation,
timing and palettes of the blows themselves are preserved. NOPs keep the size
and position of the helper.

## Verification

[READ] V223 (terminal change): 158/158 tests, 114.6 s.
[READ] V225 (terminal, font and entrance palette): 47 tests of scenes, NMI,
terminal, colors, boundaries and regressions — OK, 18.8 s. The additional NMI
test checks the unchanged music counter, the bank register and the skin color.
[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 329 632 identical
bytes relative to v035, whole track. No attempt on physical Atari.

Build: `build/visual-prototype-v225.xex`.
CPU/ANTIC preview reconstruction: `build/terminal-v225-preview.png`.
