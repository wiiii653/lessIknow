# The Less I Know The Better - Atari XE 1MB: ograniczenia techniczne

Dokument dla agenta kodującego. Uzupełnia `TLIKTB_Atari_Timeline_v2.md` (co i kiedy) i `TLIKTB_Asset_List.md` (z czego). Tu jest: w jakich granicach i co jest sprawdzone.

## Stan wdrożenia — v190

[ODCZYT] V190 zastępuje BNG! napisem BUM, zachowując BAM. Klatki tunelu
48–63 mają organiczne falujące pasma zamiast szachownicy. Bez zmiany banków,
ticków, 298 wierszy i kodu głównego (2560 B).
Szczegóły: `docs/V190_BUM_I_ORGANICZNY_TUNEL.md`.

## Historia: v189

[ODCZYT] V189 przywraca komplet grafiki koszykówki i łat szkła z v175:
12 988 B pod $4B80–$7E3B banku loadera 1. Osiem póz, cztery różne fazy
kozłowania, duża tablica i trzy fazy rozbicia. Kod, piłka i ticki zachowane.
Main 2560 B, 298 wierszy / 11 480 B, 64 banki; zmienia się tylko bank 1.
23 testy zaliczone. Stereo POKEY całego utworu: 14 992 848 zgodnych bajtów.
Szczegóły: `docs/V189_KOSZYKOWKA_I_TABLICA_V175.md`.

## Historia: v188

[ODCZYT] V188 zachowuje ciągłe PMG podczas budowania kolejnego bufora nut.
Usunięto reset GRACTL/DMACTL z aktywnych scen 10–11; raster pokazuje zero
wyłączeń zamiast około jednej klatki PAL. Main zajmuje całe $1400–$1DFF:
2560 B, zero bajtów zapasu przed pulą $1E00. 19 testów zaliczonych; cały
utwór w Atari800: 16 336 440 zgodnych bajtów stereo POKEY.
Szczegóły: `docs/V188_CIAGLE_PMG_BEZ_STROBO.md`.

## Historia: v187

[ODCZYT] V187 powiększa nuty do 16 logicznych pikseli szerokości i maksymalnie
48 scanlinii, ze stałą jasnością 14 do końcówki lotu. SIZEP=1, SIZEM=$55.
Helper 1167 B w $6A00–$6E8E, bez nowych banków. Main 2552 B,
298 wierszy / 11 480 B. 16 testów zaliczonych.
Szczegóły: `docs/V187_DUZE_NUTY_PMG.md`.

## Historia: v186

[ODCZYT] V186 synchronizuje usta i nuty w 4862–5610, kończąc melodię
przy drzwiach. Dwie skończone fale PMG, odrębne łuki, fade i ślady missiles.
Helper 1119 B w $6A00–$6E5E banku 0; main 2552 B; 298 wierszy / 11 480 B.
15 testów sceny/piłki zaliczonych. Atari800 PAL/1088XE, stereo POKEY:
6 220 440 identycznych bajtów z v035, cały utwór.
Szczegóły i pełny zestaw testów: `docs/V186_DOMKNIETA_SCENA_SPOTKANIA.md`.

## Historia: v185

[ODCZYT] V185 wydłuża gwizd PMG do 4862–5984 (około 5,6 s). Helper
zajmuje 839 B w $6A00–$6D46 banku loadera 0; dispatcher obejmuje sceny
10–12. 316 wierszy / 12 174 B, kod główny 2552 B, 64 banki.
14 testów zaliczonych; bez nowej walidacji emulatorowej.
Szczegóły: `docs/V185_DLUZSZA_MELODIA.md`.

## Historia: v183

[ODCZYT] V183 zastępuje bitmapowe nuty animacją players i missiles.
835 B kodu/danych zajmuje $6A00–$6D42 w loader index 0. PMG naprzemiennie
używa istniejących buforów $0980–$0BFF i $8980–$8BFF; publikacja w blankingu.
Main 2552 B, 316 wierszy / 12 158 B, 64 banki; 13 testów zaliczonych.
Szczegóły: `docs/V183_NUTY_PMG.md`.

## Historia: v182

[ODCZYT] V182 rozdziela portret chłopca na spojrzenie przed siebie,
odwrócenie za mijającą dziewczyną i gwizd przy drzwiach. Bez zmian banków
i ticków; 316 wierszy, 12 153 B danych, 2552 B kodu. Siedem testów
zaliczonych. Szczegóły: `docs/V182_REAKCJA_CHLOPCA.md`.

