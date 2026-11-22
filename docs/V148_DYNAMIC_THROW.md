# V148 — dance, fast throw and air rush

[READ] As corrected by the user, the stretched preparation from v147 was
removed. From 17950 to 20475 (~12.66 s) the group dances with ribbons: pose
changes every half-beat, instead of holding successive phases for long. The
loop applies to the dance; the throw itself remains single.

| Tick | Image |
|---:|---|
| 17950–20474 | Group dance, compositions 8/9/35/10 |
| 20475 | Fast crouch, composition 11 |
| 20521 | Jump in a frontal wide shot, composition 12 |
| 20568 | Cut to a camera above the girl, composition 13 |
| 20615 | Fast zoom toward the lens, composition 14 |
| 20662–20941 | Final zoom with air motion and effects, composition 15 |
| 20942 | Existing cut to the basketball player |

[READ] 187 ticks pass from the crouch to the zoom (~0.94 s).
The hall throw view was restored and the final view from above was kept.
In both flight shots the background is calm and black, without a grid. The
earlier dance uses the hall illustration. The act boundaries, the main
choreography ranges and the four music updates per frame were not changed.

## Rush on players and missiles

[READ] In both flight shots, players 0/3 form narrow air streaks moving
downward, opposite to the character's motion. They have white/cyan
maintained also across the existing music ticks. Players 1/2 remain
coloured fireworks. The four missiles have normal width instead of
double and draw four-row dashes; their vertical position changes
every 4 ticks with a held bitmap. The streaks and blooms are at the sides of
the face.

[READ] The data and masks are still produced in the inactive PMG. Bitmap
copies, mask preparation and the safe publication window are preserved. The
colour helper remains non-banked and reentrant, without shared NMI scratch.
Drawing the streaks keeps X on the stack; the original decoder may interrupt
this code, and the wrapper restores PORTB and the registers.

## Memory balance

- New wind shapes: 128 B, loader bank 49, `$7F20–$7F9F`.
- Ribbon/effects controller: 2237 B (`$5400–$5CBC`), +34 B relative to v147.
- Non-banked colour helper: +21 B; the main code is 2515 B and ends
  at `$1DD2`, leaving 45 B to the pool from `$1E00`.
- Finale boy controller: still 812 B, moved to
  `$5CD0–$5FFB`. 19 B remain between the controllers, only 4 B before `$6000`.
- Still 36 compositions and 64 banks. No new banks or source illustrations
  were needed. Net recovery relative to v141: **24 771 B = 24.19 KiB**.

## Validation

[READ] `make check`: **115 tests, 112 passed, 3 skipped**
(missing archival v126), 91.119 s. The tests check the moving dance across the
whole recovered range, the single fast throw in both shots, the absence of a
grid in flight, the player streaks and moving missile dashes, safe buffers and
restoration of the earlier effects. Decoder NMI injection now also covers the
start of the hall throw view and the shot from above.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **15 331 536
identical bytes** relative to v035 across the whole track. Without listening and
without a test on a physical Atari. The py65 tests do not determine the real FPS
with ANTIC DMA.

## Release and previews

- `build/visual-prototype-v148.xex` and JSON.
- `build/v148-dance-and-launch.gif`: the whole dance range and the fast throw.
- `build/v148-fast-launch.gif`: a short fragment with the throw, callback every 4 ticks.
- `build/v148-dynamic-launch.png`: the dance and both flight shots.

The GIFs play once. The palette and timing are approximate;
they are not an emulator recording nor a measurement of presentation deadlines.

SHA-256 XEX: `556dd9389fea101ab169bb867cc86e705ce76aab89016524e45fdccb8a7518d2`.
The numbered release and the checked working build are byte-for-byte identical.
