> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# Audit of gaps against the plan — v144, 2026-11-07

Scope: `TLIKTB_Atari_Timeline_v2.md`, `TLIKTB_Technical_Constraints.md`,
current generators and assets, and the execution of the callback from numbered
XEX v144. No scenes, production code, act boundaries or priorities were changed.
The times below are musical approximations (bar × 1.875 s).

## Largest image gaps

| Fragment | Time | Plan | v144 state |
|---|---|---|---|
| 1B, bars 8–16 | 0:15–0:30 | Girl for the first time, Trevor in the background | Girl and boy are present; Trevor is missing in the school background. |
| 5A, change in bar 92 | 2:52.5 | New kaleidoscope source or a different reflection mode | There is a switch from phases 0–15 to 16–31 of the same banana rotator. No separate source or reflection mode. Partially done. |
| 5B, bar 108 | 3:22.5 | Change of tunnel texture | Still the same spiral generator and phase set 32–63. No separate event at tick 40388. |
| 5C, bars 112–116 | 3:30–3:37.5 | Trevor Mosaic | Shared substitute effect; no mosaic of Trevor's face/figure. |
| 5D, bars 116–120 | 3:37.5–3:45 | Eyes Sequence | No eyes sequence; the shared effect continues. The former portrait blinking does not realise this scene. |
| 6A, bars 120–124 | 3:45–3:52.5 | Three comic frames and character poses | No scene and no connected assets. |
| 6B, bars 124–128 | 3:52.5–4:00 | Trevor versus the basketball player | No duel; the shared effect continues. |
| 7A, bars 128–136 | 4:00–4:15 | Dedicated neon build-up | No separate dramaturgy; the palette cycle of the shared effect does not realise the planned build-up. |
| 7B, bars 136–144 | 4:15–4:30 | Giant Trevor, flash, culmination | No scene. Trevor's earlier punches in act 4 do not replace it. |
| 8A, bars 144–152 | 4:30–4:45 | Credits: group, music, Silly Venture | No credits board and no planned logos. |
| 8B, bars 152–158 | 4:45–4:56.25 | Greetz | No board/sequence. |
| 8C, bars 158–160 | 4:56.25–5:00 | Final flash and fade to black | No final image fade-out. The musical fade does not automatically fade the graphics. |

[CONCLUSION] The last roughly **90 seconds**, from 3:30 to the end, do not yet
have the planned scenes. This stretch should not be counted as finished acts
merely because something is displayed and the music runs.

## Evidence in the code and the numbered XEX

[READ] `tools/build_bitmap_sequence.py`, section `act5_select`:
after tick 41884 it goes directly to `mosaic_frame_ready`. The dispatch for
acts 6–8, the events for 5C/5D and the ending are missing. Earlier it handles
bars 92 and 104; it does not handle a separate change at 108.

[READ] `tools/mosaic.py`: frames 0–31 use a single `banana_tile` function,
and 32–63 a single tunnel generator. A change of palette or phase adds neither
a new texture nor an image of Trevor.

[READ] The 6502 code from `build/visual-prototype-v144.xex` was executed in
py65, with the real data of its banks. Below are samples exactly at the
boundaries of the planned scenes. Identifier 6 means the shared
mosaic/rotator renderer, not act 6.

| Bar | Tick | Scene identifier | Shared effect phase |
|---|---:|---:|---:|
| 108 | 40388 | 6 | 60 |
| 112 | 41884 | 6 | 25 |
| 116 | 43379 | 6 | 23 |
| 120 | 44875 | 6 | 52 |
| 124 | 46371 | 6 | 50 |
| 128 | 47867 | 6 | 15 |
| 136 | 50858 | 6 | 42 |
| 144 | 53850 | 6 | 5 |
| 152 | 56842 | 6 | 32 |
| 158 | 59085 | 6 | 44 |
| 160 | 59833 | 6 | 27 |

SHA-256 of the examined XEX:
`8db4ca4de50c7db85d02732e416a9734b1ceab91a9e9e999c59e0e32fc828f21`.
No new FPS measurement or new full music comparison was performed during the
audit. The release results remain in `V144_LARGE_CRANE.md`.

## What not to count as a gap

- The school logo/panorama from the original intro were deliberately replaced
  by the TAME IMPALA / title boards, the city, the Crane and the fireworks.
- The earlier pompom dance is replaced by the approved side shot of the
  ribbon; the original scene is in a separate `projects/pompom-dance`.
- Four performance portraits replaced the three approved shots of the ribbons
  and the heroine's launch. They should not be restored as supposedly missing
  scenes.
- Dribbling, the layup, Trevor's entrance and his punch combinations have
  working renderers. The rainbow balls, BANG/BAM and PMG breakup are additions
  already completed.

## Open decisions and technical verification

This is a separate group from the missing scenes:

- GTIA 9 in act 5: left in the plan for a decision, with no block indicated.
  There is currently no such scene or its sources.
- Actual presentation timings, FPS/skipped phases and CPU headroom with ANTIC
  DMA and four DLIs: unconfirmed on target hardware (V1).
- Full image inspection and listening in the target configuration and on
  physical Atari 65XE/1 MB/stereo POKEY: still to be done. Music register
  comparisons in Atari800 passed; they are neither a listening test nor a
  smoothness measurement.
- A dedicated test of START/pause and clock/video stop: missing (V4).
- Full v024/v035 comparison: blocked by the missing v024 (V5).
- Experiment with unequal DLI spacing: not performed (V6). The original four
  equal spacings are preserved and verified by tests.
- Compo rules and the final expansion configuration plus player UI layout:
  still open in the documentation. They were not settled in this audit.
- ZX0, separate `.pal`/`.pmg` and alternative formats in the specification are
  a proposed convention, not an implemented pipeline. They are not additional
  scenes.

[READ] The historical assumption of trimming the player to seven banks is
incorrect for v035: bank 8 with the end marker is required. This is not
outstanding work to be done. All 64 banks are still allocated; the recovered
29 901 B are scattered places, not whole free banks. The file
`TLIKTB_Asset_List.md` mentioned in the old plan is also missing; the audit was
based on the actual Makefile and generator inputs.
