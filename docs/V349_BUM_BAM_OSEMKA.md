# v349 — płynniejsze BUM/BAM na ósemce

Po oczach cykl na bananach trwa 94 ticki: mały pusty dymek rozjaśnia się,
rozszerza do napisu BUM lub BAM, po 48 tickach cztery satelitki rozlatują się
na boki, dymek stopniowo maleje, a od 79 do 86 ticku całość gaśnie. Przez
ostatnie osiem ticków jest pusto. Ruch ósemki korzysta z zegara muzyki, nie
z klatki rotatora; tablice w bankach Trevora zajmują `$6900–$693F`.

Build stereo `build/visual-prototype-v349.xex` (1 115 783 B), SHA-256
`72294e6a35a018a0f6db6fcc549bc3a5e233f25c4ad9f80d580a3a8f0712671a`.
Generator: 298 współdzielonych wierszy i 2542 B kodu głównego. Sześć testów
directora i dziewięć testów efektów Trevora przeszło w py65. Sprawdzono etapy,
stopnie jasności, cztery satelitki, zapis wyłącznie do nieaktywnego PMG,
PORTB i zasięg toru. Nie uruchamiano emulatora ani fizycznego Atari. Artefakt
tablicy wsadu jest nadal nierozwiązany: [audyt](AUDYT_WSAD_PMG_V347.md).
