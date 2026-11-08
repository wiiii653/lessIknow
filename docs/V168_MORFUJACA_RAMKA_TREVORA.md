# V168 — morfująca ramka za Trevorem

Geometryczne pasy tunelu za Trevorem płynnie zmieniają kształt w ramach
dotychczasowych 16 faz tła. Kwadratowa/prostokątna perspektywa przechodzi
w owal i wraca do prostokąta przy zawinięciu cyklu. Morph opiera się na
interpolacji normy prostokątnej i znormalizowanej eliptycznej. Ruch jest
wyłącznie w tle: bitmapa postaci, jej kontur, uderzenia, kolory i ticki
pozostają bez zmian.

Zmiana znajduje się w `tools/trevor_polished.py`, w generatorze
`tunnel_frames`. Wykorzystuje już generowane banki faz; nie dodaje danych,
kodu runtime ani banków.

## Wydanie

XEX zbudowano poleceniem `python3 tools/build_bitmap_sequence.py --output
build/visual-prototype-v168.xex`. Budowa zakończyła się poprawnie; główny
callback nadal ma 2546 B. Testów ani odtwarzania obrazu w emulatorze nie
wykonywano w tej zmianie.

SHA-256: `cec65fb359440302247341403ba7f7bd9ce2eca8b58fa83c874b5815b320bcb5`.