## Historia: v181

[ODCZYT] V181 przywraca spacer i kadry spotkania z v175. Tor zmniejszania
dziewczyny kończy się w lewych drzwiach, a maska kurtki jest kryjąca.
275 współdzielonych wierszy, 10 630 B danych, 2552 B kodu; banki bez zmian.
Sześć testów zaliczonych; sprawdzenie muzyki Atari800 zablokowane przez FUSE.
Szczegóły: `docs/V181_WEJSCIE_DZIEWCZYNY_V175.md`.

## Historia: v180

[ODCZYT] V180 zachowuje poprawki v179 i wydłuża tunel w akcie 5. Bananowy
rotator kończy się w takcie 92 (tick 34404); spiralny tunel zaczyna się wtedy,
a jego tekstura zmienia się w radialną w takcie 108 (tick 40388). Dotychczasowy
koniec ujęcia w takcie 112 (tick 41884), dalsze granice, banki oraz kod efektów
pozostają bez zmian. Budowa `build/visual-prototype-v180.xex` poprawna; 286
współdzielonych wierszy, 11 034 B danych wierszy, 2552 B kodu. Testów ani
emulatora nie uruchomiono. Szczegóły: `docs/V180_DLUZSZY_TUNEL.md`.

## Historia: v170

[ODCZYT] V170 podmienia portret chłopca w pierwszym ujęciu szkoły: jedno oko
puszcza, usta gwiżdżą ku dziewczynie, a klucze wiolinowe i nuty układają się
w ślad melodii. Nowy obraz jest osobnym źródłem; starego nie nadpisano.
Pikselowe symbole są komponowane w 160×192, za dziewczyną w kolejności
warstw. Nie zmieniono ticków ani banków. Zajętość wspólnych wierszy rośnie
do 309 (11 913 B), kod główny pozostaje 2552 B. XEX:
`build/visual-prototype-v170.xex`; SHA-256:
`a439cbe3e2fc94cff35ccf941d5a11df21c8c79618328da034909d4fad12ac5c`.
Budowa poprawna; testów nie uruchamiano. Szczegóły:
`docs/V170_GWIZDAJACY_ZIOMEK.md`.

[ODCZYT] V169 realizuje zmianę tekstury tunelu w akcie 5 przy ticku 40388:
spiralne pasma ustępują radialnej siatce gwiazd. Oba motywy dzielą istniejące
klatki 32–63 i banki; liczba banków ani dane graficzne nie rosną. Kod główny
2552 B, osiem bajtów przed limitem `$1E00`. XEX:
`build/visual-prototype-v169.xex`; SHA-256:
`05f1c69517d4b1f459fec5b4183e59266392d9e169c72f4b6f4b3e35b9939b8e`.
Budowa poprawna; testów i odtwarzania nie wykonywano. Szczegóły:
`docs/V169_ZMIANA_TEKSTURY_TUNELU.md`.

[ODCZYT] V168 morfuje geometryczną ramkę/tunel za Trevorem od prostokąta
do owalu i z powrotem przez istniejące 16 faz tła. Sylwetka i grafika
Trevora pozostają bez zmian; nie dodano banków ani danych. Nowy XEX:
`build/visual-prototype-v168.xex`; SHA-256:
`cec65fb359440302247341403ba7f7bd9ce2eca8b58fa83c874b5815b320bcb5`.
Budowa zakończyła się poprawnie; bez uruchamiania testów i odtwarzania.
Szczegóły: `docs/V168_MORFUJACA_RAMKA_TREVORA.md`.

[ODCZYT] V167 cykluje jasny kolor refleksów tunelu po Trevorze przez 16
barw istniejącej palety, po jednej na fazę obrazu (co 16 ticków). Krótka
przebitka tunelu w akcie 3 i żółta paleta bananowego rotatora pozostają bez zmian. Nowy XEX:
`build/visual-prototype-v167.xex`; SHA-256:
`fe7e0408d324f57649d0a2d0e796dcb1dc58242177b646ad194d07ba8d5fe4d0`.
Budowa zakończyła się poprawnie; testów ani odsłuchu w tej zmianie nie
wykonywano. Kod główny nadal 2546 B. Szczegóły w
`docs/V167_TECZOWY_CYKL_KOLOROW.md`.

[ODCZYT] V166 dodaje 14 kompozycji pośrednich z dziewięciu nowych póz

