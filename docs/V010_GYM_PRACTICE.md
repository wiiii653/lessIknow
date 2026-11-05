# Wejście do sali po scenie przed szkołą — v010

Data: 2026-11-04. Wynik: `build/visual-prototype-v010.xex`.

## Przejście i obraz

- [ODCZYT] Ostatni kadr dziewczyny przy wejściu pozostaje do ticka 5983.
  Od ticka **5984** (około 30 s) scena 13 pokazuje wnętrze sali: dwóch
  koszykarzy, rzut i odbicie piłki oraz dwie dziewczyny rozciągające się
  przy drewnianych drabinkach. Ten kadr zastępuje zatrzymanie na chłopcu.
- [ODCZYT] Trening zajmuje 2992 ticki, około 15 s. Taniec zaczyna się przy
  **8976**, następna tancerka dołącza przy **9724**, trzecia przy **10472**;
  żaden z tych progów nie został przesunięty.
- [ODCZYT] Postacie i sala są bitmapą; piłka jest animowanym graczem PMG 0,
  poruszanym po 32-elementowej trajektorii według licznika muzyki. Pozostałe
  gracze są poza ekranem. W chwili rozpoczęcia tańca DMA graczy jest wyłączane.
- [ODCZYT] Źródło: `tools/gym_practice.py`. Podgląd:
  `build/v010-gym-practice.png`, render z callbacku i list ANTIC w py65.
  Kolory RGB są przybliżone; bitmapę sprawdzono również w Atari800.

## V2/V3 — banki i własność pamięci

- [ODCZYT] Kadr treningu mieści się w ostatnich 8192 B banku 8 (offset
  `$2000–$3FFF`, okno CPU `$6000–$7FFF`). Builder sprawdza, że ten obszar
  oryginału zawiera wyłącznie `$FF`. Dekoder v035 kończy odczyt banku 8
  na offsecie 2819, więc wymagany znacznik końca pozostaje zachowany.
- [ODCZYT] Banki 1–7 oraz pierwsze 8192 B banku 8 pozostają bajtowo
  identyczne. Banki 9–14 zachowują kadry tańca z poprzedniej wersji.
- [ODCZYT] Trening korzysta z istniejących dwóch buforów `$9000/$B000`
  i tego samego kopiowania przerywanego przez muzykę. Test obejmuje NMI
  podczas kopiowania także z banku 8 oraz poprawne przywrócenie PORTB.
- [ODCZYT] Dane PMG piłki zajmują `$0A00–$0A7F`; scena używa 2-liniowego
  DMA gracza. Listy ANTIC i odstępy muzycznych DLI nie zostały zmienione.
- [ODCZYT] Callback z wrapperem i trajektorią: 1621 B, `$1400–$1A54`.
  Wrapper NMI pod `$19EF`. Statyczne wiersze i rozmiar tablic bez wzrostu:
  425 wierszy, 16 515 B, tablice 3264 B.

## V6 — regresja odtwarzania i sprawdzenie scen

- [ODCZYT] Atari800, PAL, `-1088xe`, Altirra OS, stereo POKEY, headless.
  Porównanie z v035: **6 139 440 identycznych bajtów** rejestrów stereo
  POKEY, około **1710,2 s** emulacji; cały utwór objęty testem. Ciszę
  początkową wyrównano raz, bez przesuwania próbek w trakcie utworu.
- [ODCZYT] W monitorze Atari800 zatrzymywano callback po powrocie pod
  `$220D`, zapisując pamięć list obrazu i bitmap. Obrazy treningu przy
  snapshotach 6016 i 6144 oraz tańca przy 9152 były zgodne pikselowo
  z referencjami. Przy ticku **8976** odczytano scenę **3** i przesunięcie
  wejścia **192**, zgodnie z wcześniejszym początkiem tańca.
- [ODCZYT] W teście obrazów ustawiano licznik, aby szybko odwiedzić wybrane
  sceny; porównanie POKEY objęło normalny przebieg bez zmiany licznika.
- [ODCZYT] 21 testów zakończonych powodzeniem: granica wejścia do sali,
  granica tańca, trajektoria i DMA piłki, bitmapa sali, przerwania bankowe,
  szkoła, NORTH, tytuł, wszystkie grupy i pozy tancerek.
- [ODCZYT] Nie wykonano odsłuchu ani testu na fizycznym Atari.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v010.xex --seconds 10
```

[ODCZYT] Poprzedni XEX v009 pozostał bez zmian:
`258d94eb37b9efb080438c15276bea685dfd9ef3859a7bb9e5507e95361c2ed6`.
Nowy v010: `3dd2dc3a81485621eb1371874114bdb56e14b3f2f46793bbed059c4b34ba1771`.
