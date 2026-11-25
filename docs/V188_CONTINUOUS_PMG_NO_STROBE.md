> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V188 — removed gap in note display

## Cause and fix

The main `colors` path zeroed GRACTL ($D01D) and disabled PMG DMA
with a write of $22 to DMACTL ($D400) before it called the note renderer. This
prepared a second buffer and waited for the next safe blanking phase.
As a result, double buffering worked, but the previous image was already disabled.

The instruction trace of v187 with a moving VCOUNT showed PMG disabled
for 267–313 lines, that is almost the entire PAL frame. Static previews and
the previous tests checked the state after the callback finished and skipped
that period. This was a DMA control ordering bug, independent of the notes and masks.

V188 bypasses these two resets in the whistle scenes 10–11. The previous note
buffer stays active while the next one is built and while waiting for blanking.
After the image is prepared, PMBASE and the registers are switched.
On exit to scene 12 the resets still apply and the melody ends at the
door. The sizes, colours, shapes and tracks of v187 remain preserved.

## Evidence and tests

- `build/v187-whistle-raster-audit.json`: disabled periods of 267–313 lines.
- `build/v188-whistle-raster-audit.json`: zero GRACTL/DMACTL disables
  during the continuous whistle.
- The new `tests/test_whistle_raster.py` reproduces the bug on v187:
  `build/v187-whistle-raster-regression.log`.
- On v188, 48 cases pass: 3 ticks (including the bitmap change),
  8 initial raster positions and variants with 0/5000 cycle delay.
  The test traces all writes during the callback: no DMA disables,
  the old buffer untouched, publication only after the new one is complete
  and in the lower blanking, PORTB preserved.
- A separate test confirms the melody is disabled at the door.
- 19 focused tests passed, including the previous tests of the
  notes, masks, panorama, ball and the tunnel's scrolling raster.
  Log: `build/v188-focused-check.log`.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 336 440 identical
  bytes relative to v035, the whole track. `build/v188-playback-check.log`.
- `make check`: 142 tests, 129 passed, 10 failed,
  3 skipped due to the missing v126. The set of failed test names is
  identical to v186; they concern the previously described basketball, ribbon,
  memory, CPU budget and old act 5 budget tests.
  Log: `build/v188-check.log`; details of the earlier defects in the v186 report.

VCOUNT tracing is a simulation of CPU time with synthetic delay,
not a full ANTIC DMA model. No evaluation was performed on physical Atari.
POKEY agreement is not proof of raster smoothness.

## Build and memory

- `build/visual-prototype-v188.xex` and JSON; dev identical.
- SHA-256: `172e97bd75b3c188b6bf815e3dbc5b116b311ad15a75bb5f10bdec16605de6b1`.
- The fix occupies the last 8 B of the main code: 2560 B in $1400–$1DFF.
  There is no headroom left before the row pool at $1E00.
- Bank 0 containing the notes is byte-for-byte identical to v187. The helper
  calls in other banks have recomputed label addresses shifted
  in the main code. Bank allocation and 298 rows / 11 480 B unchanged.