[ODCZYT] V166 dodaje 14 kompozycji pośrednich z dziewięciu nowych póz
w trzech późniejszych ujęciach tańca. Oryginalne akcenty, boczne ujęcie,
cięcia i wyrzut bez zmian. Nowa poza trafia w środek przedziału 46/47 ticków;
bitmapa i kotwice szarf są przygotowane w nieaktywnych buforach.
Kompresja 35 840 B do 16 886 B; dekoder 140 B w ośmiu bankach,
selektor 1015 B. Zajęto 19 021 B dawnych luk banków 2 oraz 32–38.
Kontroler szarf +9 B = 2246 B, 10 B przed finałem. Runtime nadal 768 B,
z nowym kodem i prywatnym workspace w jego istniejących lukach.
Main nadal 2546 B, banków nadal 64. Zweryfikowane pozostałe luki banków:
31 623 B (30,88 KiB); mapa v165 jest historyczna. Szczegóły:
`docs/V166_PLYNNIEJSZY_TANIEC.md`, `build/v166-allocations.json`.

[ODCZYT] V165: do pierwszego pęknięcia tablicy (fazy wsadu 0–74) cztery
missiles orbitują wokół aktualnej piłki po różnych elipsach, w przeciwnych
kierunkach i z różnymi prędkościami. Faza 75 przywraca dotychczasowe szkło.
Tabele orbit: 256 B `$7E40–$7F3F`, za danymi tablicy; ogon banku 192 B.
Helper bohatera: 2859 B `$4000–$4B2A`, 85 B przed danymi `$4B80`.
Zapis live PMG czeka teraz na ograniczone okno VCOUNT 124–127, a przy
spóźnieniu na następne. Koszt +463 B; netto vs v141: 34 305 B (33,50 KiB).
Zmienił się wyłącznie bank loadera 1, bez zmian pozostałych banków/RAM-u,
main (2546 B), liczby banków (64), granic scen i muzyki.
`docs/V165_ORBITY_PRZY_WSADZIE.md`.

[ODCZYT] V164: fajerwerki obu plansz intro startują od dolnej krawędzi
aktywnego obrazu (y=190), lecą do górnych wierzchołków y=36/44/56/72,
wybuchają promieniście i rozsypują iskry. Lot: 64 ticki, kotwice co 4 ticki,
kształty co 16, kolory tęczy co 8. Kolejność napisów i ticki scen zachowane.
Banki loadera 40/41: kontroler 1428 B `$6C00–$7193`, publikacja `$7000`,
kotwice 257 B `$7280–$7380`, kształty nadal 3072 B `$7400–$7FFF`.
Koszt +648 B w obu bankach, odzysk netto vs v141: 34 768 B (33,95 KiB).
Nadal 64 banki, main 2546 B. Podwójny bufor PMG i okno VCOUNT zachowane.
`docs/V164_TECZOWE_RAKIETY.md`.

[ODCZYT] V163: Trevor wywołuje ten sam oryginalny renderer piłki rotatora
z obiema parami satelitów missiles, przesuwając cały efekt do bliższej krawędzi.
Nie odczytuje rejestrów HPOS (odczyt GTIA zwraca kolizje); przesunięcie
trafia do renderera przed publikacją pozycji. BANG/BAM i ticki bez zmian.
Usunięto kopie masek 16 × 512 B z banków 24–39. Helper Trevora: 2466 B,
`$6000–$69A1`, 94 B zapasu. Bank 2: adapter 44 B `$4000–$402B`,
14 292 B wolne `$402C–$77FF`, dotychczasowe 2048 B `$7800–$7FFF`.
Dodatkowy odzysk netto vs v162: 9695 B, vs v141: 35 416 B (34,59 KiB).
Główny kod nadal 2546 B, banków nadal 64. Szczegóły:
`docs/V163_PILKA_Z_SATELITAMI.md`.

[ODCZYT] V162 usuwa nowy cykl PMG, przywraca wcześniejszy renderer
rotatora/tunelu i zwalnia bank 2 `$4000–$77FF` (14 KiB). Zostaje tylko
helper/data `$7800–$7FFF`. Dwóch piłek Trevora używa tego samego slotu
512 B; duża leci w lewo, kompaktowa w prawo. Helper ma 2557 B,
`$6000–$69FC` (3 B zapasu). Główny kod nadal 2546 B, banków nadal 64.
Odzysk netto vs v161 12 640 B, vs v141 25 721 B.
`docs/V162_STARE_EFEKTY_I_DWIE_PILKI.md`.


