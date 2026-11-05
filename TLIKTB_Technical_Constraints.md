# The Less I Know The Better - Atari XE 1MB: ograniczenia techniczne

Dokument dla agenta kodującego. Uzupełnia `TLIKTB_Atari_Timeline_v2.md` (co i kiedy) i `TLIKTB_Asset_List.md` (z czego). Tu jest: w jakich granicach i co jest sprawdzone.

Każde twierdzenie ma status:

- **[ODCZYT]**: odczytane bezpośrednio z pliku `less-i-know-hook-v024.xex` (struktura XEX, deasemblacja, teksty na ekranie playera)
- **[WNIOSEK]**: wynika z czytania kodu, ale nie było testowane w emulatorze
- **[ZAŁOŻENIE]**: przyjęte bez sprawdzenia

Nie traktuj [WNIOSEK] i [ZAŁOŻENIE] jak faktów. Zadania V1-V7 na końcu je weryfikują i należy je wykonać przed budową silnika.

## 1. Sprzęt i cel

- Atari 65XE z rozszerzeniem do 1 MB, PAL, stereo POKEY (drugi POKEY pod `$D210`)
- [ZAŁOŻENIE] 64 banki po 16 KB poza 64 KB pamięci głównej. Układ bitów PORTB zależy od konkretnego rozszerzenia (patrz sekcja 3).
- Emulator do testów: Altirra, 65XE, 1 MB, PAL, drugi POKEY włączony. Układ banków w konfiguracji pamięci emulatora musi odpowiadać układowi wykrywanemu przez player.
- Cykli na klatkę PAL: ok. 35 568 (312 linii × 114 cykli), pomniejszone o DMA ANTIC-a i przerwania.

## 2. Plik playera `less-i-know-hook-v024.xex`

**[ODCZYT]**

- Rozmiar 233 468 B, 40 segmentów XEX.
- Kod i dane w pamięci głównej: segmenty od `$2000` do `$37BF` (kod `$2000-$24B2`, dane i tablice `$24BD-$28BC`, bufor rejestrów `$2900-$293F`, dalej `$2A00-$2F7E`, display lista `$3300-$3323`, ekran tekstowy `$3400-$37BF`).
- Rejestr zestawu znaków (CHBASE) ustawiany na `$38`, czyli font w `$3800-$3BFF`. Tego fragmentu nie ma w pliku, więc powstaje w czasie działania (skąd, nie wiadomo).
- 14 segmentów po 16 KB wczytywanych do `$8000-$BFFF`. Po każdym wywoływany jest INIT `$20EA`, który kopiuje blok do banku (okno `$4000-$7FFF`, wartość PORTB z tablicy). `$8000-$BFFF` to tylko miejsce przejściowe.
- Prawdziwe dane muzyczne: ok. 98,9 KB (6 pełnych banków plus 3 017 B w siódmym). Banki 8-14 to identyczne bloki wypełnione `$FF`.
- Wykrywanie pamięci: INIT `$2000` próbuje trzech tablic wartości PORTB (po 14), zapisując numer banku w `$4000` i sprawdzając odczyt. Po trzech porażkach wyświetla błąd.
  - Tablica 0 (`$270A`): `81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB`
  - Tablica 1 (`$2718`): `03 07 0B 0F 43 47 4B 4F 83 87 8B 8F C3 C7`
  - Tablica 2 (`$2726`): `83 87 8B 8F A3 A7 AB AF C3 C7 CB CF E3 E7`
  - Indeks pasującej tablicy zostaje w `$249D`.
- Rozmiar bloku `$FF` w bankach 8-14 sugeruje, że loader rezerwuje więcej niż potrzeba. Przycięcie do 7 banków oszczędza ok. 112 KB, ale wymaga weryfikacji V3.
- Teksty na ekranie playera: 128 BPM, 05:00, „4 UPDATES PER PAL FRAME / 199.443 HZ”, „STEREO POKEY / SILLY VENTURE 2026”, „POKEY PORT/REMIX BY OGNJEN”, „ORIGINAL: TAME IMPALA”. START = pauza/odtwarzanie, SELECT = restart.

## 3. Zachowanie playera

**[ODCZYT]**

- Player jest sterowany przez DLI, nie VBI. Wektor DLI (`$0200/$0201`) wskazuje `$2210`. W RUN `$D40E` ma wartość `$80`.
- Display lista playera (`$3300`) ma bit DLI w czterech instrukcjach, które zaczynają się w liniach 0, 73, 151 i 229 (licząc od początku listy). DLI wyzwala się na ostatniej linii instrukcji, więc praktycznie ok. linie 0, 78, 156, 234. Odstęp ok. 78 linii = 312/4, co daje 4 aktualizacje na klatkę.
- Aktualizacja: bufor `$2900-$2911` (18 bajtów) trafia do `$D200-$D208` i `$D210-$D218` (rutyna `$2C00`). `$D20F` i `$D21F` ustawione na 3 przy starcie.
- Licznik 24-bitowy `$24A7-$24A9` rośnie w ścieżce aktualizacji (`$22F4`). Licznik `$24AA-$24AC` rośnie przy każdym DLI, a pętla główna odświeża UI co 4. DLI.

**[WNIOSEK]**

- Pauza (START) zatrzymuje licznik `$24A7-$24A9`, bo omija ścieżkę aktualizacji.
- Koszt ticka: rutyna `$2C00` wykonuje ok. 21 par odczyt-zapis (kilkaset cykli), plus dekoder strumienia, którego nie prześledziłem. Całość jest nieznana.
- DLI to NMI, więc `SEI` go nie blokuje. Tick może przerwać dowolny kod, także w trakcie przełączania banku. Szczegóły w sekcji 4.

