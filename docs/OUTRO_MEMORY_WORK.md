# Credits / greetz — rozpoznanie pamięci

Status historyczny: wstępne rozpoznanie. Implementacja jest podłączona od
v216; aktualny opis: `V216_CREDITS_GREETZ.md`. Eksperymentalnej v199 nie
używać jako wydania. v198 pozostaje punktem odniesienia.

## Odczyty

- `$C000–$CEFF` należy do drugiego bufora bitmapy `$B000–$CEFF`.
  Nie wolno instalować tam zasobów statycznie przed odtworzeniem wcześniejszych scen.
- Zidentyfikowane luki poza bieżącym przydziałem scanline pool i segmentami v035:
  `$28BD–$28FF`, `$2940–$29FF`, `$2A65–$2BFF`, `$2C81–$2CFF`,
  `$2D27–$2DFF`, `$2F7F–$2FFF`, `$307F–$30FF`, `$3135–$317F`,
  `$31A4–$31EF`, `$31F1–$32FF`, `$3E58–$3FFF`.
  Łączna pojemność: 2118 B.
- [ODCZYT] `audit_music_banks.trace` z powyższymi zakresami jako
  `protected_ranges` wykonał inicjalizację dekodera i cały strumień do ticku
  59833. Nie wystąpił odczyt ani zapis muzyki w chronionych zakresach.
- To nie potwierdza jeszcze bezpieczeństwa wszystkich procedur startowych
  playera ani wizualnego działania na Atari.

## Dalsza realizacja

Zweryfikować procedury startowe i spakować zasoby tekstowe wraz z małym
loaderem w sprawdzonych lukach. Po wejściu sceny leżącego chłopca ustalić
bitmapę w jednym buforze; drugi wykorzystać na rozpakowany font i napisy.
Wcześniejsze sceny nadal muszą mieć oba pełne bufory. Zachować 53850 / 56842 /
59085 i istniejące PMG. Żadnych rezerw w bankach rozszerzenia nie przydzielono.
