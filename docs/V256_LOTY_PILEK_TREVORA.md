# V256 — loty piłek Trevora

[ODCZYT] Naprawiono dwa widoczne problemy w przylocie i odlocie piłek:
tory nie dochodzą już do ogranicznika pionowego i nie przesuwają się przez
kilka kroków wzdłuż jego krawędzi. Na początku przylotu i końcu odlotu
jasność piłek i ich satelitów stopniowo wygasa, zamiast pojawiać się lub
znikać z pełną jasnością na obrazie. Dla wszystkich 13 ciosów zachowano
odrębne kierunki w każdej fazie; kierunki przylotów i odlotów mogą się
powtarzać między fazami. Geometria piłek i satelitów, kotwice, pozycje
ciosów, BUM/BAM i ich ticki pozostają bez zmian.

[ODCZYT] Zmiana ogranicza się do loader banku 19. Helper ma 1931 B
(`$6800–$6F8A`), pozostaje 117 B przed `$7000`. Testy obejmują wszystkie
ciosy, brak osiągania ograniczników, jasność na granicach, nieaktywny bufor,
blanking i muzyczne NMI w obu lotach. Renderowany podgląd py65 nie modeluje
ANTIC DMA; nie wykonano wizualnego odsłuchu/oglądu ani próby na sprzęcie.

[ODCZYT] Podgląd wybranych klatek callbacku 6502 z przybliżoną paletą:
`build/v256-trevor-flight-preview.png` (nie jest przechwyceniem emulatora).
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 322 616 bajtów
identycznych z v035; porównanie obejmuje cały utwór.

[ODCZYT] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 199/199
testów, bez pominięć; 152,424 s.
