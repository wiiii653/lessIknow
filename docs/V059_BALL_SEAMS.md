# V059 — coloured ball seams

Four players form two colours: both physical areas of the ball can each contain
either of them. The curved seam is at the same time the colour boundary, and the
transverse seam is created by a local swap of colours. The outline and seams
have no separate black layer. The colours change from a rainbow palette; four
missiles still form the satellites. The track and scaling remain as in v058.

`make check` passed 60 tests; it was additionally verified that each physical
player area can contain both colours. A full stereo POKEY comparison with the
original v035 gave 8,663,688 identical bytes after aligning the start. The
preview comes from the 6502 renderer, not from a physical Atari.

Release: `releases/visual-prototype-v059.xex`, SHA-256
`2f8d761b8430e2aecb46d4a3fc6444bffab4262c0b669282ca352ada42633e9c`.
