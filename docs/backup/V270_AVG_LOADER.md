> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V270 — earlier loading screen and AVG diagnostics

The user reported a missing lettering when starting from AVG, on an Atari with 1088 Rambo.
In v269 the screen appeared only after the first INIT of the original player.
This INIT detects 14 banks before returning and does not return on failure.
The missing lettering is therefore consistent with a halt on that path, but does not prove it.

The release 010 variants initialise the same screen before the first INIT, keep
DMA in the initial attempt and, after a failure of that attempt, display BANK TEST FAILED.
A separate small XEX `avg-first-bank-diagnostic-001.xex` checks only that
first attempt and ends with a BANK TEST PASSED or BANK TEST FAILED screen.
It does not check the remaining 50 banks or the whole demo loader.

[READ] The CPU model ran both diagnostic paths: 14 separated
banks gives PASSED, aliased memory gives FAILED. Seven rotator tests
on the v270 stereo XEX passed. Atari800 PAL/1088XE, Altirra OS: 15 795 144
identical bytes of stereo POKEY relative to v035, the whole track.

[LIMITATION] No AVG and physical Rambo test. The early lettering and message
narrow the diagnosis; they are not proof that the reported startup failure has been fixed.
