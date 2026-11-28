> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V186 — synchronised and closed meeting scene

## Behaviour and graphics

- The boy looks straight ahead in the first shots. When passing the girl
  at 4488 he looks back at her.
- At 4862 the puckered lips and the first note at the mouth appear simultaneously.
  The whistle lasts through both shots of the girl receding.
- At 5610 the girl reaches the door. The melody is faded out, PMG is off,
  and the boy returns to a calm, turned-away pose.
- The v175 framing was preserved, along with the exact side-walk frames and all
  four scales and the girl's track from v181. Later scenes keep their ticks.

The notes and treble clef are full, readable player shapes. Two
finished waves emit them in turn, every six phases. Each glyph has its own
curved path, drifts gently away from the mouth up and to the left, has a detached missile
trail and colours passing through the Atari palette. The last ten phases of flight
gradually reduce brightness to 2. The last wave fades about 0.14 s before
the girl reaches the door; the glyphs are not cut off halfway through the next cycle.

In the whistling portrait, remnants of the old graphics' rays outside
the face were cleared and the mouth was drawn in logical pixels so that the puckered lips are distinct
at 160×64 resolution. The hair and jacket masks remain opaque.

## Memory and result

- `build/visual-prototype-v186.xex` and JSON; dev identical.
- SHA-256: `659de1c7a5bf496653094946064912e0b99cb64496b5f8efddfb224bfaca7b37`.
- 298 shared rows, 11 480 B of row data, 2552 B of main code.
- PMG helper: 1119 B, $6A00–$6E5E in loader bank 0. Up to cleanup $6F00,
  161 B remain. Banks 1–63 are byte-for-byte identical to v185.
- The two existing PMG buffers are prepared outside the active image
  and switched in the lower blanking. PORTB is restored.

## Verification and limitations

[READ] 15 targeted CPU/graphics tests passed: simultaneous
lips and first note, finished waves, separate paths, brightness of the final phases,
no PMG after reaching the door, buffers and PORTB, masks, v175 frames and panorama,
the trajectory to the door, and the ball regressions.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 6 220 440 identical
bytes relative to v035, the whole track. The emulator installed as an AppImage works
with `APPIMAGE_EXTRACT_AND_RUN=1`; the earlier FUSE obstacle was bypassed
with the standard AppImage launch mode after extraction.

[READ] `make check`: 139 tests, 126 passed, 10 failed,
3 skipped (no archived v126). Log: `build/v186-check.log`.
All ten failing tests were also reproduced on the v185 XEX:
`build/v186-baseline-check.log` and `build/v186-baseline-check-extra.log`.
They concern basketball (4), memory gaps/decoded ribbon frames (4), the old
act 5 motif boundary (1) and the callback cycle limit (1).

The 21 000-cycle limit test also failed with the earlier whistle:
for 4862/5236 v185 uses 22 054/23 000 cycles, and v186 22 102/23 098.
These are py65 instruction costs, not a measurement of real raster deadlines
with DMA. The full suite is not green; this scene has passing functional tests
and music compatibility. No assessment on physical Atari was performed.

Previews after executing the 6502 callbacks, with PMG overlaid:
`build/v186-encounter.gif` and `build/v186-encounter-preview.png`.
They are not an emulator capture and do not model ANTIC DMA.
