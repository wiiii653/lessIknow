> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V094 — Trevor's punch combinations

In the part from bar 72 to bar 88 Trevor performs combinations synchronised
with the player tick. The first five punches are right, left, left, right,
left. The two-bar motif mixes punches on the beat and on the off-beat, so that the
intervals are 46–47 or 93–94 ticks. The wind-up shows the hand of the next punch,
including consecutive punches with the same hand. The first wind-up starts
32 ticks before entering the series. Act boundaries are preserved.

BANG takes the first 16 ticks of the punch, and the particles the next 16. The particle
starting point is shared with the BANG position. The tunnel phase is refreshed every 32 ticks,
but a pose change forces a refresh regardless of phase. The table of 96 punches and the
procedure fit in Trevor's existing banks.

[READ] 69 py65 tests passed, including tests of rhythm, hand
sequence, wind-up before the hit, particle start and direction, and PORTB.
[READ] Atari800 PAL, 1088XE, Altirra OS, stereo: after a single start
alignment the POKEY register log was identical to v035 for 5 968 512 bytes;
the comparison covers the whole track. [READ] In an isolated py65 test, rebuilding
a punch frame costs about 56k cycles. [CONCLUSION] The smoothness and readability
of the fastest combinations require evaluation in an emulator with a display or on Atari;
the POKEY comparison does not replace listening.

`build/visual-prototype-v094-knockout.gif` is a programmatic preview with
approximate colours and timing, not an emulator recording. XEX:
`build/visual-prototype-v094.xex`, SHA-256
`76faf0e3fd03749d6046856344339376a2c4a2e216e5369d4aaef8e05e110f72`.
