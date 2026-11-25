> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# 3. Loading screen

## 3.1. Where it lives

`[READ]` In the current build (release 018) the screen is relocated to
high memory by `tools/build_init_trace_high.py`:

| Address | Size | Contents |
| --- | ---: | --- |
| `$3800–$3877` | 120 B | three rows of 40 characters (ATASCII − 32) |
| `$3880–$388A` | 11 B | ANTIC 2 display list |
| `$38A0–$38DC` | 61 B | INIT setting the screen and colours |
| `$02E2` | 2 B | `$38A0` |

`[READ]` In the source (`tools/loading_screen.py`) the addresses are module
parameters: `SCREEN=0x0600`, `DLIST=0x0700`, `ENTRY=0x0780`. Stage 2 overrides
them to `$3800`/`$3880`/`$38A0` so that they do not collide with runtime
segments and survive bank loading.

## 3.2. Display list

`[READ]` 11 bytes:

```
70 70 70                         3 × 8 pustych linii
42 00 38                         tryb 2 + LMS $3800
02 02                            dwie kolejne linie trybu 2
41 80 38                         JVB do $3880
```

ANTIC mode 2 is 40-column text. Each line occupies 40 screen bytes
(1 character = 1 byte), so three rows are 120 bytes from `$3800`.

## 3.3. Initialisation

`[READ]` The INIT at `$38A0` writes the OS shadows **and** the GTIA/ANTIC registers:

| Register | OS shadow | Role |
| --- | --- | --- |
| `$D400` | `$022F` | DMACTL — `$22` (playfield and DL DMA enabled) |
| `$D402/$D403` | `$0230/$0231` | DLIST |
| `$D409` | `$02F4` | **CHBASE** — `$E0`, i.e. font ROM `$E000` |
| `$D016…$D01A` | `$02C4…$02C8` | COLPF0–3 and COLBK |

### Important correction: CHBASE is `$D409`, not `$D018`

`[READ]` `$D018` is **COLPF2** (text colour in mode 2), and
`$D01A` is COLBK (background). CHBASE — the character set address — is at `$D409`,
and its OS shadow at `$02F4`.

`[READ]` In the first version `tools/loading_screen.py` wrote
`$D018=$00`, i.e. **text colour = black**. Against the black background the text
was invisible despite a correct CHBASE. The change to `$E0` made the letters brighter.

`[CONCLUSION]` The earlier diagnosis “a wrong CHBASE caused blank characters”
was incorrect. The correct description: black text on a black background. The
factual correction is in `docs/V272_AVG_INIT_TRACING.md`.

## 3.4. Current palette

`[READ]` The latest version of `tools/loading_screen.py` (after the changes of
2026-11-12 03:00) sets a dark blue background and warm letters:

| Register | Value |
| --- | --- |
| COLPF0 | `$38` |
| COLPF1 | `$2C` |
| COLPF2 | `$88` |
| COLPF3 | `$9C` |
| COLBK | `$82` |

`[LIMITATION]` Release 018 was built **before** this change — in it
COLPF1=`$0E`, COLPF2=`$E0`, default background. The new palette will only enter the
next build after the pipeline is run again.

## 3.5. Text

`[READ]` Release 018 contains three rows:

```
THE LESS I KNOW THE BETTER
SILLY VENTURE 2026 WE
AI-SLOP/OGNJEN
```

`[READ]` The latest `loading_screen.py` already has the new text:

```
THE LESS I KNOW THE BETTER
LOADING BANKS / ATARI XE STEREO
PRODUCED BY OGNJEN / SILLY VENTURE 2026
```

## 3.6. INIT progress row

`[READ]` The `$3900` wrapper (stage 2) overwrites the **second** screen row
(`$3828–$384F`) with the text:

```
INIT nn ENTER  $xxxx
INIT nn RETURN $xxxx
```

This shows which INIT is currently running, and after return — that it has
returned. This is a diagnostic tool; in a production build it can be removed by
skipping stage 2.

## 3.7. Risks

- `[READ]` The screen `$3800–$3877` lies **above** the `$3300`/`$3400` images
  and does not collide with them.
- `[ASSUMPTION]` If in future some runtime segment starts using
  `$3800–$38FF`, the screen and wrapper must be relocated; currently this is free
  space in this build.
- `[READ]` The wrapper writes only row 1; it does not touch rows 0 and 2,
  so the title and credits stay visible.
