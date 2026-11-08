# Audyt braków względem planu — v144, 2026-11-07

Zakres: `TLIKTB_Atari_Timeline_v2.md`, `TLIKTB_Technical_Constraints.md`,
aktualne generatory i assety, wykonanie callbacku z numerowanego XEX v144.
Nie zmieniano scen, kodu produkcyjnego, granic aktów ani priorytetów.
Czasy poniżej są przybliżeniem muzycznym (takt × 1,875 s).

## Największe braki obrazu

| Fragment | Czas | Plan | Stan v144 |
|---|---|---|---|
| 1B, takty 8–16 | 0:15–0:30 | Dziewczyna pierwszy raz, Trevor w tle | Dziewczyna i chłopiec są; brak Trevora w tle szkoły. |
| 5A, zmiana w takcie 92 | 2:52,5 | Nowe źródło kalejdoskopu lub inny tryb odbicia | Jest przełączenie faz 0–15 na 16–31 tego samego bananowego rotatora. Brak osobnego źródła i trybu odbicia. Częściowo wykonane. |
| 5B, takt 108 | 3:22,5 | Zmiana tekstury tunelu | Nadal ten sam generator spirali i zestaw faz 32–63. Brak osobnego zdarzenia w ticku 40388. |
| 5C, takty 112–116 | 3:30–3:37,5 | Trevor Mosaic | Wspólny efekt zastępczy; bez mozaiki twarzy/postaci Trevora. |
| 5D, takty 116–120 | 3:37,5–3:45 | Eyes Sequence | Brak sekwencji oczu; trwa wspólny efekt. Dawne mruganie portretów nie realizuje tej sceny. |
| 6A, takty 120–124 | 3:45–3:52,5 | Trzy kadry komiksowe i pozy postaci | Brak sceny i podłączonych assetów. |
| 6B, takty 124–128 | 3:52,5–4:00 | Trevor kontra koszykarz | Brak pojedynku; nadal wspólny efekt. |
| 7A, takty 128–136 | 4:00–4:15 | Dedykowane narastanie neonów | Brak osobnej dramaturgii; cykl palet wspólnego efektu nie realizuje zaplanowanego narastania. |
| 7B, takty 136–144 | 4:15–4:30 | Gigantyczny Trevor, flash, kulminacja | Brak sceny. Wcześniejsze ciosy Trevora w akcie 4 jej nie zastępują. |
| 8A, takty 144–152 | 4:30–4:45 | Credits: grupa, muzyka, Silly Venture | Brak planszy creditsów i zaplanowanych logotypów. |
| 8B, takty 152–158 | 4:45–4:56,25 | Greetz | Brak planszy/sekwencji. |
| 8C, takty 158–160 | 4:56,25–5:00 | Końcowy flash i wygaszenie do czerni | Brak końcowego wygaszenia obrazu. Muzyczny fade nie wygasza automatycznie grafiki. |

[WNIOSEK] Ostatnie około **90 sekund**, od 3:30 do końca, nie ma jeszcze
zaplanowanych scen. Nie należy zaliczać tego odcinka jako gotowych aktów
tylko dlatego, że coś jest wyświetlane i muzyka działa.

## Dowód w kodzie i numerowanym XEX

[ODCZYT] `tools/build_bitmap_sequence.py`, sekcja `act5_select`:
po ticku 41884 przechodzi bezpośrednio do `mosaic_frame_ready`. Brakuje
dispatchu aktów 6–8, zdarzeń dla 5C/5D i zakończenia. Wcześniej obsługuje
takty 92 i 104; nie obsługuje osobnej zmiany w 108.

[ODCZYT] `tools/mosaic.py`: klatki 0–31 używają jednej funkcji `banana_tile`,
a 32–63 jednego generatora tunelu. Zmiana palety lub fazy nie dodaje nowej
tekstury ani wizerunku Trevora.

