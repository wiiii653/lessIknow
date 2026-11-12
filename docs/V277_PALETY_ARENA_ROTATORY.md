# V277 — mocniejsze rotatory i nowa paleta przed areną

Odcienie rotatorów zachowują kolejność i rytm zmian. Jaśniejsza faza
pulsu jest ciemniejsza niż wcześniej, a drugi kolor ma kontrolowany zapas
jasności: pary pozostają rozróżnialne. Daje to silniejsze wrażenie koloru
na PAL, którego nasycenie nie jest osobnym parametrem rejestru GTIA.
Żółte banany zachowują paletę v275.

Ujęcia spotkania przed areną i reakcji chłopca (sceny 8–12) używają teraz
ciepłego `$38`, niebieskiego `$88` i jasnego `$2C`. Ustawienie jest w
istniejącym bankowanym helperze; przed kodem gwizdania pozostaje sprawdzana
granica `$6900`. Pozostałe sceny otrzymują wcześniejszą paletę.

Build stereo `releases/less-i-know-demo-release-015-stereo.xex` korzysta z
kompaktowego loadera AVG i późnego startu; innych wersji dźwięku nie budowano.
Nie oceniono jeszcze nowej palety ani tego builda na fizycznym Atari.

[ODCZYT] Atari800 PAL/1088XE: 16 234 920 identycznych bajtów stereo POKEY
w porównaniu z v035; obejmuje cały utwór. Testy ukierunkowane: 50/50;
pełny zestaw: 200/200 w 144,522 s.
