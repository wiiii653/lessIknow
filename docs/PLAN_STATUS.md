# Status planu dema — stan po v319

V319 rozszerza maskę kozłującego chłopca po lewej stronie sylwetki, przy
ramieniu i przedramieniu. Usuwane są wyłącznie piksele starego różowego tła
i odtwarzany jest w tych miejscach obraz hali. Pozy i klatki pozostają
bez zmian. Stereo release 052 dla AVG; test maski z porównaniem release 001
zaliczony. Bez próby na fizycznym Atari.

V317 ustawia zieleń `$C6` dla ścian trzech ujęć treningu przy drabinkach.
Ten rejestr koloru obejmuje również część ciemnych detali postaci i sali.
Pozostałe sceny zachowują swoje palety. Stereo release 050 dla AVG; trzy
ujęcia sprawdzone w py65, testy piłki 4/4. Bez próby na fizycznym Atari.

V316 rozszerza ręczne obszary usuwania starego różowego tła przy tylnej
ręce i nogach koszykarza oraz w czterech pozach wsadu. Zastępuje tylko
kolor starego tła pikselami hali; pozy, klatki i trajektoria piłki pozostają
bez zmian. Stereo release 049 dla AVG; 13 testów koszykówki zaliczonych.
Bez próby na fizycznym Atari. Paczka party v315 nadal zawiera release 048.

V315 prowadzi cztery kolorowe dymki od narożników BUM/BAM na zewnątrz,
po przekątnych. Usuwa ukośnik z końcowego dwuwiersza. Stereo release 048
dla AVG; testy uderzeń i finału 19/19 w py65, podgląd faz obejrzany. Brak
oceny na fizycznym Atari.

V314 rozdziela fazy czterech szarf w solowym ujęciu przodem: dwa pasma
poruszają się przeciwnie, jedno dwukrotnie szybciej. Zachowano zaczepy
w dłoniach i istniejące pozy. Stereo release 047 dla AVG; testy buforów,
kotwic i klatek pośrednich 17/17 w py65. Koszt utrzymywanej klatki solówki
w próbce wzrósł o 108 cykli; to nie jest pomiar FPS ani próba na Atari.

V313 unieruchamia `LOADING BANKS` w loaderze; animują się tylko trzy pozycje
kropek. Stereo release 046 dla AVG: pozycja napisu sprawdzona we wszystkich
133 stanach początkowego ekranu i wrapperów. Brak próby na fizycznym Atari.

V312 przyciemnia róż w sekwencji tańca i wyrzutu z `$4E` do `$4A`.
Stereo release 045 dla AVG; testy buforów i palety 7/7. Ocena koloru na
fizycznym Atari pozostaje do wykonania.

V311 zastępuje numery INIT i adresy w loaderze animowanymi kropkami, dodaje
ATARIMUZEUM.PL do greetz i pozostawia po wygaszeniu wyśrodkowany podpis
`A\SLOP BY OGNJEN 2026 / SILLY VENTURE WE`. Stereo release 044 dla AVG.
Testy finału i outro 15/15; sprawdzono 66 etapów loadera oraz rozstaw DLI
karty końcowej w py65. Brak próby na fizycznym Atari i odsłuchu końcówki.

V309 dodaje podpis `A\SLOP BY OGNJEN` do creditsów i glif odwrotnego
ukośnika. Stereo release 043 dla AVG; testy tekstu outro 5/5. Bez próby na
fizycznym Atari.

V308 zmienia fioletową składową obrazu tańca i wyrzutu na intensywny róż
`$4E`. Wszystkie ujęcia szarf i lot korzystają ze wspólnej palety. Stereo
release 042 dla AVG; testy buforów i palety szarf 7/7. Brak oceny na
fizycznym Atari.

V307 przywraca cztery kolorowe dymki po napisach BUM/BAM Trevora, na wzór
v215. Nadlatująca piłka pozostaje przed ciosem; kolejna nadlatująca piłka
ma pierwszeństwo przed kończącym się efektem. Stereo release 041 dla AVG;
testy uderzeń 9/9 w py65. Brak oceny na fizycznym Atari.

V305 przywraca ujęcie oczu z v292: cztery bitmapy oraz zmienną paletę.
Bitmapy są zgodne bajt po bajcie; numery klatek i kolory zgodne w 187
próbkach czasu. Test ujęcia oczu przechodzi. Stereo release 040 dla AVG;
bez próby na fizycznym Atari.

V304 przyciemnia paletę wszystkich póz Trevora: mocniejszy fiolet i róż oraz
cieplejsza skóra, szczególnie podczas odbijania piłek. Stereo release 039 dla
AVG. Sprawdzono kolory póz i uderzenia w py65; bez oceny na fizycznym Atari.

V303 zmienia wiersz loadera na `A\SLOP BY OGNJEN / SILLY VENTURE 2026 WE`.
Stereo release 038 dla AVG zawiera ten dokładny wiersz; mieści się on w 40
znakach. Nie uruchamiano buildu na fizycznym Atari.

V302 usuwa resztki niebieskiego tła przy twarzy chłopca i upraszcza rysy
dziewczyny w bocznym spacerze. Stereo release 037 dla AVG; testy sceny
szkolnej 4/4, bootstrap AVG poprawnie odtwarza pięć segmentów w py65.
Obejrzano podgląd twarzy dziewczyny; brak próby na fizycznym Atari.

V301 poprawia obrysy chłopca w trzech pozach przed areną i uzupełnia kurtkę
przy prawej krawędzi. Stereo release 036 dla AVG; podgląd trzech póz i testy
sceny szkolnej 4/4. Bootstrap AVG odtworzył pięć niskich segmentów w py65;
nie wykonano próby na fizycznym Atari ani pełnego odsłuchu Atari800.

V300 ustawia punkty zmiany kierunku i tekstury późnych tuneli na początki
taktów 98 oraz 102–132 co dwa takty. Ciągłość faz przy nawrotach zachowana.
Sam wybór okien rotatorów i tuneli nadal korzysta ze starego zegara motywów;
zmiana kierunku działa w aktywnym oknie tunelu. Stereo release 035 dla AVG;
testy reżysera montażu 4/4. Bez odsłuchu w Atari800 i na fizycznym Atari.

V299 wydłuża scenę Trevora z odbijaniem piłek do ticku 29656 (o 747
ticków), dodaje pięć uderzeń i wzmacnia paletę jego ujęć. Stereo release
034 dla AVG zbudowano; testy uderzeń 9/9. Nie wykonano próby na Atari800
ani fizycznym Atari. Początek późniejszego montażu jest odpowiednio krótszy;
koniec dema i czas outro pozostają bez zmian.

Aktualizacja v261: do listy greetz dodano KEY-G i FALCON; FOORMAN, podział
wierszy i czas terminala pozostają bez zmian. Release 008 oraz
`build/visual-prototype-v261.xex` mają ten sam SHA-256. Pełne testy bieżącego
builda: 199/199. Nie wykonano ponownego odtworzenia w Atari800 ani na sprzęcie.
Szczegóły: `V261_KEY_G_FALCON.md`.

Aktualizacja v260: na życzenie użytkownika usunięto wszystkie cztery
ostatnie komiksowe przebitki Trevora z rotatorów/tuneli; oczy, walka
i finał zachowane. `V260_ROTATORY_BEZ_TREVORA.md`.

Aktualizacja v259: powtarzaną szachownicę Trevora zastępuje jedno
zbliżenie; oczy dziewczyny zachowane. `V259_TREVOR_BEZ_SZACHOWNICY.md`.

Aktualizacja v258: podpis ładowania `AI-SLOP/OGNJEN`.
`V258_NAPIS_AI_SLOP_OGNJEN.md`.

Aktualizacja v257: komiksowe przebitki Trevora, trzech postaci,
konfrontacji i dużego Trevora w istniejącym montażu; oczy i finał zachowane.
`V257_KOMIKSOWY_MONTAZ.md`.

**Aktualny montaż:** układ v256 przywrócono w v260 i nie zmieniono go w v261.
Od v248 zajmuje ticki 28909–49849; wewnętrzny zegar wyboru motywów jest
przesunięty o 4000 ticków, ale muzyka nie. Outro zaczyna się w 49850. Oczy
dziewczyny są w 39379–40126 (v252). Przebitki komiksowe v257 wycofano w v260.
Dokładna mapa: `AKTUALNY_MONTAZ_V256.md`. Regulamin, status zgłoszenia i
rozróżnienie między release 008 a starszym pakietem v260:
`SV2026WE_PRZYGOTOWANIE.md`.

Aktualizacja v256: loty piłek Trevora bez zatrzymywania na pionowych
ogranicznikach; łagodne pojawianie i znikanie. `V256_LOTY_PILEK_TREVORA.md`.

Aktualizacja v255: orbity finałowe płynnie zmieniają się między wyraźnie
wąską i szeroką elipsą. `V255_WYRAZNE_ORBITY_FINALU.md`.

Aktualizacja v254: podpis ekranu wczytywania `AI-SLOP-OGNJEN 2026`;
zmienił się wyłącznie tekst ekranu. `V254_NAPIS_AI_SLOP.md`.

Aktualizacja v253: ekran tekstowy podczas wczytywania banków, z nazwą
Atari XE, Silly Venture 2026 WE i Ognjen 2026. Szczegóły i ograniczenia:
`V253_NAPIS_PODCZAS_WCZYTYWANIA.md`.

