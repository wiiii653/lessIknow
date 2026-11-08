# V179 — nieprzezroczysta sylwetka i reakcja po przejściu

V179 uzupełnia maskę portretu w `arena_art.actor_mask()`: czarne piksele
włosów i konturu wewnątrz prowadzącej maski sylwetki są teraz zachowywane jako
nieprzezroczyste. Kolorowe elementy postaci nadal korzystają z selekcji
spójnych obszarów, co utrzymuje czysty szyld i tło poza chłopcem.

W pierwszym szerokim kadrze chłopiec pozostaje w neutralnej pozie. Gdy
dziewczyna przejdzie przez pierwszy plan, kolejne jej ujęcia są już połączone
z portretem, w którym chłopiec puszcza oko i robi dziubek; wtedy pojawiają się
też klucze wiolinowe i nuty. Zachowano istniejące kadry, ticki i granice scen.

- Podgląd klatek kompozycji: `build/v179-opening-frames.png` (nie jest to
  przechwycenie z emulatora).
- XEX: `build/visual-prototype-v179.xex`.
- 286 współdzielonych wierszy, 11 034 B danych wierszy, 2 552 B kodu.
- SHA-256: `c6bde5abaaa7d5a472d975c811b2c2f82c61c9d212e3ef8a9772ff1a106fb101`.
- Build zakończony powodzeniem. Testów ani odtwarzania emulatorowego nie
  uruchomiono.
