# V182 — spojrzenie, odwrócenie i gwizd

Reakcja chłopca jest podzielona na trzy odrębne pozy, przy zachowanym
kadrowaniu oraz torze dziewczyny z v181:

| Tick | Reakcja |
|---|---|
| 2992, 4114 | Patrzy przed siebie; źródło `act1_boy_front.png`. |
| 4488 | Ogląda się przy mijaniu w pierwszym planie. |
| 4862, 5236 | Nadal patrzy za oddalającą się dziewczyną. |
| 5610 | Dziewczyna jest przy drzwiach: dziubek, mrugnięcie i nuty. |

Spokojna odwrócona poza korzysta z `act1_school_court_boy.png`, a gwizd
z `act1_boy_front_v170.png`. Wszystkie portrety przechodzą przez bieżącą
maskę chroniącą włosy i kurtkę oraz szyld areny. Nuty dodawane są wyłącznie
do ostatniej pozy. Spacer boczny nadal odpowiada dokładnie v175.

- XEX: `build/visual-prototype-v182.xex`; para dev jest identyczna.
- SHA-256: `6675f18047cd8e8c4e6b2dca97b80d1acce8da9a7202ab4e1a7a1544385e7d6f`.
- 316 współdzielonych wierszy, 12 153 B danych wierszy, 2552 B kodu.
  Generator zakończył alokację w istniejących regionach. Nie dodano banków.
- Siedem testów CPU/renderowania zaliczonych: kolejność trzech póz i nut,
  krycie włosów/kurtki, dokładność panoramy v175 i jej zegar, kompozycja,
  pierwszy plan i tor do drzwi.
- Podgląd po callbackach 6502: `build/v182-boy-reaction-preview.png`.
  Nie modeluje DMA ANTIC. Nie wykonywano nowego odtwarzania w emulatorze;
  instalacja Atari800 ma znaną przeszkodę FUSE opisaną przy v181.
- Ticki i granice ujęć oraz dalsze akty pozostają bez zmian.