Aktualizacja v252: czterofazowe zbliżenie oczu dziewczyny w montażu,
ticki 39379–40126. Cztery fazy tunelu ponownie wykorzystano na grafikę;
wpływ na wcześniejsze ujęcia i walidacja: `V252_OCZY_DZIEWCZYNY.md`.

Aktualizacja v250: każda nowa linia terminala zmienia cel płynnie
przekształcanych orbit gwiazdek/nut. Szczegóły i pamięć:
`V250_PLYNNE_ORBITY_TEKSTU.md`.

Aktualizacja v249: do ciosów Trevora przylatuje piłka rotatora z satelitami,
po BUM/BAM odlatuje piłka wsadu z własnymi orbitami; tory są różne dla
każdego lotu. Szczegóły i pamięć: `V249_PILKI_I_SATELITY_TREVORA.md`.

Aktualizacja v248: pełny montaż 32909–53850 przeniesiono na 28909–49850,
skracając ujęcie Trevora i przywracając wcześniej utraconą końcówkę montażu;
outro zaczyna się o 2000 ticków wcześniej niż w v247. Szczegóły, pamięć
i ograniczenia w `V248_WCZESNIEJSZE_OUTRO_PELNY_ROTATOR.md`.

Aktualizacja v247: w scenie Trevora każdemu zachowanemu ciosowi towarzyszy
przylot małej piłki, pełne BUM/BAM i odlot piłki. Oryginalne pozy i ticki
pozostają bez zmian. Szczegóły i bieżące zajęcie banku 2:
`V247_TREVOR_PILKI_I_CIOSY.md`. Zmiana nie zamyka braków fabularnych ani
testów na fizycznym sprzęcie opisanych niżej.

Legenda: ✅ wykonane w buildzie lub potwierdzone; 🟡 częściowo wykonane /
ograniczone do prototypu albo emulatora; ⬜ niezaimplementowane lub
nieweryfikowane. Wczesne granice zachowują zatwierdzony timeline; v248
przesuwa wizualny montaż po Trevorze względem muzyki.

Punktem wyjścia był audyt kodu i XEX v144 z 2026-11-07
(`AUDYT_BRAKOW_V144.md`). Tabela aktów niżej opisuje oryginalny timeline,
a nie kompletną listę bieżących ujęć. Audyt v144 jest historyczny i nie
opisuje obecnego wydania, pamięci ani walidacji. V240 przesunęło terminal
do 51850; v248 później przesunęło montaż o 4000 ticków i wejście outro
do 49850. Granice utworu i zegar muzyki pozostały bez zmian.

Zmiany scenariusza zatwierdzone przez użytkownika 2026-11-07,
**zaimplementowane w v145**:

- Trzecie ujęcie szarf: kamera z góry, dziewczyna wyrzucona ku obiektywowi;
  powiększa się, a sala i grupa oddalają się pod nią.
- Wsad: chłopiec rozbija tablicę kosza, z pęknięciem i odłamkami.
- Ostatni kadr outro: ten sam chłopiec pobity na podłodze, z gwiazdkami
  krążącymi wokół głowy; potem wygaszenie do czerni. Credits/greetz są zaimplementowane w v216 w dotychczasowych oknach.

Zegar muzyki pozostaje bez zmian. V151 na zlecenie użytkownika zmienia
wewnętrzne zakresy aktu 3, zachowując długość wyrzutu. V248 przesuwa
wizualny montaż względem muzyki; obecne ticki opisano w mapie v256.

[ODCZYT] V145: 109 testów, 106 zaliczonych, 3 pominięte (brak v126).
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 572 808 identycznych
bajtów względem v035, cały utwór. Nadal 64 banki, 25 303 B odzysku netto
względem v141. Dokładna mapa, źródła/prompty i ograniczenia walidacji:
`V145_WYRZUT_TABLICA_FINAL.md`.

[ODCZYT] V146: ujęcie z góry ma spokojne czarne tło bez kratki i linii
boiska. Szarfy wyłączone w całym trzecim ujęciu; od początku lotu, tick 20662,
po bokach rozkwitają fajerwerki players i lecą iskry missiles. Wcześniejsze
ujęcia zachowują szarfy. Nadal 64 banki, 24 954 B odzysku netto względem v141.
Kontroler końcowego chłopca przeniesiono do `$5CC0`, bez zmiany jego obrazu
i animacji. Szczegóły: `V146_WYRZUT_FAJERWERKI.md`.
Walidacja: 113 testów, 110 zaliczonych, 3 pominięte (brak v126).
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 751 288 identycznych
bajtów przez cały utwór; bez testu na fizycznym Atari.

[ODCZYT] V149: lewa baszta Żurawia połączona z korpusem bez prześwitu
plazmy; cała bryła mniejsza o około 10% w obu wymiarach (36×29).
Fajerwerki mają wznoszenie, promienisty rozkwit i opadające odłamki.
Players/missiles na pierwszym planie, także przed literami i budynkiem.
Bez zmian kolejności napisów ani synchronizacji. Nadal 64 banki;
odzysk netto względem v141: 23 683 B. `V149_ZURAW_I_PIERWSZY_PLAN.md`.
Walidacja: 115 testów, 112 zaliczonych, 3 pominięte (brak v126).
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 348 384 identyczne
bajty względem v035, cały utwór. Bez testu na fizycznym Atari.

[ODCZYT] V150: 16 różnych faz obrotu piłki rotatora i tunelu, zakrzywione
szwy, refleks, jasna krawędź i cztery nasycone kolory. Sylwetka nie pulsuje
i nie ma prześwitów; środek tunelu zasłonięty we wszystkich fazach.
Całość mieści się w 2 KiB istniejącego banku 2; nadal 64 banki.
Odzysk netto względem v141: 23 646 B. Szczegóły:
`V150_PSYCHODELICZNA_PILKA.md`.
Walidacja: 115 testów, 112 zaliczonych, 3 pominięte (brak v126),
91,038 s. Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
15 780 312 identycznych bajtów względem v035, cały utwór.
Bez testu na fizycznym Atari.

[ODCZYT] V151: wyrzut kończy się nadal w 20942. Potem tunel z neonową
piłką 20942–21690 (3,75 s), kozłowanie 21690–23186 (7,5 s), pojedynczy
wsad z rozbiciem tablicy 23186–23934 (3,75 s zamiast 7,5 s).
Wejście Trevora pozostaje w 23934. Nowe fasada i wnętrze ATARI ARENA;
duże Fuji na plecach dziewczyny zastępuje NORTH. Nadal 64 banki,
odzysk netto względem v141: 23 671 B. Szczegóły:
`V151_ATARI_ARENA_I_PRZEBITKA.md`.
Walidacja: 116 testów, 113 zaliczonych, 3 pominięte (brak v126), 86,535 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 154 704 identyczne bajty
względem v035 przez cały utwór. Bez odsłuchu i testu na fizycznym Atari.

[ODCZYT] V153: rzut, kozłowanie i wsad mają wspólną nieprzezroczystą
piłkę z ośmioma obrotami paneli, jasnymi szwami/refleksem i ciemniejszą
krawędzią. Cztery jasności 6/10/12/14 i cykl barw. Nadal 512 B masek,
bez wzrostu kodu i RAM-u. Trajektorie, kotwice dłoni i cały timeline v151
zachowane. Szczegóły: `V153_PILKA_RZUT_KOZIO_WSAD.md`.
Walidacja: 116 testów, 113 zaliczonych, 3 pominięte (brak v126), 87,461 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 373 584 identyczne bajty
względem v035, cały utwór. Bez testu na fizycznym Atari.

[ODCZYT] V155: naprawiono przezroczyste włosy i kurtkę chłopca przed
areną. Pełna maska sylwetki zachowuje czarne piksele włosów i magentę kurtki,
także na prawej krawędzi ekranu. Obie pozy objęte regresją. Bez zmian kodu,
timeline’u i liczby banków. Spakowane wiersze 10 764 B, o 163 B mniej niż
w v153; odzysk netto względem v141: 23 834 B.
Szczegóły: `V155_PELNA_MASKA_CHLOPCA.md`.
Walidacja: 117 testów, 114 zaliczonych, 3 pominięte (brak v126), 87,656 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 573 016 identycznych
bajtów względem v035, cały utwór; bez testu na fizycznym Atari.

[ODCZYT] V156: co trzeci cios Trevora po BANG/BAM wypuszcza dużą piłkę
z tunelu zamiast chmurki players. Cztery fazy obrotu, ruch w górę/prawo,
kolorowe missiles pozostają. Hit ticki i czas efektu bez zmian. Maski
zajmują `$5E00–$5FFF` banków 24–39; bank 49 jest wyłączony z instalacji.
Kontroler ma 2556 B, tylko 4 B do `$6A00`. Nadal 64 banki,
odzysk netto względem v141: 12 905 B. `V156_TREVOR_WYBIJA_PILKE.md`.
Walidacja: 118 testów, 115 zaliczonych, 3 pominięte (brak v126), 87,140 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 403 384 identyczne bajty
względem v035, cały utwór; bez testu na fizycznym Atari.

