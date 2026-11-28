> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V253 — caption during loading

[READ] After the first initialisation of the original player, before its
first music bank, the XEX creates an ANTIC 2 text screen:

```
NOW LOADING ATARI XE DEMO
SILLY VENTURE 2026 WE
OGNJEN 2026
```

Screen data `$0600–$0677`, display list `$0700–$070A`, initialisation
`$0780–$07BC`; the areas are temporary and are later overwritten by the OS RAM
loader. The registers and their OS shadows are set before copying the banks. In the v035
player the instruction disabling DMA at EVERY subsequent copy of the original
bank was replaced with three NOPs, so that the caption remains visible also
during the following INITs. The first INIT still disables DMA before configuring
the new screen. This does not change the music data or the scene boundaries.

[READ] The loading test checks the order of segments and INITs, the text, registers,
shadows and the changed instruction. No visual observation of the screen
in the emulator or an attempt on physical Atari was performed; the CPU test does not model ANTIC DMA.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 080 048
bytes identical with v035; the comparison covers the whole piece. The emulator
was started from an extracted AppImage, without FUSE.

[READ] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 196/196
cases passed, no skips; 148.545 s.
