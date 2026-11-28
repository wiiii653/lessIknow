> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V170 — the boy winks and whistles

## Shot and graphics

In the first shot of the school facade the boy has a clearly narrowed eye,
looks left and whistles after the girl. A short, pixel trail of the melody
contains two treble clefs and two notes. The symbols are composed at
160×192 resolution, instead of relying on details that vanish when
the whole image is scaled down. The melody is a background layer; in the first pass
the girl obscures it according to the scene depth.

The new source image replaces the portrait in `build/school-front.rgb`.
The original `act1_boy_front.png` remains preserved.

- Source: `assets/art/source/act1_boy_front_v170.png` (1619×971).
- Prompt: `assets/art/source/act1_boy_front_v170.prompt.txt`.
- Source processing: target 160×64, existing portrait mask and scene
  palette; melody added by `school_story.whistle_melody`.
- Previews after background and portrait composition: `build/school-v170-1-preview.png`
  and `build/school-v170-2-preview.png` (the second shot with the girl).

## Memory and synchronisation

- Ticks and act 1 boundaries unchanged.
- Banks unchanged; the number of fully free banks is still 0, known banked
  gaps still 31 623 B.
- Shared rows: 279 → 309; row memory: 10 764 → 11 913 B
  (+1 149 B). The rows remain in the existing RAM areas.
- Main code: 2552 B, eight bytes before the `$1E00` limit.
- No tests were run. The previews check the graphics composition, not
  a recording from Atari800.

The XEX was built with `python3 tools/build_bitmap_sequence.py --output
build/visual-prototype-v170.xex`.

SHA-256: `a439cbe3e2fc94cff35ccf941d5a11df21c8c79618328da034909d4fad12ac5c`.