[ODCZYT] V157: usunięto przerwy we wszystkich szarfach. Generator łączy
kolejne próbki krzywej odcinkami zamiast zaznaczać wyłącznie punkty.
Test sprawdza brak pustych wierszy i spójność ścieżki wszystkich 64 masek
players. Iskry missiles, fajerwerki i wiatr bez zmian. Bez wzrostu pamięci,
kodu, banków i bez przesuwania ticków. `V157_CIAGLE_SZARFY.md`.
Walidacja: 119 testów, 116 zaliczonych, 3 pominięte (brak v126), 89,045 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 720 904 identyczne bajty
względem v035 przez cały utwór; bez testu na fizycznym Atari.

[ODCZYT] V158: w 32909–59085 rotator i tunel mają cykl ośmiu rodzin
PMG bez szarf, z małą kryjącą piłką stale osłaniającą środek. Pozostałe
3 players i 4 missiles pokazują duże/piłki rzutu, fajerwerki, BANG/BAM,
chmurki, gwiazdki, wiatr/fajerwerki wyrzutu i odłamki. Tryb co 512 ticków,
pełna pętla 4096. Wcześniejsze sceny i finał zachowane. Nadal 64 banki;
nieużywane grafiki starego Trevora w banku 2 zastąpił nowy renderer.
Odzysk netto vs v141: 15 461 B. `V158_CYKL_PMG.md`.
Walidacja: 122 testy, 119 zaliczonych, 3 pominięte (brak v126), 90,811 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 202 576 identycznych
bajtów względem v035 przez cały utwór; bez testu na fizycznym Atari.
To urozmaica istniejące tła; nie realizuje brakujących scen fabularnych
aktów 5C/5D, 6–7 ani credits/greetz.

[ODCZYT] V159: skromny dithering 4×4 na przejściach złota/żółci bananów
oraz wąskim pasie barwnych krawędzi wiatraka tunelu. Zmienione odpowiednio
1,81% i 1,99% pikseli. Kontury czerni, białe grzbiety tunelu i otwór bez
zmian. PMG/osłona środka zachowane; bez wzrostu pamięci, kodu i banków.
`V159_DELIKATNY_DITHERING.md`.
Walidacja: 122 testy, 119 zaliczonych, 3 pominięte (brak v126), 90,768 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 9 833 112 identycznych
bajtów względem v035, cały utwór; bez testu na fizycznym Atari.

[ODCZYT] V160 zastępuje osobną kryjącą piłkę v158: otwór zasłania teraz
aktualny efekt PMG swoją własną sylwetką. Fajerwerki usunięto z cyklu;
pojawiło się bijące czerwono-różowe serce. Piłka, komiksowy wybuch, chmurka,
gwiazda, podmuch i odłamek mają pełny środek i używają wszystkich players.
Przedział i tempo cyklu zachowane, wcześniejsze sceny bez zmian.
Bank 2 zajmuje 14 705 B; nadal 64 banki. Odzysk netto vs v141: 13 081 B.
`V160_SERCE_I_MASKOWANIE_EFEKTEM.md`.
Walidacja: 124 testy, 121 zaliczonych, 3 pominięte (brak v126), 90,686 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 806 592 identyczne bajty
względem v035, cały utwór; bez testu na fizycznym Atari.

[ODCZYT] V161 usuwa dithering bananów i tunelu na życzenie użytkownika.
Wszystkie 64 klatki efektów są identyczne z v158. Pozostałe banki i RAM
niebankowany identyczne z v160; serce i maskowanie aktywnym efektem zachowane.
Bez zmian pamięci i timeline’u. `V161_BEZ_DITHERINGU.md`.
Walidacja: 124 testy, 121 zaliczonych, 3 pominięte (brak v126), 90,701 s.
Potwierdzona binarna zgodność przywróconych banków z v158 i wszystkich
innych banków/niebankowanego RAM-u z v160; nie powtarzano POKEY.

[ODCZYT] V162 usuwa nowy cykl PMG z rotatora/tunelu, serce i ich dane.
Przywrócony ten sam wcześniejszy renderer piłki i satelitów; test sprawdza
zasłonięcie otworu tunelu. Bank 2 ma całe `$4000–$77FF` wolne (14 KiB).
W bitce co trzecie BANG/BAM wypuszcza naprzemiennie dużą piłkę tunelu
w lewo lub kompaktową piłkę rzutu w prawo. Dotychczasowe odłamki pozostają.
Te same 512 B masek, po dwie fazy każdego rodzaju; bez nowych banków.
Odzysk względem v161: 12 640 B netto; względem v141: 25 721 B.
`V162_STARE_EFEKTY_I_DWIE_PILKI.md`.
Walidacja: 121 testów, 118 zaliczonych, 3 pominięte (brak v126), 90,643 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 383 304 identyczne bajty
względem v035, cały utwór; bez testu na fizycznym Atari.

[ODCZYT] V163: co trzeci cios po napisie wypuszcza pełną piłkę rotatora
z obiema orbitami satelitów. To wywołanie tego samego renderera, z 16 fazami
obrotu i oryginalnymi kolorami. Całość odlatuje ku bliższej krawędzi według
dłoni Trevora; BANG/BAM, pozostałe chmurki, ticki i długość bez zmian.
Usunięto wszystkie kopie masek z banków 24–39 (8192 B). Bank 2 ma adapter
44 B oraz dotychczasowy helper 2048 B; 14 292 B pozostaje wolne.
Helper Trevora 2466 B, 94 B zapasu. Odzysk dodatkowy vs v162: 9695 B;
łącznie vs v141: 35 416 B. `V163_PILKA_Z_SATELITAMI.md`.
Walidacja: 122 testy, 119 zaliczonych, 3 pominięte (brak v126), 90,000 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 13 910 544 identyczne bajty
względem v035, cały utwór. Bez testu na fizycznym Atari; py65 nie modeluje
ANTIC DMA ani rzeczywistego FPS.

[ODCZYT] V164: rakiety w intro lecą od dolnej krawędzi do górnej części
nieba, z płynną kotwicą co 4 ticki. Wybuch: centralny błysk, promienie,
opadające fragmenty i rozsuwające się na boki missiles. Kolory tęczy
cyklicznie zmieniają się co 8 ticków. Obie plansze zachowują napisy,
Żuraw, kolejność, długość, pełne foreground PMG i podwójny bufor.
Koszt +648 B w bankach 40/41; netto vs v141: 34 768 B. Nadal 64 banki,
main 2546 B. Mapa i walidacja w `V164_TECZOWE_RAKIETY.md`.
[ODCZYT] Pełne `make check`: 124 testy, 121 zaliczonych,
3 pominięte (brak archiwalnego v126), 95.022 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 601 744 identyczne bajty
względem v035, cały utwór. Bez testu na fizycznym Atari.

[ODCZYT] V165: cztery różne orbity satelitów piłki przy wsadzie do kosza,
przeciwne kierunki, jedna szybsza i jedna pochylona. Orbity podążają za
piłką przez wszystkie pozy do pierwszej rysy (fazy 0–74); od 75 pozostają
oryginalne odłamki. Bez zmian kozłowania, grafiki, ticków i długości scen.
Bank loadera 1: +207 B helpera i 256 B tabel, koszt +463 B.
Helper 2859 B, 85 B przed danymi; tablice orbit `$7E40–$7F3F`, ogon
192 B. Pozostałe 63 banki i RAM niebankowany identyczne z v164.
Netto vs v141: 34 305 B. Szczegóły: `V165_ORBITY_PRZY_WSADZIE.md`.
[ODCZYT] Pełne `make check`: 127 testów, 124 zaliczone,
3 pominięte (brak archiwalnego v126), 96,416 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 964 744 identyczne bajty
względem v035, cały utwór. Bez testu na fizycznym Atari.

[ODCZYT] V166: 14 rzeczywistych kompozycji pośrednich, 9 nowych póz,
w trzech późniejszych ujęciach tańca. Wstawiane w połowie odstępów między
starymi akcentami; długość, tempo, cięcia i szybki wyrzut zachowane.
Boczne ujęcie: 32 kolejne próbki obrazu/PMG/rejestrów identyczne z v165;
wszystkie sześć oryginalnych banków tańca i osiem bocznych aktorów bez zmian.
Nowe bitmapy: 16 886 B zamiast 35 840 B; dekodery/selektor podnoszą
zajętość dawnych luk bankowych do 19 021 B. Kontroler +9 B, main bez zmian,
nadal 64 banki. Znane pozostałe luki banków 31 623 B (30,88 KiB).
Walidacja: 132 testy, 129 zaliczonych, 3 pominięte (brak v126), 101,725 s.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 057 720 identycznych
bajtów względem v035, cały utwór. CPU najdroższej sprawdzonej zmiany:
91 282 cykle; nie jest to pomiar FPS ani DMA. Bez testu na fizycznym Atari.
Szczegóły: `V166_PLYNNIEJSZY_TANIEC.md`.

[ODCZYT] V171 zawierał cztery nowe klatki solówki, ale błędnie kierował
dekoder do banków 8–11, gdzie pod adresem `$5E00` znajdowała się grafika.
Wydanie nie nadawało się do odtwarzania. V172 przenosi 3805 B do ogonów
banków 32–35, z istniejącymi dekoderami. Selektor: 1370 B; wolne luki:
27 463 B. Budowa v172 powiodła się. Próba testu py65 nie wystartowała, bo
brakuje zależności `py65`; nie ma walidacji emulatorowej ani sprzętowej.
Szczegóły: `V171_DODATKOWE_KLATKI_SOLOWKI.md` i
`V172_POPRAWKA_DEKODERA_TANCA.md`.

