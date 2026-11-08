# V161 — powrót do grafiki bez ditheringu

Na życzenie użytkownika usunięto dodany w v159 raster z przejść cienia
bananów i krawędzi wiatraka tunelu. Przywrócono gładkie barwne pola.
Cykl PMG v160, bijące serce i zasłanianie otworu aktualnym efektem
pozostają zachowane. Nie przywrócono osobnej osłaniającej piłki ani
fajerwerków cyklu.

[ODCZYT] Porównanie po załadowaniu XEX potwierdza:

- wszystkie 64 klatki i pełne banki rotatora/tunelu (loader 3–18) są
  identyczne bajt w bajt z v158, sprzed ditheringu;
- wszystkie inne banki oraz cały niebankowany RAM są identyczne z v160.

To wyłącznie podmiana danych bitmap. Brak zmian kodu Atari, rozmiarów
banków, zapotrzebowania na RAM, przebiegu muzyki i ticków scen.
Mapa pamięci i bilans v160 są nadal aktualne.

[ODCZYT] `make check`: 124 testy, 121 zaliczonych, 3 pominięte
(brak archiwalnego v126), 90,701 s.

Nie powtarzano odsłuchu ani porównania POKEY: nie zmieniono kodu ani danych
muzyki. Ostatnia kontrola stereo POKEY v160 obejmowała cały utwór.
Testy py65 nie modelują DMA ANTIC i nie ustalają FPS na fizycznym Atari.

## Wydanie

`build/visual-prototype-v161.xex` i JSON.
Podgląd: `build/v161-smooth-textures.png`, po callbacku 6502, paleta przybliżona.

SHA-256 XEX: `ba6f25cf957b46d316b1b21858f596edb95bac03715d91094f56f1f68823751b`.
Numerowane XEX/JSON są identyczne z plikami roboczymi dev.
