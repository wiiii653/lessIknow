# V177 — production character art

I replaced the test character graphics in the opening and the basketball sequence
with new RGBA sources:

- Boy: portrait on a transparent layer, looking left, blinking and whistling.
- Girl: 2×2 sheet of four walk-left poses, in a jacket with the Fuji emblem.
- Basketball player: six full poses for dribbling, run-up and dunk.

The real alpha channels create the character masks anew. I removed the guide
polygons that selected character and backboard elements from the old backgrounds. The basketball player
is now composited directly onto the hall floor, and the hoop and backboard are drawn
separately on that floor. The backboard crack, ball flight and satellites use
the same phases and ticks.

Sources:

- `assets/art/source/act1_boy_whistle_v177.png`
- `assets/art/source/act1_girl_walk_cycle_v177.png`
- `assets/art/source/act3_basketball_hero_v177.png`

Bitmap compositing previews (not emulator dumps):

- `build/v177-opening-cast-preview.png`
- `build/v177-arena-walk-preview.png`
- `build/v177-basketball-preview.png`

Build:

- XEX: `build/visual-prototype-v177.xex`
- 292 of 309 shared rows; 10 919 B of scanline data
- 2 552 B of main code
- Banks and timeline unchanged
- SHA-256: `2d867354e852762a20ef3e6119a851021353514012963efb883920305048172b`
- Build completed successfully. Tests and emulator playback were not
  run.
