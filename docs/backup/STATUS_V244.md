> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# Project STATUS — state as of v244 (10.11.2026)

Demo: "The Less I Know The Better" at Silly Venture. Last commit
`e6cd188 Add v244 demo build` (9.11.2026). Full test suite green:
189/189; stereo POKEY audio comparison with the original byte-exact
(10,589,472 B). Physical Atari test not yet performed.

## Completed stages

| Part | Status |
|---|---|
| Intro (plasma, Crane, fireworks) | done (V140–V149) |
| Act 1 (meeting, whistle with PMG notes) | done (V176–V188) |
| Act 2 (ribbon dance, solo, heart throw) | done (V142–V173, V233) |
| Act 3 (basketball, dunk, backboard smash) | done (V156–V196) |
| Act 4 (Trevor, BUM/BAM speech bubbles) | done (V168, V190–V192) |
| Act 5 (bananas bunch/peeled, tunnel with ball) | done (V236/V239/V243/V244) |
| After Trevor (tunnel/banana director) | done (V231/V240) |
| Outro (terminal with credits/greetz, finale, fade) | done (V216–V242) |

## Open items before SV

1. **Scenes 5C "Trevor Mosaic" and 5D "Eyes"** — planned, never
   implemented. The segment around 3:30 shows a continuous organic tunnel.
   Decision: do them before SV or leave the tunnel as a stand-in (currently it
   looks coherent thanks to V194/V231).
2. **Test on physical Atari 1088XE** — so far only py65 (without the
   ANTIC DMA model) and Atari800 (audio comparison with v035 and raster attempts).
   FPS and raster stability must be confirmed on hardware before SV.

## Memory

- All 64 extension banks allocated. Free ranges in the start
  image: **119,226 B ≈ 116.4 KiB**; after subtracting whole banks 40–48
  (title/staging overlay) and 3–10 (raw bananas), the conservative pool outside
  these overlays is **61,497 B ≈ 60.1 KiB**. These are scattered gaps,
  not one continuous area; details and limitations:
  `docs/backup/BANK_MEMORY_FREE_V244.md`.
- Main code: `$1400–$1DFC` (2557 B), free **3 B before the row pool**
  `$1E00` — any further unbanked element requires a refactor.
- Gap: according to the notes, before `$4B80` in bank 1 (hero) there should be a free
  skip; a measurement from the v244 XEX shows content there. When planning
  new data in bank 1, this map must first be refreshed (base:
  `docs/backup/BANK_MEMORY_FREE_V244.md`).
- Reserved after the title (do not occupy): banks 40–48, `$4A00–$53FF`
  of bank 39, `$7800–$7FFF` of bank 2, fireworks zones 40/41.

## Plan before SV

1. Make the 5C/5D decision (do them or formally drop them).
2. Run the demo on a physical 1088XE in the SV configuration (PAL, 1 MB,
   stereo POKEY) and listen to the whole run.
3. (Option) Measurement of real FPS on hardware — so far only
   CPU cycles in py65 are measurable.

## Auxiliary files from the day's review

- `docs/TIMELINE_MAP.md` — map of shots in m:ss + rotators A–D.
- `docs/backup/BANK_MEMORY_FREE_V244.md` — free-per-bank report.
- `docs/backup/GREETZ_AND_CREDITS.md` — credits content (committed).
