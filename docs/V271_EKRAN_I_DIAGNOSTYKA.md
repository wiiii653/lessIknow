# V271 — naprawiony ekran wczesny i diagnostyka banków

## Co było źle

[ODCZYT] `tools/loading_screen.py` ustawiał `$D018=$00`. W ANTIC-u pole
CHBASE wskazuje wtedy stronę `$0000`, a nie font ROM pod `$E000`. Ekran
ANTIC 2 był więc wypełniony pustymi znakami: czarny obraz bez tekstu.
Grafika ekranu, display lista i kod INIT były poprawne.

[ODCZYT] Ten sam błąd jest w `releases/avg-first-bank-diagnostic-001.xex`.
Czarny ekran tego pliku nie jest wynikiem `BANK TEST FAILED`; to brak
widocznego fontu. Nie wolno na tej podstawie wnioskować o bankach.

[ODCZYT] `less-i-know-release-v035.xex` i remiksy Starfish startują na tym
samym Atari. To potwierdza działanie oryginalnego playera, jego pierwszego
wykrywania 14 banków i sposobu uruchamiania XEX przez AVG. Nie potwierdza
naszego dodatkowego loadera 50 banków wideo.

## Poprawka

`$D018=$E0` w `tools/loading_screen.py`. Przebudowany
`build/visual-prototype-dev.xex` różni się od poprzedniego **jednym bajtem**
(`$00` → `$E0` pod offsetem `$0D71`, segment INIT `$0780`). Pełny zestaw:
200/200 testów.

Release 011 (`releases/less-i-know-demo-release-011-avg-stereo.xex`) powstaje
z release 009 przez `tools/build_avg_candidate.py` i zawiera tę samą poprawkę.

## Nowe narzędzia diagnostyczne

- `tools/build_early_screen_diagnostic.py` →
  `releases/avg-early-screen-diagnostic-004.xex` (1,1 KiB). Bez banków i bez
  playera. Jeśli na Atari widać napis `EARLY SCREEN OK`, wczesny INIT, DMA
  i font ROM działają w środowisku AVG. Brak napisu wskazuje na ładowanie
  INIT-ów przez AVG, nie na banki.
- `tools/build_first_bank_diagnostic_002.py` →
  `releases/avg-first-bank-diagnostic-004.xex` (2,7 KiB). Zawiera wyłącznie
  dwa oryginalne segmenty playera (`$2000–$24B2`, `$24BD–$28BC`), bez banków
  muzyki i grafiki. Uruchamia oryginalne wykrywanie 14 selektorów i kończy
  ekranem `BANK TEST PASSED` albo `BANK TEST FAILED`. Ekran i kod leżą
  w `$2B00–$2DFF`, poza wszystkimi segmentami tego pliku.

Oba ekrany ustawiają CHBASE=`$E0` i wyłączają DMA tylko na czas zapisu.

## Ograniczenia

- [ODCZYT] Skopiowanie na kartę wersji 1106 B zamiast 2664 B wyjaśnia
  wcześniejsze `EARLY SCREEN OK`; nie jest to wynik testu banków.
- [OGRANICZENIE] Nie wykonano próby na AVG ani fizycznym Rambo.
- [OGRANICZENIE] Błąd CHBASE wyjaśnia czarny ekran diagnostyki, ale nie
  dowodzi przyczyny braku startu pełnego dema.
- [OGRANICZENIE] Diagnostyka 004 sprawdza tylko pierwsze 14 selektorów.
  Nie testuje 50 banków wideo ani kopiowania 16 KiB.
- Pełny start dema na docelowej maszynie pozostaje niepotwierdzony.

## Próba na Atari i wniosek z diagnostyki

[ODCZYT] `avg-early-screen-diagnostic-004.xex` wyświetlił `EARLY SCREEN OK`
na docelowym Atari. Wczesny INIT, DMA i font ROM działają w AVG.

[ODCZYT] `avg-first-bank-diagnostic-004.xex` pokazał `ORIGINAL V035 BANK
PROBE`, ale bez wiersza wyniku. Ten wariant nie zawierał segmentów `$3300`
i `$3400` ani ośmiu banków muzyki, więc nie jest wiarygodnym testem
oryginalnego wykrywania; jego brak wyniku nie mówi nic o bankach.

## Nowy, samodzielny test mapy 64 selektorów

`tools/build_bank_map_diagnostic.py` →
`releases/avg-bank-map-diagnostic-001.xex` (473 B, 11 segmentów, bez playera
i bez banków). Każdy z 64 selektorów dostaje unikalny znacznik w swoim banku
pod `$4000`; druga pętla sprawdza, czy żadne dwa selektory nie wskazują tego
samego banku. Wynik: `BANK MAP PASSED` albo `BANK MAP FAILED`.

64 selektory w tym teście są **identyczne** z zestawem wyprowadzonym z
działającego `rdc02-fws (2).xex`. Test nie zależy od v035, muzyki ani AVG.

- `PASSED`: mapowanie 64 banków jest dostępne; szukać błędu w kopiowaniu
  i obsłudze błędów naszego loadera, nie w samych selektorach.
- `FAILED`: któryś selektor wskazuje ten sam bank; problem sprzętowy lub
  w założeniach mapy.

[ODCZYT] Model py65: mapa 64 rozdzielonych banków daje `PASSED`, a każde
celowe aliasowanie dwóch selektorów daje `FAILED`. Pierwsza wersja testu
miała błąd — strona INIT kończyła się pętlą zamiast `RTS`, więc probe się nie
uruchamiał; poprawiona wersja ma 466 B.

[ODCZYT] Kolejna próba na Atari: INIT wyświetlił `PROBING - PLEASE WAIT`, ale
wynik się nie pojawił. Ten sam objaw miał `avg-first-bank-diagnostic-004`:
INIT działa, natomiast kod pod wektorem RUN `$02E0` nie wykonał się lub padł.

[ODCZYT] `releases/avg-bank-map-diagnostic-003.xex` (485 B) przenosi CAŁY
probe do INIT — wyświetlenie, sondowanie i wynik — więc nie zależy od RUNAD.
Nie czyta też `$D301`; PORTB jest write-only na prawdziwym sprzęcie, a odczyt
zwraca śmieci. Na koniec wpisuje stałe `$FF` (normalny stan XL/XE). Model
py65: mapa rozdzielona → `BANK MAP PASSED`, alias → `BANK MAP FAILED`.

[WNIOSEK] Jeśli `003` pokaże wynik, a pełne demo nadal nie startuje, głównym
podejrzanym staje się wektor RUN `$13E0` i jego zależność od odczytu PORTB,
a nie mapa banków.

## Czy problemem jest zbyt wczesne użycie ROM-u?

[WNIOSEK] Nie widać takiego błędu. `less-i-know-release-v035.xex` czyta tabelę
selektorów spod `$2734/$2737`, ale to dane z segmentu XEX `$24BD–$28BC`
w RAM-ie, nie z ROM-u. Oryginalne wykrywanie ustawia `$D301=$FF` tylko po to,
by przywrócić widoczność OS, i działa na tym Atari. Nasz dodatkowy loader
również trzyma bit 0 PORTB ustawiony podczas sondowania.

[WNIOSEK] W kodzie `school_portrait_bank.loader()` nie widać błędu w liście
selektorów: 64 kandydatów jest identyczne z wyprowadzonymi przez działający
`rdc02-fws (2).xex`. Otwarte pozostają: kopiowanie 16 KiB, banki 0/1 liczone
bez weryfikacji oraz cicha pętla `no_bank` (tylko zmiana COLBK, bez tekstu).
