# Four-row terminal across the main acts

[main_act_terminal.py](../tools/main_act_terminal.py) types a continuous
40-column one-color ANTIC C log below the full 192-scanline picture. The bottom row
types at one character every four PAL frames. The cursor blinks while
typing and during pauses. Each Enter scrolls the three most recent lines
up and starts a new bottom row. See [current captions](main_act_terminal.md).

## Display and palette

The normal display lists at `$8000` and `$8400` jump to separate tails
while captions are active. Relative scanlines 201–202 provide the gap
before four eight-scanline text rows at 203–234. Each text row begins with
a blank scanline and uses seven 20-byte one-bit bitmap scanlines. The gap
DLI applies the published terminal ink to PF0. The top split restores the
scene's PF0 from RAM. At a scene cut, the terminal eases to the next ink
over about 0.6 seconds. The current text and typing position carry through
the cut.
The four music events stay on relative lines 0, 78, 156 and 234.

The main act uses the first ink from each previous dimmed palette. The
cold-start opening has its own palette and fade. The credits and greetings
use their animated rainbow ANTIC 4 text.

## Allocation and publication

The two bitmap pages use eight 140-byte slots at `$D800`, `$DA20`,
`$DB20` and `$DC00–$DEBB`. The total is 1,120 bytes of unbanked bitmap
storage. The display-list tails are at `$DF6D` and `$DAEB`. The transcript,
glyphs, palette ramps and foreground writer live in the final Atari Arena
panorama bank. The build validates these allocations against the existing
bitmap, scanline and practice framebuffer tables.

The foreground prepares the inactive caption screen and the final music
interrupt publishes it during bounded early blanking. If the interrupt
misses the publication window, the old screen stays visible until the next
commit. A palette-only update publishes without swapping the bitmap pages.
Each page caches the transcript line and character count in each slot.
Typing and cursor changes update the affected character pairs. Enter
rotates the display-list pointers and reuses completed rows. A seek
rebuilds any slots that need different contents.
The normal footer is restored for credits or restart.

## Palette cues

| Palette | Player tick | Act |
|---|---:|---|
| 01 | 2,992 | Atari Arena arrival |
| 02 | 5,984 | Basketball practice |
| 03 | 8,975 | First side-dancer sequence |
| 04 | 11,967 | Early tunnels and rotators |
| 05 | 14,959 | Ribbon dance |
| 06 | 20,942 | Tunnel cutaway |
| 07 | 21,690 | Basketball hero |
| 08 | 23,934 | Trevor fight |
| 09 | 29,656 | Post-Trevor montage |
| 10 | 38,705 | Bananas leading into the eye sequence |
| Credits preparation | 41,804 | Retire the main terminal and prepare the closing portrait |
| Credits handoff | 41,876 | First visible portrait and credits terminal in the Atari800 trace |

The palette cues come from `CUES` in the source. Each entry in `CAPTIONS`
has a music-clock window for the action it describes. Typing starts on the
first PAL frame at least three frames into that window. The builder checks
that the full line fits before the action ends and leaves at least 48 ticks
before the next line starts. Short moments such as the backboard crack use
short entries. Practice cues follow the close-up, shot at the hoop, then
wall-bar stretches. The first tunnel rotation changes have short cues for
the actual spiral or organic view, and the lift has its own cue when the
trio starts the launch. Completed lines scroll across scene cuts. See the
[timeline](TIMELINE_MAP.md) for the scene ranges.

## Regression checks

`tests/test_main_act_terminal.py` exercises all ten cues, the palette
split, blanking deferral, double buffering, training framebuffer maps and
the credits handoff. It checks that caption palette interrupts leave the
music clock unchanged. See [Project Status](PLAN_STATUS.md) for which
artifacts have been tested. The [terminal text plan](backup/TERMINAL_TEXT_PLAN.md)
preserves the earlier draft copy.
