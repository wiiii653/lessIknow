# Opening terminal and title reflection

[Loader and opening text](terminal_opening.md) transcribes both screens.
[Project Status](PLAN_STATUS.md) records the current build and the evidence
for numbered prereleases.

## Cold start

The full-rate AVG loader animates the star during loading. Its last INIT
wrapper restores the OS VBI and shuts off ANTIC DMA before later payloads
overwrite loader assets. The final `$4800` bootstrap restores low RAM and
jumps to the runtime entry at `$13E0`. The run stub clears the second
framebuffer with DMA disabled, then enters the silent opening terminal.

[terminal_opening.py](../tools/terminal_opening.py) reconstructs the star
using the 32 existing poses and types two pages below it. The interlude
counts PAL blanking edges before the music player starts. Page two begins
at frame 144, the fade starts at frame 288, and the handoff follows frame
319. The cleanup helper at `$FD92` blanks the display, clears the startup
scratch in `$9000–$9BFF`, and jumps to the player entry at `$2146`.
SELECT restarts the scored sequence from the title rather than replaying
the cold-start interlude.

The opening text has its own three-ink palettes and fades. The later
main-act brightness change applies to the captions after the title.

## Scored opening

The plasma starts at player tick 0. Fireworks begin at tick 768. The city
and water reveal together from tick 1024, the song title takes over at
tick 1496, and school starts at tick 2992. The water renderer samples the
live plasma before the skyline is drawn, then adds narrow reflections
from the composited city.

The inactive title framebuffer holds 440 bytes of water at offset `$0B00`
and a 103-byte display-list tail at offset `$0D00`. Water occupies relative
scanlines 201–233. The last music DLI stays on line 234. The renderer
publishes the picture and water together, restores the regular footer at
the school handoff, and leaves the [main-act terminal](TERMINAL_MAIN_ACTS_IMPLEMENTATION.md)
to publish its own footer.

## Regression checks

The startup check in `tests/test_sequence.py` covers framebuffer clearing,
star phases, page changes, fade and player handoff. The title tests cover
reveal and PMG fireworks behavior. For hardware changes, use the
[loader contract](HARDWARE_LOADER_CONTRACT.md) and record the exact artifact
and setup. The [original opening brief](TERMINAL_OPENING_BRIEF.md) records
the earlier design.
