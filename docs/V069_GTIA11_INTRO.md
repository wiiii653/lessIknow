# V069 — wielokolorowe litery na początku

Dwie plansze otwierające używają ANTIC F i GTIA 11: obraz 80×192 pikseli
z maksymalnie 16 odcieniami przy wspólnej jasności. Litery otrzymały tęczowe
wypełnienie, przesunięty kolorowy cień i pulsowanie jasności. Pixel o wartości
zero pozostaje czarny. Treść i granice plansz są takie jak w v064.

Pomocnik `$FEF0–$FF92` przełącza wyłącznie nieaktywną display listę pomiędzy
trybami F i E, zachowując bity muzycznych DLI. Pracuje podczas zwykłych
plansz; przed scenami bankowanymi obie listy wracają do trybu E. Odtwarzacz
muzyki nie został zmieniony.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 63 testy OK,
w tym kolory GTIA 11, przełączanie trybów i DLI na liniach 0, 78, 156 i 234.
Atari800 7.2.1, PAL, 1088XE, Altirra OS, stereo: 14 958 klatek do ticku
59832 miało liczniki muzyki i cztery próbkowane rejestry POKEY zgodne z v064.
Od ticku 3200 skróty ekranu były zgodne na wszystkich porównanych klatkach;
na przejściu z tytułu do szkoły różniły się dwie klatki. Pełne porównanie
stereo POKEY z oryginalnym v035 dało 7 489 080 identycznych bajtów po
jednokrotnym wyrównaniu początku. To nie zastępuje odsłuchu na docelowym Atari.

Podgląd jest zrzutem z Atari800 z przybliżoną paletą emulatora. Wydanie:
`releases/visual-prototype-v069.xex`; SHA-256
`a7e7599a2ab63df7d88b492bc284582abdbbaa66fb59fdd01b814eae1704916c`.
