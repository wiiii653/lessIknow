> **Historical text draft.** Use this for draft page copy. Its timing,
> display layout and implementation suggestions are superseded by the
> [main-act implementation plan](TERMINAL_MAIN_ACTS_IMPLEMENTATION.md).

# Terminal text plan — main acts

**Decision:** the title panorama is **without** the terminal. The 4-row strip
starts with the school act (tick ~2,992) and runs through the main demo, then
merges into the existing terminal credits. The final card is clean.

This document is a text/planning draft; no code is changed here.

## Display model

- 192-row scene bitmap, unchanged.
- 4 text rows below it (`HISTORY_ROWS = 4`, `TEXT_ROWS = 4`), 40 columns.
- Same font and typing engine as the ending terminal.
- Uppercase `A–Z`, `0–9`, `space ! " # ' + , - . / : > \`; no underscore.
- Keep every line at 37 characters or fewer.
- The strip is typed once at the act start, holds while the act plays, and is
  replaced at the next act.

## Pages by act

| Ticks | Time | Act | Page |
|---:|---:|---|---|
| 0–2,991 | 0:00–0:15 | opening / title | **no terminal** |
| 2,992–5,984 | 0:15–0:30 | school arrival | 01 |
| 5,984–8,975 | 0:30–0:45 | basketball practice | 02 |
| 8,975–11,967 | 0:45–1:00 | first side-dancer | 03 |
| 11,967–14,958 | 1:00–1:15 | banana roto-zoom / tunnel | 04 |
| 14,959–20,941 | 1:15–1:45 | ribbon dance | 05 |
| 20,942–21,689 | 1:45–1:49 | tunnel cutaway | 06 |
| 21,690–23,933 | 1:49–2:00 | basketball hero / dunk | 07 |
| 23,934–29,655 | 2:00–2:29 | Trevor fight | 08 |
| 29,656–38,704 | 2:29–3:13 | bananas / tunnels | 09 |
| 38,705–41,883 | 3:13–3:30 | eyes / late bananas | 10 |
| 41,884–51,231 | 3:30–4:17 | terminal credits | existing pages |
| 51,232+ | 4:17+ | final shot / card | **no terminal** |

## Page text

### 01 — school arrival

```
SYS.OPEN SCENE 01 [OK]
SCHOOL / ARRIVAL
SHE PASSES. HE WHISTLES.
THE LESS I KNOW THE BETTER
```

### 02 — basketball practice

```
SYS.OPEN SCENE 02 [OK]
PRACTICE / GYM
HE SHOOTS. HE MISSES.
THE BALL NEVER LIES.
```

### 03 — first side-dancer

```
SYS.OPEN SCENE 03 [OK]
RIBBON DANCE / TRIO
THREE GIRLS. ONE BEAT.
HOLD THE POSE.
```

### 04 — banana roto-zoom

```
SYS.OPEN SCENE 04 [OK]
BANANA ROTO-ZOOM
SPIRAL. ORGANIC. REPEAT.
THE FRUIT IS A PORTAL.
```

### 05 — ribbon dance

```
SYS.OPEN SCENE 05 [OK]
RIBBON DANCE / SOLO
HALF-BEAT POSES
SMOOTH INBETWEENS
```

### 06 — tunnel cutaway

```
SYS.OPEN SCENE 06 [OK]
TUNNEL / CUTAWAY
THE DIRECTOR CUTS.
NEXT: THE DUNK.
```

### 07 — hero / dunk

```
SYS.OPEN SCENE 07 [OK]
HERO / DUNK
FOUR SATELLITES
GLASS ON FIRST CRACK
```

### 08 — Trevor

```
SYS.OPEN SCENE 08 [OK]
TREVOR / 13 HITS
HE TAKES THE BALLS.
HE KEEPS COMING.
```

### 09 — bananas / tunnels

```
SYS.OPEN SCENE 09 [OK]
BANANAS / TUNNELS
32 PASSAGES
A CUT EACH BAR
```

### 10 — eyes / late bananas

```
SYS.OPEN SCENE 10 [OK]
GIRL'S EYES
BANANAS BEFORE / AFTER
BUM / BAM
```

### Credits and final card

Keep the existing `CREDITS` and `GREETZ` pages. The final card gets no
terminal; optionally one closing line if a row can be spared:

```
SYS.CLOSE [OK]
```

## Lyrics option

The pages above are commentary. A lyric variant could replace the third or
fourth line in 01, 03, 05 and 10 with the refrain:

```
THE LESS I KNOW THE BETTER
```

Do not print long verbatim lyric passages. A short refrain is a rights
consideration; the current text deliberately talks about the song instead.

## Timing

- Typing speed is the existing `PROMPT_DELAY` / `ENTER_DELAY` in
  `tools/terminal_typing.py`; a 30-character line takes roughly 38 ticks.
- A 4-line page types in under a second, then holds for the act.
- Page starts must be driven by the music clock (`tools/music_timing.py`),
  not by a frame counter.
- The page should be complete before the act's first visual beat; start the
  typing one or two bars early if needed.

## Implementation notes

1. The strip needs the same display-list addition the ending already uses:
   192 bitmap rows, a gap, then `TEXT_ROWS` mode 2/4 rows. This must be added
   to the act display lists, not only the outro.
2. The text page and the terminal state (`CACHED_LINES`, `ROW_STATE`,
   `COUNT`) must survive bank switches between acts. Decide on fixed
   addresses outside the banked window, or re-stage them with each act.
3. Terminal row writes must be VBLANK-safe. Reuse the loader's raster-sync
   pattern instead of writing at an arbitrary beam position.
4. The terminal engine is currently staged late (`tools/outro_loader.py`).
   Moving its text schedule and cache into the main acts needs a bank/staging
   plan; the 1 MiB file has little headroom and all 64 banks are allocated.
5. Keep the 4-row strip out of the title and the final card so the panorama
   and the final image stay clean.

## Open questions

1. Persistent strip for every act, or only at selected acts (01, 05, 08, 09)?
   Persistent is more work in every display list and more visual noise.
2. Does the strip sit on a solid black band, or over the bottom of the scene
   bitmap?
3. Should the text stay visible for the whole act, or clear a few bars after
   typing?
4. Commentary only, or a short lyric refrain too?
5. Is `SYS.CLOSE [OK]` wanted on the final card, or should it stay clean?
