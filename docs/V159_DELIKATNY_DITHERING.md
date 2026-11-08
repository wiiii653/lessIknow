# V159 — delikatny dithering bananów i wiatraka tunelu

Banany otrzymują rzadki złoty raster na przejściu między cieniem a żółtą
powierzchnią. Wzór 4×4 jest przypisany do współrzędnych tekstury, więc
obraca się razem z owocami. Czarne obrysy i korona kiści nie są zmieniane.

Tunel ma lekki raster mieszający dwa kolory na wąskim pasie krawędzi
ramion wiatraka. Próg obejmuje 3 z 16 pozycji macierzy Bayera tylko w tym
pasie, nie całą powierzchnię. Wzór jest stały w przestrzeni ekranu,
bez losowania lub naprzemiennego przełączania rastra między klatkami.
Białe grzbiety, czarne szczeliny oraz centralny otwór są zachowane.

## Zakres i pamięć

[ODCZYT] Porównanie wszystkich 64 spakowanych klatek v158/v159:

- Rotator: 8920 z 491 520 pikseli zmienionych, **1,81%**. Tylko żółć → złoto;
  żaden piksel czerni nie jest zmieniony.
- Tunel: 9796 z 491 520 pikseli zmienionych, **1,99%**. Tylko mieszanie
  dwóch barwnych pól; żaden piksel czerni ani białego grzbietu nie jest zmieniony.

Rozmiary bitmap/banków i kod Atari pozostają identyczne. Brak dodatkowego
RAM-u, nowych banków, kosztu CPU rasteryzacji lub zmian timeline’u.
Cykl PMG v158 i nieprzezroczysta piłka osłaniająca środek są bez zmian.
Mapa pamięci i bilans v158 pozostają aktualne.

## Walidacja i wydanie

`build/visual-prototype-v159.xex` i odpowiadający JSON.
`build/v159-subtle-dither.png` pokazuje oba efekty po callbacku 6502,
z przybliżoną paletą; nie jest to nagranie emulatora.

[ODCZYT] `make check`: 122 testy, 119 zaliczonych, 3 pominięte
(brak archiwalnego v126), 90,768 s.
[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
9 833 112 identycznych bajtów względem v035 przez cały utwór.

Testy py65 nie modelują DMA ANTIC ani rzeczywistego FPS. Bez odsłuchu
i testu na fizycznym Atari; brak losowego rastra nie jest pomiarem migotania
na docelowym ekranie.

SHA-256 XEX: `5f42b0f3d11381ed8e2193544f46fe9ea07315350cd253f88ce7ae4eec565997`.
Numerowane pliki XEX/JSON są identyczne z roboczym dev.
