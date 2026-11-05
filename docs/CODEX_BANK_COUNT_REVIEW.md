# Zlecenie dla Codexa — niezależna weryfikacja banków muzyki v035

## Pytanie

Czy player `less-i-know-release-v035.xex` potrzebuje **7 czy 8 banków danych muzycznych**? Proszę zweryfikować niezależnie tezę z obecnego audytu, że bank 8 jest potrzebny, bo zawiera czytany znacznik końca. Nie należy opierać odpowiedzi wyłącznie na założeniu zapisanym dla v024.

## Materiały do sprawdzenia

- Player: `less-i-know-release-v035.xex`
- Wyodrębnione segmenty: `assets/music/v035/bank_01.bin` … `bank_14.bin`
- Manifest i hashe: `assets/music/v035/manifest.json`
- Implementacja ekstrakcji: `tools/extract_music.py`
- Śledzenie dekodera: `tools/audit_music_banks.py`
- Dotychczasowy wynik: `docs/MUSIC_BANK_AUDIT.md`
- Starsze założenia i zadania V1–V7: `TLIKTB_Technical_Constraints.md`

SHA-256 badanego XEX: `6d5d9cf3004f9003ede8d91aa4891a100f672c5a0e9429a6ecf20d1f5fef0ff0`.

## Teza do niezależnego potwierdzenia lub obalenia

Obecny audyt twierdzi, że:

- segmenty `$8000–$BFFF` zawierają 14 bloków po 16 384 B w kolejności ładowania;
- dekoder czyta całe banki 1–7 oraz 2 820 B banku 8;
- ostatni bajt danych różny od `$FF` znajduje się pod offsetem 2818 banku 8, a `$FF` pod offsetem 2819 jest czytanym znacznikiem końca;
- banki 9–14 nie są czytane, a ich zawartość to `$FF`;
- zatem **7 banków nie wystarcza; minimum dla obecnego strumienia v035 to 8**.

Proszę sprawdzić w kodzie XEX i w ścieżce dekodera, czy liczby te wynikają z rzeczywistych odczytów, a nie tylko z rozmiaru bloków lub liczby segmentów. Wyjaśnić też różnicę między liczbą banków ładowanych przez oryginalny XEX (14), liczbą banków odczytywanych przez dekoder (rzekomo 8) i liczbą banków, które można bezpiecznie usunąć lub ponownie wykorzystać po inicjalizacji playera.

## Dodatkowe punkty kontrolne

1. Potwierdzić indeksowanie banków i dokładny adres/offset każdego odczytu końcowego, w szczególności odczyt `$FF` pod offsetem 2819 w banku 8. Czy usunięcie banku 8 lub skrócenie jego zawartości powoduje brak znacznika końca albo zmianę zachowania playera?
2. Sprawdzić, czy model PORTB w `tools/audit_music_banks.py` odpowiada ścieżce wykrywania pamięci w v035. Wskazać ewentualne ograniczenia symulacji względem prawdziwego Atari/Altirry.
3. Zweryfikować liczbę aktualizacji do końca: raport podaje 59 833, podczas gdy timeline wylicza 59 840 (`160 × 374`). Ustalić, czy różnica wynika z inicjalizacji/znacznika końca/sposobu liczenia, czy jest nierozwiązaną rozbieżnością. Oddzielić tę kwestię od odpowiedzi 7-vs-8.
4. W v035 używanym tutaj nie ma w katalogu pliku v024 do porównania. Jeśli nie da się potwierdzić, skąd wzięło się starsze założenie siedmiu banków, zaznaczyć to wprost — nie zgadywać.

## Oczekiwany wynik

Dopisać do tego raportu krótką konkluzję: **7 czy 8 banków dla v035**, wraz z uzasadnieniem, dokładnym zakresem odczytów, ograniczeniami weryfikacji i bezpiecznym zaleceniem dotyczącym skracania/ponownego użycia bloków. Jeśli wynik audytu obecnego narzędzia jest błędny, wskazać konkretny błąd i sposób reprodukcji poprawionego wyniku.

## Ograniczenia pracy

- Analiza tylko do odczytu. Nie modyfikować oryginalnego XEX, banków, narzędzi ani buildów demo.
- Jeśli potrzebny jest zapis raportu maszyny lub logów, kierować go do `/tmp`, nie do `build/` w aktywnym projekcie.
- Nie wykonywać przycinania ani przebudowy playera w ramach tej weryfikacji.

---

