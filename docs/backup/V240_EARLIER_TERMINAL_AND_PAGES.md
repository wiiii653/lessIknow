> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V240 — earlier terminal, fast typing and time to read

At the user's explicit instruction, the terminal and the lying boy start
at **51850 instead of 53850** — 2000 ticks, about 10 s earlier. The end of the
text at 59085, the fade from 59705 and the permanent black from 59833 remain preserved.
The lower frame, the PMG orbit and the seven-line terminal layout do not change.

## Typing and prompt

- The prefix of each entry is `>`. Before the text starts, `>_` is visible.
- The underscore is a thin cursor on the bottom line of the character, instead of a block.
- The cursor **always blinks** while the terminal is running: both while
  typing and during the pause after a finished screen. Bit 6 of the timer
  gives about 0.32 s per state and about 0.64 s for a full cycle.
- Typing: 1 character per tick; the prompt and Enter have 4 ticks each. The long
  pauses before/after each single line are gone.
- The whole screen appears in 55–180 ticks (about 0.28–0.90 s), after which
  it stays motionless for 667–900 ticks (about 3.34–4.51 s).

## Screens

Each greetz paragraph is a separate screen; no entry was removed.
There is no longer continuous history scrolling while reading.

| Start | Content | Typing / pause in ticks |
|---:|---|---:|
| 51850 | Author, Codex, LLM | 166 / 834 |
| 52850 | Music | 147 / 853 |
| 53850 | Silly Venture / AI | 100 / 900 |
| 54850 | Family | 133 / 714 |
| 55697 | Anecdote about mum | 131 / 716 |
| 56544 | Friends, D3cker, Blasph | 180 / 667 |
| 57391 | Groups and portals | 55 / 792 |
| 58238 | Silly Venture crew and guests | 136 / 711 |

## Memory and synchronisation

55 time entries (110 B) and 54 lengths are loaded together with the font, into
unused control glyphs: $C828–$C895 and $C8A8–$C8DD. Printable
characters start only from $C900. There are no static inserts
into the previously used second bitmap buffer.

The disabled UI $23CE–$2450 is now fully available for staging; 49 B were used.
Total staging is 1914 B, resources after compression 1832 B. The loader is still
373 B and ends at $3FCC, before the resources at $3FCE. $23CD remains RTS,
the router $2451 and the live player variables from $249C are not touched.

The typewriter has 172 B at $EB44–$EBEF, 23 B less. The rotator/tunnel director
stops at 51850: after cutting the unused later points it has
60 cues and 301 B at $EC20–$ED4C. The reserves of both helpers remain, so the shared row pool
was not moved. Main code is still 2521 B.

No additional banks or their gaps were used. **All 64 payload banks are byte-identical to v239**.
The four musical DLIs keep positions 1/79/157/235; the additional palette split remains at 57.

## Verification

[READ] 59 targeted tests passed: completeness of the eight screens,
fast typing and the motionless pause, cursor blinking also during
typing, the exact prompt/underscore, the new scene boundary and preserved
buffers, PMG orbit, DLI and PORTB.

[READ] Atari800 PAL/1088XE, stereo POKEY: **11 175 336 identical
bytes** relative to v035, the whole track. No test on physical Atari.

CPU/ANTIC/PMG previews: `build/terminal-v240.png`,
`build/terminal-v240.gif` (fast typing of the first screen and the pause with the cursor).

[READ] Full regression: **183/183 tests**, no skips, 133.5 s.
The working build and v240 are identical. SHA-256:
`b72619f7da4a364b5f13099411b31530d10fd4ceda32ebe75cfce6fe6fa5dcb7`.