[ODCZYT] V161 przywraca grafiki bananów/tunelu bez ditheringu, identyczne
z v158. Inne banki i niebankowany RAM są identyczne z v160. Cykl z sercem,
maskowanie aktywnym PMG, mapa pamięci, kod i ticki pozostają bez zmian.
`docs/V161_BEZ_DITHERINGU.md`.


[ODCZYT] V160 usuwa stałą piłkę/osłonę i fajerwerki cyklu. Otwór zasłania
aktualny efekt PMG; player 0 ma osobne maski/pozycje/rozmiary dla każdej
klatki. Nowy tryb bijącego serca. Helper 497 B, dodatkowe maski 2048 B,
metadane 192 B, wskaźniki 128 B zamiast dawnej wspólnej maski 16 B.
Koszt względem v159: +2380 B, bank 2 zajmuje 14 705 B i ma 1679 B luk.
Bez nowych banków i zmian main/ticków. Netto vs v141: 13 081 B.
Aktualna mapa i walidacja: `docs/V160_SERCE_I_MASKOWANIE_EFEKTEM.md`.


[ODCZYT] V159 dodaje dithering uporządkowany 4×4 do przejść cienia
bananów i barwnych krawędzi wiatraka tunelu. To zmiana istniejących
bitmap: bez nowego RAM-u, kodu, banków i zmian ticków. Czarne kontury,
białe grzbiety i osłona środka pozostają. Mapa pamięci v158 aktualna.
`docs/V159_DELIKATNY_DITHERING.md`.


[ODCZYT] V158: cykl ośmiu rodzin PMG w 32909–59085. Player 0 stale kryje
środek tunelu; players 1–3/missiles zmieniają efekt co 512 ticków.
Nieużywany stary Trevor w banku loadera 2 zastąpiony rendererem PMG;
wcześniejszy helper `$7800` zachowany z przekierowaniem po ticku 32909.
Nowy helper 469 B, dane 8192 B, metadane 1344 B, wskaźniki 256 B,
rdzeń 16 B. Łącznie bank 2 zajmuje 12 325 B zamiast 14 881 B,
czyli odzyskano 2556 B. Nadal 64 banki, main 2546 B.
Netto vs v141: 15 461 B. Mapa i walidacja: `docs/V158_CYKL_PMG.md`.


[ODCZYT] V157 naprawia rasteryzację krzywych szarf: odcinki między próbkami
wypełniają pomijane wiersze. Nadal 5120 B strumieni, bez wzrostu kodu
lub banków. Mapa pamięci v156 pozostaje aktualna.
Szczegóły: `docs/V157_CIAGLE_SZARFY.md`.


[ODCZYT] V156: co trzeci cios wypuszcza piłkę tunelu po napisie.
Maski po 512 B w `$5E00–$5FFF` banków akcji 24–39; nie banku 49.
Helper Trevora 2556 B (`$6000–$69FB`), 4 B przed `$6A00`.
Łączny przyrost zajętości 10 929 B, odzysk vs v141 12 905 B.
PMG nadal podwójnie buforowane; bez zmian muzyki, main i ticków ciosów.
Szczegóły: `docs/V156_TREVOR_WYBIJA_PILKE.md`.


[ODCZYT] V155 naprawia maskę portretów chłopca: czarne włosy oraz fragmenty
kurtki są nieprzezroczyste w obu pozach. Pełna sylwetka zamiast selekcji
komponentów koloru, także na prawej krawędzi. Bez zmian rozmiarów kodu,
banków i timeline’u. Spakowane wiersze 10 764 B (−163 B względem v153).
Odzysk netto względem v141: 23 834 B. `docs/V155_PELNA_MASKA_CHLOPCA.md`.


[ODCZYT] V153 wymienia 512 B wspólnych masek piłki rzutu, kozłowania
oraz wsadu na pełną kulę z kolorowymi panelami i jasnymi szwami. Bez wzrostu
kodu, danych ani liczby banków; nadal 2546 B main i 2652 B hero.
Aktualny timeline i bilans pamięci v151 pozostają w mocy.
Szczegóły: `docs/V153_PILKA_RZUT_KOZIO_WSAD.md`.


[ODCZYT] Dokument powstał dla v024. Opisy jego deasemblacji i pierwotne
propozycje assetów poniżej są historyczne; obecny build używa v035. Bieżący
postęp i wyniki V1–V7: `docs/PLAN_STATUS.md`; mapa zajętości: `AGENTS.md`.
Pliku `TLIKTB_Asset_List.md` obecnie nie ma w checkoutcie — odwołania do niego
opisują wcześniejszy plan, nie dostępną listę wejść generatora.

