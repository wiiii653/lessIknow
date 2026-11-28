> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# Banked memory report — v168

## Result

The target configuration provides 64 banks of 16 KiB each, 1 MiB of banked
memory in total. **There is no wholly free bank.** Confirmed gaps inside
already used banks add up to **31 623 B (30.88 KiB)**.
That is about 3.0% of the banked capacity, but the memory is divided into small
areas with different owners and access constraints. It cannot be
treated as one free block or as a new bank.

V168 changes the geometry of Trevor's tunnel graphics within the existing phase
banks. It does not allocate a bank or increase the size of the main code. The set
of gaps remains as in the verified v166 map; the generator details and
stream sizes are in `V166_SMOOTHER_DANCE.md`.

## Breakdown of confirmed gaps

| Owner / location | Free bytes | Notes |
|---|---:|---|
| Loader index 2 — tunnel helper bank | 4 251 | Largest single gap: `$6E0F–$77FF`, 2 545 B. The tunnel helper stays at `$7800–$7FFF`. |
| Indexes 24–31 and tails 32–38 | 14 016 | Covers 4 096 B in side-actor banks and 9 920 B of tails of banks with intermediate frames. |
| Slots of former ball masks | 7 212 | Nine gaps of 512 B and seven tails of 372 B. Part of index 39 is occupied by the final boy. |
| Original player banks 9–14 | 6 144 | 1 024 B each under `$7C00–$7FFF` in each of the six dance banks. |
| **Total** | **31 623** | Scattered gaps in used banks. |

## Occupancy that must not be confused with free space

- Loader indexes 0–63 are allocated. "Loader index" means the number
  selected by `school_portrait_bank.bank_value()`, not the PORTB number
  or the bank number from the original player.
- Indexes 0–7 cover code/player and music. The v035 decoder requires eight
  banks; the idea of reducing to seven is not available.
- Player banks 9–14 hold compacted dance frames; only the
  indicated tails are free, not whole banks.
- Bank 49 contains Trevor's silent graphics, the ribbon and finale controller,
  Trevor's code, ribbon data and metadata. Its unused historical slots are not
  a free block after the v166 release.
- The XEX stores full banks. Free tails reduce the chance of collision on
  the next allocation, but they do not reduce the XEX size proportionally to
  the number of empty bytes.

**Sources read:** `AGENTS.md` (Current Memory Ownership),
`docs/backup/V166_SMOOTHER_DANCE.md` and `build/v168-allocations.json`.
V168 did not re-audit every memory cell or run hardware tests; the number of
gaps is based on the detailed v166 audit, and the lack of allocation change
follows from the use of existing slots.
