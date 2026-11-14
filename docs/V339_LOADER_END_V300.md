# V339 — loader i końcówka z v300

Przywrócono treść ekranu ładowania z v300 oraz bazową obsługę końcowej sceny:
reset klatki chłopca, ładowanie terminala przez bootstrap i fade do czerni.
Przywrócono też znaczniki czasu końcówki z v300: scena chłopca zaczyna się na
ticku 49850, tekst terminala kończy się na 59085, fade zaczyna się na 59705,
a trwała czerń na 59833.

Aktualne creditsy i greety, w tym `A\SLOP` i `ATARIMUZEUM.PL`, pozostały.
Nie uruchamiano testów, emulatora ani próby na Atari. Stereo XEX zbudowano z
298 współdzielonymi wierszami i 2560 B kodu głównego. v330 pozostaje ostatnią
wersją potwierdzoną na fizycznym Atari.
