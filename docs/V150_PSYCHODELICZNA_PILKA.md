# V150 — psychodeliczna piłka rotatora i tunelu

## Obraz i animacja

Piłka ma 16 różnych faz obrotu zamiast ośmiu pulsujących masek.
Sylwetka pozostaje pełną kulą o stałym rozmiarze. Obrót odbywa się wewnątrz:
projekcja sferyczna z pochyloną osią przesuwa zakrzywione szwy i kolorowe
panele. Jasna krawędź i refleks w górnej części wzmacniają odczyt kuli.
Szwy zmieniają kolor panelu, nie wycinają przezroczystych pikseli.

Cztery players mają odrębne nasycone barwy, cyklicznie przesuwane po kole
kolorów co 16 ticków playera. Jasności korpusu/paneli to 8/10/14/12;
rozróżniają krawędź i powierzchnię. Jasne satelity missiles zachowują
poprzednie dwie elipsy i pozycje. Nowa piłka jest wspólna dla rotatora
bananów i tunelu, także ich wcześniejszego zakresu w akcie 2.
Nie zmieniono muzyki, trajektorii, granic aktów ani ticków ujęć.

## Pamięć i termin aktualizacji

[ODCZYT] Całość mieści się w dotychczasowym banku loadera 2:

- `$7800–$7BFF`: kod, palety, współrzędne, obrysy i wyrównanie.
- `$7C00–$7DFF`: 16×32 B paneli lewej połowy.
- `$7E00–$7FFF`: 16×32 B paneli prawej połowy.

Przygotowywane są cztery płaszczyzny PMG, ale przechowywane tylko dwie.
Pozostałe są ich dopełnieniem wewnątrz stałej maski sylwetki (2×32 B).
Druga połowa obrotu przełącza stronę źródła w tym samym banku.
Połączono powielone tabele satelitów tworzących pary missiles.

Helper ma 2048 B zamiast 2011 B, czyli **+37 B**, bez nowego banku.
Łączny odzysk netto względem v141 wynosi **23 646 B = 23,09 KiB**.
Nadal 64 banki i 2515 B głównego kodu (`$1400–$1DD2`).

Zachowane wejście w oknie VCOUNT 124–127, brak wyłączania piłki
w oczekiwaniu i odtworzenie PORTB. Czyszczenie obejmuje dokładnie 640 B
PMG, w pięciu odcinkach po 128 B; usunięto powtórne zapisy wspólnego zakresu.
Dzięki temu większa liczba faz i rekonstrukcja paneli nie wymagają długiego
przepisywania pełnych czterech masek z dodatkowego banku.

[ODCZYT] py65, powtórny callback 33024 → 33028: v149 8109 cykli,
v150 8211 cykli (+102). To koszt CPU w tym konkretnym przypadku,
bez DMA ANTIC i bez modelowania realnego FPS.

## Walidacja

Testy sprawdzają 16 różnych masek, stały obrys, pełne odtworzenie wszystkich
czterech płaszczyzn z kodu 6502, kolory, ruch oraz zakrycie centralnego otworu
tunelu w całym cyklu. Zachowano regresje późnego VCOUNT ze sztucznym
zatrzymaniem CPU, przekazywania buforów i wstrzykiwania NMI muzyki.

[ODCZYT] `make check`: **115 testów, 112 zaliczonych, 3 pominięte**
(brak archiwalnego v126), 91,038 s.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **15 780 312
identycznych bajtów** względem v035; porównanie obejmuje cały utwór.
Bez odsłuchu i weryfikacji na fizycznym Atari. Testy CPU i zgodność POKEY
nie ustalają rzeczywistego FPS ani stabilności rastra z DMA na sprzęcie.

## Wydanie i podglądy

- `build/visual-prototype-v150.xex` i odpowiadający JSON.
- `build/v150-ball-rotator.gif` — ruch piłki na rotatorze bananów.
- `build/v150-ball-tunnel.gif` — animacja i kolory w tunelu.
- `build/v150-psychedelic-ball.png` — oba efekty obok siebie.
- `build/v150-ball-sheet.png` — 16 masek, stała paleta do porównania geometrii.

Podglądy powstają po wykonaniu callbacku 6502; kolory i tempo są
przybliżone. Nie są nagraniem emulatora ani pomiarem płynności.

SHA-256 XEX: `0ec48a19fce0c8ec89909b30b7b18ec20e9046c37f86efeac56ac60f088b64ae`.
Numerowane pliki XEX/JSON są identyczne z roboczymi `visual-prototype-dev`.
