> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V227 — no split stars and notes above the head

The bug was not intentional. The finale controller was reading `$D407` (PMBASE),
an ANTIC register that is write-only. On hardware it did not obtain the
number of the visible buffer this way, so it could draw again into the active PMG.
Additionally, the text renderer shifted already published masks by 16 bytes
(32 lines), which let DMA see an incomplete version of the object.

The choice of the next buffer now comes from RAM state `$83E8`. The Y coordinates
are generated immediately with a +16 byte offset; the entire secondary
rewriting pass from `outro_text` was removed. All four masks are cleared
and drawn in the invisible buffer before PMBASE publication. After publication
there are no more writes to the PMG bitmaps. On the first entry PMG is disabled
during preparation so that inherited objects are not displayed.

The four orbiting objects and alternating stars/notes remain. The appearance of
the masks, the orbit, the colours, the head position, the terminal and Trevor's palette
were preserved. The finale controller: 814 B, `$5CD0–$5FFD`; no bank was added.

## Evidence

- A test with memory returning `$FF` on a PMBASE read reproduces the v225 bug:
  it detects writes to PMG after its publication. V227 passes the same test.
- The test covers 48 successive phases, stars and notes: each of the four players
  contains exactly one expected mask, with no pixels outside it, and the old
  visible buffer is not written during successive frames.
- 14 tests of publication, the finale, NMI, restarts and regression — OK, 6.1 s.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 144 952 identical bytes
  relative to v035; the whole track. No attempt on physical Atari.
- The regression compares the content of enabled players/missiles only:
  disabled PMG and the inactive buffer are scratch space and do not determine
  the visible image.

The full run of 162 tests showed one old assertion that also compared
disabled missiles after scrolling to scene 3472; the remaining tests passed.
After narrowing that assertion to the actually enabled PMG, the repeated set
of 14 tests, including this regression and the write-only PMBASE test, passed.
