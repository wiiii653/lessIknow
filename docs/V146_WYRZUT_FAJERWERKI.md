# V146 — czytelny wyrzut i fajerwerki

[ODCZYT] Na prośbę użytkownika usunięto kratkę, prostokąt boiska i jego
linie z całego trzeciego ujęcia tańca. Dziewczyna i dwie podstawy są teraz
na spokojnym czarnym tle. Perspektywa z góry, powiększanie bohaterki oraz
oddalanie pozostałych dziewczyn pozostają w dotychczasowych fazach.

[ODCZYT] W przygotowaniu do wyrzutu nie ma żadnych animowanych szarf.
W pierwszym etapie lotu, tick 20662, zaczynają się fajerwerki: rakiety,
rozkwit promienistych kształtów i rozrzucone punkty na players, z małymi
iskrami na missiles. To osiem faz po 16 ticków, cztery rozkwity przesunięte
w fazie. Efekt trwa do końca tego ujęcia, w 20942.

[ODCZYT] Players są dwukrotnie szerokie (16 pikseli logicznych), zamiast
czterokrotnie szerokich pętli szarf. Lewa para mieści się w kolumnach 10–25,
prawa w 134–149 obrazu 160-pikselowego. Środki rozkwitów znajdują się
w (18,42), (18,132), (142,54), (142,147) w pikselach logicznych/liniach rastra.
Duże maski nie przykrywają centralnego pasa twarzy. Dotychczasowe cykle
barw po muzycznych DLI obejmują także nowe fajerwerki.

[ODCZYT] Wcześniejszy taniec z boku, grupa i solówka zachowują poprzednie
szarfy oraz iskry. Także wielokrotne skoki między tymi ujęciami przywracają
odpowiednią szerokość i maski PMG. W całej scenie zachowano przygotowanie
nieaktywnego PMG/bitmapy i ograniczone okno publikacji VCOUNT 124–127.
Nie przesunięto etapów wyrzutu, ujęć, aktów ani ticków muzyki.

## Pamięć

[ODCZYT] Osiem kształtów fajerwerków zajmuje 128 B. Razem z nowym wyborem
efektu i kopiowaniem koszt wzrasta o 349 B: kontroler w banku loadera 49
ma teraz 2203 B i zajmuje `$5400–$5C9A`. Bitmapy i istniejące strumienie
szarf zachowują rozmiary. Nadal 36 kompozycji i 64 banki.

[ODCZYT] Aby zachować rozłączność kodu, kontroler końcowego chłopca
przeniesiono z `$5B80` do `$5CC0–$5FEB` (nadal 812 B). Między kontrolerami
pozostaje 37 B, a przed kodem Trevora od `$6000` tylko 20 B. Instalatory
odrzucają kolizje. Główny kod nadal ma 2494 B, a bitmapa finału i muzyka
zachowują dotychczasowe miejsca.

[ODCZYT] Aktualny odzysk netto względem v141: **24 954 B = 24,37 KiB**.
Nie oznacza to zwolnienia całych banków ani obniżenia wymagań sprzętowych.

## Podglądy

- `build/v146-launch-fireworks.gif`: całe trzecie ujęcie, callback co 12 ticków.
- `build/v146-flight-fireworks.gif`: krótki podgląd samego finałowego lotu.
- `build/v146-launch-storyboard.png`: przygotowanie, początek lotu i zbliżenie.
- `build/visual-prototype-v146.xex` i JSON: numerowane wydanie.

Kształty i efekty powstają w `tools/ribbon_dance.py`. Nie generowano nowych
źródłowych ilustracji. GIF ma przybliżoną paletę i tempo; wykonanie py65
nie modeluje DMA ANTIC ani rzeczywistych terminów prezentacji.

## Walidacja

[ODCZYT] `make check`: **113 testów, 110 zaliczonych, 3 pominięte**
(brak archiwalnego v126), 89,829 s. Nowe testy sprawdzają usunięcie linii,
zerowe maski szarf w przygotowaniu, osiem różnych faz rozkwitu, kolumny
efektów poza twarzą, rozmiary players, iskry missiles, powrót do wcześniejszych
szarf i zapisy wyłącznie do nieaktywnego PMG. Dotychczasowy test NMI
obejmuje teraz też początek fajerwerków; test ruchomego VCOUNT sprawdza
zarówno szarfy, jak i nowe rozkwity.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **14 751 288
identycznych bajtów** względem v035 przez cały utwór. Końcowy chłopiec,
fade i powroty między scenami również przechodzą testy po relokacji kodu.
Bez odsłuchu i próby na fizycznym Atari; zgodność rejestrów nie jest
pomiarem rzeczywistej płynności obrazu.

[ODCZYT] XEX: 1 109 034 B, bez zmiany rozmiaru względem v145.
SHA-256: `7b0184401c7dfcc1a85b51d199671ce2e9731b71f9297b8086e3c168783624d9`.
Numerowane wydanie i sprawdzony build roboczy są identyczne bajt w bajt.
