# V189 — przywrócona koszykówka i tablica z v175

## Przywrócone ujęcia

Cały zestaw grafiki kozłowania, wsadu i rozbicia tablicy odtworzono
bezpośrednio z zachowanego XEX-a v175. Źródłem bieżącego buildu jest
`assets/art/reference/v175/basketball.bin`: 12 988 B z banku loadera 1,
$4B80–$7E3B. To pięć pełnych klatek 160×56, trzy łaty ramienia 44×28
i trzy łaty rozbijanej tablicy 48×24.

Zestaw odtwarza osiem oryginalnych póz: cztery różne fazy ręki podczas
kozłowania oraz przygotowanie, wyskok, lot do kosza i wsad. Przywrócona
tablica ma rysunek, wielkość i położenie v175. Pierwsze pęknięcie,
wypadnięcie większych fragmentów i rozsypanie szkła są dokładnie oryginalne.
Piłka, jej satelity, moment przejścia satelitów w odłamki i błysk również
zachowują zgodność z v175. Tło pochodzi z tej samej sekwencji hali ATARI ARENA.

Wersja v177 podmieniła obrazy bez zmiany mechanizmu aktualizacji małego
obszaru ramienia i bez przestawienia łat szkła. Nowe pozy wychodziły poza
ten obszar, dwie fazy ramienia powielały inne, a nowa mniejsza tablica
nie odpowiadała obszarowi pęknięć. Odtworzenie całego zgodnego zestawu
usuwa te rozbieżności; cztery wcześniej niezaliczone testy koszykówki
teraz przechodzą.

## Pamięć i płynność

Przywrócone cztery odmienne fazy ramienia poprawiają czytelność ruchu
bez dodawania nowych danych. Zachowano tempo i klatki kluczowe v175.
Nie dokładano nowych pełnych klatek: jedna kosztuje 2240 B, a w banku
pozostaje 85 B między kodem a DATA, 4 B przed orbitami i 192 B na końcu.

Zmiana dotyczy wyłącznie banku loadera 1; pozostałe 63 banki są identyczne
bajt w bajt z v188. Kod główny nadal zajmuje 2560 B, dane wspólnych wierszy
11 480 B / 298 wierszy. Nie dodano banku ani kosztu dekompresji.
Poprawka ciągłości nut z v188 i dalsze sceny pozostają aktywne.

## Build i sprawdzenie

- `build/visual-prototype-v189.xex` i JSON; dev identyczny.
- SHA-256: `5e597f13563f7b63657a2da29f92bbad4da87a3d981e7ee30ad427db896e8c05`.
- 23 ukierunkowane testy zaliczone: osiem póz, obie serie kozłowania,
  wsad, wszystkie fazy szkła i drobiny, finał, ciągłość PMG, porównanie
  surowych danych oraz działających klatek, piłki i satelitów z v175.
  Log: `build/v189-focused-check.log`.
- `make check`: 144 testy, 135 zaliczonych, 6 niezaliczonych,
  3 pominięte (brak v126). Cztery błędy koszykówki z v188 zniknęły;
  pozostałe dotyczą wcześniej opisanych testów szarf/pamięci (4),
  starego progu aktu 5 (1) i limitu CPU (1).
  Log: `build/v189-check.log`.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 992 848 identycznych
  bajtów z v035; cały utwór. Log: `build/v189-playback-check.log`.
- Podglądy po callbackach 6502: `build/v189-basketball.gif` i
  `build/v189-basketball-preview.png`. Nie modelują DMA ANTIC ani rzeczywistego
  FPS; nie wykonano nowej oceny na fizycznym Atari.