[ODCZYT] Testowana konfiguracja to Atari800 PAL/1088XE, Altirra OS, stereo
POKEY. Wszystkie 64 banki są przydzielone; nie ma już 50 wolnych banków.
Muzyka v035 wymaga ośmiu banków, w tym odczytu znacznika końca w ósmym;
loadera nie wolno przycinać do siedmiu. Wolne po INIT obszary playera oraz
sloty opisane historycznie w V120 zostały wykorzystane przez wideo.
V142 ponownie uwalnia `$4A00–$53FF` w bankach loadera 24–39 oraz
`$7C00–$7FFF` w sześciu oryginalnych bankach playera 9–14. Łącznie
47 104 B wolnych slotów; po koszcie dodatkowego kodu i metadanych odzysk
netto względem v141 to 46 633 B. Nie oznacza to wolnych całych banków.
V143 wykorzystuje 16 KiB tych slotów na niezależną, maskowaną postać,
przesuwaną w poziomie wraz z PMG. Bieżący odzysk netto to 29 901 B;
mapa v142 powyżej opisuje stan historyczny. Aktualna mapa jest w `AGENTS.md`.
V144 powiększa Żurawia do 40×32 pikseli źródłowych wewnątrz istniejących
klatek plazmy. Przebudowa masek napisów i PMG nie zwiększa danych Atari;
bilans pamięci v143 pozostaje aktualny.
V145 realizuje wyrzut z kamery nad dziewczyną, rozbicie tablicy przy wsadzie
i ostatni kadr chłopca na podłodze z gwiazdkami oraz fade'em. Nadal 64 banki;
bieżący odzysk netto względem v141 to 25 303 B. Nowa bitmapa zajmuje slot
`$4A00–$53FF` banku loadera 39, kontroler `$5B80–$5EAB` banku 49.
Mapa `AGENTS.md` uwzględnia także nowe dane i kod rozbicia tablicy w banku 1.
V146 usuwa kratkę tła w trzecim ujęciu tańca i zastępuje szarfy fajerwerkami
podczas lotu. Kontroler szarf/fajerwerków ma 2203 B (`$5400–$5C9A`),
kontroler finału jest teraz w `$5CC0–$5FEB`; pozostaje 20 B przed `$6000`.
Nadal 64 banki; bieżący odzysk netto względem v141 to 24 954 B.
V147 zmienia kolejność istniejących póz trzeciego ujęcia na pojedynczy
przebieg bez pętli. Mapa pamięci, rozmiary danych i kodu pozostają jak w v146.
V148 zastępuje wolne przygotowanie tańcem i szybkim wyrzutem w dwóch
planach, z efektem pędu na players/missiles. Nowe kształty wiatru zajmują
`$7F20–$7F9F` banku 49, kontroler ma 2237 B (`$5400–$5CBC`). Kontroler
finału przeniesiono do `$5CD0–$5FFB`; przed `$6000` zostają tylko 4 B.
Główny kod ma 2515 B. Aktualny odzysk netto względem v141: 24 771 B.
V149 scala lewą basztę Żurawia z korpusem i zmniejsza go do 36×29 pikseli.
Fajerwerki intro są na pierwszym planie (`PRIOR=$C1`), bez maskowania przez
litery i budynek. W bankach loadera 40/41 kontroler ma 1356 B
(`$6C00–$714B`), kotwice `$73F8–$73FC`, kształty `$7400–$7FFF` (3072 B).
Dłuższe ślady missiles mają własną tabelę adresów. Koszt względem v148:
1088 B, w istniejących bankach. Bieżący odzysk netto względem v141:
23 683 B (23,13 KiB), nadal 64 banki. Główny kod nadal 2515 B.
Szczegóły i walidacja: `docs/V149_ZURAW_I_PIERWSZY_PLAN.md`.
V150: piłka rotatora/tunelu ma 16 faz, stałą nieprzezroczystą sylwetkę,
zakrzywione szwy, refleks i cztery neonowe barwy. Dwie maski paneli
(2×512 B) i dwa obrysy (2×32 B) zastępują cztery pełne strumienie.
Po scaleniu tabel par missiles całość mieści się w dotychczasowych 2 KiB
banku loadera 2 (`$7800–$7FFF`), +37 B względem v149. Bez nowych banków.
Odzysk netto względem v141: 23 646 B (23,09 KiB). Główny kod bez zmian.
Walidacja i ograniczenia: `docs/V150_PSYCHODELICZNA_PILKA.md`.
V151 realizuje zatwierdzoną przebitkę po wyrzucie: tunel 20942–21690,
kozłowanie 21690–23186 i wsad 23186–23934. Wyrzut oraz wejście Trevora
zachowują czas. Nowe fasada i wnętrze ATARI ARENA zastępują istniejące
bitmapy; duże Fuji zastępuje NORTH na plecach dziewczyny. Nadal 64 banki.
Główny kod ma 2546 B (`$1400–$1DF1`), tylko 14 B do puli od `$1E00`.
Hero ma 2652 B kodu (`$4000–$4A5B`), 292 B do danych `$4B80`.
Wiersze po spakowaniu: 10 927 B, o 71 B mniej niż w v150. Bilans względem
v150: +31 B main +15 B hero −71 B wierszy = −25 B zajętości.
Bieżący odzysk netto względem v141: 23 671 B (23,12 KiB).
Walidacja, źródła i pełne prompty: `docs/V151_ATARI_ARENA_I_PRZEBITKA.md`.




