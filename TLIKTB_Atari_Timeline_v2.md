# The Less I Know The Better - Atari XE 1MB Demo Timeline (v2)

Wersja poprawiona po analizie `less-i-know-release-v035-preview.mp3` i playera `less-i-know-hook-v024.xex`.

## Założenia

- PAL (VBI ok. 49,86 Hz, nie 50,0 Hz)
- 128 BPM, 5:00 = 300 s, 160 taktów, takt = 1,875 s
- Player: 4 aktualizacje POKEY na klatkę PAL, ok. 199,44 Hz
- 373,95555 aktualizacji playera na takt; granica taktu `n` to pierwszy cały tick nie mniejszy niż `n × 373,95555`
- Takt ma ok. 93,5 klatki PAL (poprzednio 93,75 przy założeniu 50 Hz, co dawało dryf ok. 0,8 s na całym utworze)
- Siatka rytmiczna mp3 jest stała (128 BPM bez dryfu), takt n zaczyna się w n × 1,875 s

## Synchronizacja

- Zegarem głównym jest licznik ticków playera (24 bity, `$24A7-$24A9` w v024; adres zweryfikować w kodzie v035). Zdarzenia timeline'u wyzwalaj po tickach, nie po klatkach VBI.
- Z odczytu kodu v024 wynika, że licznik rośnie tylko w ścieżce odtwarzania, więc pauza powinna go zatrzymać, a wideo zatrzymałoby się razem z muzyką. To wniosek z kodu, nie test: do sprawdzenia w emulatorze (zadanie V4 w `TLIKTB_Technical_Constraints.md`).
- Przeliczenie granic: `tick(n) = ceil(n × 373,95555)`. Zaokrąglamy po wyznaczeniu absolutnej pozycji, a nie osobno długość każdego taktu.

## ACT 1 - SCHOOL DAYS
Takty: 0-24 | Ticki: 0-8975

- 1A (takty 0-8, ticki 0-2992): logo szkoły, panorama boiska, scroll chmur
- 1B (8-16, 2992-5984): cheerleaderka pojawia się pierwszy raz, Trevor w tle
- 1C (16-24, 5984-8975): po zniknięciu dziewczyny za drzwiami cięcie do wnętrza sali; chłopcy trenują koszykówkę, dziewczyny rozciągają się przy drabinkach. Animowana piłka: rzut i odbicie. Realizacja w v010; taniec zaczyna się bez przesunięcia, przy ticku 8975.

## ACT 2 - CRUSH
Takty: 24-56 | Ticki: 8975-20942 (zmiana: było 24-48)

Granice podakt wynikają ze zmian w muzyce w taktach 32, 40 i 56. W takcie 48 nie ma wyraźnego markera.

- 2A (24-32, 8975-11967): zbliżenia cheerleaderki, serduszka
- 2B (32-40, 11967-14959): patterny psychodeliczne
- 2C (40-56, 14959-20942): PMG animacje twarzy (blink, hair_anim), wariant twarzy co 4 takty

## ACT 3 - BASKETBALL HERO
Takty: 56-64 | Ticki: 20942-23934 (zmiana: było 48-64)

Muzyka ma zmianę w 56 i spadek gęstości uderzeń w 60.

- 3A (56-60, 20942-22438): kozłowanie
- 3B (60-64, 22438-23934): wsad, światła stadionu

## ACT 4 - TREVOR AWAKENS
Takty: 64-88 | Ticki: 23934-32909

- 4A (64-72, 23934-26925): cichy fragment (głośność spada o ok. 8 dB, szeroka stereo, więcej basu). Trevor wyłania się z tła, ciemna paleta, powolne wejście; zmiana pozy w takcie 68, tick 25429.
- 4B (72-88, 26925-32909): w takcie 72 wraca pełna energia (najsilniejsza zmiana strukturalna w utworze). Zoom PMG, rotacje i sinusy.

## ACT 5 - PSYCHEDELIC BREAKDOWN
Takty: 88-120 | Ticki: 32909-44875

Podział na 4 bloki odpowiada 4 efektom. Zmiany w muzyce w 92, 104, 108 i 116.

