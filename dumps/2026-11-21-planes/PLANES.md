# Płaszczyzny — zrzut runtime i warstwy źródłowe

Data: 2026-11-21. Źródło runtime: `build/visual-prototype-dev.xex`
(SHA-256 `435b801c9f8c1b3310c92b89c936d07526522153216f80452ca0c6fcf893e746`).
Wydanie referencyjne: `releases/less-i-know-demo-release-126-stereo.xex`.

Ten katalog **nie powtarza** zrzutu bitmap z `dumps/2026-11-21/`. Zawiera
dokładnie to, czego tam nie było: prawdziwe płaszczyzny runtime oraz — osobno,
wyraźnie oznaczone — warstwy źródłowe builda.

## 1. `runtime/` — płaszczyzny z pamięci dema

Każdy moment powstał przez uruchomienie prawdziwego callbacku 6502 w py65 dla
wybranego ticku, a nie przez rysowanie „na oko”.

```
runtime/<moment>/
  playfield.png            bitmapa ANTIC 160×235, bez PMG (indeksy 1:1)
  playfield@4x.png         podgląd
  composite.png            playfield + PMG w przybliżonym priorytecie GTIA
  pmg/p0..p3.png           P0–P3 w przestrzeni ekranu (RGBA, alfa = pixel)
  pmg/p0..p3@4x.png
  pmg/p0..p3-stored.png    surowa strona 8×128 px (8 px × linie PMG)
  pmg/m0..m3.png           M0–M3 w przestrzeni ekranu
  pmg/raw/p0..p3.bin       dokładne 128 B strony z pamięci
  pmg/raw/missiles.bin     dokładne 128 B strony missiles
  background/…             czyste tło z banku, gdy istnieje osobno
  overlay/…                osobne bitmapowe overlaye (bok tancerki, maski liter)
  state.json               rejestry: pozycje, rozmiary, kolory, PRIOR, $D400, adresy

stored-overlays/portraits/  4 zapisane portrety 80x52 (publikowane na cięciach)
```

| moment | tick | scena | co jest osobno |
|---|---:|---:|---|
| 01-artist-plasma | 96 | 0 | plazma + maski liter + PMG fajerwerki |
| 02-title-plasma | 1592 | 1 | plazma + maski liter + PMG fajerwerki |
| 03-school | 2992 | 8 | brak PMG; postacie w bitmapie |
| 04-portrait | 3653 | 14 | brak PMG; twarz w bitmapie |
| 05-whistle | 4882 | 10 | 4 nuty na P0–P3 + iskry na M0–M3 |
| 06-practice | 7081 | 13 | tęczowa piłka na PMG; ilustracja w bitmapie |
| 07-dance-side | 9600 | 14 | `background/gym-24.png` + `overlay/side-4-*` + akcenty PMG |
| 08-dance-front | 15200 | 14 | taniec grupowy (front); tancerka w bitmapie + PMG |
| 09-kaleidoscope | 12000 | 6 | tunel w bitmapie + piłka PMG |
| 10-dance-group | 19000 | 14 | tancerka w bitmapie + akcenty PMG |
| 11-kiss | 20700 | 14 | serce na PMG; sala w bitmapie |
| 12-hero | 22100 | 15 | bohater/arena w bitmapie + piłka/satelity PMG |
| 13-trevor-bang | 26965 | 16 | Trevor/tunel w bitmapie + BUM na P0–P3 + M0–M3 |
| 14-bananas | 39000 | 6 | kiście w bitmapie + świecące punkty PMG |
| 15-final | 51500 | 17 | chłopiec w bitmapie + gwiazdy/nuty PMG; linie tekstowe pominięte |

Ważne:

- `playfield.png` to **to, co naprawdę pobiera ANTIC** z listy wyświetlania.
  W scenach z compositingiem CPU (bok tancerki, litery tytułu, portrety)
  zawiera już te warstwy. Do edycji tła użyj `background/` + `overlay/`.
- `pX-stored.png` i `raw/*.bin` to zapis dokładnie taki, jak w pamięci:
  128 B na playera (tryb dwuliniowy), 128 B na cztery missiles.
  Pozycje, rozmiary i kolory **nie są** w tej stronie — leżą w kodzie/tabelach
  i w rejestrach opisanych w `state.json`.
- PMG w tym demie jest dwubuforowe: aktywny adres wynika z `$D407`.
  W większości momentów jest to `$8A00`/`$8980`, w kalejdoskopie `$0A00`/`$0980`.

Portrety `stored-overlays/portraits/` to zapisane płaszczyzny 4×80×52,
kopiowane do bufora w scenie Crush; publikacja zależy od cięcia, dlatego nie
przypisano ich do jednej klatki.

## 2. `source/` — warstwy źródłowe builda (nie runtime)

Te pliki to wejścia, z których build składa pełne klatki. Są przydatne do
edycji tła pod postacią, ale **demo ich nie przechowuje** — w XEX są już
złożone bitmapy.

- `school/` — czyste tło 160×64 i 200×64, dziewczyna (cutout, dalsza, bliska,
  4 klatki chodu), chłopiec z alfą oraz trzy pełne klatki `school*.rgb`,
  w których chłopiec jest wpieczony.
- `dance/` — czysta sala 160×192, 4 pozy tancerki 48×128 z alfą, arkusze szarf
  (dancer, side, overhead, trzy warianty inbetweens) z zewnętrznym czarnym
  tłem zamienionym na alfę.
- `hero/` — 6 póz z `basketball-hero-v177.rgba` (arkusz produkcyjny; montaż
  używa klatek v175) oraz tło areny 160×56 i panorama 200×64.

Każdy plik RGBA ma bliźniaczą maskę `*-mask.png`. `manifest.json` zawiera
SHA-256 użytych źródeł.

## 3. Czego nie da się rozdzielić

- `practice`, `trevor`, `final`: pojedyncze ilustracje 160×192 / 160×64;
  nie istnieje czyste tło ani osobna maska postaci.
- `school`: chłopiec jest wpieczony w `school*.rgb`; dziewczyna ma osobną
  warstwę źródłową, ale nie runtime.
- `dance` przód: tancerka jest wpieczona w klatki banków 8–13.
- `hero`: bohater i arena to jedna bitmapa 160×56.
- `trevor`: panele i tunel mają Trevora w bitmapie.

## 4. Ponowne wgranie

- PMG: edytuj `pX-stored.png` (lub `raw/*.bin`) i spakuj z powrotem 128 B;
  pozycje/kolory ustawia kod sceny, nie strona.
- Bok tancerki: 952 B pikseli + 952 B maski w banku 24–31 pod `$4A00`/`$4E00`,
  wiersz 17 B, placement x=4, y=8.
- Warstwy źródłowe: po edycji uruchom build ponownie; kwantyzacja i maski
  przejdą te same ścieżki co dotychczas.
