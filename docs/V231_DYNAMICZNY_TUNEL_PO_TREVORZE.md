# V231 — dynamiczny tunel po Trevorze

## Montaż

Odcinek od ticka 41984 do 53849 ma teraz sterowanie frazami muzycznymi.
Długość odcinka i wejście leżącego chłopca w 53850 pozostają zachowane.
Zmiana dotyczy wyłącznie okien tunelu wewnątrz dotychczasowego cyklu.

- Istniejący spiralny „wiatrak” przeplata się z organicznym tunelem.
- Kolejne akcenty zmieniają kierunek animacji i prędkość 1×/2×.
- Bazowy rytm zmian to pół taktu (około 0,94 s), z krótszym akcentem
  ćwierćtaktowym na końcu każdej czterotaktowej frazy.
- Tabela ma 72 wpisy; w oknach bananów jest celowo pomijana.
- Piłka, jej kolory i satelity działają nadal według istniejącego efektu.
  Wariant tunelu przekazywany jest także do kontrolera piłki, więc maska
  pozostaje dopasowana do aktualnej klatki i zakrywa centralny otwór.

Nie dodano bitmap ani nowych efektów PMG. Grafika obu tuneli i bananów,
wcześniejsze wystąpienia tych efektów oraz granice aktów są zachowane.
Zgłaszany wcześniej problem niepełnego obrotu bananów nie jest przedmiotem
tej zmiany.

## Kod i pamięć

`tools/post_trevor_director.py` generuje procedurę wyboru klatki oraz
tabelę punktów muzycznych. Zastępuje obliczanie globalnej klatki w głównym
callbacku; poza docelowym odcinkiem odtwarza pierwotny wynik.

- Procedura wraz z tabelami: 337 B, $EC20–$ED70.
- Rezerwa: 384 B, do $ED9F; wspólne statyczne wiersze zaczynają się w $EDA0.
- Rezerwa helpera intro wzrosła z 1888 do 2272 B; właściwy kod intro
  i terminala zachowuje adresy.
- Główny callback: 2524 B, o 36 B mniej niż w v230.
- Scratch: $0DDA. Brak nowych banków rozszerzenia i wykorzystania ich luk.

## Weryfikacja

[ODCZYT] 38 testów ukierunkowanych zaliczonych: zegar scen, granice montażu,
dwa motywy, przywracanie PORTB, PMG i zakrycie każdego piksela otworu wokół
punktów cięć. Testy sprawdzają także niezmieniony zegar bananów i wcześniejszych
ujęć.

[ODCZYT] Atari800 PAL/1088XE, stereo POKEY: 10 104 192 bajty identyczne
z v035; porównanie objęło cały utwór. Cztery muzyczne aktualizacje na ramkę
i procedury NMI nie zostały zmienione.

[ODCZYT] Pełny przebieg: 168 testów w 115,9 s; 167 zaliczonych, jeden
porównywał klatki z dawnym zegarem montażu. Zaktualizowano dobór ticków
w tym teście, zachowując sprawdzenie wszystkich 64 bitmap i własności
nieaktywnego bufora. Ponowny przebieg modułu: 4/4 zaliczone. Kod XEX nie
wymagał po tym zmian; łącznie wszystkie 168 przypadków zweryfikowane.

[ODCZYT] Koszt samego directora w punktach tabeli: 85–1348 cykli NMOS
6502. To pomiar CPU bez ANTIC DMA i muzycznych NMI, nie pomiar FPS.

Podgląd rekonstrukcji CPU/PMG: `build/post-trevor-v231.gif`.
To rekonstrukcja klatek, nie pomiar FPS ani zapis z fizycznego Atari.
