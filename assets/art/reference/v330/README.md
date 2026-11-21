# Dziewczyna z wersji party

[Kadry wzorcowe z Atari800](opening.png) pochodzą z archiwalnego
wydania 058 / v330. Górny rząd pokazuje trzy pozycje z bocznej panoramy.
Dolny rząd pokazuje zbliżenie od tyłu i dwa ujęcia drogi do wejścia.
Te sześć kadrów jest identycznych w wydaniu 061 / v352.

Wzorzec XEX to [stereo 058](../../../../releases/less-i-know-demo-release-058-stereo.xex).
Jego SHA-256 to `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`.

- Tył postaci pochodzi z [act1_north_girl.png](../../source/act1_north_girl.png).
  `school_story.party_girl()` zwraca oryginalną grafikę 48 × 64 z maską
  i znakiem Fuji. Pozycje i skala pochodzą z `GIRL_PLACEMENTS`.
- Chód pochodzi z [arena-pan.bin](../v175/arena-pan.bin).
  `school_parallax.party_frames()` zwraca komplet 18 klatek z trzema
  poprawkami profilu, które były już w wersji party.

Kolejne poprawki otwarcia powinny wychodzić z tych klatek. Od v362
`school_story.foreground_girl()` pobiera zbliżenie z tego samego rysunku
bezpośrednio na siatkę sceny. Retusz bocznej panoramy jest zapisany
osobno w `PROFILE_POLISH`. Testy sprawdzają sumy oryginałów v330.
