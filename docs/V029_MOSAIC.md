# v029 — mozaika demoscenowa

Zastępuje dawny nieruchomy obraz z przesuwaniem wierszy dwoma geometrycznymi
motywami: obracającymi się kaflami z zoomem oraz skręconym tunelem z pierścieni.
64 klatki 160×96, dwukrotne powtórzenie linii przez ANTIC daje obraz 160×192.
Kontury, jasne krawędzie i ciemne szczeliny zachowują czytelność w czterech kolorach.
Jasność pulsuje według zegara playera, modulo 187 ticków. Palety zmieniają się
w czasie. Klatki są generowane matematycznie podczas budowania, bez nowych
obrazów AI i bez obliczeń trygonometrycznych na Atari.

Granice scen pozostają bez zmian: efekt jest używany przez istniejący dispatch
mozaiki w tickach 11968–14959 oraz od 32912. Późniejsze akty nadal korzystają
z tego zastępczego dispatchu; ta wersja nie implementuje ich osobnej dramaturgii.
Efekt wybiera klatkę co 16 ticków (~80 ms), a nie 50 nowych klatek na sekundę.
GIF pokazuje klatki wykonane przez kod 6502, z przybliżeniem palety PAL.

## Pamięć i wykonanie

- 16 nowych banków po 16 KiB; razem 33 banki / 528 KiB rozszerzenia.
- Cztery klatki po 3840 B w każdym nowym banku: `$4000`, `$4F00`, `$5E00`, `$6D00`.
- Identyczny renderer w każdym banku pod `$7C00`, do końca banku `$8000`.
- Nowe selektory PORTB: `$08C3–$08D2`; region `$08C0–$08FF` wyłączony z puli grafiki.
- Rozszerzony alias probe sprawdza wszystkie wcześniej załadowane banki,
  używa dwóch znaczników i odtwarza badany bajt także przy odrzuconym kandydacie.
- `$24B6` to zachowany bajt próby, `$24B7` to tymczasowy selektor próby.
- ANTIC czyta wyłącznie RAM niebankowany. Kopiowanie trafia do nieaktywnego
  bufora `$9000` lub `$B000`; DL przełącza się w pionowym wygaszaniu.
- Niezmieniona klatka pomija kopiowanie. Cache innych scen zostaje unieważniony.
- PMG piłki, pomponów i Trevora pozostają w poprzednich scenach.
- Główny kod zajmuje 1782 B (limit do `$1B00`); dokładna wartość w JSON wydania.

## Walidacja V5–V7

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 45 testów PASS.
Nowe testy obejmują wszystkie 64 klatki, brak zapisów do aktywnego bufora,
cache, przejścia scen, restart i ostatni bank z zachowaniem 32 wcześniejszych.
Test przerwań muzyki obejmuje również mozaikę: bank foreground wraca po NMI,
a piksele pozostają zgodne ze źródłem. Koszt zmienionej klatki poniżej 90000
cykli instrukcji w testowanych fazach (bez DMA/WSYNC i przerwań).

[ODCZYT] Atari800, PAL, `-1088xe`, Altirra OS, stereo POKEY: 89 zrzutów
pamięci, w tym wszystkie klatki mozaiki i przejścia ze szkoły, sali, portretów
oraz Trevora. Obrazy odczytane z aktywnego DL zgodne z grafiką źródłową.

[ODCZYT] Pełne porównanie rejestrów muzyki:

```sh
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py \
  --demo build/visual-prototype-v029.xex --seconds 12
```

7 904 232 identyczne bajty stereo POKEY, około 2201,8 s emulacji, cały utwór.
Rejestracja co 78 linii potwierdza zachowanie czterech aktualizacji na klatkę.
To test cyfrowego strumienia rejestrów; nie jest deklaracją odsłuchu na sprzęcie.

[WNIOSEK] Buforowanie i bankowanie nowego efektu nie naruszają przebiegu
muzyki w sprawdzonej konfiguracji. Fizyczny Atari XE 1 MB i Altirra nie były
osobno testowane w tej iteracji.

## Wydanie

```sh
make build/visual-prototype-v029.xex
```

Builder zachowuje istniejące pliki XEX i odmawia nadpisania. v027 i pośredni
v028 zostały zachowane.

SHA256 v029: `c8a509af600bafa2c16e198cf5c2f90ecf2afb9f1a33fee81dee8540107543f7`.
SHA256 zachowanego v027: `43c4e5bb2120325b0947b6221487cff01ca5a46b38c29669ccc9a1ea42df704f`.

Podgląd: `build/v029-mosaic.gif`, plansza: `build/v029-mosaic-sheet.png`.
