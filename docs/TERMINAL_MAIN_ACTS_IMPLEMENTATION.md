# Four-row terminal across the main acts

[main_act_terminal.py](../tools/main_act_terminal.py) types ten pages of
40-column ANTIC 4 text. The strip sits below the full 192-scanline picture
from school through the post-Trevor montage. Each finished page stays
visible until the next cue. See [current captions](main_act_terminal.md)
for the screen copy.

## Display and palette

The normal display lists at `$8000` and `$8400` jump to separate tails
while captions are active. Relative scanlines 201–202 provide the gap
before four eight-scanline text rows at 203–234. The gap DLI applies three
fixed caption inks, and the top split restores the scene inks from RAM.
The four music events stay on relative lines 0, 78, 156 and 234.

The current palettes retain each act's hues and lower each GTIA luminance
value by 6, which is three even luminance steps. The brightness change is
limited to the ten main-act pages. The cold-start opening has its own
palette and fade, and the credits sequence uses its animated rainbow
palette through the greetings.

## Allocation and publication

The strip font is at `$D800`, its two screens start at `$DA20` and `$DB20`,
and its writer starts at `$DC00`. The training renderer still uses the two
legacy framebuffer maps at descriptor indices 2 and 3. Their shared low
bytes are at `$D960`, with high bytes at `$E180` and `$FDC8`. The allocator
checks these ranges alongside the caption and runtime data.

The foreground prepares the inactive caption screen and the final music
interrupt publishes it during bounded early blanking. If the interrupt
misses the publication window, the old screen stays visible until the next
commit. The normal footer is restored for credits or restart.

## Caption cues

| Page | Player tick | Act |
|---|---:|---|
| 01 | 2,992 | School arrival |
| 02 | 5,984 | Basketball practice |
| 03 | 8,975 | First side-dancer sequence |
| 04 | 11,967 | Early tunnels and rotators |
| 05 | 14,959 | Ribbon dance |
| 06 | 20,942 | Tunnel cutaway |
| 07 | 21,690 | Basketball hero |
| 08 | 23,934 | Trevor fight |
| 09 | 29,656 | Post-Trevor montage |
| 10 | 38,705 | Bananas leading into the eye sequence |
| Credits handoff | 41,884 | Boy portrait and credits terminal |

The eyes themselves enter at tick 39,379. The caption cues come from
`CUES` in the source. See the [timeline](TIMELINE_MAP.md) for the scored
scene ranges.

## Regression checks

`tests/test_main_act_terminal.py` exercises all ten cues, the palette
split, blanking deferral, double buffering, training framebuffer maps and
the credits handoff. It checks that caption palette interrupts leave the
music clock unchanged. See [Project Status](PLAN_STATUS.md) for which
artifacts have been tested. The [terminal text plan](TERMINAL_TEXT_PLAN.md)
preserves the earlier draft copy.
