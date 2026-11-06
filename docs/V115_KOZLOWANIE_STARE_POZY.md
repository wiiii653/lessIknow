# V115 — naturalne ramię z wcześniejszych ilustracji

Porównano dwie oryginalne pozy kozłowania ze źródła v024 i banku grafik
XEX v100: indeksowane piksele obu ilustracji są identyczne. Wycofano ramię
rysowane z prostych segmentów. Nowa animacja używa wyciętych z wcześniejszych
rysunków konturów ramienia, łokcia, nadgarstka i palców. Dwie pośrednie fazy
powstają z tych samych kształtów. Fazy kontaktu, pchnięcia, puszczenia i
powrotu nadal korzystają z tej samej fazy piłki PMG.

Wspólne tło i ciało pozostają stałe. Usunięto resztki starego opuszczonego
ramienia, które wcześniej mogły pozostawać pod uniesioną dłonią. Każda zmiana
nadal kopiuje fragment 44×28, czyli 308 bajtów. Poprawny adres obu buforów z
v110 jest zachowany.

Zachowano także poprawkę kolejności Trevora: podczas wejścia są tylko
spokojne pozy. Pierwszy zamach zaczyna się w części akcji, a cios 32 ticki
później. Sylwetka Trevora pozostaje zarejestrowana względem tunelu; jego
faza nie przesuwa postaci przypadkowo. Ostatni cios nie zapowiada kolejnego,
nieistniejącego uderzenia.

[ODCZYT] 77 testów zakończyło się poprawnie, w tym ciągłe odtwarzanie dwóch
odbić, zakres zapisów tła i kolejność wszystkich 40 ciosów Trevora.
[ODCZYT] Porównanie źródłowych klatek z v100 dało 0 różniących się pikseli.
[ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: zapis POKEY był zgodny z
v035 dla 5 899 680 bajtów po jednokrotnym wyrównaniu początku; obejmuje cały
utwór. Programowy podgląd odtwarza dwa kolejne odbicia na tym samym CPU i
buforach; kolory i tempo są przybliżone.

XEX: `build/visual-prototype-v115.xex`; podgląd:
`build/visual-prototype-v115-kozlowanie.gif`; SHA-256
`a9514828e9340c7b0d6a985204ce01e26f5899eddc0e0152f9810e47ebb7a2c7`.
