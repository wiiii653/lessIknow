> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V158 — PMG effect cycle after Trevor

From the end of the fight, tick 32909, to the entry of the final boy at 59085,
the rotator/tunnel presents in sequence:

1. The large spinning tunnel ball.
2. A smaller throw ball with coloured panels.
3. City fireworks.
4. Comic BANG/BAM.
5. Expanding and shrinking clouds.
6. Circling finale stars.
7. Air rush and ejection fireworks.
8. Splatter of board fragments.

Each mode lasts 512 player ticks (about 2.57 s); the loop is 4096 ticks
(about 20.54 s). Phases change every 16 ticks. The ribbons are not part of the
cycle. Act boundaries, music and background images were not changed; the
addition does not replace the missing story scenes or the credits/greetz
screens.

## Centre occlusion

Player 0 remains a small, solid ball in the centre of the image, also during
mode changes. It covers the entire tunnel opening regardless of the remaining
animation. The other three players and four missiles show the effects. The
source shapes are fitted to this budget: the large ball has three colour layers
instead of four, and the lettering uses compact glyphs. The sources for the
balls, fireworks, clouds, wind and stars come from existing effects; they are
variants of their staging.

The entire PMG is prepared in the inactive `$08`/`$88` buffer. Only
at VCOUNT 124–127 is the complete image and the registers published.
The old image stays visible during preparation and waiting.

The earlier act 2 rotator and the cut after the ejection keep the original
v150 ball. The finale entry and the returns to earlier scenes restore
the proper masks and settings.

## Memory

The reference audit confirmed that the old `trevor_awakens` artwork/code in
loader bank 2 no longer rendered Trevor: his production code uses the
polished banks 24–39 and 49. Bank 2 was called only for the `$7800` ball helper.
That helper remained; after Trevor it redirects to the new renderer.
The historical generator remains as `legacy_bank()`; the sources and old
numbered XEX files were not removed.

- `$4000–$41D4`: cycle renderer, 469 B.
- `$4400–$63FF`: 64 mask frames, 8192 B.
- `$6400–$693F`: position, size and colour metadata, 1344 B.
- `$6A00–$6AFF`: address tables, 256 B.
- `$6B00–$6B0F`: opaque centre mask, 16 B.
- `$7800–$7FFF`: previous renderer for earlier scenes, 2048 B.

[READ] The bank occupies 12 325 B instead of 14 881 B, a recovery of 2556 B.
Still 64 banks, main 2546 B with 14 B of headroom. Net relative to v141:
15 461 B (15.10 KiB). The data/code of the remaining banks does not grow.

## Validation

The test of all 64 frames checks the mode order, full agreement of the player
and missile masks with the data, the constant core and the occlusion of every
pixel of the central tunnel opening. Separate tests cover the inactive buffer,
mode transitions, earlier scenes and the finale, late VCOUNT with artificial CPU
stalling, and real injected decoder NMIs with PORTB restoration.

[READ] `make check`: 122 tests, 119 passed, 3 skipped
(no archival v126), 90.811 s.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 202 576 identical bytes relative to v035, covering the whole track.
No listening test and no test on physical Atari. py65 does not model ANTIC DMA
or the real FPS; the tests do not establish raster stability on hardware.

## Release

`build/visual-prototype-v158.xex` and JSON.
`build/v158-pmg-cycle.gif` shows the full loop. `v158-cycle-a.png`
and `v158-cycle-b.png` present the eight modes. Previews after the 6502
callback, with approximate tempo/palette; they are not an emulator recording.

SHA-256 of the XEX: `41bf7d50144ba3737ceda6c9edc9ac331b0bc4482e5bf420b699c28e34be450d`.
The numbered XEX/JSON files are identical to the working dev files.
