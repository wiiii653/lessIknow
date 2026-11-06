# V091 — dithering kolorów plazmy

Przejścia pomiędzy odcieniami poruszających się blobów wykorzystują
uporządkowany raster Bayera 4×4. Raster miesza sąsiednie odcienie przy ich
granicach, a jego położenie jest stałe względem ekranu. Efekt jest obliczany
podczas budowania klatek i wykorzystuje istniejące 16 klatek oraz te same
banki; nie zwiększa pracy procesora podczas odtwarzania. Zachowano ciemną
jasność, rastrowe wyłanianie i zanik oraz maski liter i ich przejście.

[ODCZYT] 69 testów py65 zakończyło się poprawnie, w tym test rozkładu
rastra i zachowania maski liter. [ODCZYT] Porównanie XEX v090 i v091 wykazało zmiany wyłącznie w czterech
segmentach banków klatek plazmy; pozostałe segmenty są identyczne.
[ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: zapis rejestrów POKEY był
identyczny z v035 dla 6 047 640 bajtów po jednokrotnym wyrównaniu początku;
porównanie obejmuje cały utwór. [WNIOSEK] Nie zastępuje to odsłuchu ani oceny
obrazu na rzeczywistym Atari.

Programowy podgląd `build/visual-prototype-v091-plazma.gif` ma przybliżone
kolory i tempo; nie jest nagraniem emulatora. XEX: `build/visual-prototype-v091.xex`;
SHA-256 `4de36c73b10fb178827663e93f740a3ec7fcb6a8bb10a38cb3b22553eeb3b2a7`.
