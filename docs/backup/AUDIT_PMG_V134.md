> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# Ball, rotator and tunnel audit — v134

Update: the path that disables the ball and the too-late start of PMG writes
were fixed in v135. Results and validation scope: `V135_STABLE_PMG.md`.
The audit below describes the state of v134.

## Confirmed bug: disabling the ball for a visible frame

[READ] `tools/mosaic.py:159–160` sets `$D01D=0` and `$D400=$22`:
it disables PMG display and its DMA. This also applies to the cache hit.
Then the dispatcher (`tools/build_bitmap_sequence.py:687–688`) calls a
separate ball helper. This again waits for `$D40B >= 124`
(`tools/tunnel_ball.py:51`), clears the memory, draws the ball and satellites, and only
at the end restores `$D01D=3`, `$D400=$2E` (lines 73–74).

[READ] Both waits accept any line 248–311, with no upper bound
and no common acknowledgement of the background and PMG. If the end of the frame falls between
these waits, the ball remains disabled for the next visible frame.

[READ] Reproduction on 6502 code from the current XEX: warm callback,
tick 38904, start at line 306. Simplified raster counter:

| Event | Line from the start of the run |
| --- | ---: |
| `$D01D=0` | 311.85 |
| entry into the ball helper | 312.11 — already a new frame |
| first PMG write after the wait | 560.17 — line 248 of the next frame |
| `$D01D=3` | 623.32 — line 311 of the next frame |

[CONCLUSION] There is a reachable path that disables the ball for almost a full PAL
frame, about 20 ms. This matches the reported flicker and the exposure of the hole
in the tunnel. The code is shared by the rotator and the tunnel. It does not require a bug
in the ball mask or corruption of the banks. The banana changes did not create this structure,
although their additional instructions may shift the entry phase into the existing race.

## Artefacts above the ball — established scope, cause unconfirmed

[READ] Above the ball two stars deliberately appear, composed of four
missiles (`tools/tunnel_ball.py:61–68`). The mere appearance of a coloured cross
does not prove a bug; irregular streaks or truncated shapes require separate
confirmation in the raster image.

[READ] Clearing and writing PMG take place in a single area `$0980–$0BFF`,
without a second buffer. From the first write to the last write of PMG memory,
7102 instruction cycles elapse in the examined phase, about 62.3 lines without DMA/NMI.
With the callback starting at line 305, PMG returns only at line 62.66 of the next
frame. The highest stars may begin around line 48 (taking into account the
vertical movement of the rotator), and their exact position depends on the phase.

[CONCLUSION] The code does not guarantee restoring PMG before the first line of the satellites;
a late enable may cut off their top. DMA and NMI further reduce the margin.
This is a concrete candidate for the second symptom, but it is not yet confirmation
of the cause of all reported artefacts. No capture of a
defective frame in an emulator with full ANTIC/GTIA was performed.

## Why the tests did not detect this

[READ] `tests/test_sequence.py:33` sets VCOUNT permanently to 124.
The tests observe the state after the callback has finished. They do not see PMG being disabled
during it, nor the crossing of the frame end. The stereo POKEY comparison does not check
the image. The existing hole test checks the finished mask, not the timing of its display.

[READ] An additional run of ticks 38892–39912 every 4 ticks: 256 finished
ball states; no exposed pixels of the examined hole according to the PMG mapping
used by the existing test. In this range no bug was found in the
size/position of the finished mask. This is not a test of all raster phases.

## Reproduction and further repair

`/tmp/opencode/tliktb-venv/bin/python tools/audit_tunnel_pmg.py`

Results: `docs/AUDIT_PMG_V134.txt`. The model shifts VCOUNT every 114 instruction
cycles, 312 PAL lines. It does not model DMA, WSYNC, PMG reads or NMI;
it demonstrates the ordering bug and the reachability of the path, not the frequency of the symptom
in Atari800 or on physical Atari.

[CONCLUSION] The fix should prepare the new content without blanking the previous
ball, and acknowledge the background, PMG and position registers in a common, bounded
raster window. A test of crossing line 311/0 is needed, as well as observation of
the first satellite lines with DMA and music running.

No effect code or XEX was changed as part of this audit.
