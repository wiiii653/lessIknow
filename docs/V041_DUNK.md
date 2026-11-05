# v041 — tempo wsadu i śledzenie dłoni

Ujęcie wsadu zachowuje ticki 22440–23935. Przygotowanie trwa 752 ticki,
następne dwie pozy w locie po 224 ticki, a końcowa poza 296 ticków. Zmiany
pozy są zsynchronizowane z istniejącym zegarem muzyki. To cztery ilustracje;
przyspieszenie akcji uzyskano przez ich montaż, bez dodatkowych klatek rysunku.

Środek piłki PMG jest przypięty do dłoni osobno w każdej z czterech póz:
(85,102), (99,28), (115,18), (124,32), w logicznych współrzędnych 160×192.
Po przytrzymaniu przy obręczy piłka spada; błysk następuje przy wypuszczeniu.
Piłka zachowuje kolorowe duszki i pociski.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 52 testy PASS,
w tym położenia piłki na granicach póz, moment wypuszczenia, pojedynczy spadek,
przejście scen i odtwarzanie PMG po restarcie.

[ODCZYT] Atari800 PAL 1088XE: 11 zrzutów faz wsadu, prawidłowe pozy, współrzędne
piłki oraz dane PMG. `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py
--demo build/visual-prototype-v041.xex --seconds 12`: 9 203 904 identycznych
bajtów stereo POKEY, około 2563,8 s emulacji, pełny utwór. Nie wykonano
osobnego odsłuchu na fizycznym Atari.

Podgląd: `build/v041-dunk.gif`. SHA256 XEX:
`6728426166c4151323cb9ccd4def6a81cd00c2d15599eab12a1991d04bc541ee`.
