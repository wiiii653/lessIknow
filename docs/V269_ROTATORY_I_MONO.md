# V269 — dłuższe cofki i jeden POKEY

Montaż po Trevorze używa dłuższych, zasadniczo dwutaktowych przebiegów,
z zachowaniem fazy przy zmianie kierunku. Organiczny tunel ma 12 faz;
sloty oczu pozostają oddzielne. Granice scen i muzyki pozostają bez zmian.

Wersja mono wyłącza zapisy do drugiego POKEY w oryginalnym playerze;
zachowuje cztery głosy pierwszego układu. Nie jest to redukcja ośmiu
głosów do czterech. `tools/make_mono.py` sprawdza adresy przed podmianą.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS: 15 431 472 identycznych bajtów
stereo względem v035. Porównanie mono z wariantem stereo: 840 776 próbek
pierwszego POKEY bez różnic, drugi zestaw rejestrów zerowy.
[ODCZYT] Pełny zestaw: 200 testów zaliczonych.

[OGRANICZENIE] Brak próby na fizycznym Atari. Zgłoszony problem startu na
1 MB nie został zdiagnozowany ani usunięty. Loader zatrzymuje się, gdy nie
potrafi znaleźć banku; potrzebne są szczegóły rozszerzenia i loadera.
