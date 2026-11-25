> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V142 — side ribbons and a separate pom-pom project

## Image and synchronisation

[READ] In line with the user's decision, the pom-pom dance at 8975–11967
(~0:45–1:00, bars 24–32) was replaced with a side shot of the girl with a
ribbon. She looks left and takes steps backwards. The camera keeps her on the
right side of the frame, the hall moves left: the wall by 4 pixels per phase,
the floor by 2. Eight new illustrations and 16 background phases form a cyclic
pan. The rainbow loops are created on four players, and the coloured sparks on
missiles.

[READ] The later shots 14959–20942 gain poses 32–35: an extra hip turn and a
crouch in the group, a turn in the solo, and extra group movement before the
toss. All three shots have extended choreography.
Altogether 36 compositions: 16 side ones and 20 later ones, each 160×64,
repeated three times vertically by ANTIC. These are not 36 unique body poses:
the compositions also take into account background movement and the group
arrangement.

[READ] Scene boundaries, the heroine's final toss, the music clock and the four
music DLIs remain at the approved positions. The side frames are selected by the
phase `(tick >> 4) & 15`; the later dance remains on half-beat boundaries.
The cache also checks the owner of the active display list, so that ribbon frame
numbers do not collide when jumping from another shot. Both the PMG and bitmap
buffers keep the rule of preparing the inactive area before publication.

## Balance relative to v141

| Area | V141 | V142 | Difference |
|---|---:|---:|---:|
| Former six pom-pom banks | 98 304 B | 92 160 B of ribbons | −6144 B |
| Ribbon bitmaps in Trevor's banks | 40 960 B | 0 B | −40 960 B |
| Ribbon controller | 1527 B | 1762 B | +235 B |
| PMG anchors | 128 B | 288 B | +160 B |
| Main non-banked code | 2484 B | 2560 B | +76 B |
| **Net recovery** | | | **46 633 B = 45.54 KiB** |

[READ] Removing the pom-pom bitmaps alone would free 96 KiB. The new material
uses 90 KiB, but also includes the later ribbons, which until now occupied
another 40 KiB. Hence 46 KiB of freed slots, minus 471 B of additional code and
anchors. The source PNG/RGB on disk is not Atari memory.

[READ] The free places have specific owners:

- Original player banks 9–14, `$26FC` table indices 8–13:
  six bitmaps of 2560 B each under `$4000–$7BFF`, free `$7C00–$7FFF` (6 × 1024 B).
- Loader banks 24–39 (different numbering): free again `$4A00–$53FF`
  (16 × 2560 B). Trevor's art and code remain outside these slots.
- Loader bank 49: controller `$5400–$5AE1`, anchors `$7E00–$7F1F`.
  PMG streams `$6A00–$7DFF` and the hit helper `$6000–$69FF` unchanged.

[READ] All 64 banks are still allocated. The XEX is 1 109 098 B,
76 B more than v141; neither the loader nor the hardware requirements were
trimmed. The recovery concerns space for further data. The code `$1400–$1DFF`
already fills the whole slot before the row pool from `$1E00`; it requires
watching on further changes.

## Pom-pom project preserved separately

[READ] `projects/pompom-dance` is a standalone project with its own player,
sources of both graphics, generator, Makefile, tests, RAM map and a numbered
`build/pompom-dance-v001.xex`. It does not import anything from the parent
directory. The 12-frame reference (98 304 B) comes directly from the v141 banks;
the generator checks full byte compatibility. `reference/provenance.json`
contains the source checksums. The original v141 release is also preserved.

Archive to move: `build/pompom-dance-project-v001.zip` (2 528 481 B).
It was unpacked into a separate directory in `/tmp`, built from source and 3/3
tests were run without parent-directory files. The rebuilt XEX has an identical
SHA-256 to the frozen v001.
The standalone show loops the entries of one, two and three girls from the
beginning of the original music. It does not carry the remaining demo scenes.
It has a simpler full 8 KiB copy renderer; its CPU cost should not be equated
with the former dirty-copy.

## Validation

[READ] `make check`: 100 tests, 97 passed, 3 skipped due to the
missing archival v126; 80.715 s. The tests cover all 16 side
frames, the two scroll speeds, the shot boundaries, the new later poses, the
recovered slots, the cache after jumps between scenes and the protection of
active buffers. Music NMIs injected also during the copy of the new side shot:
PORTB restored, the resulting bitmap consistent. The variable-VCOUNT simulation
checks the PMG publication window; py65 does not model ANTIC DMA.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 297 256
identical bytes relative to v035, the whole track. Separate project: 3/3 tests,
16 312 896 identical POKEY bytes through the whole track. This is a comparison
of registers; without listening and without a trial on physical Atari. Playing
the XEX in the target configuration remains for assessing smoothness.

The preview `build/v142-side-ribbon.gif` comes from 64 successive 6502
callbacks, every 4 ticks. `build/v142-side-storyboard.png` shows four phases.
The palette and tempo are approximate; the GIF does not show the copy time or
DMA.

## Sources and releases

The new graphic was created in built-in imagegen based on the costume from the
earlier v136 sheet. The procedural background and ribbons are created in
`tools/ribbon_dance.py`.

- Graphic: `assets/art/source/act2_ribbon_side_v142.png`.
- Generation description: `assets/art/source/act2_ribbon_side_v142.prompt.txt`.
- Main release: `build/visual-prototype-v142.xex` and JSON.
- Pom-pom project: `projects/pompom-dance/build/pompom-dance-v001.xex` and JSON.

SHA-256 of the main XEX:
`f7733c3f766a38664dc7169bccc74f17b722221aaca8da10c4ac980a9619db36`.
Byte-for-byte identical to the working build used for the full validation.
