# V184 — gwizd o jeden beat wcześniej

Na życzenie użytkownika wejście gwizdu wraz z ostatnią pozycją dziewczyny
przy drzwiach przesunięto o 94 ticki (około 0,47 s) wcześniej: z ticku 5610
na 5516. Dziubek i emisja PMG zaczynają się razem. Wspólna stała
`school_story.WHISTLE_START` steruje zarówno sceną 12, jak i zegarem PMG.

Końcowe ujęcie trwa do dotychczasowego ticku 5984. Pozostałe fazy spotkania,
tor dziewczyny, ruch nut i kolejne ujęcia zachowane. Bez wzrostu kodu i banków:
316 wierszy, 12 158 B danych wierszy, 2552 B kodu głównego.

- XEX: `build/visual-prototype-v184.xex`; dev identyczny.
- SHA-256: `0237b12cca45dd65878fc3cbc2b2ddefc438e3e40fb36b6914df6483eea5920c`.
- 13 testów CPU/grafiki zaliczonych; sprawdzono również brak PMG tick przed
  nowym początkiem i emisję przy ustach od nowego początku.
- Nie wykonywano nowego odtwarzania emulatorowego ani sprzętowego.
