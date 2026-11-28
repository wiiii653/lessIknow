> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V165 — different satellite orbits at the dunk

## Image

Before the backboard shatters, the dunk ball has four orbiting missile satellites:

- a wide ellipse, clockwise in the screen y coordinate system;
- a taller ellipse, counter-rotation;
- a strongly flattened ellipse, twice as fast;
- a tilted ellipse, counter-rotation.

Each satellite is a three-row diamond of double missile width.
They inherit the ball's four cyclically changing colours. Their positions are
offsets from the current ball centre, so all orbits
move together with it through the boy's successive poses.

[READ] The orbits work only in dunk phases 0–74, up to the first
crack in the backboard. From phase 75 the missiles take over the previous trajectories and shapes of the glass
shards, with their former width restored.
Dribbling still uses the previous specks. The ball and arena graphics,
the backboard shatter phases, ticks, dunk length and scene boundaries are preserved.

32 trajectory phases are selected by the player counter `tick >> 3`. A full normal
orbit lasts 256 ticks (about 1.28 s), the fast one 128. The change does not use
an extra frame counter or alter the music ticks.

## Memory and publication

[READ] Only loader bank 1 (hero) changed. All
other 63 banks and non-banked RAM are identical byte for byte to v164.

- Hero controller: 2859 B, `$4000–$4B2A`, 207 B more than v164.
  85 B remain before the data from `$4B80`.
- The existing images, ball and backboard fixes still end at `$7E3B`.
- Orbit tables: 256 B, `$7E40–$7F3F`, four pairs of x/y tables with 32 samples each.
  4 B of gap remain after the backboard fixes and 192 B at the end of the bank.
- The installer checks the separation of the existing data and the new tables
  and the end of the bank `$8000`.

Net cost: **207 + 256 = 463 B**. Recovery relative to v141:
**34 305 B = 33,50 KiB**. Still 64 banks; main still 2546 B.

Hero PMG is still written in the existing range `$0980–$0BFF`.
Before clearing it, the window was limited to VCOUNT 124–127:
a late entry waits for the next blanking instead of starting the update
at the end of the current one. No GTIA HPOS reads or musical DLI changes were added.
PORTB is restored by the existing trampoline.

## Validation

The tests run 6502 callbacks through the whole orbit cycle. They check four
different trajectories, opposite signs of rotation direction, twice the speed
of one orbit, the full diamond shapes, missile widths and PORTB.
Additional cases cover jumps between poses at phases 47/61 and the last
moment before the shatter, and then the restoration of the shards at 75/81/87/93.

The moving-VCOUNT regression checks late entries for four ball
positions and completion of the write before the first satellite of the next frame.
[READ] An additional check of 24 cases has a minimum CPU margin
of 23.9 lines. This model does not include ANTIC DMA or the cost of all NMIs.

[READ] Hero and finale tests before adding the VCOUNT regression:
18 passed in 4.530 s.
[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
11 964 744 identical bytes relative to v035, about 3332,9 s of emulation,
covering the whole tune. This is a comparison of register data, without listening.

Preview `build/v165-dunk-orbits.gif`, combined frame
`build/v165-orbits-to-glass.png`: after the 6502 callbacks, with approximate
colours and pace. It is not an emulator recording.
[CONCLUSION] py65 and POKEY compatibility do not confirm the actual FPS
or DMA/raster deadlines. No test on physical Atari.

[READ] Full `make check`: 127 tests, 124 passed,
3 skipped (missing archival v126), 96.416 s.

## Release

`build/visual-prototype-v165.xex` and the corresponding JSON are identical
to the tested dev working files. Previous releases preserved.
XEX SHA-256: `dd5182f53a36d54f2fa3012b70a5761c958f52b51a6a7e62f72ac370d14d829c`.
