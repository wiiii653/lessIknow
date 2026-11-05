# Silnik v013 — cache, częściowe kopie i PMG

## V1 — CPU i muzyka

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 26 testów OK.
Profil py65 zapisano w `build/engine-profile-v013.json`. Koszty instrukcji
callbacku bez DMA ANTIC, NMI muzyki i oczekiwania na vblank:

| Przypadek | v011 | v013 |
| --- | ---: | ---: |
| Nieruchomy tytuł | 16166 | 403 |
| Nieruchoma szkoła | 16340 | 454 |
| Nieruchomy trening | 93424 | 434 |
| Zmiana pozy solo po zapełnieniu buforów | 93788 | 70272 |
| Zmiana pozy duo po zapełnieniu buforów | 93773 | 70213 |
| Zmiana pozy trio po zapełnieniu buforów | 93754 | 69785 |
| Ta sama poza solo | 93788 | 984 |

[ODCZYT] Pierwsze napełnienie bufora nadal kosztuje około 93 tys. cykli.
Pełna kopia: 7936 B, częściowa: 5376 B (strony 4–24). To konserwatywny
obszar zmian, sprawdzany przy budowaniu dla każdej pary póz w danej grupie.
Klucze zawartości obu buforów zapobiegają użyciu różnic z niewłaściwej klatki.
Nie jest to kopiowanie wyłącznie pojedynczych zmienionych bajtów.

[ODCZYT] Pełny test w Atari800 PAL, rozszerzenie `-1088xe`, stereo POKEY:

```sh
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v013.xex --seconds 12
```

Wynik: 8 792 424 identyczne bajty stereo POKEY, około 2449,2 s emulacji.
Jednorazowe wyrównanie początku nagrania; cały utwór objęty porównaniem.

[WNIOSEK] Typowa zmiana pozy zużywa około 25% mniej cykli instrukcji,
a nieruchome ujęcia zwalniają prawie cały wcześniejszy koszt renderera.
Nie wyznacza to gwarantowanego wolnego budżetu w każdej linii rastra.

## V2 / V3 — pamięć i przerwania

[ODCZYT] Każdy bufor ma osobny klucz zawartości. Cache obrazu uwzględnia
ujęcie, przesunięcie wejściowe i amplitudę kalejdoskopu. Cache-hit nadal
aktualizuje paletę i PMG w vblank. Wrapper muzyki odtwarza foreground PORTB.
Test przerwań podczas kopiowania i kontrola oryginalnych banków przechodzą.
Pomocniki zajmują końce buforów: `$AF00–$AFD5` oraz `$CF00–$CFC3`;
kopiowanie ich nie obejmuje. Missiles `$0980–$09FF`, players `$0A00–$0BFF`.

## V6 — obraz i akcenty

[ODCZYT] W rzeczywistym Atari800 sprawdzono 14 kolejnych zrzutów pamięci
po callbacku: nieruchomy trening, trzy ujęcia, napełnianie obu buforów,
częściowe kopie solo, duo i trio. Każdy raster zgadza się piksel w piksel
z materiałem źródłowym. Testy py65 sprawdzają także dowolną kolejność póz.

[ODCZYT] Cztery gwiazdki playerów i cztery kreski missiles pulsują nad
postaciami, przez 24 ticki co około 93/94 ticki. Kolory przechodzą od jasnego
ciepłego przez cyjan do różu. Dane PMG są wczytane z góry; callback zmienia
rejestry. DMA PMG jest wyłączone poza aktywną fazą efektu. Podgląd:
`build/v013-dance-pmg.png`.

[ODCZYT] Granice scen i progi ticków pozostają takie jak w v011.

[ZAŁOŻENIE] Nie wykonano odsłuchu na fizycznym Atari ani pomiaru zapasu
cykli w każdej linii z DMA PMG. Pełna walidacja sprzętowa V1–V7 pozostaje
osobnym zadaniem; porównanie POKEY dotyczy wskazanego emulatora i konfiguracji.
