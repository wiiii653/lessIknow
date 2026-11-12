# 3. Ekran ładowania

## 3.1. Gdzie leży

`[ODCZYT]` W obecnym buildzie (release 018) ekran jest przeniesiony do
wysokiej pamięci przez `tools/build_init_trace_high.py`:

| Adres | Rozmiar | Zawartość |
| --- | ---: | --- |
| `$3800–$3877` | 120 B | trzy wiersze po 40 znaków (ATASCII − 32) |
| `$3880–$388A` | 11 B | display lista ANTIC 2 |
| `$38A0–$38DC` | 61 B | INIT ustawiający ekran i kolory |
| `$02E2` | 2 B | `$38A0` |

`[ODCZYT]` W źródle (`tools/loading_screen.py`) adresy są parametrami
modułu: `SCREEN=0x0600`, `DLIST=0x0700`, `ENTRY=0x0780`. Etap 2 nadpisuje
je na `$3800`/`$3880`/`$38A0`, żeby nie kolidowały z segmentami runtime
i żeby przeżyły ładowanie banków.

## 3.2. Display lista

`[ODCZYT]` 11 bajtów:

```
70 70 70                         3 × 8 pustych linii
42 00 38                         tryb 2 + LMS $3800
02 02                            dwie kolejne linie trybu 2
41 80 38                         JVB do $3880
```

Tryb 2 ANTIC to tekst 40 kolumn. Każda linia zajmuje 40 bajtów ekranu
(1 znak = 1 bajt), więc trzy wiersze to 120 bajtów od `$3800`.

## 3.3. Inicjalizacja

`[ODCZYT]` INIT `$38A0` zapisuje cienie OS **i** rejestry GTIA/ANTIC:

| Rejestr | Cień OS | Rola |
| --- | --- | --- |
| `$D400` | `$022F` | DMACTL — `$22` (włączone DMA playfieldu i DL) |
| `$D402/$D403` | `$0230/$0231` | DLIST |
| `$D409` | `$02F4` | **CHBASE** — `$E0` czyli font ROM `$E000` |
| `$D016…$D01A` | `$02C4…$02C8` | COLPF0–3 i COLBK |

### Ważna poprawka: CHBASE to `$D409`, nie `$D018`

`[ODCZYT]` `$D018` to **COLPF2** (kolor tekstu w trybie 2), a
`$D01A` to COLBK (tło). CHBASE — adres zestawu znaków — jest pod `$D409`,
a jego cień OS pod `$02F4`.

`[ODCZYT]` W pierwszej wersji `tools/loading_screen.py` wpisywano
`$D018=$00`, czyli **kolor tekstu = czarny**. Przy czarnym tle napis był
niewidoczny mimo poprawnego CHBASE. Zmiana na `$E0` rozjaśniła litery.

`[WNIOSEK]` Wcześniejsza diagnoza „zły CHBASE powodował puste znaki” była
błędna. Poprawny opis: czarny tekst na czarnym tle. Poprawkę merytoryczną
zawiera `docs/V272_SLEDZENIE_INIT_AVG.md`.

## 3.4. Obecna paleta

`[ODCZYT]` Najnowsza wersja `tools/loading_screen.py` (po zmianach z
2026-11-12 03:00) ustawia ciemnoniebieskie tło i ciepłe litery:

| Rejestr | Wartość |
| --- | --- |
| COLPF0 | `$38` |
| COLPF1 | `$2C` |
| COLPF2 | `$88` |
| COLPF3 | `$9C` |
| COLBK | `$82` |

`[OGRANICZENIE]` Release 018 powstał **przed** tą zmianą — w nim
COLPF1=`$0E`, COLPF2=`$E0`, tło domyślne. Nowa paleta wejdzie dopiero do
następnego builda po ponownym przejściu potoku.

## 3.5. Tekst

`[ODCZYT]` Release 018 zawiera trzy wiersze:

```
THE LESS I KNOW THE BETTER
SILLY VENTURE 2026 WE
AI-SLOP/OGNJEN
```

`[ODCZYT]` Najnowszy `loading_screen.py` ma już nowy tekst:

```
THE LESS I KNOW THE BETTER
LOADING BANKS / ATARI XE STEREO
PRODUCED BY OGNJEN / SILLY VENTURE 2026
```

## 3.6. Wiersz postępu INIT

`[ODCZYT]` Wrapper `$3900` (etap 2) nadpisuje **drugi** wiersz ekranu
(`$3828–$384F`) tekstem:

```
INIT nn ENTER  $xxxx
INIT nn RETURN $xxxx
```

Dzięki temu widać, który INIT właśnie się wykonuje, a po powrocie — że
wrócił. To narzędzie diagnostyczne; w buildzie produkcyjnym można je
usunąć, pomijając etap 2.

## 3.7. Ryzyka

- `[ODCZYT]` Ekran `$3800–$3877` leży **powyżej** obrazów `$3300`/`$3400`
  i nie koliduje z nimi.
- `[ZAŁOŻENIE]` Jeśli w przyszłości jakiś segment runtime zacznie używać
  `$3800–$38FF`, ekran i wrapper trzeba przenieść; obecnie jest to wolny
  obszar w tym buildzie.
- `[ODCZYT]` Wrapper zapisuje tylko wiersz 1; nie rusza wierszy 0 i 2,
  więc tytuł i credits pozostają widoczne.