[ODCZYT] Licznik `$24A7–$24A9` jest używany w bieżącym v035. Wrapper NMI
zachowuje PORTB. ANTIC czyta niebankowane bufory bitmap `$9000`/`$B000`;
PMG wstęg i efektów ciosów ma bufory `$0980–$0BFF` oraz `$8980–$8BFF`.
Przygotowanie trafia do nieaktywnego bufora, zatwierdzenie w ograniczonym
oknie początku wygaszania. Sam warunek VCOUNT >= 124 nie zapewnia terminu.

[ODCZYT] V136 zastąpiło dawne portrety choreografią trzech ujęć ze wstęgami;
V137 dodało tęczę po istniejących tickach muzyki, V138 BANG/BAM i kolorowy
rozpad PMG. Nie zmieniono czterech muzycznych DLI ani granic aktów.
V142 zastępuje wcześniejszy taniec z pomponami bocznym ujęciem szarfy
w 8975–11967, dodaje pozy późniejszych ujęć i archiwizuje poprzednią scenę
jako samodzielny projekt. 36 bitmap po 2560 B mieści się w sześciu bankach.
Akt 5 pozostaje częściowy, akty 6–7 oraz credits/greetz nie są zrealizowane;
finałowe ujęcie 8C działa od v145. Testy CPU i zgodność
stereo POKEY nie zastępują kontroli obrazu/odsłuchu na docelowym sprzęcie.

Każde twierdzenie ma status:

- **[ODCZYT]**: odczytane bezpośrednio z pliku `less-i-know-hook-v024.xex` (struktura XEX, deasemblacja, teksty na ekranie playera)
- **[WNIOSEK]**: wynika z czytania kodu, ale nie było testowane w emulatorze
- **[ZAŁOŻENIE]**: przyjęte bez sprawdzenia

Nie traktuj [WNIOSEK] i [ZAŁOŻENIE] jak faktów. Historyczne zadania V1–V7
mają aktualne statusy w `docs/PLAN_STATUS.md`; nie uruchamiaj ponownie V7
według dawnego założenia siedmiu banków.

## 1. Sprzęt i cel

- Atari 65XE z rozszerzeniem do 1 MB, PAL, stereo POKEY (drugi POKEY pod `$D210`)
- [ZAŁOŻENIE] 64 banki po 16 KB poza 64 KB pamięci głównej. Układ bitów PORTB zależy od konkretnego rozszerzenia (patrz sekcja 3).
- Emulator do testów: Altirra, 65XE, 1 MB, PAL, drugi POKEY włączony. Układ banków w konfiguracji pamięci emulatora musi odpowiadać układowi wykrywanemu przez player.
- Cykli na klatkę PAL: ok. 35 568 (312 linii × 114 cykli), pomniejszone o DMA ANTIC-a i przerwania.

## 2. Plik playera `less-i-know-hook-v024.xex`

**[ODCZYT]**

