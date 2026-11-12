# Stan projektu — 12 listopada 2026, v330

## Aktualne wydanie

- Stereo release 058: `releases/less-i-know-demo-release-058-stereo.xex`
- Rozmiar: 936 240 B; SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`
- Źródłowy build: `build/visual-prototype-v330.xex`; pakiet v330 jest w `releases/less-i-know-sv2026we-v330-submission/` oraz ZIP obok.
- Czas: ok. 4:20.7; terminal od ticku 41884, koniec tekstu 51232, fade od 51232, trwała czerń od 51980.
- Trevor kończy się przy ticku 29656. Director przejmuje sterowanie na pierwszym callbacku po nim, bez resetu fazy bananów. Od taktu 80 zmienia motyw, kierunek i prędkość na granicach taktów. Oczy dziewczyny: 39379–40126.

Aktualny timeline po Trevorze: [montaż v330](AKTUALNY_MONTAZ_V330.md). Zmiana wydania: [v330](V330_KROTSZY_MONTAZ_I_DIRECTOR.md). Szczegółowa historia pozostaje w notatkach Vxxx; ten plik opisuje tylko stan bieżący.

## Walidacja i ograniczenia

- 28 ukierunkowanych testów py65 dla rotatorów, granic scen, timeline’u i creditsów zaliczyło v330.
- Pełnego `make check` po ostatnich zmianach nie uruchomiono. Nie należy deklarować, że cały zestaw testów przechodzi. Usunięto nieaktualne porównanie z XEX v198, test wydzielonego projektu pomponów oraz dawne asercje cyklu rotatora zastąpione testami aktualnego directora.
- Użytkownik potwierdził, że v330 działa bez zarzutu z karty AVG na Atari 1088 Rambo. To pozytywna próba pełnego przebiegu na docelowym sprzęcie; nie wykonano osobnego pomiaru FPS ani nowego porównania stereo POKEY.
- Ostatnie pełne porównanie ścieżki stereo z playerem v035 dotyczy starszego buildu v260. Nie powtarzano go dla v330.
- Wszystkie 64 banki są przydzielone. Nie wnioskować o wolnej pamięci ze starszych raportów odzysku; przed zmianą sprawdzać bieżący allocator i JSON buildu.
- Budujemy wyłącznie stereo. Wariant mono jest wycofany.

## Zamknięcie projektu

Główne sceny i montaż są ukończone. Próba release 058 na Atari 1088 Rambo z kartą AVG została potwierdzona jako bezproblemowa. Pełne `make check` i nowe porównanie stereo POKEY nie były uruchamiane dla v330. Termin zgłoszeń Silly Venture 2026 WE (12 listopada 2026, 12:00 CET) minął; w repo nie ma potwierdzenia wysłania formularza. Nie deklarować zgłoszenia ani gotowości konkursowej bez takiego potwierdzenia.

Status paczki i autorstwa muzyki: [przygotowanie SV](SV2026WE_PRZYGOTOWANIE.md). Pierwotne cele audytu V1–V7 i dokumenty `TLIKTB_*` są materiałem projektowym/historicznym, nie listą blokującą release.
