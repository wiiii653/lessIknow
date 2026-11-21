# V356 — korekta miksu POKEY w wydaniach 068 i 069

Punkt wyjścia to obraz i montaż v356. Wersja stereo 068 stroi oba basy
według lewego głosu, aby usunąć wprowadzone w v035 rozstrojenie. Zapisane
poziomy każdego układu są ograniczane do sumy 24 tylko podczas głośnych
nakładek, wobec maksimum 30 wcześniej. To dodatkowy zapas poziomu, nie
pomiar analogowego przesterowania.

Mono 069 zachowuje główny głos melodii przez całą jego aktywność i bierze
prawy głos w przerwach. Perkusja utrzymuje wybraną stronę podczas obwiedni.
Nowy, głośniejszy atak z drugiej strony może przejąć kanał. Oba poziomy
basu składają się w jeden głos z lewym strojem. Suma głośności na układzie
nie przekracza 24. Starsze mono 067 mogło zmieniać stronę przy samym
przecięciu poziomów, co powodowało skoki wysokości lub rodzaju szumu.

Generator `tools/build_audio_revision.py` odczytuje zamrożony prototyp v356.
Pakiety są kodowane w tym samym formacie i pakowane loaderem 058. Obie
wersje zachowują player, liczbę aktualizacji, układ 64 banków i dane grafiki.
Strumień zajmuje 116 582 B (stereo) albo 106 785 B (mono) w dotychczasowym
limicie 117 520 B. Zmieniają się dane muzyczne pierwszych ośmiu banków i
słownik `$2E00/$2E80/$2F00`. W mono zmieniają się też zapisy do POKEY w
kodzie `$2000–$24B2` i `$2C00–$2C80`. Oryginalne poziomy dla wskaźników
wizualnych mono pozostają w nieużywanych rejestrach bufora prawego głosu.

- `releases/less-i-know-demo-release-068-stereo.xex`, 945 968 B,
  SHA-256 `d35ce3ff150f57701e1638b81ecabff714adb1a52b674de900ea330858de3936`.
- `releases/less-i-know-demo-release-069-mono.xex`, 945 968 B,
  SHA-256 `1a3ace400b563d2001afd6fe6edd679d0b6f20f3f0d244da2292f101624a942d`.

Weryfikacja: Atari800 PAL, 1088 XE, Altirra OS. Wszystkie 59 833 zapisy
aktualizacji odpowiadają wyliczonemu miksowi. Stereo sprawdzono z dwoma
POKEY, mono z jednym oraz z dwoma, aby potwierdzić brak zapisów muzyki na
drugi układ. Utwór trwa 5:00, a na karcie końcowej cztery aktualizacje
zajmują dokładnie jedną ramkę PAL.

Próba sprzętowa użytkownika: brzmienie mono 069 jest w porządku na
fizycznym Atari z jednym POKEY. W tym zgłoszeniu nie podano modelu,
PAL/NTSC, konfiguracji pamięci ani zakresu odsłuchu. Użytkownik nie ma
maszyny stereo do sprawdzenia 068, więc dla tego wydania dostępny jest
wyłącznie wynik Atari800.