## Niezależna weryfikacja — wynik

**Dla obecnego strumienia v035 i jego obecnego dekodera potrzeba 8 banków
po 16 KiB.** Siedem mieści tylko 114 688 B, natomiast odczytywany strumień ma
117 508 B, w tym wymagany odczyt w ósmym banku. Nie jest to dowód, że nie da
się zmieścić muzyki w siedmiu bankach po zmianie formatu lub dekodera.

[ODCZYT] SHA-256 XEX zgadza się z podanym w zleceniu. Wszystkie 14 segmentów
`$8000–$BFFF` jest bajt w bajt zgodnych z plikami `bank_01.bin`–`bank_14.bin`
i z sumami w manifeście. Banki 9–14 zawierają wyłącznie `$FF`.

[ODCZYT] Niezależny ślad py65 wykonał procedury inicjalizacji `$232D`, wstępne
dekodowanie `$237D` i oryginalną ścieżkę NMI od `$2210` do ustawienia flagi
`$24C8`. Odczyty były ciągłe, każdy z poniższych bajtów odczytano raz:

| Bank ładowania, numerowany od 1 | Odczyt w oknie CPU `$4000–$7FFF` | Offsety | Bajty |
| --- | --- | --- | ---: |
| 1–7, każdy | `$4000–$7FFF` | 0–16383 | 16384 każdy |
| 8 | `$4000–$4B03` | 0–2819 | 2820 |
| 9–14 | brak | brak | 0 |

Ostatnie odczyty z banku 8: offsety 2813–2817 (`$4AFD–$4B01`) mają wartość
`$00` przy aktualizacji 59825; offset 2818 (`$4B02`) to `$86` przy 59826;
offset 2819 (`$4B03`) to `$FF` przy 59833. Pobranie wykonuje instrukcja
`LDA ($A0),Y` pod `$2353`. Dekoder poleceń pod `$2A0C` porównuje wynik z
`$FF` i skacze do `$2A5F`, gdzie ustawia flagę końca. Adres kursora po tym
odczycie to `$4B04`. Znacznik jest więc potrzebny jako **bajt o wartości**
`$FF`; nie musi być fizycznie tym samym bajtem pliku, jeśli w tym samym
logicznym miejscu inny prawidłowy loader zapewni `$FF`.

[ODCZYT] Niezależnie uruchomiono oryginalny XEX w Atari800, PAL, `-1088xe`,
Altirra OS. Po INIT tablica `$26FC–$2709` wynosiła
`81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB`. Przy zatrzymaniu na `$2A5F`
akumulator zawierał `$FF`, indeks banku `$24A5` był równy 7 (liczenie od
zera), kursor `$A0/$A1` wskazywał `$4B04`, a licznik `$24A7–$24A9` wynosił
59833. Zatrzymanie nastąpiło przed wykonaniem instrukcji ustawiającej flagę.
To potwierdza końcową ścieżkę na konkretnej konfiguracji emulatora; nie jest
pełnym niezależnym śladem wszystkich odczytów na rzeczywistym sprzęcie.

### Próby zmiany danych w modelu — bez modyfikacji XEX

[ODCZYT] Po podmianie w pamięci tylko banku 8 na same `$FF` flaga końca
ustawiła się po 58221, zamiast 59833, aktualizacjach — 1612 ticków wcześniej
(ok. 8,1 s przy 199,44 Hz). W tym wariancie pierwsze bajty `$FF` w banku 8
zostały najpierw użyte jako dane pakietu, a znacznik końca rozpoznano przy
offsecie 3. To nie jest równoważne dowolnemu fizycznemu usunięciu banku:
rzeczywista zawartość nieprzydzielonej pamięci zależy od sprzętu i loadera.

[ODCZYT] Po zmianie samego bajtu 2819 z `$FF` na `$00`, przy pozostawieniu
reszty końcówki `$FF`, dekoder odczytał również offsety 2820–2822 i zakończył
po 59834 aktualizacjach. Zatem usunięcie tego konkretnego znacznika zmienia
ścieżkę; w tej próbie nie powoduje trwałego braku końca, bo późniejsze `$FF`
pozostają dostępne. Nie wolno zakładać, że skrócenie danych i pozostawienie
niezainicjalizowanej pamięci zapewni właściwy bajt na `$4B03`.

### Ograniczenia i zalecenie