- 5A (88-104, 32909-38892): Kaleidoscope. W takcie 92 (tick 34404) zmiana źródła lub trybu odbicia.
- 5B (104-112, 38892-41884): Tunnel. W takcie 108 (tick 40388) zmiana tekstury.
- 5C (112-116, 41884-43379): Trevor Mosaic (głośność spada o ok. 2 dB w 112-119)
- 5D (116-120, 43379-44875): Eyes Sequence
- GTIA9: do decyzji, w którym bloku. W asset list brak dla niego assetów.

## ACT 6 - LOVE TRIANGLE
Takty: 120-128 | Ticki: 44875-47867 (zmiana: było 120-136)

- 6A (120-124, 44875-46371): komiksowe kadry (panel_left, panel_center, panel_right, pozy postaci)
- 6B (124-128, 46371-47867): Trevor vs koszykarz

## ACT 7 - TREVOR WINS
Takty: 128-144 | Ticki: 47867-53850 (zmiana: było 136-152)

Najgłośniejsza część utworu zaczyna się w takcie 128 (ok. 3 dB głośniej), szczyt jest w 136-143.

- 7A (128-136, 47867-50858): neon glow, narastanie
- 7B (136-144, 50858-53850): gigantyczny Trevor, flash, kulminacja

## ACT 8 - OUTRO
Takty: 144-160 | Ticki: 53850-59833 (zmiana: było 152-160)

W takcie 144 muzyka się zmienia. Wyciszenie dopiero w 158-159.

- 8A (144-152, 53850-56842): credits (logo_group, logo_music, logo_sv)
- 8B (152-158, 56842-59085): greetz
- 8C (158-160, 59085-59833): flash i fade do czerni, koniec utworu

## Tabela zdarzeń dla silnika

| Takt | Tick | Zdarzenie |
|---|---|---|
| 0 | 0 | start, Act 1 |
| 8 | 2992 | 1B |
| 16 | 5984 | 1C |
| 24 | 8975 | Act 2 / 2A |
| 32 | 11967 | 2B |
| 40 | 14959 | 2C |
| 56 | 20942 | Act 3 / 3A |
| 60 | 22438 | 3B |
| 64 | 23934 | Act 4 / 4A |
| 72 | 26925 | 4B (uderzenie) |
| 88 | 32909 | Act 5 / 5A |
| 92 | 34404 | zmiana w kalejdoskopie |
| 104 | 38892 | 5B tunnel |
| 108 | 40388 | zmiana tekstury tunelu |
| 112 | 41884 | 5C mosaic |
| 116 | 43379 | 5D eyes |
| 120 | 44875 | Act 6 / 6A |
| 124 | 46371 | 6B |
| 128 | 47867 | Act 7 / 7A |
| 136 | 50858 | 7B |
| 144 | 53850 | Act 8 / 8A |
| 152 | 56842 | 8B greetz |
| 158 | 59085 | 8C fade |
| 160 | 59833 | koniec |

## Zmiany względem v1

1. Zegar po tickach playera, nie po klatkach (93,75 klatki na takt zastąpione 93,5).
2. Act 2 wydłużony do taktu 56, Act 3 skrócony do 8 taktów.
3. Act 4 podzielony na ciszę (64-72) i uderzenie (72-88).
4. Act 5 podzielony na 4 efekty.
5. Act 6 skrócony do 8 taktów, Act 7 zaczyna się w 128.
6. Act 8 wydłużony do 16 taktów, zaczyna się w 144.

## Do weryfikacji

- Granice wynikają z analizy energii i brzmienia mp3, nie z odsłuchu melodii. Przesłuchaj punkty zmian: 24, 32, 40, 56, 64, 72, 88, 92, 104, 108, 112, 116, 120, 128, 144, 158.
- Plik .xex to v024, a mp3 to v035. Sprawdź, że licznik ticków w nowym buildzie daje te same punkty.
- Koszt CPU ticków muzyki (4 na klatkę) i konflikt o DLI z efektami (tunel, zoom, rotacje) trzeba zmierzyć w Altirze.
- Pamięć przestanie być wąskim gardłem po przycięciu loadera playera do 7 banków. Zakłada to, że player nigdy nie czyta banków 8-14, czego z kodu nie wykluczono testem (zadanie V3 w `TLIKTB_Technical_Constraints.md`).
- Szczegóły techniczne, stan wiedzy i zadania weryfikacyjne: `TLIKTB_Technical_Constraints.md`.
