# V242 — stable lower frame without restoring the older display list

After moving the outro in v240 to 51850, the guard in `title_plasma.invalidate`
still compared the tick with the old hard-coded 53850. It treated every subsequent
call during the first 2000 ticks of the ending as a backward seek.
It restored the normal lists, published $8400, and the terminal republished
$BC00. Although the final callback state was correct, between publications
ANTIC could see a higher frame. Hence the flicker/two character positions.

The guard now takes both parts of the boundary from `outro_text.START`. In the current
outro it does not trigger a reset, and a real seek before 51850 still restores
the normal lists for earlier scenes. Graphics, PMG position, terminal start and end,
palettes and music remain preserved.

A new regression tracks writes on successive callbacks from 51854 to 53870:
after the first publication it must not write $D403 or restore the normal
DL $8000/$8400; the terminal state must remain 2, and the lower bitmap map constant.
The test **reproduces the bug on v241 already at 51854** and passes on v242.
Earlier tests checked the state after the callback, which did not detect a momentary
switch to the old list and back before the end of the call.

[READ] 23 targeted tests passed, including the new regression, terminal,
PMG publication, character position, finale and fade.

[READ] Full regression: **185/185 tests**, without skips, 122.9 s.
Atari800 PAL/1088XE, whole track stereo: **10 731 888 bytes identical
to v035**. Without a test on physical Atari. The XEX differs from v241 by exactly
two bytes, keeps its size; the working build updated to v242.
