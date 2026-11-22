# V156 — Trevor knocks the ball away with every third hit

Every third hit (3rd, 6th, 9th, …) keeps the usual start of BANG/BAM,
and after the lettering releases a large neon ball from the tunnel. It replaces
the players cloud at the age of the hit 80–135 ticks, flies up/right and rotates.
The remaining hits keep the existing shatter. Missiles still draw sparks
and fragments. Not a single tick of the hit, the effect length or the act boundary was changed.

This is exactly the geometry of the large ball from `tunnel_ball.masks()`, four phases
0/4/8/12, 32 double lines each. Two pairs of players compose the left and right
half, four saturated colours still change cyclically. This is not
the smaller throw ball nor a new background bitmap.

## Memory

[READ] Each of the 16 action banks of loader 24–39 receives 512 B of masks
in the so-far empty `$5E00–$5FFF`. Mask occupancy 8192 B. The data are shared
logically, duplicated physically, to render without switching banks
in the middle of the controller. The area does not collide with the side dancer or the final bitmap.

Bank 49 does not get masks: its `$5CD0–$5FFB` is occupied by the final
boy controller. The installer writes the ball only into the action banks.

Trevor's helper grew from 2395 to **2556 B**, ends at `$69FB` and has already
**only 4 B** before the data from `$6A00`. Across 17 copies of the helper this gives +2737 B.
Total cost +10 929 B; net recovery relative to v141: 12 905 B (12.60 KiB).
Still 64 banks. The main code and its 14 B of headroom remain unchanged.

## Validation

The every-third-hit test compares all four planes with the tunnel
ball masks at five moments of flight and three hits. Regressions for the ordinary clouds,
BANG/BAM and fragments were preserved. The inactive buffer and moving VCOUNT tests
also cover the ball's flight; music NMI injection
now runs during that flight.

[READ] `make check`: 118 tests, 115 passed, 3 skipped
(missing archived v126), 87.140 s.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 403 384 identical bytes relative to v035 through the whole track.
No listening test or test on physical Atari was performed. The py65 tests do not model
ANTIC DMA and do not determine the real FPS or raster stability on hardware.

## Release and previews

`build/visual-prototype-v156.xex` and JSON.
`build/v156-ball-punch.gif` and `build/v156-ball-punch.png` show the lettering,
the appearance of the ball and the flight. Previews after the 6502 callback, with approximate palette
and tempo; they are not an emulator recording.

XEX SHA-256: `6e8d3a2e2a2c7916804507081a166b21da4183b816e74bd5afcd22ff29b1a616`.
The numbered XEX/JSON are identical to the dev working files.
