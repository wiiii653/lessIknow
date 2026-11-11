# V249 — dwie piłki z satelitami przy ciosach

Każdy z 13 zachowanych ciosów zaczyna się przylotem pełnej piłki rotatora
z dwiema parami orbitujących gwiazd. Po dotychczasowym BUM/BAM odlatuje
mniejsza piłka wsadu z czterema niezależnymi orbitami. Wykorzystano dokładne
maski, fazy, kształty satelitów i palety oryginalnych efektów. Trzynaście
różnych wektorów przylotu i trzynaście innych wektorów odlotu obejmuje boki,
górę i dół; tor zmierza do istniejącej pięści. Czas ciosów, bitmapy Trevora,
długość BUM/BAM i granice scen v248 pozostają.

## Pamięć i walidacja

Nowy renderer 1853 B mieści się w loader banku 19 `$6800–$6F3C`, po danych
obrazów szkolnego spaceru i przed jego kodem `$7000`. W tym samym banku maski
dużej piłki zajmują `$7300–$7AFF`, małej `$7B00–$7CFF`, tablice orbit
`$7D00–$7E7F`, a przemieszczeń `$7F00–$7FE6`. Instalator sprawdza zerowy
obszar przed użyciem. Helper lotu v247 usunięto z banku 2; pozostałe
użytkowanie tego banku według v248 bez zmian. Nadal 64 banki i 2560 B main.

Maski i satelity są przygotowywane w nieaktywnym PMG, a rejestry publikowane
we wczesnym oknie blankingu. Testy sprawdzają faktyczne maski obu piłek,
oryginalne orbity i kolory, unikalne wektory, nieaktywny bufor, ruchomy raster,
muzyczne NMI i brak odczytu rejestrów HPOS. Granice v248 pozostają.

[ODCZYT] Atari800 PAL/1088XE, stereo POKEY: 15 917 976 bajtów identycznych
z v035 przez cały utwór. Bez odsłuchu, pomiaru FPS z DMA i testu na fizycznym Atari.
Podgląd `build/v249-flight-preview.png` pokazuje wybrane klatki wygenerowane
po callbackach 6502, z przybliżoną paletą PAL; nie jest nagraniem emulatora.

[ODCZYT] Pełne `make check`: 190/190 testów, 145,141 s.
