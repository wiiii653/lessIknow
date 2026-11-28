> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V086 — full-screen title plasma

In the GTIA 11 opening the plasma fills the whole screen; the letters are part
of the same image and differ from their surroundings in hue. The motion comes
from 16 frames of overlapping radial waves. Successive text rows are overlaid
through a hue-shifting mask, without black panels. Spatial masks fade the
effect unevenly, and brightness reaches zero before the screen boundaries.
The boundaries and ticks are unchanged.

The frames are 80×64; ANTIC shows each row three times. Code under the system
ROM combines phase and mask in the inactive buffer; the plasma code and data
occupy seven additional extension banks. In total 61 banks of the 1 MB
configuration are used. The music NMI restores PORTB; after composing a frame
the program restores the previous bank. The dance buffers are marked as
requiring a reload.

[READ] 64 tests run with py65 passed, including a comparison of the resulting
pixels against the phases, the letter and fade masks, and a test of the return
to the intro.
[READ] Atari800 PAL, 1088XE, Altirra OS, stereo: after a single alignment of
the start, the POKEY register recording was identical to the original for
5 837 112 bytes; the comparison covers the whole track. [READ] In an isolated
py65 test, rebuilding a phase takes about 53–130 thousand 6502 cycles; phases
change every 32 ticks, but the cost may cause phases to be skipped on target
hardware.
[CONCLUSION] The POKEY results do not replace listening or an assessment of
smoothness on real Atari.

`build/visual-prototype-v086-preview.gif` is a display-list preview and has
approximate colours; it is not an emulator recording. The XEX has SHA-256
`af2080e95c3daa7459b6df17a92266850b223dcd7f0896679d269406ac24f7a0`.
