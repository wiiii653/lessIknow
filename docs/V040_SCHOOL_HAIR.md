# v040 — pasma włosów

Usunięto przesuwanie dużego prostokątnego fragmentu włosów, przez które obraz
się rozrywał. Oryginalna sylwetka i włosy pozostają nieruchome względem głowy;
trzy wąskie pasma są zakotwiczone na istniejących pikselach i mają końcówki
poruszające się niezależnie w pionie, z różnymi fazami. Ujęcie nadal jest
przygotowane jako 18 klatek: ruch tła, postaci, kadr i granice scen bez zmian.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 51 testów PASS.
Testy obejmują stałe korzenie na oryginalnych pikselach, ciągłość pasm, trzy
położenia końców każdego pasma, różne fazy i wszystkie klatki ujęcia.
Atari800 PAL 1088XE: 18 zrzutów obrazu zgodnych z wygenerowanymi klatkami.

[ODCZYT] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v040.xex --seconds 12`: 8 747 712 identycznych bajtów
stereo POKEY, około 2436,7 s emulacji i cały utwór. Bez odrębnego odsłuchu na
fizycznym Atari. Podgląd: `build/v040-school-hair.gif`.

SHA256: `fb7487dc9731923fd51dd7b283c4210b689da7a1ed7acb99f4f035b1045da3f4`.
