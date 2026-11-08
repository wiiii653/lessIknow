# Audyt piłki, rotatora i tunelu — v134

Aktualizacja: ścieżka wyłączająca piłkę i zbyt późne rozpoczęcie zapisu PMG
zostały poprawione w v135. Wyniki i zakres walidacji: `V135_STABILNE_PMG.md`.
Poniższy audyt opisuje stan v134.

## Potwierdzony błąd: wyłączenie piłki na widoczną klatkę

[ODCZYT] `tools/mosaic.py:159–160` ustawia `$D01D=0` i `$D400=$22`:
wyłącza wyświetlanie PMG oraz jego DMA. Dotyczy również trafienia cache.
Następnie dispatcher (`tools/build_bitmap_sequence.py:687–688`) wywołuje
osobny helper piłki. Ten ponownie czeka na `$D40B >= 124`
(`tools/tunnel_ball.py:51`), kasuje pamięć, rysuje piłkę i satelity, a dopiero
na końcu przywraca `$D01D=3`, `$D400=$2E` (linie 73–74).

[ODCZYT] Oba oczekiwania akceptują dowolną linię 248–311, bez górnej granicy
i bez wspólnego zatwierdzenia tła oraz PMG. Jeśli koniec klatki wypada pomiędzy
tymi oczekiwaniami, piłka pozostaje wyłączona przez kolejną widoczną ramkę.

[ODCZYT] Reprodukcja na kodzie 6502 z bieżącego XEX: ciepły callback,
tick 38904, początek w linii 306. Uproszczony licznik rastra:

| Zdarzenie | Linia od początku przebiegu |
| --- | ---: |
| `$D01D=0` | 311,85 |
| wejście do helpera piłki | 312,11 — już nowa klatka |
| pierwszy zapis PMG po oczekiwaniu | 560,17 — linia 248 następnej klatki |
| `$D01D=3` | 623,32 — linia 311 następnej klatki |

[WNIOSEK] Jest osiągalna ścieżka wyłączająca piłkę na prawie pełną ramkę
PAL, około 20 ms. To pasuje do zgłoszonego mrugania i odkrywania otworu
w tunelu. Kod jest wspólny dla rotatora i tunelu. Nie wymaga to błędu maski
piłki ani uszkodzenia banków. Zmiany bananów nie stworzyły tej struktury,
choć ich dodatkowe instrukcje mogą przesunąć fazę wejścia w istniejący wyścig.

## Artefakty nad piłką — ustalony zakres, przyczyna niepotwierdzona

[ODCZYT] Nad piłką celowo pojawiają się dwie gwiazdki, składane z czterech
missiles (`tools/tunnel_ball.py:61–68`). Samo pojawienie się kolorowego krzyżyka
nie dowodzi błędu; nieregularne kreski lub urwane kształty wymagają oddzielnego
potwierdzenia w obrazie rastra.

[ODCZYT] Kasowanie i zapis PMG odbywają się w jednym obszarze `$0980–$0BFF`,
bez drugiego bufora. Od pierwszego zapisu do ostatniego zapisu pamięci PMG
upływa w badanej fazie 7102 cykli instrukcji, około 62,3 linii bez DMA/NMI.
Przy początku callbacku w linii 305 PMG wraca dopiero w linii 62,66 następnej
ramki. Najwyższe gwiazdki mogą zaczynać się w okolicy linii 48 (z uwzględnieniem
ruchu pionowego rotatora), a ich konkretna pozycja zależy od fazy.

[WNIOSEK] Kod nie gwarantuje przywrócenia PMG przed pierwszą linią satelitów;
późne włączenie może ucinać ich górę. DMA i NMI dodatkowo zmniejszają zapas.
To konkretny kandydat na drugi objaw, ale nie jest jeszcze potwierdzeniem
przyczyny wszystkich zgłoszonych artefaktów. Nie wykonano przechwycenia
wadliwej klatki w emulatorze z pełnym ANTIC/GTIA.

## Dlaczego testy tego nie wykryły

[ODCZYT] `tests/test_sequence.py:33` ustawia VCOUNT stale na 124.
Testy oglądają stan po zakończeniu callbacku. Nie widzą wyłączenia PMG w jego
trakcie ani przejścia przez koniec ramki. Porównanie stereo POKEY nie sprawdza
obrazu. Dotychczasowy test otworu sprawdza gotową maskę, nie termin jej pokazania.

[ODCZYT] Dodatkowy przebieg ticków 38892–39912 co 4 ticki: 256 gotowych
stanów piłki; brak odkrytych pikseli badanego otworu według mapowania PMG
używanego przez dotychczasowy test. W tym zakresie nie znaleziono błędu
rozmiaru/pozycji gotowej maski. To nie jest test wszystkich faz rastra.

## Odtworzenie i dalsza naprawa

`/tmp/opencode/tliktb-venv/bin/python tools/audit_tunnel_pmg.py`

Wyniki: `docs/AUDIT_PMG_V134.txt`. Model przesuwa VCOUNT co 114 cykli
instrukcji, 312 linii PAL. Nie modeluje DMA, WSYNC, odczytów PMG ani NMI;
wykazuje błąd kolejności i osiągalność ścieżki, nie częstotliwość objawu
w Atari800 ani na fizycznym Atari.

[WNIOSEK] Naprawa powinna przygotowywać nową zawartość bez gaszenia poprzedniej
piłki, a tło, PMG i rejestry pozycji zatwierdzać we wspólnym, ograniczonym
oknie rastra. Potrzebny jest test przejścia przez linię 311/0 oraz obserwacja
pierwszych linii satelitów z działającym DMA i muzyką.

Nie zmieniono kodu efektu ani XEX-a w ramach tego audytu.
