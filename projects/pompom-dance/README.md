# Pompom Dance — samodzielny projekt Atari

Wydzielona scena pomponiar z TLIKTB v141. Zawiera własne źródła, obie grafiki
wejściowe, oryginalny player v035, referencyjne klatki, generator, testy
i gotowy `build/pompom-dance-v001.xex`. Nie wymaga plików projektu nadrzędnego.

## Uruchomienie

PAL, stereo POKEY, rozszerzenie zgodne z Atari800 `1088XE` (ta sama konfiguracja
testowa co główne demo), Altirra OS. W Altirrze wybierz 65XE/PAL z rozszerzeniem
1 MB i stereo POKEY. Projekt używa 14 banków po 16 KiB: 8 muzycznych i 6 grafiki.

```sh
atari800 -1088xe -pal -nobasic -run build/pompom-dance-v001.xex
```

Od początku muzyki zapętlane są wejścia jednej, dwóch i trzech dziewczyn,
w cyklu 2992 ticków (~15 s). Zachowano cztery pozy każdej grupy, cienie,
czterokolorową salę i akcenty PMG. To osobny pokaz sceny; nie zawiera pozostałych
aktów głównego dema. Muzyka pozostaje pełnym utworem v035.

## Budowanie i weryfikacja

Python 3, GNU Make i ImageMagick (`convert`):

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
make all PYTHON=.venv/bin/python
make check PYTHON=.venv/bin/python
```

`make all` tworzy wymienialny `build/pompom-dance-dev.xex` i JSON. Numerowanych
wydań nie nadpisuj. Nowe wydanie:

```sh
.venv/bin/python tools/build_pompom_demo.py --output build/pompom-dance-v002.xex
```

`reference/dance_frames_v141.bin` zawiera dokładnie 98 304 B: 12 klatek po
8192 B. Generator odmawia budowy, jeżeli odtworzona grafika różni się choćby
bajtem. `reference/provenance.json` zapisuje sumy źródeł i wyjściowego v141.

Testy sprawdzają wszystkie grupy i pozy przez wykonanie kodu 6502, identyczność
referencji, banków muzycznych i odstępów czterech DLI. Kopia pełnej bitmapy
jest przygotowywana w nieaktywnym buforze; ten projekt nie używa optymalizacji
dirty-pages głównego dema. Tempo callbacków wymaga oceny w emulatorze/sprzęcie.

Porównanie muzyki wymaga Atari800 i ROM-u Altirra OS. Ścieżki oraz ustawienia
znajdują się w `tools/check_playback.py`; w środowisku macierzystym polecenie
`make playback PYTHON=/path/to/python` korzystało z dostępnego wrappera Atari800.

## Wyniki v001

[ODCZYT] 3/3 testy zaliczone. Oryginalna grafika wszystkich 12 klatek zgodna
bajt w bajt z v141. Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
16 312 896 identycznych bajtów względem v035; cały utwór.
Nie przeprowadzono testu na fizycznym Atari ani pomiaru FPS z DMA ANTIC.

XEX: 253 197 B, SHA-256:
`47c558dd06ba0bf2163b69e7d6bf8441e9fe1589d4f819d2df2e763a731ee8e5`.

Mapa RAM: callback `$1000`, stan `$13E0`, display lists `$1400`/`$1800`,
efekty `$1C00`, bufory bitmap `$8000`/`$A000`, PMG `$0980–$0BFF`.
Archiwalne notatki rozwoju sceny znajdują się w `docs/`; opisują wcześniejszy
silnik głównego projektu, a powyższa mapa dotyczy samodzielnego v001.
