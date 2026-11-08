# V142 — szarfy z boku i osobny projekt pomponiar

## Obraz i synchronizacja

[ODCZYT] Zgodnie z decyzją użytkownika taniec z pomponami w 8975–11967
(~0:45–1:00, takty 24–32) zastąpiono bocznym ujęciem dziewczyny ze szarfą.
Patrzy w lewo i robi kroki do tyłu. Kamera utrzymuje ją po prawej stronie
kadru, sala przesuwa się w lewo: ściana o 4 piksele na fazę, podłoga o 2.
Osiem nowych ilustracji i 16 faz tła tworzy cykliczny przejazd. Pętle tęczy
powstają na czterech players, a kolorowe iskry na missiles.

[ODCZYT] Późniejsze ujęcia 14959–20942 zyskują pozycje 32–35: dodatkowy
skręt bioder i przykucnięcie w grupie, skręt w solówce oraz dodatkowy ruch
grupy przed wyrzutem. Wszystkie trzy ujęcia mają rozszerzoną choreografię.
Łącznie 36 kompozycji: 16 bocznych i 20 późniejszych, każda 160×64,
powtarzana przez ANTIC trzykrotnie w pionie. Nie jest to 36 unikalnych póz
ciała: kompozycje uwzględniają także ruch tła i układ grupy.

[ODCZYT] Granice scen, końcowy wyrzut bohaterki, zegar muzyki i cztery
muzyczne DLI pozostają w zatwierdzonych pozycjach. Boczne klatki wybiera
faza `(tick >> 4) & 15`; późniejszy taniec pozostaje na granicach półuderzeń.
Cache sprawdza również właściciela aktywnego display list, by numery klatek
szarf nie kolidowały przy skoku z innego ujęcia. Oba bufory PMG i bitmap
zachowują regułę przygotowania nieaktywnego obszaru przed publikacją.

## Bilans względem v141

| Obszar | V141 | V142 | Różnica |
|---|---:|---:|---:|
| Dawne sześć banków pomponiar | 98 304 B | 92 160 B szarf | −6144 B |
| Bitmapy szarf w bankach Trevora | 40 960 B | 0 B | −40 960 B |
| Kontroler szarf | 1527 B | 1762 B | +235 B |
| Kotwice PMG | 128 B | 288 B | +160 B |
| Główny kod niebankowany | 2484 B | 2560 B | +76 B |
| **Odzysk netto** | | | **46 633 B = 45,54 KiB** |

[ODCZYT] Usunięcie samych bitmap pomponiar uwalniałoby 96 KiB. Nowy materiał
zużywa 90 KiB, ale obejmuje również późniejsze szarfy, zajmujące dotąd kolejne
40 KiB. Stąd 46 KiB zwolnionych slotów, pomniejszone o 471 B dodatkowego
kodu i kotwic. Źródłowy PNG/RGB na dysku nie jest pamięcią Atari.

[ODCZYT] Wolne miejsca mają konkretnych właścicieli:

- Oryginalne banki playera 9–14, indeksy tablicy `$26FC` 8–13:
  sześć bitmap po 2560 B pod `$4000–$7BFF`, wolne `$7C00–$7FFF` (6 × 1024 B).
- Banki loadera 24–39 (inna numeracja): ponownie wolne `$4A00–$53FF`
  (16 × 2560 B). Art i kod Trevora pozostają poza tymi slotami.
- Bank loadera 49: kontroler `$5400–$5AE1`, kotwice `$7E00–$7F1F`.
  Strumienie PMG `$6A00–$7DFF` i helper ciosów `$6000–$69FF` bez zmian.

[ODCZYT] Nadal przydzielone są wszystkie 64 banki. XEX ma 1 109 098 B,
o 76 B więcej niż v141; nie przycięto loadera ani wymagań sprzętowych.
Odzysk dotyczy miejsca na następne dane. Kod `$1400–$1DFF` zajmuje już cały
slot przed pulą wierszy od `$1E00`; wymaga pilnowania przy następnych zmianach.

## Pomponiary zachowane osobno

[ODCZYT] `projects/pompom-dance` to samodzielny projekt z własnym playerem,
źródłami obu grafik, generatorem, Makefile, testami, mapą RAM i numerowanym
`build/pompom-dance-v001.xex`. Nie importuje niczego z katalogu nadrzędnego.
Referencja 12 klatek (98 304 B) pochodzi bezpośrednio z banków v141;
generator sprawdza pełną zgodność bajtów. `reference/provenance.json`
zawiera sumy źródeł. Oryginalne wydanie v141 również pozostaje zachowane.

Archiwum do przeniesienia: `build/pompom-dance-project-v001.zip` (2 528 481 B).
Rozpakowano je do osobnego katalogu w `/tmp`, zbudowano od źródeł i wykonano
3/3 testy bez plików katalogu nadrzędnego. Odtworzony XEX ma identyczny
SHA-256 jak zamrożony v001.
Samodzielny pokaz zapętla wejścia jednej, dwóch i trzech dziewczyn od początku
oryginalnej muzyki. Nie przenosi pozostałych scen dema. Ma prostszy renderer
pełnej kopii 8 KiB; nie należy utożsamiać jego kosztu CPU z dawnym dirty-copy.

## Walidacja

[ODCZYT] `make check`: 100 testów, 97 zaliczonych, 3 pominięte z powodu
braku archiwalnego v126; 80,715 s. Testy obejmują wszystkie 16 bocznych
klatek, dwa tempa scrolla, granice ujęcia, nowe późniejsze pozy, odzyskane
sloty, cache po skokach między scenami i ochronę aktywnych buforów. NMI
muzyki wstrzykiwane także podczas kopii nowego bocznego ujęcia: PORTB
odtworzony, wynikowa bitmapa zgodna. Symulacja zmiennego VCOUNT sprawdza
okno publikacji PMG; py65 nie modeluje DMA ANTIC.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 297 256
identycznych bajtów względem v035, cały utwór. Osobny projekt: 3/3 testy,
16 312 896 identycznych bajtów POKEY przez cały utwór. To porównanie
rejestrów; bez odsłuchu i bez próby na fizycznym Atari. Do oceny płynności
pozostaje odtworzenie XEX-a w docelowej konfiguracji.

Podgląd `build/v142-side-ribbon.gif` pochodzi z 64 kolejnych callbacków
6502, co 4 ticki. `build/v142-side-storyboard.png` pokazuje cztery fazy.
Paleta i tempo są przybliżone; GIF nie pokazuje czasu kopiowania ani DMA.

## Źródła i wydania

Nowa grafika powstała w built-in imagegen na podstawie stroju z wcześniejszego
arkusza v136. Proceduralne tło i szarfy powstają w `tools/ribbon_dance.py`.

- Grafika: `assets/art/source/act2_ribbon_side_v142.png`.
- Opis generacji: `assets/art/source/act2_ribbon_side_v142.prompt.txt`.
- Główne wydanie: `build/visual-prototype-v142.xex` i JSON.
- Pomponiary: `projects/pompom-dance/build/pompom-dance-v001.xex` i JSON.

SHA-256 głównego XEX:
`f7733c3f766a38664dc7169bccc74f17b722221aaca8da10c4ac980a9619db36`.
Zgodny bajt w bajt z buildem roboczym użytym do pełnej walidacji.
