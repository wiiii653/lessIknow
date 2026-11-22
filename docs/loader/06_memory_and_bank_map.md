# 6. Memory map and bank allocation

## 6.1. Addresses used by the loader

| Range | Size | Owner / role |
| --- | ---: | --- |
| `$0400–$07E4` | 997 B | runtime: tables, buffers; restored from buffer |
| `$0800–$08BF` | 192 B | runtime: `bank_value`/bank tables (`$08C3+`) |
| `$0900–$0974` | 117 B | runtime: PMG/helper data |
| `$0980–$09FF` | 128 B | PMG buffer no. 1 (missiles) |
| `$0A00–$0BFF` | 512 B | PMG buffer no. 2 (players) |
| `$1000` | ~373 B | OS-RAM loader (INIT) |
| `$13E0–$13F0` | 17 B | start stub (`run_stub`) |
| `$1400–$1DFF` | 2560 B | main scene code |
| `$1E00–$1FFF` | 512 B | shared row pool |
| `$2000–$24B2` | 1203 B | original player code |
| `$24B3–$24B5` | 3 B | bank selectors 0–2 |
| `$24BD–$28BC` | 1024 B | player tables (incl. `$26FC`, `$270A`, `$2734`) |
| `$3300–$3323` | 36 B | player display list |
| `$3400–$37BF` | 960 B | player screen |
| `$3800–$3877` | 120 B | loading screen |
| `$3880–$388A` | 11 B | loading display list |
| `$38A0–$38DC` | 61 B | loading screen INIT |
| `$3900–$398B` | 140 B | INIT wrapper (diagnostics) |
| `$3A00–$3A24` | 37 B | clearing `$8000–$BFFF` |
| `$4000–$47FF` | 2048 B | low-memory buffer |
| `$4800–$4873` | 116 B | bootstrap and `JMP $13E0` |
| `$8000–$BFFF` | 16 KiB | bank window (bank data) |
| `$C000–$CFFF`, `$D800–$FFFF` | 14 KiB | copy of OS ROM in RAM |

`[READ]` Addresses `$3800–$3AFF` are occupied **only in AVG builds**
(stage 2). In the base build the loading screen lies at `$0600/$0700/$0780`.

## 6.2. Allocation of the 50 video banks

`[READ]` Order from `tools/build_bitmap_sequence.py` (lines 866–886):

| Index | Content |
| ---: | --- |
| 0 | girl frame (school bank 0) |
| 1 | basketball player (`basketball_hero`) |
| 2 | Trevor bank + `post_trevor_director` + `ribbon_inbetweens` |
| 3–18 | mosaics/rotators (16 banks, `mosaic.banks()`) |
| 19–23 | school panorama (5 banks); bank 19 additionally `trevor_ball_flight` |
| 24–39 | ribbon side actors (16 phases); bank 39 final bitmap |
| 40–48 | title screens/plasma (9 banks); 40–41 fireworks; 46 and 48 are banana resource banks |
| 49 | ribbon controller + final boy controller |

`[READ]` Together 50 additional banks (0–49) + 14 v035 music banks
= **64 banks**, i.e. a full 1 MB.

`[READ]` Selected constants:

```
ribbon_dance.FIRST_BANK      = 8
ribbon_dance.SIDE_BANK       = 24
ribbon_dance.FRAME_COUNT     = 36
final_boy.BITMAP_BANK        = 39
title_plasma.FIRST_BANK      = 40
banana_cache.RESOURCE_BANK   = 46
banana_cache.SPARE           = 48
trevor_ball_flight.BANK_INDEX= 19
```

## 6.3. Where the bank selectors are stored

| Index | Selector address |
| ---: | --- |
| 0 | `$24B3` |
| 1 | `$24B4` |
| 2 | `$24B5` |
| 3–49 | `$08C3–$08F1` |

`[READ]` Read in code: `tools/school_portrait_bank.py`, function
`bank_value(index)`:

```python
BANK_VALUE = 0x24b3
def bank_value(index):
    return BANK_VALUE + index if index < 3 else 0x08c0 + index
```

## 6.4. v035 music banks

`[READ]` The original player detects and loads 14 banks; their selectors
end up in `$26FC–$2709`. The decoder reads 8 of them (7 full + 2820 B
of the eighth), and banks 9–14 are not read by the music and the demo uses
them for graphics.

`[READ]` Selector table on this configuration:

```
$26FC: 81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB
```

## 6.5. Player pointer tables

| Address | Role |
| --- | --- |
| `$270A–$2717` | 14 default-variant selectors |
| `$2718–$2725` | "non-81" variant |
| `$2734–$2741` | low bytes of configuration pointers |
| `$2737–$2744` | high bytes of configuration pointers |

`[READ]` Code `$201D–$2023` copies 14 bytes from the pointer into
`$26FC–$2709`, so the contents of `$2734/$2737` select the correct list
for a given machine.

## 6.6. Map limitations

- `[LIMITATION]` Addresses `$3800–$3AFF` are free **in this build**;
  there is no guarantee they will remain free after adding new scenes.
- `[LIMITATION]` The `$4000–$47FF` buffer lies in the bank window and occupies
  2 KiB of one of the 1 MB banks — check which one if you add data.
- `[READ]` The `$0C00–$0F3F` area is reserved for runtime
  (composer, frame selectors); do not place assets there.