[ODCZYT] Wykonano kod 6502 z `build/visual-prototype-v144.xex` w py65,
z rzeczywistymi danymi jego banków. Poniżej próbki dokładnie na granicach
planowanych scen. Identyfikator 6 oznacza wspólny renderer mozaiki/rotatora,
nie akt 6.

| Takt | Tick | Identyfikator sceny | Faza wspólnego efektu |
|---|---:|---:|---:|
| 108 | 40388 | 6 | 60 |
| 112 | 41884 | 6 | 25 |
| 116 | 43379 | 6 | 23 |
| 120 | 44875 | 6 | 52 |
| 124 | 46371 | 6 | 50 |
| 128 | 47867 | 6 | 15 |
| 136 | 50858 | 6 | 42 |
| 144 | 53850 | 6 | 5 |
| 152 | 56842 | 6 | 32 |
| 158 | 59085 | 6 | 44 |
| 160 | 59833 | 6 | 27 |

SHA-256 badanego XEX:
`8db4ca4de50c7db85d02732e416a9734b1ceab91a9e9e999c59e0e32fc828f21`.
Nie wykonywano nowego pomiaru FPS ani nowego pełnego porównania muzyki
podczas audytu. Wyniki wydania pozostają w `V144_DUZY_ZURAW.md`.

## Czego nie liczyć jako brak

- Szkolne logo/panorama z pierwotnego intro zostały świadomie zastąpione
  planszami TAME IMPALA / tytuł, miastem, Żurawiem i fajerwerkami.
- Wcześniejszy taniec z pomponami zastępuje zatwierdzone boczne ujęcie
  szarfy; oryginalna scena jest w osobnym `projects/pompom-dance`.
- Cztery portrety występu zastąpiły trzy zatwierdzone ujęcia szarf i wyrzut
  bohaterki. Nie należy przywracać ich jako rzekomo brakujących scen.
- Kozłowanie, wsad, wejście Trevora i jego kombinacje ciosów mają działające
  renderery. Tęczowe piłki, BANG/BAM i rozpad PMG są dodatkami już wykonanymi.

## Otwarte decyzje i weryfikacja techniczna

To osobna grupa od brakujących scen:

- GTIA 9 w akcie 5: w planie pozostawione do decyzji, bez wskazanego bloku.
  Nie ma obecnie takiej sceny ani jej źródeł.
- Rzeczywiste terminy prezentacji, FPS/pominięte fazy i zapas CPU z DMA
  ANTIC oraz czterema DLI: niepotwierdzone na docelowym sprzęcie (V1).
- Pełna kontrola obrazu i odsłuch w konfiguracji docelowej oraz fizyczne
  Atari 65XE/1 MB/stereo POKEY: pozostają do wykonania. Porównania rejestrów
  muzyki Atari800 przechodziły; nie są odsłuchem ani pomiarem płynności.
- Dedykowany test START/pauza i zatrzymania zegara/wideo: brak (V4).
- Pełne porównanie v024/v035: blokuje je brak v024 (V5).
- Eksperyment z nierównymi odstępami DLI: niewykonany (V6). Oryginalne
  cztery równe odstępy są zachowane i sprawdzane przez testy.
- Zasady compo i ostateczna konfiguracja rozszerzenia oraz los UI playera:
  w dokumentacji nadal otwarte. Nie rozstrzygano ich w tym audycie.
- ZX0, osobne `.pal`/`.pmg` i alternatywne formaty w specyfikacji to
  propozycja konwencji, nie wdrożony pipeline. Nie są dodatkowymi scenami.

[ODCZYT] Historyczne założenie przycięcia playera do siedmiu banków jest
nieprawidłowe dla v035: wymagany jest bank 8 ze znacznikiem końca. To nie
jest zaległe zadanie do zrobienia. Nadal przydzielone są 64 banki; odzyskane
29 901 B to rozproszone miejsca, a nie wolne całe banki. Brakuje też
wspomnianego w dawnym planie pliku `TLIKTB_Asset_List.md`; audyt oparto
na faktycznych wejściach Makefile i generatorów.
