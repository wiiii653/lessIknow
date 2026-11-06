# V055 — faza efektów obrazu

[ODCZYT] V055 zachowuje mapowanie taktów PAL i progi scen z v053. Dla akcentów
PMG w tańcu oraz zmian palety mozaiki przywraca fazowanie używane przez v051.
Przy początku obu ujęć mozaiki wynik odejmowania jest ograniczony do zera,
gdy scena zaczyna się przed dawnym punktem początkowym efektu.

[ODCZYT] Puls mozaiki celowo używa jak w v051 stałych odstępów 187 ticków
na półtakt. Ma więc niewielki dryf względem dokładnej siatki PAL: około
3,2 ticka przez 72 takty drugiej mozaiki, poza początkowym przesunięciem
fazy. Nie zmienia to zegara playera ani progów głównych scen.

[ODCZYT] W Atari800 7.2.1, PAL, 1088XE, Altirra OS, stereo, porównano
14 958 klatek aż do ticku 59832. Dwa wcześniej zbadane pulsy palety, które w
v053 wyprzedzały v051, w v055 ponownie przypadły na te same próbki klatkowe
co w v051: ticki 12560 i 33128. Stan scen i próbkowane rejestry POKEY są
zgodne między wersjami na wszystkich porównanych klatkach.

| Fragment | Różnice skrótu klatki v053 względem v051 | V055 względem v051 |
|---|---:|---:|
| Taniec, 748 klatek | 46 | 25 |
| Pierwsza mozaika, 748 klatek | 333 | 44 |
| Koszykówka, 748 klatek | 190 | 190 |
| Druga mozaika, 6731 klatek | 3168 | 824 |

Skróty FNV-1a identyfikują potencjalne różnice obrazu; nie zastępują oceny
wizualnej. Próba zmiany fazy kozłowania w v054 zwiększyła liczbę różniących
się klatek koszykówki do 325, więc została wycofana w v055. Animacja
koszykówki pozostaje taka jak w v053.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python` przeszedł 58
testów, w tym porównanie palet z zachowanym v051.
Wcześniejsze testy v053 miały sześć przestarzałych oczekiwań związanych z
fazą klatek po korekcie ticków; poprawiono je, zachowując kontrolę obrazu i
kosztu utrzymanej klatki.

[ODCZYT] Pełne porównanie stereo POKEY v055 z oryginalnym v035 w Atari800
dało 7 762 320 identycznych bajtów po jednokrotnym wyrównaniu początku.
Nadal potrzebny jest odsłuch i wizualne porównanie A/B: równość rejestrów
audio ani zgodność dwóch wybranych pulsów nie dowodzi idealnego dopasowania
do słyszalnego beatu.

Wydanie: `releases/visual-prototype-v055.xex`, SHA-256
`a327afb8c96b7638764e3159b196ff32bedece44907db6cb8b7c7be90c780d08`.
