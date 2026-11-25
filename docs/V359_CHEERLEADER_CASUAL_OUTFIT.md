> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V359 — cheerleader in casual outfit

The character reference is the girls dancing with ribbons and the squad poses screen.
The outline, readable shadow patches and pixel scale were compared with the boy in
the opening and at training and with Trevor's fight. Light curls, a small blue
headband and a gentler profile distinguish the girl from the boy.

For the walk she has a pink sleeveless top, denim shorts with rolled-up
legs and sports shoes. The arms have a different outline than in the jacket version.
Her own poses and outfit details remain readable as the camera moves away.
The 18 panorama frames preserve the step with opposite arm movement, a natural
knee transition and a raised heel. The girl, the background and the boy have the same
four-colour palette. The scene timing and the camera pan remain as in v358.

The changed bank images have indices 33–37, counting from zero. The pool has 298
rows and 11 517 B, the main code 2542 B, 64 banks are still allocated.
Packing of both variants follows the 058 loader contract.

- `releases/less-i-know-demo-release-074-stereo.xex`, 945 208 B,
  SHA-256 `140604783090054071942b316063394ff257702d78d7e566d03991ec09785b6d`.
- `releases/less-i-know-demo-release-075-mono.xex`, 945 208 B,
  SHA-256 `f7f5d4324dc11b263fba0fa3cea32b070ae157f8accc7c98cd5816df90f82a13`.

21 scene, composition and loader tests passed. Trace of 59 833 updates in
Atari800 PAL, 1088 XE, Altirra OS: 074 with two POKEYs is identical to 072,
075 with one POKEY is identical to 073. The track lasts 5:00. Frames from the
emulator were inspected in `build/v359-style-comparison.png` and a GIF was prepared
`build/v359-walk-comparison.gif`. Without a physical test and a full `make check`.