[ODCZYT] V173 dopracowuje cztery dodatkowe pozy solówki, dopasowując je do
konkretnych faz ruchu. Timingi oraz routing banków 32–35 pozostają jak w v172.
Nowe strumienie zajmują 3945 B; potwierdzone wolne luki to 27 323 B.
Zbudowano `build/visual-prototype-v173.xex` (309 wierszy, 2552 B kodu).
Testów py65 i emulatora nie uruchomiono; py65 nie jest zainstalowany.
Szczegóły: `V173_DOPRACOWANIE_SOLOWKI.md`.

## Timeline i akty

[ODCZYT] V148 zastępuje wolne przygotowanie z v147 dynamicznym tańcem grupy
w 17950–20475. Potem pojedynczy szybki wyrzut: przykucnięcie, lot z widoku
ogólnego, cięcie do kamery z góry i zbliżenie w mniej niż sekundę. W obu
planach działają białe/cyjanowe smugi players i ruchome kreski missiles,
z bocznymi fajerwerkami. Granice aktów i ujęć głównych zachowane.
Odzysk netto w v148: 24 771 B względem v141. Szczegóły:
`V148_DYNAMICZNY_WYRZUT.md`.
Walidacja: 115 testów, 112 zaliczonych, 3 pominięte (brak v126).
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 331 536 identycznych
bajtów względem v035 przez cały utwór; bez próby na fizycznym Atari.

[ODCZYT] V147: usunięto cykliczną sekwencję przygotowania w trzecim ujęciu.
Kolejne fazy występują pojedynczo: przygotowanie, obniżenie przed wyrzutem,
wznoszenie i zatrzymane końcowe zbliżenie. Fajerwerki i moment startu lotu
pozostają z v146. Bez zmian wielkości danych, kodu i granic ujęć.
Szczegóły: `V147_JEDEN_WYRZUT.md`.
Walidacja: 114 testów, 111 zaliczonych, 3 pominięte (brak v126).
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 837 040 identycznych
bajtów względem v035 przez cały utwór; bez próby na fizycznym Atari.

| Akt / zakres z timeline’u | Status | Co mamy teraz |
|---|---|---|
| **Act 1 — School Days**, takty 0–24, ticki 0–8975 | 🟡 | Fasada ATARI ARENA zamiast szkoły, wejście dziewczyny z Fuji na plecach, ujęcia chłopca i dziewczyny, sala gimnastyczna oraz animowana piłka. Chłopiec obserwuje dziewczynę i gwiżdże; nuty/klucz wiolinowy są PMG. Brak planowanego Trevora w tle wczesnego aktu; pierwotne intro zastąpiono planszami tytułowymi. |
| **Act 2 — Crush**, takty 24–56, ticki 8975–20942 | 🟡 | W 8975–11967 boczny taniec ze szarfą: cofająca się dziewczyna, przeciwbieżny scroll sali i paralaksa podłogi. Pomponiary zachowane w osobnym projekcie. Po rotozoomerze trzy ujęcia szarf: grupa, solówka, grupa i wyrzut bohaterki. Jest 36 bazowych kompozycji (16 bocznych + 20 późniejszych) oraz 14 nowych klatek pośrednich w trzech późniejszych ujęciach; ticki akcentów i cięcia bez zmian. Podwójne bufory PMG i tęczowe iskry. Testy CPU i stereo POKEY wykonane; ocena płynności obrazu z DMA i artystyczna na docelowym sprzęcie pozostaje. |
| **Act 3 — Basketball Hero**, takty 56–64, ticki 20942–23934 | ✅ | Po niezmienionym wyrzucie 3,75 s tunelu z piłką, potem 7,5 s kozłowania i 3,75 s wsadu we wnętrzu ATARI ARENA. Animowany chłopiec, piłka i ramię; rozbicie tablicy: pęknięcie, rozpad i odłamki PMG, obracająca się tęczowa piłka oraz błysk. Tło sali przy kozłowaniu pozostaje statyczne. |
| **Act 4 — Trevor Awakens**, ticki 23934–28908 | ✅ | Ciche wejście, 13 kompletnych ciosów BUM/BAM z lotami piłek; ograniczenie do 28909 w v248 zachowuje ostatni efekt. |
| **Act 5 — montaż po Trevorze**, ticki 28909–49849 | 🟡 | Rotator/tunele i muzycznie sterowany montaż; oczy dziewczyny 39379–40126. Cztery komiksowe przebitki v257 wycofano w v260. |
| **Akty 6–7 — historyczne etykiety timeline’u** | 🟡 | Obecny build kontynuuje montaż rotatora/tuneli; nie ma w nim przebitek komiksowych ani nowej sceny konfrontacji. Granice z oryginalnej tabeli nie są bieżącym podziałem ujęć. |
| **Act 8 — Outro**, ticki 49850–59833 | 🟡 | Stały kadr chłopca, siedmiowierszowy terminal, 3 strony credits i 5 stron greetz (w tym KEY-G/FALCON), gwiazdki/nuty i końcowy fade. Próba na fizycznym Atari pozostaje. |

Intro TAME IMPALA / album title z plazmą i ditheringiem działa w tickach 0–2992 przed ujęciami szkoły. Kolory liter zmieniają się co uderzenie. V140 dodaje miasto i fajerwerki PMG; kolejność wejść na drugiej planszy to I KNOW → THE BETTER → THE LESS, z niezmienionym układem końcowym. W v140 maski chroniły litery i cienie także podczas przenikania; v149 usuwa tę ochronę na życzenie użytkownika, pokazując kompletne fajerwerki przed obrazem. To późniejszy dodatek, który zastępuje początkowe logo szkoły z timeline’u; dalszych granic nie przesunięto.

[ODCZYT] V141: oba zestawy napisów podniesiono, zachowując kolejność wejść.
Panorama zawiera pikselowego Żurawia; litery i cienie kończą się powyżej
jego najwyższego punktu. Bez nowych banków i bez dodatkowych danych Atari.

[ODCZYT] V144: Żuraw ma teraz 40×32 piksele na siatce 80×64, czyli połowę
szerokości i wysokości aktywnego obrazu. Dwie baszty, dachy i wysunięta
drewniana część według historycznej bryły; kontrast turkusu, ciepłych dachów
i czerni. Napisy są w górnej połowie, z zachowaną kolejnością wejść.
PMG omija też sylwetkę Żurawia. Bez wzrostu RAM, liczby banków i kodu 6502.
Szczegóły: `V144_DUZY_ZURAW.md`.
Walidacja końcowa: 101 testów, 98 zaliczonych, 3 pominięte (brak v126).
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 12 213 216 identycznych
bajtów względem v035 przez cały utwór. Bez próby na fizycznym Atari.

[ODCZYT] V137: scena wstęg ma rasterowy cykl tęczy oraz lecące iskry
na missiles. Podwójne bufory zachowane, bez dodatkowych banków. Pełne wyniki:
`V137_TECZOWE_SZARFY.md`.

[ODCZYT] V138: opis efektów ciosów i walidacji znajduje się
w `V138_BANG_BAM_ROZPAD.md`. V142 przenosi bitmapy szarf do banków dawnego
tańca: odzysk netto 46 633 B, nadal 64 przydzielone banki. Bieżąca mapa
w `AGENTS.md`, szczegóły i osobny projekt w `V142_SZARFY_Z_BOKU_I_ARCHIWUM_POMPONOW.md`.

[ODCZYT] V142: `make check` — 100 testów, 97 zaliczonych, 3 pominięte
(brak archiwalnego v126). Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 297 256 identycznych bajtów względem v035, cały utwór. Osobny projekt:
3/3 testy oraz 16 312 896 identycznych bajtów POKEY. Bez pomiaru FPS
z DMA ANTIC i bez próby na fizycznym Atari.

## Zadania weryfikacyjne V1–V7

[ODCZYT] V143: dziewczyna w bocznym ujęciu przechodzi z lewej na prawą
razem z szarfami i iskrami. Niezależny maskowany aktor zajmuje dodatkowe
16 KiB; obecny odzysk netto względem v141 to 29 901 B. `make check`:
101 testów, 98 zaliczonych i 3 pominięte (brak v126). Atari800 PAL/1088XE,
Altirra OS, stereo POKEY: 15 040 296 identycznych bajtów, cały utwór.
Płynność na fizycznym Atari nadal nieweryfikowana. Szczegóły w
`V143_PRZEJSCIE_Z_SZARFA.md`.

[ODCZYT] Dla roboczej zmiany aktu 5 porównanie Atari800 PAL/1088XE, stereo
POKEY z v035 dało 14 789 088 identycznych bajtów (cały utwór). Nie jest to
odsłuch ani pomiar FPS na fizycznym Atari.

