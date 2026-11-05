# v035 — dwa plany w przebitce przed szkołą

Wykorzystana jest dokładnie postać z kadru v033: wycięta maską z oryginalnej
ilustracji, z zachowaniem jej skali i kadrowania. Zrekonstruowano tło pod jej
sylwetką, a płótno rozszerzono do 200 pikseli. W czasie przebitki tło przesuwa
się o 18 pikseli w lewo, a dziewczyna o 38 pikseli w prawo. Niezależne drobne
przesunięcia pasm włosów tworzą powiew wiatru. Ujęcie trwa od ticku 3553 do
4113; następne cięcia pozostały na dotychczasowych pozycjach.

18 klatek powstaje podczas budowania przez złożenie wyciętej postaci i tła;
Atari odtwarza gotowe klatki co 32 ticki i kopiuje je do nieaktywnego bufora.
Do pięciu nowych banków trafia łącznie 20 miejsc na klatki (dwa ostatnie to
powtórzenia), kod renderujący i tablice. Razem demo używa 38 banków. Efekt
nie jest liczony jako dwie nakładane warstwy w każdej klatce na 6502.

Źródło postaci: `assets/art/source/act1_girl_side_walking_v033.png`.
Uzupełnione tło `assets/art/source/act1_school_background_v034.png` powstało
przez usunięcie dziewczyny z tego obrazu i odtworzenie zasłoniętych fragmentów
w imagegen. Maska i przygotowanie pikseli: `tools/prepare_school_pan.py`
(systemowy Python z Pillow). Generator klatek: `tools/school_parallax.py`.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 49 testów PASS,
w tym wszystkie 18 klatek i granice scen. Atari800 PAL 1088XE: zrzuty aktywnej
listy ekranu wszystkich 18 klatek zgodne z grafiką źródłową.

[ODCZYT] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v035.xex --seconds 12`: 7 637 040 identycznych bajtów
stereo POKEY (~2127,4 s emulacji, cały utwór). Nie wykonano osobnego odsłuchu
na fizycznym Atari. Podgląd GIF jest generowany z wykonania kodu 6502, kolory
PAL przybliżone.

SHA256 v035: `3bbea99f540375d923b531b6c8f0ac3a9b072c66e14647018826be17ad8a9726`.
Zachowano v033 i pośredni v034.
