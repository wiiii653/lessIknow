# V191 — centred BUM and bubbles at the fists

BUM kept the alignment of the old four-letter BNG!, which is why the three
letters were shifted to the left. Both words, BUM and BAM, now have a
24-pixel field centred in a 32-pixel bubble: offset +4.

Each of the 40 punches receives a pseudorandom point, calculated by an xorshift
generator and stored in a table. The spread is limited to ±6 logical pixels
horizontally and ±3 PMG double rows (±6 image lines) vertically
around the anchor of the proper fist. Over the course there are 16 different
points for one hand and 18 for the other. The position is constant during a
single punch; the text, the bubble and the splash use the same origin.
The sequence is repeatable between playbacks and does not consume CPU time
for randomisation during the raster. The balls bounced by Trevor keep their paths.

- XEX: `build/visual-prototype-v191.xex`; dev identical.
- SHA-256: `218d1ab3524b13cb78d5e7486306f8bb6dbacb5295790e263a9f699d885d11ad`.
- Trevor helper: 2500 B, 60 B headroom to $6A00; main 2560 B without headroom.
- 24 tests passed: centring of both words, all 40 anchors and constancy
  through a punch, the spread in the proper area, the texts, the PMG buffers and Trevor's
  scenes. Log: `build/v191-focused-check.log`.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 037 712 identical
  bytes with v035, the whole track. `build/v191-playback-check.log`.
- Preview after the 6502 callbacks: `build/v191-impact-preview.png`.
  It is not an emulator capture and does not model ANTIC DMA.
- The full test set was not rerun; earlier unrelated
  discrepancies are described under v189. Without a new assessment on physical Atari.
