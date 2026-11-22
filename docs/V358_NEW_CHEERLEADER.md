# V358 — new cheerleader in the shots before the arena

Reference points: the shots from 058 (v330, party pack), 061 (v352) and 070
(v357). They were viewed in Atari800. In 070 the close-up of the girl duplicated
48×64 grid samples, while the boy's face had contours on the target
160×64 grid. The side walk still used the earlier torso and arm movement.

The girl is drawn from scratch in the arena palette. Up close she has single
contour columns, a pink facial shadow similar to the boy's, dark hair
with a bow and a jacket with Fuji. The further shots use separate poses and scales.
The side panorama shows a silhouette with a skirt, socks and shoes. Eight
walk phases give a foot roll, heel lift, knee change and arm movement
opposite to the step. The phases fill 18 existing frames from tick 3553.
The arena background still moves in the opposite direction. The shots after the boy's
glance remain cuts to the successive poses of the receding girl.

Comparisons of actual emulator frames: `build/v358-opening-comparison.png`
and the 18-frame `build/v358-walk-comparison.gif` (058, 070, 072).
The boy's frame to the right of the composition line, his reactions and the scene ticks are
preserved. The opening tunnels and the banana entry after Trevor correspond to v357.

## Memory and loader

The new panorama frames change five staging images with indices 33–37
(counting from zero), without allocating another bank. The shared pool
contains 297 rows and 11 481 B; the main code has 2542 B. The generator limits the
pools from `$0400` and `$0900` to the last bytes replayed by the 058 bootstrap
(`$07DF` and `$0976`). All 64 images and the loader contract are preserved.

## Files and verification

- Stereo `releases/less-i-know-demo-release-072-stereo.xex`, 945 059 B,
  SHA-256 `4a4399db47153d5d8a2c938a05b8b25f4633a20e7e9604c4309156e22b3f4251`.
- Mono `releases/less-i-know-demo-release-073-mono.xex`, 945 059 B,
  SHA-256 `9291792352a01006bdfa85044505e6b6418c8023ebd2cf65bf33cc0c7f9e6b48`.

21 targeted tests of composition, panorama, scenes and loader passed.
In Atari800 PAL, 1088 XE, Altirra OS, 59 833 updates each were compared: 072
with two POKEYs gives values identical with 070, and 073 with one POKEY gives
values identical with 071. The full piece lasts 5:00. The emulator frames were viewed.
No physical attempt of these files or full `make check` was performed.
