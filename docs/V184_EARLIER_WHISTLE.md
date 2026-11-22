# V184 — whistle one beat earlier

At the user's request, the whistle entry together with the girl's last pose at
the door was moved 94 ticks (about 0,47 s) earlier: from tick 5610 to 5516.
The pout and the PMG emission start together. The shared constant
`school_story.WHISTLE_START` drives both scene 12 and the PMG clock.

The final shot lasts until the previous tick 5984. The remaining meeting
phases, the girl's path, the note motion and the following shots are preserved.
No increase in code or banks: 316 rows, 12 158 B of row data, 2552 B of main
code.

- XEX: `build/visual-prototype-v184.xex`; dev identical.
- SHA-256: `0237b12cca45dd65878fc3cbc2b2ddefc438e3e40fb36b6914df6483eea5920c`.
- 13 CPU/graphics tests passed; it was also checked that there are no PMG
  ticks before the new start and that emission at the lips begins at the new
  start.
- No new emulator or hardware playback was performed.
