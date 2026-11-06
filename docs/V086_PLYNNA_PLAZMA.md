# V086 — pełnoekranowa plazma tytułowa

W otwarciu GTIA 11 plazma wypełnia cały obraz; litery są częścią tego samego
obrazu i różnią się od otoczenia odcieniem. Ruch uzyskano z 16 klatek
nakładających się fal radialnych. Kolejne wiersze napisów są nakładane przez
maskę zmieniającą odcień, bez czarnych paneli. Maski przestrzenne wygaszają
efekt nierównomiernie, a jasność dochodzi do zera przed granicami plansz.
Granice i ticki nie uległy zmianie.

Klatki mają rozdzielczość 80×64; ANTIC pokazuje każdy wiersz trzykrotnie.
Kod pod ROM-em systemowym łączy fazę i maskę w nieaktywnym buforze; kod i dane
plazmy zajmują siedem dodatkowych banków rozszerzenia. Łącznie używane jest
61 banków konfiguracji 1 MB. Muzyczne NMI przywraca PORTB; program po złożeniu
klatki przywraca poprzedni bank. Bufory tańca są oznaczane jako wymagające
ponownego wczytania.

[ODCZYT] 64 testy wykonane z py65 zakończyły się poprawnie, w tym porównanie
wynikowych pikseli z fazami, maskami liter i zaniku oraz test powrotu do intra.
[ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: po jednokrotnym wyrównaniu
początku zapis rejestrów POKEY był identyczny z oryginałem dla 5 837 112 bajtów;
porównanie obejmuje cały utwór. [ODCZYT] W izolowanym teście py65 przebudowa
fazy trwa około 53–130 tys. cykli 6502; fazy zmieniają się co 32 ticki, ale
koszt może powodować pomijanie faz na docelowym sprzęcie.
[WNIOSEK] Wyniki POKEY nie zastępują odsłuchu ani oceny płynności na Atari.

`build/visual-prototype-v086-preview.gif` jest podglądem display listy i ma
przybliżone kolory; nie jest nagraniem emulatora. XEX ma SHA-256
`af2080e95c3daa7459b6df17a92266850b223dcd7f0896679d269406ac24f7a0`.
