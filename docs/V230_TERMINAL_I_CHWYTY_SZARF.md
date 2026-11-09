# V230 — cztery ostatnie uwagi: terminal, szarfy, jasność i szósty wiersz

## Terminal

- Prompt `XE:> ` i wszystkie litery są wyrównane do stałych kolumn.
  Nie ma poziomego falowania. Pisanie, pauza przed wpisem, Enter i blokowy
  kursor działają jak w sesji terminala; podczas pisania kursor jest pełny,
  przed/po nim miga. Nagłówki SYS.OPEN / UPLINK i wszystkie credits zachowano.
- Dodano szósty wiersz — status `[XE-OS] LINK:ONLINE // SV2026 [OK]`.
  Pozostałe pięć wierszy to przewijana historia z promptami.
- Aby nie ruszyć chłopca, dodatkowy wiersz zastępuje pierwsze osiem czarnych
  linii bitmapy. Display lista pokazuje 184 pozostałe linie w tych samych
  fizycznych pozycjach. Żaden piksel postaci nie jest ucinany ani skalowany.
- Zielone litery mają teraz luminancję $0E zamiast $0C. Raz na około 1,28 s
  pojawia się jednoramkowa zmiana zieleni na biel i pojedynczy artefakt w
  statusie. Pozycje liter i kolor skóry pozostają stałe; tło jest czarne.
- Zwykłe muzyczne DLI pozostają po 1/79/157/235 liniach. Dodatkowy split
  palety wypada po 49, jest rozpoznawany przy VCOUNT 28 i nie dekoduje muzyki.

## Chwyty szarf

Audyt wykazał błędne nominalne dłonie w bazowej pozie 3 i stosowanie punktów
starego arkusza do czterech klatek ćwiartkowych. Poprawiono widoczną dłoń
pozy 3 i dodano osobne QUARTER_HANDS dla nowego arkusza. Ponieważ poza 3 ma
jedną widoczną dłoń, oba strumienie środkowej postaci wychodzą z tej dłoni.
Nie dorysowano innej sylwetki.

Po przeliczeniu współrzędnych punkt chwytu zostaje przyciągnięty najwyżej
w obrębie 4 pikseli do skóry tej konkretnej postaci (nie podłogi ani sąsiadki).
Brak takiego punktu przerywa build. Dotyczy ujęć z przodu, solo, trzech
postaci i klatek pośrednich. Ujęcie z boku zachowuje dotychczasowe kotwice.

Przy nasadzie każdej szarfy dodano ciągły uchwyt w dwóch środkowych kolumnach
i trzech wierszach PMG. Niweluje to różnicę między środkiem 3,5 a zaokrągleniem
na piksel 4 i zapobiega odsuwaniu końca szarfy od dłoni w niektórych fazach.
Kontroler szarf korzysta teraz z cienia PMBASE w RAM zamiast odczytu $D407.
Zmieniły się metadane i PMG; same bitmapy tancerek pozostały zachowane.

## Pamięć i bezpieczeństwo

Rezerwa helpera intro wynosi 1888 B. Typewriter: 194 B od $EB44 do $EC05,
scanline pool zaczyna się pod $EC20. Brak nowych banków rozszerzenia.
Status mieści się w nieużywanych znakach kontrolnych fontu $C800 (ASCII
wiersza, nie dane używanych glyphów). Prywatny DL $BC00 ma 575 B.

Router palety ma 74 B i kończy się na $249A. **$249C–$24A4 to żywe zmienne
playera i detekcji pamięci**, nie wolne miejsce po UI. Assert w generatorze
pilnuje tej granicy. Większy router z roboczej v229 został odrzucony po
próbie rzeczywistego startu emulatora; nie używać tego wydania do pokazu.

## Weryfikacja

Testy obejmują dłonie wszystkich bazowych i 18 dodatkowych klatek, uchwyt
we wszystkich 16 fazach każdej szarfy, dekodowanie danych, callbacki, NMI,
stały kadr i niezmienione cztery aktualizacje muzyki na ramkę.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 297 880 identycznych bajtów
względem v035, cały utwór. Brak próby na fizycznym Atari.

Podglądy rekonstrukcji CPU/ANTIC: `build/terminal-v230.gif`,
`build/terminal-v230-preview.png`, `build/ribbon-v230-grips.png`.

[ODCZYT] Pełny zestaw dla v230: **165/165 testów, bez pominięć**, 113,7 s.
