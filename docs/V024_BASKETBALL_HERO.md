# v024 — BASKETBALL HERO

[READ] Act 3 replaces the placeholder in ticks 20944–23935.
Dribbling lasts 20944–22439, the dunk 22440–23935. Changes to earlier
acts and the start of Trevor (23936) keep their ticks. After 23936 the
kaleidoscope still runs as a placeholder for the next act.

## Image

[READ] Six illustrations: two dribbling poses and four dunk phases.
European comic, player in a cyan uniform with pink accents,
hall and low camera at the parquet. The illustrations contain no ball.
The ball, 16×32 logical pixels, consists of four players with rotated
seams and panels. Four missiles draw coloured droplets.
Dribbling has a period of 187 ticks, the dunk a single sequence across the whole sub-act.
On passing through the hoop there is a short flash of the lighting colour.

[READ] Source material:
`assets/art/source/act3_basketball_hero_v024.png`.
Conversion to six 160×56 frames; rows are repeated up to 192 lines.
Previews: `build/v024-dribble.gif`, `build/v024-dunk.gif`.

## V2 / V3 — memory

[READ] Bank 16 continues the detected PORTB table: in the tested configuration
bank 15 is `$AC`, bank 16 `$AE`. Runtime values stored at
`$24B3` and `$24B4`. The new INIT preserves PORTB and loads 16 KiB.
Code in bank 16: `$4000–$4779` (1914 B); six images of 2240 B each:
`$4B80–$7FFF`. The NMI preserves the foreground bank also while executing
code in bank 16. Buffers and lists stay in unbanked RAM.

[READ] The image is rebuilt when the pose changes. Holding updates
PMG, without copying the whole frame and rebuilding the list.
Leaving the act and restarting restore the dance scene PMG.
Main code is 1788 B, up to `$1AFB`; only 4 B remain before `$1B00`.
Subsequent acts require further moving of the dispatch into banks or
reworking of the code layout. Do not assume that the next bank can be obtained
by simply increasing PORTB to `$B0`; so far `$AC/$AE` have been checked.

## V1 / V6 — verification

[READ] 39 tests OK: act boundaries, all six poses and their pixels,
dribbling time, a single dunk, the flash, cache and PMG restoration.
Full stereo POKEY music identical to the original: 8 767 152 identical
bytes, about 2442.2 s of emulation.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v024.xex --seconds 12
```

[ASSUMPTION] The reference configuration is Atari800 PAL `-1088xe` with stereo
POKEY. Physical hardware and the other extension tables require checking.
The GIFs approximate PAL colours and pixel aspect ratios.

## Graphics — built-in image_gen

The imagegen skill and the built-in tool were used. Final prompt:

```text
Production illustration-story asset for Atari audiovisual demo. SIX equal landscape panels, EXACT 2 columns by 3 rows, edge-to-edge panels without gutters, labels or writing. Same teenage male basketball player in all panels, dark short hair, CYAN basketball uniform with pink trim, peach skin. EUROPEAN bande dessinee comic, realistic natural facial proportions, small eyes, bold thick black outlines, broad clean flat shapes, NOT manga/anime. School gym interior with roof beams, tall windows, wallbars, wooden parquet. Four colors only black #000000 hotpink #ff32a0 cyan #00dcff peach #ffbe96. NO gradients. Reference supplies world/palette only, make face more European. IMPORTANT: NO BALL DRAWN ANYWHERE, ball will be hardware animated later. Leave space just below or above open hands for the ball. Each panel readable at160x64 logical pixels, composed like a cinematic 2.5:1 view. Row1 left and right: SAME FIXED very low court-side camera, full player at left/center with body bent toward dribble, hand extended on his RIGHT toward empty space at x60percent and y60percent. Left is downstroke with bent knees, right is recovery with slightly straighter knees and raised right hand. Player entire body, parquet foreground, hoop far upper right. Keep architecture identical between this pair. Row2 left: dunk approach, NEW fixed low camera, basket and backboard upper right, player center-left crouches for jump, empty hands at chest height. Row2 right: SAME camera and basket, player airborne mid jump, right arm extended diagonally high toward rim, knees bent behind him, no ball. Row3 left: SAME camera/basket, player at apex beside basket, right open hand immediately above rim upperright, ready to slam ball, left hand stretched back for balance. Row3 right: alternate follow-through dunk pose with one hand gripping rim and legs below. Realistic basketball anatomy and strong silhouettes. Gym lights visible as simple peach ceiling fixtures. Keep hoop in same location for last four panels. No text, no basketball in image, no decorative particles, no extra foreground players.
```

[READ] Additionally, 24 further memory dumps were checked in Atari800:
earlier scenes, entering act 3, dribbling and holding it,
four dunk phases, the flash, the last tick of the act, exit and restart.
All compared rasters match the source.
