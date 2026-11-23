# Basketball hero artwork drafts

Use `draft-in-arena.png` to review the eight poses against the arena and
`current-poses.png` to compare with the current art. In playback order the
dribble uses 0, 1, 6 and 7. The dunk uses 2 (crouch), 3 (rise), 4 (reach) and
5 (dunk). The three board fracture stages reuse pose 5 and are shown in
`draft-shatter-preview.png`.

The `poses/` folder contains eight aligned 160 × 56 RGBA PNGs and their
matching binary masks. White in a mask keeps the sprite pixel, including
opaque black contour and hair. Black leaves the arena visible. The ball
and particles are separate hardware effects and are absent from the artwork.

The atlas was generated with built-in ImageGen from the current poses and the
pre-arena and cheerleader style references. The individual PNGs were then
fitted into the original frame coordinate space and reduced to four inks.
These are approval drafts. Check hand-to-ball alignment and consistency across
the dribble cycle before integrating them. The arena composites are previews,
with colors chosen to show the artwork alongside the style references.
