# Credits and greetz — current text v261

**Status:** credits and greetz implemented. V261 has seven terminal rows
(status + six lines of text), fast typing of whole cards and pauses for reading.
Prompt `>_`, the cursor also blinks while typing. KEY-G and FALCON added;
the FOORMAN spelling and the number of pages remain unchanged.
V235 adds two lines about creating with LLM/AI (`V235_LLM_AI_W_CREDITS.md`).
The opening message remains a proposal and is not displayed.

## 1. Opening message

Proposed disclaimer before the intro:

```text
THIS DEMO IS NOT INTENDED TO PROMOTE VIOLENCE.
IT IS SOLELY A DEMONSTRATION OF THE
POWER AND CAPABILITIES OF THE ATARI XE.

ANY RESEMBLANCE BETWEEN CHARACTERS
IN THIS DEMO AND OTHER DEPICTIONS
IS PURELY COINCIDENTAL AND
WAS NEVER INTENDED.
```

The preferred place is a short card before tick 0, so as not to shift the
musical boundaries of the intro; however, it would extend the total presentation
time. An alternative is a legible overlay on the opening plasma, without shifting
ticks. The choice of method and display length remains to be approved after a
preview.

## 2. Reserved windows

| Sequence | Ticks | Time | Background / constraints |
|---|---:|---:|---|
| 8A — credits | 49850–52850 | about 15 s | Static frame of the boy, three quickly typed cards with a pause. |
| 8B — greetz | 52850–59085 | about 31.2 s | The same background; five cards, each paragraph separately, no scrolling while reading. |
| 8C — finale | 59085–59833 | 3.75 s | Separate final frame and fade. No credits/greetz text may enter this range. |

The boundaries agree with `TLIKTB_Atari_Timeline_v2.md`. In v197 the 8C finale
alternately shows orbiting stars and notes/treble clef; the greetz text
disappears at tick 59085 and does not interfere with this effect. V240 moved the
terminal to 51850, and v248 moved it further to 49850 together with the montage.
The current starts of the eight pages are 49850, 50850, 51850, 52850, 54097, 55344,
56591 and 57838.

## 3. On-screen text in v261

The on-screen text is in English. The lines below correspond to the current
pages in `tools/outro_text.py`; the terminal status headers are not part of the
credits/greetz content.

### 8A — Credits

Three pages, about 5 seconds per page; after fast typing each remains
visible until the next boundary.

**Card 1 — author / group**

```text
THE LESS I KNOW THE BETTER
AN ATARI XE 1 MB DEMO
BY OGNJEN
MADE WITH OPENAI CODEX
HUMAN VISION / LLM CODE
```

**Card 2 — music**

```text
SONG / TAME IMPALA
THE LESS I KNOW THE BETTER
POKEY / OGNJEN / CODEX
MIDI / MIDISHOW 200337
```

**Card 3 — event**

```text
MADE FOR
SILLY VENTURE 2026
AI TOOLS / ATARI SOUL
```

### 8B — Greetz

Five cards show these paragraphs separately; the lines are typed quickly and then
remain still until the next page.

```text
GREETINGS TO ALL MY CHOOMS!
ESPECIALLY MY SON VICVIP AND HIS
MUM, MY MUM AND DAD,
AND THE REST OF MY FAMILY.
```

```text
I TOLD MUM: "IT'S AN ATARI DEMO."
SHE SAID: "I CAN HEAR THAT!"
SHE'D HEARD AN ATARI XE
ABOUT 30 YEARS AGO.
```

```text
TO MY FRIENDS AND NEIGHBOURS -
SPECIAL THANKS TO D3CKER,
WHO INTRODUCED ME TO AI AGENTS,
AND BLASPH, WHO GAVE ME THE IDEA:
TAME IMPALA ON THE ATARI!
```

```text
VIRUS / FOORMAN / MAQ / KEY-G
FALCON / ATARIONLINE.PL / PTODT
```

```text
ALL THE GUESTS AT SILLY VENTURE,
THE WHOLE SILLY VENTURE CREW,
AND EVERYONE WATCHING -
EACH OF YOU, PERSONALLY!
```

## 4. Guidance for the image realisation

- Keep the current ticks 49850, 52850 and 59085; do not shorten the 8C finale.
- First prepare a preview of the text overlay on the existing background of the
  lying boy. The character occupies a large part of the frame, and PMG objects move
  around the head, so do not place text on the face or on the orbit of the stars/notes.
- For credits, check three high-contrast cards. For the longer greetz,
  each paragraph is a separate card; after fast typing leave a pause
  for reading, with no letter or story movement during that time.
- Maintain legibility over bright parts of the costume: consider a small,
  dark strip/backing or letter outline. Do not assume that text will be legible
  directly over the whole image.
- Before the next edit, confirm the spelling of handles and group names; the current pages
  contain no additional `[NAME]` slots.
- All 64 banks are allocated. Before adding a font, data or code,
  check the current memory map in `AGENTS.md` and do not assume that historical
  gaps are still free. Preserve bank ownership, PMG double buffers and the existing
  finale controller.

## 5. Music source and scope of confirmed information

- The project uses original music from the v035 player; the documentation describes the piece
  as **Tame Impala — “The Less I Know The Better”**.
- OGNJEN states that the MIDI from Midishow was the main source of the score for further
  adaptation to POKEY, performed by him with the help of the Codex agent.
- The source link given: <https://www.midishow.com/en/midi/the-less-i-know-the-better-midi-download-200337>.
  An attempt to read the page while preparing the draft returned HTTP 403;
  the uploader and the MIDI licence could not be verified. We therefore do not attribute
  MIDI authorship or licence status without additional confirmation.
- The screen shows the abbreviated description `MIDI / MIDISHOW 200337`; the full link remains
  in the documentation, because the source and licence have not been independently verified.

## 6. Validation before inclusion in the release

1. Before submission, view v261 on Atari800/Altirra and, if available,
   on the target Atari; automated tests do not replace an A/V assessment.
2. Check that the five greetz pages fit in the 8B window, and that at tick 59085
   only the planned 8C finale remains.
3. After text changes, run the scene boundary and terminal tests. V261 passes the
   full `make check` (199/199); after v261 no emulator playback
   or hardware test was performed.
4. Do not treat CPU tests as confirmation of legibility, raster smoothness or
   operation on physical hardware.