- Rozmiar 233 468 B, 40 segmentów XEX.
- Kod i dane w pamięci głównej: segmenty od `$2000` do `$37BF` (kod `$2000-$24B2`, dane i tablice `$24BD-$28BC`, bufor rejestrów `$2900-$293F`, dalej `$2A00-$2F7E`, display lista `$3300-$3323`, ekran tekstowy `$3400-$37BF`).
- Rejestr zestawu znaków (CHBASE) ustawiany na `$38`, czyli font w `$3800-$3BFF`. Tego fragmentu nie ma w pliku, więc powstaje w czasie działania (skąd, nie wiadomo).
- 14 segmentów po 16 KB wczytywanych do `$8000-$BFFF`. Po każdym wywoływany jest INIT `$20EA`, który kopiuje blok do banku (okno `$4000-$7FFF`, wartość PORTB z tablicy). `$8000-$BFFF` to tylko miejsce przejściowe.
- Prawdziwe dane muzyczne: ok. 98,9 KB (6 pełnych banków plus 3 017 B w siódmym). Banki 8-14 to identyczne bloki wypełnione `$FF`.
- Wykrywanie pamięci: INIT `$2000` próbuje trzech tablic wartości PORTB (po 14), zapisując numer banku w `$4000` i sprawdzając odczyt. Po trzech porażkach wyświetla błąd.
  - Tablica 0 (`$270A`): `81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB`
  - Tablica 1 (`$2718`): `03 07 0B 0F 43 47 4B 4F 83 87 8B 8F C3 C7`
  - Tablica 2 (`$2726`): `83 87 8B 8F A3 A7 AB AF C3 C7 CB CF E3 E7`
  - Indeks pasującej tablicy zostaje w `$249D`.
- Rozmiar bloku `$FF` w bankach 8-14 sugeruje, że loader rezerwuje więcej niż potrzeba. Przycięcie do 7 banków oszczędza ok. 112 KB, ale wymaga weryfikacji V3.
- Teksty na ekranie playera: 128 BPM, 05:00, „4 UPDATES PER PAL FRAME / 199.443 HZ”, „STEREO POKEY / SILLY VENTURE 2026”, „POKEY PORT/REMIX BY OGNJEN”, „ORIGINAL: TAME IMPALA”. START = pauza/odtwarzanie, SELECT = restart.

## 3. Zachowanie playera

**[ODCZYT]**

- Player jest sterowany przez DLI, nie VBI. Wektor DLI (`$0200/$0201`) wskazuje `$2210`. W RUN `$D40E` ma wartość `$80`.
- Display lista playera (`$3300`) ma bit DLI w czterech instrukcjach, które zaczynają się w liniach 0, 73, 151 i 229 (licząc od początku listy). DLI wyzwala się na ostatniej linii instrukcji, więc praktycznie ok. linie 0, 78, 156, 234. Odstęp ok. 78 linii = 312/4, co daje 4 aktualizacje na klatkę.
- Aktualizacja: bufor `$2900-$2911` (18 bajtów) trafia do `$D200-$D208` i `$D210-$D218` (rutyna `$2C00`). `$D20F` i `$D21F` ustawione na 3 przy starcie.
- Licznik 24-bitowy `$24A7-$24A9` rośnie w ścieżce aktualizacji (`$22F4`). Licznik `$24AA-$24AC` rośnie przy każdym DLI, a pętla główna odświeża UI co 4. DLI.

**[WNIOSEK]**

- Pauza (START) zatrzymuje licznik `$24A7-$24A9`, bo omija ścieżkę aktualizacji.
- Koszt ticka: rutyna `$2C00` wykonuje ok. 21 par odczyt-zapis (kilkaset cykli), plus dekoder strumienia, którego nie prześledziłem. Całość jest nieznana.
- DLI to NMI, więc `SEI` go nie blokuje. Tick może przerwać dowolny kod, także w trakcie przełączania banku. Szczegóły w sekcji 4.

## 4. Ograniczenia dla silnika wideo

1. **Muzyka nie może stracić ticków.** Cztery DLI na klatkę w odstępach ok. 78 linii. Nie wiadomo, czy nierówne rozmieszczenie psuje rytm (V6), więc zachowaj odstępy. Własny handler DLI może obsługiwać także efekty (zmiany palety), ale tick musi wykonać się punktualnie.
2. **PORTB.** Handler NMI zachowuje bank foreground na wejściu i przywraca przed RTI. Utrzymuj to zabezpieczenie; ANTIC obecnie czyta niebankowaną RAM. Kolory wstęg są obsługiwane po ticku, w kodzie niebankowanym i bez współdzielonej pamięci tymczasowej.
3. **Banki.** Wszystkie 64 banki są przydzielone; fizyczne selektory wynikają z wykrywania rozszerzenia. Nie zakładaj wolnych banków ani wolnych slotów V120. Bieżąca mapa zajętości jest w `AGENTS.md` i generatorach, które sprawdzają nakładanie danych.
4. **Pamięć główna.** Player v035 i silnik współdzielą RAM według aktualnego generatora XEX, nie mapy v024. Nie nadpisuj obszarów na podstawie ich dawnego przeznaczenia (font/ekran/UI). Zachowaj sprawdzanie nakładania segmentów i rezerwację obu buforów PMG.
5. **CPU.** Budżet klatki to ok. 35 568 cykli minus DMA ANTIC-a (tryby bitmapowe zabierają dużo), minus 4 ticki. Efekty z DLI na każdą linię lub z ciężkimi tablicami (tunel, zoom, rotacje, kalejdoskop) zmierz wcześnie.
6. **Zegar.** Zdarzenia z timeline'u wyzwalaj po liczniku ticków playera, nie po klatkach VBI. VBI w PAL to ok. 49,86 Hz, a nie 50,0.

