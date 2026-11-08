# V180 — dłuższe ujęcie tunelu

W akcie 5 bananowy rotator kończy się teraz w takcie 92 (tick 34404), a
spiralny tunel zaczyna się od razu po nim. Wcześniej tunel zaczynał się
dopiero w takcie 104 (tick 38892). Daje to ujęciu tunelu 20 taktów do
niezmienionego przejścia w kolejną kompozycję w takcie 112 (tick 41884),
zamiast dotychczasowych 8 taktów.

Zmiana tekstury tunelu pozostaje w takcie 108 (tick 40388): spirala przechodzi
w radialną siatkę gwiazd. Nie zmieniono granic aktu 5/6, dalszych ujęć, kodu
animacji, banków ani rytmu muzyki. Modyfikacja ogranicza się do progu
wyboru motywu w dispatcherze aktu 5.

- XEX: `build/visual-prototype-v180.xex`.
- 286 współdzielonych wierszy, 11 034 B danych wierszy i 2 552 B kodu.
- SHA-256: `5c2580f79e50d6d671f58d5ae16d9e44ceda959c345078faad9a5c9224613e65`.
- Build zakończył się powodzeniem. Testów ani emulatora nie uruchomiono.
