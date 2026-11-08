# V153 — wspólna neonowa piłka rzutu, kozłowania i wsadu

Zamiast dawnych prążków i przezroczystych szczelin wszystkie trzy ujęcia
korzystają z pełnej kuli: osiem odmiennych faz obrotu, zakrzywione kolorowe
panele, jasne szwy i refleks oraz ciemniejsza krawędź. Wygląd nawiązuje
do większej piłki v150 z tunelu; kompaktowa wersja zachowuje wielkość
potrzebną do kontaktu z dłonią. Geometria nie pulsuje i nie odsłania tła.

Cztery współpołożone players mają jasności 6/10/12/14. Barwy cyklicznie
przechodzą przez paletę Atari. Trajektorie rzutu i odbić, kotwice dłoni,
uwolnienie piłki, rozbicie tablicy oraz cały timeline v151 są zachowane.

## Pamięć

[ODCZYT] Nowe maski to nadal **8 × 4 × 16 = 512 B**, dokładnie tyle,
ile poprzednio. Zarówno helper rzutu (2235 B), jak i hero (2652 B)
mają niezmienioną długość. Zmieniono dane masek i wartości barw;
**koszt dodatkowego RAM-u i nowych banków wynosi 0 B / 0 banków**.

[ODCZYT] Nadal 64 banki, główny kod 2546 B, tylko 14 B przed `$1E00`.
Odzysk netto względem v141 nadal 23 671 B (23,12 KiB). Nie potrzeba
przełączania do banku dużej piłki podczas rzutu lub wsadu.

## Walidacja

Testy sprawdzają osiem odmiennych masek, wspólną pełną sylwetkę,
niepokrywające się płaszczyzny, zachowanie ruchu i kolorów, kotwice dłoni,
wszystkie fazy wsadu i rozbicia tablicy, przywracanie masek oraz PORTB.

[ODCZYT] `make check`: 116 testów, 113 zaliczonych, 3 pominięte
(brak archiwalnego v126), 87,461 s.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
15 373 584 identyczne bajty względem v035 przez cały utwór.
Bez odsłuchu i testu na fizycznym Atari.

Testy py65 nie modelują DMA ANTIC ani rzeczywistego FPS. Porównanie POKEY
nie zastępuje odsłuchu i kontroli obrazu na fizycznym Atari.

## Wydanie

- `build/visual-prototype-v153.xex` i JSON; identyczne z roboczym dev.
- `build/v153-ball-shot.gif` — rzut.
- `build/v153-ball-dribble.gif` — kozłowanie.
- `build/v153-ball-dunk.gif` — wsad.

GIF-y pokazują callback 6502, z przybliżoną paletą i tempem.
Wcześniejszy kandydat v152 zachowany; v153 usuwa powtórzenia połowy faz.

SHA-256: `784b75809316314ba8e897736083bebb9c417a9e41875519b577f15f18c44a0b`.
