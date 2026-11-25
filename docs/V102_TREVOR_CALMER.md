> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V102 — more readable Trevor hits

The tempo of the scene was reduced: the combination keeps the order right,
left, left, right, left, but the intervals are 140–141 or 187 ticks. BANG and
the flash last 48 ticks, and the particles another 48; together three times
longer than in v100. Between the hits the wind-up of the actual hand is visible.
The particle start point is still tied to the BANG position. Act boundaries were
not changed.

A detected tunnel phase jump before the first punch was removed: the wind-up
uses the bank of the same animated phase as the rest of the scene, instead of a
brief return to phase zero. The brightness of the second entry screen and the
hall neon, Trevor's outline, the tunnel flashes and the thickness of the BANG
letters were refined. The additions fit within existing banks and do not change
the number of expansion banks.

[READ] 71 py65 tests passed, including tests of the first wind-up phase, tempo,
pose, effect lengths, particle direction and PMG restoration after a scene
change. [READ] Atari800 PAL, 1088XE, Altirra OS, stereo: after a single alignment
of the start the POKEY register dump was identical to v035 for 5,834,736 bytes;
the comparison covers the whole song. [CONCLUSION] An assessment of image
smoothness and listening on the target Atari are still needed; the POKEY test
does not visually confirm the cause of every observed frame fault.

`build/visual-prototype-v102-trevor.gif` is a software preview of the scene with
approximate colours and tempo, not an emulator recording. XEX:
`build/visual-prototype-v102.xex`; SHA-256
`a749d448bb54b516c1e3efa84cddac72ad7aa9d7e0ca2b47fda90f8ffd005efa`.
