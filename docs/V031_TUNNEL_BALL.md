# v031 — piłka w głębi tunelu

W punkcie zbiegu tunelu znajduje się pomarańczowo-złota piłka koszykowa.
Osiem masek obraca zakrzywione szwy i lekko zmienia promień. Ciemny obrys
odcina piłkę od mozaiki. Cztery pociski krążą wokół niej z krótkimi ogonkami;
kolor iskier przechodzi przez paletę Atari. Piłka występuje tylko w motywie
tunelu, nie w obrotowych kaflach. Granice scen i zegar muzyki bez zmian.

## Sprzęt i pamięć

- P0/P1: dwie połówki pomarańczowo-złotej piłki; P2/P3: szwy i obrys.
- Rozdzielczość masek 16×32, podwójna szerokość graczy i podwójne linie DMA:
  obszar 32×64 w logicznych współrzędnych ekranu (koło przy proporcji pikseli Atari).
- M0–M3: niezależne pozycje czterech iskier; tryb piątego gracza, kolor `$D019`.
- PRIOR `$11`, DMACTL `$2E`, GRACTL `$03`. Motyw kafli wyłącza PMG.
- Kod i tablice 1595 B w wolnym ogonie banku 17, `$7800–$7E3A`.
  Bez nowych banków: nadal 33 banki.
- Wrapper z RAM niebankowanego przełącza po rendererze mozaiki bank 17,
  wywołuje efekt i odtwarza PORTB. Wrapper NMI pozostaje bez zmian.
- Główny callback 1783 B; usunięto nieużywane gałęzie starego kalejdoskopu.
- Wyjście z mozaiki przywraca grafiki PMG tańca. Bez zmian bitmapy tunelu.

## V5–V7: wyniki

[ODCZYT] 47 testów PASS:

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
```

Testy obejmują osiem obrotów, rozłączne maski koloru i szwów, wszystkie cztery
pociski, ruch przy nieruchomej bitmapie, wyłączenie przy przejściu do kafli,
przywrócenie gwiazdek tańca i zachowanie banku podczas przerwań muzyki.
Aktualizacja na trzymanej klatce tunelu kosztuje w teście poniżej 14000 cykli
instrukcji (bez DMA, NMI i oczekiwania na raster).

[ODCZYT] Atari800 PAL, `-1088xe`, Altirra OS: 89 zrzutów pamięci obejmujących
wszystkie klatki mozaiki, wcześniejsze sceny i przejścia. Piksele bitmapy
zgodne ze źródłem; cztery płaszczyzny PMG piłki zgodne z maskami obrotu,
pociski obecne w motywie tunelu.

[ODCZYT] Pełne cyfrowe porównanie stereo POKEY, próbka co 78 linii:

```sh
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py \
  --demo build/visual-prototype-v031.xex --seconds 12
```

8 265 816 identycznych bajtów, około 2302,5 s emulacji; cały utwór pokryty.
Nie wykonano osobnego odsłuchu na fizycznym Atari ani testu w Altirra.

## Pliki

- `build/visual-prototype-v031.xex`
- `build/v031-tunnel-ball.gif` — próbki kodu 6502 co 8 ticków; kolory PAL przybliżone,
  podgląd nie jest pomiarem liczby klatek osiąganej przez emulator.
- `build/v031-tunnel-ball-sheet.png`

SHA256 v031: `db98f9398570e10238a6a411734d7cb1ac9b52fac9cfef3c4885954c7913ade8`.
Zachowano v029 (`c8a509af600bafa2c16e198cf5c2f90ecf2afb9f1a33fee81dee8540107543f7`)
i pośredni v030. Builder odmawia nadpisania istniejącego XEX.
