# Task: fix loading-screen flicker + cut load time (Atari 1088 Rambo demo)

Target: `less-i-know-demo-prerelease-170-stereo.xex` (Tame Impala "The Less I Know the Better", 2xPOKEY).
Goals, in priority order:

1. Remove flicker/stutter of the animated loading screen while loading.
2. Reduce total load time (currently extremely long).

**READ FIRST: `HARDWARE_LOADER_CONTRACT.md`. Its rules override everything in this file.**
Findings here come from **static analysis of the built XEX** (segment parse + 6502 disassembly), not from running it.
Items marked **VERIFY** are hypotheses to confirm in the source before changing code.

---

## 0. Hard constraints (from the hardware contract)

- The last full run confirmed on real hardware is **release 058** (936,240 B, AVG + Atari 1088 Rambo). Releases 059/060 did **not start** on hardware; the cause is **unresolved**. A prototype with a different loading path (v353) also failed later. So **any change to the loading path is a risk until proven on hardware.**
- **Do not change**: bank detection (original v035) and the 50 extra video-bank selectors; the map/order of banks; the 66 INITs routed through the `$3900` wrapper in release 058 order (wrapper preserves registers and flags around loading-screen refreshes); the clear of `$8000-$BFFF` via INIT `$3A00` before each of the 64 bank images; reconstructed images byte-identical to the raw prototype (incl. RAM-under-ROM image).
- Final runtime data for `$0400-$0BFF` stays **deferred to `$4000-$47FF`** and is restored by the `$4800` bootstrap (IRQ/NMI off, restore ranges `$0400-$07DF`, `$0800-$08BF`, `$0900-$0976`, `$0980-$09FF`, `$0A00-$0BFF`, then `JMP $13E0`). **PORTB must not change** between loading `$4000` buffer and the bootstrap.
- Packaged file must stay **below 1 MiB** (compatibility condition).
- Do not move progress dots into low RAM. Never overwrite numbered releases (use a new filename; the packager enforces this). Build via `tools/build_hardware_xex.py` as in the contract.
- **py65 and Atari800 results do not replace a full AVG / 1088 Rambo test.** Never claim "fixed" without it.
- **One change per candidate.** Because 059/060 failed for an unknown reason, ship each change as its own numbered candidate so a hardware result can be attributed to it.

## 1. Structure of the analysed file (measured)

- 1,044,733 B, 1538 segments; SHA-256 starts `f0f0f7c9ac6cbea6` (not the 058 reference). **Larger than 058 by ~108 KB (936,240 B)** — more data means proportionally longer load; **VERIFY** what grew.
- Only **3,843 B below 1 MiB** (1,048,576 - 1,044,733): the size limit leaves almost no room for adding loader code or data.
- Matches the contract layout: 66 x `INIT $3900`, 64 x `INIT $3A00`, one `INIT $38A0`, one `INIT $4800`, `RUNAD $13E0`, deferred `$4000-$47FF` segment, bootstrap `$4800-$4873`, **no direct loads into `$0400-$0BFF`**.
- 65 groups split at each `INIT $3A00`: 64 bank groups + final resident group (86 segments, ~62 KB). Each bank group: `INIT $3900` -> `INIT $3A00` -> data into `$8000-$BFFF` (sparse segments skip zero runs). No duplicate banks.
- Compressibility per bank (zlib -9 / lzma): **total 373 KB / 341 KB vs ~1027 KB raw (~36% / ~33%)**. A 6502 packer (ZX0/LZSA2) will do somewhat worse — measure.

## 2. How the loader works today (from disassembly)

| Address | What it does |
|---|---|
| `INIT $38A0` | Sets shadow regs (`$022F`, `$0230/1`, `$02F4`, `$02C4-C8`) **and writes the same values directly to hardware** (`$D400`, `$D402/3`, `$D409`, `$D016-$D01A`). Ends with `JMP $1100`. |
| `$1100` | First call only (flag `$1184`): saves old `VVBLKI`, installs **immediate VBI** `$112E` via `SETVBV`. Later calls `RTS`. |
| VBI `$112E` | Reads RLE/XOR delta stream from `$1400` and XORs it into charset `$0CF0+X`; chains to old VBI. Runtime is **data-dependent**. |
| `INIT $3900` (wrapper) | `JSR $38A0`, copy 40 B `$393C -> $3828`, `JSR $2000`, `JSR $38A0`, copy 40 B `$3964 -> $3828`. So **2 hardware re-inits + 2 text rewrites per INIT**. |
| `$2000` | `SEI`, `NMIEN=0`, bank probe (candidate tables at `$2734`), then restores shadows and `NMIEN=$40`; error path hangs at `$20BB`. |
| `INIT $3A00` | `PHP/SEI`, zero-fills `$8000-$BFFF` (~4.6 PAL frames); NMI stays on, animation keeps running. |
| `$20EA` | `SEI`, `NMIEN=0`, select bank via table `$26FC`, copy `$8000-$BFFF -> $4000-$7FFF` (~6.4 frames), restore, `NMIEN=$40`. **VERIFY: caller not found by static search.** |

---

## Part A — Flicker (allowed, lowest risk first)

### A1. Make the per-INIT display refresh VBLANK-safe (do NOT remove it)
`$38A0` writes `DMACTL`, `DLISTL/H`, `CHBASE`, `COLPF0-COLBK` at an arbitrary beam position, twice per wrapper call. That is the most likely visible flash at bank boundaries.
- **Keep** the 66 wrapper calls, their order, and the register/flag preservation. Change only *when* the hardware writes happen.
- Sync to VBLANK first (works even with `CRITIC` set), then do the burst:
  ```
  lda $14
  cmp $14
  beq *-2        ; wait for next VBLANK stage-1 tick
  ; short burst of hardware + text writes here
  ```
  Alternative: write only shadow regs and let the OS/VBI apply them — but deferred VBI is skipped while `CRITIC` is set, so verify it still gets applied.
