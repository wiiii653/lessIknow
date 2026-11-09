# The Less I Know The Better - Atari XE 1MB Demo Timeline (v2)

Wersja poprawiona po analizie `less-i-know-release-v035-preview.mp3` i playera `less-i-know-hook-v024.xex`.

## Założenia

- PAL (VBI ok. 49,86 Hz, nie 50,0 Hz)
- 128 BPM, 5:00 = 300 s, 160 taktów, takt = 1,875 s
- Player: 4 aktualizacje POKEY na klatkę PAL, ok. 199,44 Hz
- 373,95555 aktualizacji playera na takt; granica taktu `n` to pierwszy cały tick nie mniejszy niż `n × 373,95555`
- Takt ma ok. 93,5 klatki PAL (poprzednio 93,75 przy założeniu 50 Hz, co dawało dryf ok. 0,8 s na całym utworze)
- Siatka rytmiczna mp3 jest stała (128 BPM bez dryfu), takt n zaczyna się w n × 1,875 s

Korekta grafiki v153: rzut, kozłowanie i wsad korzystają ze wspólnej
pełnej neonowej piłki z ośmioma fazami paneli, szwami i refleksem.
Trajektorie, pozycje dłoni oraz wszystkie zatwierdzone ticki pozostają bez zmian.

## Synchronizacja

- Zegarem głównym jest licznik ticków playera (24 bity, `$24A7-$24A9` w v024; adres zweryfikować w kodzie v035). Zdarzenia timeline'u wyzwalaj po tickach, nie po klatkach VBI.
- Z odczytu kodu v024 wynika, że licznik rośnie tylko w ścieżce odtwarzania, więc pauza powinna go zatrzymać, a wideo zatrzymałoby się razem z muzyką. To wniosek z kodu, nie test: do sprawdzenia w emulatorze (zadanie V4 w `TLIKTB_Technical_Constraints.md`).
- Przeliczenie granic: `tick(n) = ceil(n × 373,95555)`. Zaokrąglamy po wyznaczeniu absolutnej pozycji, a nie osobno długość każdego taktu.

## ACT 1 - SCHOOL DAYS
Takty: 0-24 | Ticki: 0-8975

Zmiana miejsca zatwierdzona w v151: dawne ujęcia przed szkołą (2992–5984)
są teraz przed fikcyjną ATARI ARENA inspirowaną ERGO ARENĄ. Zachowane
ruchy postaci i czas ujęć; duże Fuji zastępuje NORTH na plecach dziewczyny.


Korekta intro v149: zwarta sylwetka Żurawia 36×29 pikseli źródłowych;
fajerwerki wznoszą się, rozkwitają i opadają przed plazmą, napisami oraz
budynkiem. Kolejność wejścia napisów, ich układ i ticki 0–2992 bez zmian.

Korekta intro v164: cztery przesunięte w fazie rakiety startują z dołu
aktywnego kadru i lecą ku górnym punktom eksplozji. Lot trwa 64 ticki;
potem rozbłysk, promienisty rozkwit i opadające odłamki missiles.
Kolory tęczy zmieniają się także podczas wybuchu. Efekt pozostaje przed
napisami i Żurawiem, bez zmiany kolejności tekstu ani ticków obu plansz.

- 1A (takty 0-8, ticki 0-2992): logo szkoły, panorama boiska, scroll chmur
- 1B (8-16, 2992-5984): cheerleaderka pojawia się pierwszy raz, Trevor w tle
- Realizacja v170: portret chłopca na fasadzie robi oko i gwiżdże w lewo;
  pikselowe klucze wiolinowe oraz nuty tworzą krótki ślad dźwięku. Warstwa
  melodii znajduje się za przechodzącą dziewczyną. Bez zmiany ticków.
