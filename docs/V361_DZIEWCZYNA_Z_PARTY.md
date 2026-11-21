# V361 — dziewczyna z wersji party

Punktem wyjścia jest oryginał z v330 / 058. Wszystkie 18 klatek panoramy
i cztery ujęcia przy arenie odtworzono piksel w piksel przed retuszem.
W zbliżeniu od tyłu dodano 36 pikseli pasm włosów. W panoramie skorygowano
cztery piksele profilu na klatkę przy uchu i podbródku. Sylwetka, kurtka
ze znakiem Fuji, pozy, tło i wszystkie trzy dalsze ujęcia pochodzą z party.

[Oryginalne kadry i źródła](../assets/art/reference/v330/README.md) ·
[Porównanie z Atari800](../build/v361-party-opening-comparison.png)

## Wydania AVG

Oba pliki mają po 945 929 B i przechodzą przez loader sprzętowy wydań
opartych na 058. Prototyp v361 zajmuje 64 banki i używa 298 wspólnych
wierszy (11 527 B). Kod główny ma 2 542 B.

- [079 mono, jeden POKEY](../releases/less-i-know-demo-release-079-mono.xex)
  · SHA-256 `69c4a9a7a4ef114bec788527d8a406003834052d46548af417ea909b99e4911d`
- [078 stereo](../releases/less-i-know-demo-release-078-stereo.xex)
  · SHA-256 `d947ca8088af51ab5f6589eb712233a92386ba300757d8fe0057b798ea17d270`

## Weryfikacja

Przeszło 21 testów grafiki, przejść scen, loadera i directora po Trevorze.
Sprawdzono odtworzenie 64 banków i końcowy bootstrap. Atari800 PAL,
emulowane 1088 XE i Altirra OS pokazały takie samo otwarcie w obu
wydaniach. Kadry wykonane później są zgodne z odpowiednio 076 i 077.

W każdym wydaniu porównano 59 833 aktualizacje rejestrów POKEY z poprzednim
miksem. Dane były identyczne, a cztery aktualizacje dalej przypadają na
każdą ramkę PAL na planszy końcowej. Nowe pliki sprawdzono w emulatorze.
Próba na fizycznym Atari i pełne `make check` pozostają niewykonane.
