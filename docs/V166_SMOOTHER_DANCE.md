> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V166 — real dance in-between frames

## Effect and synchronisation

The three later ribbon dance shots have 14 new in-between compositions.
Nine new anatomical poses of the heroine are used at various scales and group
arrangements. The original poses enter on their unchanged `STEPS` ticks, and
the new ones halfway through the 46/47-tick intervals.
This gives successive motion phases every 23/24 ticks, about 0.117 s, without
slowing the choreography and without lengthening the scenes.

The transition between two poses uses the same in-between image also
in the opposite direction. Six images concern the first group, four solos,
four groups before the throw. Identical consecutive poses and cuts between
shots remain without artificial interpolation. The quick preparation,
throw and close-up from above keep the earlier frames and ticks.

The side shot remains unchanged. The ribbons keep the earlier continuous
masks and rainbow DLI, while the hand anchors of the in-between poses match
the new images. The bitmap and PMG are prepared in inactive buffers;
a complete image with its matching ribbons reaches the screen.

## Source graphics

The built-in `imagegen` tool was used, following the imagegen skill,
based on the original sheet `act2_ribbon_dancer_v136.png`.
The new 3×3 sheet keeps the heroine, costume and style; it presents nine
new motion phases between the used poses. The original sheet was not changed.

- Source: [act2_ribbon_inbetweens_v166.png](../assets/art/source/act2_ribbon_inbetweens_v166.png).
- Full prompt: [act2_ribbon_inbetweens_v166.prompt.txt](../assets/art/source/act2_ribbon_inbetweens_v166.prompt.txt).
- The Makefile prepares `build/ribbon-inbetweens-v166.rgb`, a 1329×1329 grid.
- `ribbon_dance.actor(..., mid=True)` uses the same scale and sampling method,
  black detail protection and keyline as the earlier images.
- The new compositions are stored as native four-colour 160×64 bitmaps.

## Compact format and banks

14 full images would require 35 840 B. The new simple LZ stores them
in **16 886 B**. The stream contains literal runs of 1–128 B or backward
references to the already reconstructed bitmap. Copying a run happens in a fast
Y-indexed loop. The encoder prefers matches of at least eight bytes:
smaller files with lots of short matches consumed more CPU time.
Each stream is replayed at build time and compared with the bitmap.

[READ] The new data fits in the previously free gaps:

| Owner | Range | Occupancy |
|---|---|---:|
| Loader bank 2: selector, timings, anchors, descriptors | `$4040–$4436` | 1015 B |
| Bank 2: first four images | `$4600–$5AA6` | 5287 B |
| Bank 2: images 4–6 | `$6000–$6E0E` | 3599 B |
| Banks 32–38: images 7–13 | from `$4A00` in each | 8000 B |
| Bank 2 and 32–38: decoders | `$5E00–$5E8B` in each | 8 × 140 B |

Together **19 021 B filled former bank gaps**. The ribbon controller grows by
9 B: 2246 B, `$5400–$5CC5`, with 10 B before the finale controller
at `$5CD0`. The main code remains identical, 2546 B, with 14 B before `$1E00`.
The number of banks is still 64. The XEX stores fixed full banks, so lower
data occupancy in the banks does not mean a correspondingly smaller XEX.

The unbanked runtime remains in its previous reservation
`$0C00–$0EFF`. The added wrapper/entry uses `$0D60–$0DB9` (90 B, including
alignment), a private workspace `$0DC0–$0DCF` (16 B), and the previous
composer under `$0E00` gets 11 B of routing. Neither the runtime nor the main
code pool was extended. The gap owners are updated in `AGENTS.md`.

[READ] The remaining confirmed gaps in the banks:

| Area | Free |
|---|---:|
| Bank 2, below the original tunnel helper | 4251 B |
| Tails of the side actors and remaining parts of slots 32–38 | 14 016 B |
| Leftovers of the old ball mask slots | 7212 B |
| Tails of the six original dance banks | 6144 B |
| **Total** | **31 623 B = 30.88 KiB** |

The largest single gap in bank 2 is `$6E0F–$77FF`, 2545 B.
Do not treat the entire former 14 KiB or all Trevor slots as free.
Exact size of each compressed image:
`build/v166-allocations.json`. Older "net recoveries vs v141" refer to
historical balances, not to the complete current free-memory map.

## Calls, anchors and cache

The original image IDs 0–35 and the special finale ID 36 remain unchanged;
the tables in the tight main code were not enlarged. Python IDs 37–50 serve
to describe/preview the new compositions. The runtime stores the base
number of the old image in `$83ED`, and the `$80` in-between flag in `$83E5`.

The wrapper at `$0D60` keeps the bank on the stack and calls the bank 2
selector. This selects the proper stream and prepares eight anchors. After
returning, the wrapper restores the controller bank and updates its metadata.
Ordinary poses always recover their original anchors from the unchanged copy.
The cache accounts for the in-between flag, so the old and new pose do not
collide.

The composer recognises the flag before the ordinary copying. For a new frame
it selects the stream bank and runs the local decoder; the output passes
through the previous unbanked trampoline, which restores the controller bank.
For old frames, the side actor and the finale, the previous path remains.
The music NMI preserves the selected bank, and the ribbon colours use
the previous private stack.

## Validation

[READ] Dance-specific tests: 24 passed, 16.206 s.
[READ] Full `make check`: **132 tests, 129 passed,
3 skipped** (no archival v126), 101.725 s.

All new compositions were checked after the 6502 callbacks, the midpoint
timings, the original accents and cuts, full decompression agreement, anchor
matching, returns to old anchors, the cache, ownership of the inactive
bitmaps/PMG, PORTB restoration, late VCOUNT, and injected real music NMIs
during decompression from both bank 2 and the action bank. The ribbon masks
still have continuous vertical runs without missing rows.

[READ] All six original dance banks and eight side
pixel/mask actors are identical to v165. 32 consecutive samples of the
side shot were also compared: identical bitmap, active PMG and all GTIA registers.
Loader banks 2, 32–38 and 49 and the runtime gaps in use changed.
The main code is identical to v165.

[READ] The most expensive of the 14 checked new-frame callbacks:
**91 282 CPU cycles**; the others 75 583–80 959. A retained in-between frame
uses the cache and stays within 25 000 cycles. These are CPU costs in py65,
without ANTIC DMA; they are not a measurement of FPS or presentation latency
in the emulator.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
**15 057 720 identical bytes** relative to v035, about 4194.4 s of emulation,
covering the whole track. This is a comparison of register data, without
listening.
No test on physical Atari; the results are not a declaration of compo readiness.

## Previews

- `build/v166-dance-v166.gif`: three new shots, one dance cycle each.
- `build/v166-dance-v165.gif`: the same ticks and shots before the change.
- `build/v166-inbetween-contact.png`: old → in-between → old pose.

The previews are the result of real 6502 callbacks, with approximate tempo
and palette, without DMA emulation. They are not an Atari800 recording.

## Release

`build/visual-prototype-v166.xex` and the matching JSON are identical
to the dev files. After the full tests, only the reported free-memory fields
in the JSON were corrected; a rebuild produced an identical XEX, confirmed by SHA-256.
Earlier releases were kept.

SHA-256 of the XEX: `edafa81faca46c2335cf2e21e9f2cc29d99da1060c6f3fd7ebbe3b27ff6489c1`.
