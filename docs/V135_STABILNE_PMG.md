# V135 — stabilne PMG piłki i satelitów

[ODCZYT] Usunięto gaszenie PMG i wyłączanie DMA w rendererze mozaiki/tunelu.
Poprzednia piłka pozostaje widoczna również podczas oczekiwania na nowe
okno aktualizacji. Helper piłki dopuszcza rozpoczęcie zapisu wyłącznie
przy VCOUNT 124–127 (linie 248–255 PAL). Spóźnione wywołanie czeka do
kolejnego okna, zachowując dotychczasowe PMG. Nie zmieniono granic scen,
ticków muzyki ani masek piłki/gwiazdek.

[ODCZYT] Nowy test `tests/test_tunnel_raster.py` używa przesuwającego się
VCOUNT i sprawdza 4 fazy × 11 pozycji początkowych rastra × 2 warianty
opóźnienia. Dodatkowy wariant zatrzymuje CPU na 3500 cykli po pierwszym
zapisie PMG. Wszystkie zapisy pamięci i rejestrów kończą się przed linią 48
następnej ramki, PMG/DMA nie są gaszone. Test wykrywa błąd na archiwalnym
v134 i przechodzi na v135. To model cykli instrukcji z syntetycznym
opóźnieniem, nie pełna emulacja ANTIC ani pomiar sprzętowy.

[ODCZYT] Atari800 PAL/1088XE: 14 967 504 identyczne bajty stereo POKEY
względem v035; cały utwór. Podgląd gotowego rastra callbacku:
`build/v135-pmg-preview.png` (przybliżone kolory PAL). Nie jest nagraniem
przebiegu rastra w emulatorze.

XEX: `build/visual-prototype-v135.xex`, identyczny z buildem roboczym.
SHA-256: `a797a26fc7cae52da34e7e5df5ab2c81494002d362219f2a9dcb05a527f15f65`.

[ODCZYT] Pełny `make check`: 87 testów, 84 zaliczone, 3 pominięte
z powodu braku archiwalnego v126; 77,469 s.
