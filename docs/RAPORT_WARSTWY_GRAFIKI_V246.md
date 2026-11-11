# Raport warstw grafiki — v246

**Data:** 2026-11-11  
**Zakres:** eksport warstw i teł dla `build/visual-prototype-v246.xex`; bez
zmian kodu źródłowego, generatorów ani plików XEX. Dodano wyłącznie raport
oraz PNG-i wynikowe; testów nie uruchamiano.

## 1. Wynik eksportu

Warstwy znajdują się w `build/v246-scene-layers/`:

- 159 plików PNG w katalogach `characters/`, `backgrounds/` i
  `composite-only/`;
- `INDEX.md` zawiera spis, źródła i ograniczenia każdego rodzaju zasobu;
- `build/v246-scene-layers.zip` zawiera cały zestaw.

Eksport jest zakotwiczony w XEX v246 o SHA-256
`449defc2cfd2d3cdd0af3d4c34acc5171168f9718592deb544c5ed4e26ab0fba`.

## 2. Co oznacza „osobny plan” w tym zestawie

Pliki mają trzy różne rodzaje separacji. Nie należy ich traktować jako
równoznacznych:

1. **Przezroczysta postać (`RGBA`)** — alfa pochodzi ze źródła produkcyjnego
   albo z maski używanej przez obecny generator. Można ją kłaść na inne tło.
2. **Warstwa różnicowa (`aligned delta`)** — przechowuje tylko piksele, które
   różnią się od konkretnej płyty tła. Jest dokładna po złożeniu z tą płytą,
   ale nie jest uniwersalną sylwetką postaci.
3. **Kompozyt spłaszczony** — postać i tło są już jednym obrazem źródłowym.
   Plik jest zachowany jako referencja; nie udajemy, że ma prawdziwą alfę.

Wyłączenie PMG w poprzednim eksporcie usuwało sprzętowych graczy i pociski
z podglądów. Nie rozdzielało postaci narysowanych bezpośrednio w bitmapie.

## 3. Zawartość według scen

| Scena | Postacie / plany | Status separacji |
|---|---|---|
| Intro | 16 faz plazmy, miasto i Żuraw; sześć masek napisów | Tło i maski tekstu osobno; atlas tła używa stałej jasności GTIA 6, więc nie odtwarza zmian jasności DLI. |
| Act 1 — fasada | Chłopiec, dziewczyna, płyta ATARI ARENA | Płyta z generatora; dziewczyna w RGBA; trzy kadry chłopca jako różnice do płyty. Czysty source sprite gwizdającego chłopca jest osobno. |
| Act 1 — trening | Storyboard trzech treningowych ujęć | Wejściowy storyboard jest spłaszczony. Nie ma w v246 oddzielnych masek postaci i sali, więc ujęcia są w `composite-only/`. |
| Act 2 — szarfy | Pozy grupowe, boczne, z góry oraz klatki pośrednie V166/V171/V173 | Osobne przezroczyste arkusze pozy; tła sali i przewijanej sali są osobno. |
| Act 3 — koszykówka | Osiem runtime’owych klatek V175 i płyta hali | Warstwa runtime zawiera wszystkie piksele różniące klatkę od płyty — postać, piłkę i elementy tablicy. To nie jest czyste wycięcie samego koszykarza. Arkusz V177 jest czysty RGBA, ale **nie jest** grafiką używaną przez v246 (V189 przywrócił klatki V175). |
| Act 4 — Trevor | Wejście, cztery pozy walki, osobny PMG reveal | Postać i fazy tunelu są rozdzielone. PMG reveal to dodatkowa osobna warstwa. |
| Act 5 / po Trevorze | Banany, spiralny i organiczny tunel, okna dyrektora | Reprezentatywne bitmapowe plansze v246 bez PMG; w tych ujęciach sama bitmapa jest tłem/efektem. |
| Finał | Leżący chłopiec i siatka podłogi | Sylwetka chłopca ma maskę runtime; siatka jest osobną płytą. |

Pełny spis plików i ich ścieżek znajduje się w
`build/v246-scene-layers/INDEX.md`.

## 4. Ograniczenia i ryzyko pomyłki

- **Chłopiec z Act 1:** neutralna, odwrócona i gwiżdżąca bitmapa szkolna
  jest złożona z płyty. Eksport `*-aligned-delta.png` odtwarza różnicę dla
  tej konkretnej fasady; nie należy używać jej jak odizolowanej sylwetki na
  dowolnym tle. Czysty sprite gwizdującego chłopca ma osobną nazwę `source`.
- **Trening:** oddzielenie osób od storyboardu wymagałoby nowych masek lub
  ręcznego odrysowania. W tym raporcie nie dodano takich przybliżeń.
- **Koszykówka:** źródłowy arkusz V177 wygląda jak sam koszykarz, ale v246
  renderuje odzyskane klatki V175 wraz z piłką/tablicą. Nie wolno opisywać
  arkusza V177 jako wiernego wycięcia z runtime.
- **Warstwy bitmapowe i PMG:** piłka, fajerwerki i fragmenty mogą należeć do
  osobnych PMG, podczas gdy koszykarz lub Trevor są bitmapą. Wyłączenie PMG
  usuwa pierwszą grupę, nie drugą.

## 5. Kontrakt dla dalszej rozbudowy

Przy dodawaniu lub poprawianiu scen zalecany jest następujący układ źródeł:

```text
scene-layers/<scene-id>/
  background.png
  characters/<character-id>/<pose-id>.png
  overlays/<effect-id>/<phase>.png
  manifest.json
```

Manifest powinien opisywać co najmniej: `scene`, `character/effect`, wersję
źródła, rozmiar, kotwicę i skalę ekranową, metodę maskowania, identyfikator
tła bazowego oraz status `runtime-exact`, `source-only`, `aligned-delta` albo
`composite-only`.

Zasady jakości:

1. Nową postać dostarczać z prawdziwym kanałem alfa i osobną płytą tła; nie
   używać czerni jako przezroczystości dla włosów, konturów i kurtek.
2. Warstwę różnicową zawsze parować z hashem/ID tła, względem którego ją
   policzono.
3. Każdy zestaw `background + postacie + overlays` sprawdzać przez ponowne
   złożenie i porównanie z odpowiadającym PNG v246. Odchylenia oznaczać, nie
   ukrywać pod nazwą „cutout”.
4. Dla spłaszczonych źródeł (obecnie storyboard treningowy) najpierw uzyskać
   oryginalne warstwy od autora albo zatwierdzić ręczne maski. Nie zmieniać
   buildowego kodu kompozytora bez osobnej zgody.
5. PMG utrzymywać jako własną warstwę sprzętową; eksporty bez PMG są
   referencjami do bitmapy, a nie kompletnym odtworzeniem wszystkich efektów.

## 6. Następne prace bez zmian kodu

1. Przejrzeć `INDEX.md` i wskazać, czy potrzebne są ręczne maski dla
   storyboardu treningowego.
2. Zdecydować, czy koszykarz ma pozostać zgodny z runtime V175, czy ma wrócić
   do źródłowego RGBA V177; to decyzja artystyczna i pamięciowa, nie sam
   eksport plików.
3. Przy kolejnych zmianach scen zapisywać nowe płyty i maski w osobnych
   źródłach, a potem odświeżać warstwowy eksport z nowego numeru XEX.