[ODCZYT] Model `audit_music_banks.py` podstawia pierwszą z tablic selektorów i
mapuje każdą jej wartość na osobną tablicę bajtów. Nie wykonuje procedury
wykrywania banków ani kopiującego INIT, nie modeluje aliasów PORTB, CPU/ANTIC,
ROM, DMA, czasu linii ani rzeczywistych rejestrów POKEY. Zapis do `$4000–$7FFF`
w modelu nie jest zapisem do modelowanego banku. Dlatego sam model dowodzi
odczytów na ścieżce dekodera przy założonej poprawnej mapie, a nie poprawności
wszystkich konfiguracji rozszerzeń. Atari800 potwierdził, że dla badanej
konfiguracji player faktycznie wykrył tę pierwszą tablicę i doszedł do tego
samego końca. Dotychczasowy eksperyment z `$55` na nieczytanych obszarach jest
dodatkowym dowodem dla badanego emulatora, nie gwarancją dla każdego rozszerzenia.

[WNIOSEK] 14 to liczba oryginalnie ładowanych bloków; 8 to liczba banków,
z których dekoder faktycznie czyta. Po zakończeniu INIT można przeznaczyć całe
banki 9–14 oraz końcówkę banku 8 od offsetu 2820 na inne dane, pod warunkiem
prawidłowego rozpoznania rzeczywistych banków i zabezpieczenia własności PORTB.
Nie wolno nadpisywać banków 1–7 ani pierwszych 2820 bajtów banku 8 podczas
odtwarzania. Usunięcie sześciu segmentów z **oryginalnego pliku** to osobna
modyfikacja loadera/formatu i wymaga ponownej weryfikacji INIT, synchronizacji,
restartu oraz kompletnego odtwarzania — sam brak późniejszych odczytów nie
jest dowodem, że dowolne fizyczne obcięcie XEX zadziała. To rozróżnienie jest
istotne także dla obecnego dema, które już wykorzystuje wskazane nieczytane
obszary.

### 59833 a 59840

[ODCZYT] Wstępne wywołanie `$237D` następuje przed liczeniem NMI. Przyjęty
model zliczył 59833 wywołania NMI do flagi końca i licznik playera również
wynosił 59833; Atari800 na oryginalnym XEX potwierdził 59833 na wejściu w
procedurę końca. Ostatnie polecenie `$86` odczytano przy 59826, a końcowy
`$FF` przy 59833, siedem aktualizacji później. Ten odstęp opisuje końcówkę
strumienia, ale sam nie wyjaśnia różnicy do 59840; wyjaśnia ją rachunek tempa
i częstotliwości PAL poniżej.

[ODCZYT] Timeline przyjmuje 128 BPM, 160 taktów po 4 uderzenia i czas 300 s.
Dokument playera podaje 4 aktualizacje na klatkę PAL, czyli 199,443 Hz.
Podręcznik referencyjny Altirry podaje idealny zegar PAL 49,86074 Hz; cztery
aktualizacje dają 199,44296 Hz, co zaokrągla się do napisu playera.

[WNIOSEK] Jeden takt trwa 1,875 s, więc odpowiada `199,44296 × 1,875 =
373,95555` aktualizacji, nie dokładnie 374. Dla 160 taktów wychodzi
`373,95555 × 160 = 59832,888`, czyli 59833 całkowite ticki. Zmierzony licznik
59833 odpowiada 300,00056 s — praktycznie dokładnie pięciu minutom. Wcześniejsza
mapa silnika mnożyła numer taktu przez 374, np. 24 × 374 = 8976 i 160 × 374 =
59840. To kumulowało nadmiar 0,04445 ticka na takt do 7,112 ticków (35,7 ms).

[ODCZYT] Silnik v051 używał tych przybliżonych wartości w progach scen i ujęć.
To błąd mapowania taktów na ticki w silniku obrazu, nie błąd licznika ani brak
aktualizacji playera.

[ODCZYT] W v052 wspólna funkcja `tools/music_timing.py` wyznacza próg taktu jako
`ceil(n × 373,95555)` od początku utworu. Przykładowo takt 24 zaczyna się przy
8975, takt 88 przy 32909, a takt 160 przy 59833. Rytm kolorów mozaiki używa
naprzemiennych odstępów 186/187 ticków, a nie stałych 187. W v053 tą samą mapą
objęto też wewnętrzny próg ujęcia Trevora przy takcie 68.

[ODCZYT] W tym checkoutcie nie ma XEX v024. Genezy założenia o siedmiu bankach
nie da się więc tu potwierdzić; nie należy przenosić go na v035.
