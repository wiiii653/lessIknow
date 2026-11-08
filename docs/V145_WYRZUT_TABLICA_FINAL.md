# V145 — wyrzut ku kamerze, rozbita tablica i chłopiec w finale

Zmiany scenariusza zatwierdzone i zlecone przez użytkownika 2026-11-07.
Nie przesunięto granic aktów, dotychczasowych ujęć ani czterech ticków
muzyki na ramkę PAL. Nadal używany jest pełny player v035 i 64 banki.

## Trzecie ujęcie szarf — kamera z góry

[ODCZYT] W 17950–20942, po grupie i solówce, kamera patrzy z góry na
grupę na parkiecie. Nowe pozy mają widoczną twarz skierowaną ku obiektywowi,
rozłożone włosy i skróty perspektywiczne nóg. Podstawy oraz linie boiska
znajdują się pod bohaterką. Końcowe klatki 12–15 powiększają ją ku kamerze,
a tło i podstawy zmniejszają się. Pozy 8–11 i dodatkowa 35 też mają nową
perspektywę. Pozostałe dwa ujęcia i boczny taniec zachowane.

[ODCZYT] Zegar wybiera te same kroki co wcześniej; cztery etapy lotu
pozostają na końcu trzeciego ujęcia. Nowa grafika zastępuje istniejące
kompozycje w 36-klatkowym zestawie, bez dokładania bankowanych bitmap.
Szarfy i iskry nadal korzystają z podwójnego PMG i rasterowej tęczy.

## Wsad rozbija tablicę

[ODCZYT] Pierwszy kontakt z tablicą następuje w istniejącej pozie chwytu
obręczy: faza 75 wsadu, tick 23638. Fazy 75–80 pokazują promieniste
pęknięcie, 81–86 rozbitą płytę, a 87–93 pozostałe kawałki i odłamki.
Obręcz, siatka oraz reszta sylwetki pozostają czytelne. Cztery missiles
wyrzucają kolorowe szczątki od kosza, z ruchem w bok i opadaniem.
Piłka nadal używa czterech players i dotychczasowej trajektorii.

[ODCZYT] Trzy prostokątne łatki 48×24 zajmują 3 × 288 B = 864 B.
Nakładane są na pełną końcową pozę w nieaktywnej bitmapie. Klucz cache
obejmuje etap zniszczenia, więc trzymana poza nie blokuje dalszego rozpadu.
Pomiędzy etapami aktualizują się odłamki PMG bez ponownego kopiowania tła.

## Finał na parkiecie

[ODCZYT] Ujęcie 8C zaczyna się w ticku 59085 (~4:56,25). Chłopiec w swoim
cyjanowo-różowym stroju leży na plecach na podłodze sali. Cztery niezależnie
kolorowane gwiazdki krążą po elipsie wokół głowy; to ruchome players,
nie gwiazdki wrysowane w bitmapę. Animacja trwa przy trzymanym tle.

[ODCZYT] Końcowe 128 ticków zawiera fade; po jego zakończeniu kolory pola
są zerowe, PMG wyłączony. Po ticku 59833 obraz pozostaje czarny, również
przy kolejnych callbackach. ANTIC i rozkład muzycznych DLI pozostają aktywne.
Maski gwiazdek przygotowywane są poza ekranem i publikowane w oknie
VCOUNT 124–127; bitmapa również powstaje wyłącznie w nieaktywnym buforze.

To realizacja ostatniego kadru. Akty 5C/5D, 6–7 oraz wcześniejsze plansze
credits/greetz w 8A/8B nadal wymagają wykonania. Ich zakresów nie zajęto
nową sceną. Audyt `AUDYT_BRAKOW_V144.md` pozostaje historycznym stanem v144.

## Pamięć i silnik

| Zmiana względem v144 | Koszt |
|---|---:|
| Nowa perspektywa wewnątrz istniejących bitmap szarf | 0 B netto |
| Trzy łatki tablicy | +864 B |
| Kod/tablice wsadu i odłamków | +428 B |
| Kontroler finału | +812 B |
| Bitmapa finału | +2560 B |
| Usunięcie martwego dispatchu pomponiar, po dodaniu nowego dispatchu | −66 B |
| **Koszt netto** | **4598 B** |

[ODCZYT] Względem v141 nadal odzyskane **25 303 B = 24,71 KiB**. To
rozproszone miejsca w obecnych bankach; liczba banków ani wymagania RAM
nie zostały zmniejszone. Pliki źródłowych PNG/RGB nie są pamięcią Atari.

