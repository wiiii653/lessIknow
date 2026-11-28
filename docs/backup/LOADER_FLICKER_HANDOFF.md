> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# Loading-screen flicker — findings and handoff

**Status:** The user confirmed that the raster-synced candidate loads and
runs with a clean loading animation. Some visual glitches remain after loading
and before the opening plasma. The earlier experiments below are historical.

## Hardware-confirmed loading candidate

- File: `build/hardware-loader-raster-sync.xex` (development candidate).
- Size: 1,044,748 bytes.
- SHA-256: `60dbf31abf9e6c483fdc2503c08ca0ba3b2296d4b7fc334c4e9b22ee6735dcdd`.
- Derived from `build/hardware-dev.xex` by loading a 14-byte helper at
  `$3B80` before the first INIT. The helper waits for ANTIC `VCOUNT`
  124–127 and jumps to the original refresh at `$38A0`.
- The patch redirects 131 wrapper refresh calls and preserves the final VBI
  stop call, INIT order, clears, bank payloads and bootstrap. The XEX segment
  map shows that the helper is live through the last wrapper.
- The earlier `$3C00` experiment called its helper before it was loaded and
  overwrote it with resident data while later wrappers still needed it.
- The raster sync patch lives in this candidate binary. The standard build
  command still produces the original refresh path. Integrating the patch into
  the release builder and investigating the post-load transition are pending.
- The latest report did not restate the Atari model, video standard, memory
  expansion or stereo configuration.

## TL;DR

- The loading-screen blink comes from the two `JSR $38A0` display refreshes
  in every `$3900` bank wrapper. They rewrite `DMACTL`, `DLIST`, `CHBASE`
  and the colours twice per bank at an arbitrary beam position.
- In the isolated clone, removing those refreshes removes the blink
  completely (`--mode direct --clear --no-init`, hardware-confirmed).
- In the real demo, removing them makes the **demo load and run**, but the
  loading screen itself gets destroyed during loading. So the real
  AVG/OS loader does disturb the display (or the loading-screen memory),
  and the refresh is doing real work there.
- A VBLANK-synced refresh candidate (`prerelease-170-vblank.xex`) was
  reported still broken. Cause not yet identified.

## Artifacts and SHAs

Real loader (all in `build/`, none are numbered releases):

| File | Size | SHA-256 | What it is |
|---|---:|---|---|
| `releases/less-i-know-demo-prerelease-170-stereo.xex` | 1,044,733 | `f0f0f7c9…` | approved candidate, control |
| `build/hardware-dev.xex` | 1,044,730 | — | current dev tree (rebuilt 08:52) |
| `build/hardware-norefresh.xex` | 1,044,730 | `5bae9240…` | dev + all wrapper `$38A0` calls NOPed |
| `build/hardware-norefresh-last.xex` | 1,044,730 | `6908ee35…` | dev, all but the last wrapper NOPed |
| `build/prerelease-170-norefresh.xex` | 1,044,733 | `79f54222…` | 170 + 130 calls NOPed |
| `build/prerelease-170-vblank.xex` | 1,044,746 | `e00028d4…` | 170 + VBLANK-synced refresh |

Clone (`projects/loader-clone/build/`):

| File | Size | SHA-256 | Behaviour |
|---|---:|---|---|
| `loader-clone-copy.xex` | 4,808 | `72c32ed8…` | copy path; animates, blinks |
| `loader-clone-direct.xex` | 4,767 | `c7549530…` | no copy; delay keeps animation visible |
| `loader-clone-direct-clear.xex` | 4,770 | `81621445…` | no copy, `$3A00` clear |
| `loader-clone-direct-portb.xex` | 4,780 | `ac773718…` | no copy, copy's PORTB sequence |
| `loader-clone-direct-noinit.xex` | 4,770 | `24336977…` | no copy, clear, **no per-bank `$38A0`**; hardware-confirmed smooth |
| `loader-clone-minimal.xex` | 4,757 | `52367bf1…` | no VBI, static by design |

## Hardware results as reported

1. Clone `copy`: animates, visible blink at bank boundaries.
2. Clone `direct`/`minimal`: static at first. Cause: `$38A0` installs the
   VBI but nothing set `NMIEN=$40`; only the copy routine did. Fixed.
3. Clone `direct-noinit`: **works perfectly — animates, no blink.**
4. Real `norefresh` (wrapper calls removed): demo loads and runs, but the
   animation screen is destroyed during loading.
5. Real `norefresh` built from the dev tree: post-loading "blue rectangle
   with white OK" and strange graphics. Not reproduced from 170.
6. Real `prerelease-170-vblank`: reported still broken.

The clone and the real loader differ. Treat the clone as a proof that the
refresh is the blink source, not as a ready patch.

## Loader architecture facts

- XEX: 1,538 segments, 64 bank groups + resident group, RUNAD `$13E0`.
- Each bank group: `$1000` loader (video banks) or `$3900` wrapper +
  `JSR $20EA` (music banks) → `$02E2` INIT → `$3A00` clear → `$02E2`
  INIT → sparse data at `$8000–$BFFF`.
- The copy/clear order is deferred by one group: the wrapper copies the
  previous group's staging, then the `$3A00` clear wipes it, then the new
  data loads.
- `$38A0` (93 bytes) sets shadows `$022F`, `$0230/1`, `$02F4`,
  `$02C4–$02C8` and hardware `$D400`, `$D402/3`, `$D409`, `$D016–$D01A`,
  then `JMP $1100` to install the VBI.
- `$1100` installs VBI `$112E` with `SETVBV` (A=6). On the XL OS,
  `SETVBV` takes X=high, Y=low; the code uses `$11/$2E`, i.e. `$112E`.
  Verified against `ATARIXL.ROM`.
