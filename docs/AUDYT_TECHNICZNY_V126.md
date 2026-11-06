# Audyt techniczny i wydajności v126 — 2026-11-06

Zakres: aktualny silnik `lessIknow-thebetter`, generator XEX, efekty, bankowanie, testy i proces budowania. Osobny silnik 3D z katalogu nadrzędnego oraz projekt muzyczny `impala-lessIknow` nie są objęte tym pomiarem. Nie zmieniono kodu produkcyjnego, granic scen ani ticków.

Wniosek: architektura chroni muzykę i aktywny obraz, ale koszt aktualizacji grafiki jest wysoki. Największy potencjał to usunięcie pracy wykonywanej ponownie dla niezmiennych danych: display list, rozszerzania portretów, kompozycji plazmy i szerokich kopii pozy. Nie ma podstaw do stwierdzenia, że całość spełnia budżet 50 Hz. Również przekroczenie pojedynczej ramki nie oznacza automatycznie błędu: animacje mają rzadsze fazy, a muzyka działa niezależnie.

## Weryfikacja

[ODCZYT] 80 testów w py65 1.2.0, 79 OK, 1 FAIL, czas 79,768 s. Błąd `tests/test_mosaic.py:49–55`: test oczekuje pozy tańca z `tick >> 5`, silnik i pozostałe testy używają `tick >> 4`. Pierwsza rozbieżność: 5 zamiast 3. To niespójne oczekiwanie testu; nie dowód uszkodzonego przejścia. Ponieważ test zatrzymuje się na pierwszej asercji, dalsze przejścia w tej konkretnej metodzie nie są sprawdzone.

[ODCZYT] Rebuild do `/tmp/atari-audit-v126.xex` identyczny z dostarczonym v126:
`06b97337f904bff25a271f299bb440ff645b092414a2395866683eaf69c04da1` (SHA-256).

[ODCZYT] `tools/check_playback.py --seconds 12`: PASS, 3 631 536 identycznych bajtów stereo POKEY, około 1011,6 s emulacji, cały utwór. Atari800, PAL, 1088XE, Altirra OS, uruchomienie bez obrazu i dźwięku. To potwierdza zgodność strumienia rejestrów w tej konfiguracji; nie stanowi odsłuchu ani pomiaru równomierności przerwań na fizycznym sprzęcie.

## Pomiary kosztu callbacku

[ODCZYT] `tools/profile_engine.py`, dane `docs/AUDIT_V126_CYCLES.json`. 589 wywołań: kolejne ticki co 4 wewnątrz każdego badanego fragmentu, nowy CPU na początek fragmentu. Koszt obejmuje pierwsze napełnienia oraz trafienia cache. Harness z `tests/test_sequence.py` ustawia stale VCOUNT=124 i nie uruchamia DMA ani NMI. Próbkowanie nie odtwarza rzeczywistego upływu czasu podczas renderowania, nie jest pełnym przebiegiem utworu ani pomiarem FPS. Maksima dotyczą wyłącznie tych próbek.

| Fragment, ticki (koniec wyłączny) | Mediana cykli | Maksimum | Wywołania >35 568 / próbki |
|---|---:|---:|---:|
| Intro, 0–100 | 1 325 | 114 773 | 4/25 |
| Tytuł, 1496–1596 | 1 089 | 120 904 | 4/25 |
| Szkoła, 2992–3092 | 649 | 17 416 | 0/25 |
| Parallax, 3553–3853 | 5 978 | 53 684 | 10/75 |
| Trening, 6000–6100 | 594 | 93 168 | 1/25 |
| Taniec solo, 9216–9472 | 1 157 | 92 904 | 16/64 |
| Mozaika, 12000–12300 | 8 038 | 73 698 | 19/75 |
| Portret, 18000–18100 | 5 739 | 130 470 | 1/25 |
| Koszykarz, 21000–21300 | 6 611 | 66 049 | 2/75 |
| Trevor, 27000–27300 | 7 816 | 55 496 | 15/75 |
| Późna mozaika, 59000–59300 | 12 718 | 78 378 | 20/75 |

