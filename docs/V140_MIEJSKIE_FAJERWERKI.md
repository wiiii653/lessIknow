# V140 — miejskie fajerwerki i kolejność wejścia tytułu

[ODCZYT] Końcowy układ drugiej planszy pozostał bez zmian: THE LESS u góry,
I KNOW pośrodku, THE BETTER na dole. Zgodnie z doprecyzowaniem użytkownika
zmieniono wyłącznie kolejność wejść: I KNOW, THE BETTER, THE LESS. Dotychczasowe
chwile wyzwalania masek i przejścia między planszami pozostają bez zmian.

[ODCZYT] Obie plansze mają sylwetkę miasta u dołu plazmy oraz fajerwerki:
rakietę, rozkwit, rozszerzające się ramiona i opadające iskry. Cztery players
i cztery missiles używają normalnych kolorów nad GTIA 11 (`PRIOR=$C1`,
bez piątego gracza). Maski PMG uwzględniają sumę obu kompletnych plansz
liter i ich cieni. Dzięki temu nie zasłaniają również tekstu przenikającego
między kartami. Jasność PMG podąża za fade’em planszy.

## Pamięć i raster

[ODCZYT] Brak nowych banków i nowych pełnych bitmap. Zmieniono istniejące
16 klatek tła, dodając niską sylwetkę miasta. Fajerwerki zajmują dawne puste
końcówki banków plazmy 40–41 (indeksy loadera): kontroler `$6C00`, osobne
wejście zatwierdzania `$7000`, 16 × 5 × 32 B masek `$7400–$7DFF`,
pięć kotwic pionowych `$7E00–$7E04`. Kontroler ma 1324 B wraz z paddingiem
do stałego wejścia; z danymi i kotwicami to 3889 B na bank. Kod niebankowany
urósł o 70 B względem v138. Nadal przydzielone są te same 64 banki.

[ODCZYT] Obliczenia i zapis PMG idą do nieaktywnego z istniejących buforów
`$0980–$0BFF` / `$8980–$8BFF`, przed kompozycją plazmy. Przy prezentacji
pozostają przełączenie PMBASE i rejestrów w ograniczonym oknie wygaszania.
Nie dodano DLI ani ticków muzyki. Kolory samych liter nadal zmieniają się
według istniejącej fazy uderzeń.

[ODCZYT] Pomiar instrukcji na pierwszej implementacji: przygotowanie PMG
dodało około 9,6 tys. cykli. Z tego powodu rozdzielono przygotowanie od
publikacji, aby długie kopiowanie nie odbywało się po oczekiwaniu na wygaszanie.
Regresyjny limit CPU dla próbek intro zmieniono z 140 tys. do 150 tys. cykli;
nie jest to termin jednej ramki PAL. Sama wcześniejsza kompozycja plazmy
przekraczała już pojedynczą ramkę; nie deklarujemy 50 nowych klatek/s.

## Sprawdzenie

Testy obejmują kolejność i zachowanie pozycji słów, wszystkie fazy masek,
ochronę liter/cieni, rzeczywisty stan PMG podczas przenikania plansz,
brak zapisów do aktywnego PMG, późne wejścia w raster, restart oraz powrót
do ANTIC E w scenie szkoły. Podgląd `build/v140-city-fireworks.gif` pochodzi
z 187 kolejnych wykonań callbacku co 16 ticków; kolory i tempo są przybliżone,
a model nie obejmuje ANTIC DMA i rzeczywistych terminów sprzętowych.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 714 136
identycznych bajtów względem v035, cały utwór. Nie jest to odsłuch na sprzęcie.

Źródła: `tools/title_plasma.py`, `tools/title_fireworks.py`.
Wydanie: `build/visual-prototype-v140.xex`.

[ODCZYT] Końcowy `make check`: 99 testów, 96 zaliczonych, 3 pominięte
z powodu braku archiwalnego v126; 85,614 s. Roboczy XEX identyczny z v140.
SHA-256: `089c298b9a098d686fe069b69e0cca397d456bb5a4ec775453d3d63a4f9a976e`.
