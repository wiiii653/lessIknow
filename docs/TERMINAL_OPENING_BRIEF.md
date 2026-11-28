> **Historical design brief.** See the [current opening implementation](TERMINAL_OPENING_IMPLEMENTATION.md)
> and [current loader and opening copy](terminal_opening.md).

# Opening: loader star + 4-row terminal, then title with water

**Status:** design brief for implementation. No code has been changed for this
idea yet.

**Goal:** start the demo with the loading star still spinning while a 4-row
terminal types an opening message underneath, then dissolve into the title
scene over a city panorama with water reflections.

## Sequence

1. **Loading** — unchanged. The raster-synced loader candidate
   (`releases/less-i-know-demo-prerelease-171-stereo.xex` and later) keeps
   the animation clean.
2. **Opening interlude** — same star/mark on the upper screen, a 4-row
   terminal strip at the bottom typing the opening lines.
3. **Transition** — the terminal clears/scrolls away, the title scene takes
   the full bitmap, the city appears with water reflections below.
4. **Main demo** — no permanent terminal. The 4-row strip is not carried
   through the scenes.
5. **Ending** — the existing terminal credits/greetz.

## Why this shape

- The terminal already exists with a 4-row window (`HISTORY_ROWS = 4`), a
  font, typed timing, cached rows and paging. Reusing it costs far less than
  building a new text engine.
- The 4-row strip sits **below** the 192-row bitmap, so the scene art is not
  shrunk or cropped.
- Keeping the loader animation alive *inside the loader* is the expensive
  variant: the late low-RAM segments overwrite the loader font/VBI/delta at
  the end, and the terminal engine is staged late. A first demo scene can
  show the same thing without touching the loader contract.
- A persistent terminal across the whole demo competes with every scene and
  forces a split display list in every act. Do not do that for the first
  version.

## Current assets and code map

| Part | Where |
|---|---|
| Loader screen, font, star mark, VBI, delta, `$38A0` patch | `tools/animated_loading.py` |
| Loader wrapper/clear/copy, raster sync | `tools/build_hardware_xex.py`, `tools/build_compact_xex.py`, `tools/school_portrait_bank.py` |
| Terminal text and 4-row layout | `tools/outro_text.py` (`HISTORY_ROWS = 4`, `CREDITS`, `GREETZ`, `TEXT_DL`, `TEXT_ROWS`) |
| Typed terminal engine | `tools/terminal_typing.py` (`ENTRY`, `TIMES`, `LENGTHS`, `schedule`, `CACHED_LINES`) |
| Terminal staging | `tools/outro_loader.py` |
| Title, plasma, city, mode patches | `tools/build_sequence.py`, `tools/title_plasma.py`, `tools/title_mode.py` |
| Scene director, banks, rows | `tools/build_bitmap_sequence.py` |

## Recommended implementation (scene-first)

### 1. Add an opening act before the title

The current timeline starts with the title/intro. Add a short act in front:

- one star/mark display, or a reused loader star frame;
- a 4-row terminal below it;
- a fixed tick window (about 6–10 s) driven by the existing music-tick
  director.

The scene director already drives acts from player ticks (`music_timing.py`);
use a new tick constant, not a frame counter.

### 2. Display list

- Keep 192 bitmap rows for the star area if it is a bitmap; add 4 mode 2/4
  text rows below, as the outro already does (`TEXT_DL`, `TEXT_ROWS`).
- Alternatively, the star can be a PMG/bitmap header and the terminal rows
  the only playfield content; choose whichever costs fewer rows and less
  bank space.
- The terminal writes must be VBLANK-safe. The loader already has the raster
  sync pattern (`$3B80`, `VCOUNT 124–127`); reuse that idea for the text
  rows.

### 3. Terminal content

Use 4-row pages. Suggested opening (edit freely; 40 columns, uppercase and
the supported glyph set):

```
SYS.OPEN BEGIN.SYS [OK]
THE LESS I KNOW THE BETTER
TAME IMPALA / ATARI XE 1 MB
LOADING TITLE...
```

Then a second page while the star settles:

```
CITY PANORAMA
WATER REFLECTIONS
SILLY VENTURE 2026
```

The terminal engine already pages in 4-row chunks and types at
`PROMPT_DELAY`/`ENTER_DELAY`. Keep each line ≤ 37 characters.

### 4. Star animation

Two options:

- **Reuse the loader star VBI** if its assets can be kept alive into the
  first scene. This is the expensive path: the late low-RAM segments
  overwrite `$0C00–$1EA3` and `$3300–$3BF3`.
- **Re-render the star in the opening act** (a small bitmap or PMG with a
  short frame loop). This is cheaper and keeps the loader untouched. The
  viewer cannot tell the difference if the frames match the loader mark.

Prefer the second.

### 5. Water in the title

- Add a procedural reflection band under the city: mirror the lower city
  rows, offset each row horizontally by a slow sine, darken the palette.
- Do not add precomputed reflection frames unless banks are freed; the
  1 MiB headroom is small and all 64 banks are allocated.
- Keep the water and the terminal from competing: the terminal clears
  before the water appears, or the water sits above a 4-row strip only in
  the opening.

### 6. Transition

- Terminal clears or scrolls off.
- Star/mark fades or is replaced by the title bitmap.
- City + water resolve.
- Avoid a hard cut; use the existing fade/blanking mechanisms.

## Alternative (loader-native) — not recommended first

Keep the live loader VBI running past the last bank and type the terminal
under it. Requires:

- delaying the late low-RAM overwrite until the interlude ends;
- staging the terminal engine before the demo starts;
- a split display list in the loader;
- fighting the ~3.8 KB headroom and all-bank allocation.

It gives the same visible result as the scene-first version at much higher
risk. Only attempt it if the scene-first version cannot match the intended
look.

## Constraints

- 4 rows exactly (`HISTORY_ROWS = 4`); do not shrink or crop the 192-row
  scene art.
- Keep the loader contract: 66 wrappers, 64 clears, sparse fragments,
  `$4800` bootstrap, below 1 MiB.
- All 64 banks are allocated. New content must fit an existing bank or
  replace something.
- The terminal engine's resources are currently staged late; moving them to
  the opening needs a bank/staging plan.
- No lowercase; supported glyphs are `A–Z`, `0–9`,
  `space ! " # ' + , - . / : > \`.
- Lyrics: the demo currently contains no Tame Impala lyrics. A few lines is
  a rights consideration; the existing text talks about the song instead.

## Validation

1. py65: scene handoff, terminal rows, text paging, no bank overlap.
2. Atari800: animation visible during typing, no tearing of the 4 text rows,
   title/water transition.
3. Size < 1 MiB; `make check` green.
4. Real AVG / 1088 Rambo: the only acceptance for "works". Record the file,
   SHA, size and result.

## Open questions for the author

1. Should the star be the live loader VBI or a re-rendered copy in the
   opening scene?
2. How long should the opening interlude last relative to the first bar?
3. Does the water replace the bottom of the city, or sit under it as a
   separate band?
4. Should the terminal appear again between acts (one line at scene cuts) or
   only at the opening and ending?
5. Opening text: use the suggested lines, or a dedicated intro text?
