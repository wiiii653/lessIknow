# v051 — komiksowy BANG Trevora

W energetycznej części sceny, przy pozie z pięścią skierowaną do przodu,
dawne małe iskry ustępują na chwilę komiksowemu efektowi. Rozbłysk narasta,
pojawia się czarny napis BANG! na migającym jasnym tle, a całość rozpada się
na rozprysk. Pozostałe momenty sceny zachowują iskry. Animowany tunel,
Trevor, cięcia i granice aktu pozostały bez zmian.

Cztery duszki tworzą litery, a cztery szerokie pociski tworzą kształt wybuchu
w trybie piątego gracza; jego kolor zmienia się z zegarem muzyki. Fazy efektu
są przypisane do zegara playera: 0–15 ticków narastanie, 16–95 napis,
96–127 rozprysk. Efekt pojawia się przy pozie z ciosem, następnie wracają iskry.
Po opuszczeniu sceny poprzednie duszki i pociski są odtwarzane. Użycie piątego
gracza i priorytetów opisuje [Altirra Hardware Reference Manual](https://www.atari800xl.eu/docs/reference/altirra-hardware-reference-manual.pdf).

Podgląd programowy poprawiono tak, aby przy `PRIOR=$11` najpierw rysował piątego
gracza, a potem litery na duszkach. Kolory PAL w podglądzie są przybliżone.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 57 testów PASS.
Testy obejmują wszystkie fazy, glify BANG!, dane pocisków, powrót iskier i
przywrócenie PMG sceny tańca. Atari800 PAL 1088XE: zrzuty danych PMG podczas
narastania, napisu i rozprysku oraz na granicach scen.

[ODCZYT] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v051.xex --seconds 12`: 8 224 920 identycznych bajtów
stereo POKEY, około 2291,1 s emulacji, cały utwór. Bez osobnego odsłuchu na
fizycznym Atari. Podgląd: `build/v051-trevor-bang.gif`.

SHA256 XEX: `2e05ae19460fcb15921634fd2ae40671e6cbd2e8808c376334e59632e0e81733`.
Poprzednie wersje zachowane.
