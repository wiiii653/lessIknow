# Audyt artefaktów wsadu — v347

Grafika i kod banku wsadu w v347 są identyczne z v330. W porównaniu 94 faz py65 renderował te same piksele i PMG. Nie rozstrzyga to zachowania ANTIC na fizycznym Atari.

Ustalono potencjalną przyczynę sprzętową: `basketball_hero.helper` czyści i uzupełnia aktywny PMG po oczekiwaniu na `$D40B >= 124`. W py65 dla faz 60, 75 i 82 od pierwszego do ostatniego zapisu PMG upływa odpowiednio 4959, 4898 i 4870 cykli CPU (około 43 linie po 114 cykli); dotyczy to zakresu `$0980–$0BFF`. Nie można wykluczyć, że aktualizacja zachodzi podczas wyświetlania górnej części obrazu. py65 nie modeluje DMA ANTIC, a pomiar nie jest dowodem przyczyny artefaktu.

Bezpieczna poprawka wymaga przygotowania nieaktywnego PMG i pozycji/kolorów, następnie publikacji w ograniczonym oknie wygaszania. W banku wsadu pozostało 52 B przed danymi `$4B80` oraz 192 B pod `$7F40–$7FFF`; przed modyfikacją należy uwzględnić własność tych obszarów, NMI, sprite'y obu buforów i czas publikacji. Nie dokonano zmian kodu ani nie zbudowano nowego XEX.
