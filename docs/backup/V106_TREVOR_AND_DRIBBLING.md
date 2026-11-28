> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V106 — consistent Trevor lighting and shared dribbling background

In Trevor's poses the brightness of the main colours and skin was equalised; the
swings have only a slightly darker secondary colour. Flickering bright outline
fragments dependent on the tunnel phase were removed. The preview renderer was
also fixed, as it assigned a special, much brighter RGB colour to one of the
shades.

Dribbling uses one shared hall background. The second pose is stored
as a 76×56 fragment, and after both buffers are initialised the animation copies only that
area containing the character. The amount of copied data drops from 2240 to 1064
bytes; the graphic data take 1176 bytes less in the existing bank. The number of
physical banks and the XEX segment size remain the same. The feed scene
keeps separate frames. Both animations still use the music clock.

[READ] The full set of 72 tests passed. Then a brightness regression for all
Trevor poses was added and 9 tests of that module were checked.
The dribbling test tracks memory writes and requires that, after the buffers
are warmed up, no pixels are written outside the character fragment. [READ] Atari800 PAL,
1088XE, Altirra OS, stereo: 5 746 896 bytes of POKEY registers were identical
to v035 after a single alignment of the start; this covers the whole piece.
[CONCLUSION] Software previews do not replace assessment of smoothness and colours on Atari.

Previews: `build/visual-prototype-v106-trevor.gif` and
`build/visual-prototype-v106-dribble.gif` (approximate colours and timing).
XEX: `build/visual-prototype-v106.xex`; SHA-256
`98773f3886d5aaf00e825d23f263e49ef2a8380f3fa3c7c7a72f46d551fd6140`.