- Bank loadera 1: helper koszykarza `$4000–$4A4C` (2637 B), dane
  `$4B80–$7E3B` (12 988 B); nowe łatki `$7ADC–$7E3B`. Zostaje 307 B
  przerwy przed danymi i 452 B na końcu banku.
- Bank loadera 39: bitmapa finału `$4A00–$53FF`, zamiast wolnego slotu.
- Bank loadera 49: kontroler finału `$5B80–$5EAB` (812 B), za kontrolerem
  szarf kończącym się `$5B3D`, przed kodem Trevora od `$6000`.
- Niebankowany kod główny `$1400–$1DBD` (2494 B), 66 B zapasu do `$1E00`.
  Usunięta jest nieużywana ścieżka starego tańca z pomponami; jej archiwalny
  samodzielny projekt pozostaje kompletny.
- Trampoline kopii ma osobną trasę `FRAME_KEY=36` do bitmapy finału.
  Normalne klatki szarf nadal mają numery 0–35. Kod przełączający banki
  wykonuje się poza oknem `$4000–$7FFF`; NMI przywraca PORTB.

## Źródła grafiki i prompty

Oba obrazy wygenerowano w **built-in imagegen**. Referencje to istniejący
arkusz tancerki v136 i arkusz koszykarza v024; nie używano CLI/API fallback.

- Arkusz ośmiu póz z góry:
  [act2_ribbon_overhead_v145.png](../assets/art/source/act2_ribbon_overhead_v145.png).
- Pełny prompt:
  [act2_ribbon_overhead_v145.prompt.txt](../assets/art/source/act2_ribbon_overhead_v145.prompt.txt).
- Chłopiec leżący na podłodze:
  [act8_boy_floor_v145.png](../assets/art/source/act8_boy_floor_v145.png).
- Pełny prompt:
  [act8_boy_floor_v145.prompt.txt](../assets/art/source/act8_boy_floor_v145.prompt.txt).

Podłogi, perspektywa, skala, szarfy, pęknięcia, odłamki i gwiazdki powstają
w kodzie generatorów. Źródłowa ilustracja koszykarza przy wsadzie zachowana.

## Podglądy i wydanie

- `build/v145-overhead.gif`: trzecie ujęcie i lot ku kamerze.
- `build/v145-shatter.gif`: wsad i rozpad tablicy.
- `build/v145-final.gif`: ostatni kadr i fade.
- `build/v145-story-beats.gif`: trzy fragmenty połączone do przeglądu.
- `build/v145-scenes.png`, `build/v145-board-storyboard.png`: kadry kontrolne.

Podglądy pochodzą z sekwencyjnego wykonania callbacków 6502 w py65.
Paleta i tempo są przybliżone; nie uwzględniają DMA ANTIC ani rzeczywistego
czasu prezentacji. Nie zastępują nagrania emulatora lub próby na Atari.

Wydanie: `build/visual-prototype-v145.xex` i JSON, 1 109 034 B.
SHA-256: `f9d1a723bb6604759eaf56897c1ce27e2d350323a1f0712690c2078eb5f57c47`.
Numerowane wydanie jest identyczne bajt w bajt ze sprawdzanym buildem roboczym.

## Walidacja

[ODCZYT] Końcowy `make check`: **109 testów, 106 zaliczonych, 3 pominięte**
(brak archiwalnego v126), 87,627 s. Osiem nowych testów kontroluje etapy
tablicy i granicę wsadu, odłamki przy trzymanej bitmapie, wzrost bohaterki,
orbitę czterech gwiazdek, fade i trwałą czerń, przejścia/restart, brak zapisów
do aktywnych buforów, publikację rejestrów w ruchomym VCOUNT oraz NMI
oryginalnego dekodera podczas kopiowania finału. Testy palet mozaiki kończą
się przed nową sceną 8C; jej celowe wygaszanie ma osobne asercje.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **15 572 808
identycznych bajtów** względem v035, cały utwór. To porównanie rejestrów,
bez odsłuchu i bez próby na fizycznym Atari. Nowe ujęcia obejrzano w podglądach
callbacku; płynność i rzeczywiste terminy rastra pozostają do oceny z DMA.

[ODCZYT] Próbki samego CPU py65, bez DMA/NMI:

| Próbka | Zimne wejście | Trzymana klatka, +4 ticki |
|---|---:|---:|
| Pęknięcie, tick 23638 | 55 744 | 5527 |
| Rozpad, tick 23734 | 55 799 | 5565 |
| Odłamki, tick 23838 | 55 765 | 5554 |
| Finał, tick 59085 | 43 602 | 4950 |
| Czarny koniec, tick 59833 | 43 564 | 4912 |

Nie są to pomiary FPS ani dowód zmieszczenia aktualizacji w jednej ramce PAL.
