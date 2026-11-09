# V242 — stały dolny kadr bez przywracania starszej display listy

Po przesunięciu outro w v240 do 51850 guard w `title_plasma.invalidate`
nadal porównywał tick ze starym, wpisanym na sztywno 53850. Każde kolejne
wywołanie podczas pierwszych 2000 ticków końcówki uznawał za seek wstecz.
Przywracał normalne listy, publikował $8400, a terminal ponownie publikował
$BC00. Chociaż końcowy stan callbacku był poprawny, pomiędzy publikacjami
ANTIC mógł zobaczyć wyższy kadr. Stąd miganie/dwa położenia postaci.

Guard pobiera teraz obie części granicy z `outro_text.START`. W aktualnym
outro nie wywołuje resetu, a prawdziwy seek przed 51850 nadal przywraca
normalne listy dla wcześniejszych scen. Grafika, pozycja PMG, start i koniec
terminala, palety oraz muzyka pozostają zachowane.

Nowa regresja śledzi zapisy przy kolejnych callbackach od 51854 do 53870:
po pierwszej publikacji nie wolno pisać $D403 ani przywracać normalnych
DL $8000/$8400; stan terminala musi pozostać 2, a mapa dolnej bitmapy stała.
Test **odtwarza błąd na v241 już w 51854** i przechodzi na v242.
Wcześniejsze testy sprawdzały stan po callbacku, co nie wykrywało chwilowego
przełączenia na starą listę i powrotu przed końcem wywołania.

[ODCZYT] 23 testy ukierunkowane zaliczone, w tym nowa regresja, terminal,
publikacja PMG, pozycja postaci, finał i fade.

[ODCZYT] Pełna regresja: **185/185 testów**, bez pominięć, 122,9 s.
Atari800 PAL/1088XE, cały utwór stereo: **10 731 888 bajtów identycznych
z v035**. Bez próby na fizycznym Atari. XEX różni się od v241 dokładnie
dwoma bajtami, zachowuje rozmiar; build roboczy zaktualizowany do v242.
