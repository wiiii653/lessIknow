> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# 7. Bank switching during playback

## 7.1. General principle

`[READ]` In the runtime code, every block that reads from or writes to a bank
uses the same pattern:

```
LDA $D301     ; save the current PORTB
PHA
LDA <selector>; from the $24B3+ / $08C3+ table
STA $D301
JSR <code in bank>
PLA
STA $D301     ; restore
RTS
```

`[CONCLUSION]` As a result, interrupts (the music NMI) run in a consistent
mapping: the handler cannot land on a bank swapped out by the foreground.

## 7.2. Main switching points

`[READ]` `tools/build_bitmap_sequence.py`:

| Label / line | What it does |
| --- | --- |
| `banked_effects` (~729) | selects the effects bank (`BANK_VALUE`) and calls `BALL_ENTRY` |
| `hero` (~279) | selects the basketball player's bank (`HERO_BANK`) |
| `crush` (~292) | selects `$08F1` (bank 49) for the ribbon controller |
| `final_boy` (~269) | selects `$08F1` for the finale controller |
| `ribbon_copy` (~759) | selects the frame bank from `$26FC+X` or `$08C0+39` |
| `banana_bootstrap` (~769) | selects the banana resource bank (`bank_value(46)`) |
| `hero_cutaway` (~722) | selects bank 2 (Trevor) via `post_trevor_director` |

`[READ]` Ribbon frame selection (`ribbon_copy`, `build_bitmap_sequence.py`
~759–767):

```
LDA $D301 / PHA
LDX $83ED                  ; frame number
CPX #FRAME_KEY (36)        ; final frame?
BNE ribbon_frame_bank
LDA $08C0+39               ; final bitmap in bank 39
STA $D301
LDA #(BITMAP_SOURCE>>8)
JMP ribbon_source_ready
ribbon_frame_bank:
LDY ribbon_banks,X         ; table: 8 + i//6
LDA $26FC,Y                ; music bank selector
STA $D301
LDA ribbon_sources,X       ; source page (A) for the compositor
...
```

`[READ]` `ribbon_banks` is the table `8 + i//6` for `i` in `0..35`, that is six
frames per bank in banks 8–13 (the original music banks).

## 7.3. Banks 24–39 and the side compositor

`[READ]` `ribbon_dance.install_side_actor` places one side-actor phase in each of
the 16 banks (24–39). Bank selection:

```
LDA $83E0        ; phase/scene
...              ; (SCENE)
LDA $08C0+24+phase
STA $D301
```

`[READ]` Bank 39 additionally contains the final boy bitmap
(`final_boy.install_bitmap`), so it must not be cleared.

## 7.4. Banks 40–48 (plasma, fireworks, bananas)

`[READ]` `title_plasma` selects banks 40/41 for the two title screens, and
`title_fireworks` adds the controller and shapes in the free tails of the same
banks.

`[READ]` `banana_cache` uses:

- `RESOURCE_BANK = 46` — compressed frame sources,
- `SPARE = 48` — temporary buffer for frames that overlap the source,
- banks 40–47 become raw banana frames after the title ends (temporal overlay).

`[READ]` Switching to the banana resource bank has its own trampoline
(`banana_bootstrap`), which preserves PORTB and works only when the high byte of
the tick is `$0C` (ticks 3072–3327).

## 7.5. Bank 49 — controllers

`[READ]` Bank 49 contains:

- the ribbon and fireworks controller (`ribbon_dance.install_control`),
- the final boy controller (`final_boy.install_control`),
- anchor tables, wind shapes and the final orbits.

`[READ]` Selection: `LDA $08F1 / STA $D301` (because `bank_value(49) = $08C0+49
= $08F1`).

## 7.6. Music NMI

`[READ]` `music_entry` (in the main code) does:

```
PHA / TXA / PHA / TYA / PHA
JSR outro_palette      ; terminal palette router
LDA $D301
STA $83FE              ; shadow save
LDY $24A5
LDA $26FC,Y
STA $D301              ; music bank according to the original table
JMP $2218              ; original handler
```

`[READ]` `music_exit` restores PORTB from `$83FE` and handles the additional
colours only in scene 14.

`[CONCLUSION]` The music bank is selected **in the NMI handler**, not in the
foreground — which is why the foreground must restore PORTB before returning.

## 7.7. Risks

- `[READ]` All switches rely on `LDA $D301`; on a clone with an unreadable PORTB
  one would have to keep a separate shadow in RAM.
- `[READ]` Bank 39 and bank 49 are shared by several systems — they must not be
  overwritten.
- `[LIMITATION]` The py65 tests do not model the effect of ANTIC DMA on the
  switch timing; raster stability is confirmed only by hardware.
