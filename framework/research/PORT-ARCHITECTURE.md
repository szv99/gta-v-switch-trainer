# Kierunek portu rozbudowanego menu — 13 wrzesnia 2026

## Co naprawde dziala

Framework 0.1 w pamieci GTA: instalacja, tekst i menu, sterowanie z PC,
spawnowanie, raportowanie uchwytu utworzonego pojazdu, sprzatanie efektow,
przywrocenie skryptu oraz reload. Uzytkownik potwierdzil Addera; test PC
potwierdzil Sultana. Pozniejszy odczyt wykazal 9 udanych spawnow w tej sesji.
Nie jest to port Menyoo ani loader uruchamiany z karty.

Aktualny payload: 1656 bajtow kodu, 37 natywnych funkcji, 18 zmiennych
statycznych. Obecny host cheat_controller ma okolo 15.8 KB kodu, 1551 bajtow
tekstow, 151 wpisow native i 95 slotow statycznych. Testowany budzet stosu
wynosi 256 slotow, z czego konserwatywny rachunek payloadu wykorzystuje 176.
Te limity oznaczaja, ze obecny sposob podmiany nie jest baza do wsadzenia
calego duzego menu C++ do jednego skryptu. Jest dobrym srodowiskiem do
sprawdzania zgodnosci funkcji i zachowania gry.

## Proponowany podzial

1. **Loader ARM64 tylko dla tego tytulu i profilu buildu.** Automatyczny start,
   kontrola zgodnosci, log uruchomienia, wylaczenie moda bez zmiany assetow gry.
2. **Adapter do gry.** Mapowanie hash -> native, kontekst wywolania natywnych
   funkcji, wykonywanie w prawidlowym watku/skrypcie, kolejkowanie i WAIT.
   Nie wywolywac dowolnych natives z nowego watku bez potwierdzonego kontekstu.
3. **Warstwa platformy.** Kontroler, pliki SD, czas, ustawienia, logowanie,
   odpowiedniki wymaganych mechanizmow Windows. Oddzielna od funkcji menu.
4. **Port logiki menu z ustalonej rewizji publicznego zrodla.** Pojazdy,
   postac, swiat, Spooner i zapis obiektow przenoszone kategoriami; wspolny
   rejestr funkcji i status zgodnosci zamiast obiecywania 100% z gory.
5. **Dane i presety.** Zachowac format oryginalnego menu, gdy wykonalne.
   Pokazywac brak modeli/animacji zamiast powodowac crash przez nieobecne DLC.
6. **Narzedzia PC.** Dotychczasowy GDB, kopie, telemetry i testy pozostaja
   srodowiskiem developerskim nawet po dodaniu samodzielnego loadera.

## Kandydaci loadera, nie potwierdzone rozwiazania dla GTA

W snapshotach procesu GTA znajduje sie saltysd_core.elf, wiec kod SaltyNX
juz jest w tym procesie. Nie dowodzi to zgodnosci nowego pluginu ani miejsca
na duzy modul. Projekt SaltyNX sam poleca exlaunch do modow konkretnej gry:
https://github.com/masagrator/SaltyNX/blob/master/README.md

Exlaunch opisuje sie jako framework do wstrzykiwania kodu C/C++ na Switchu:
https://github.com/shadowninja108/exlaunch

Skyline to kolejny kandydat. Jego README wyraznie wskazuje potrzebe
dopasowania inicjalizacji/NPDM do niektorych gier:
https://github.com/skyline-dev/skyline

Pierwszy test loadera powinien wykonac tylko log + heartbeat, potem jedna
zweryfikowana funkcje na wlasciwym watku. Dopiero po wielokrotnym poprawnym
starcie, stopie i wyjsciu z GTA warto przenosic duzy interfejs.

## Co oznacza cel 100%

Nalezy wskazac dokladny commit/release menu i spis jego funkcji. Kazda
funkcja dostaje status: dziala / wymaga adaptacji / brak assetow / niedostepna
w porcie / nieprzetestowana. Pelna zgodnosc najnowszego wydania z GTA2699
nie wynika z mozliwosci spawnowania auta. Ograniczenia platformy i brakujace
DLC moga uniemozliwic parytet z najnowszym PC. Zachowane optional-dlc-backup
pozwala rozpatrywac przywracanie danych, ale nie tworzy nowych funkcji silnika.

## Online jako osobny tor

Nie laczyc menu online z pracami nad backendem i nie zakladac, ze UI odblokuje
sieciowy stan klienta. Odczyt online-runtime.json: signed_in=true,
signed_online=false, network_game_in_progress=false, session_active=false.
Reason7 to wniosek z kodu i odczytanych flag, nie wynik wywolania native.
Pierwszy kamien milowy: rzeczywiste zadanie tego klienta do kontrolowanego
backendu i zaakceptowana odpowiedz. Potem sesja solo; synchronizacja dwoch
klientow jest odrebnym testem. Pelne GTA Online wymaga dalszych uslug i danych.
