# V236 — pełny, ciągły obrót bananów

## Przyczyny

1. `mosaic.pixels()` wyliczało fazę 0–2π, ale kąt obrotu dzieliło przez 4.
   Wszystkie 32 bitmapy obejmowały więc tylko 90°. Zawinięcie 31 → 0
   przeskakiwało z 87,1875° do 0°, zamiast kontynuować ruch. Asymetryczny
   kafel kiści nie ma symetrii ćwierćobrotowej, więc skok był widoczny.
2. Dispatcher aktu 5 maskował fazę przez 15, zapętlając osobno 0–15,
   a po ticku 34404 doklejał bit 16 i zapętlał 16–31. Oznaczało to reset
   co 16 klatek oraz dodatkowy skok na granicy taktu 92. Samo poprawienie
   kąta w grafikach nie usunęłoby tych resetów.

## Poprawka

Kąt jest teraz pełną fazą, bez dzielenia przez 4. Istniejące 32 klatki
obejmują 360° z krokiem 11,25°; zawinięcie 31 → 0 jest takim samym
krokiem kątowym jak pozostałe. Zoom zachowuje dotychczasową sinusoidę.

Akt 5 bierze wszystkie pięć bitów fazy (`AND $1F`) i nie ma rozdzielania
animacji w takcie 92. W 34403 i 34404 wyświetla tę samą fazę 6, zamiast
skoku 6 → 22. Kolejna faza 7 pojawia się normalnie w 34416.

Nie zmieniono granic scen, miejsc rotatora ani montażu tuneli v231.
Kafel kiści, złoto/żółta paleta, brak ditheringu i grafika piłki pozostają.
Osiem banków z obiema teksturami tunelu jest identycznych z v235.
Bankowane helpery bananów również pozostają identyczne; zmieniły się
tylko ich bitmapy i główny wybór fazy w akcie 5.

## Pamięć

Nadal 32 klatki bananów i ten sam przydział banków. Nie dodano danych
PMG ani tabel. Usunięcie logiki półcykli skraca główny kod o **30 B**:
teraz 2521 B, czyli 39 B zapasu przed $1E00.

## Weryfikacja

[ODCZYT] 44 testy ukierunkowane zaliczone. Nowe regresje sprawdzają
orientacje 0/90/180/270°, ciągłe odwiedzenie wszystkich 32 faz w akcie 5,
brak resetu w połowie obrotu i w ticku 34404 oraz naturalne zawinięcie
ostatniej klatki. Test porównania z v198 zachowuje kontrolę PMG i palety
bananów tam, gdzie stary i nowy zegar wybierają tę samą fazę.

[ODCZYT] Osiem banków tunelu i helpery ośmiu banków bananów porównano
bezpośrednio z v235 — identyczne bajtowo.

[ODCZYT] Atari800 PAL/1088XE, stereo POKEY: **11 186 424 bajty identyczne
z v035**, cały utwór. Bez próby na fizycznym Atari.

[ODCZYT] Pełny przebieg zaliczył 174 dotychczasowe testy (117,8 s).
Nowy moduł miał błąd kolejności importów przy discovery bez PYTHONPATH;
po poprawieniu importu `test_sequence` przed `mosaic` osobne discovery
zalicza 3/3 nowe regresje (2,6 s). Łącznie wszystkie 177 przypadków
zweryfikowane. XEX nie wymagał po tym zmian. Build roboczy jest identyczny
z v236; SHA-256:
`63bce85afb9d3b1e792c29fb308e969b7a5e36b9f59e1bbee37addf0400ce764`.

Podglądy CPU/PMG: `build/bananas-v236.gif` (dwa pełne obroty, także
przejście 31 → 0) i `build/bananas-v236-cardinals.png` (cztery orientacje).