| Zadanie | Status | Ustalenie |
|---|---|---|
| **V1 — profil ticka muzyki** | 🟡 | Są profile instrukcji py65 i pomiary kosztów callbacku. To nie obejmuje pełnego pomiaru cykli z DMA ANTIC ani potwierdzenia czasu linii na Atari/Altirrze. |
| **V2 — przywracanie PORTB** | ✅ | Wrapper NMI zachowuje i odtwarza bank foreground. Testy przełączeń banków i przerwań przechodzą; odtwarzanie stereo POKEY w Atari800 zgadza się z oryginałem. Nie jest to test fizycznego rozszerzenia. |
| **V3 — odczyty banków muzyki** | ✅ | Ślad dekodera i Atari800 potwierdziły 8 wymaganych banków dla v035; banki 9–14 nie są czytane przez dekoder. Po INIT te banki są wykorzystywane na wideo. |
| **V4 — pauza zatrzymuje licznik** | ⬜ | Brak dedykowanego testu START/pauza i sprawdzenia, czy `$24A7–$24A9` stoi podczas pauzy. |
| **V5 — porównanie v024/v035** | 🟡 | Potwierdzono adresy i zachowanie używanego v035. Pliku v024 nie ma w repozytorium, więc pełnego porównania obu playerów nie da się wykonać. |
| **V6 — równe odstępy DLI** | ⬜ | Produkcja zachowuje cztery ticki na klatkę w dotychczasowym układzie, ale nie ma eksperymentu przesuwającego DLI i oceny wpływu na rytm. |
| **V7 — przycięcie loadera do 7 banków** | 🚫 | Nie wykonywać według obecnego planu: dla strumienia v035 dekoder czyta znacznik końca w banku 8, więc potrzeba 8 banków. Banki 9–14 można wykorzystać dopiero po inicjalizacji, co demo już robi. |

## Pozostałe decyzje i walidacja

- ⬜ GTIA 9 w akcie 5 oraz konkretne źródła i paleta.
- ⬜ Decyzja, czy zachować UI playera; część UI/fontu jest już wyłączona, by zwolnić RAM dla scen.
- ⬜ Ustalenie zasad compo: PAL, dopuszczalny interlace/flicker, rozmiar i konfiguracja sprzętu.
- 🟡 Testy pełnego utworu i porównanie stereo POKEY wykonywane są w Atari800 PAL/1088XE z Altirra OS; potwierdzają, że wideo nie zmieniło strumienia muzyki. Nie zastępują kontroli obrazu, odsłuchu A/V na Altirrze ani próby na fizycznym Atari.
- ⬜ Walidacja na fizycznym Atari 65XE 1 MB ze stereo POKEY oraz pomiar zapasu CPU w najcięższych scenach.

Źródła statusu: `TLIKTB_Atari_Timeline_v2.md`, `TLIKTB_Technical_Constraints.md`, bieżący `README.md` oraz notatki w `docs/` (m.in. audyt banków, profil silnika i wydania V117–V125).


[ODCZYT] V174 naprawia przezroczyste/czarne plamy na szyldzie ATARI ARENA
w pierwszym ujęciu chłopca. Maska portretu wybiera teraz spójne, kolorowe
elementy postaci zamiast całego wielokąta obejmującego także tło; nuty i klucze
wiolinowe są umieszczone nad napisem. Podgląd: `build/v174-arena-sign-preview.png`.
Zbudowano `build/visual-prototype-v174.xex` (307 współdzielonych wierszy,
2552 B kodu). Bez zmian ticków i alokacji banków. Testów py65 i odtwarzania
emulatorowego nie uruchomiono. Szczegóły: `V174_CZYTELNY_SZYLD_ARENY.md`.


[ODCZYT] V175: w dymkach Trevora słowo BANG zmieniono na BNG!; co drugi
cios nadal pokazuje BAM. Zachowano szerokość efektu, animację i momenty
uderzeń. Zbudowano `build/visual-prototype-v175.xex` (307 współdzielonych
wierszy, 2552 B kodu). Nie uruchamiano testów ani emulatora. Szczegóły:
`V175_TREVOR_BNG.md`.


[ODCZYT] V176 odświeża sylwetkę dziewczyny w panoramie ATARI ARENA: nowa
grafika pokazuje ją w profilu skierowaną w lewo, w Atariowej kurtce. Postać
i tło przesuwają się teraz od prawej do lewej. Ujęcie chłopca zachowuje
winknięcie i gwizdanie z nutami. Długości, ticki i granice scen bez zmian.
Podgląd: `build/v176-arena-walk-preview.png`. Zbudowano
`build/visual-prototype-v176.xex` (307 współdzielonych wierszy, 2552 B kodu).
Nie uruchamiano testów ani emulatora. Szczegóły: `V176_SPACER_WZDLUZ_ARENY.md`.


[ODCZYT] V177 zastępuje portret chłopca, cztery klatki spaceru dziewczyny i
sześć póz koszykarza nowymi arkuszami RGBA. Maska każdej postaci pochodzi
z kanału alfa nowej grafiki; usunięto stare wielokątne maski portretu,
koszykarza i obręczy. Koszykarz i obręcz są komponowani na czystej płycie hali.
Granice, ticki, rytm kozłowania/wsadu i banki pozostają bez zmian.
Zbudowano `build/visual-prototype-v177.xex`: 292 z 309 współdzielonych
wierszy, 2552 B kodu, 10 919 B danych skanlinii. Podglądy bitmapowe:
`build/v177-opening-cast-preview.png`, `build/v177-arena-walk-preview.png`,
`build/v177-basketball-preview.png`; to nie są przechwycenia z emulatora.
Testów i odtwarzania emulatorowego nie uruchomiono. Szczegóły:
`V177_GRAFIKA_PRODUKCYJNA_POSTACI.md`.


[ODCZYT] V178 przywraca ustalone kadry otwarcia z v176: zbliżenie chłopca
po prawej oraz cztery znane skale/pozycje dziewczyny. Zachowuje czytelną
maskę portretu i poprawny szyld; nowy cykl spaceru w panoramie nadal idzie
z prawej na lewo. Nowe sześć póz koszykarza z v177 pozostaje aktywne. Ticki,
długości i przydział banków bez zmian. Podgląd:
`build/v178-opening-framing-preview.png`. Zbudowano
`build/visual-prototype-v178.xex` (307/309 wierszy, 12 084 B danych
skanlinii, 2552 B kodu). Testów i emulatora nie uruchomiono. Szczegóły:
`V178_KADRY_OTWARCIA.md`.


[ODCZYT] V179 naprawia maskę portretu chłopca: czarne piksele włosów i kurtki
wewnątrz maski sylwetki pozostają kryjące. Neutralna poza jest używana przed
przejściem dziewczyny; mrugnięcie, dziubek i nuty pojawiają się w kolejnych
ujęciach po przejściu. Ticki i granice scen bez zmian. Podgląd:
`build/v179-opening-frames.png` (kompozycja źródłowa, nie emulator).
Zbudowano `build/visual-prototype-v179.xex` (286 współdzielonych wierszy,
11 034 B danych wierszy, 2552 B kodu). Testów i emulatora nie uruchomiono.
Szczegóły: `V179_MASKA_I_REAKCJA_CHLOPCA.md`.


[ODCZYT] V180 wydłuża ujęcie tunelu w akcie 5: bananowy rotator kończy się
w takcie 92 (tick 34404), a tunel zaczyna się tam i trwa do niezmienionego
momentu kolejnej kompozycji w takcie 112 (tick 41884). Spiralna tekstura
przechodzi w radialną siatkę w takcie 108 (tick 40388), jak wcześniej.
Granice aktów, dalsze ujęcia, muzyczne ticki oraz banki bez zmian. XEX:
`build/visual-prototype-v180.xex`; 286 współdzielonych wierszy, 11 034 B
danych wierszy, 2552 B kodu. Build poprawny; testów ani emulatora nie
uruchomiono. Szczegóły: `V180_DLUZSZY_TUNEL.md`.
Ten historyczny podział czasu zastępuje harmonogram v193 opisany wyżej.


[ODCZYT] V181 przywraca boczny spacer klatka w klatkę z XEX-a v175 i dawną
kolejność kadrów spotkania. Skale postaci pozostają z v175; tor zmniejszania
dziewczyny prowadzi do lewych drzwi areny, do punktu (82,52). Uzupełniono
krycie kurtki chłopca. Sześć testów CPU/grafiki zaliczonych. Podgląd po
callbacku 6502: `build/v181-opening-preview.png`; nie jest to przechwycenie
z emulatora z DMA. Porównanie muzyki Atari800 zablokował brak FUSE dla
zainstalowanego AppImage. Banki i ticki pozostają bez zmian; 275 wierszy,
10 630 B danych wierszy, 2552 B kodu. Szczegóły:
`V181_WEJSCIE_DZIEWCZYNY_V175.md`.


[ODCZYT] V182: chłopiec patrzy przed siebie w ujęciach 2992 i 4114, ogląda
się przy mijaniu (4488) i podczas oddalania dziewczyny (4862,5236). Gwiżdże
z dziubkiem i nutami dopiero w 5610, przy dziewczynie w drzwiach. Kadry,
panorama v175 i tor wejścia z v181 bez zmian. Siedem testów CPU/grafiki
zaliczonych; 316 wierszy, 12 153 B danych, 2552 B kodu. Bez nowej walidacji
emulatorowej (znana przeszkoda FUSE). `V182_REAKCJA_CHLOPCA.md`.


[ODCZYT] V183 usuwa spłaszczone bitmapowe nuty nad areną. Od ticku 5610
nuty i klucz wiolinowy wylatują z ust na czterech players, unoszą się w górę
i w lewo, mienią kolorami i mają krótkie ślady missiles. Efekt wyłączany
przy następnym ujęciu w 5984. Podwójne bufory PMG i publikacja w blankingu.
835 B helpera w luce banku 0; 63 pozostałe banki identyczne z v182.
13 testów zaliczonych; podgląd CPU: `build/v183-whistle.gif`. Bez nowej
walidacji emulatorowej. Szczegóły: `V183_NUTY_PMG.md`.


