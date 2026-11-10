# Wolne pamięci w bankach rozszerzenia — raport (stan v244)

Policzono wprost z gotowego artefaktu `build/visual-prototype-v244.xex`:
rozparserowano wszystkie sekcje XEX-a i wyodrębniono **50 obrazów banków**
(16 KiB każdy, ładowanych rozszerzonym ładowarką `school_portrait_bank`
do okna `$4000–$7FFF` komórki rozszerzenia), a dla każdego obrazu znaleziono
jednorodne strony (`00`/`FF`) i strefy bajtów wypełnienia. Wyniki
skonfrontowano z kodem generatorów (odczyt plików) i aktualnymi notami V
— bez uruchamiania buildera.

Oznaczenia: **[ODCZYT]** = zmierzone z XEX-a; **[WNIOSEK]** = wniosek
(wyciągnięty z pomiarów/dokumentacji); granice adresowe w `$`-notation.

## Metodologia [ODCZYT]

- parsing sekcji XEX (nagłówki `start/end` + payload),
- identyfikacja loaderów po rozkazie probe (`0xC0, 14+index, 0xD0`)
  → indeks loadera 0–49,
- banki 0/1 (specjalny wariant komikatu) rozpoznane po pozycji w kolejności
  instalacji (dziewczyna, bohater),
- „wolne stronicowe" = ciąg dalszych pełnych 256-bajtowych stron o jednym
  bajcie wypełnienia (`$00` lub `$FF`); „wolne szczegółowe" = zweryfikowane
  odczytem przestrzenie poniżej granicy strony.

## Tabela per bank