- 1C (16-24, 5984-8975): po zniknięciu dziewczyny za drzwiami cięcie do wnętrza sali; chłopcy trenują koszykówkę, dziewczyny rozciągają się przy drabinkach. Animowana piłka: rzut i odbicie. Realizacja w v010; taniec zaczyna się bez przesunięcia, przy ticku 8975.

## ACT 2 - CRUSH
Takty: 24-56 | Ticki: 8975-20942 (zmiana: było 24-48)

Granice podakt wynikają ze zmian w muzyce w taktach 32, 40 i 56. W takcie 48 nie ma wyraźnego markera.

- 2A (24-32, 8975-11967): zatwierdzone ujęcie z boku — dziewczyna cofa się tyłem, pracując szarfą; od v143 przechodzi przez kadr z lewej na prawą wraz z duszkami i pociskami. Sala przewijana w przeciwną stronę, z paralaksą podłogi. V142 zastępuje tu taniec z pomponami, zachowany w osobnym projekcie `projects/pompom-dance`. Granice bez zmian.
- 2B (32-40, 11967-14959): patterny psychodeliczne
- 2C (40-56, 14959-20942): choreografia ze wstęgami PMG, zatwierdzona zamiast dawnych zbliżeń twarzy. Trzy ujęcia: grupa (40-44), solówka (44-48), grupa i wyrzut bohaterki (48-56). Zmiana scenariusza zatwierdzona 2026-11-07: ostatnie ujęcie ma kamerę nad grupą, skierowaną w dół. Wyrzucana dziewczyna leci ku obiektywowi, rośnie w kadrze, widzimy jej twarz i pracującą szarfę; pod nią oddalają się podłoga sali i pozostałe tancerki. To zastępuje dotychczasowy boczny widok wznoszenia. Zachowane dotychczasowe ticki wejścia i końca; dawny marker 52 nie oznacza już kolejnego cięcia kamery.

Korekta wyglądu 2C (v146, 2026-11-07): w ujęciu z góry brak kratki i linii
boiska. Przygotowanie bez animowanych szarf; podczas lotu ku kamerze
(od ticka 20662) boczne fajerwerki players i iskry missiles. Bez zmiany
dotychczasowych granic ujęć i etapów wyrzutu.

Korekta ruchu 2C (v147): przygotowanie w trzecim ujęciu i sam wyrzut mają
przebiec tylko raz. Kolejne pozy tworzą ciągłą sekwencję bez powrotu
do poprzednich faz; po dojściu dziewczyny ku kamerze trzymany jest finałowy
kadr do cięcia. Bez zapętlania przygotowania.

Korekta dynamiki 2C (v148, aktualne wymaganie użytkownika): zamiast wolnego
przygotowania z v147 czas do 20475 wypełnia taniec grupy. Jedno przykucnięcie
w 20475, wybicie w planie ogólnym w 20521, cięcie do kamery z góry w 20568
i zbliżenie w 20662. W obu planach lotu smugi pędu powietrza na players
i missiles; boczne fajerwerki zachowane. Taniec może się powtarzać, sam
wyrzut tylko raz. Bez zmian granic aktów i głównych przedziałów 2C.

Detal finału 2C (v233): w zbliżeniu z góry w 20615 dziewczyna puszcza
oczko, a w 20662 robi dziubek. Z ust startuje jedno przestrzenne serce
PMG: osiem faz wzrostu, lekkiego obrotu i oddalania się po skosie ku
kamerze. Pociski zachowują smugi pędu; w tej ostatniej fazie players
przejmuje serce. Cięcie w 20942 i długość całego wyrzutu pozostają.

Korekta płynności v166: trzy późniejsze plany tańca (40–48 oraz taniec
przed wyrzutem w 48–56) dostają rzeczywiste klatki pośrednie. Stare pozy
pozostają na tickach `STEPS`; nowe wchodzą w połowie odstępu 46/47 ticków,
co daje zmiany co 23/24 ticki, bez zwalniania ruchu i wydłużania scen.
14 kompozycji korzysta z 9 nowych póz. Kotwice dłoni i szarf odpowiadają
nowym obrazom; cięcia, przygotowanie i szybki wyrzut pozostają pojedyncze.
Ujęcie z boku (24–32) bez zmian.

