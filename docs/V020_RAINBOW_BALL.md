# v020 — tęczowa piłka na PMG

[ODCZYT] Efekt aktywny tylko w ujęciu rzutu: ticki 6981–7977.
Nieruchomą piłkę usunięto z konwertowanego tła. Cztery playery składają
się na cztery pasy piłki; każdy ma osobny, cyklicznie zmieniany kolor GTIA.
Cztery missiles tworzą po trzy kolorowe krople. Po łuku piłka wpada
w okolice obręczy, opada i odbija się. Sekwencja trwa 256 ticków i powtarza
się w czasie ujęcia. Zdarzenia scen pozostają bez zmian.

## V1 / V2 / V3 — silnik

[ODCZYT] Efekt wykonuje się w vblank, również przy trafieniu cache tła.
Przykładowe podtrzymanie ujęcia kosztuje około 6100 cykli instrukcji py65,
bez DMA i NMI. Nie ma kolejnego kopiowania bitmapy ani budowania listy.
Dodatkowy bank 15 ma teraz 16 KiB: portret szkolny w pierwszych 8 KiB,
rutyna piłki pod `$6000`, przywracanie PMG pod `$6F00`.
Wrapper zapisuje i odtwarza PORTB; NMI zachowuje bank przerwanego kodu.
PMG używa `$0980–$0BFF`, podwójnej wysokości linii, czterech playerów
oraz czterech missiles. Przy wyjściu z ujęcia wracają oryginalne dane
błysków sceny tanecznej, także przy przeskoku zegara.

## V6 — sprawdzenie

[ODCZYT] 32 testy obejmują ruch, cztery jednoczesne barwy, zmianę palety,
cztery strumienie kropli, podtrzymanie bitmapy i odtworzenie PMG tańca.
W Atari800 PAL `-1088xe` sprawdzono zrzuty kilku faz rzutu, sąsiednie
ujęcia, przebitkę szkolną i cztery późniejsze kadry występu.

[ODCZYT] Pełny zapis stereo POKEY zgodny z oryginałem:
9 143 784 identyczne bajty, około 2547,1 s emulacji.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v020.xex --seconds 12
```

[ZAŁOŻENIE] Kolory GIF są przybliżeniem palety PAL. Fizyczny sprzęt
pozostaje do sprawdzenia. Podgląd: `build/v020-rainbow-ball.gif`.