| Indeks | Co w nim jest | Wolne [B] | Wolne miejsca |
|---:|---|---:|---|
| 0 | otwarcie szkoły: portret chłopca + dane kodu otwarcia; **helper melodii PMG** `$6A00–$6E8E` (V185–V187) | **5632** | `$4A00–$5FFF` [ODCZYT] |
| 1 | koszykarz: kod 2892 B (V165/V189), art `$4B80–$7E3B` w tym trzy łaty tablicy `$7ADC–$7E3B`, orbity `$7E40–$7F3F` | **196** | `$7E3C–$7E3F` (4 B), `$7F40–$7FFF` (192 B) [WNIOSEK: zmierzone wypełnienia, patrz drift poniżej] |
| 2 | rejestracja boku: rebound `$4000–$402B`, selektor `$4040–$4599`, spakowane ramki `$4600–$5AA6` i `$6000–$6E0E`, dekoder LZ `$5E00–$5E8B`, helper tunelu/buki `$7800–$7FFF` | **3896** | `$402C–$403F` 20 B, `$45A0–$45FF` ~102 B, `$5AA7–$5DFF` 841 B, `$5E8C–$5FFF` 372 B, `$6E0F–$77FF` 2545 B [ODCZYT dla 3 z 5; suma zgodna z dokumentacją „free gaps 3896 B"] |
| 3–10 | **banany** (V243/V244): gęsty pakiet/RLE + w v244 surowe klatki kiścia; helper `$7840–$7BFE`, wejście `$7C00–$7C6B`, selektor `$7C80`, dekoder `$7D00`, pętla `$7E00`, dispatch `$7F00`, wskaźniki `$7F80–$7F8F` — **8 banków** | **3755 razem (~469/bank)** | [ODCZYT: strony pełne; 3755 B zgodnie z notą V243] |
| 11–18 | **tunel (kaleidoskop)**: po 4 półklatki na bank na `$4000/$4F00/$5E00/$6D00` (3840 B każda) + wspólny kod 1024 B na `$7C00–$7FFF` — **8 banków** | **0** | [ODCZYT = pełny] |
| 19–23 | tło korytarza/spaceru (`school_parallax`, wejście `$7000`) — **5 banków** | **5376 / bank** | `$6800–$6FFF` (2048), `$7300–$7FFF` (3328); razem w 5 bankach **26 880** [ODCZYT] |
| 24–31 | aktor boczny tańca (V142/V143): piksele/maski `$4A00–$51FF` — **8 banków** | **1536 / bank** | `$5200–$53FF`, `$5E00–$5FFF`, `$7E00–$7FFF` (po 512 B); razem **12 288** [ODCZYT] |
| 32–34 | aktor boczny + spakowane ramki środkowe od `$4A00` + strumienie ćwiartek (V173) | **1396 / bank** | `$5200–$53FF` 512, `$5E8C–$5FFF` 372, `$7E00–$7FFF` 512 [ODCZYT] |
| 35 | j.w. | **1140** | `$5300–$53FF` 256, `$5E8C–$5FFF` 372, `$7E00–$7FFF` 512 [ODCZYT] |
| 36 | j.w. | **1908** | `$5000–$53FF` 1024, `$5E8C–$5FFF` 372, `$7E00–$7FFF` 512 [ODCZYT] |
| 37–38 | j.w. | **2164 / bank** | `$4F00–$53FF` 1280, `$5E8C–$5FFF` 372, `$7E00–$7FFF` 512 [ODCZYT] |
| 39 | **bitmapa finałowego chłopca** `$4A00–$53FF` (2560 B, nie kasować) | **1024** | `$5E00–$5FFF` 512, `$7E00–$7FFF` 512 [ODCZYT] |
| 40–41 | banki plazmy tytułowej + **fajerwerki** (V164–V166): kod `$6C00–$7193`, kotwice `$7280–$7380`, kształty `$7400–$7FFF` | **512 / bank** | `$6E00–$6FFF` (stronicowo) + ~364 B szczelin podstronicowych [ODCZYT/WNIOSEK] |
| 42–43 | plazma tytułowa (bez fireworks) | **5120 / bank** | `$6C00–$7FFF` [ODCZYT] |
| 44–48 | plazma pozostała (title banks 40–48 tylko do ticka 2992!) | **9984 / 6400 / 7936 / 9216 / 9472** | okna: `$4300–$49FF/$4F00–$53FF/$5900–$5EFF/$6200–$68FF/$6D00–$71FF/$7700–$7FFF` wg pomiaru (szczególnie bank 44) i mniejsze w 45–48 [ODCZYT] |
| 49 | kontroler szarfy `$5400–$5CCB` (2252 B, V233), kontroler finału `$5CD0–$5FFF`, silnik Trevora `$6000–$69xx` (2500 B), strumienie szarf `$6A00–$7DFF`, kotwice `$7E00–$7F1F`, wiatr `$7F20–$7F9F`, końcówka glifów `$7FA0+` | **~60–70** | szczeliny strukturalne: `$5CCC–$5CCF` (4 B), do `$6A00` ~60 B [WNIOSEK; strony pełne] |

## Sumy

- Wolne stronicowe łącznie z obrazów XEX-a: **114 432 B**
- Po doliczeniu stref sub-stronicowych i liczb z dokumentacji
  (bank 1, bank 2, dekodery 32–38, banany 3–10, bank 49):
  **~118 900 B ≈ 116 KiB** wolnego „w obrazie załadowania". [ODCZYT+WNIOSEK]
- **Dostępne w trakcie normalnego odtwarzania (po tytule):**
  v244 na ticku 3072 nadpisuje banki 40–47 surowymi klatkami bananów
  obranych, a bank 48 obchodzi staging/helpery; w bankach 3–10 surowe
  banany nadpisują pakiet. Wyłączenie 40–48 i wolnych 3–10 z bilansu daje
  **~63 300 B ≈ 61,9 KiB** rzeczywiście wolnych po pierwszych ~15 s
  odtwarzania [WNIOSEK]. Banki 40–48 po tytule są **zarezerwowane**
  (V244: „Do not add post-title assets to banks 40–48").

## Rozbieżności dokumentacji z pomiarem [ODCZYT]

- **Bank 1 (hero)**: noty (V165/V189) opisują 52 B / „85 B code gap"
  przed `$4B80`. Pomiar pokazuje niezerową treść na `$4B4C–$4B7F`
  (15 unicznych wartości) — ta przestrzeń obecnie jest używana, nie wolna.
  Wolne pozostają `$7F40–$7FFF` (192 B) i 4 B między latami tablicy `$7E40`
  a jej kotwicą.
- **Bank 49 (kontroler finału)**: noty V216/V240 mówią „`$5CD0–$5FFF`
  dokładnie 816 B", a mapa v244 „814 B, kończy się `$5FFD` i 4 B przed
  `$6000`". Pomiar bajtowy wskazuje koniec ~`$5FFx` — różnica rzędu
  kilkudziesięciu B, nie zmienia rzędu wielkości wolnego.
- **Banki 24–31 i 39** — strefa `$7E00–$7FFF` nie jest ujęta w opisie
  wolnych 512-bajtowych „starych slotów piłki"; pomiar potwierdza
  512 B wolnych w **każdym** z banków 24–39 (9 szt.).

## Czego nie zająć

- bank 48 (`$4000–$4EFF`, pomocnicze szablony `$6000–$67FF`) — staging
  i szablony helperów bananów (V244),
- `$4A00–$53FF` w banku 39 — bitmapa finałowa (V145/V197),
- `$5E00–$5E8B` w bankach 32–38 — dekoder LZ (140 B/bank); za nim wolne
  `$5E8C–$5FFF` (372 B/bank) — to wolne można brać,
- `$7800–$7FFF` banku 2 — helper piłki rotatora/tunelu (V150),
- `$6C00–$7193`, `$7280–$7380`, `$7400–$7FFF` w bankach 40–41 — fireworks,
- wszystko w banku 49 poza szczelinami w tabeli powyżej.

## Referencje kodu (odczyt)

Mapa loader index ↔ treść wynika z kolejności wywołań w
`tools/build_bitmap_sequence.py:857–876` (girl/hero/ribbon/mosaic/school_pan/
aktorzy 24–39/plazma 40–48/kontrola 49), z `tools/mosaic.py:216–228`
(16 banków: 8 bananów + 8 tunelu, half-frames i kod `$7C00`) oraz
`tools/final_boy.py:25–26` (`BITMAP_BANK=39`, `BITMAP_SOURCE=0x4a00`) i
`tools/school_portrait_bank.py:9–48` (format ładowania/proby banku).

Raport sporządzono odczytem XEX-a; nie uruchamiano buildera ani testów.