## 4. Ograniczenia dla silnika wideo

1. **Muzyka nie może stracić ticków.** Cztery DLI na klatkę w odstępach ok. 78 linii. Nie wiadomo, czy nierówne rozmieszczenie psuje rytm (V6), więc zachowaj odstępy. Własny handler DLI może obsługiwać także efekty (zmiany palety), ale tick musi wykonać się punktualnie.
2. **PORTB.** Player ustawia PORTB przy przełączaniu banków. Nie wiadomo, czy po ticku przywraca poprzednią wartość (V2). Do czasu weryfikacji silnik musi sam zabezpieczyć: handler DLI zapisuje PORTB na wejściu, wywołuje tick, a przed RTI przywraca zapisaną wartość. Dotyczy to też trybu, w którym ANTIC czyta z banku rozszerzonego.
3. **Banki.** Loader zajmuje 14 banków. Wolne: 50 (ok. 800 KB), po przycięciu 57 (ok. 912 KB) [ZAŁOŻENIE: 64 banki]. Silnik musi omijać banki, w których siedzi muzyka (zależnie od dopasowanej tablicy PORTB, sekcja 2).
4. **Pamięć główna.** Dopóki V3 i sprawdzenie okolic `$3800` nie dadzą odpowiedzi, traktuj `$0200-$02FF` i `$2000-$3FFF` jako zarezerwowane przez player.
5. **CPU.** Budżet klatki to ok. 35 568 cykli minus DMA ANTIC-a (tryby bitmapowe zabierają dużo), minus 4 ticki. Efekty z DLI na każdą linię lub z ciężkimi tablicami (tunel, zoom, rotacje, kalejdoskop) zmierz wcześnie.
6. **Zegar.** Zdarzenia z timeline'u wyzwalaj po liczniku ticków playera, nie po klatkach VBI. VBI w PAL to ok. 49,86 Hz, a nie 50,0.

## 5. Zadania weryfikacyjne (przed budową silnika)

Wykonuj w Altirze. Każde zadanie kończy się krótką notatką: wynik i czy zmienia założenia powyżej.

- **V1.** Profiler: koszt ticka (od wejścia w `$2210` do RTI), minimum, średnia, maksimum cykli.
- **V2.** Czy tick przywraca PORTB: odczytaj kod ścieżki aktualizacji i sprawdź w teście, przełączając bank w pętli głównej podczas odtwarzania i słuchając artefaktów.
- **V3.** Czy player czyta banki 8-14: loguj zapisy do `$D301` podczas całego 5-minutowego odtwarzania, wyznacz największy używany bank. Ustal też, która tablica PORTB została dopasowana (`$249D`) w docelowej konfiguracji.
- **V4.** Czy pauza zatrzymuje `$24A7-$24A9`.
- **V5.** Porównaj v024 z v035: adresy licznika, DLI, wektor, układ pamięci.
- **V6.** Czy tick wymaga równych odstępów DLI: przesuń DLI i sprawdź rytm.
- **V7.** Przytnij loader do 7 banków, zbuduj i przesłuchaj całość.

## 6. Konwencje assetów (propozycja do akceptacji)

- Tryby: ANTIC E (160×192, 4 kolory, 40 B na linię, 7 680 B na ekran) jako domyślny. Tryb znakowy ANTIC 4 lub 5 dla teł, fontów i tekstów. PMG w rozdzielczości 1 linii (256 B na gracza na klatkę) dla postaci. GTIA 9 (80×192) dla wybranych scen aktu 5 (do decyzji, patrz sekcja 8).
- Paleta: 6-8 kolorów z palety Atari (róż, magenta, cyjan, żółć), konkretne wartości do ustalenia. Paleta per scena w osobnym pliku `.pal`.
- Formaty plików: surowe bitmapy `.bin` (7 680 B na ekran E), palety `.pal`, PMG `.pmg`, fonty `.fnt`, wszystkie dane kompresowane ZX0 (`.zx0`). Nazewnictwo `snake_case` z prefiksem aktu, np. `act2_hearts_tile.bin`, zgodnie z `TLIKTB_Asset_List.md`.
- Konwerter: skrypt w Pythonie (Pillow): obraz źródłowy, dithering (Bayer lub Floyd-Steinberg), wyjście `.bin` plus `.pal`.
- Dekompresja ZX0 trwa kilka klatek na pełny ekran. Rozpakowuj następną scenę w tle do ukrytego banku, nie w trakcie wyświetlania.

## 7. Zasady pracy

- Nie zmieniaj granic aktów, ticków ani priorytetów produkcyjnych bez potwierdzenia człowieka.
- Kolejność prac z asset list: Trevor PMG, Cheerleader PMG, Kaleidoscope, Tunnel, Finale Trevor, Credits.
- Każdy build testuj w Altirze w konfiguracji z sekcji 1 i słuchaj, czy muzyka nie gubi rytmu.
- Zaznaczaj w notatkach, co zweryfikowałeś, a co założyłeś.

## 8. Otwarte decyzje (dla człowieka)

- GTIA 9 w akcie 5: w którym bloku, i dopisanie assetów (palety, obrazy źródłowe).
- Czy zachować UI playera (ekran tekstowy) w demie, czy usunąć.
- Zasady compo: czy dopuszczalne są interlace i flicker, jaki jest standard (PAL), jakie są limity rozmiaru i sprzętu.
- Docelowy układ rozszerzenia pamięci 1 MB i emulator referencyjny.
