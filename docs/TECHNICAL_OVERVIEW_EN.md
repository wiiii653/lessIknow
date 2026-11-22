# Technical Overview

## Target and release state

This is a stereo Atari XL/XE demo for a PAL machine with a 1 MB expansion and
two POKEY chips. The latest approved release is stereo 133 / v390. The current
source tree contains later development edits and is not itself a numbered,
approved release. Release 058 / v330 is the last full run confirmed on physical
Atari 1088 Rambo hardware from AVG.

The music uses the original v035 player and a tracker arrangement. Its clock
advances four evenly spaced update ticks per PAL frame. Visual scene changes
are synchronized to those ticks. Emulator and py65 results do not establish
physical playback or raster timing.

## Video and memory model

- Story images use ANTIC E (160 × 192 pixels, four playfield colours, 40 bytes
  per scanline). Two RAM framebuffers are prepared alternately and published
  during vertical blank.
- The active allocator assigns all 64 expansion banks. The bank window is
  `$4000–$7FFF`, selected through PORTB at `$D301`. Bank accesses must preserve
  PORTB across music NMI and callbacks.
- A shared pool at `$1E00` currently holds 298 unique 40-byte scanlines.
  Display-list LMS pointers reuse and reorder rows for scrolling and mosaics.
- PMG graphics use double buffers. New buffers are prepared before publication
  in a bounded early blanking interval. Long PMG writes cannot rely only on a
  late raster check.
- Music DLIs retain the four update points per PAL frame. Other DLI splits may
  change palettes without advancing the music clock.

## Current scene techniques

| Scene | Rendering approach |
|---|---|
| Opening | Procedural plasma and staged city reveal; title cards; PMG fireworks that build over time |
| School and arena | ANTIC E artwork, masked character sprites, row-pointer parallax and PMG notes |
| Practice and basketball | Bitmap poses, PMG basketball, satellites and impact effects |
| Ribbon dance | Banked base compositions and in-between poses; double-buffered PMG ribbons and sparks |
| Trevor | Bitmap poses, PMG impact words and bubbles, protected ball effects |
| Post-Trevor montage | Banked banana mosaic, tunnel images and eye frames selected by a music-tick director |
| Terminal | Low-resolution ANTIC text with the established DLI glitch treatment and text fade |
| Final shot | Bitmap portrait with orbiting PMG stars/notes and a fade to black |

The current opening derives plasma and the city reveal procedurally from a
single panorama source. This is intended to reduce duplicated frame storage.
The terminal and credits use the established low-resolution text treatment;
the proposed high-resolution system-font approach is not the current design.

## Hardware packaging

Raw `visual-prototype-*.xex` files do not carry the hardware-confirmed AVG
loading protocol. Package hardware candidates with `tools/build_hardware_xex.py`
or `make hardware`. That path uses stereo release 058 as an immutable loader
reference and approved release 133 as the music source. Preserve the loading
screen, 66 INIT wrappers, 64 bank staging clears, deferred low-memory restore
and final `$4800` bootstrap. See
[`HARDWARE_LOADER_CONTRACT.md`](HARDWARE_LOADER_CONTRACT.md).

## Verification limits

`make check` runs py65 checks. Atari800 playback comparison checks POKEY
register output and timing. Neither models all ANTIC DMA behavior or proves
physical raster deadlines. The project has no current full-run hardware
confirmation beyond release 058.
