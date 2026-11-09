# V218 — nieruchomy chłopiec i terminal

Od pierwszego ujęcia outro chłopiec pozostaje w tej samej niższej pozycji.
Po 59085 pięć wierszy tekstu dostaje puste rekordy; nie przywracamy wyższego
kadru. Ten sam układ 235 linii i przesunięcie PMG +32 linie obowiązują do
końcowego fade. Pełna postać jest zachowana, bez skalowania. Górne poziome
linie bitmapy (wiersze źródłowe 5 i 9) usunięto, pozostawiając czarne pole.

Tekst: zielony fosfor (hue $C0, luminance $0E), ciemne tło, bitmapowy font
5×7 i znaki zachęty `>`. Skrócono nagłówki do SONG / POKEY / MIDI, zachowując
nazwy i autorów. Falowanie tekstu pozostaje. Terminal znika wraz z fade;
brak powrotu postaci w górę. Reset zwykłych DL działa wyłącznie przy wyjściu
z outro do wcześniejszej sceny, np. podczas przewijania wstecz.

Ticki 53850 / 56842 / 59085 / 59833 i cztery przerwania muzyczne pozostają
bez zmian. Nie zajęto nowych banków. Szczegóły bazowej architektury i
weryfikacji v216: `V216_CREDITS_GREETZ.md`. Podgląd CPU/ANTIC:
`build/outro-v218-preview.png` (rekonstrukcja z przybliżoną paletą PAL).

Pierwszy kadr z chłopcem nie jest publikowany w starym, wyższym układzie.
Publikacja następuje dopiero po przygotowaniu prywatnego DL przy `$BC00`.
Spakowane dane: 1752 B; loader: 362 B.

[ODCZYT] 40 testów scen, PMG, granic, budżetów i regresji zakończonych
powodzeniem; po dodaniu sprawdzenia pierwszej publikacji osobno przeszły
wszystkie 4 testy outro. Wcześniejszy pełny przebieg v217 miał jedną starą
asercję oczekującą `$8400` po końcu napisów; dostosowano ją do stałego
`$BC00` i ponowny test przeszedł w zestawie 40 testów.
Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 106 144 identyczne bajty
względem v035, cały utwór. Weryfikacja nie obejmuje fizycznego Atari.
