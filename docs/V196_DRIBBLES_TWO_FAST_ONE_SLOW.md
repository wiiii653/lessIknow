> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V196 — palm contact and dribble rhythm

The centre of the ball was moved from X=97 to X=84, under the centre of the palm
from the original frames. The track runs vertically between contact at the hand
and the floor, along a sinusoidal arc. The original character graphics and ball
masks are retained.

The dribble sequence lasts 374 ticks: fast 94, fast 94, slow 186. This
corresponds to about 0.47 + 0.47 + 0.93 s. The same clock selects the ball phase
and the arm, so the acceleration covers both animations. Scene and payload
boundaries unchanged.

Build: `build/visual-prototype-v196.xex`; 298 rows, 2560 B of main code.
21 basketball and finale tests passed, including unchanged frames of the payload
and table compared with v175. Software preview (without ANTIC DMA emulation):
`build/v196-dribble.gif` and `build/v196-dribble-contact.png`.

V195 with ball dithering was reverted at the user's request.
