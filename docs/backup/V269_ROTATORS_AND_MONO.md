> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V269 — longer reverses and one POKEY

The edit after Trevor uses longer, essentially two-bar runs,
preserving the phase when changing direction. The organic tunnel has 12 phases;
the eye slots remain separate. Scene and music boundaries remain unchanged.

The mono version disables writes to the second POKEY in the original player;
it preserves the four voices of the first chip. This is not a reduction from eight
voices to four. `tools/make_mono.py` checks the addresses before substitution.

[READ] Atari800 PAL/1088XE, Altirra OS: 15 431 472 identical bytes
of stereo relative to v035. Mono compared with the stereo variant: 840 776 samples
of the first POKEY without differences, the second register set zero.
[READ] Full suite: 200 tests passed.

[LIMITATION] No test on physical Atari. The reported startup problem on
1 MB was neither diagnosed nor fixed. The loader stops when it
cannot find a bank; details of the expansion and loader are needed.
