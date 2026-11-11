# V260 — rotatory bez ostatnich przebitek Trevora

[ODCZYT] Na polecenie użytkownika wycofano cztery komiksowe przebitki v257:
powtarzane/zastąpione zbliżenie Trevora, panele trzech postaci, konfrontację
i duży portret Trevora. W ich miejscu ponownie działa ruchomy montaż
bananów/tuneli jak w v256. Sekwencja oczu dziewczyny, wcześniejsza walka
Trevora z piłkami, terminal, finałowy chłopiec, muzyka i ticki pozostają.
Dawne pliki generatora/testów zachowano w `docs/archive/` poza buildem.

[ODCZYT] XEX v260 różni się od v256 wyłącznie 17 bajtami podpisu ładowania
`AI-SLOP/OGNJEN`; pozostałe segmenty są identyczne. W tym przywrócone są
cztery fazy tunelu wyparte przez v257. Kolejne cztery nadal zawierają oczy
v252. Nie ma dodatkowych banków. 16 testów ukierunkowanych zaliczonych;
testy CPU nie dowodzą realnego FPS ani zachowania ANTIC DMA na sprzęcie.

[ODCZYT] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 199/199
przypadków, bez pominięć; 152,233 s. Atari800 PAL/1088XE, Altirra OS,
stereo POKEY: 16 272 720 identycznych bajtów z v035 przez cały utwór.
