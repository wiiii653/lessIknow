# v044 — dopracowanie Trevora

Stary Trevor był powiększaną sylwetką PMG na siatce 16×24. Zastąpiono ją
czterema bardziej szczegółowymi komiksowymi kadrami 160×64: wejściem przez
drzwi, bliższym ujęciem w sali oraz dwiema pozami w neonowej sali. W pierwszej
części postać zbliża się w dwóch cięciach, a obraz stopniowo się rozjaśnia.
Po muzycznym uderzeniu dwie ilustracje zmieniają się co 256 ticków; cztery
pociski PMG tworzą poruszające się kolorowe iskry. Zamiast poprzedniego
sprzętowego zoomu zastosowano dwa ilustrowane zbliżenia i zmianę póz.

Granice są bez zmian: 23936 początek, 26928 uderzenie, 32912 kolejna scena.
Kadry bitmapowe przechowuje nowy bank 39, wykrywany tym samym sprawdzaniem
aliasów; jego selektor znajduje się pod `$08D8`. Muzyka i otaczające sceny
zachowują banki. Wcześniejszy bank Trevora pozostaje używany przez efekt piłki
w tunelu i rotatorze. Każde zbliżenie jest kopiowane do nieaktywnego bufora;
przy nieruchomym kadrze odświeżane są tylko iskry i kolory.

Źródło: `assets/art/source/act4_trevor_polished_v043.png`. Wygenerowano przy
użyciu imagegen z oryginalną kartą Trevora jako odniesieniem.

Prompt: "Production contact sheet for an Atari 8-bit demo, exact 2 columns x
2 rows of equal wide landscape panels without gutters. Based on reference, same
character Trevor: muscular gorilla with violet fur, pink chest, pale expressive
face, natural proportions, confident expression. European bande dessinée /
1980s European comic, not anime, no manga or giant eyes. Flat graphic, bold
black shapes and contours, restricted palette EXACTLY black, dark violet
#740090, hot pink #ff32a0, pale pink #ffbece. Designed to remain readable when
each panel is reduced to 160 x 64 pixels: large features, no tiny lines, broad
separations. Top left: Trevor waist-up emerging through the dark doors at far
end of a school gym, centered and ominous, gym wall bars and floor visible,
no other people. Top right: same Trevor closer, from waist up, strong chest and
arms, face readable, dark gym setting. Bottom left: Trevor in dramatic upper-body
front three-quarter pose, one fist forward, energised neon gym, converging
geometric architectural beams behind him. Bottom right: same character in
alternate strong pose with raised fist, dramatic head-and-torso closeup and
stylized neon gym beams. Same recognizable face and body across panels. Crisp
large silhouette, no text, no numbers, no watermark, no decorative frames."

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 53 testy PASS,
w tym wszystkie kadry, granice aktu, ruch iskier i powrót pozostałych efektów.
Atari800 PAL 1088XE: 18 zrzutów obejmujących scenę, jej granice oraz restart;
aktywna bitmapa zgodna z kadrami źródłowymi, dane pocisków obecne.

[ODCZYT] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v044.xex --seconds 12`: 7 539 984 identycznych bajtów
stereo POKEY (~2100,3 s emulacji, cały utwór). Bez osobnego odsłuchu na
fizycznym Atari. `build/v044-trevor.gif` pokazuje podgląd z przybliżeniem barw PAL.

SHA256 XEX: `ab0f017d68e57e69186865c4e51c96a4c794b0e29dc0c66bb1e6f149bf18dea6`.
Poprzednie XEX-y zachowane.
