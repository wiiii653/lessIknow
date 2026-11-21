# Uwaga sprzętowa — 2026-11-17
Użytkownik potwierdził awarię surowego prototypu v353 na fizycznym Atari.
Do kolejnej próby przygotowano `releases/less-i-know-demo-release-062-stereo.xex`
z loaderem działającego 058. Zasady i rzeczywista walidacja:
[kontrakt loadera](HARDWARE_LOADER_CONTRACT.md). Sam prototyp poniżej nie jest
plikiem dystrybucyjnym na AVG.

# V353 — pierwszy szlif postaci po party

Prototyp stereo do oceny grafiki. Zachowuje montaż v352 i jego ticki playera.
Nie jest nowym wydaniem produkcyjnym ani paczką na Pouët.

## Zmiany obrazu

- Otwarcie: ręcznie zdefiniowana postać dziewczyny na siatce 48×64,
  osobna maska nieprzezroczystości oraz celowo narysowany daleki wariant
  12×16. Czarny piksel konturu pozostaje nieprzezroczysty; przestrzenie
  między nogami pokazują tło. Zachowano pozycje, skalę ujęć i Fuji na kurtce.
- Spacer przed areną: głowa, profil i włosy zastępują zaszumiony fragment
  kadru w 18 istniejących klatkach. Wokół nowej sylwetki odtwarzana jest
  czysta płyta areny z dotychczasowym przesunięciem parallax. Korpus,
  ręce, nogi, ticki i kierunek ruchu pozostają z zachowanych kadrów.
- Koszykarz: wybrane, jawnie wskazane ubytki wewnątrz materiału i skóry
  w pięciu klatkach źródłowych; łaty kozłowania dziedziczą poprawki.
  Nie stosowano filtra do całej postaci. Zachowano tablicę i łaty szkła,
  kontury, pozy, trajektorie piłki oraz renderer PMG.

## Pamięć i artefakty

Kod główny nadal zajmuje 2542 B od `$1400`, przed pulą pod `$1E00`.
Pula: 297 wierszy i 11 486 B (v352: 298 i 11 527 B). Zmieniają się
adresy części współdzielonych wierszy. Nadal przydzielone są wszystkie
64 banki; zmiany zawartości banków dotyczą indeksu loadera 15
(grafika koszykarza od `$4B80`) i 33–37 (kadry spaceru).
Nie zmieniano logiki kodu 6502, własności banków, zakresów PMG ani NMI.
Generator i testy pamięci sprawdziły nakładanie danych.

- XEX: `build/visual-prototype-v353.xex`, JSON obok.
- SHA-256: `d002ff99361640ac1bfe38c903e91e2e1a6945b0655fa8111024a061bd87dfb4`.
- Porównanie: `build/polish-audit/v353-review.png`; rozszerzone kadry:
  `build/polish-audit/before-after.png`. Obrazy odtworzono z bitmap
  po callbackach 6502 dla obu XEX. Kolory przybliżone, bez nakładek PMG
  i symulacji rastera; nie są zrzutami z fizycznego Atari.

## Wykonana walidacja

`make all PYTHON=/tmp/lessiknow-polish-venv/bin/python` oraz osobna budowa
numerowanego prototypu przeszły; dev i v353 mają identyczny SHA-256.

34 testy ukierunkowane przeszły: `test_girl_back_art`,
`test_school_parallax`, `test_basketball_hero`,
`test_basketball_v175_restore`, `test_memory_allocations`,
`test_display_lists`, `test_post_trevor_director`.

Pełne `make check`: 200 testów, 32 porażki i 1 błąd. Osobno wyeksportowano
niezmienione `tools/` i `tests/` z HEAD do `/tmp`, uruchomiono je z XEX/JSON
v352: 198 testów, te same 32 porażki i 1 błąd. Lista wszystkich 33 wpisów,
łącznie z podprzypadkami rastera, jest identyczna. Obejmują banany/cache,
loader, paletę Trevora, finał i piłkę/raster tunelu. Wynik nie oznacza,
że usterki są nieistotne; nie usuwano ich ani nie luzowano ich asercji.
Raport: `build/polish-audit/validation-v353.json`.

Atari800: PAL, emulowane 1088 XE, dwa POKEY, Altirra OS, turbo,
bez okna i odsłuchu, rejestracja stereo co 78 linii. Polecenie:

```sh
/tmp/lessiknow-polish-venv/bin/python tools/check_playback.py --seconds 15 --demo build/visual-prototype-v353.xex --reference build/visual-prototype-v352.xex --minimum-seconds 270
```

Wynik: **10 721 808 identycznych bajtów stereo**, ok. 2986,6 s
emulowanych, co obejmuje pełny przebieg i okres po zakończeniu montażu.
Nowe opcje `--reference` i `--minimum-seconds` pozwalają sprawdzać regresję
względem zapisanego dema; domyślne odniesienie nadal stanowi player v035.
Osobne porównania v353 i v352 z v035 dały tę samą pierwszą różnicę
na bajcie 935 784 (ok. 260,7 s, przy końcu montażu).
Nie ustalano tutaj przyczyny tej różnicy i nie deklarujemy pełnej zgodności
z v035.

Nie wykonano pełnego wizualnego odtwarzania, odsłuchu ani próby fizycznej.
py65 nie modeluje DMA ANTIC i fizycznych terminów rastera. Dotychczasowy
artefakt tablicy wsadu z audytu v347 pozostaje do osobnej naprawy.
Ostatnie potwierdzone sprzętowo wydanie nadal stanowi release 058 / v330;
plików wydań produkcyjnych nie zmieniano.
