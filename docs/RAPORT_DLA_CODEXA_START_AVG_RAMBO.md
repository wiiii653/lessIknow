# Raport dla Codexa — start dema na Atari z Rambo 1 MB przez AVG

Data: 2026-11-11. Autor: sesja OpenCode. Zakres: diagnoza braku startu
pełnego dema na fizycznym Atari użytkownika. **Nie zmieniano produkcyjnego
timeline'u, muzyki ani alokacji banków.**

Legenda: `[ODCZYT]` — fakt sprawdzony; `[WNIOSEK]` — wniosek z dowodów;
`[ZAŁOŻENIE]` — hipoteza do sprawdzenia. `[OGRANICZENIE]` — czego nie
wolno traktować jako potwierdzenia.

---

## 1. Środowisko użytkownika

- Fizyczne Atari XL/XE z klonem rozszerzenia **Rambo 1 MB** (informacja
  użytkownika).
- Pliki XEX uruchamiane z **AVG** (loader kartridżowy; dokładny model i
  firmware nieznane).
- Ten sam zestaw sprzętowy uruchamia poprawnie:
  - `less-i-know-release-v035.xex` (oryginalny player z muzyką),
  - remiksy Starfish (player + muzyka),
  - inne demo 1 MB, które samo wykrywa banki i ładuje 53 banki.
- Pełne demo (`releases/less-i-know-demo-release-008.xex` = v261 oraz
  kandydaci 009/010/011) **nie startuje**; objaw: brak obrazu / brak napisu
  ładowania.

`[ODCZYT]` SHA-256 `less-i-know-release-v035.xex`:
`6d5d9cf3004f9003ede8d91aa4891a100f672c5a0e9429a6ecf20d1f5fef0ff0`
(234 348 B).

---

## 2. Fakty potwierdzone w kodzie i XEX-ach

### 2.1. Naprawiony błąd ekranu wczesnego (CHBASE)

`[ODCZYT]` `tools/loading_screen.py` ustawiał `$D018=$00`. ANTIC wskazywał
wtedy CHBASE na stronę `$0000`, a nie na font ROM `$E000`, więc wszystkie
znaki były puste → czarny ekran bez tekstu.

`[ODCZYT]` Po poprawce na `$D018=$E0` przebudowany
`build/visual-prototype-dev.xex` różni się od poprzedniego **jednym bajtem**
(offset `$0D71`: `$00` → `$E0`). Pełny zestaw testów: **200/200**.

`[ODCZYT]` Ten sam błąd zawierał `releases/avg-first-bank-diagnostic-001.xex`
i pierwsze wersje diagnostyk. **Czarny ekran tych plików nie był wynikiem
testu banków.**

### 2.2. Ekran wczesny działa na sprzęcie

`[ODCZYT użytkownika]` `releases/avg-early-screen-diagnostic-004.xex`
(1106 B) wyświetlił na Atari `EARLY SCREEN OK` / `AVG / XEX INIT + ROM FONT`.
Wniosek: wczesny INIT w XEX, DMA, font ROM i tryb ANTIC 2 działają
w środowisku AVG.

### 2.3. INIT działa, RUN (`$02E0`) nie

`[ODCZYT użytkownika]` `releases/avg-first-bank-diagnostic-004.xex` pokazał
tylko nagłówek `ORIGINAL V035 BANK PROBE`, bez wiersza wyniku. Ten sam objaw
miał `avg-bank-map-diagnostic-001.xex`: INIT wyświetlił `PROBING...`, ale
wynik się nie pojawił.

`[WNIOSEK]` Kod wykonywany przez INIT działa; kod pod wektorem RUN `$02E0`
**nie wykonał się lub padł** w tych dwóch buildach.

`[ODCZYT]` W oryginalnym `v035` wektor RUN `$13E0` jest używany i player
działa. `[WNIOSEK]` Loader AVG obsługuje RUNAD przynajmniej dla tego pliku,
więc samego mechanizmu nie można wykluczyć — ale nie ma bezpośredniego
dowodu, że nasz RUN `$13E0` został w pełni wykonany.

