# v042 — piłka w rotatorze i tunelu

Piłka pozostaje widoczna zarówno w tunelu, jak i w rotatorze. W tunelu jest
na środku. Podczas 1024-tickowej fazy rotatora wykonuje pełne poziome wahnięcie:
środek → prawa strona → środek → lewa strona → środek; skrajne odchylenie to
40 logicznych pikseli. Ruch i pozycje satelitów są liczone względem piłki.
Na granicy z następnym tunelem jest ponownie na środku. Rotacja, tęczowa paleta,
cztery duszki i cztery pociski zostają zachowane; czasy scen bez zmian.

Tablica 64 położeń jest indeksowana z zegara muzyki, bez zależności od liczby
wywołań renderera. Klatki bitmapy rotatora oraz istniejąca sekwencja jego
kolorów nie uległy zmianie. Procedura PMG w banku 17 ma 1817 bajtów i mieści
się w przedziale `$7800–$7FFF`. Po opuszczeniu sceny odtwarzana jest grafika
PMG dla tańca.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 53 testy PASS,
w tym 64 fazy przelotu, obie skrajne strony, ruch wszystkich pocisków z piłką,
powrót do środka, przejścia scen i odtworzenie duszków tańca.

[ODCZYT] Atari800 PAL, 1088XE: 11 zrzutów obejmujących fazy przejścia przez
rotator i powrót do tunelu, położenie oraz dane graczy i pocisków. Porównanie
stereo POKEY `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v042.xex --seconds 12`: 8 250 336 identycznych bajtów,
około 2298,2 s emulacji i cały utwór. Bez osobnego odsłuchu na fizycznym Atari.

Podgląd: `build/v042-rotator-ball.gif` (kolory PAL przybliżone). SHA256 XEX:
`70deb4337487574a6d40ce04535bf81e536abaa0cf3dd2550f2c3a0bab33581a`.
