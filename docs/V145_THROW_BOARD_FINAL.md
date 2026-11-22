# V145 — throw toward the camera, shattered backboard and the boy in the finale

Script changes approved and commissioned by the user on 2026-11-07.
The act boundaries were not moved, nor were the existing shots or the four
music ticks per PAL frame. The full v035 player and 64 banks are still used.

## Third ribbon shot — camera from above

[READ] At 17950–20942, after the group and the solo, the camera looks down at
the group on the dance floor. The new poses have a visible face turned toward
the lens, spread hair and foreshortened legs. The bases and court lines are
under the character. The final frames 12–15 enlarge her toward the camera, while
the background and bases shrink. Poses 8–11 and the additional 35 also have the
new perspective. The other two shots and the side dance are preserved.

[READ] The clock selects the same steps as before; the four flight stages remain
at the end of the third shot. The new graphics replace existing compositions in
the 36-frame set, without adding banked bitmaps. The ribbons and sparks still use
double PMG and the raster rainbow.

## Dunk shatters the backboard

[READ] The first contact with the backboard happens in the existing hoop-grip
pose: dunk phase 75, tick 23638. Phases 75–80 show a radial crack, 81–86 the
shattered board, and 87–93 the remaining pieces and shards. The hoop, net and
the rest of the silhouette remain legible. Four missiles eject coloured debris
from the basket, with sideways motion and falling. The ball still uses four
players and the existing trajectory.

[READ] The three rectangular 48×24 patches occupy 3 × 288 B = 864 B.
They are overlaid on the full final pose in the inactive bitmap. The cache key
includes the destruction stage, so a held one does not block further decay.
Between stages the PMG shards update without recopying the background.

## Finale on the dance floor

[READ] Shot 8C starts at tick 59085 (~4:56.25). The boy in his
cyan-pink outfit lies on his back on the hall floor. Four independently
coloured stars orbit an ellipse around his head; these are moving players,
not stars drawn into the bitmap. The animation runs over the held background.

[READ] The final 128 ticks contain a fade; once it completes, the field colours
are zero and PMG is off. After tick 59833 the image remains black, also on
subsequent callbacks. ANTIC and the music DLI layout remain active. The star
masks are prepared off-screen and published in the VCOUNT 124–127 window; the
bitmap also comes into being only in the inactive buffer.

This is the realisation of the last frame. Acts 5C/5D, 6–7 and the earlier
credits/greetz boards in 8A/8B still need to be made. Their ranges were not
taken by the new scene. The `AUDIT_GAPS_V144.md` audit remains the historical
v144 state.

## Memory and engine

| Change relative to v144 | Cost |
|---|---:|
| New perspective within the existing ribbon bitmaps | 0 B net |
| Three backboard patches | +864 B |
| Dunk and shard code/tables | +428 B |
| Finale controller | +812 B |
| Finale bitmap | +2560 B |
| Removal of dead pom-pom dispatch, after adding the new dispatch | −66 B |
| **Net cost** | **4598 B** |

[READ] Relative to v141, **25 303 B = 24.71 KiB** is still recovered. These are
scattered places in the current banks; neither the bank count nor the RAM
requirements were reduced. Source PNG/RGB files are not Atari memory.

- Loader bank 1: basketball helper `$4000–$4A4C` (2637 B), data
  `$4B80–$7E3B` (12 988 B); new patches `$7ADC–$7E3B`. 307 B of
  gap remains before the data and 452 B at the end of the bank.
- Loader bank 39: finale bitmap `$4A00–$53FF`, instead of the free slot.
- Loader bank 49: finale controller `$5B80–$5EAB` (812 B), after the ribbon
  controller ending at `$5B3D`, before the Trevor code from `$6000`.
- Non-banked main code `$1400–$1DBD` (2494 B), 66 B of headroom to `$1E00`.
  The unused old pom-pom dance path is removed; its archival standalone
  project remains complete.
- The copy trampoline has a separate route `FRAME_KEY=36` to the finale bitmap.
  Normal ribbon frames still have numbers 0–35. The bank-switching code
  executes outside the `$4000–$7FFF` window; the NMI restores PORTB.

## Graphics sources and prompts

Both images were generated in **built-in imagegen**. The references are the
existing dancer sheet v136 and basketball player sheet v024; no CLI/API fallback
was used.

- Sheet of eight poses from above:
  [act2_ribbon_overhead_v145.png](../assets/art/source/act2_ribbon_overhead_v145.png).
- Full prompt:
  [act2_ribbon_overhead_v145.prompt.txt](../assets/art/source/act2_ribbon_overhead_v145.prompt.txt).
- Boy lying on the floor:
  [act8_boy_floor_v145.png](../assets/art/source/act8_boy_floor_v145.png).
- Full prompt:
  [act8_boy_floor_v145.prompt.txt](../assets/art/source/act8_boy_floor_v145.prompt.txt).

Floors, perspective, scale, ribbons, cracks, shards and stars are produced
in the generator code. The source basketball player illustration at the dunk
is preserved.

## Previews and release

- `build/v145-overhead.gif`: third shot and the flight toward the camera.
- `build/v145-shatter.gif`: dunk and backboard decay.
- `build/v145-final.gif`: last frame and fade.
- `build/v145-story-beats.gif`: three fragments joined for review.
- `build/v145-scenes.png`, `build/v145-board-storyboard.png`: control frames.

The previews come from sequential execution of 6502 callbacks in py65.
The palette and timing are approximate; they do not account for ANTIC DMA or the
real presentation time. They do not replace an emulator recording or an Atari
test.

Release: `build/visual-prototype-v145.xex` and JSON, 1 109 034 B.
SHA-256: `f9d1a723bb6604759eaf56897c1ce27e2d350323a1f0712690c2078eb5f57c47`.
The numbered release is byte-for-byte identical to the working build that was
checked.

## Validation

[READ] Final `make check`: **109 tests, 106 passed, 3 skipped**
(missing archival v126), 87.627 s. Eight new tests check the backboard stages
and the dunk boundary, the shards over the held bitmap, the character growing,
the orbit of the four stars, fade and permanent black, transitions/restart, no
writes to active buffers, register publication at a moving VCOUNT, and the
original decoder's NMI during the finale copy. The mosaic palette tests end
before the new scene 8C; its intentional fading has separate assertions.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **15 572 808
identical bytes** relative to v035, the whole track. This is a register
comparison, without listening and without a test on a physical Atari. The new
shots were watched in callback previews; smoothness and the real raster
deadlines remain to be assessed with DMA.

[READ] py65 CPU-only samples, without DMA/NMI:

| Sample | Cold entry | Held frame, +4 ticks |
|---|---:|---:|
| Crack, tick 23638 | 55 744 | 5527 |
| Decay, tick 23734 | 55 799 | 5565 |
| Shards, tick 23838 | 55 765 | 5554 |
| Finale, tick 59085 | 43 602 | 4950 |
| Black end, tick 59833 | 43 564 | 4912 |

These are not FPS measurements nor proof that the updates fit in one PAL frame.
