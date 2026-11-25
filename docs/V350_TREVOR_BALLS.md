> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v350 — slower incoming flight of Trevor's balls

The flight of each ball takes 48 instead of 32 ticks. The same 32-step path is
spread over a longer time; the hits, punch poses and BUM/BAM timings remain
at the existing music ticks. The first incoming flight begins the entry into the
action background 16 ticks earlier. The departures after the hit remain unchanged.

The table of 49 conversions is in bank 19 at `$7250–$7280`, after the panorama code
ending at `$7245`. The generator checks whether the occupied space is
empty. The flight code occupies 2041 B at `$6800–$6FF8`.

Stereo `build/visual-prototype-v350.xex` (1 115 783 B), SHA-256
`2ff0dff063ceedce22953b7c7d481cd875171ceb6f1340d901cdee3354a6eca1`.
Generator: 298 shared rows, 2542 B of main code. py65 tests
cover the incoming and outgoing flights of all punches, music interrupts, the PMG buffer,
the entry boundaries and the director. The emulator and physical Atari were not run.
The previously reported dunk table artifacts still require fixing.
