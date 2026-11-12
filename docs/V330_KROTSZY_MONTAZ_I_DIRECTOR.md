# V330 — krótszy montaż i natychmiastowe przejęcie przez director

V330 skraca demo do około 4:20.7. Montaż rotatorów i tuneli po Trevorze
kończy się wcześniej, a director przejmuje sterowanie już na pierwszym
callbacku po walce (tick 29656). Pierwsze cięcie kierunku/tempa następuje
muzycznie na takcie 80; dalej motyw, kierunek i prędkość zmieniają się co
takt. Przejęcie zachowuje bieżącą fazę bananów.

Outro zaczyna się na takcie 112 (tick 41884). Credits/greetz i ostatni kadr
zachowują czas ekspozycji: koniec tekstu i początek fade to tick 51232,
trwała czerń zaczyna się na ticku 51980. Oczy dziewczyny pozostają w
przedziale 39379–40126.

Wydanie: stereo release 058, `releases/less-i-know-demo-release-058-stereo.xex`.
SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`.

28 ukierunkowanych testów py65 obejmujących reżysera, rotatory, granice
montażu, timeline i credits zaliczyło v330. Pełnego `make check` po zmianie
nie uruchomiono. Nie wykonano fizycznej próby Atari ani nowego pełnego
porównania stereo POKEY dla v330.
