> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# Entering the gym after the pre-school scene — v010

Date: 2026-11-04. Result: `build/visual-prototype-v010.xex`.

## Transition and image

- [READ] The last frame of the girl at the entrance remains until tick 5983.
  From tick **5984** (about 30 s) scene 13 shows the interior of the gym: two
  basketball players, a shot and the ball bouncing, and two girls stretching
  by the wooden ladders. This frame replaces the freeze on the boy.
- [READ] Practice takes 2992 ticks, about 15 s. The dance starts at
  **8976**, the next dancer joins at **9724**, the third at **10472**;
  none of these thresholds was shifted.
- [READ] The characters and the gym are a bitmap; the ball is an animated PMG 0 player,
  moved along a 32-element trajectory according to the music counter. The remaining
  players are off-screen. At the moment the dance begins, player DMA is disabled.
- [READ] Source: `tools/gym_practice.py`. Preview:
  `build/v010-gym-practice.png`, a render from the callback and ANTIC lists in py65.
  RGB colours are approximate; the bitmap was also checked in Atari800.

## V2/V3 — banks and memory ownership

- [READ] The practice frame fits in the last 8192 B of bank 8 (offset
  `$2000–$3FFF`, CPU window `$6000–$7FFF`). The builder verifies that this area
  of the original contains only `$FF`. The v035 decoder ends reading bank 8
  at offset 2819, so the required end marker remains preserved.
- [READ] Banks 1–7 and the first 8192 B of bank 8 remain byte-for-byte
  identical. Banks 9–14 keep the dance frames from the previous version.
- [READ] Practice uses the existing two buffers `$9000/$B000`
  and the same copying interrupted by music. The test covers NMI
  during copying also from bank 8 and correct restoration of PORTB.
- [READ] The ball's PMG data occupy `$0A00–$0A7F`; the scene uses 2-line
  player DMA. The ANTIC lists and the musical DLI gaps were not changed.
- [READ] Callback with wrapper and trajectory: 1621 B, `$1400–$1A54`.
  NMI wrapper at `$19EF`. Static rows and table sizes without growth:
  425 rows, 16,515 B, tables 3264 B.

## V6 — playback regression and scene check

- [READ] Atari800, PAL, `-1088xe`, Altirra OS, stereo POKEY, headless.
  Comparison with v035: **6,139,440 identical bytes** of stereo
  POKEY registers, about **1710.2 s** of emulation; the whole track covered by the test. The initial
  silence was aligned once, without shifting samples during the track.
- [READ] In the Atari800 monitor the callback was stopped after returning to
  `$220D`, saving the display-list and bitmap memory. The practice images at
  snapshots 6016 and 6144 and the dance at 9152 matched the references pixel for
  pixel. At tick **8976**, scene **3** and entrance offset
  **192** were read, consistent with the earlier start of the dance.
- [READ] In the image tests the counter was set so as to visit selected
  scenes quickly; the POKEY comparison covered the normal run without changing the counter.
- [READ] 21 tests completed successfully: gym entrance boundary,
  dance boundary, ball trajectory and DMA, gym bitmap, bank interrupts,
  school, NORTH, title, all groups and dancer poses.
- [READ] No listening session or physical Atari test was performed.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v010.xex --seconds 10
```

[READ] The previous v009 XEX remained unchanged:
`258d94eb37b9efb080438c15276bea685dfd9ef3859a7bb9e5507e95361c2ed6`.
New v010: `3dd2dc3a81485621eb1371874114bdb56e14b3f2f46793bbed059c4b34ba1771`.
