# V165 — różne orbity satelitów przy wsadzie

## Obraz

Przed rozbiciem tablicy piłka wsadu ma cztery krążące satelity missiles:

- szeroka elipsa, zgodnie z ruchem wskazówek w ekranowym układzie y;
- wyższa elipsa, obrót przeciwny;
- mocno spłaszczona elipsa, dwukrotnie szybsza;
- pochylona elipsa, obrót przeciwny.

Każdy satelita to trójwierszowy diament o podwójnej szerokości missile.
Dziedziczą cztery cyklicznie zmieniane kolory piłki. Ich pozycje są
przesunięciami względem aktualnego środka piłki, więc wszystkie orbity
przenoszą się razem z nią w kolejnych pozach chłopca.

[ODCZYT] Orbity działają wyłącznie w fazach wsadu 0–74, do pierwszej
rysy tablicy. Od fazy 75 dotychczasowe trajektorie i kształty odłamków
szkła przejmują missiles, z przywróceniem ich dawnej szerokości.
Kozłowanie nadal korzysta z poprzednich drobinek. Grafika piłki i areny,
fazy rozbicia tablicy, ticki, długość wsadu i granice scen są zachowane.

32 fazy trajektorii wybiera licznik playera `tick >> 3`. Pełna zwykła
orbita trwa 256 ticków (około 1,28 s), szybka 128. Zmiana nie korzysta
z dodatkowego licznika klatek ani ze zmieniania ticków muzyki.

## Pamięć i publikacja

[ODCZYT] Zmienił się wyłącznie bank loadera 1 (bohater). Wszystkie
pozostałe 63 banki i niebankowany RAM są identyczne bajt w bajt z v164.

- Kontroler bohatera: 2859 B, `$4000–$4B2A`, o 207 B więcej niż v164.
  Zostaje 85 B przed danymi od `$4B80`.
- Dotychczasowe obrazy, piłka i poprawki tablicy nadal kończą się na `$7E3B`.
- Tabele orbit: 256 B, `$7E40–$7F3F`, cztery pary tablic x/y po 32 próbki.
  Zostaje 4 B przerwy za poprawkami tablicy i 192 B na końcu banku.
- Instalator sprawdza rozdzielenie dotychczasowych danych i nowych tabel
  oraz koniec banku `$8000`.

Koszt netto: **207 + 256 = 463 B**. Odzysk względem v141:
**34 305 B = 33,50 KiB**. Nadal 64 banki; main nadal 2546 B.

PMG bohatera jest nadal zapisywane w istniejącym zakresie `$0980–$0BFF`.
Przed jego czyszczeniem okno zostało ograniczone do VCOUNT 124–127:
spóźnione wejście czeka na następny blanking zamiast zaczynać aktualizację
pod koniec bieżącego. Nie dodano odczytów HPOS GTIA ani zmian muzycznych
DLI. PORTB przywraca istniejący trampoline.

## Walidacja

Testy wykonują callbacki 6502 przez cały cykl orbit. Sprawdzają cztery
różne trajektorie, przeciwne znaki kierunku obrotu, dwukrotną prędkość
jednej orbity, pełne kształty diamentów, szerokości missiles i PORTB.
Dodatkowe przypadki obejmują skoki między pozami w fazach 47/61 i ostatni
moment przed rozbiciem, a następnie przywrócenie odłamków w 75/81/87/93.

Regresja ruchomego VCOUNT sprawdza późne wejścia dla czterech pozycji
piłki i zakończenie zapisu przed pierwszym satelitą następnej klatki.
[ODCZYT] Dodatkowa kontrola 24 przypadków ma najmniejszy zapas CPU
23,9 linii. Ten model nie obejmuje DMA ANTIC ani kosztu wszystkich NMI.

[ODCZYT] Testy bohatera i finału przed dodaniem regresji VCOUNT:
18 zaliczonych w 4,530 s.
[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
11 964 744 identyczne bajty względem v035, około 3332,9 s emulacji,
obejmujące cały utwór. To porównanie danych rejestrów, bez odsłuchu.

Podgląd `build/v165-dunk-orbits.gif`, kadr zbiorczy
`build/v165-orbits-to-glass.png`: po callbackach 6502, z przybliżonymi
kolorami i tempem. Nie jest to nagranie emulatora.
[WNIOSEK] py65 i zgodność POKEY nie potwierdzają rzeczywistego FPS
ani terminów DMA/rastera. Bez testu na fizycznym Atari.

[ODCZYT] Pełne `make check`: 127 testów, 124 zaliczone,
3 pominięte (brak archiwalnego v126), 96,416 s.

## Wydanie

`build/visual-prototype-v165.xex` i odpowiadający JSON są identyczne
z przetestowanymi plikami roboczymi dev. Poprzednie wydania zachowane.
SHA-256 XEX: `dd5182f53a36d54f2fa3012b70a5761c958f52b51a6a7e62f72ac370d14d829c`.
