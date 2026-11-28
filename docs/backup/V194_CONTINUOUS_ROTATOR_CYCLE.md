> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V194 — continuous rotator and tunnel cycle

## Found short fragment

After bar 112 (tick 41884) the dispatcher switched to the global 64-frame phase.
The clock was then at the end of the banana phase: frames 25–31 showed
bananas only until tick 41984, i.e. for 100 ticks / about 0.5 seconds.
Then the cycle moved on to the spiral tunnel.

## Correction

The start boundary of the global cycle was aligned to tick 41984 —
the beginning of the full tunnel phase. The organic tunnel runs through tick 41983,
and then the cycle resumes from the spiral tunnel. The rest of the v193 schedule,
including the full rotator 32909–35900 and the boy's entrance at 53850, is preserved.

The change concerns only the dispatcher tick. Graphics, effect animation
phases, renderers and memory allocation were not changed.

## Validation

`build/visual-prototype-v194.xex` and the matching JSON were built. The build has
298 shared rows and 2560 B of main code. 10 targeted tests of motif,
scene and finale boundaries pass; the test covers ticks 41884, 41983
and 41984. No full audio comparison or test on physical Atari was performed.