[ODCZYT] V184 przesuwa wejście ostatniego ujęcia przy drzwiach i gwizdu PMG
o jeden beat wcześniej: tick 5516 zamiast 5610 (94 ticki, około 0,47 s).
Dziubek i pierwsza nuta startują razem. Wspólna stała WHISTLE_START; koniec
ujęcia i początek kozłowania w 5984 bez zmian.
`V184_WCZESNIEJSZY_GWIZD.md`.


[ODCZYT] V185: gwizd i nuty zaczynają się w 4862, po mijaniu w pierwszym
planie, i trwają do 5984 (około 5,6 s). Etapy oddalania dziewczyny zachowują
oryginalne ticki; ostatnia pozycja przy drzwiach ponownie w 5610. Nuty
unoszą się wolniej (jedna faza na osiem ticków), pozostając czytelne dłużej.
14 testów zaliczonych. Podgląd CPU: `build/v185-whistle.gif`. Bez nowego
odtwarzania emulatorowego. Szczegóły: `V185_DLUZSZA_MELODIA.md`.


[ODCZYT] V186: dziubek i pierwsza nuta razem w 4862; gwizd i melodia
kończą się przy dojściu dziewczyny do drzwi w 5610. Dwie skończone fale
nut/kluczy PMG mają odrębne krzywe lotu, ślady i wygaszanie. Poprawiony
rysunek ust, usunięte resztki starych promieni przy twarzy; kadry i tor
dziewczyny zachowane. 15 testów sceny i piłki zaliczonych. Porównanie
całego utworu w Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 6 220 440
identycznych bajtów z v035. Podgląd CPU: `build/v186-encounter.gif`.
Pełny zestaw i starsze rozbieżności: `V186_DOMKNIETA_SCENA_SPOTKANIA.md`.


[ODCZYT] V187 powiększa nuty PMG dwukrotnie w obu osiach, utrzymuje pełną
jasność prawie przez cały lot, przeplata kolory białymi błyskami oraz poszerza
ślady missiles. Tory szerzej rozchodzą się po niebie. Synchronizacja ust
i końca przy drzwiach oraz kadry bez zmian. 16 testów zaliczonych.
Podgląd: `build/v187-whistle.gif`. `V187_DUZE_NUTY_PMG.md`.

[ODCZYT] V187: porównanie całego utworu w Atari800 PAL/1088XE, stereo
POKEY — 16 221 456 identycznych bajtów z v035. Pozostałe 63 banki identyczne
z v186; zmiana ograniczona do banku 0 i sterowania wielkością/barwami PMG.


[ODCZYT] V188 naprawia wyłączanie GRACTL/DMACTL przed przygotowaniem PMG
w scenach 10–11. Poprzednio nuty znikały na 267–313 linii ekranu na każdej
aktualizacji. Teraz front pozostaje aktywny do publikacji gotowego bufora.
Regresja z poruszającym się rastrem i opóźnieniami potwierdza brak przerw
(48 przypadków). 19 testów ukierunkowanych zaliczonych. Atari800 PAL/1088XE,
stereo POKEY: 16 336 440 bajtów identycznych z v035, cały utwór. Main
2560 B — bez zapasu przed $1E00. `V188_CIAGLE_PMG_BEZ_STROBO.md`.


[ODCZYT] V189 odtwarza osiem póz koszykarza, kozłowanie, wsad i trzy fazy
rozbicia tablicy bezpośrednio z v175. Przywrócone cztery różne fazy ręki
usuwają powielenia i błędne łaty nowych póz v177. Wszystkie klatki kluczowe,
rysunek i położenie tablicy oraz trajektorie piłki zachowują zgodność z v175.
Zmienił się tylko bank 1; poprawki nut v188 pozostają. 23 testy ukierunkowane
zaliczone, w tym porównanie działających klatek i PMG z archiwalnym v175.
Cały utwór w Atari800: 14 992 848 identycznych bajtów stereo POKEY z v035.
Podgląd: `build/v189-basketball.gif`. `V189_KOSZYKOWKA_I_TABLICA_V175.md`.

[ODCZYT] Pełny `make check` v189: 144 testy, 135 zaliczonych,
6 niezaliczonych, 3 pominięte (brak v126). Zniknęły wszystkie cztery
wcześniejsze błędy testów koszykówki. Pozostałe są opisane w raporcie v189.

[ODCZYT] V190: Trevor pokazuje BUM/BAM, a ostatnia tekstura tunelu
(klatki 48–63) ma organiczne falujące pasma. Timing, piłka i przydział
pamięci zachowane. `V190_BUM_I_ORGANICZNY_TUNEL.md`.

[ODCZYT] V191 centruje BUM/BAM w dymku i dodaje ograniczony pseudolosowy
rozrzut wokół właściwej pięści: ±6 pikseli X i ±6 linii ekranu Y. Pozycja
stała przez cały cios, wspólna dla tekstu i dymka. 24 testy zaliczone; cały
utwór stereo POKEY identyczny z v035 (16 037 712 B).
`V191_DYMKI_PRZY_PIESCI.md`.

[ODCZYT] V192 zmienia U w BUM na odwrócone pionowo A z BAM bez poprzeczki.
Zachowane centrowanie, rozrzut przy pięściach i rozmiary danych.
`V192_U_Z_ODWROCONEGO_A.md`.

[ODCZYT] V193 wydłuża bananowy rotator z taktów 88–92 do 88–96
(32909–35900), dzięki czemu odtwarza obie połowy istniejącego cyklu.
Tunel zaczyna się w 35900; zmiana organicznej tekstury przy 40388 oraz
granice ujęć w 41884 i 43379 pozostają bez zmian. Kadr leżącego chłopca
zaczyna się pod credits/greetz w takcie 144 (53850); pełny finał w 59085
pozostaje. Zmieniono wyłącznie timing, bez zmian grafiki i procedur efektów.

[ODCZYT] V194 lokalizuje i usuwa błysk rotatora trwający 100 ticków (ok.
0,5 s) przy wejściu w placeholderowy cykl po takcie 112. W ticku 41884
globalna faza zaczynała od bananów i przechodziła do tunelu w 41984.
Dispatcher trzyma organiczny tunel do 41983, po czym cykl startuje od
spiralnego tunelu. 10 testów granic scen, motywów i finału zaliczonych.

[ODCZYT] V196 centruje piłkę pod dłonią (X=84 zamiast 97) i wspólnie
animuje ramię oraz piłkę w rytmie 94 + 94 + 186 ticków. Wsad i tablica
z v175 zachowane; 21 testów zaliczonych. Dithering v195 wycofany.
`V196_KOZLY_DWA_SZYBKIE_JEDEN_WOLNY.md`.

V197: finałowy chłopiec ma naprzemiennie gwiazdki i nuty/klucz wiolinowy z początku, co 256 ticków. Ta sama orbita, kolory i wygaszenie; +140 B w banku 49. Szczegóły: `V197_NUTKI_W_FINALE.md`.

V198: 19 nasyconych kolorów GTIA cyklicznie barwi orbitujące gwiazdki i symbole melodii; cztery duszki mają przesunięte fazy. Bez zmian orbity, czasu i zajętości pamięci. Szczegóły: `V198_TECZOWE_KOLORY_FINALE.md`.

## V216 — credits i greetz

W v216 credits zajmowały 53850–56842, a greetz 56842–59085; był to
historyczny rozkład czasu, później przesunięty przez v240 i v248. Pełny chłopiec
i PMG zachowane, od 59085 wraca stary finał. Brak nowych banków.
Zasoby 1738 B + loader 364 B w lukach podstawowej pamięci. Prywatny DL
`$BC00` zachowuje muzyczne DLI co 78 linii. Patrz `V216_CREDITS_GREETZ.md`.

[ODCZYT] V216: 154/154 testy, bez pominięć. Atari800 PAL/1088XE, stereo:
9 791 424 identyczne bajty POKEY względem v035, cały utwór. Ponowny build
identyczny bajtowo; wszystkie banki poza blokiem kontrolera finału zgodne
z v198.

V218: jedna niższa pozycja chłopca od 53850 do fade, również po 59085.
Zielony terminal z `>`, puste górne wiersze po greetz; usunięte górne linie.
Patrz `V218_STALY_KADR_TERMINAL.md`.

V222: właściwe pisanie terminala znak po znaku, migający kursor za tekstem,
Entery i scroll historii pięciu wierszy. Stały dolny kadr zachowany.
158 testów w pełnym przebiegu v221; 44 testy dopracowanej v222 oraz cały
utwór stereo w Atari800 zaliczone. `V222_TERMINAL_PISANIE.md`.

V225: zielone litery ANTIC 4 na czarnym tle, przełączenie palety z DLI
bez piątego ticka muzyki; brak zapisów terminala do koloru skóry. Wejście
Trevora używa palety bitki `$48/$68/$2A`. 47 testów i pełne stereo Atari800
zaliczone. `V225_PALETY_TERMINAL_I_TREVOR.md`.

V227: usunięte rozdwojenie PMG finału — prawidłowy cień PMBASE i kompletne
maski na docelowej wysokości przed publikacją. Test sprzętowego odczytu
write-only odtwarza błąd v225 i przechodzi na v227.

