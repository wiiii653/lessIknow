# v349 — smoother BUM/BAM on the eight

After the eyes, the cycle on the bananas lasts 94 ticks: a small empty bubble brightens,
expands into the BUM or BAM text, after 48 ticks four satellites scatter
to the sides, the bubble gradually shrinks, and from tick 79 to 86 the whole thing goes dark. For the
last eight ticks it is empty. The eight's movement uses the music clock, not
the rotator frame; the tables in Trevor's banks occupy `$6900–$693F`.

Stereo build `build/visual-prototype-v349.xex` (1 115 783 B), SHA-256
`72294e6a35a018a0f6db6fcc549bc3a5e233f25c4ad9f80d580a3a8f0712671a`.
Generator: 298 shared rows and 2542 B of main code. Six
director tests and nine Trevor effect tests passed in py65. Checked the stages,
brightness levels, four satellites, writing only to inactive PMG,
PORTB and path range. No emulator or physical Atari was run. The artifact
of the input table is still unresolved: [audit](AUDIT_DUNK_PMG_V347.md).
