# V127 — optymalizacja kopii, display list i PMG

[ODCZYT] Wydanie: `build/visual-prototype-v127.xex`. SHA-256:
`7a344c4aa5afe7fe8f2acc15e7164498bb1ed20edfa6d8ac149d1da7b8370d5b`.
V126 pozostaje zachowane i niezmienione. Roboczy build `visual-prototype-dev.xex`
jest identyczny bajtowo z v127. Nie zmieniono granic scen, ticków ani materiału graficznego.

## Zmiany silnika

- Wspólny kod poza oknem bankowania kopiuje pięć stron na obrót indeksu.
  Parallax i Trevor kopiują dwie takie grupy, mozaika trzy. Zastępuje to
  pętle wykonujące INY/BNE po każdym bajcie osobnej strony.
- Dwie niezależne etykiety układu display list pozwalają pominąć budowanie
  192 adresów LMS, gdy nieaktywny DL ma już wymagany układ. Mozaika,
  tripled-64 (parallax/Trevor), koszykarz i portrety mają osobne klucze.
  Renderer zwykłych scen unieważnia oba klucze przed zmianą adresów.
  Cache układu DL nie zastępuje cache zawartości framebufferów.
- Faza kolorów mozaiki używa dzielenia przez malejące wielokrotności 187:
  osiem kroków zamiast rosnącej liczby odejmowań. Bazy 11968/32912,
  przesunięcie palety i faza pulsowania pozostają zgodne z v126.
- Czyszczenie PMG w koszykarzu, portretach i BANG używa pięciu rozłącznych
  odcinków po 128 B. Usuwa podwójne zapisy do $0A00–$0A7F i zmniejsza
  liczbę iteracji z 256 do 128. Końcowe dane $0980–$0BFF są identyczne.
- Koszykarz kopiuje ogon bitmapy bez JSR/RTS i ponownego przepisywania
  operandów na każdy z 192 bajtów.
- Emiter odrzuca powtórzone etykiety zamiast cicho zmieniać ich adresy.

[ODCZYT] Rezerwacja $0C00–$0DFF na helper kopii, sprawdzanie kluczy i klucze
$0DFE/$0DFF. Pula pakowanych wierszy zaczyna się w tym fragmencie od $0E00;
kontrola kolizji obejmuje helper. Kod głównego callbacku rośnie z 1822 do
1830 B. Kod nadal mieści się w dotychczasowych limitach i tych samych bankach.
Wspólny helper nie zmienia PORTB; wrapper NMI nadal przywraca bank foreground.

## Wyniki CPU

[ODCZYT] Ten sam zestaw 589 próbek co w audycie v126. Dane surowe:
`AUDIT_V126_CYCLES.json` i `V127_CYCLES.json`. Maksimum dotyczy badanego
fragmentu, a suma obejmuje także trafienia cache i pierwsze napełnienia.

| Fragment | Maksimum v126 | Maksimum v127 | Mniej cykli maksimum | Mniej cykli sumy próbek |
|---|---:|---:|---:|---:|
| Parallax | 53 684 | 43 511 | 19,0% | 21,1% |
| Mozaika | 73 698 | 58 255 | 21,0% | 25,8% |
| Portrety | 130 470 | 129 065 | 1,1% | 8,7% |
| Koszykarz | 66 049 | 56 004 | 15,2% | 24,8% |
| Trevor | 55 496 | 44 046 | 20,6% | 31,5% |
| Późna mozaika | 78 378 | 58 525 | 25,3% | 37,5% |

[ODCZYT] Liczba wywołań ponad 35 568 cykli spadła z 10 do 2 na 75 próbek
parallaxu oraz z 15 do 2 na 75 próbek Trevora. Pozostałe fazy nadal mogą
przekraczać budżet jednej ramki. Intro/tytuł/szkoła/taniec/trening mają do
10 cykli dodatkowego kosztu na przebudowę DL wskutek unieważniania kluczy;
ich główne pętle renderowania nie zostały przyspieszone. Na początku mozaiki
bounded division może kosztować więcej niż krótka stara pętla (minimum
7842 zamiast 7698); usuwa natomiast narastający koszt późnej części utworu.

[ZAŁOŻENIE] To pomiary instrukcji CPU w py65: bez ANTIC DMA, muzycznych NMI
oraz rzeczywistego oczekiwania na raster. Suma próbek nie jest procentem
przyspieszenia całego dema ani wynikiem FPS. Dla porównania na emulatorze
ze sprzętowym czasem pozostaje zmierzenie momentów prezentacji i pominiętych faz.

## Weryfikacja

[ODCZYT] `make check PYTHON=/tmp/atari-audit-venv/bin/python`: **83 testy OK**,
88,662 s. Obejmuje dotychczasowe testy pikseli, aktywnego bufora, bankowania,
muzycznych przerwań oraz trzy nowe testy regresji:

- raster, rejestry GTIA i pamięć PMG kontra archiwalne v126 przy granicach
  scen, restartach oraz 40 deterministycznych losowych skokach ticka;
- zgodność palet na granicach beatów i pulse, dla obu baz fazy kolorów;
- pomijanie zapisów LMS po rozgrzaniu obu układów i spadek łącznego kosztu
  aktualizacji w badanych scenach.

Poprawiono stare oczekiwanie `tick >> 5` na `tick >> 4` wyłącznie dla pozy
TAŃCA w teście przejść. Wybór drugiej połowy motywu mozaiki zachowuje `>>5`.

[ODCZYT] Atari800 PAL/1088XE, stereo POKEY, Altirra OS:
`tools/check_playback.py --seconds 12` — PASS, **3 637 368 identycznych bajtów**,
około **1013,2 s** emulacji, cały utwór. Testowano końcowy roboczy build,
identyczny z v127. To zgodność rejestrów, nie odsłuch na fizycznym Atari.

## Budowanie i powtarzanie pomiaru

`make` generuje teraz nadpisywalny build `visual-prototype-dev.xex` wraz z JSON.
Oba są wspólnym celem Make, zależnym od narzędzi i wszystkich plików atlasów.
`make check` wymaga py65 zamiast pozwalać na pominięcie testów CPU.
Numerowane wydania tworzymy jawnym `--output` bez `--replace`.

```sh
make all PYTHON=/tmp/atari-audit-venv/bin/python
make check PYTHON=/tmp/atari-audit-venv/bin/python
/tmp/atari-audit-venv/bin/python tools/profile_engine.py --xex build/visual-prototype-v126.xex --output /tmp/v126-cycles.json
/tmp/atari-audit-venv/bin/python tools/profile_engine.py --xex build/visual-prototype-v127.xex --output /tmp/v127-cycles.json
```

## Pozostały potencjał

Największe dalsze tematy z audytu: przygotowanie rozszerzonych portretów przed
sceną, mniejsze aktualizacje tańca oraz ograniczenie przebiegów kompozycji
plazmy. V127 nie wdraża tych zmian formatów danych. Obecny etap usuwa wspólny
narzut i daje sprawdzoną bazę do tych bardziej rozległych optymalizacji.
