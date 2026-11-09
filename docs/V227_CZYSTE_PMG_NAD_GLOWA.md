# V227 — bez rozdwojonych gwiazdek i nut nad głową

Błąd nie był zamierzony. Kontroler finału odczytywał `$D407` (PMBASE),
rejestr ANTIC tylko do zapisu. Na sprzęcie nie otrzymywał w ten sposób
numeru widocznego bufora, więc mógł rysować ponownie do aktywnego PMG.
Dodatkowo renderer tekstu przesuwał już opublikowane maski o 16 bajtów
(32 linie), co pozwalało DMA zobaczyć niekompletną wersję obiektu.

Wybór następnego bufora pochodzi teraz ze stanu RAM `$83E8`. Współrzędne Y
są od razu generowane z przesunięciem +16 bajtów; usunięto cały wtórny
przepisujący przebieg z `outro_text`. Wszystkie cztery maski są wyczyszczone
i narysowane w niewidocznym buforze przed publikacją PMBASE. Po publikacji
nie ma już zapisów do bitmap PMG. Na pierwszym wejściu PMG jest wyłączone
na czas przygotowania, aby nie wyświetlać odziedziczonych obiektów.

Cztery obiekty na orbicie i naprzemienne gwiazdki/nutki pozostają. Zachowano
wygląd masek, orbitę, kolory, położenie głowy, terminal i paletę Trevora.
Kontroler finału: 814 B, `$5CD0–$5FFD`; nie dodano żadnego banku.

## Dowody

- Test z pamięcią zwracającą `$FF` przy odczycie PMBASE odtwarza błąd v225:
  wykrywa zapisy do PMG po jego publikacji. V227 przechodzi ten sam test.
- Test obejmuje 48 kolejnych faz, gwiazdki i nutki: każdy z czterech graczy
  zawiera dokładnie jedną oczekiwaną maskę, bez pikseli poza nią, a stary
  widoczny bufor nie jest zapisywany podczas kolejnych klatek.
- 14 testów publikacji, finału, NMI, restartów i regresji — OK, 6,1 s.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 144 952 identyczne bajty
  względem v035; cały utwór. Brak próby na fizycznym Atari.
- Regresja porównuje zawartość wyłącznie włączonych graczy/pocisków:
  wyłączone PMG i nieaktywny bufor są przestrzenią roboczą i nie określają
  widocznego obrazu.

Pełny przebieg 162 testów wykazał jedną starą asercję porównującą także
wyłączone pociski po przewinięciu do sceny 3472; pozostałe testy przeszły.
Po ograniczeniu tej asercji do faktycznie włączonego PMG ponowny zestaw
14 testów, obejmujący tę regresję i test write-only PMBASE, przeszedł.
