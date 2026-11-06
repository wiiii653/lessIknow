# V110 — ruch ręki i poprawny bufor kozłowania

Naprawiono adres bazowy bufora używany w display liście po aktualizacji
fragmentu postaci. Wcześniej kopia mogła trafiać do jednego bufora, podczas
gdy display lista nadal wskazywała drugi. Testy izolowanych klatek nie
wykrywały tego błędu; nowa regresja wykonuje dwa pełne cykle na tym samym CPU
i porównuje rzeczywiście wyświetlany obraz.

Chłopiec ma cztery rysowane fazy ramienia: kontakt z piłką, pchnięcie,
puszczenie i powrót. Ruch jest przypisany do fazy tej samej piłki PMG;
przed kolejnym odbiciem dłoń wraca do pozy kontaktowej. Stare ramię usunięto
ze wspólnej grafiki. Sylwetka i sala są stałe, a aktualizowana część ma
44×28 pikseli i zajmuje 308 bajtów. Trzy dodatkowe fragmenty oraz jedna
pełna baza kozłowania zajmują łącznie mniej pamięci niż dwie dawne pełne
klatki. Pozostałe cztery klatki wsadu nie zostały zmienione.

[ODCZYT] 75 testów zakończyło się poprawnie, w tym test dwóch pełnych odbić,
czterech widocznych pozycji ramienia, stałego tła i zakresu zapisów do
pamięci. [ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: po jednokrotnym
wyrównaniu początku 5 925 960 bajtów POKEY było identycznych z v035;
porównanie obejmuje cały utwór.

Podgląd `build/visual-prototype-v110-kozlowanie.gif` powstał z kolejnych
wykonań na tych samych buforach py65. Kolory i tempo są przybliżone;
nie jest to nagranie emulatora. XEX: `build/visual-prototype-v110.xex`;
SHA-256 `dcd09eca4bb190edcbd42d0dc89899e5c7716e0ac8c390fdb02b3a42e5a55310`.
