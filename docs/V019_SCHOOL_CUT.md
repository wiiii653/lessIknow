# v019 — przebitka na dziewczynę przed szkołą

[ODCZYT] Wstawiono portret blondynki przed szkołą, z odłożonego materiału
`assets/art/source/act1_blonde_portraits_reserved_v014.png` (lewy górny kadr).
Nie generowano nowej ilustracji. Konwersja 160×64, każdy wiersz powtórzony
trzykrotnie, jak pozostałe obrazy przed szkołą.

| Ticki | Ujęcie |
| --- | --- |
| 2992–3552 | Chłopiec od przodu |
| 3553–3926 | Dziewczyna od przodu, przed szkołą |
| 3927–4487 | Powrót do chłopca od przodu |
| 4488–4861 | Dziewczyna pojawia się na pierwszym planie, chłopiec jeszcze patrzy przed siebie |
| 4862–5983 | Dziewczyna oddala się ku drzwiom, chłopiec ogląda się za nią |
| 5984 | Początek sali i treningu, bez przesunięcia |

## V2 / V3 — dodatkowy bank

[ODCZYT] Dotychczasowe 14 banków nie miało miejsca na kolejny pełny obraz.
Nowy INIT ładuje dodatkowe 8 KiB w kolejnym banku, zachowując PORTB.
Wartość banku zapisana jest pod `$24B3`, w przerwie między istniejącymi
segmentami playera. Dobór kontynuuje wykrytą tablicę PORTB: `$AA→$AC`,
`$C6→$CA` lub `$E6→$EA` (wartości runtime z wyłączonym OS).
Nie przesuwa ani nie nadpisuje banków 1–14. Dane trafiają do nieaktywnego
bufora istniejącą kopią, a NMI przywraca bank foreground.

## V1 / V6 — walidacja

[ODCZYT] 30 testów OK, w tym cała kolejność ujęć oraz ich piksele,
przejście do treningu i dotychczasowe testy sceny występu.
W Atari800 PAL `-1088xe` porównano pełne zrzuty pamięci: chłopiec,
przebitka na dziewczynę, podtrzymanie, powrót do chłopca, wejście i
oddalanie dziewczyny oraz cztery późniejsze kadry występu. Wszystkie
obrazy zgadzają się ze źródłami.

[ZAŁOŻENIE] Dwie pozostałe tablice rozszerzeń i fizyczne Atari wymagają
osobnego sprawdzenia; test emulatora dotyczy wskazanego `-1088xe`.
Podgląd: `build/v019-school-cuts.png`.

[ODCZYT] Porównanie pełnego utworu stereo POKEY w Atari800:
8 648 064 identyczne bajty, około 2409,0 s emulacji.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v019.xex --seconds 12
```
