> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V356 — finale star and stable payload publication

In the opening an eye appeared, along with the shadow of the jaw and the cool
edge of the girl's hair. The profile remains legible in the large frame and in
the shots pulling away from the character. The arena palette and camera
positions correspond to the v355 montage.

In act 3 the ball, satellites and debris are prepared on the invisible PMG page.
The completed ANTIC and PMG lists go to the screen together with their positions
in the blanking interval. The buffer selection stores the payload bank, without
reading PMBASE. The invisible buffer is cleared in the range `$0980–$0BFF` or
`$8980–$8BFF`. The existing frames, trajectories and moments of the three board
cracks remain. This removes the write to visible PMG indicated in the v347
audit. The cause of the artefact observed on physical Atari remains to be
confirmed.

The finale closes with a faceted star cut by two orbits, composed of ANTIC 5
tiles. The sign takes up the motif of four stars above the lying boy. The final
list was designed with four DLIs on lines 0, 78, 156 and 234. The sign uses
unused font and screen characters under `$BF00` after the terminal expires. The
card still enters at tick 51980, and the music ends after 5:00.

## Memory areas

- Payload code change in video bank 1, `$4000–$4B7F`. A size check guards the
  bitmap data boundary under `$4B80`.
- Card in control bank 49. The list starts under `$5C60`, the code and tiles fit
  in the gaps before `$5CD0`, `$6000` and the orbit state under `$69B8`. No part
  uses the ribbon stream range `$6A00–$7DFF`.
- Only the staging images of indices 15 and 63 (counting from zero) differ from
  v355. The shared pool has 299 rows and 11 491 B. The main code has 2542 B; all
  64 banks remain allocated.

## File and verification

`releases/less-i-know-demo-release-066-stereo.xex`, 945 964 B.
SHA-256 `2369853082b52dc69ebb03d88101722e3246f9a1a669c8d48a3bbde40a8f6fdd`.
Packaging according to loader 058, with verification of all 64 images and the
bootstrap.

Over 29 targeted tests of the payload, character, finale, ANTIC lists and loader
passed. The moving VCOUNT test checked the publication and the absence of writes
to visible PMG at various payload phases and frame entries. A full `make check`
was not run.

Atari800 PAL, 1088 XE, Altirra OS, two POKEYs. The full run produced 59 834
register packets identical to 064 in the same order, including the initial
muting. In the payload scene 543 PMBASE publications were recorded, alternating
`$08` and `$88`, on lines 248–256 in emulation. Selected frames were viewed,
saved in `build/v356-kadry-atari800.png` and
`build/v356-karta-finalowa.png`. No physical AVG trial, FPS measurement or
analogue listening test was carried out.
