# V255 — wyraźna zmiana toru nad chłopcem

[ODCZYT] Kolejne linie terminala nadal wybierają cel orbity gwiazdek/nut.
Osiem kształtów przechodzi teraz od wysokiej, wąskiej elipsy (promienie
9 × 30) do szerokiej, płaskiej (30 × 9), zamiast podobnych elips różniących
się głównie kątem. Zmiana odbywa się płynnie o jeden stopień co 8 ticków;
faza obiegu pozostaje jak wcześniej, co 16 ticków. Sąsiednie kształty
zmieniają współrzędną duszka najwyżej o 4 jednostki. Tekst, terminy,
kolory i fade zachowane.

[ODCZYT] Testy finale sprawdzają różnicę skrajnych orbit, kolejne cele,
płynność, aktywny bufor, powrót do sceny oraz tekst. Brak wizualnej oceny
na fizycznym Atari; testy CPU nie mierzą ANTIC DMA ani FPS.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 266 664
bajty identyczne z v035; porównanie obejmuje cały utwór.

[ODCZYT] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 197/197
przypadków, bez pominięć; 150,166 s.
