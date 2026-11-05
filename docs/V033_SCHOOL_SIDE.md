# v033 — boczne ujęcie przed szkołą

Przebitka w tickach 3553–4113 pokazuje blond dziewczynę z profilu, w pół kroku,
przed szkołą. To statyczny kadr przedstawiający ruch, nie animacja chodu.
Oryginalna przebitka kończyła się w ticku 3927; wydłużenie o 187 ticków
(~0,94 s) skraca ujęcie chłopca po niej. Dziewczyna wchodzi na pierwszy plan
w dotychczasowym ticku 4488, pozostałe granice scen bez zmian.

Źródło: `assets/art/source/act1_girl_side_walking_v033.png`. Wygenerowano
na podstawie istniejących ilustracji szkoły i dziewczyny, z profilem w kroku,
w europejskim stylu komiksowym i paletą czerni, cyjanu, różu i jasnej brzoskwini.
Kadr przeliczany jest do 160×64 i wyświetlany przez istniejący renderer.

[ODCZYT] 48 testów PASS (`make check PYTHON=/tmp/tliktb-girl-venv/bin/python`),
w tym granice przebitki i sąsiadujących ujęć. Atari800 PAL 1088XE, stereo
POKEY: `tools/check_playback.py --demo build/visual-prototype-v033.xex --seconds 12`
z `APPIMAGE_EXTRACT_AND_RUN=1`: 8 606 664 identycznych bajtów rejestrów,
~2397,5 s emulacji, pełny utwór. Nie wykonano odsłuchu na fizycznym sprzęcie.

Podgląd: `build/v033-girl-side.png`. SHA256 XEX:
`3b47be7910e46ba2537ac0cee18a0eb91e0eaf066ed9f3bd1161c72de5725fd9`.
