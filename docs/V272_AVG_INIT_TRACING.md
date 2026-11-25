> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V272 — tracing the INITs of the full demo

[USER READ] The RUNAD test showed INIT OK and RUN OK. The RUN vector itself
works; the missing result of the earlier diagnostics did not prove its failure.

`releases/avg-full-demo-init-trace-001.xex` instruments the 66 INITs of the full
stereo 011 version. It shows the number, address and ENTER before the call and
RETURN after the return. The wrapper preserves A/X/Y and the flags. The temporary $1200
is overwritten by the final segments of the runtime image as in the source.
The list of stages: the matching `.stages.txt` file. This file serves diagnostics,
it does not replace the production release. Operation on AVG was not confirmed.

Note on the earlier report: CHBASE is at $D409, and $D018 is COLPF2.
Changing $D018 does not change the font address; the erroneous comment in the source was corrected.

[READ] Atari800 PAL/1088XE, Altirra OS: the whole track, 15 965 064
identical stereo POKEY bytes relative to v035. This is an emulator regression check,
not a confirmation of the behaviour of the physical AVG loader.
