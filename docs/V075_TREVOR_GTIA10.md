# v075 — Trevor w GTIA 10

[ODCZYT] Scena Trevora używa ANTIC F / GTIA 10 (80 × 192). Cztery oryginalne kadry i animowany tunel przekonwertowano do palety o niezależnych odcieniach i jasnościach. Liczba wykorzystanych kolorów zależy od ujęcia. Podczas uderzenia obraz oszczędza rejestry kolorów duszków na czarne litery i cząstki; kolor dymku jest współdzielony z rejestrem tła GTIA 10. Pierwszy kolor PM jest czarny, aby uniknąć zmieniającego się koloru ramki, więc pierwszy pocisk jest ciemny. Utrzymano czas scen i zachowanie BANG.

[ODCZYT] Przed wyświetleniem ujęcia jego nieaktywna display lista dostaje tryb F; mozaika przywraca E. Identyfikatory pamięci podręcznej Trevora i mozaiki rozdzielono, żeby przy przejściu wykonać zmianę trybu. Test obejmuje bezpośrednie przejście na granicy sceny i zachowanie muzycznych DLI.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 63 testy OK. `tools/check_playback.py --demo build/visual-prototype-v075.xex --seconds 12`: 8 371 872 identyczne bajty stereo POKEY; cały utwór. Podgląd GIF pochodzi z Atari800 7.2.1 (PAL, 1088XE, Altirra OS, turbo, bez odsłuchu). Nie sprawdzano na fizycznym Atari.

[ODCZYT] `releases/visual-prototype-v075.xex`, SHA-256 `081fa9c9db74224164305cf1b2895c09efde5b992897ace1155bcc25a904a7d4`.
