# v038 — palety rotatora i tunelu

Rotator i tunel zmieniają parę barw raz na pół taktu (187 ticków). Sekwencja
obejmuje 161 różnych uporządkowanych par odcieni, bez powtarzania zestawu:
16 par w pierwszym wystąpieniu (tick 11968–14959), kolejne od ticku 32912
przez koniec utworu. Dwa odcienie w parze są zawsze różne. Poszczególne
odcienie siłą rzeczy wracają w innych zestawieniach: GTIA ma skończoną paletę.
Jasność nadal pulsuje w rytmie. Gdyby efekt trwał poza końcową pozycję 59840,
utrzymywana jest ostatnia para zamiast odczytu poza tablicą.

Piłka i satelity zachowują istniejącą animację kolorów PMG. Bez zmian granic
scen, geometrii efektu, banków pamięci czy muzycznego przerwania.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 50 testów PASS;
dodatkowy test wykonał callback 6502 dla wszystkich 161 par, sprawdzając brak
powtórzeń, dwa różne odcienie i puls jasności.

[ODCZYT] Atari800 PAL, 1088XE, stereo POKEY: `APPIMAGE_EXTRACT_AND_RUN=1
python3 tools/check_playback.py --demo build/visual-prototype-v038.xex --seconds 12`
porównał pełny utwór: 8 702 928 identycznych bajtów, około 2424,3 s emulacji.
Nie wykonano osobnego odsłuchu na fizycznym Atari.

Podgląd 12 kolejnych zestawów: `build/v038-palettes.png` (paleta PAL
przybliżona). SHA256 XEX v038:
`7c8e7be755c581d7246f17baa516890ed7445ad8622cb9f8b65dd0bcb7863031`.
Poprzednie pliki XEX pozostają zachowane.
