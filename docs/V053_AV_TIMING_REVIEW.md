# Porównanie synchronizacji obrazu v051 i v053

## Metoda

[ODCZYT] Uruchomiono oba wydania XEX w osobno skompilowanym Atari800 7.2.1:
PAL, `-1088xe`, Altirra OS, stereo POKEY, bez BASIC, z rysowaniem każdej klatki.
Instrumentowany emulator i ślady zapisano w `/tmp`; plików XEX nie zmieniano.
Ślad klatkowy zawiera licznik muzyki `$24A7–$24A9`, stan sceny `$83E0`,
wskaźnik display listy, kolory GTIA, cztery rejestry POKEY i skrót FNV-1a
poprzednio wyrenderowanego bufora ekranu. Osobny ślad rejestruje rzeczywiste
zapisy do GTIA, ANTIC i POKEY z licznikiem, linią rastra i pozycją cyklu.

[ODCZYT] Porównano 14 958 klatek od pierwszego niezerowego licznika do ticku
59832. Na odpowiadających sobie klatkach licznik muzyki, stan sceny i cztery
próbkowane rejestry POKEY były zgodne. Skrót ekranu i stan sceny opisują różne
chwile: skrót dotyczy poprzednio wyrenderowanej klatki. Zgodny stan `$83E0`
nie dowodzi sam w sobie, że nowe ujęcie jest już widoczne.

## Zaobserwowane różnice

[ODCZYT] W pierwszych scenach szkoły i treningu oraz w portretach dziewczyny
i scenie Trevora skróty odpowiadających sobie klatek były zgodne w badanym
przebiegu. Różnice wystąpiły w tańcu (46 z 748 klatek), pierwszej mozaice
(333 z 748), koszykówce (190 z 748) i drugiej mozaice (3168 z 6731). Skrót
FNV jest wskaźnikiem różnic, nie analizą ich treści ani dowodem braku kolizji.

[ODCZYT] Pierwsza mozaika, zapis GTIA `$D016` wartości `$8A`: v053 przy ticku
12552, linia 255; v051 przy ticku 12560, linia 255. Różnica wynosi dwie klatki
PAL, około 40 ms. W obu wersjach zapis POKEY AUDF1 wartości `$03` nastąpił
przy ticku 12528, linia 9. To punkt odniesienia w strumieniu rejestrów; sam
zapis AUDF nie dowodzi, że jest słyszalnym początkiem beatu.

[ODCZYT] Druga mozaika, zapis GTIA `$D016` wartości `$AA`: v053 przy ticku
33112, linia 254; v051 przy ticku 33128, linia 310. Jest to około cztery
klatki i 56 linii rastra różnicy, około 84 ms. W obu wersjach zapis AUDF1
wartości `$FE` wystąpił przy ticku 33095, linia 243. W v053 zmiana GTIA
następuje przed późniejszym zapisem AUDF1 `$43` przy ticku 33118, linia 166;
w v051 po nim. Nie ustalono, który zapis POKEY odpowiada odbieranemu beatowi.

[WNIOSEK] Zmiana w v053 przesuwa niektóre faktyczne akcenty obrazu bardziej,
niż wynikałoby z samej różnicy 1–3 progowych ticków: callback może pracować
przez kilka klatek i zakończyć aktualizację na innym wygaszaniu. To wyjaśnia
możliwość odczuwalnej różnicy względem v051, ale samo w sobie nie wskazuje,
która wersja jest lepiej dopasowana do słyszalnego ataku muzycznego.

## Ograniczenia

- Ślad rejestrów ma rozdzielczość instrukcji emulatora i raster, a ślad obrazu
  jest próbkowany raz na klatkę. Nie wykonano analizy rzeczywistego przebiegu
  audio ani odsłuchu A/B; wpis AUDF to zmiana rejestru, nie automatycznie beat.
- Poprzednie porównanie stereo POKEY v053 z v035 wyrównywało nagrania przy
  pierwszej niezerowej próbce; nie mierzyło absolutnej synchronizacji A/V.
- Zbadano Atari800 i jedną konfigurację rozszerzenia, nie Altirrę ani sprzęt.
- Ślady tymczasowe: `/tmp/tliktb-v051-trace.csv`, `/tmp/tliktb-v053-trace.csv`,
  `/tmp/tliktb-v051-writes.csv`, `/tmp/tliktb-v053-writes.csv`. Instrumentowany
  kod znajduje się w `/tmp/atari800-7.2.1/src/` i nie jest częścią wydania.