Korekta v173 udostępnia cztery dodatkowe klatki wyłącznie w solówce (44–48):
pojawiają się w 3/4 wybranych przejść między pozami, skracając ich drugą
połowę do 11/12 ticków. Długość ujęcia i akcenty pozostają bez zmian; nowe
grafiki zajmują ogony banków 32–35 z dekoderami LZ. W v173 dopracowano ich
układy pod konkretne fazy ruchu; routing dekodera poprawiono w v172.

## ACT 3 - BASKETBALL HERO

Takty: 56-64 | Ticki: 20942-23934 (zmiana: było 48-64)

Muzyka ma zmianę w 56 i spadek gęstości uderzeń w 60.

Zmiana montażu zatwierdzona przez użytkownika w v151: po niezmienionym
wyrzucie krótki tunel z piłką, następnie kozłowanie i krótszy wsad.
Granice aktu 56–64 i wejście Trevora w 23934 pozostają bez zmian.

- 3A0 (56-58, 20942-21690): przebitka spiralnego tunelu z neonową piłką, 3,75 s.
- 3A (58-62, 21690-23186): kozłowanie we wnętrzu ATARI ARENA, 7,5 s.
- 3B (62-64, 23186-23934): szybki wsad we wnętrzu ATARI ARENA, 3,75 s, światła stadionu. Zmiana scenariusza zatwierdzona 2026-11-07: przy wsadzie chłopiec rozbija tablicę kosza. Pęknięcie wynika z kontaktu z koszem, po nim czytelny rozpad i lecące odłamki. Całe zdarzenie mieści się w skróconym zakresie wsadu v151; fazy co 8 zamiast 16 ticków.

Korekta wsadu v165: od początku wsadu do pierwszego pęknięcia tablicy
(fazy 0–74) satelity krążą wokół piłki po czterech różnych orbitach,
w przeciwnych kierunkach; jedna orbita jest dwukrotnie szybsza. Zmiany
pozy chłopca przesuwają cały układ razem z piłką. Od fazy 75 obowiązują
wcześniejsze odłamki szkła. Granice, ticki i długość wsadu bez zmian.

## ACT 4 - TREVOR AWAKENS
Takty: 64-88 | Ticki: 23934-32909

- 4A (64-72, 23934-26925): cichy fragment (głośność spada o ok. 8 dB, szeroka stereo, więcej basu). Trevor wyłania się z tła, ciemna paleta, powolne wejście; zmiana pozy w takcie 68, tick 25429.
- 4B (72-88, 26925-32909): w takcie 72 wraca pełna energia (najsilniejsza zmiana strukturalna w utworze). Trevor na tle tunelu, zamachy i kombinacje ciosów. Naprzemienne BANG/BAM, chmurka rozchodząca się kolorowymi fragmentami players oraz rozprysk i drobne szczątki na missiles. Zachowana siatka ciosów; animacja i cykle barw synchronizowane tickiem playera. V163: po napisie przy co trzecim ciosie (3., 6., 9., …) odlatuje gotowa piłka rotatora z obiema orbitami satelitów. Cały efekt leci ku bliższej krawędzi, zgodnie ze stroną dłoni: lewa w lewo, prawa w prawo. Oryginalne 16 faz obrotu i kolory; pozostałe ciosy zachowują chmurki i odłamki. Napisy BANG/BAM i czas efektu bez zmian.

## ACT 5 - PSYCHEDELIC BREAKDOWN

Korekta v162: wycofano nowy cykl PMG v158–v160. Rotator i tunel używają
tego samego wcześniejszego renderera piłki i satelitów, który zasłania środek
tunelu. Dithering pozostaje wyłączony. Granice aktów i planowane brakujące
sceny bez zmian.