V230: stały kolumnowy terminal, 6 wierszy (status + 5 historii), jaśniejsza
zieleń i rzadki glitch wyłącznie tekstu; poprawione wszystkie chwyty szarf
ujęć solo/trio i dodatkowych klatek. Kadr chłopca i zegar muzyki zachowane.
`V230_TERMINAL_I_CHWYTY_SZARF.md`.

V231: montaż po Trevorze przeplata istniejące dwa tunele, odwraca kierunek
i wprowadza przyspieszenia 2× w rytmie półtaktów oraz krótkich zakończeń fraz.
W v231 dotyczyło okien 41984–53849; v248 przesunęło montaż i wejście finału.
Bez nowych bitmap/banków w v231; główny kod 2524 B, director
337 B w pamięci podstawowej. 38 testów ukierunkowanych i pełne porównanie
stereo Atari800 zaliczone. `V231_DYNAMICZNY_TUNEL_PO_TREVORZE.md`.

[ODCZYT] Regresja v231: 167/168 w pełnym przebiegu; po dostosowaniu
testu wyboru 64 klatek do nowego montażu moduł mosaic zalicza 4/4.
Wszystkie 168 przypadków zweryfikowane, XEX bez dalszych zmian.

V233: pojedyncze oczko i buziak w istniejących fazach zbliżenia wyrzutu,
następnie ośmiofazowe serce PMG z różowym przodem, białym połyskiem
i fioletową głębią. Start przy ustach 20662, koniec sceny nadal 20942;
wszystkie cztery missile trails pozostają. 992 B wykorzystanej końcówki
banku tańca, 5152 B pozostałych końcówek. Bez nowych banków i bitmap.
`V233_OCZKO_BUZIAK_SERCE.md`.

[ODCZYT] V233: 172/172 testy, 118,6 s; Atari800 PAL/1088XE, cały utwór
stereo — 11 608 128 bajtów identycznych z v035. Build roboczy zgodny z v233.

V234: siedem wierszy terminala (status + sześć historii), dodatkowy wiersz
pozostawia widoczną wcześniejszą linię greetz. Zastępuje wyłącznie kolejne
8 czarnych linii bitmapy; chłopiec i orbita zachowują położenie. Bez zmiany
tekstów i ich ticków; muzyczne DLI nadal 1/79/157/235, split palety teraz 57.
46 testów ukierunkowanych i cały utwór stereo Atari800 zaliczone.
`V234_SIODMY_WIERSZ_TERMINALA.md`.

[ODCZYT] V234: 173/173 testy, 119,4 s. Build roboczy zgodny z v234.

V235: dopisane `HUMAN VISION / LLM CODE` oraz `AI TOOLS / ATARI SOUL`
w istniejących planszach credits. Pierwsza wykorzystuje szósty wiersz
historii. Greetz, kadr i granice scen zachowane. 1795 B zasobów po kompresji;
dodatkowe 12 B w wyłączonym UI, bez luk banków rozszerzenia.
`V235_LLM_AI_W_CREDITS.md`.

[ODCZYT] V235: 174/174 testy, 118,6 s; pełny utwór stereo Atari800
zgodny z v035 (10 847 448 B). Build roboczy zgodny z v235.

V236: naprawiony niepełny obrót bananów. Generator 32 klatek obejmuje
360° zamiast 90°, a akt 5 nie resetuje już osobno połówek 0–15 i 16–31
ani nie wymusza zmiany fazy w 34404. Timeline, kafel bananów, paleta,
piłka i tunele zachowane. Main 2521 B, bez nowych banków. 44 testy
ukierunkowane i pełne stereo Atari800 zaliczone.
`V236_PELNY_OBROT_BANANOW.md`.

[ODCZYT] V236: 174 dotychczasowe testy zaliczone w pełnym przebiegu;
po naprawie importu nowego modułu jego osobne discovery zalicza 3/3.
Łącznie 177 przypadków zweryfikowanych; build roboczy zgodny z v236.

V239: kiść i pojedynczy banan obrany do połowy pojawiają się wymiennie,
co drugie wejście bananowego rotatora. Oba mają pełne 32-klatkowe obroty.
Dwa komplety mieszczą się po RLE w tych samych 8 bankach, zostawiając
9910 B luk; bez użycia rezerwy innych banków. Main nadal 2521 B.
Cały utwór stereo Atari800 zgodny z v035; tunele identyczne bajtowo.
`V239_KISC_I_OBRANY_BANAN.md`.

[ODCZYT] V239: 181/181 testów, 133,7 s; cały utwór stereo Atari800
zgodny z v035 (11 570 400 B). Build roboczy zgodny z v239.

V240: terminal i leżący chłopiec od 51850, około 10 s wcześniej.
Osiem plansz (3 credits + 5 akapitów greetz): szybkie wpisanie wszystkich
wierszy i pauzy ponad 3 s. Prompt `>_`, podkreślnik miga także w czasie
pisania. Zakończenie tekstu 59085 i fade zachowane; wszystkie 64 banki
identyczne z v239. 59 testów ukierunkowanych i cały utwór stereo Atari800
zaliczone. `V240_WCZESNIEJSZY_TERMINAL_I_PLANSZE.md`.

[ODCZYT] V240: 183/183 testy, 133,5 s; cały utwór stereo Atari800
zgodny z v035 (11 175 336 B). Build roboczy zgodny z v240.

V241: usunięte rozpakowywanie RLE obu bananów. Symetryczne pary owoców
pozwalają przechować surowe półobroty i odtworzyć 32 próbki kątowe bez
skoku; zmienia się układ tła i częstotliwość zoomu. Koszt kolejnej klatki
około 47 tys. cykli, na poziomie tuneli. W tych samych 8 bankach zostaje
344 B (zamiast wcześniejszych 9910 B). Terminal i timeline zachowane.
`V241_SZYBKIE_BANANY_BEZ_RLE.md`.

[ODCZYT] V241: 184/184 testy, 123,5 s; cały utwór stereo Atari800
zgodny z v035 (11 610 936 B). Build roboczy zgodny z v241.

V242: naprawione miganie leżącego chłopca między niższym i starszym wyższym
kadrem. Guard przywracania normalnej display listy używa teraz aktualnego
outro_text.START (51850), zamiast starego 53850. Test kolejnych callbacków
odtwarza błąd v241 i potwierdza brak przełączeń w v242.
`V242_STALY_KADR_BEZ_RESETOW.md`.

[ODCZYT] V242: 185/185 testów, 122,9 s; cały utwór stereo Atari800
zgodny z v035 (10 731 888 B). Tylko 2 zmienione bajty XEX względem v241.


V243: przywrócone gęste rozmieszczenie bananów sprzed v241: wszystkie
64 bitmapy identyczne z v240, pełne 32 fazy obu motywów i dotychczasowy zegar.
Przyspieszenie dotyczy dekodera RLE, bez zmiany wzoru. Najdroższy rozgrzany
callback: kiść 75139 zamiast 78748 cykli, obrany 72819 zamiast 78599.
To odpowiednio 4,6% i 7,4% mniej CPU; nadal drożej od surowego tunelu
(47233 cykle). To pomiar CPU bez ANTIC DMA, nie deklaracja FPS.
Te same osiem banków; 3755 B wolnego. Pozostałe banki i naprawa finału v242
pozostają identyczne. `V243_GESTE_BANANY_SZYBSZY_DEKODER.md`.

[ODCZYT] `make check PYTHON=/tmp/finale197-venv/bin/python`: **186/186
testów**, bez pominięć, 137,5 s. Cały utwór Atari800 stereo: 11376072
identycznych bajtów względem v035. Build roboczy zgodny z v243.


V244: oba banany odtwarzane bez RLE po przygotowaniu w tle. Banki planszy
tytułowej 40–48 są używane ponownie po zakończeniu tytułu; liczba fizycznych
banków nadal 64. Właściwe klatki, zoom, palety, piłka i ticki pozostają.
[ODCZYT] Atari800 PAL/1088XE: cache gotowy w ticku 8609, przed pierwszym
wyborem renderera w ticku 11976. Granica okna Act 2B pozostaje w ticku
11968 (bar 32); 11976 to pierwszy zmierzony wybór rotatora/tunelu w callbacku.
Odczyt kolejnych faz: 63 przejścia kiści i 38 obranego, wszystkie o jeden krok,
bez pominięcia. Rozgrzany callback: 47323/47402
cykle wobec tunelu 47245. Muzyka stereo: 10589472 identyczne bajty z v035.
`V244_SUROWE_BANANY_I_BANKI_PO_TYTULE.md`.

[ODCZYT] `make check PYTHON=/tmp/finale197-venv/bin/python`: **189/189
testów**, bez pominięć, 151,2 s. Build roboczy i v244 identyczne.

V251 poprawia czytelność orbit finałowych. V250 zmieniał głównie promień,
przez co tor nadal wyglądał niemal jak okrąg. Każda nowa linia tekstu wybiera
teraz elipsę o innym mimośrodzie i nachyleniu; przejście zmienia pozycję
każdego duszka najwyżej o 4 piksele na krok co 16 ticków. Rytm tekstu, scena,
kolory i fade pozostają bez zmian. Szczegóły: `V251_WIDOCZNE_ZMIANY_ORBITY.md`.

[ODCZYT] V253: `make check` 196/196, bez pominięć. Porównanie całego
utworu stereo w Atari800 zgodne z v035 (16 080 048 bajtów). Ekran
ładowania nie był wizualnie obserwowany w emulatorze ani na sprzęcie.