### 2.4. Pierwsza diagnostyka 004 nie była wiarygodna

`[ODCZYT]` `avg-first-bank-diagnostic-004.xex` (2664 B) zawiera tylko dwa
segmenty playera: `$2000–$24B2` i `$24BD–$28BC`. **Nie zawiera** segmentów
`$3300`/`$3400` ani banków muzyki (`$8000–$BFFF`). Oryginalne wykrywanie
14 selektorów czyta dane spod `$26FC`, `$270A`, `$2734`, `$2737` i zapisuje
do `$4000` w oknie banku — bez pełnego kontekstu wynik nie jest miarodajny.

### 2.5. Lista selektorów naszego loadera jest spójna z mapą tego sprzętu

`[ODCZYT]` `tools/school_portrait_bank.py` generuje 64 kandydatów:

```
81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB AD AF
C1 C3 C5 C7 C9 CB CD CF E1 E3 E5 E7 E9 EB ED EF
01 03 05 07 09 0B 0D 0F 21 23 25 27 29 2B 2D 2F
41 43 45 47 49 4B 4D 4F 61 63 65 67 69 6B 6D 6F
```

Bity: **0 = zawsze 1, 4 = zawsze 0**, zmienne **1, 2, 3, 5, 6, 7**
(6 bitów = 64 banki).

`[ODCZYT]` Niezależna analiza innego dema 1 MB, które na tym samym Atari
działa i ładuje 53 banki, pokazuje następujący sposób wyprowadzania
selektorów: baza liczona jako obrót numeru indeksu (`LSR` + trzy `ROR` +
`ADC #1`), następnie cztery warianty na bazę przez `EOR #$04` / `EOR #$0C`
przy `AND #$FE`, a przy przełączaniu banku `ORA #$01`.

`[WNIOSEK]` Po uwzględnieniu `|1` zbiór wyprowadzony tą metodą jest
**identyczny** z 64 wartościami naszego loadera. Ta sama kombinacja bitów
(1, 2, 3, 5, 6, 7) wystarcza więc na tym sprzęcie do zaadresowania co
najmniej 53 banków. Nasza lista kandydatów nie jest więc unikalnym błędem
dema.

`[OGRANICZENIE]` To nie dowodzi, że wszystkie 64 wartości są unikalne na
tej maszynie — tylko że co najmniej 53 z nich działa. Brakującą liczbę
rozstrzyga `avg-bank-map-diagnostic-003.xex`.

### 2.6. Mechanizm loadera wideo

`[ODCZYT]` `tools/school_portrait_bank.py`, funkcja `loader(frame, index)`:

- `index < 2`: selektor liczony arytmetycznie (`$2709 + 2` lub `+ 4`),
  **bez weryfikacji unikalności**; zapis do `$24B3+index`.
- `2 <= index < 50`: pętla po 64 kandydatach, test unikalności przez
  wpisanie `$55`/`$AA` do `$4000` i porównanie z bankami znanymi; wynik
  zapisywany do `$08C0+index` po `AND #$FE`.
- Brak banku: `no_bank` — `LDA #$32 / STA $D01A` i **pętla bez tekstu**.

`[ODCZYT]` XEX demo (release 009/011) ładuje 64 segmenty `$8000–$BFFF`
i wykonuje 67–68 INIT-ów; RUN = `$13E0`.

`[ODCZYT]` Stub startowy `tools/os_ram.py`, funkcja `run_stub()`:

```
78 A9 00 8D 0E D4 AD 01 D3 29 FE 8D 01 D3 4C 46 21
SEI / LDA #0 / STA $D40E / LDA $D301 / AND #$FE / STA $D301 / JMP $2146
```

`[ZAŁOŻENIE]` To read-modify-write na `$D301`. Na XL/XE PORTB jest portem
PIA i zwykle można go odczytać, ale nie jest to gwarantowane na wszystkich
klonach; jeśli odczyt zwróci śmieci, okno `$4000–$7FFF` zostanie przełączone
na zły bank i player padnie mimo poprawnego obrazu.

