> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V090 — wind-up before every punch

Trevor raises the arm he is about to strike with: a mirrored frame of that arm
was added to the existing wind-up pose, matched to the mirrored punch frame.
In the first phases of the punch the figure also makes a slight movement
towards the fist, which strengthens the impression of a thrust. The impact
timings, BANG and the start of the splash remain as in v089.

In the 16 tunnel-phase banks, the place of the copy of the first intro screen
is now taken by the new wind-up frame; both calm-intro images and the restoring
code were placed in the last free extension bank. The demo uses all 64 16 KiB
banks of the 1 MB configuration. The control code restores PORTB after every
scene and after the music interrupt.

[READ] 68 py65 tests passed, including verification of the correct wind-up
immediately before four consecutive punches, the impact poses, the splash, bank
switching and the return to the remaining scenes.
[READ] Atari800 PAL, 1088XE, Altirra OS, stereo: after a single alignment of
the start, the POKEY register recording was identical to v035 for 6 193 728
bytes; the comparison covers the whole track. [CONCLUSION] This does not replace
a separate listening test or an assessment of smoothness on real Atari.

`build/visual-prototype-v090-trevor.gif` is a software preview of the display
list and PMG with approximate colours and timing. XEX: `build/visual-prototype-v090.xex`;
SHA-256 `350e90212aca6a970dbd41676c993c0b0e809e68ec6c4d6b752a61dd289eabc3`.