## 5. Zadania weryfikacyjne (przed budową silnika)

Wykonuj w Altirze. Każde zadanie kończy się krótką notatką: wynik i czy zmienia założenia powyżej.

- **V1.** Profiler: koszt ticka (od wejścia w `$2210` do RTI), minimum, średnia, maksimum cykli.
- **V2.** Czy tick przywraca PORTB: odczytaj kod ścieżki aktualizacji i sprawdź w teście, przełączając bank w pętli głównej podczas odtwarzania i słuchając artefaktów.
- **V3.** Czy player czyta banki 8-14: loguj zapisy do `$D301` podczas całego 5-minutowego odtwarzania, wyznacz największy używany bank. Ustal też, która tablica PORTB została dopasowana (`$249D`) w docelowej konfiguracji.
- **V4.** Czy pauza zatrzymuje `$24A7-$24A9`.
- **V5.** Porównaj v024 z v035: adresy licznika, DLI, wektor, układ pamięci.
- **V6.** Czy tick wymaga równych odstępów DLI: przesuń DLI i sprawdź rytm.
- **V7.** Zadanie historyczne zablokowane: v035 potrzebuje ośmiu banków. Nie przycinać do siedmiu. Zweryfikowane odzyskiwanie obszarów po INIT opisuje `docs/PLAN_STATUS.md`.

## 6. Konwencje assetów (propozycja do akceptacji)

- Tryby: ANTIC E (160×192, 4 kolory, 40 B na linię, 7 680 B na ekran) jako domyślny. Tryb znakowy ANTIC 4 lub 5 dla teł, fontów i tekstów. PMG w rozdzielczości 1 linii (256 B na gracza na klatkę) dla postaci. GTIA 9 (80×192) dla wybranych scen aktu 5 (do decyzji, patrz sekcja 8).
- Paleta: 6-8 kolorów z palety Atari (róż, magenta, cyjan, żółć), konkretne wartości do ustalenia. Paleta per scena w osobnym pliku `.pal`.
- Formaty plików: surowe bitmapy `.bin` (7 680 B na ekran E), palety `.pal`, PMG `.pmg`, fonty `.fnt`, wszystkie dane kompresowane ZX0 (`.zx0`). Nazewnictwo `snake_case` z prefiksem aktu, np. `act2_hearts_tile.bin`, zgodnie z `TLIKTB_Asset_List.md`.
- Konwerter: skrypt w Pythonie (Pillow): obraz źródłowy, dithering (Bayer lub Floyd-Steinberg), wyjście `.bin` plus `.pal`.
- Dekompresja ZX0 trwa kilka klatek na pełny ekran. Rozpakowuj następną scenę w tle do ukrytego banku, nie w trakcie wyświetlania.

## 7. Zasady pracy

- Nie zmieniaj granic aktów, ticków ani priorytetów produkcyjnych bez potwierdzenia człowieka.
- Kolejność prac z asset list: Trevor PMG, Cheerleader PMG, Kaleidoscope, Tunnel, Finale Trevor, Credits.
- Każdy build testuj w Altirze w konfiguracji z sekcji 1 i słuchaj, czy muzyka nie gubi rytmu.
- Zaznaczaj w notatkach, co zweryfikowałeś, a co założyłeś.

## 8. Otwarte decyzje (dla człowieka)

- GTIA 9 w akcie 5: w którym bloku, i dopisanie assetów (palety, obrazy źródłowe).
- Czy zachować UI playera (ekran tekstowy) w demie, czy usunąć.
- Zasady compo: czy dopuszczalne są interlace i flicker, jaki jest standard (PAL), jakie są limity rozmiaru i sprzętu.
- Docelowy układ rozszerzenia pamięci 1 MB i emulator referencyjny.