`[ODCZYT]` Analogiczny wzorzec `LDA $D301 / PHA … PLA / STA $D301` jest
w `school_portrait_bank.loader`, `banana_cache`, `build_bitmap_sequence`
(`banked_effects`, `ribbon_copy`, `final_boy`).

### 2.7. Konflikt bitów PORTB między rozszerzeniami

`[ODCZYT]` Standard 130XE: bit 0 = OS ROM, bit 1 = BASIC, bity 2–3 = bank
CPU, bity 4–5 = bank ANTIC. Klony 1 MB (Rambo, Newell, Compy-Shop, Ultimate
1 MB) przypisują bity **różnie**; U1MB ma dodatkowo rejestry `$D380–$D3FF`.

`[WNIOSEK]` Nasze 64 selektory używają bitu 1 jako bitu banku, a bitu 4 nie
używają wcale. Jeśli w danym klonie bit 1 steruje BASIC-em, a nie bankiem,
to `$81` i `$83` wskazują ten sam bank i dostępnych jest tylko 32 banki.
Wtedy loader po wyczerpaniu kandydatów wchodzi w `no_bank` i wisi — co
pasuje do zgłoszonego objawu.

`[OGRANICZENIE]` Co najmniej 53 banki z tego zestawu bitów działają na tym
sprzęcie, ale nie wiadomo, czy wszystkie 64 są unikalne — ten wariant wymaga
potwierdzenia testem.

---

## 3. Błędy znalezione w narzędziach diagnostycznych (naprawione)

1. `loading_screen.py`: `$D018=$00` → `$E0` (pusty ekran). **Naprawione.**
2. `avg-bank-map-diagnostic-001`: strona INIT kończyła się pętlą `halt`
   zamiast `RTS`, więc probe nigdy nie startował. **Naprawione w 002/003.**
3. `avg-bank-map-diagnostic-001`: pętla przełączała `PORTB=$00`, co wyłącza
   ROM OS bez kopii pod ROM i wywala wektor NMI. **Naprawione w 002/003.**
4. `avg-bank-map-diagnostic-003`: nie czyta `$D301`; na koniec wpisuje stałe
   `$FF`. **To wersja do uruchomienia.**

---

## 4. Artefakty diagnostyczne

| Plik | Rozmiar | SHA-256 | Przeznaczenie | Wynik na sprzęcie |
| --- | ---: | --- | --- | --- |
| `releases/avg-early-screen-diagnostic-004.xex` | 1 106 B | `49992187…e4a6ce4` | tylko ekran + INIT + font ROM | **OK**: `EARLY SCREEN OK` |
| `releases/avg-first-bank-diagnostic-001.xex` | 3 589 B | `2f1a7d66…4b3fa92e2f` | pierwsza próba 14 banków (stary, wadliwy CHBASE) | czarny ekran |
| `releases/avg-first-bank-diagnostic-004.xex` | 2 664 B | `92185952…ac8a2169d160` | nagłówek + PASS/FAIL po próbie | **tylko nagłówek** |
| `releases/avg-bank-map-diagnostic-001.xex` | 466 B | `c1bc824b…40208e24` | 64 selektory, wynik przez RUN | `PROBING…`, brak wyniku |
| `releases/avg-bank-map-diagnostic-002.xex` | 487 B | `dfb7c2a1…765a0ce8` | wszystko w INIT | nieuruchamiany |
| `releases/avg-bank-map-diagnostic-003.xex` | 485 B | `46b812e0…c885f2763320` | wszystko w INIT, bez odczytu `$D301` | **`BANK MAP PASSED`** |
| `releases/avg-run-vector-diagnostic-001.xex` | 285 B | `2f31a6fc…d101e6359` | INIT pisze `INIT OK`, RUN pisze `RUN OK` | **do uruchomienia** |

`[ODCZYT]` Pliki `*.debug.xex` to wcześniejsze, wadliwe warianty zachowane
dla historii; nie są przeznaczone do testów na sprzęcie.

### 4.1. Co dokładnie robi `avg-bank-map-diagnostic-003.xex`

`[ODCZYT]` 11 segmentów, wszystkie poniżej `$4000`:

