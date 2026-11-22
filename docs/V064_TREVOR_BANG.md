# V064 — Trevor's BANG

The exclamation mark was removed from the G glyph. The speech bubble starts
with a smaller flash, grows, and then disappears; in the final phase four
separate missiles spread to the sides as coloured stars. As with the ball
satellites, each missile gets a separate position and shape in PMG memory. The
distance of the stars from the fist grows during the scatter phase.

Subsequent hits choose one of four small X/Y offsets. The same offset is applied
to the caption, the speech bubble and the later stars, so that parts of the
effect stay together. The caption is full size during the visible phase; only
the flash is scaled.

`make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 62 tests OK, including
control of the caption, the different positions, the star spreading and the
return to the dance scene. Full comparison of v064 stereo POKEY with the
original v035 in Atari800: 8 244 648 identical bytes after a single alignment
of the start. This does not replace listening. The GIF preview comes from the
6502 renderer; its frame timing is approximate and is not a recording from
physical Atari.

Release: `releases/visual-prototype-v064.xex`, SHA-256
`6e24e90a0cb8cede78d7b2fcdfcaa14db9335f6e9f43cfe1ccce101b4a603e15`.
