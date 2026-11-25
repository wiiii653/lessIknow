> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V063 — four-colour ball and stars

The four ball players receive four different saturated colours with brightness
`$0A` or `$0C`, instead of two brighter fields. Adjacent players have
similar colours so that the hardware split in the middle is less pronounced than the
curved seam. This does not completely remove the boundary between the players.

The four missiles were merged into two symmetrical stars, two missiles
each. One moves along an ellipse with radii 25×14, the other 40×23 PMG
units; their phases are offset. The stars remain bright and change colour.
The ball keeps the figure-eight path and the scale change from v058 and covers the centre of the tunnel.

`make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 61 tests OK, including
comparison of both orbits, the missile shape, the four colours, the figure eight and the coverage
of the tunnel centre. A full stereo POKEY comparison with the original v035 in Atari800
gave 8 819 280 identical bytes after a single start alignment.
The preview is a 6502 render with an approximate palette, not a recording from Atari.

Release: `releases/visual-prototype-v063.xex`; SHA-256
`ab1aac7b311c00050a710a34400bf55a1cee421d4e2d77ca5d9477e86df2cc60`.
