> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# Free memory in expansion banks — report (state v244)

Counted directly from the finished artifact `build/visual-prototype-v244.xex`:
all XEX sections were parsed and **50 bank images** were extracted
(16 KiB each, loaded by the extended loader `school_portrait_bank`
into the `$4000–$7FFF` window of the expansion cells), and for each image
uniform pages (`00`/`FF`) and zones of fill bytes were found. The results
were confronted with the generator code (file reads) and the current V notes
— without running the builder.

Notation: **[READ]** = measured from the XEX; **[CONCLUSION]** = conclusion
(drawn from measurements/documentation); address boundaries in `$` notation.

## Methodology [READ]

- parsing XEX sections (`start/end` headers + payload),
- loader identification by the probe instruction (`0xC0, 14+index, 0xD0`)
  → loader index 0–49,
- banks 0/1 (special comic variant) identified by position in the installation
  order (girl, hero),
- uniform pages (`$00`/`$FF`) are candidates for free space, not
  automatic proof of free ownership: they must be checked against the code,
  image data and generator padding. The balance below excludes the final
  image page in bank 39 and the helper padding in banks 40/41,
- additional, non-full-page ranges were counted from owner boundaries and
  checked against the XEX payload.

## Per-bank table

| Index | What is in it | Free [B] | Free slots |
|---:|---|---:|---|
| 0 | school opening: boy portrait + opening code data; **PMG melody helper** `$6A00–$6E8E` (V185–V187) | **5632** | `$4A00–$5FFF` [READ] |
| 1 | basketball player: 2892 B of code (V165/V189), art `$4B80–$7E3B` including three table patches `$7ADC–$7E3B`, orbits `$7E40–$7F3F` | **196** | `$7E3C–$7E3F` (4 B), `$7F40–$7FFF` (192 B) [CONCLUSION: measured fills, see drift below] |
| 2 | side registration: rebound `$4000–$402B`, selector `$4040–$4599`, packed frames `$4600–$5AA6` and `$6000–$6E0E`, LZ decoder `$5E00–$5E8B`, tunnel/buki helper `$7800–$7FFF` | **3896** | `$402C–$403F` 20 B, `$459A–$45FF` 102 B, `$5AA7–$5DFF` 857 B, `$5E8C–$5FFF` 372 B, `$6E0F–$77FF` 2545 B. Sum: **20+102+857+372+2545=3896 B**; all ranges are zero in the v244 payload [READ] |
| 3–10 | **bananas** (V243/V244): dense pack/RLE + in v244 raw fist frames; helper `$7840–$7BFE`, entry `$7C00–$7C6B`, selector `$7C80`, decoder `$7D00`, loop `$7E00`, dispatch `$7F00`, pointers `$7F80–$7F8F` — **8 banks** | **3755 total (~469/bank)** | [READ: pages full; 3755 B per the V243 note] |
| 11–18 | **tunnel (kaleidoscope)**: 4 half-frames per bank at `$4000/$4F00/$5E00/$6D00` (3840 B each) + shared 1024 B of code at `$7C00–$7FFF` — **8 banks** | **0** | [READ = full] |
| 19–23 | corridor/walk background (`school_parallax`, entry `$7000`) — **5 banks** | **5376 / bank** | `$6800–$6FFF` (2048), `$7300–$7FFF` (3328); total across 5 banks **26 880** [READ] |
| 24–31 | dance side actor (V142/V143): pixels/masks `$4A00–$51FF` — **8 banks** | **1536 / bank** | `$5200–$53FF`, `$5E00–$5FFF`, `$7E00–$7FFF` (512 B each); total **12 288** [READ] |
| 32–34 | side actor + packed middle frames from `$4A00` + quarter streams (V173) | **1396 / bank** | `$5200–$53FF` 512, `$5E8C–$5FFF` 372, `$7E00–$7FFF` 512 [READ] |
| 35 | as above | **1140** | `$5300–$53FF` 256, `$5E8C–$5FFF` 372, `$7E00–$7FFF` 512 [READ] |
| 36 | as above | **1908** | `$5000–$53FF` 1024, `$5E8C–$5FFF` 372, `$7E00–$7FFF` 512 [READ] |
| 37–38 | as above | **2164 / bank** | `$4F00–$53FF` 1280, `$5E8C–$5FFF` 372, `$7E00–$7FFF` 512 [READ] |
| 39 | **final boy bitmap** `$4A00–$53FF` (2560 B, do not clear) | **1024** | `$5E00–$5FFF` 512, `$7E00–$7FFF` 512 [READ] |
| 40–41 | title plasma banks + **fireworks** (V164–V166): helper segment `$6C00–$7193` (including the zero padding `$6E00–$6FFF` up to the publication entry `$7000`), anchors `$7280–$7380`, shapes `$7400–$7FFF` | **363 / bank** | `$7194–$727F` 236 B and `$7381–$73FF` 127 B. The `$6E00–$6FFF` padding (512 B/bank) is part of the helper reservation and is not counted as free without changing the installer [READ] |
| 42–43 | title plasma (without fireworks) | **5120 / bank** | `$6C00–$7FFF` [READ] |
| 44–48 | remaining plasma (title banks 40–48 only up to tick 2992!) | **9984 / 6400 / 7936 / 9216 / 9472** | windows: `$4300–$49FF/$4F00–$53FF/$5900–$5EFF/$6200–$68FF/$6D00–$71FF/$7700–$7FFF` according to the measurement (especially bank 44) and smaller in 45–48 [READ] |
| 49 | ribbon controller `$5400–$5CCB` (2252 B), finale controller 814 B `$5CD0–$5FFD`, Trevor engine 2500 B `$6000–$69C3`, finale orbit data 48 B `$69C4–$69F3`, ribbon streams `$6A00–$7DFF`, anchors `$7E00–$7F1F`, wind `$7F20–$7F9F`, glyph data 95 B `$7FA0–$7FFE` | **17** | free: `$5CCC–$5CCF` 4 B, `$69F4–$69FF` 12 B, `$7FFF` 1 B. The last 2 B of the controller slot (`$5FFE–$5FFF`) remain reserved [READ from generators/JSON] |

