# v049 — Trevor przed poruszającym się tunelem

Obie istniejące pozy Trevora z części energetycznej zostały wycięte z bitmapy
maskami w `tools/trevor_polished.py`; ich piksele wewnątrz masek pozostały takie
same. Dawne nieruchome tło zastąpił tunel o pierścieniach rozszerzających się
od środka. Daje to wrażenie przemieszczania się widza w kierunku Trevora.
Cztery ruchome iskry PMG pozostają. Dwa wcześniejsze kadry wejścia do sali,
uderzenie w ticku 26928 i wyjście w ticku 32912 są zachowane.

Tunel ma 16 faz zmieniających się co 16 ticków, dla każdej z dwóch póz.
Obraz jest składany podczas budowania i kopiowany do nieaktywnego bufora;
Atari nie składa osobnych bitmap w czasie rzeczywistym. Banki z kopiami kodu
mają po 16 KiB, są wykrywane przez sprawdzanie aliasów i łącznie demo używa
54 banków (864 KiB). Selektory nowych wariantów `$08D8–$08E7`. Oryginalny
bank 17 nadal obsługuje piłkę w tunelu/rotatorze. Sekwencja kolorów pozostała.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 55 testów PASS.
Testy obejmują wszystkie fazy, zachowanie pikseli Trevora w maskach, zmianę
samego tła, obie pozy, granice scen i PMG. Atari800 PAL 1088XE: 39 zrzutów
obejmujących wszystkie fazy i obie pozy, wejście oraz restart; zawartość
aktywnej bitmapy jest zgodna z wygenerowaną grafiką.

[ODCZYT] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v049.xex --seconds 12`: 8 601 480 identycznych bajtów
stereo POKEY (~2396,0 s emulacji, cały utwór). Nie wykonano osobnego odsłuchu
na fizycznym Atari. Podgląd: `build/v049-trevor-tunnel.gif`; kolory przybliżają
PAL, a prędkość odpowiada wybranym fazom zegara muzyki.

SHA256 XEX: `55405a1328e9fce22f1b574f39ad68f20767be0d701c443bb125585a32c101a7`.
Poprzednie XEX-y zachowane.
