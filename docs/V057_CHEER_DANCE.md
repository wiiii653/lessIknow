> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V057 — cheerleader dance

[READ] The new hall and four cheerleader poses use a four-colour conversion
to ANTIC E. Sources: `assets/art/source/act1_gym_dance_v056.png`
and `assets/art/source/act1_cheer_dance_v056.png`. The compositor adds a black
outline and shadows, and for three figures selects pose phases `0, 1, 3`. Each
pose lasts 32 music ticks. The entry boundaries of the solo, duo, trio and
kaleidoscope remain as in v055. Twelve finished frames still occupy six banks.

[READ] Four players and four missiles create sliding accents on the beats. Each
player has a separate colour; the missile uses its colour. The PMG helper
occupies 228 bytes in `$AF00–$AFE3`, does not disturb the frame copy area and
restores its contents after other scenes.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 60 tests OK,
including tests of the four trio phases, the colours and PMG movement, the copy
into the inactive buffer, the music NMIs and the returns to other scenes. A full
comparison of stereo POKEY with the original v035 in Atari800 gave 7 890 552
identical bytes after a single alignment of the start. The measurement does not
replace listening.

[READ] Comparison of v055 and v057 in instrumented Atari800 7.2.1, PAL,
1088XE, Altirra OS and stereo: 14 958 frames up to tick 59832; the music counter
and the four sampled POKEY registers agree in every pair. Outside the dance
section and the direct transition to the mosaic the frame skips agree. The GIF
preview is a render of the 6502 routine, with an approximate palette, and not a
recording of the emulator screen or of physical Atari.

Release: `releases/visual-prototype-v057.xex`; SHA-256
`aa87e68ffb919c69491fbcd55bc338f6f91344aef95659ae4a7f7152a3379645`.

## Source artwork

Both graphics were generated with the built-in imagegen tool, using the
existing training board as a style reference; the dance board was an additional
pose reference. Prompts:

- „Use case: illustration-story. Asset for an Atari 8-bit demo animation sprite sheet. Image 1 is the existing four-pose sheet (composition reference); image 2 is the gym scene (art direction reference). Produce a clean 2 by 2 grid of four consecutive full-body poses of ONE SAME young adult blonde/dark blonde school cheerleader, dancing with two large pom-poms. European comic illustration, credible anatomy, bold confident ink, mature appealing face, no manga, matching the gym scene's 1980s European graphic novel style. Four clearly different readable action poses with arms and legs moving in a coherent dance sequence; head, body proportions, costume and placement consistent for frame-by-frame animation. Each panel isolated on pure solid black, no borders or text, exact 2x2 equal grid, each full body centered with generous black margins and all pom-poms within its own cell. Use only solid black, bright magenta, cyan, and warm peach flat color fills; no other colors or gradients, bold large shapes designed for severe reduction to 48 by 144 pixels. Pink and cyan uniform, blonde hair suggested by warm peach because of the four-color constraint; crisp uncluttered silhouette.” In the pipeline the result is scaled to 48×128 so that the animated fragments fit within the partial copy area.
- „Use case: illustration-story. Asset: empty school gym background for an Atari 8-bit animated scene, referenced image is the style and location. A symmetrical wide shot of the SAME school gym from the reference, seen straight on with clear basketball hoop, high wide windows, beams, polished wooden basketball court with restrained perspective. Reserve the middle foreground for three dancers to be composited later, no people, no silhouettes. European comic book artwork with strong clean black inking, restrained flat geometric shapes, bright cyan windows, magenta wall accents and warm peach floor, black shadows. Exactly four flat colors: black, cyan, vivid pink, warm peach. No gradients, text, logos, or tiny textures. Bold graphic architecture, readable when reduced to 160 by 192 Atari pixels. Entire image is one uninterrupted scene, no panels.”
