# V161 — return to graphics without dithering

At the user's request, the raster of shade transitions on the bananas and on the
edges of the tunnel fan, added in v159, was removed. Smooth colour fields were
restored. The v160 PMG cycle, the beating heart and the hole coverage by the
current effect remain preserved. The separate covering ball and the cycle
fireworks were not restored.

[READ] A comparison after loading the XEX confirms:

- all 64 frames and the full rotator/tunnel banks (loader 3–18) are identical
  byte for byte with v158, from before the dithering;
- all other banks and the entire unbanked RAM are identical with v160.

This is purely a replacement of bitmap data. No changes to Atari code, bank
sizes, RAM requirements, music progression and scene ticks. The memory map and
the v160 balance are still current.

[READ] `make check`: 124 tests, 121 passed, 3 skipped
(no archival v126), 90.701 s.

No listening test or POKEY comparison was repeated: neither the code nor the
music data was changed. The last v160 stereo POKEY check covered the whole song.
py65 tests do not model ANTIC DMA and do not determine FPS on a physical Atari.

## Release

`build/visual-prototype-v161.xex` and JSON.
Preview: `build/v161-smooth-textures.png`, after a 6502 callback, approximate palette.

XEX SHA-256: `ba6f25cf957b46d316b1b21858f596edb95bac03715d91094f56f1f68823751b`.
The numbered XEX/JSON are identical to the dev working files.
