# v046 — kołysanie piłki w tunelu

Piłka na końcu tunelu porusza się w poziomie o maksymalnie pięć logicznych
pikseli oraz w pionie o maksymalnie cztery linie obrazu. Niezależne przebiegi
sinusoidalne tworzą ruch w różnych kierunkach; cztery satelity poruszają się
razem z nią. Sprzętowe playery i pociski, obrót oraz tęczowe kolory pozostają
w użyciu. Ruch w rotatorze i momenty przejść pozostały bez zmian.

[ODCZYT] Test 32 faz sprawdza każdy piksel geometrycznej dziury tunelu
(`radius < 5` w układzie tekstury) pod kątem zasłonięcia przez maski czterech
playerów. Obszar jest pokryty we wszystkich fazach. 54 testy PASS:
`make check PYTHON=/tmp/tliktb-girl-venv/bin/python`.

[ODCZYT] Atari800 PAL 1088XE: 32 zrzuty faz pokazują prawidłowe przesunięcia
oraz obecność danych duszków i pocisków. Porównanie stereo POKEY poleceniem
`APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v046.xex --seconds 12` dało 7 840 944 identyczne bajty
(~2184,2 s emulacji, cały utwór). Nie wykonano osobnego odsłuchu na sprzęcie.
Podgląd: `build/v046-tunnel-bob.gif`, barwy PAL przybliżone.

SHA256 XEX: `174064fc5525a5097869e609955467807532d647928245ce55ab57203d146bad`.
Poprzednie XEX-y zachowane.