```
$2C00 DLIST (21 B)          $2C16 TITLE      $2C3E PROBING
$2C66 PASSED                $2C8E FAILED     $2CC0..$2D7F kod (192 B)
$2E00 CANDIDATES (64 B)     $2E40 INDEX      $02E2 INIT = $2CC0
$02E0 RUN = $2CC0 (bezpieczna pętla halt)
```

Algorytm: dla każdego z 64 kandydatów wybierz bank i wpisz do `$4000`
unikalny znacznik (`index+1`); w drugim przebiegu odczytaj znacznik przez
ten sam kandydat i porównaj. Niezgodność = dwa selektory wskazują ten sam
bank → `BANK MAP FAILED`. Bit 0 PORTB pozostaje ustawiony (ROM OS widoczny,
VBI żyje), a na końcu wpisywane jest `$FF`.

`[ODCZYT]` Symulacja py65: mapa rozdzielona → `BANK MAP PASSED`; celowe
aliasowanie `$A5`→to samo co `$A7` → `BANK MAP FAILED`.

---

## 5. Otwarte hipotezy, w kolejności prawdopodobieństwa

**H1. Klon Rambo 1 MB ma inną semantykę bitów PORTB.**
`[ODCZYT]` **TEST SPRZĘTOWY OBALIŁ TĘ HIPOTEZĘ.** `avg-bank-map-diagnostic-003.xex`
pokazał `BANK MAP PASSED`, czyli wszystkie 64 selektory wskazują różne banki.
Mapa bitów 1, 2, 3, 5, 6, 7 jest na tym klonie poprawna, a bit 4 może zostać
zerowy. Nie ma tu konfliktu z BASIC-em ani z Self-Testem.

**H2. Odczyt `$D301` (write-only) w `run_stub()` i w loaderach.** Jeśli
odczyt zwraca śmieci, `AND #$FE` i zapis przełączają okno banku na zły bank,
mimo poprawnego wcześniejszego ładowania.
Rozstrzygnięcie: zamienić read-modify-write na zapis stałej; sprawdzić na
sprzęcie.

**H3. Kopiowanie 16 KiB przy włączonym BASIC/ROM.** Źródło `$8000–$BFFF`
może czytać ROM BASIC, jeśli dany selektor ustawia bit 1. Skutek:
uszkodzone klatki, niekoniecznie hang.
Rozstrzygnięcie: porównać 16 KiB po skopiowaniu (suma kontrolna na ekranie).

**H4. Wektor RUN nieobsługiwany lub przerywany przez loader AVG.**
Mechanizm RUNAD działa dla oryginalnego playera, ale nie ma dowodu, że nasz
`$13E0` wykonuje się w całości; dwa testy diagnostyczne zatrzymały się na
stanie z INIT.
Rozstrzygnięcie: build, który robi wszystko w INIT (już jest: 003).

**H5. Banki 0/1 liczone bez weryfikacji** (`$2709 + 2` / `+4`). Jeśli
pierwszy selektor nie jest `$81` (inny klon), arytmetyka trafia w zły bank.
Rozstrzygnięcie: dodać weryfikację jak dla pozostałych indeksów.

---

## 6. Plan dla Codexa (kolejność wykonania)

1. `[ODCZYT]` `avg-bank-map-diagnostic-003.xex` → **`BANK MAP PASSED`**.
   64 selektory są rozróżnialne; mapa bitów jest poprawna. Hipoteza H1
   obalona, nie zmieniać listy kandydatów „na ślepo”.
2. Uruchomić `avg-run-vector-diagnostic-001.xex` (285 B): INIT pisze
   `INIT OK` w wierszu 0, RUN pisze `RUN OK - RUNAD WORKS` w wierszu 2.
   - tylko `INIT OK` → ten loader nie wykonuje RUNAD dla naszego XEX;
     demo musi startować z ostatniego INIT, a nie z `$02E0`.
   - oba wiersze → RUNAD działa i problem jest w loaderze/kopiowaniu.
