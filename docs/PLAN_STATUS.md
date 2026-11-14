# Stan projektu — 14 listopada 2026, kandydat v352

## Aktualne wydanie

- Stereo release 058: `releases/less-i-know-demo-release-058-stereo.xex`
- Rozmiar: 936 240 B; SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`
- Najnowszy kandydat stereo: `build/visual-prototype-v352.xex`; SHA-256: `b3031752e9615e3f69c7ab877cb115c1d798b39efdb500e1b0ee00d63f795d1d`.
- Ostatnie wydanie produkcyjne pozostaje stereo release 058 / v330. Źródło v330: `build/visual-prototype-v330.xex`; paczka SV v330 pozostaje w `releases/less-i-know-sv2026we-v330-submission/` oraz ZIP obok.
- Czas v352: ok. 4:20.7; terminal od ticku 41884, tekst do 51232, fade od 51852, końcowa karta od 51980.
- Trevor kończy się przy ticku 29656. Director przejmuje sterowanie na pierwszym callbacku po nim, bez resetu fazy bananów. Od taktu 80 zmienia motyw, kierunek i prędkość na granicach taktów. Oczy dziewczyny: 39379–40126.
- Director steruje także rotatorami od ticku 11967 i tunelem od 20942 do 21689. BUM/BAM i dymki pojawiają się na ostatnich bananach przed oczami oraz na bananach po nich. Szczegóły: [v352](V352_BANANY_PRZED_OCZAMI.md).
- V349 dodaje mniejszy dymek, wygaszenie i niezależną szeroką ósemkę: [notatka](V349_BUM_BAM_OSEMKA.md).
- V350 wydłuża dolot piłek Trevora z 32 do 48 ticków, zachowując momenty uderzeń: [notatka](V350_PILKI_TREVORA.md).
- V351 poprawia dolne piksele cyfry 7 w foncie creditsów: [notatka](V351_CYFRA_7.md).
- V352 włącza BUM/BAM od taktu 104 na bananach przed oczami, zachowując ujęcie oczu z piłką i satelitami.

Zmiany v331 obejmowały większe serce; wadliwy dodatkowy parallax chmur został usunięty w v333, bo przesuwał górę głowy idącej dziewczyny. V332 dodawał ruch stopy leżącego chłopaka co beat; animację wycofano w v335 i przywrócono statyczną pozę z v330. V334 rozjaśnia i nasyca paletę serca. V336 wyrównuje jasność klatek ciosu Trevora. V338 przełącza późne rotatory bananowe na BUM/BAM, pozostawiając piłkę w tunelach: [notatka v338](V338_BUM_BAM_W_BANANACH.md). V339 przywrócił loader i końcówkę z v300, co przesunęło finał o ok. 40 sekund i usunęło kartę końcową. V340 poprawił ósemkę BUM/BAM, satelity i serce: [notatka v340](V340_BUM_BAM_OSEMKA_I_SERCE.md). V341 przywrócił timing i kartę końcową v330 oraz tor piłki w ujęciu oczu: [notatka v341](V341_OCZY_OSEMKA_FINAL_V330.md). V342 przywrócił tekst loadera v330; v343 dodaje postęp kropek po kolejnych bankach bez przesuwania napisu: [notatka v343](V343_LOADER_PROGRESS_DOTS.md). Szczegóły wcześniejszych zmian: [v331](V331_CHMURY_I_SERCE.md), [v332](V332_STOPA_W_RYTMIE.md), [v333](V333_NAPRAWA_PANORAMY.md), [v334](V334_PALETA_SERCA.md), [v335](V335_STOPA_STATYCZNA.md), [v336](V336_PALETA_TREVORA.md).

Aktualny timeline po Trevorze: [montaż v330](AKTUALNY_MONTAZ_V330.md). Zmiana wydania produkcyjnego: [v330](V330_KROTSZY_MONTAZ_I_DIRECTOR.md). Szczegółowa historia pozostaje w notatkach Vxxx; ten plik opisuje tylko stan bieżący.

## Walidacja i ograniczenia

- 28 ukierunkowanych testów py65 dla rotatorów, granic scen, timeline’u i creditsów zaliczyło v330.
- Pełnego `make check` po ostatnich zmianach nie uruchomiono. Nie należy deklarować, że cały zestaw testów przechodzi. Usunięto nieaktualne porównanie z XEX v198, test wydzielonego projektu pomponów oraz dawne asercje cyklu rotatora zastąpione testami aktualnego directora.
- Użytkownik potwierdził, że v330 działa bez zarzutu z karty AVG na Atari 1088 Rambo. To pozytywna próba pełnego przebiegu na docelowym sprzęcie; nie wykonano osobnego pomiaru FPS ani nowego porównania stereo POKEY.
- v352 zbudowano jako stereo (298 współdzielonych wierszy, 2542 B kodu). Siedem testów directora i dziewięć testów Trevora przeszło w py65. Piłkę i PMG w oczach porównano z v351 w pięciu momentach. Emulatora ani Atari nie uruchamiano; v330 pozostaje ostatnią wersją sprawdzoną na sprzęcie.
- Ostatnie pełne porównanie ścieżki stereo z playerem v035 dotyczy starszego buildu v260. Nie powtarzano go dla v330.
- Wszystkie 64 banki są przydzielone. Nie wnioskować o wolnej pamięci ze starszych raportów odzysku; przed zmianą sprawdzać bieżący allocator i JSON buildu.
- Budujemy wyłącznie stereo. Wariant mono jest wycofany.

## Zamknięcie projektu

Główne sceny i montaż są ukończone. Próba release 058 na Atari 1088 Rambo z kartą AVG została potwierdzona jako bezproblemowa. Termin zgłoszeń Silly Venture 2026 WE minął; w repo nie ma potwierdzenia wysłania formularza. Nie deklarować zgłoszenia ani gotowości konkursowej bez takiego potwierdzenia.

Status paczki i autorstwa muzyki: [przygotowanie SV](SV2026WE_PRZYGOTOWANIE.md). Pierwotne cele audytu V1–V7 i dokumenty `TLIKTB_*` są materiałem projektowym/historicznym, nie listą blokującą release.

## Release 061 i AVG

Kandydat stereo `releases/less-i-know-demo-release-061-stereo.xex` (v352), SHA-256 `90426fde4adcbfc83f7e52c8ec93265112da518ee85f8464d54a88b5e819e433`. Paczka: `releases/less-i-know-sv2026we-v352-release061-submission.zip`. Release 059 i 060 nie uruchomiły się na sprzęcie użytkownika (AVG, Atari 1088 Rambo); nie używać ich do zgłoszenia. Release 061 zawiera ekran loadera, 66 wrapperów INIT i bootstrap identyczne bajtowo z działającym release 058; liczby INIT i adresy porównano z release 058. Start release 061 na fizycznym Atari pozostaje niepotwierdzony.
