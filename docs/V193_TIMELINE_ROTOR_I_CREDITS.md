> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V193 — full rotator and earlier outro background

## Timeline change

- Bars 88–92 (ticks 32909–34404): first half of the existing banana rotator.
- Bars 92–96 (34404–35900): second half of that rotator.
- Bars 96–108 (35900–40388): spiral tunnel.
- Bars 108–112 (40388–41884): existing organic tunnel texture.
- The boundaries of the further Act 5 shots at bars 112 and 116 remain unchanged.
- From bar 144 / tick 53850 the lying boy with orbiting stars appears as the
  intended background of the credits and greetz windows. The credits/greetz
  text itself is not there yet.
- Bar 158 / tick 59085 still starts the final two-bar close to
  black; the end remains at bar 160 / tick 59833.

## Technical scope

The transition boundary from the banana rotator to the tunnel was changed from bar 92 to 96
in `tools/build_bitmap_sequence.py`. `tools/final_boy.py` starts the existing
frame from bar 144, keeping the existing data, star animation and ending.
No graphics, effect generators or memory allocation were changed.

Build: `build/visual-prototype-v193.xex` and its corresponding JSON.
298 shared rows, 2560 B of main code.

## Validation

10 tests of scene boundaries, Act 5 motifs and the finale passed. The tests check the
transitions at ticks 34404, 35900, 40388 and 53850 and the retention of the full
final frame. No full audio comparison and no test on physical Atari.