3. Jeśli RUNAD działa, sprawdzić kopiowanie 16 KiB (suma kontrolna po
   skopiowaniu) oraz `run_stub()` czytający `$D301`.
4. Po każdej zmianie: `make check` (200 testów) i porównanie stereo POKEY
   w Atari800 1088XE jako regresję — **pamiętając, że 1088XE nie jest tym
   samym co Rambo 1 MB**.
5. Nie ogłaszać gotowości compo bez próby na fizycznym Atari.

---

## 7. Reprodukcja i komendy

```sh
# Zależności testów (py65 nie ma w systemowym Pythonie)
python3 -m venv /tmp/opencode/tliktb-venv
/tmp/opencode/tliktb-venv/bin/pip install -r requirements-dev.txt

# Pełny zestaw testów
PYTHONPATH=tests:tools /tmp/opencode/tliktb-venv/bin/python \
  -m unittest discover -s tests

# Przebudowa roboczego builda
PYTHONPATH=tools /tmp/opencode/tliktb-venv/bin/python \
  tools/build_bitmap_sequence.py --replace

# Odtworzenie diagnostyk
PYTHONPATH=tools python3 tools/build_early_screen_diagnostic.py
PYTHONPATH=tools python3 tools/build_first_bank_diagnostic_002.py
PYTHONPATH=tools python3 tools/build_bank_map_diagnostic.py
PYTHONPATH=tools python3 tools/build_avg_candidate.py \
  releases/less-i-know-demo-release-009-stereo.xex \
  releases/less-i-know-demo-release-011-avg-stereo.xex

# Podgląd mapy segmentów XEX
python3 -c "from pathlib import Path; from tools.extract_music import segments; \
[print(i, hex(a), hex(b), len(x)) for i,(a,b,x) in \
 enumerate(segments(Path('releases/avg-bank-map-diagnostic-003.xex').read_bytes()))]"
```

`[ODCZYT]` Buildery zapisują nowe pliki w trybie `xb` (odmowa nadpisania).
Aby przebudować, trzeba najpierw usunąć plik albo zmienić nazwę wyjściową.

---

## 8. Stan repozytorium (istotne pliki)

Zmienione lub dodane w tej sesji:

- `tools/loading_screen.py` — **`$D018=$E0`** (naprawa CHBASE).
- `tools/build_early_screen_diagnostic.py` → `avg-early-screen-diagnostic-004.xex`.
- `tools/build_first_bank_diagnostic_002.py` → `avg-first-bank-diagnostic-004.xex`.
- `tools/build_bank_map_diagnostic.py` → `avg-bank-map-diagnostic-00{1,2,3}.xex`.
- `tools/build_avg_candidate.py` (wcześniej) → `less-i-know-demo-release-011-avg-stereo.xex`.
- `docs/V271_EKRAN_I_DIAGNOSTYKA.md` — notatka zmian.
- `docs/RAPORT_DLA_CODEXA_START_AVG_RAMBO.md` — ten raport.

Nieśledzone i pozostawione bez zmian: `releases/less-i-know-demo-release-009*`,
`010*`, `011*`, katalog `releases/less-i-know-sv2026we-v260-candidate/` oraz
starsze ZIP-y. Release 008 (`fff207ea…`) to nadal oficjalny v261.

`[ODCZYT]` `build/visual-prototype-dev.xex` po naprawie:
SHA-256 `c9a73fdf68b86558b0c8d5204c79d612ab741ba5146958d16e4b948a3734022c`,
2 560 B kodu, 298 współdzielonych wierszy.

---

## 9. Czego ten raport nie twierdzi

- Nie potwierdza, że demo zostało naprawione.
- Nie potwierdza, że przyczyna to banki, PORTB, RUNAD ani odczyt `$D301`.
- Nie zawiera próby na fizycznym Atari wykonanej w tej sesji — wszystkie
  wyniki sprzętowe pochodzą od użytkownika.
- Atari800 w konfiguracji `-1088xe` nie odwzorowuje klonu Rambo 1 MB.
- Testy py65 nie modelują ANTIC DMA, VBI, czasu linii ani zachowania
  write-only rejestrów.
