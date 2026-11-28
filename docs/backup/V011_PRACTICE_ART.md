> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# Three training shots — v011

[READ] New graphics in the style of `act1_school_court_boy.png`: close-up of
the basketball player (5984–6980), the throw (6981–7977), the girls at the wall
bars (7978–8975). The dance still starts at 8976. Each shot is a static
160×64 illustration displayed in 192 lines. The former PMG ball was disabled.
The remaining scenes were kept after review; the main inconsistency concerned
the simple geometric training characters.

## V2/V3

[READ] All three shots fit together in the existing 8 KiB area at the end of
bank 8. Buffers and PORTB protection rules as in v010.

## V6

[READ] 21 tests passed. Atari800 PAL/1088XE, stereo POKEY:
6 776 136 identical register bytes relative to v035 (~1887,5 s of emulation),
the whole tune covered by the comparison. No test on physical Atari and no
listening test.

## Graphics and preparation method

Built-in image_gen; style reference: `assets/art/source/act1_school_court_boy.png`.
Saved original: `assets/art/source/act1_practice_storyboard_v011.png`.
Conversion: ImageMagick, point sampling 160×192, nearest colour from the Atari palette.

Prompt:
Use attached image solely as exact visual style reference. Create a SINGLE storyboard contact sheet with three equal horizontal landscape panels stacked vertically, no gutters or text. Each panel aspect ratio 5:3. Retro Atari pixel illustration same sophisticated comic face design as reference, natural teenage athletic proportions NOT chibi, NOT stick figures, bold black silhouettes, only black, bright cyan, hot magenta and peach palette. Flat clean pixel shapes no gradients, compose to survive 160x64 logical pixel reduction. Panel top: cinematic waist-up close-up of handsome dark-haired school basketball player holding basketball at chest, focused expression, cyan jersey, gym windows behind. Middle: dynamic medium shot of basketball player releasing jump shot toward visible hoop at upper right, another player at left, natural anatomy, detailed gym architecture, strong readable silhouettes. Bottom: medium shot of two teenage girls in modest sportswear stretching beside wooden gym wall bars, one overhead side stretch and other leg stretch, natural faces like reference, floor and window depth. Same coherent gym, graphic polish and palette in all panels, no text or panel labels. Output the full contact sheet as one image.