Korekta wizualna v150: rotator i tunel używają 16-fazowej piłki z obrotem
paneli/szwów, refleksami i szybkim cyklem czterech neonowych barw. Stała
sylwetka zasłania środek tunelu. Tory ruchu i ticki scen pozostają bez zmian.

Takty: 88-120 | Ticki: 32909-44875

Podział zachowuje wejście rotatora w takcie 88 i muzyczne zmiany tekstury
w takcie 108 oraz następnych ujęć w 112 i 116. Zmiana v193 wydłuża pełny
rotator do ośmiu taktów. V236 usuwa osobne zapętlanie połówek: wszystkie
32 klatki tworzą ciągłe 360°, bez resetu fazy w takcie 92.

- 5A (88-96, 32909-35900): pełny bananowy rotator (15 s).
  Od v239 kolejne widoczne wejścia bananów w całym demie przeplatają kiść
  z pojedynczym bananem obranym do połowy. Każdy motyw ma 32 klatki i pełne
  360°; zmiana następuje dopiero przy kolejnym wejściu motywu. Cały ten
  odcinek 5A jest trzecim wejściem i zachowuje kiść, bez zmiany w takcie 92.
  V241 przywraca bezpośrednie kopiowanie bitmap: motywy ułożone są parami
  z symetrią środkową, a zoom powtarza się po półobrocie. Pozwala to użyć
  16 unikalnych bitmap dla 32 kroków kątowych bez skoku i bez runtime RLE.
- 5B (96-112, 35900-41884): tunel spiralny. W takcie 108 (tick 40388)
  przechodzi w organiczne pasma. Klatki i banki bez zmian.
- 5C (112-116, 41884-43379): Trevor Mosaic (głośność spada o ok. 2 dB w 112-119).
  Bieżąca faza tunelu jest trzymana do ticku 41984; dopiero wtedy globalny
  cykl przechodzi na pełną fazę spiralną. Eliminuje to półsekundowy błysk
  bananów po granicy taktu 112.
- 5D (116-120, 43379-44875): Eyes Sequence
- GTIA9: do decyzji, w którym bloku. W asset list brak dla niego assetów.

## ACT 6 - LOVE TRIANGLE
Takty: 120-128 | Ticki: 44875-47867 (zmiana: było 120-136)

- 6A (120-124, 44875-46371): komiksowe kadry (panel_left, panel_center, panel_right, pozy postaci)
- 6B (124-128, 46371-47867): Trevor vs koszykarz

## ACT 7 - TREVOR WINS
Takty: 128–około 138,65 | Ticki: 47867–51850 (v240: wcześniejsze outro na polecenie użytkownika)

Najgłośniejsza część utworu zaczyna się w takcie 128 (ok. 3 dB głośniej), szczyt jest w 136-143.

- 7A (128-136, 47867-50858): neon glow, narastanie
- 7B (od 136, 50858–51850): planowana kulminacja; bieżący rotator/tunel
  ustępuje terminalowi w 51850, około 10 s wcześniej niż przed v240.

## ACT 8 - OUTRO
Takty: około 138,65–160 | Ticki: 51850–59833 (v240: wejście 2000 ticków wcześniej)

W takcie 144 muzyka się zmienia. Wyciszenie dopiero w 158-159.

- 8A (51850–54850): trzy plansze credits na tle leżącego chłopca;
  wejścia 51850/52850/53850. Szybkie wpisanie całej planszy, potem pauza.
- 8B (54850–59085): pięć plansz greetz, osobno dla każdego akapitu;
  wejścia 54850/55697/56544/57391/58238. Prompt `>_`, migający podkreślnik
  podczas pisania i pauzy. Siedem wierszy: status + sześć tekstu.
  Chłopiec i orbita pozostają w jednym stałym niższym położeniu.
