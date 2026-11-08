# V164 — tęczowe rakiety od dołu do górnego nieba

## Efekt

Obie plansze otwierające demo mają cztery przesunięte w fazie wystrzały.
Rakieta zaczyna przy dolnej krawędzi aktywnego obrazu (y=190), zostawia
przerywany ogon i leci do górnej części kadru. Cztery wierzchołki leżą
na y=44, 72, 56 i 36. Przy wierzchołku następuje szeroki centralny błysk,
rozkwit dwunastu promieni, a potem opadające, przerzedzające się iskry.
Dodatkowe odłamki missiles odlatują na boki poza obrys głównego wybuchu.

[ODCZYT] Wznoszenie trwa 64 ticki playera (około 0,32 s); cały cykl
256 ticków (około 1,28 s). Kolejna rakieta jest przesunięta o 64 ticki.
Kotwice pionowe mają 64 fazy na cykl i zmieniają się co 4 ticki, dlatego
lot nie ogranicza się do czterech skoków zapisanych w kształtach.
Kształty mają nadal 16 faz, a kolory zmieniają się co 8 ticków — również
w czasie rozkwitu i rozpadu. Każdy player i jego missile mają własną
fazę tęczowej palety; bez włączania trybu piątego playera.

Napisy zachowują układ i kolejność wejść I KNOW → THE BETTER → THE LESS.
Historyczny Żuraw, tła, granice obu plansz, fade i wszystkie ticki scen
pozostają takie jak w v163. Pełne fajerwerki są na wierzchu liter, budynku
i plazmy (`PRIOR=$C1`).

## Bufory i pamięć

Przygotowanie nadal zapisuje wyłącznie nieaktywny zakres PMG
`$0980–$0BFF` lub `$8980–$8BFF`. Publikacja przełącza kompletny bufor,
pozycje i kolory w ograniczonym oknie VCOUNT 124–127. Żaden nowy zapis
nie odczytuje rejestrów pozycji GTIA. PORTB jest przywracany przez
istniejący kod wywołujący. Nie zmieniono aktualizacji muzyki.

[ODCZYT] W każdym z banków loadera 40/41:

- kontroler: 1428 B, `$6C00–$7193`, publikacja nadal `$7000`;
- kotwice: 257 B, `$7280–$7380` — cztery tablice po 64 i stała kotwica
  dla 64-wierszowej płaszczyzny missiles w górnej części nieba;
- kształty: nadal 3072 B, `$7400–$7FFF` — 4 × 16 × 32 wiersze players
  oraz 16 × 64 wiersze missiles.

Instalator sprawdza puste miejsce oraz rozdzielenie kontrolera, metadanych
i kształtów. Dodatkowe tabele rozsuwania missiles są częścią kontrolera.
Koszt względem v163: **2 × (72 B kodu/tabel + 252 B kotwic) = 648 B**.
Odzysk netto względem v141: **34 768 B = 33,95 KiB**. Nadal 64 banki,
main 2546 B i 14 B zapasu przed `$1E00`.

[ODCZYT] Porównanie v163/dev potwierdza, że zmieniły się wyłącznie banki
loadera 40/41. Wszystkie pozostałe 62 banki i cały niebankowany RAM są
identyczne bajt w bajt.

## Walidacja

Testy wykonują callbacki 6502 i sprawdzają start każdej z czterech rakiet
przy dolnej krawędzi, kolejne malejące pozycje y, eksplozję wysoko nad
miastem, szeroki rozbłysk i dwanaście lub więcej barw podczas wybuchu.
Sprawdzają również boczny ruch missiles, pełne kształty nad napisami
i Żurawiem, opadanie/zanikanie iskier, nieaktywny bufor, przywrócenie
PORTB, tryb GTIA 11, kolejność tekstu oraz publikację przy późnym VCOUNT.

[ODCZYT] Testy samej sceny: 8 zaliczonych w 7,205 s.
[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 601 744 identyczne bajty względem v035, około 4067,4 s emulacji,
obejmujące cały utwór. To porównanie danych rejestrów, bez odsłuchu.

Podglądy: `build/v164-title-fireworks.gif` oraz
`build/v164-launch-to-burst.png`. Wykonane po rzeczywistych callbackach
6502, z przybliżoną paletą i tempem; nie są nagraniem emulatora.
[WNIOSEK] py65 nie modeluje DMA ANTIC ani rzeczywistych terminów rastra;
zgodność POKEY nie jest pomiarem FPS. Bez testu na fizycznym Atari.

[ODCZYT] Pełne `make check`: 124 testy, 121 zaliczonych,
3 pominięte (brak archiwalnego v126), 95.022 s.

## Wydanie

`build/visual-prototype-v164.xex` i odpowiadający JSON są identyczne
z przetestowanymi plikami roboczymi dev. Poprzednie wydania zachowane.
SHA-256 XEX: `3b81a480977e7bc0523cfe84165cb3c766c5c6b366c6d99c2ec645e149037370`.
