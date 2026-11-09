# V241 — szybkie banany bez rozpakowywania

## Przyczyna i wynik

V239/v240 rozpakowywały obie animacje RLE na każdej zmienianej klatce.
Koszt kolejnych klatek rósł z około 47 tys. do 68–79 tys. cykli CPU.
Sam limit 90000 cykli nie gwarantował zachowania tempa z ANTIC DMA.

V241 całkowicie usuwa runtime RLE. Bitmapy są kopiowane bezpośrednio
z banków taką samą procedurą jak tunele. Porównanie przy tym samym
wywoływaniu callbacku co 16 ticków:

| Motyw | Pierwsze dwie klatki | Maksimum kolejnych 30 |
|---|---:|---:|
| Kiść | 58644 / 58650 | 47300 |
| Obrany | 58682 / 58688 | 47375 |
| Tunel | 58660 / 58671 | 47233 |

To pomiary instrukcji CPU bez ANTIC DMA, nie pomiar FPS. Eliminują
jednak dodatkowy koszt, który odróżniał banany od tuneli. Test wszystkich
64 logicznych klatek obu wariantów wymaga teraz mniej niż 62000 cykli,
również przy zimnym wejściu; osobny test pilnuje parytetu z tunelem.

## Układ grafiki i ciągłość

Żeby oba warianty mieściły się bez kompresji, zmieniono kompozycję tła:
źródłowy kafel 128×128 zawiera dwie przeciwległe kopie tego samego owocu,
z symetrią środkową. Rysunek kiści i pojedynczego obranego banana zachowano,
ale ich rozmieszczenie jest rzadsze i parami. Zoom powtarza się co półobrót.

Układ po obrocie 180° jest identyczny, dlatego potrzeba **16 unikalnych
bitmap na motyw**, odtwarzanych jako **32 próbki kątowe pełnego obrotu**.
Nie są to 32 unikalne bitmapy. Przejścia 15→16 i 31→0 odpowiadają zwykłemu
krokowi 11,25°, bez resetu asymetrycznej kiści z poprzedniego błędu.
Testy sprawdzają symetrię kafla, niezależne orientacje czterech ćwiartek
i ciągłość seamów. Naprzemienność wejść oraz PMG piłki pozostają.

## Pamięć i kod

Osiem dotychczasowych banków: cztery dla kiści i cztery dla obranego.
Każdy mieści cztery surowe bitmapy (15360 B) i 981 B helpera. Łącznie
pozostaje **344 B wolnych luk**, a nie 9910 B z v239. To świadomy koszt
przywrócenia szybkości; nie użyto dodatkowych banków ani luk innych scen.

Helper: $7C00–$7FD4. Ma własny cache $0DDE i klucz wariantu $0DDD,
z unieważnianiem wspólnego klucza przy przejściu do innych rendererów.
Nie ma dekodera, strumieni RLE ani używania strony zerowej.

Selektor wariantu $EBF0–$EC11 (34 B) i banku $ED4D–$ED8F (67 B)
wykorzystują wolne końcówki istniejących rezerw intro. Asserty chronią
granice typewritera i directora. Pula wierszy nadal od $EDA0. Main 2518 B.

## Weryfikacja

21 testów ukierunkowanych zaliczonych przed pełną regresją. Obejmują
obrazy, własność nieaktywnego bufora, przejścia, palety, PMG oraz NMI.
Osiem banków tuneli identycznych bajtowo z v240. Terminal i ticki scen
pozostają v240.

[ODCZYT] Atari800 PAL/1088XE, stereo POKEY: **11 610 936 identycznych
bajtów** względem v035, cały utwór. Bez próby na fizycznym Atari.

Podglądy CPU/PMG: `build/banana-v241-variants.png`,
`build/banana-v241-bunch.gif`, `build/banana-v241-peeled.gif`.

[ODCZYT] Pełna regresja: **184/184 testy**, bez pominięć, 123,5 s.
Build roboczy i v241 identyczne; SHA-256:
`c17b9eb0d58fc9e35e84b159fa844a46d6c71f054afcd1fb10c54ff14a1de917`.
