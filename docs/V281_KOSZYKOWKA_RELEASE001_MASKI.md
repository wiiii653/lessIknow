# V281 — koszykówka z release 001 i poprawione maski

[ODCZYT] `less-i-know-demo-release-001.xex` to v254. Bajty koszykarza w
jego banku 15 odpowiadają zachowanemu `assets/art/reference/v175/basketball.bin`.
Zestaw pięciu pełnych klatek, trzy łaty kozłowania, cztery pozy ręki, fazy
wsadu, trajektorie piłki i trzy łaty rozbicia tablicy wróciły do tego źródła.
Wcześniejsza podmiana na sześć póz v177 została wycofana.

`tools/hero_mask_cleanup.py` usuwa fragmenty fioletowego tła z otoczenia ud,
przestrzeni między nogami i okolic nóg. Małe, jawnie wyznaczone obszary
ujemnej maski zastępują tylko piksele starego różu odpowiednimi pikselami
czystej hali; kontury, skóra i turkusowy strój nie są przemalowywane.
Korekta obejmuje również łaty ruchomej ręki, aby nie przywracały tła.

Build stereo `releases/less-i-know-demo-release-018-stereo.xex` używa
kompaktowego loadera AVG i późnego startu. Układ banku i rozmiar grafiki
koszykarza pozostają jak w release 001; dodatkowe pełne klatki v177 i ich
helper nie są już instalowane.

[ODCZYT] Porównanie z release 001 sprawdza oryginalne dane, niezmienione
łaty rozbicia tablicy, kluczowe fazy, pozy, parametry piłki oraz ograniczenie
zmian pikseli do jawnych masek. Podgląd klatek po korekcie został obejrzany.
Porównanie kozłowania co 8 ticków zachowuje numery póz, fazy i pozycję
piłki z release 001.
[ODCZYT] Pełny zestaw: 200/200 testów, 146,239 s; dodatkowe porównanie
kozłowania z release 001 także zaliczone. Atari800 PAL/1088XE: 16 097 040
identycznych bajtów stereo POKEY względem v035, cały utwór.

[OGRANICZENIE] Nie sprawdzono jeszcze tego buildu na fizycznym Atari.
Emulacja i testy CPU nie potwierdzają rzeczywistej płynności ani odsłuchu.
