# The Less I Know The Better — Technical Overview

A PAL Atari XL/XE demo. Everything on screen is real ANTIC/GTIA/PMG output:
no interlace tricks, no flicker frames, no prerendered video.

## Requirements and build

| Item | Value |
| --- | --- |
| Machine | Atari XL/XE, PAL, 1 MB expansion (64 × 16 KiB banks) |
| Sound | Stereo POKEY (two chips) |
| Executable | Stereo XEX, 936,121 bytes (release 048 / v315) |
| Loader | AVG-compatible XEX with a low-memory late-start bootstrap |
| Music | original v035 player, score-based, no samples |

## Video pipeline

- **Playfield:** ANTIC mode E, 160 × 192 pixels, 4 colours (2 bits per
  pixel, 40 bytes per row). Two RAM framebuffers at `$9000`/`$B000` are
  prepared alternately; the inactive one is composed, then published in
  vertical blank.
- **Rows, not full frames:** a pool of 298 unique 40-byte rows is shared by
  all bitmap scenes. Display lists address rows through per-row LMS
  pointers, so scrolling, row reordering and mosaic effects cost only
  pointer updates — no bitmap copy for those parts.
- **Sprites:** 4 players and 4 missiles, always double-buffered. The
  completed buffer is published only inside a bounded VCOUNT window, so
  the beam never sees a half-written sprite.
- **Palettes:** music DLIs at raster lines 1/79/157/235 keep the four
  updates per frame. Additional palette-only splits (e.g. line 57 in the
  outro) change colours without adding music ticks.
- **Banked art:** `$4000–$7FFF` is a 16 KiB window switched through PORTB
  (`$D301`). Scene code saves and restores the caller's bank around every
  access, so music NMIs always run in a consistent mapping.

## Scenes and how each effect is made

| Scene | What you see | Technique |
| --- | --- | --- |
| Opening cards | City skyline, Gdańsk crane, two title cards, colourful fireworks | ANTIC F 80 × 192 with GTIA 11 (16 hues), two cards dissolved; PMG fireworks with rising rockets, radial bursts and falling fragments in front of the letters |
| School / arena | Girl walking past the arena, boy's reaction, whistle notes | ANTIC E bitmap with alpha-masked sprites; parallax pan by row-pointer shifts; PMG notes and treble clef on four players |
| Practice & basketball | Dribble, dunk, shattering backboard | Bitmap keyframes; ball drawn on four players with a shared 512-byte neon sphere; orbit satellites on missiles; glass shards as PMG |
| Ribbon dance | Side dancer, then group/solo/overhead ribbon shots, throw and kiss | 36 base compositions plus real in-between poses stored in banks; ribbons drawn as PMG players (double-line rows), sparks on missiles; rainbow colours advanced by a reentrant raster helper |
| Trevor | 13 punches, BUM/BAM bubbles, flying balls | Bitmap poses from the original art; three-letter words and cloud fragments on PMG; every third hit borrows the rotator ball with both missile satellites |
| Post-Trevor montage | Banana rotozoomer, spiral and organic tunnels, girl's eyes | Banked 160 × 96 ANTIC E frames (32 banana phases, 16 spiral, 12 organic, 4 eye frames); a music-cued director selects motif, direction and speed; eyes are four hand-built bitmaps |
| Outro terminal | Typed credits and greetz, cursor, scrolling history | ANTIC 4 text (green COLPF0 on black), seven rows, typewriter effect and Enter handling; palette split by an extra DLI |
| Final shot | Boy on the floor, orbiting stars and notes, fade to black | Bitmap frame plus four PMG players on an ellipse; 19 vivid GTIA colours rotating with phase offsets; fade ends in permanent black |

## Effects catalogue by technique

- **ANTIC E bitmap:** all story scenes, mosaics, eyes, final frame.
- **ANTIC F + GTIA 11:** both opening cards (16 hues, 80 × 192).
- **ANTIC 4 text:** terminal rows in the outro.
- **PMG (players + missiles):** fireworks, notes, ribbons, sparks, ball,
  satellites, punch bubbles, cloud fragments, glass, orbiting stars.
- **DLI palette splits:** music ticks, terminal palette, ribbon rainbow.
- **LMS row addressing:** scrolling and mosaic row reordering.
- **PORTB bank switching:** 1 MB of artwork, ~50 banks of video assets plus
  14 music banks.
- **Lifetime overlays:** after the title, retired title banks are reused as
  raw banana frames; nothing is loaded from disk during playback.

## Loader

The XEX holds 64 bank blocks. Long zero runs are omitted and each bank is
zeroed by a small INIT before its data arrives. Low runtime RAM is staged
in a buffer and restored by a final INIT that jumps straight into the player
(`JMP $13E0`), so start-up does not depend on the RUN vector being honoured.
A loading screen with title, platform and credits is shown while banks are
copied.

## Honest limitations

- PAL only; timings are tied to the PAL frame and music clock.
- Requires a 1 MB expansion; the layout assumes 16 KiB banks at `$4000–$7FFF`.
- The maintained release is stereo and requires two POKEY chips.
- Not every scene updates at 50 fps: the heaviest ones (side dancer, ribbons,
  rotator/tunnel) take about two frames of CPU per update. Music stays in
  time because it runs from NMI.
- Earlier releases were started from AVG on a 1088 Rambo machine. Release 048
  has not been re-tested on physical hardware. CPU tests and the older full-track
  Atari800 comparison do not establish current full-run smoothness, audio, or
  real raster timing.
- Graphics and music come from original sources and a MIDI score; no samples
  from the commercial recording are used. AI tools assisted development and
  this is reported in the competition entry, as the rules require.

## Credits

Code, graphics and direction: Ognjen. Music: v035 player engine with an
original POKEY arrangement based on Tame Impala's composition. Produced for
Silly Venture 2026 WE. AI assistance is disclosed in the entry file.
