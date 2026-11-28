> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V082 — plasma and opening titles

Both existing GTIA 11 screens keep their boundaries: the performer from
tick 0, the title from 1496, the school from 2992. The plasma brightens out
of darkness, flows through a change of line addresses and reveals successive
rows of the title. Towards the end of each screen the lines fade out in a
different order. The phase change uses the music counter every 16 ticks; DLI
were neither added nor shifted. The titles have a black background in their
bands to preserve readability and fit the image within the available memory.

The effect code and data occupy `$E4C0–$E9D2` under the system ROM; the whole
reserve `$E4C0–$EABF` is excluded from the row pool. The procedure modifies
only the inactive display list. The buffers of later scenes remain available,
and the plasma code also behaves correctly when returning to the beginning of
the track.

[READ] `make check PYTHON=/tmp/tliktb-plasma-venv/bin/python`: 64 tests OK,
including the title phases, the fade-out, the return to the intro, the scene
boundaries and four DLI positions.
[READ] Atari800, PAL, 1088XE, Altirra OS, stereo POKEY: comparison with v035
passed for 4,670,136 bytes after a single alignment of the start; it covers
the whole track. [READ] In an isolated py65 test, rebuilding the intro image
takes about 40–46 thousand 6502 cycles, so a single phase may last several
frames.
[CONCLUSION] Music interrupts remain active during the rebuild; the POKEY
comparison is no substitute for listening or a test on a real Atari.

The preview `build/visual-prototype-v082-preview.png` uses approximate
colours computed from the display list; it is not an emulator screenshot. XEX:
`build/visual-prototype-v082.xex`, SHA-256
`3aac79b1a6c03b6a4d95f267937d979133f956b892cb15639cb206056c08a6dc`.
