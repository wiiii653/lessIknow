# V094 — kombinacje ciosów Trevora

W części od taktu 72 do taktu 88 Trevor wykonuje kombinacje zsynchronizowane
z tickiem odtwarzacza. Pierwsze pięć ciosów to prawa, lewa, lewa, prawa,
lewa. Dwutaktowy motyw miesza ciosy na miarę i na pół miary, dzięki czemu
odstępy wynoszą 46–47 albo 93–94 ticki. Zamach pokazuje rękę następnego ciosu,
włącznie z następującymi po sobie ciosami tą samą ręką. Pierwszy zamach zaczyna
się 32 ticki przed wejściem w serię. Granice aktów są zachowane.

BANG zajmuje pierwsze 16 ticków ciosu, a cząstki kolejne 16. Punkt początkowy
cząstek jest wspólny z pozycją BANG. Faza tunelu jest odświeżana co 32 ticki,
ale zmiana pozy wymusza odświeżenie niezależnie od fazy. Tablica 96 ciosów i
procedura mieszczą się w istniejących bankach Trevora.

[ODCZYT] 69 testów py65 zakończyło się poprawnie, w tym testy rytmu, sekwencji
rąk, zamachu przed uderzeniem, początku i kierunku cząstek oraz PORTB.
[ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: po jednokrotnym wyrównaniu
początku zapis rejestrów POKEY był identyczny z v035 dla 5 968 512 bajtów;
porównanie obejmuje cały utwór. [ODCZYT] W izolowanym teście py65 przebudowa
klatki ciosu kosztuje około 56 tys. cykli. [WNIOSEK] Płynność i czytelność
najszybszych kombinacji wymagają oceny w emulatorze z obrazem lub na Atari;
porównanie POKEY nie zastępuje odsłuchu.

`build/visual-prototype-v094-knockout.gif` jest programowym podglądem z
przybliżonymi kolorami i tempem, nie nagraniem emulatora. XEX:
`build/visual-prototype-v094.xex`, SHA-256
`76faf0e3fd03749d6046856344339376a2c4a2e216e5369d4aaef8e05e110f72`.
