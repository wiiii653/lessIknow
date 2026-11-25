> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V058 — rotator, tunnel and ball movement

The rotator uses periodic, four-fold symmetric rosettes; the tunnel uses
curved bands and spiral waves. The patterns loop through frames.

The ball on the players performs a full horizontal figure-eight path in the rotator:
the X and Y positions are computed independently, without drawing a trail. Its rotating
masks change the area from 156 to 352 PMG pixels, suggesting
receding and approaching. The missiles still orbit around the ball. In the tunnel
a separate small movement of both axes is retained; the test checks coverage of its centre.

The scene boundaries and the player remain as in v057. `make check` passed 60
tests, including the path of both axes, the return to the centre and coverage of the tunnel hole;
after adding the mask scale check, that test was also run separately. A full
stereo POKEY comparison with the original gave 8,152,272 identical bytes after
a one-off alignment of the start. The previews are a render of the 6502 procedures with
an approximate palette, not a recording from a physical Atari.

Release: `releases/visual-prototype-v058.xex`, SHA-256
`549e4b2bc6c42c9331f4685709836fa31a8a98e84f991ef3e0b7a8dcbf276c24`.
