> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V136 — three ribbon-dance shots

## Content and synchronisation

[READ] The four former performance illustrations in 14959–20942 were replaced
with three shots: group 40–44, solo 44–48, group with preparation and the
heroine's launch 48–56. The final launch has four ascent positions. The player
clock selects poses according to a table of 128 half-beat boundaries; a separate cycle of 16 ribbon
shapes follows from the consistent tick copy. The act boundaries and the four
music updates per frame were not changed. The content change and the three shots were approved by the user.

[READ] Eight source poses compose 16 frames of 160×64, repeated
three times by ANTIC. The background shows a shared hall; the characters use
four colours, and four players and four missiles form the ribbons and
thin accents. This is an adaptation of the choreography and costumes, not a rotoscope of the music video.

## Memory and presentation

[READ] Still 64 banks. Confirmed free slots were used:

- Banks 24–39: `$4A00–$53FF`, 16 × 2560 B = 40 960 B of bitmap.
- Bank 49: controller `$5400`, 1412 B; sashes `$6A00–$7DFF`, 5120 B;
  attachment positions `$7E00–$7E7F`, 128 B. Trevor's original poses/code
  remain in their areas; the installer rejects overwriting non-zero data.
- The new unbanked copy trampoline is 25 B. PORTB is preserved
  also by the music NMI.
- PMG buffers: `$0980–$0BFF` and `$8980–$8BFF`. The second area was taken
  from the static row pool and those rows were re-laid out during the build.
  During writing, the previous PMG is active; PMBASE switches together with the position
  registers in a bounded raster window. The bitmap is also produced in the inactive
  buffer `$9000` / `$B000`.

[READ] The former portraits were removed from the resulting bank 8; the music below
`$4B10` and the training above `$6000` are preserved. The new scene uses more
data than the old four static illustrations, but fits within the existing
configuration without adding banks.

## Validation

[READ] Full `make check`: 90 tests, 87 passed, 3 skipped
due to the missing archived v126; 81.307 s. New/adjusted tests cover
128 steps, jumps between shots, ribbon movement with a frozen pose,
no writes to the active PMG/bitmap, safe publishing at various
raster positions, and copying with real decoder NMIs and PORTB restoration.
The VCOUNT simulation does not model ANTIC DMA or hardware deadlines.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 744 880
identical bytes relative to v035, the whole track. This is a register comparison,
not a listening test on physical Atari or a measurement of image smoothness.

The preview `build/v136-ribbon-dance.gif` comes from 250 consecutive executions of the 6502
callback; 24-tick interval, about 30 seconds. The tempo and palette are approximate;
the GIF does not account for DMA, copy time or phase skipping in the emulator.
Playback of the XEX remains for artistic evaluation and target smoothness.

## Art sources

Built-in imagegen, costume reference from the designer's material:
https://www.behance.net/gallery/31604763/Tame-Impala-Textile-Design

- Art: `assets/art/source/act2_ribbon_dancer_v136.png`.
- Full prompt: `assets/art/source/act2_ribbon_dancer_v136.prompt.txt`.
- Generator and renderer: `tools/ribbon_dance.py`.
- Release: `build/visual-prototype-v136.xex`.
