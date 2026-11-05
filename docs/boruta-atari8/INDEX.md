# Atari 8-bit — biblioteka dokumentacji dla agenta

Zebrane 29.10.2026. Każdy plik sprawdzony: HTTP 200, poprawny nagłówek PDF.

**Uwaga o warstwie tekstu — sprawdzone empirycznie `pdftotext`, nie założone:**
- **mają tekst (grep działa):** Altirra manual (204 925 słów), pakiet 553 stron (129 345),
  Atari Graphics & Arcade Game Design (169 939), Mapping the Atari (96 466),
  De Re Atari (82 754), Player-Missile Graphics (35 220), VBXE FX (8 535).
- **NIE mają tekstu (czyste skany, grep nic nie da):**
  `atari-800-technical-reference-notes.pdf` (275 B tekstu na cały plik) oraz
  `atari-400-800-os-a-source-listing-1981.pdf` (162 B). Treść Technical Reference
  Notes jest jednak dostępna **tekstowo** w pakiecie 553 stron — sięgaj tam.
  Listing źródeł OS w całym zbiorze istnieje tylko jako obraz; OCR nie jest
  zainstalowany na tej maszynie.

**Jak z tego korzystać:**
- `text/` — wyciągnięty tekst (5,7 MB). **Zacznij tutaj**: `grep -rn "PORTB" text/` jest tańszy niż czytanie skanu.
- `pdf/` — oryginały ze rysunkami i schematami (431 MB). Sięgaj, gdy potrzebny obraz, tabela albo diagram.
- `html/` — źródła HTML (684 KB), na wypadek gdy tekst źle się wyciągnął.

---

## Sprzęt i architektura

### `altirra-hardware-reference-manual.pdf` — 2,2 MB
Avery Lee (autor emulatora Altirra). **Najmocniejsza pozycja w całym zbiorze.**
Dokładna semantyka rejestrów ANTIC/GTIA/POKEY/PIA, cykle per dostęp, zachowania
nieudokumentowane, tryby wyświetlania linia po linii, quirk-i oryginalnych układów.
Do tego: `text/altirra-hardware-reference-manual.txt`.

### `atari-400-800-tech-ref-notes-os-manual-os-source-hw-manual-553p.pdf` — 21 MB
Pakiet 553 stron: Technical Reference Notes + OS User's Manual + OS Source Listing
+ Hardware Manual w jednym. Historyczne źródło prosto od Atari.

### `atari-800-technical-reference-notes.pdf` — 21 MB
**Skan bez warstwy tekstu** (całe 275 B tekstu z `pdftotext`). Sens ma tylko
jako źródło rysunków i schematów — do czytania bierz pakiet 553 stron,
gdzie ta sama treść jest już zeskanowana z OCR.

### `atari-400-800-os-a-source-listing-1981.pdf` — 54 MB
**Pełny listing źródłowy OS A (1981)** — ale to czysty skan (162 B tekstu).
Do przeglądania okiem, nie do grepowania: OCR-u na tej maszynie nie ma.

### `de-re-atari.pdf` — 244 strony, 81 MB
Klasyk: architektura 400/800 od środka — ANTIC, GTIA, POKEY, PIA, przerwania,
display listy, player/missile. Ma warstwę OCR, więc grep działa.

### `mapping-the-atari.pdf` — 308 stron, 83 MB
Ian Chadwick. **Mapa pamięci do bajtu**: co leży pod każdym adresem `$0000-$D7FF`,
co jest bezpieczne, co nadpisuje OS. Najszybsza droga do odpowiedzi "czy mogę tu pisać".

### `atari-graphics-and-arcade-game-design.pdf` — 484 strony, 148 MB
Grafika i projekty gier: tryby, player/missile, animacja, projektowanie plansz.
Najgrubsza pozycja, ale i najwięcej praktyki.

---

## Efekty i programowanie

### `text/dli-tutorial.txt` — 15 229 słów
Player/Missile Podcast: DLI od podstaw do zaawansowanych. Kiedy przerwanie
ugryzie za późno, ile cykli zostaje, jak nie rozerwać obrazu.

### `text/fine-scrolling-tutorial.txt` — 11 407 słów
Fine scrolling: `HSCROL`, `VSCROL`, `LMS`, precyzja co do koloru zegara.

### `text/avery-lee-reverse-engineering-atari-video.txt` — 3 273 słowa
Blog Avery'ego Lee o reverse engineeringu układu wideo Atari. Kopalnia
nieudokumentowanych szczegółów, spisana przez człowieka, który zrobił emulator.

### `text/retrogamecoders-atari8.txt` — 1 400 słów
Zwięzła, uporządkowana ściąga platformy: tryby, rejestry, konwencje.

---

## Assembler i narzędzia

### `text/mads-manual.txt` — 24 335 słów (największy tekst w zbiorze)
MADS — asembler, którym robi się atarowskie dema. Pełna instrukcja: makra,
dyrektywy, relokacja, banki.

### `tech-docs-index-pigwa.txt`
Indeks archiwum dokumentacji technicznej (ftp.pigwa.net) — spis tego, czego
jeszcze można szukać.

---

## VBXE

### `vbxe-fx-programming-en.pdf` — 176 KB
Programowanie VBXE: rejestry, tryby, FX core. Po angielsku.
Do tego `text/vbxe-blitter-manual.txt` — 5 707 słów o blitterze.

---

## Player/Missile i grafika obiektowa

### `player-missile-graphics-in-basic.pdf` — 40 MB
Philip Seyer. PMG od podstaw — duchy, kolizje, priorytety. W Basicu, ale
zasady sprzętowe te same.

---

## Czego tu nie ma i dlaczego

- **atariarchives.org** (De Re Atari, Mapping the Atari, AGAGD w HTML) — serwis
  postawił **Cloudflare Turnstile**. Zweryfikowane: każda strona zwraca 1108 B
  „Please confirm you are human". Dla agenta to ściana. Dlatego książki wzięte
  ze skanów atarimania (z warstwą OCR).
- **atariwiki.org** — HTTP 502 w chwili pobierania (główna strona padła).
  Działa natomiast `data.atariwiki.org`, skąd wzięły się dwa duże PDF-y.
- **seriouscomputerist.atariverse.com** — HTTP 500.

## Linki do rzeczy, których nie ma sensu kopiować

```
RMT (muzyka)        https://github.com/raster-atari-org/RASTER-Music-Tracker
SAP — specyfikacja  https://asap.sourceforge.net/sap-format.html
SAP-R + player      https://github.com/dmsc/lzss-sap
Silly Venture       https://sillyventure.eu/
AtariAge VBXE       https://forums.atariage.com/topic/346667-vbxe-tutorials-summary-of-all-vbxe-topics/
Instrukcja 6502     https://www.masswerk.at/6502/6502_instruction_set.html
```

## Progi cykli, o których warto pamiętać

```
PAL:  312 linii × 114 cykli = 35 568 cykli na ramkę (50 Hz)
NTSC: 262 linie × 114 cykli = 29 868 cykli na ramkę (60 Hz)
STA abs,Y  = 5 cykli        LDA abs,Y = 4 cykle
```
