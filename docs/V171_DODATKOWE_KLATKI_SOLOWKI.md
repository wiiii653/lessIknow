# V171 — dodatkowe klatki solówki

> **Wydanie v171 jest wadliwe i nie należy go odtwarzać.** Strumienie
> skompresowanych klatek trafiły do banków obrazu bez dekodera. Poprawka v172
> przenosi je do banków 32–35, które zawierają dekoder.

## Zmiana animacji

Do centralnego ujęcia solówki dodałem cztery nowe fazy ruchu: przy zmianie
pozy 6→7, 7→8, 8→9 i 9→8. Wypadają przy 3/4 przejścia, około 34–35 ticków
po poprzednim akcencie. Dotychczasowa klatka pośrednia pozostaje w połowie
przejścia, a nowe klatki skracają jego końcowe odstępy do około 11–12 ticków.
Nie zmieniłem długości sceny, akcentów muzycznych, bocznego ujęcia, grupowego
tańca ani wyrzutu dziewczyny.

## Grafika i pamięć

Nowe pozy pochodzą z arkusza 3×3, z którego używane są cztery kadry. Każda
została skomponowana w oryginalnej skali solówki, sprowadzona do natywnej
bitmapy 160×64 i dopasowana do kotwic dłoni. Dane są szybkim LZ i zostały
sprawdzone przez lokalne odtworzenie strumieni przed złożeniem banków.

- Źródło: `assets/art/source/act2_ribbon_inbetweens_v171.png`.
- Opis generowania: `assets/art/source/act2_ribbon_inbetweens_v171.prompt.txt`.
- W pierwotnym v171 cztery klatki zajmowały 3805 B w ogonach banków 8–11 od
  `$7C00`. Ta lokalizacja nie zawierała dekodera i powodowała błąd odtwarzania.
- Selektor rośnie z 1015 do 1370 B, używa `$4040–$4599`; pierwszy strumień
  nadal zaczyna się pod `$4600`.
- Główny kod i niebankowany runtime zachowują swoje rozmiary. Poprawiony
  routing banków opisuje [V172](V172_POPRAWKA_DEKODERA_TANCA.md).

Wszystkie pozostałe klatki i ich kotwice wracają do poprzedniego wyboru przy
kolejnym akcencie. Banki tańca są wczytywane bez zmiany ich rozmiaru, a dane
nowych klatek zajmują wcześniej wolne ogony.

## Zakres walidacji

Pierwsze wydanie XEX zbudowało się, ale sam build nie sprawdził obecności
dekodera w wybranym banku. Problem odtwarzania naprawiono w v172.