[WNIOSEK] 312 linii × 114 cykli = 35 568 cykli na ramkę PAL przed DMA. Aktualizacja tytułu zajmuje do 3,4 takich ramek samego CPU. Dobre mediany wynikają z cache; nie opisują kosztu zmiany fazy. Potrzebny jest pomiar czasu od pobrania ticka do pokazania obrazu oraz liczby pominiętych faz. Nie należy przeliczać tej tabeli wprost na rzeczywisty FPS.

## Najważniejsze usprawnienia

### 1. Stałe display listy są budowane ponownie — wysoki priorytet

[ODCZYT] `mosaic.py:83–88`, `school_parallax.py:64–69`, `trevor_polished.py:190–195`, `basketball_hero.py:184–193`: przy zmianie obrazu kod ponownie wpisuje adresy dla 192 linii. Każdy wiersz dodatkowo modyfikuje operandy dwóch instrukcji zapisu przez dodawanie 3 i obsługę przeniesienia. Geometria jest stała w obrębie danego trybu sceny.

[ZAŁOŻENIE] Jednorazowa inicjalizacja obu DL dla danego układu i baz $9000/$B000 powinna usunąć kilkanaście do około 20 tys. cykli na zmianę obrazu. To szacunek z instrukcji, nie benchmark poprawionej wersji. Należy przechowywać osobny identyfikator układu dla każdej DL i zachować bity DLI, LMS i końcowy skok. Lista może zostać nadpisana przez inną scenę; inicjalizacja tylko raz od startu programu byłaby błędna.

### 2. Portrety są rozszerzane w czasie odtwarzania — wysoki priorytet

[ODCZYT] `crush_portraits.py:37–49`: dla każdego bajtu źródła wykonywane są dwa odczyty, rozpakowanie półbajtów, lookup rozszerzenia i aktualizacje czterech operandów samomodyfikującego się kodu. Maksimum całego callbacku: 130 470 cykli.

[WNIOSEK] Przygotować portrety w końcowym formacie 160×52 już podczas budowania lub INIT, potem kopiować zwykłym blokiem. Cztery obrazy wymagają 8320 B zamiast 4160 B, czyli dodatkowe 4160 B. W obecnym miejscu banku muzyki nie należy zakładać, że się zmieszczą: użyć sprawdzonego wolnego obszaru/banku albo rozwinąć je przed sceną. Zysk wymaga benchmarku; dokładanie RAM jest tu sensowniejsze od mikrooptymalizacji pojedynczego przesunięcia.

### 3. Kopie bankowane mają wolną pętlę bajtową — wysoki priorytet

[ODCZYT] `mosaic.py:80–82`, `school_parallax.py:61–63`, `trevor_polished.py:187–189`: LDA abs,Y; STA abs,Y; INY; BNE, około 14 cykli/bajt bez dodatkowych page-crossing. Sama kopia mozaiki 3840 B kosztuje około 54 tys. cykli. Niektóre klatki zaczynają się od niezerowych młodszych adresów, więc dochodzi koszt przekroczenia stron przy odczycie.

[WNIOSEK] Zastosować częściowo rozwinięte kopie kilku stron na jeden indeks, analogicznie do `engine_effects.copy_helper`. Para LDA/STA to 9 cykli/bajt, a koszt pętli można amortyzować. Potencjał około 30–35% samej kopii, nie całego callbacku. Kod musi wykonywać się poza zmienianym oknem i nie nadpisywać pomocników $AF00/$CF00. Dodatkowo w `basketball_hero.py:166` ogon 192 B używa JSR/RTS na każdy bajt: sam narzut tych wywołań to 2304 cykle, które można usunąć przez lokalną pętlę inline.

### 4. Taniec kopiuje zbyt szeroki obszar — wysoki priorytet

[ODCZYT] `build_bitmap_sequence.py:420–482`, `engine_effects.py:8–31`: po rozgrzaniu buforów nadal kopiowane jest 5376 B (21 pełnych stron), także dla solo. Pełne napełnienie to 7936 B. Istnieje poprawna kontrola zawartości obu buforów.

