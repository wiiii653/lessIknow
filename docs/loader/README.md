# Bieżący kontrakt sprzętowy
Przed użyciem historycznych komend poniżej przeczytaj
[HARDWARE_LOADER_CONTRACT.md](../HARDWARE_LOADER_CONTRACT.md).
Roboczy XEX sprzętowy buduje `make hardware`. Polecenie odtwarzające wydanie
po party z miksem stereo podaje [README](../../README.md).
Stare przykłady mono i ręczne składanie etapów nie są procedurą wydawniczą.

# Dokumentacja loadera — The Less I Know The Better (Atari XE)

Katalog opisuje potok 64 banków, kompaktowanie XEX, ekran ładowania
w wysokiej pamięci i późny start z niskiej pamięci. Część szczegółowych
tabel niżej pochodzi ze starszego release 018; sprawdzaj je względem aktualnego
builda i instalatorów przed zmianami.

Historyczny stan opisany poniżej: 2026-11-12, stereo release 048/v315,
`releases/less-i-know-demo-release-048-stereo.xex`.

Legenda (zgodnie z `AGENTS.md`):

- `[ODCZYT]` — sprawdzone w kodzie, XEX-ie lub na sprzęcie;
- `[WNIOSEK]` — wniosek z dowodów;
- `[ZAŁOŻENIE]` — hipoteza, wymaga sprawdzenia;
- `[OGRANICZENIE]` — czego nie wolno traktować jako potwierdzenia.

---

## 1. Co ten loader robi

1. Ładuje oryginalny player v035 (muzyka, 14 banków) i podmienia jego
   wejście na własny kod.
2. Ładuje do 50 dodatkowych banków 16 KiB z grafiką i kodem scen.
3. Pokazuje stały napis `LOADING BANKS` z animowanymi kropkami, bez numerów
   INIT-ów ani adresów.
4. Na końcu odtwarza niską pamięć wykonawczą i **skacze bezpośrednio do
   playera** (`JMP $13E0`), bez polegania na wektorze RUN.

## 2. Potok budowania (skrót)

```
build_bitmap_sequence.py   → 64 banki, obrazy scen, ~1.11 MB
        ↓
build_init_trace_high.py   → ekran ładowania w $3800, wrapper INIT w $3900
        ↓
build_compact_xex.py       → zero-run compression + INIT czyszczący $3A00
        ↓
build_avg_late_lowram.py   → bufor niskiej pamięci $4000, bootstrap $4800
        ↓
(releases/less-i-know-demo-release-018-stereo.xex, 935 472 B)
```

Szczegóły i komendy: [01_potok_budowania.md](01_potok_budowania.md).

## 3. Spis treści

| Plik | Zawartość |
| --- | --- |
| [01_potok_budowania.md](01_potok_budowania.md) | narzędzia, wejścia/wyjścia, komendy |
| [02_xex_i_start.md](02_xex_i_start.md) | format XEX, INIT/RUNAD, dlaczego późny start |
| [03_ekran_ladowania.md](03_ekran_ladowania.md) | ekran, display lista, kolory, CHBASE |
| [04_bankowanie.md](04_bankowanie.md) | PORTB, 64 selektory, wykrywanie i kopiowanie banków |
| [05_kompakt_i_pozny_start.md](05_kompakt_i_pozny_start.md) | czyszczenie banku, pomijanie zer, bootstrap |
| [06_mapa_pamieci_i_bankow.md](06_mapa_pamieci_i_bankow.md) | adresy loadera i przydział 50 banków |
| [07_przelaczanie_runtime.md](07_przelaczanie_runtime.md) | przełączanie banków w czasie odtwarzania |
| [08_diagnostyka.md](08_diagnostyka.md) | pliki diagnostyczne i co dowiodły |
| [09_odtwarzanie_i_testy.md](09_odtwarzanie_i_testy.md) | reprodukcja, testy, checklista |
| [10_analiza_optymalizacji.md](10_analiza_optymalizacji.md) | analiza zysków i ryzyk, bez zmian w kodzie |
| [11_mozaiki_szkola_i_banany.md](11_mozaiki_szkola_i_banany.md) | profile scen, propozycje przyspieszenia i naprzemienny obrót bananów |

## 4. Szybka ściąga

### 4.1. Adresy loadera w obecnym buildzie

| Adres | Rola |
| --- | --- |
| `$3800–$3877` | ekran tekstowy 3×40 (ATASCII−32) |
| `$3880–$388A` | display lista ANTIC 2 |
| `$38A0–$38DC` | INIT ekranu ładowania (kolory, DLIST, CHBASE, DMA) |
| `$3900–$398B` | wrapper INIT-a: aktualizuje kropki `LOADING BANKS` |
| `$3A00–$3A24` | kod czyszczący $8000–$BFFF przed każdym bankiem |
| `$4000–$47FF` | bufor niskiej pamięci (2 KiB) |
| `$4800–$4873` | bootstrap: kopiuje bufor do $0400–$0BFF, `JMP $13E0` |
| `$8000–$BFFF` | okno banku 16 KiB (dane banków) |

### 4.2. Niezmienniki, których nie wolno łamać

- `$3800–$38FF` i `$3900` muszą pozostać wolne od danych runtime.
- Segment bufora `$4000–$47FF` i bootstrap `$4800` muszą być ładowane przy
  **tym samym** wyborze banku (PORTB) — bootstrap czyta ten sam bank.
- Kod czyszczący `$3A00` musi zachować A/X/Y i flagi; jest wywoływany jako
  INIT przed każdym z 64 banków.
- Każdy INIT musi przywrócić PORTB (albo oddać sterowanie bezpowrotnie).
- Ekran ładowania nie może kolidować z segmentami runtime; obecnie leży
  w `$3800–$38FF`, ponad obrazami `$3300`/`$3400`.

### 4.3. Rozmiary (referencyjne)

| Plik | Rozmiar |
| --- | ---: |
| `build/visual-prototype-dev.xex` (baza 64 banków) | ~1 111 730 B (1.06 MiB) |
| `releases/less-i-know-demo-release-048-stereo.xex` | 936 121 B |
| `releases/less-i-know-demo-release-018-stereo.xex` (historyczny) | 935 472 B |
| `releases/avg-final-segment-trace-001.xex` | 938 896 B |

`[ODCZYT]` Historyczny release 018: 1775 segmentów, 64 bloki banków,
INIT-y `$38A0`×1, `$3900`×66, `$3A00`×64, `$4800`×1, RUN `$13E0`.
Release 048 jest aktualnym pakietem party; pełnego przebiegu na fizycznym
Atari nie potwierdzono.

## 5. Czego ta dokumentacja nie potwierdza

- `[OGRANICZENIE]` Potwierdzony jest **start** wersji kompaktowej z późnym
  startem na fizycznym Atari z AVG; nie ma potwierdzenia pełnego przebiegu,
  płynności ani odsłuchu na sprzęcie.
- `[OGRANICZENIE]` Dokładna przyczyna awarii starszych buildów (1.06 MiB,
  start przez RUNAD) nie została rozstrzygnięta — zmianie uległy
  jednocześnie rozmiar pliku i sposób startu.
- `[OGRANICZENIE]` Testy py65 i Atari800 nie modelują fizycznego loadera AVG,
  DMA ani zachowania write-only rejestrów.
