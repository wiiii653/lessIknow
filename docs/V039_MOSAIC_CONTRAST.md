# v039 — kontrast szachownicy

Palety rotatora i tunelu wybierają barwy o odległości co najmniej 60° według
przybliżonego koła barw PAL używanego w podglądzie. Jedno pole jest dodatkowo
jaśniejsze. Filtr sprawdza obie fazy pulsowania, aby nie dobierać podobnych
kolorów także w przyciemnionej fazie. Podgląd PAL jest przybliżeniem; rzeczywisty
wygląd zależy od wyświetlacza i emulacji.

W całym utworze 161 różnych par wartości kolorów. Pierwsze 144 mają różne
pary odcieni; po ich wykorzystaniu ostatnie 17 wraca do wcześniejszych odcieni
z odwróconą różnicą jasności, zachowując kontrast. Pozostały rytm zmian,
animacje, PMG, przejścia i czasy scen bez zmian.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 50 testów PASS;
sprawdzono 161 kombinacji w obu fazach jasności i brak identycznych zestawów.

[ODCZYT] Atari800 PAL 1088XE stereo POKEY: `APPIMAGE_EXTRACT_AND_RUN=1 python3
tools/check_playback.py --demo build/visual-prototype-v039.xex --seconds 12`:
8 954 784 identycznych bajtów (~2494,4 s emulacji), pełny utwór. Bez osobnego
odsłuchu na fizycznym Atari. Podgląd: `build/v039-palettes.png`.

SHA256: `6e37272884e90d8125ae8204e04980c74ee8932a641cb9559c6663a007580b77`.