## Totals

- The raw scan found **114 432 B** in full `$00`/`$FF` pages. That is the number
  of candidates, not free memory: we subtract 256 B of the `$4A00–$4AFF` page of bank
  39 (it belongs to the final bitmap) and 1024 B of `$6E00–$6FFF` padding in banks
  40/41 (it belongs to the helper reservation). **113 152 B** of confirmed
  full-page gaps remain.
- Additional ranges, without recounting full pages: bank 1 **196 B**;
  bank 2 **568 B** beyond its 13 full pages (3896 B in total);
  banks 3–10 **3755 B**; decoder tails in 32–38 **812 B**;
  banks 40/41 **726 B**; bank 49 **17 B**. Together with the full pages:
  **119 226 B ≈ 116.4 KiB** of free ranges in the boot image [READ +
  explicitly indicated owner boundaries].
- **Conservative pool outside banks with lifetime overlap:** after subtracting
  whole banks 40–48 (**53 974 B**) and banana banks 3–10 (**3755 B**),
  **61 497 B ≈ 60.1 KiB** remains. This is the sum of scattered gaps outside those
  overlays, not one continuous area nor a complete measurement of every possible
  runtime slot. Banks 40–48 after the title are **reserved** (V244: "Do not add
  post-title assets to banks 40–48").

## Discrepancies between documentation and measurement [READ]

- **Bank 1 (hero)**: the notes (V165/V189) describe 52 B / an "85 B code gap"
  before `$4B80`. The measurement shows non-zero content at `$4B4C–$4B7F`
  (15 unique values) — that space is currently in use, not free.
  What remains free is `$7F40–$7FFF` (192 B) and 4 B between the patches of
  table `$7E40` and its anchor.
- **Bank 49 (finale controller)**: V216/V240 describe 816 B as the reserved
  slot `$5CD0–$5FFF`; the current v244 generator/JSON emits 814 B, ending at
  `$5FFD`. The last 2 B of the slot remain reserved, they are not added to
  free memory. The finale orbit data also occupy 48 B of the former gap
  `$69C4–$69F3`; therefore 12 B remain in this place, not about 60 B.
- **Banks 24–31 and 39** — the `$7E00–$7FFF` zone is not included in the
  description of the free 512-byte "old ball slots"; the measurement confirms
  512 B free in **each** of banks 24–39 (9 of them).

## What not to occupy

- bank 48 (`$4000–$4EFF`, auxiliary templates `$6000–$67FF`) — staging
  and banana helper templates (V244),
- `$4A00–$53FF` in bank 39 — final bitmap (V145/V197),
- `$5E00–$5E8B` in banks 32–38 — LZ decoder (140 B/bank); behind it free
  `$5E8C–$5FFF` (372 B/bank) — this free space can be taken,
- `$7800–$7FFF` of bank 2 — rotator/tunnel ball helper (V150),
- `$6C00–$7193`, `$7280–$7380`, `$7400–$7FFF` in banks 40–41 — fireworks,
- everything in bank 49 outside the gaps in the table above.

## Code references (read)

The loader index ↔ content map follows from the call order in
`tools/build_bitmap_sequence.py:857–876` (girl/hero/ribbon/mosaic/school_pan/
actors 24–39/plasma 40–48/control 49), from `tools/mosaic.py:216–228`
(16 banks: 8 bananas + 8 tunnel, half-frames and code `$7C00`) as well as
`tools/final_boy.py:25–26` (`BITMAP_BANK=39`, `BITMAP_SOURCE=0x4a00`) and
`tools/school_portrait_bank.py:9–48` (bank loading/probe format).

The report was revised by reading the XEX and the generator boundaries; neither
the full builder nor the tests were run.
