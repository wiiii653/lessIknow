# V138 — BANG/BAM i kolorowy rozpad chmurki

## Efekt ciosu

[ODCZYT] Kolejne ciosy przeplatają BANG i BAM. Krótszy napis jest wycentrowany
we wspólnej chmurce. Czcionka pozostaje czarna podczas fazy czytelnego słowa,
a tło na missiles cyklicznie zmienia jasne barwy.

| Wiek od ciosu, ticki | Faza |
| --- | --- |
| 0–7 | Rozbłysk i rozwinięcie chmurki |
| 8–79 | Czytelne BANG albo BAM |
| 80–103 | Litery znikają; cztery kolorowe fragmenty players odrywają się od środka |
| 104–119 | Chmurka rozchodzi się na boki; cztery missiles tworzą rozdzielone szczątki |
| 120–135 | Zmniejszone players i missiles, małe osobne fragmenty z przerwami |
| od 136 | Efekt gaśnie przed następnym ciosem |

[ODCZYT] Nie zmieniono `HITS`, sekwencji rąk, granic scen ani ticków muzyki.
Istniejąca końcówka rozprysku nadal może trwać podczas kolejnego zamachu.
Paleta fragmentów używa cyklu 16 odcieni i przesunięć między czterema players.
W początkowej chmurce missiles działają jako piąty gracz; po rozpadzie
otrzymują cztery odpowiadające players kolory. Barwy zmieniają się na PMG,
bez przemalowywania Trevora ani jego tła. Nie dodano DLI.

## Pamięć i raster

[ODCZYT] Helper Trevora wzrósł z 1748 do 2395 B i nadal mieści się w swoim
slocie `$6000–$69FF`. Pozostaje 165 B do granicy `$6A00`, gdzie w banku 49
zaczynają się wstęgi. Kod jest powielony w 16 bankach akcji i banku wejścia:
przyrost zajętych danych wynosi 17 × 647 B = 10 999 B, w istniejących bankach.
Nie dodano banków ani obrazów źródłowych. Nadal używane są wszystkie 64 banki.

[ODCZYT] Efekt korzysta z już wydzielonych buforów PMG `$0980–$0BFF` oraz
`$8980–$8BFF`. Operandy zapisów są kierowane do nieaktywnego bufora;
pozycje, rozmiary, paleta i PMBASE są zatwierdzane w oknie początku wygaszania.
Poprzedni obraz PMG nie jest kasowany podczas przygotowania następnego.
Poza aktywnym efektem PMG może być wyłączone, zgodnie z dotychczasową sceną.

## Dokumentacja i źródła

Zaktualizowano `AGENTS.md`, `README.md`, `docs/PLAN_STATUS.md`, timeline
i ograniczenia techniczne. Aktualna mapa odróżnia indeksy loadera od PORTB,
oznacza sloty V120 jako już zajęte, opisuje podwójny PMG, blokadę dawnego V7
oraz braki aktów 5–8. Historyczne notatki wydań pozostają zachowane.

Kod: `tools/trevor_polished.py`. Nowe testy sprawdzają oba napisy, oba kierunki
ciosu, separację/kurczenie i kolory fragmentów, brak zapisów do aktywnego PMG,
późne pozycje rastra, przerwania dekodera z odtworzeniem PORTB i powrót do tańca.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 283 288
identycznych bajtów z v035, cały utwór. Nie jest to odsłuch fizycznego Atari.
Testy ruchomego VCOUNT nie modelują DMA ANTIC ani rzeczywistych pobrań GTIA.

Podgląd: `build/v138-bang-bam.gif`, sekwencyjne callbacki co 4 ticki,
przybliżona paleta i tempo; to nie nagranie pełnego emulatora.
Wydanie: `build/visual-prototype-v138.xex`.

[ODCZYT] Końcowy `make check`: 94 testy, 91 zaliczonych, 3 pominięte
z powodu braku archiwalnego v126; 84,481 s. Test rzeczywistych NMI dekodera
potwierdza identyczny gotowy PMG i rejestry po przerwanym renderowaniu.
Roboczy XEX jest identyczny z v138.
SHA-256: `0f37cc4d8edab22027ee34a9c248cf68f91b22989f04dec40615805287dd83e1`.
