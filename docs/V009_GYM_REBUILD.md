# Przebudowa sali gimnastycznej — v009

Data: 2026-11-04. Wynik: `build/visual-prototype-v009.xex`.

## Obraz

- [ODCZYT] Sala wypełnia cały kadr: belki i ściany w perspektywie, wysokie
  okna, proporce, boczne trybuny, drzwi, tablica z koszem oraz duży parkiet.
  Postacie mają ciemny obrys i cienie kontaktowe. Geometria jest zapisana
  w `tools/gym_background.py`, kompozycja w `tools/build_sequence.py`.
- [ODCZYT] Pełne obrazy dla solo, duetu i trio zastępują prostokątne maski
  PMG. Tło jest obecne także za tancerkami, a źródłowe kolorowe piksele
  wszystkich czterech póz pozostają zachowane.
- [ODCZYT] Podglądy `build/v009-gym-{solo,duo,trio}.png` odtworzono z RAM
  rzeczywistego Atari800, po starcie loadera i wykonaniu callbacku z aktywnymi
  przerwaniami. Kolory RGB są przybliżone. Obrazy mają proporcje szerokich
  pikseli ANTIC E: 160×192 logicznie odpowiada 320×192.

## V2 — własność PORTB

- [ODCZYT] Wrapper NMI pod `$1963` zachowuje rejestry jak oryginalny player,
  wykonuje WSYNC, zapisuje PORTB i wybiera bank dekodera z `$24A5` oraz tablicy
  `$26FC`. Wchodzi do oryginalnej obsługi pod `$2218`.
- [ODCZYT] Epilog pod `$2312` kieruje do wrappera przywracającego poprzedni
  PORTB przed odtworzeniem rejestrów i RTI. Muzyka może przerwać kopiowanie
  dowolnego z sześciu banków grafiki.
- [ODCZYT] Test py65 wstrzykuje prawdziwe NMI podczas kopiowania w każdym
  banku: poprawny powrót, zachowany PORTB i wynikowy obraz zgodny pikselowo.

## V3 — banki oraz pamięć główna

- [ODCZYT] Wykorzystano sześć banków 9–14, wcześniej zbadanych jako nigdy
  nieczytane przez dekoder v035. Każdy zawiera dwa kadry po 8 KiB: razem
  cztery pozy × trzy liczby tancerek. Banki muzyczne 1–8 są bajtowo identyczne
  z oryginałem. Nie usunięto znacznika końca muzyki w banku 8.
- [ODCZYT] RAM `$9000–$AFFF` i `$B000–$CFFF` to dwa bufory obrazu. CPU kopiuje
  do nieaktywnego bufora przy aktywnych NMI; ANTIC czyta dotychczasowy bufor.
  Przełączenie listy następuje podczas pionowego wygaszania. Każdy wiersz
  pozostaje wewnątrz strony DMA 4 KiB.
- [ODCZYT] `$3300–$3BFF` mieści statyczne bitmapy. Wyłączono starą wizualizację
  wskaźników i inicjalizację fontu. Pięć cyfr starego zegara przeniesiono
  spod `$34DA–$34DE` do `$83F0–$83F4` w kodzie restartu i odliczania; instrukcje
  zachowują typy i czas wykonania.
- [ODCZYT] Pełny przebieg dekodera i restartu przez 59 833 aktualizacje z
  ochroną `$3300–$3BFF` i `$9000–$CFFF` nie wykazał dostępu do tych regionów.
  W tej izolowanej próbie odtworzono oryginalny epilog RTI, ponieważ tracer
  wywołuje `$2210` bezpośrednio. Wrapper osobno obejmuje test przerwań.
- [ODCZYT] 425 statycznych wierszy zajmuje 16 515 B po współdzieleniu;
  callback z wrapperem: 1417 B; tablice wierszy: 3264 B.

## V6 — regresja muzyki i czasu

- [ODCZYT] Atari800, PAL, `-1088xe`, Altirra OS, stereo POKEY, headless.
  DLI pozostają w liniach 0, 78, 156 i 234. Granice scen oraz progi solo,
  duetu i trio zachowują poprzednie wartości licznika muzyki.
- [ODCZYT] Porównanie v009 z v035: **6 620 400 identycznych bajtów stereo
  POKEY**, około 1844,2 s emulacji, obejmujące cały utwór. Początkową ciszę
  wyrównano tylko raz; nie przesuwano ani nie pomijano próbek w trakcie.
- [ODCZYT] Rzeczywiste odstępy między callbackami tańca w Atari800: 16–20
  ticków, około 10–12,5 klatki obrazu/s. W 16 kolejnych kadrach wystąpiły
  wszystkie cztery pozy, z okazjonalnym przeskokiem pozy przy dłuższym
  kopiowaniu. Tick muzyki działa niezależnie i nie gubi aktualizacji.
- [ODCZYT] Nie wykonano odsłuchu ani testu na fizycznym Atari. Ten test nie
  zmienia odstępów DLI w ramach eksperymentu V6.

## Weryfikacja i odtworzenie

- [ODCZYT] 20 testów zakończonych powodzeniem.
- [ODCZYT] Dodatkowo porównano cały raster z RAM rzeczywistego Atari800 dla
  tytułu, pierwszego kadru dziewczyny, solo, duetu i trio: każdy obraz zgodny
  piksel po pikselu z referencją, bez korupcji statycznych danych.
- [ODCZYT] Monitor Atari800 zatrzymywano na `$220D`, po powrocie callbacku;
  zrzuty `$0000–$CFFF` oraz `$D800–$FFFF` zawierały listy ANTIC i dane obrazu.
  Zmieniano licznik `$24A7–$24A9` wyłącznie w teście obrazów, aby szybko
  sprawdzić konkretne sceny. Porównanie muzyki przebiegało bez takiej zmiany.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v009.xex --seconds 10
```

[ODCZYT] Poprzednie XEX-y zachowano; v008 jest pośrednim buildem przebudowy.
SHA-256 v009: `258d94eb37b9efb080438c15276bea685dfd9ef3859a7bb9e5507e95361c2ed6`.
SHA-256 v007 pozostało `60fe082a4fd87b1529ede5d0349adde5a48bb57861a32dd93e9512a12a1f022d`.
