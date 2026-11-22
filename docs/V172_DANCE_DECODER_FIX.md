# V172 — dance decoder routing fix

## Cause of the v171 bug

The new solo frames were compressed and placed in the tails of banks 8–11, which
belong to the six dance bitmap banks. After selecting them, the selector ran the
decoder at `$5E00`, but in those banks that address contains graphics, not
decoder code. The processor therefore executed image bytes as instructions. This
was a bank addressing bug, not memory exhaustion.

## Fix

The four streams kept their fast LZ form but were moved to the free tails of
loader indices 32–35, directly after the existing compositions. Those banks
already contain the decoder at `$5E00`. The selector, frame IDs, timings and
bitmaps remain the same. The original banks 8–13 again keep their unchanged six
frames and a full, free 1 KiB tail each.

The new data occupy 970, 940, 889 and 1006 B. The payload ends remain below
`$5400`; each bank's driver still fits the decoder at `$5E00–$5E8B`.
Total confirmed free gaps: 27 463 B. The scene length and all ticks remain
unchanged.

## Release and validation

Fixed XEX: `build/visual-prototype-v172.xex`.

The build completed successfully, 309 shared rows, 2552 B of code. An attempt to
run the py65 tests did not reach execution: the environment does not have
`py65` installed, so the test module cannot import `TrackedMemory`.
Playback in the emulator or on Atari has not yet been confirmed.