[ODCZYT] V257: 203/203 testy bez pominięć; cały utwór stereo POKEY w
Atari800 zgodny z v035 (16 377 408 bajtów). Gotowości na sprzęcie nie
potwierdzono.

V258 zmienia podpis ekranu ładowania na `AI-SLOP/OGNJEN`. V259 zastąpiło
szachownicę Trevora pojedynczym zbliżeniem; v260 wycofało wszystkie cztery
komiksowe przebitki i przywróciło ruchomy montaż v256. Oczy dziewczyny,
walka, ticki i finał pozostają. Pełne `make check` v260: 199/199; Atari800
PAL/1088XE, Altirra OS, stereo POKEY: 16 272 720 identycznych bajtów z v035.
Testy CPU nie potwierdzają DMA/FPS ani działania na sprzęcie.
`V260_ROTATORY_BEZ_TREVORA.md`.

V261 dodaje KEY-G i FALCON do dwóch istniejących wierszy greetz, zachowując
FOORMAN, liczbę stron i harmonogram. `build/visual-prototype-v261.xex` oraz
`releases/less-i-know-demo-release-008.xex` są identyczne (SHA-256
`fff207ea35990a0d4694e1e510f4c785fa43a7c06d3d2010733c2165b8a6d836`).
Pełne `make check`: 199/199, 152,147 s. Nie powtórzono odtworzenia w Atari800
po tej zmianie tekstu ani próby fizycznej. Katalog
`releases/less-i-know-sv2026we-v260-candidate/` (nieśledzony) oraz
`releases/less-i-know-sv2026we-v260-candidate.zip` są starszymi artefaktami
v260/release 007; nie są pakietem release 008 i pozostały nietknięte.

### Uruchomienie przez AVG na fizycznym Atari — 2026-11-12

[ODCZYT użytkownika] Na Atari z rozszerzeniem 1088 Rambo, ładowanym przez
AVG, obie ostatnie wersje diagnostyczne pełnego dema wystartowały:
`releases/avg-compact-late-start-001.xex` oraz
`releases/avg-final-segment-trace-001.xex`.

[ODCZYT] Te pliki są mniejsze niż 1 MiB. Dane 64 banków wariantu
kompaktowego odtworzono bajt w bajt względem poprzedniego obrazu; pełne
porównanie stereo POKEY w Atari800 przeszło dla obu wariantów. Dane niskiej
pamięci są ładowane do bufora i kopiowane w ostatnim INIT, po czym następuje
bezpośredni skok do playera. Szczegóły: `V273_START_AVG_RAMBO.md`.

[OGRANICZENIE] Potwierdzono start, nie pełny przebieg, płynność, odsłuch na
sprzęcie ani gotowość konkursową. Wariant mono oraz wcześniejsze pliki release
nie zostały objęte tym potwierdzeniem. Dokładna przyczyna wcześniejszej awarii
nie została rozstrzygnięta; limit rozmiaru i kolizja loadera pozostają
hipotezami.

V275 rozjaśnia palety scen fabularnych i nadaje obu wariantom bananów żółte
odcienie PAL. Release 013 stereo używa kompaktowego loadera z późnym startem.
Pełna muzyka stereo sprawdzona w Atari800; dalsze buildy tylko stereo.
Wizualna ocena nowej palety i start release 013 na Atari pozostają do próby.
Szczegóły: `V275_SOCZYSTE_PALETY.md`.

V277 wzmacnia wizualnie kolory rotatorów przez dobór jasności i kontrastu;
spotkanie przed areną (sceny 8–12) ma nową, cieplejszą paletę. Stereo
release 015 używa kompaktowego loadera AVG z późnym startem. Ocena kolorów
i tego builda na fizycznym Atari pozostaje do wykonania. Zob. `V277_PALETY_ARENA_ROTATORY.md`.

V278 przywraca chłopca z sześciu póz v177 w kozłowaniu i wsadzie, z pełnymi
klatkami ruchu zamiast dawnych zbyt małych łat. Osobne łaty rozbicia tablicy
uwzględniają nową postać. Stereo release 016 ma kompaktowy loader AVG;
ocena obrazu i płynności na fizycznym Atari pozostaje do wykonania. Zob.
`V278_KOSZYKARZ_V177.md`.

V280 poprawia proporcje sześciu póz koszykarza v177, ustawienie na parkiecie,
etapy wyskoku i tor piłki względem dłoni. Stereo release 017 korzysta z
kompaktowego loadera AVG; sprawdzenie animacji na Atari pozostaje do wykonania.
Szczegóły: `V280_PILKA_I_PROPORCJE_KOSZYKARZA.md`.

V281 przywraca pozy, klatki kluczowe i tor piłki koszykarza z release 001;
poprawia wycieki fioletowego tła wokół nóg, w tym w łatach kozłowania.
Stereo release 018 korzysta z kompaktowego loadera AVG. Ocena i odsłuch tego
buildu na fizycznym Atari pozostają do wykonania. Szczegóły:
`V281_KOSZYKOWKA_RELEASE001_MASKI.md`.

V282 stosuje paletę z referencji do całej pierwszej sekwencji szkolnej, ociepla
i przyciemnia sceny w hali, a ekranowi ładowania nadaje granatowe tło i
brzoskwiniowy tekst z informacją o produkcji. Komunikat o ładowaniu banków
pozostaje. Stereo release 019 ma 935 281 B i używa kompaktowego loadera AVG.
Sprawdzono podglądy rendererem; nie uruchamiano testów ani Atari800 i nie
sprawdzono go na fizycznym Atari. Szczegóły: `V282_PALETA_SCEN_I_EKRAN_LADOWANIA.md`.

V283 dopisuje `WE` po `2026` na ekranie ładowania, skracając `PRODUCED` do
`PROD.` tak, aby zachować tekst w limicie 40 znaków. Stereo release 020 ma
935 281 B; w gotowym XEX potwierdzono wiersz `PROD. BY OGNJEN / SILLY VENTURE 2026 WE`.
Nie uruchamiano testów ani fizycznego Atari.

V284 usuwa zaznaczone przez użytkownika tło zza ramienia i drobny fragment
przy twarzy w pozycji kozłowania; korekta obejmuje też łaty ruchomej ręki.
Stereo release 021 używa kompaktowego loadera AVG. Trzy testy porównania z
release 001 przeszły; build nie był sprawdzony na fizycznym Atari.

V285 uzupełnia brakujące piksele kolana w pozycji kozłowania i jej trzech
łatach ręki. Ubytek występował w grafice release 001, a maska stykała się z
jego krawędzią. Stereo release 022 używa kompaktowego loadera AVG; trzy testy
porównania z release 001 przeszły. Brak próby na fizycznym Atari.

V286 naprawia regresję v282: przywraca pierwotne przypisanie pikseli grafiki
szkolnej, zachowując paletę GTIA. Klatki sceny szkolnej w siedmiu punktach
mają identyczne indeksy pikseli jak v281; testy szkoły 4/4 i koszykówki 3/3.
Stereo release 023 dla AVG nie był sprawdzony na fizycznym Atari.

V287 dodaje oko, nos i usta dziewczyny do wszystkich 18 klatek spaceru przed
areną. Detale przesuwają się razem z postacią; pozostałe piksele klatek są
zgodne z zachowaną grafiką. Stereo release 024 dla AVG; testy panoramy 4/4.
Brak próby na fizycznym Atari.

V288 powiększa rysy dziewczyny we wszystkich klatkach spaceru i dodaje
wyraźną otwartą paszczę Trevorowi w obu pozach ciosu oraz ich odbiciach.
Stereo release 025 dla AVG; testy panoramy 4/4 i Trevora 13/13. Brak próby
na fizycznym Atari.

V291 wzmacnia satelity po BUM/BAM: większy kształt, wolniejszy odlot,
kolory oparte na cyklu dymków v215 i dłuższe wygaszanie. Nadlatująca
kolejna piłka ma pierwszeństwo, dlatego przy krótkich odstępach odlot
poprzedniej kończy się wcześniej. Paleta samego dymka odpowiadała już v215.
Stereo release 028 dla AVG; testy uderzeń 9/9. Brak próby na fizycznym Atari.
Release 026 był pośredni i ma błąd nakładania lotów; nie używać go.

V292 usuwa dużą paszczę dorysowaną w v288 i uzupełnia po kilka pikseli
środka oryginalnej linii ust w obu pozach ciosu. Stereo release 029 dla AVG;
testy uderzeń 9/9. Brak próby na fizycznym Atari.

V293 upraszcza tempo późnych rotatorów w nawiązaniu do v215: normalna prędkość,
dłuższe przejścia do przodu i czterotaktowe cofnięcia, przy zachowaniu
dodatkowych tekstur i okna oczu. Portret oczu ma jasne włosy, paletę skóry,
białka i spojrzenie w górę, nawiązując do dziewczyny spod areny. Stereo
release 030 dla AVG; testy montażu, oczu, palet i rastra 8/8. Podgląd
callbacku obejrzany; Atari800: 15 116 112 identycznych bajtów stereo POKEY
względem v035. Brak oceny płynności i kolorów na fizycznym Atari.

V294 przyciemnia i ociepla całą sekwencję szarf i wyrzutu, a szarfom nadaje
intensywniejszy cykl barw. Stereo release 031 dla AVG; testy sceny 27/27,
Atari800 stereo POKEY zgodny z v035. Szczegóły: `V294_SZARFY_CIEPLA_PALETA.md`.
