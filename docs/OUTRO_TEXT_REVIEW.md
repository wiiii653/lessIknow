# Terminal text and ending cards — review copy

**Source of truth:** `tools/outro_text.py`.

Nothing is stored as a separate `.txt` asset. The strings are Python
constants in that file and are compiled into the demo. This document is a
read-only review copy; edit the Python file, not this document.

## Character limits

- The screen is 40 columns; the longest current line is 37 characters
  (`GREETZ`). Keep new lines at 40 or fewer.
- The font is uppercase only: `A–Z`, `0–9`, and
  `space ! " # ' + , - . / : > \`.
- Lowercase will not render. `\` is the SLOP logo glyph.
- The terminal lines are shown as a scrolling history; blank strings are
  spacing lines and are preserved.

## Terminal — `CREDITS` (3 screens)

`tools/outro_text.py:57`

```
SYS.OPEN CREDITS [OK]
THE LESS I KNOW THE BETTER
A\SLOP BY OGNJEN / ATARI XE 1 MB
I STARTED VIBECODING IN JULY 2026
THIS IS MY FIRST WORK FOR ATARI
MADE WITH OPENAI CODEX

SYS.OPEN AUDIO.LOG [OK]
SONG / TAME IMPALA
THE LESS I KNOW THE BETTER
POKEY / OGNJEN / CODEX
MIDI / MIDISHOW 200337

UPLINK SV2026 [CONNECTED]
MADE FOR
SILLY VENTURE 2026
AI TOOLS / ATARI SOUL
HUMAN VISION / LLM CODE
```

## Terminal — `GREETZ` (26 lines)

`tools/outro_text.py:66`

```
GREETINGS TO ALL MY CHOOMS!
ESPECIALLY MY SON VICVIP AND HIS
MUM, MY MUM AND DAD,
AND THE REST OF MY FAMILY.

I TOLD MUM: "IT'S AN ATARI DEMO."
SHE SAID: "I CAN HEAR THAT!"
SHE'D HEARD AN ATARI XE 30 YEARS AGO.

TO MY FRIENDS AND NEIGHBOURS -
SPECIAL THANKS TO D3CKER,
WHO INTRODUCED ME TO AI AGENTS,
AND BLASPH, WHO GAVE ME THE IDEA:
TAME IMPALA ON THE ATARI!

SPECIAL GREETS TO KEVIN PARKER,
THE CAUSE OF THIS DEMO.

VIRUS / FOORMAN / MAQ / KEY-G
FALCON / ATARIONLINE.PL / PTODT
ATARIMUZEUM.PL

ALL THE GUESTS AT SILLY VENTURE,
THE WHOLE SILLY VENTURE CREW,
AND EVERYONE WATCHING -
EACH OF YOU, PERSONALLY!
```

## Ending cards — `FINAL_CARD_PAGES` (5 pages)

`tools/outro_text.py:47`

```
PAGE 1
A\SLOP BY OGNJEN 2026
SILLY VENTURE WE

PAGE 2
STEREO MUSIC PLAYER / 2 POKEYS
CREATED AS A SEPARATE PROJECT
4 POKEY UPDATES PER PAL FRAME

PAGE 3
OPENING EFFECTS
PROCEDURAL PLASMA / CITY REVEAL
TITLE REVEAL / PMG FIREWORKS

PAGE 4
LOADER / TEXT EFFECTS
ANIMATED STAR / LOADING DOTS
RAINBOW DLI GLITCH / TEXT FADES

PAGE 5
SCENE DIRECTOR
MUSIC TICKS CUE EACH SCENE
ANTIC MODES / BANKED 1 MB RAM
```

## How to correct

1. Edit `CREDITS`, `GREETZ` or `FINAL_CARD_PAGES` in `tools/outro_text.py`.
2. Keep each string in the supported glyph set and within 40 columns.
3. Rebuild:

   ```sh
   make all PYTHON=/path/to/venv/bin/python
   make check PYTHON=/path/to/venv/bin/python
   ```

4. `outro_text.py` has build-time assertions for unsupported characters and
   for line-address space; a bad glyph fails the build rather than the
   display.
5. The terminal timing is separate (`tools/terminal_typing.py`, `TIMES`,
   `LENGTHS`, `schedule`). Changing a line length may need a timing review.
6. Do not edit generated dumps or the binary; they are rebuilt from these
   constants.
