> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# 4. Bank Switching and Detection

## 4.1. PORTB

On Atari XL/XE, `$D301` is PORTB. On a standard 130XE, its bits control OS and
BASIC ROM visibility, CPU banks and ANTIC banks. One-megabyte expansions
repurpose different bits to address 64 banks of 16 KiB. Selector bytes are
therefore hardware-specific.

The selector map documented here was checked on the user's 1 MB Rambo-style
configuration. The test covered all 64 candidate selectors and reported
`BANK MAP PASSED`. It is evidence for that machine only.

## 4.2. Selector candidates

`tools/school_portrait_bank.py` defines these 64 candidate PORTB values:

```
81 83 85 87 89 8B 8D 8F   A1 A3 A5 A7 A9 AB AD AF
C1 C3 C5 C7 C9 CB CD CF   E1 E3 E5 E7 E9 EB ED EF
01 03 05 07 09 0B 0D 0F   21 23 25 27 29 2B 2D 2F
41 43 45 47 49 4B 4D 4F   61 63 65 67 69 6B 6D 6F
```

These are eight groups of eight: bits 5–7 select a group and bits 1–3 select
within that group.

## 4.3. Startup detection by the original v035 player

The first player INIT at `$2000` selects a table based on the detected memory
configuration, then probes 14 selectors. It records the results in
`$26FC–$2709`. In the tested configuration the values are:

```
81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB
```

The candidate tables are loaded into RAM from XEX segment `$24BD–$28BC`.
Pointers at `$2734/$2737` select the appropriate list. Detection writes a
marker through `$4000`, switches selectors, and checks that the marker reads
back from the same bank.

## 4.4. Additional video banks

`tools/school_portrait_bank.py` allocates 50 extra video banks. It uses the
player's detected selectors as its starting point, then probes the hardcoded
candidate list to reject aliases. The first two additional selectors are
derived arithmetically from the detected table rather than individually
checked; later selectors are found by alias probing.

The resulting selector values are stored at `$24B3–$24B5` and `$08C3–$08F1`.
The helper maps a logical index through `bank_value(index)`; code should use
that helper rather than assume a raw logical bank number is a PORTB value.

## 4.5. Known limits

- The first two derived selectors are not independently checked for aliasing.
- The no-free-bank path loops after setting the background colour; it does not
  print a diagnostic message.
- Marker-based alias probing has a theoretical false positive if an existing
  bank happens to contain the test marker at the probed location.
- The tests detect selector aliasing; they do not prove that every possible
  physical bank exists on arbitrary expansion hardware.
- Some runtime helpers read and restore `$D301`. The tested expansion supports
  that behavior; clones where PORTB reads differ need separate validation.

## 4.6. Hardware evidence

`releases/avg-bank-map-diagnostic-003.xex` tested all 64 selectors by writing
unique markers and checking that no two selectors alias. It displayed
`BANK MAP PASSED` on the tested machine. Do not generalize this result to other
memory-expansion designs without a corresponding hardware test.
