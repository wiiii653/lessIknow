> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V089 — alternating Trevor punches

In the punch scene an opposite fist pose was added, created by mirroring the
silhouette and graphics of the existing punch. Successive punches switch the
fist; the existing preparation pose is used between them. The flashes keep the
previous 512-tick cycle and the scene boundaries. At the tunnel edges, moving
glints were added and the width of its coloured bands was refined.

BANG and the four particles use a shared position offset. The particles start
near the centre of the flash and spread to the left and right, also after the
hand changes. The additional frame occupies `$7400–$7DFF` in the existing
Trevor phase bank; it does not require another expansion bank.

[READ] 66 py65 tests passed. The tests cover the alternation of poses, the
preserved punch timings, all BANG positions, the start and direction of the
particles, and the PMG restoration when returning to the dance. [READ] Atari800
PAL, 1088XE, Altirra OS, stereo: 6 127 344 POKEY register bytes identical to
v035 after a single alignment of the start; the comparison covers the entire
track. [CONCLUSION] The comparison does not replace a listening test or an
assessment of smoothness on hardware.

`build/visual-prototype-v089-trevor.gif` is a software preview of the display
list and PMG, with approximate colours, and not an emulator recording. XEX:
`build/visual-prototype-v089.xex`, SHA-256
`e1e693aacfe8fc4d5d7f4f490d987cbdb0c5cb375bf2c6fac397a59facd8bf7c`.
