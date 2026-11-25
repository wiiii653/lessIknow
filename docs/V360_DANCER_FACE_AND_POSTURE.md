> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V360 — dancer's face and upright posture

The reference points are the dancers with ribbons and the girl at the wall bars.
The close-up uses the face and curls from `act2_ribbon_dancer_v136.png`,
transferred to the four arena colours. The bright edge of the smile was reproduced
on the target grid. The neck is bright and set above the shoulders, and around
the face a thin contour line remained. In the further shots, when the girl
walks to the door, mainly the hair is visible from behind.

In the side walk the head was moved above the shoulders and the protrusion of the
face was reduced. The step still has 18 frames and the same rhythm. The everyday outfit was kept:
a sleeveless shirt, denim shorts and sports shoes. A comparison of actual
Atari800 frames is in `build/v360-opening-review.png`, and the movement in
`build/v360-walk-comparison.gif`.

The pool contains 301 shared rows and 11 605 B, the main code 2542 B.
The generator, if space is short, rearranges whole row chains within
the existing ranges. Pixels, impassable ANTIC page boundaries and the low RAM ranges
replayed by the loader remain protected. The changed bank images have indices 33–37 (from zero).
The packing preserves the 058 contract.

- Stereo `releases/less-i-know-demo-release-076-stereo.xex`, 945 368 B,
  SHA-256 `43d71c3b078816ef048b1f51ccc0b9847b5efcfd45eb33f412679e9c281eb203`.
- Mono `releases/less-i-know-demo-release-077-mono.xex`, 945 368 B,
  SHA-256 `686ed212ba5cbe781b76233391ac880bbac814707c838d0d3f5cad0cb9e614c6`.

21 targeted tests passed. Atari800 PAL, 1088 XE, Altirra OS:
59 833 POKEY updates in 076 agree with 074, and in 077 agree with 075.
The piece lasts 5:00. The indicated frames were viewed. Without a full `make check`
and without an attempt of the new files on physical Atari.
