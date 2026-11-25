> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V235 — LLM and AI in credits

At the author's request, two short lines about how the demo was made were added:

```text
HUMAN VISION / LLM CODE
AI TOOLS / ATARI SOUL
```

The first is the sixth entry of the author screen, after `MADE WITH OPENAI CODEX`.
It starts at 54408 and uses the new terminal row. The second is the fourth entry
of the Silly Venture screen, from 56162. Both have the existing typing animation
and cursor. The ticks of the earlier entries, the start of the greetz at 56842,
the end of the text at 59085 and all the graphics remain preserved.

## Memory

38 raw text records fit in the existing two areas of 44 B per record; the second
ends at $CEEC. The number of logical slots (47), time entries (48) and the
terminal width/height do not grow.

After compression the assets occupy 1795 B, 52 B more than v234. The audited 35 B
of disabled UI $242E–$2450 were added; 12 B were used. The area lies exactly
after the 96-byte time table and before the palette router $2451. An assert
guards the time boundary $242E. The total staging capacity is now 1818 B.

Two already used, adjacent ranges $2C81–$2D00 and $2D00–$2E00 were merged into
one copy region. The saved chunk-loop instruction allows the loader to be kept at
373 B in $3E58–$3FCC; it does not enter the asset tail at $3FCE.
Main code still 2551 B, no extension bank gaps occupied.

## Verification

The terminal test checks both full lines in a running 6502. The staging test
checks that assets do not overlap the time table or the palette router.
CPU/ANTIC/PMG preview: `build/ai-credits-v235.png`.

[READ] Full regression: **174/174 tests**, no skips, 118.6 s.
Atari800 PAL/1088XE, stereo POKEY: **10 847 448 identical bytes**
against v035, the entire track. No test on physical Atari.
The numbered XEX and the working build are identical; SHA-256:
`53ba615148430ee79a68639cec5ca2e1554e4bf342e1694c6915729b14fa46ee`.