[WNIOSEK] Wygenerować podczas budowania listy zmienionych odcinków wierszy, osobno dla solo/duo/trio i pary poprzednia→nowa poza. Kopiować prostokąty lub runy, zamiast wszystkich kolumn szerokiego pasa. Zachować pełną ścieżkę przy wejściu z innej sceny. Różnica musi odnosić się do zawartości bufora docelowego, nie ostatniej pokazanej klatki. Zysk zależy od liczby runów i narzutu; wymaga pomiaru, szczególnie dla trio.

### 5. Plazma wykonuje kilka pełnych przebiegów — średni/wysoki priorytet

[ODCZYT] `title_plasma.py:263–335`: przy zmianie maski kopiuje 2560 B do cache, potem składa 2560 B z maską i kolorem. Fade dodaje kolejny pełny odczyt/maskowanie/zapis. Cache i rozwinięcie stron już istnieją, więc nie jest to naiwny renderer bez optymalizacji.

[WNIOSEK] Pierwszy krok: zlać fade z kompozycją, aby nie czytać i zapisywać wyniku ponownie, jeśli pozwoli układ banków. Dalej rozważyć gotowe klatki dla najdroższych przejść i ich dokładnych kombinacji faz. Nie zakładać, że wszystkie kombinacje masek, plazmy, kolorów i fade zmieszczą się w zwolnionych 48 640 B opisanych w V120; potrzebna jest tabela rzeczywiście osiągalnych stanów. Samo przeniesienie kolejnych instrukcji do tablic bez redukcji przebiegów da mniejszy efekt.

### 6. Mozaika robi coraz droższe modulo — średni priorytet

[ODCZYT] `mosaic.py:95–104`: wyznacza fazę co wywołanie przez odejmowanie 187 aż do zejścia poniżej 187. Przy ticku 59000 to około 139 iteracji od bazy 32912. Koszt rośnie z upływem sceny także przy trafieniu cache obrazu. Próbki: mediana około 8 tys. na początku i 12,7 tys. pod koniec (różnica obejmuje również pozostałe ścieżki kolorów).

[WNIOSEK] Zastąpić algorytmem o ograniczonej liczbie kroków: wyszukiwanie granic beatów albo dzielenie binarne przez stałą. Przy rozwiązaniu przyrostowym obsłużyć restart, pauzę i duże skoki ticka. Zachować dokładnie obecną fazę 187 i bazę kolorów; zmiana na inne tempo byłaby zmianą artystyczną. Krótki lookup kontrastu można później zastąpić tablicą flag, lecz ma mniejszy priorytet.

### 7. PMG jest szeroko czyszczone nawet przy podobnych klatkach — średni priorytet

[ODCZYT] `basketball_hero.py:198–202`, `crush_portraits.py:69–73`, `trevor_polished.py:222–225`: trzy zapisy indexed na każdy z 256 indeksów. To 768 operacji zapisu i około 5,1 tys. cykli pętli. Zakresy częściowo się pokrywają: $0980–$0A7F oraz $0A00–$0AFF.

[WNIOSEK] Czyścić poprzednio zajęte przedziały PMG, a pełne czyszczenie zostawić na zmianę właściciela/sceny. Można też wyeliminować nakładające się zapisy. Sprawdzić stare pozycje piłki, BANG i oczy po przejściach; samo wyłączenie GRACTL nie usuwa dawnych danych.

## Ryzyka techniczne i proces budowania

**Synchronizacja rastra: wymaga pomiaru.** Pętle `VCOUNT >=124` w wielu efektach czekają na okno, nie na początek nowej ramki. Dwa wywołania mogą przejść w tym samym oknie, a NMI może opóźnić dalsze zapisy. PMG bywa czyszczone dopiero po tym oczekiwaniu. Nie wykazano tearingu, ale stałe VCOUNT=124 w testach nie może go wykluczyć. Potrzebny ślad w emulatorze z DMA: linia wejścia, czas renderowania, linia przełączenia DL, ostatni zapis PMG, odstępy czterech ticków muzyki. Przed zmianą schematu synchronizacji sprawdzić wpływ na oryginalne DLI.

