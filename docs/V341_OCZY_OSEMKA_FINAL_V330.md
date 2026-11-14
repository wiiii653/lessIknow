# V341 — piłka w ujęciu oczu i końcówka v330

W ujęciu oczu klatki 60–63 nadal pokazują oczy dziewczyny, a piłka z czterema
satelitami dostaje własną fazę z zegara muzyki. Dzięki temu obiega 64-punktową
ósemkę przez całe ujęcie; pozostałe tunele zachowują swój dotychczasowy ruch.

Przywrócono granice końcówki v330: terminal startuje w ticku 41884, jego tekst
kończy się w 51232, fade zaczyna się w 51852, a karta `A\\SLOP BY OGNJEN 2026`
/ `SILLY VENTURE WE` wchodzi w ticku 51980. Bieżące creditsy, greety i tekst
terminala pozostają. W kodzie nie ma osobnego rampowania tempa playera; wróciła
ta sama część utworu i te same znaczniki czasu co w v330.

Zbudowano `build/visual-prototype-v341.xex` jako stereo: 298 współdzielonych
wierszy, 2560 B kodu głównego, 1 111 781 B XEX. SHA-256:
`9def0b8ed69eb2b35e0115ca45749c71d6634d8138e87d48706f06b0a208b004`.
Generator i kontrole alokacji przeszły. Nie uruchamiano testów, emulatora ani
próby na Atari; v330 pozostaje ostatnią wersją potwierdzoną sprzętowo.