- Same for the 40-byte text rewrite at `$3828` (VBLANK, or swap a double-buffered line).
- **VERIFY** with the watchpoint test whether the second `JSR $38A0` per wrapper is needed at all, but removing calls is a *separate* candidate and needs hardware confirmation.

### A2. VBI cost cap (loader code only)
VBI `$112E` has a data-dependent loop. NMI entry sets I, so POKEY serial IRQs are held off while it runs; heavy frames can cost SIO bytes (retries/stalls) and overrun VBLANK (torn charset rows). Cap XOR bytes per frame (~24-32) or pre-split the delta stream at build time. Does not touch bank logic.

### A3. NMI-off window in `$20EA` (only after A1/A2 pass on hardware)
~6.4 frames/bank with `NMIEN=0` freezes the animation. Slicing the copy or keeping NMI on changes timing around PORTB; the contract requires PORTB to stay stable only for the `$4000` buffer -> bootstrap path, but **this touches bank handling**. Treat as a separate, optional, hardware-tested candidate. **Locate the caller of `$20EA` first.**

### Dropped from the earlier version (conflict with the contract)
- ~~Remove the zero-fill in `$3A00`~~ — **required by contract** (clear before each bank; byte-identical reconstruction). At most: a faster byte-identical clear (unrolled `STA abs,X`, saves ~2 frames/bank, ~2 s total) — low value, optional.
- ~~Run the bank probe only once~~ — contract says preserve the original v035 bank detection.
- ~~Load straight into the `$4000` bank window~~ — changes the bank-loading path; the `$8000` staging + clear + copy is part of the reference design. Do not attempt without explicit approval and hardware validation.

---

## Part B — Load time

Rough model (**ESTIMATE; assumes standard 19200 baud SIO, 128 B sectors, ~1.3-1.6 KB/s effective**): 1,044,733 B ≈ 11-13 min. Per-bank loader overhead (clear + copy ≈ 11 frames) ≈ 14 s total, so **transfer volume/speed is the real lever, not the loader code.** **AVG's transport is unknown to me — it may not be plain SIO** (ask the author), which changes what B2 can do.

### B1. Compression — EXPERIMENTAL track, not the first candidate
Biggest potential win (~3x less data), but it is a **new loading path**, and the contract's history (059/060, v353) shows loading-path changes fail on hardware for unresolved reasons. If pursued:
- Keep 66 wrapper INITs, order, `$3A00` clear, bank map, deferred `$4000-$47FF` buffer, bootstrap and PORTB rules unchanged; only replace *how the nonzero fragments of each bank image reach `$8000-$BFFF`* (compressed stream -> small staging -> decompress into `$8000-$BFFF`, then the existing copy runs unchanged).
- Verify in py65 that the reconstructed images are **byte-identical** to the raw prototype (all 64 banks + RAM-under-ROM), and that the handoff to `$4800` is unchanged.
- Decompressor must live outside `$8000-$BFFF`, `$3800-$39FF`, charset/loader areas, and fit in the remaining 3,843 B headroom *or* be paid for by the compression savings (compressed file will be far smaller — compute the net).
- Ship as its own numbered candidate; mandatory full AVG / 1088 Rambo test.

### B2. Faster transfer (no loader-logic change, lowest risk)
- Find out how it is loaded (AVG mode, any SIO speed settings, sector size, image format). If the device supports high-speed SIO or a larger sector size (256 B), use it; consider a standard/known-good loader entry that does so **only if it keeps the XEX contents and INIT order as is**.
- Check the ATR/image writing is sequential (no seeks) if a disk image is involved.

### B3. Less data (content decision, owner's call)
The file grew ~108 KB since 058. Identify what was added; trimming or deduplicating content is a direct load-time win with no loader risk. Frame/tile sharing across banks must keep the "reconstructed images match raw prototype" check meaningful (the prototype itself would change).

---

## Suggested order

1. Baseline on emulator (SIO patch off, accurate sector timing): time-to-RUN, video of loading screen, watchpoint log.
2. **Candidate N+1: A1 only** (VBLANK-synced refresh inside the wrapper). Hardware test.
3. **Candidate N+2: A2** (VBI cap). Hardware test.
4. B2 findings (no code change) in parallel; B3 with the author.
5. Only then A3 and/or B1, each separately, each with a full hardware run.

## Testing / acceptance

- Altirra: disable the SIO patch; enable accurate sector timing. Break on writes to `$D400, $D402, $D403, $D409, $D016-$D01A` and log `VCOUNT`. Pass = no writes outside VBLANK after startup.
- Frame-step across several bank boundaries: no colour flash, no charset garbage, no torn text line, no animation freeze > 1 frame.
- py65: reconstructed bank images byte-identical, wrapper preserves regs/flags, bootstrap handoff unchanged. Packager checks (`tools/build_hardware_xex.py`) pass and 058 SHA-256 verified.
- **Real hardware (AVG + 1088 Rambo) full run is the only acceptance for "works".** Record file name, SHA-256, size, result.
- Size must stay < 1 MiB.

## Open questions for the author

1. What is AVG exactly (transport, speed options, sector size)? PAL/NTSC and 2nd POKEY setup are unconfirmed — do not assume.
2. Source repo / assembler and build script locations.
3. Where is `$20EA` (bank copy) called from?
4. What accounts for the ~108 KB growth vs release 058?
5. Is the music data already compressed?