- VBI `$112E` XORs the charset at `$0CF0+X` from the delta stream at
  `$1400`, chains to the saved old VBI at `$1172/3`, resets on `$FF`.
- The loading VBI is only enabled by the copy routines (`NMIEN=$40` at the
  end). `$38A0` does not enable it.
- `$3A00` clears `$8000–$BFFF` with NMI still enabled.
- The 16 KiB copy runs with `NMIEN=0` (~6.4 PAL frames), then restores
  `NMIEN=$40`.

## The clone project

Path: `projects/loader-clone/`.

```sh
python3 projects/loader-clone/build.py \
    --mode direct --clear --no-init \
    --output projects/loader-clone/build/loader-clone-direct-noinit.xex
```

Other switches:

- `--mode copy` — real 16 KiB copy (staging → `$4000`), blinks.
- `--mode direct` — no copy; `$1000` spends a delay with NMI on.
- `--clear` / `--no-clear` — force/skip the `$3A00` clear.
- `--no-init` — NOP the wrapper's two `$38A0` calls.
- `--no-vbi` — static screen for isolation.
- `--portb` — mirror the copy's PORTB save/select/restore.
- `--banks N` — number of bank cycles (default 64).

The clone imports the parent `tools/` and reads the immutable 058 reference
for the wrapper, clear and INIT bytes. It is not fully standalone.

The clone's `direct-noinit` proves this chain works on hardware:
VBI installed + `NMIEN=$40` + text/dots + clear + no per-bank `$38A0`
= animation without blink.

## What still differs in the real loader

The clone's loader is the Atari800/OS XEX loader. The real demo is loaded
from **AVG on a 1088 Rambo**. The AVG path apparently changes something
during loading that the per-bank refresh restores. Candidates, in order:

1. **Display registers.** The AVG/OS loader changes `DMACTL`, `DLIST`,
   `CHBASE` or the colours between banks. The refresh restores them;
   removing it destroys the screen.
2. **Loading-screen memory.** Something writes into `$3800`/`$3880`/
   `$0C00`/`$1100`/`$1400` during loading. A register refresh cannot
   restore memory, so check RAM snapshots across banks.
3. **VBI ownership.** AVG may install its own VBI or change `NMIEN`.
   Removing the refresh also removes the only regular `$38A0` calls; the
   `stop` call at the end is not enough to keep the screen alive.
4. **The dev tree is not 170.** `build/hardware-dev.xex` is 1,044,730 B;
   170 is 1,044,733 B. Three bytes of content differ. Any hardware test
   must state which file was flashed.

## Why the VBLANK candidate may have failed

`prerelease-170-vblank.xex` replaces all wrapper `JSR $38A0` with
`JSR $3C00`, where:

```
$3C00: A5 14      LDA $14
$3C02: C5 14      CMP $14
$3C04: F0 FC      BEQ $3C02
$3C06: 4C A0 38   JMP $38A0
```

Open questions:

- Does `$14` (RTCLOK low) actually advance during AVG loading? If AVG
  holds the OS VBI off, the loop spins forever. That would look like a
  hang or a destroyed screen, not a blink.
- The sync waits for the **next** tick, then the writes run. If the writes
  are after the VBLANK window (e.g., a slow SIO/AVG VBI), they can still
  land mid-frame.
- `$3C00` is free during loading but overwritten by the resident runtime
  at the end. Confirm the sync segment is loaded before the first bank.
- The wrapper's first refresh happens before the copy; the second after.
  Both are synced. If AVG changes the display between them, the second
  refresh may be too late.

## Suggested next steps for Codex

1. **Establish the control.** Flash unmodified 170 and record the exact
   symptom (blink only, or destruction). Then flash `hardware-dev.xex`
   (unpatched) to see whether the 3-byte dev difference already breaks the
   loading screen.
2. **Watchpoints on hardware or in a cycle-accurate emulator:** log writes
   to `$D400`, `$D402/3`, `$D409`, `$D016–$D01A` together with `$D40B`
   (VCOUNT). Identify who writes what and when. The hypothesis is that
   something other than `$38A0` changes these during loading.
3. **Snapshot RAM across banks.** After each bank, dump `$0C00–$0FFF`,
   `$1100–$1184`, `$1400–$1EA3`, `$3800–$3877`, `$3880–$389B`,
   `$38A0–$38FC`, `$3900–$398B`. Compare with the first bank. If any
   differ, the loader is overwriting the screen.
4. **Test `norefresh-last`** (`6908ee35…`): all but the last wrapper
   refresh removed. If it loads cleanly, the issue is the per-bank timing,
   not the refresh itself.
5. **If `$14` does not advance under AVG**, replace the VBLANK sync with a
   direct `$D40B` (VCOUNT) wait, or use the VBI itself to perform the
   refresh (set a flag in the VBI, do the writes there).
6. **Only then** cut a numbered prerelease. Record the SHA, size and the
   exact hardware result.

## Constraints

- `docs/HARDWARE_LOADER_CONTRACT.md` governs the loader. The wrapper order,
  66 INITs, 64 clears, sparse fragments, `$4800` bootstrap and the 1 MiB
  bound are part of the hardware-confirmed path. Do not change the bank
  map or order based on emulator results.
- The 1 MiB bound: 170 has 3,843 B headroom; the vblank candidate 3,830 B.
  Any added loader code must fit.
- py65 and Atari800 do not model ANTIC DMA or physical raster deadlines.
  Only a full AVG / 1088 Rambo run counts as proof.

## Related documents

- `docs/HARDWARE_LOADER_CONTRACT.md`
- `docs/backup/PRERELEASE-170-AUDIT.md`
- `docs/backup/fix-loader-glitch-and-load-time.md`
- `projects/loader-clone/README.md`
