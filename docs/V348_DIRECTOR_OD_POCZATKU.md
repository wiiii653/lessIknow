# v348 — director od pierwszych rotatorów

Director zmienia tempo i kierunek w pierwszych rotatorach (ticki 11967–14958), w tunelu przed wsadem (20942–21689) i w montażu po Trevorze (29656–41883). Cięcia scen fabularnych pozostają bez zmian. Oczy są w tickach 39379–40126; BUM/BAM z bocznymi dymkami jest aktywne tylko na bananach po tym ujęciu. Banany trwają do ticku 41135, po czym wracają tunele.

Build stereo `build/visual-prototype-v348.xex`: SHA-256 `1a30a191f06580a8662dc16bb9d4be682b3f9820db3de505983fd5c7da9c2f65`. Generator: 298 współdzielonych wierszy, 2542 B kodu. Pięć testów directora i dwa testy przejścia przez tunel/wsad przeszły w py65. Osobno sprawdzono na dwóch taktach BUM, BAM i wszystkie cztery bufory dymków, wyłączenie nakładki w oczach oraz zachowanie PORTB. Bez sprawdzenia w emulatorze lub na fizycznym Atari. Nie naprawiono zgłoszonych wcześniej artefaktów tablicy wsadu; patrz [audyt](AUDYT_WSAD_PMG_V347.md).