- 8C (158-160, 59085-59833): finałowy kadr po zwycięstwie Trevora — chłopiec leży pobity na podłodze sali, a wokół jego głowy krążą komiksowe gwiazdki. Zmiana scenariusza zatwierdzona 2026-11-07. Domknięcie losu tej samej postaci, która wcześniej rozbiła tablicę przy wsadzie. Końcowy flash/przejście i fade do czerni pozostają w obecnym zakresie; credits i greetz z 8A/8B zachowane.

## Tabela zdarzeń dla silnika

| Takt | Tick | Zdarzenie |
|---|---|---|
| 0 | 0 | start, Act 1 |
| 8 | 2992 | 1B |
| 16 | 5984 | 1C |
| 24 | 8975 | Act 2 / 2A |
| 32 | 11967 | 2B |
| 40 | 14959 | 2C |
| 56 | 20942 | Act 3 / 3A |
| 60 | 22438 | 3B |
| 64 | 23934 | Act 4 / 4A |
| 72 | 26925 | 4B (uderzenie) |
| 88 | 32909 | Act 5 / 5A |
| 92 | 34404 | 5A — środek odcinka, bez resetu fazy rotatora |
| 96 | 35900 | 5B tunnel — początek tunelu spiralnego |
| 108 | 40388 | zmiana tekstury tunelu |
| 112 | 41884 | 5C mosaic |
| — | 41984 | start globalnego cyklu od pełnej fazy tunelu (v194) |
| 116 | 43379 | 5D eyes |
| 120 | 44875 | Act 6 / 6A |
| 124 | 46371 | 6B |
| 128 | 47867 | Act 7 / 7A |
| 136 | 50858 | 7B |
| — | 51850 | Act 8 / 8A — terminal i leżący chłopiec, 10 s wcześniej |
| — | 52850 | 8A — plansza audio |
| 144 | 53850 | 8A — plansza Silly Venture / AI |
| — | 54850 | 8B — pierwsza plansza greetz |
| — | 55697 | 8B — anegdota o mamie |
| — | 56544 | 8B — podziękowania / AI |
| — | 57391 | 8B — znajomi i grupy |
| — | 58238 | 8B — ekipa i goście Silly Venture |
| 158 | 59085 | 8C — finałowy kadr / fade |
| 160 | 59833 | koniec |

## Zmiany względem v1

1. Zegar po tickach playera, nie po klatkach (93,75 klatki na takt zastąpione 93,5).
2. Act 2 wydłużony do taktu 56, Act 3 skrócony do 8 taktów.
3. Act 4 podzielony na ciszę (64-72) i uderzenie (72-88).
4. Act 5 podzielony na 4 efekty.
5. Act 6 skrócony do 8 taktów, Act 7 zaczyna się w 128.
6. Act 8 wydłużony do 16 taktów, zaczyna się w 144.

## Do weryfikacji

- Granice wynikają z analizy energii i brzmienia mp3, nie z odsłuchu melodii. Przesłuchaj punkty zmian: 24, 32, 40, 56, 64, 72, 88, 92, 104, 108, 112, 116, 120, 128, 144, 158.
- Obecny build używa v035; adresy jego licznika i synchronizacja są zweryfikowane. Dawny opis dotyczył v024, którego brak w checkoutcie; pełne porównanie obu wersji pozostaje niewykonane.
- Koszt CPU ticków muzyki (4 na klatkę) i konflikt o DLI z efektami (tunel, zoom, rotacje) trzeba zmierzyć w Altirze.
- Dawne założenie przycięcia playera do 7 banków zostało obalone audytem v035: bank 8 zawiera wymagany znacznik końca. Nie wykonywać takiego przycięcia. Obecnie 64 banki są przydzielone, a odzyskane sloty opisują `AGENTS.md` i `docs/PLAN_STATUS.md`.
- Szczegóły techniczne, stan wiedzy i zadania weryfikacyjne: `TLIKTB_Technical_Constraints.md`.
