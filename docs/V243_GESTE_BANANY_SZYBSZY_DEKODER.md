# V243 — gęste banany i szybszy dekoder

Na polecenie użytkownika cofnięto oszczędność przez symetrię obrazu z v241.
Obie grafiki wracają dokładnie do v240: gęsty kafel 64×64, jednakowy
kierunek sąsiadujących owoców, pierwotny zoom. Każdy wariant ma 32 różne
klatki pełnego obrotu. Nie zmieniono ticków ani tempa wyboru faz.

## Przyspieszenie

Nowe RLE rozdziela indeksy wejścia Y i wyjścia X. Strumień jest pakowany
z uwzględnieniem granic stron źródła i framebufferu, więc pętle nie muszą
przeliczać dwóch wskaźników 16-bitowych dla każdego pakietu. Literały
kopiowane są po dwa bajty, wypełnienia po osiem. Token 0 przeskakuje
padding do kolejnej strony wejścia; koniec następuje po 15 stronach bitmapy.
Generator dobiera próg pakowania oddzielnie dla klatek w ramach pojemności
każdego banku, ograniczając koszt najdroższej klatki.

[ODCZYT] Callback z piłką i paletą, po przygotowaniu obu display list:

| Motyw | v240 maks. | v243 maks. | Mniej CPU |
|---|---:|---:|---:|
| Kiść | 78748 | 75139 | 4,6% |
| Obrany | 78599 | 72819 | 7,4% |

To oszczędność CPU względem poprzedniego **gęstego** wzoru, nie względem
surowej symetrii v241. Nadal nie dorównuje kosztowi surowego kopiowania.
Kontrolny tunel zachowuje koszt v242: 47233 cykle.
py65 nie modeluje ANTIC DMA; powyższe liczby nie są pomiarem FPS.
Pierwsze callbacki z budowaniem DL: kiść 87317/85847, obrany 70821/75345.

## Pamięć i izolacja

- Osiem dotychczasowych banków loadera 3–10; żadnej luki z innych scen.
- Grafika 113981 B; kod i tablice 1667 B na bank; pozostaje 3755 B.
- Dane $4000–$783F; helper $7840; wejście $7C00; selektor $7C80;
  dekoder $7D00; wypełnienia $7E00; tablica skoków $7F00;
  osiem wskaźników $7F80–$7F8F.
- Scratch $0DC0–$0DC1 i $0DC4–$0DC6, prywatny cache $0DDE, klucz $0DDD.
  Bez korzystania ze strony zerowej ani scratcha NMI.
- Rozpakowywany jest wyłącznie nieaktywny framebuffer. PORTB chroni
  dotychczasowy wrapper muzyczny, a wspólny cache $83FA jest unieważniany.

[ODCZYT] Porównanie załadowanej pamięci z v242: różnią się tylko banki
17–24 oraz 13 bajtów selektora $ED83–$ED8F. Pozostałe 56 banków są
identyczne, łącznie z tunelami, piłką i kodem finału.

## Weryfikacja

[ODCZYT] 9 testów ukierunkowanych: wszystkie 64 klatki dekodowane zgodnie
z generatorem i bitmapami v240, brak zapisów do frontu, pełny obrót,
naprzemienność motywów, seeki i przerwania oryginalnego playera w dekoderze.
Nowa regresja kosztu wymaga maks. 76000/74000 cykli dla rozgrzanych motywów.

Podgląd: `build/banana-v243-variants.png`, animacje
`build/banana-v243-bunch.gif` i `build/banana-v243-peeled.gif`.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **11376072
identycznych bajtów** względem v035, cały utwór. Bez próby na fizycznym Atari.
Build roboczy i v243 mają ten sam SHA-256:
`5c83f6d149be22dfa2cc778579f4d3c5dbd5cd71db135929fbb94e522df41785`.

[ODCZYT] `make check PYTHON=/tmp/finale197-venv/bin/python`: **186/186
testów**, bez pominięć, 137,5 s. Cały utwór Atari800 stereo: 11376072
identycznych bajtów względem v035. Build roboczy zgodny z v243.