**Snapshot nie jest czasem prezentacji.** `build_bitmap_sequence.py:224–233` poprawnie pobiera spójny wielobajtowy tick, ale po 90–130 tys. cykli pokazuje stan już starszy o kilka ramek. To opóźnienie obrazu, nie spowolnienie zegara muzyki. Testy powinny mierzyć pominięte fazy i opóźnienie ważnych uderzeń, zamiast jedynie wymagać kosztu poniżej 110/140 tys. cykli.

**Inkrementalny make jest niespójny z ochroną wydań.** `Makefile:37–38` próbuje ponownie wygenerować ten sam v126 po zmianie zależności, a `build_bitmap_sequence.py:48–49` odmawia nadpisania istniejącego XEX. Rebuild po edycji źródeł zakończy się błędem. Zachować archiwalne wydania, lecz zapewnić osobny nadpisywalny cel roboczy lub jawne wersjonowanie celu. `make clean` usuwa bieżący XEX, więc nie jest dobrym sposobem obejścia ochrony wydań.

**Niepełne zależności assetów.** Generator czyta m.in. wszystkie cztery `trevor-polished-*.rgb`, ale główny cel deklaruje tylko `-0.rgb`. Podobnie zestawy dance/trevor. Zmiana lub usunięcie pojedynczego pozostałego pliku nie musi przebudować XEX. Zadeklarować wszystkie rzeczywiste wejścia i artefakt JSON używany przez testy; testy powinny mieć pewność, że badają aktualny build.

**Fałszywa zieleń bez py65.** `requirements-dev.txt` nazywa py65 opcjonalnym; testy CPU mogą zostać pominięte i unittest nadal zwróci sukces. W wymaganym sprawdzaniu wydania zależność musi być obowiązkowa. Aktualny audyt zainstalował py65 i nie polega na pominiętych testach.

**Utrzymanie kodu.** Powtarzany emiter DL/kopii/PMG w kilku plikach utrudnia jednolite poprawki. Wydzielić generatory sekwencji z parametrami, bez dokładania kosztu wywołań 6502. Dodać odrzucanie powtórzonej etykiety w `Code.label`, która obecnie cicho nadpisuje symbol. `AGENTS.md` opisuje brak źródeł i testów, mimo że oba istnieją; dokument jest nieaktualny.

## Co jest zrobione dobrze

- Rysowanie do nieaktywnego bufora i osobne klucze jego zawartości; testy kontrolują zapisy do aktywnego obrazu.
- Wrapper muzyki zachowuje rejestry i PORTB, banki wideo nie zastępują wymaganych banków dekodera.
- Kontrole kolizji segmentów i limitów pamięci, sondowanie aliasów banków oraz testy oryginalnych pikseli.
- Synchronizacja scen z zegarem playera, a nie z liczbą callbacków; muzyka przechodzi pełne porównanie w emulatorze.
- Build z aktualnych wejść odtwarza dostarczony XEX bajtowo.

## Zalecana kolejność

1. Poprawić nieaktualny test i proces roboczego rebuilda; włączyć wymagane testy CPU.
2. Dodać pomiar rzeczywistych ramek z DMA/NMI i terminów prezentacji.
3. Usunąć ponowne budowanie stałych DL i przyspieszyć wspólne kopie; porównać piksele, własność buforów i POKEY.
4. Przygotować portrety z góry i wprowadzić mniejsze aktualizacje tańca.
5. Usunąć narastające modulo, ograniczyć czyszczenie PMG i zoptymalizować przebiegi plazmy.

Nie podaję procentu przyspieszenia całego dema: dotychczasowe pomiary pokazują koszt aktualnego kodu, a podane oszczędności pojedynczych pętli są szacunkami. Wydanie po zmianach powinno przejść testy obrazu, bankowania, pełnego POKEY i rzeczywistego czasu prezentacji.
