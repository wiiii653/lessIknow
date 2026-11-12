# 6. Mapa pamięci i przydział banków

## 6.1. Adresy używane przez loader

| Zakres | Rozmiar | Właściciel / rola |
| --- | ---: | --- |
| `$0400–$07E4` | 997 B | runtime: tabele, bufory; odtwarzane z bufora |
| `$0800–$08BF` | 192 B | runtime: `bank_value`/tabele banków (`$08C3+`) |
| `$0900–$0974` | 117 B | runtime: PMG/dane pomocnicze |
| `$0980–$09FF` | 128 B | bufor PMG nr 1 (missiles) |
| `$0A00–$0BFF` | 512 B | bufor PMG nr 2 (players) |
| `$1000` | ~373 B | loader OS-RAM (INIT) |
| `$13E0–$13F0` | 17 B | stub startowy (`run_stub`) |
| `$1400–$1DFF` | 2560 B | główny kod scen |
| `$1E00–$1FFF` | 512 B | pula współdzielonych wierszy |
| `$2000–$24B2` | 1203 B | kod oryginalnego playera |
| `$24B3–$24B5` | 3 B | selektory banków 0–2 |
| `$24BD–$28BC` | 1024 B | tabele playera (m.in. `$26FC`, `$270A`, `$2734`) |
| `$3300–$3323` | 36 B | display lista playera |
| `$3400–$37BF` | 960 B | ekran playera |
| `$3800–$3877` | 120 B | ekran ładowania |
| `$3880–$388A` | 11 B | display lista ładowania |
| `$38A0–$38DC` | 61 B | INIT ekranu ładowania |
| `$3900–$398B` | 140 B | wrapper INIT (diagnostyka) |
| `$3A00–$3A24` | 37 B | czyszczenie `$8000–$BFFF` |
| `$4000–$47FF` | 2048 B | bufor niskiej pamięci |
| `$4800–$4873` | 116 B | bootstrap i `JMP $13E0` |
| `$8000–$BFFF` | 16 KiB | okno banku (dane banków) |
| `$C000–$CFFF`, `$D800–$FFFF` | 14 KiB | kopia ROM OS w RAM |

`[ODCZYT]` Adresy `$3800–$3AFF` są zajęte **tylko w buildach AVG**
(etap 2). W bazowym buildzie ekran ładowania leży w `$0600/$0700/$0780`.

## 6.2. Przydział 50 banków wideo

`[ODCZYT]` Kolejność z `tools/build_bitmap_sequence.py` (linie 866–886):

| Indeks | Zawartość |
| ---: | --- |
| 0 | klatka dziewczyny (school bank 0) |
| 1 | koszykarz (`basketball_hero`) |
| 2 | bank Trevora + `post_trevor_director` + `ribbon_inbetweens` |
| 3–18 | mozaiki/rotatory (16 banków, `mosaic.banks()`) |
| 19–23 | panorama szkoły (5 banków); w 19 dodatkowo `trevor_ball_flight` |
| 24–39 | aktorzy boczni szarf (16 faz); w 39 bitmapa finałowa |
| 40–48 | plansze tytułowe/plazma (9 banków); 40–41 fajerwerki; 46 i 48 to banki zasobów banana |
| 49 | kontroler szarf + kontroler finałowego chłopca |

`[ODCZYT]` Razem 50 banków dodatkowych (0–49) + 14 banków muzyki v035
= **64 banki**, czyli pełne 1 MB.

`[ODCZYT]` Wybrane stałe:

```
ribbon_dance.FIRST_BANK      = 8
ribbon_dance.SIDE_BANK       = 24
ribbon_dance.FRAME_COUNT     = 36
final_boy.BITMAP_BANK        = 39
title_plasma.FIRST_BANK      = 40
banana_cache.RESOURCE_BANK   = 46
banana_cache.SPARE           = 48
trevor_ball_flight.BANK_INDEX= 19
```

## 6.3. Gdzie zapisane są selektory banków

| Indeks | Adres selektora |
| ---: | --- |
| 0 | `$24B3` |
| 1 | `$24B4` |
| 2 | `$24B5` |
| 3–49 | `$08C3–$08F1` |

`[ODCZYT]` Odczyt w kodzie: `tools/school_portrait_bank.py`, funkcja
`bank_value(index)`:

```python
BANK_VALUE = 0x24b3
def bank_value(index):
    return BANK_VALUE + index if index < 3 else 0x08c0 + index
```

## 6.4. Banki muzyki v035

`[ODCZYT]` Oryginalny player wykrywa i ładuje 14 banków; ich selektory
trafiają do `$26FC–$2709`. Dekoder czyta 8 z nich (7 pełnych + 2820 B
ósmego), a banki 9–14 nie są odczytywane przez muzykę i demo wykorzystuje
je na grafikę.

`[ODCZYT]` Tabela selektorów na tej konfiguracji:

```
$26FC: 81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB
```

## 6.5. Tabele wskaźników playera

| Adres | Rola |
| --- | --- |
| `$270A–$2717` | 14 selektorów wariantu domyślnego |
| `$2718–$2725` | wariant „nie-81” |
| `$2734–$2741` | dolne bajty wskaźników konfiguracji |
| `$2737–$2744` | górne bajty wskaźników konfiguracji |

`[ODCZYT]` Kod `$201D–$2023` kopiuje 14 bajtów spod wskaźnika do
`$26FC–$2709`, więc zawartość `$2734/$2737` wybiera właściwą listę
dla danej maszyny.

## 6.6. Ograniczenia mapy

- `[OGRANICZENIE]` Adresy `$3800–$3AFF` są wolne **w tym buildzie**;
  nie ma gwarancji, że pozostaną wolne po dodaniu nowych scen.
- `[OGRANICZENIE]` Bufor `$4000–$47FF` leży w oknie banku i zajmuje
  2 KiB jednego z banków 1 MB — sprawdź, którego, jeśli dodajesz dane.
- `[ODCZYT]` Obszar `$0C00–$0F3F` jest zarezerwowany na runtime
  (kompozytor, selektory klatek); nie umieszczaj tam assetów.
