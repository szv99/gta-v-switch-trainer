# Online na Switchu: badanie wykonalności

Stan sprawdzenia: 2026-09-13. GTA V Legacy 2699, port 9b485eb8. Badanie kodu publicznego backendu i istniejących lokalnych wyników; bez zmian w konsoli, bez uruchamiania serwera i bez korzystania z wycieku źródeł Rockstar.

**Rekomendacja: najpierw dowód jednego prawdziwego żądania klienta i poprawnego przejścia stanu usług, potem własna sesja solo, dopiero potem dwa identyczne klienty Switch.** Nie ma podstaw obiecywać zgodności z publicznymi sesjami PS4/Xbox 360.

## Co wiadomo

Oficjalna strona LSO deklaruje Xbox 360 i PS4. Repozytorium opisuje się jako backend PS4; zawiera Node.js, Prisma/PostgreSQL, API kont i matchmakingu. Licencja package.json to AGPL-3.0-only. Publiczna strona organizacji wskazuje aktualizację 11 lipca 2026. Nie znaleziono publicznej macierzy dokładnych wspieranych wersji gry ani potwierdzenia Switcha. [Strona LSO](https://lossantosonline.com/), [repozytorium](https://github.com/Los-Santos-Online/Los-Santos-Online), [organizacja](https://github.com/Los-Santos-Online).

Są endpointy nazwane dla PC, PS3, PS4/PS5 i XBL. Obecność endpointu nie jest dowodem gotowego klienta na każdą platformę. Publiczne wyszukiwania exact build 9b485eb8, NSGTA i źródeł portu nie ujawniły zweryfikowanego repozytorium źródłowego tego portu. Nie oznacza to, że źródła nie istnieją; nie mamy ich do analizy ani budowania.

Lokalny odczyt runtime przekazany przez głównego agenta: signin guard = 0, signin flags = 2, game-in-progress = 0; obecne wątki sieciowe. Z wcześniej rozpoznanych handlerów wynika signed-in = true (bit o indeksie 1, maska 2), signed-online = false (bit o indeksie 2, maska 4). Nie mylić surowych flag z własnym polem netBits trainera. Nie wykonywałem tego pomiaru ponownie. Import nn::socket i istniejące wątki nie dowodzą kompletnej implementacji usług.

## Konkretne przeszkody w LSO

1. **Matchmaking:** find.js wymaga biletu, filtruje dokładnie platformę i niepusty gameVersion. Pusta wersja pomija filtr, lecz nie naprawia protokołu. Backend przekazuje sesyjne Data; zgodność nagłówków nie oznacza zgodności tego bloba ani synchronizacji. [find.js](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/src/endpoints/matchmaking/find.js).
2. **Transport i identyfikacja platformy:** middleware odczytuje platformName z nagłówka ROS i uruchamia dekoder. GTAEncryption.js nie zawiera pozycji SWITCH, a fallback odwołuje się do nieistniejącej pozycji PC. Dla wejścia SWITCH konstruktor próbuje Buffer.from(undefined), więc sama normalizacja tekstu w matchmakingu nie zapewnia nawet przejścia transportu. Port może nadal deklarować PCROS — trzeba to zmierzyć, nie zgadywać. [middleware.js](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/src/utils/rc4Encryption/middleware.js), [GTAEncryption.js](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/src/utils/rc4Encryption/GTAEncryption.js).
3. **Tożsamość:** PS4 CreateTicketNp4 sprawdza authCode przez BlueSphere i zwraca 401 bez poprawnej weryfikacji. currentGameVersion pochodzi z odpowiedzi BlueSphere. Backend umożliwia konfigurację adresu weryfikatora; to nie dostarcza adaptera kont Switch ani nie tworzy zgodnego klienta. PC CreateTicketSc3 ma odrębną ścieżkę konta email/hasło. Dla prywatnego prototypu potrzebny będzie jawny adapter własnych kont testowych, dobrany do rzeczywistej ścieżki klienta. [PS4 auth](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/src/endpoints/auth/PS4/createTicketNp4.js), [PC auth](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/src/endpoints/auth/PC/createTicketSC3.js).
4. **Zaufanie:** dokumentacja opisuje pinning całego certyfikatu TLS, lokalne wydawanie certyfikatów P2P i osobną parę kluczy relay. Trzeba ustalić faktyczną ścieżkę zaufania klienta Switch oraz dodać własny certyfikat testowy do właściwej konfiguracji klienta. HTTP 200 nie sprawdza akceptacji certyfikatu i sesji przez grę. [certificates.md](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/docs/certificates.md).
5. **Relay nie jest dostarczony jako działająca usługa w tym Compose.** README i getting-started sugerują start UDP relay, ale compose.yaml publikuje tylko HTTP/HTTPS, kod reklamuje i podpisuje zewnętrzny adres, a configuration.md wyraźnie potwierdza zewnętrzny relay. Nie znaleziono implementacji listenera UDP w tym repozytorium. To rozbieżność dokumentacji, nie gotowa infrastruktura przekazywania pakietów. [configuration.md](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/docs/configuration.md), [compose.yaml](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/compose.yaml), [GetRelayServers](https://github.com/Los-Santos-Online/Los-Santos-Online/blob/main/src/endpoints/geoLocation/getRelayServers.js).

## Pierwszy mały test

Przygotować osobną funkcję diagnostyczną trainera: zapis Build ID, czasu, signed-in, signed-online, CAN_ACCESS_MULTIPLAYER wraz z kodem powodu, game-in-progress i session-active. Odczyty są lepszym pierwszym krokiem niż wymuszenie bitu online. Nie ma jeszcze dowodu, że kod powodu 7 jest aktualnym wynikiem wywołania całej funkcji — wcześniejszy warunek może zwrócić inny kod.

Następnie w jednej kontrolowanej próbie wejścia do Online zanotować przez debugger:

- czy wywołuje się inicjalizacja usług, DNS/connect i klient HTTP;
- domenę/docelowy adres, metodę i ścieżkę, platformName i wersję ROS;
- wynik transportu, błąd TLS lub odpowiedź parsera, moment zmiany stanu;
- jeśli nie ma żądania: konkretny warunek lub stub, który zatrzymał inicjalizację.

Log nie powinien przechowywać haseł, biletów ani prywatnych kluczy. Sukces etapu: realne żądanie GTA zidentyfikowane i odpowiedź lokalnej usługi zaakceptowana przez właściwy parser. Sam test curl lub syntetyczne wywołanie find.js nie spełnia kryterium. Tego testu w ramach niniejszego badania jeszcze nie wykonano.

Aktualizacja pomiaru 15:38:49: główny agent zapisał `online-runtime.json` obok raportu. Potwierdzono guard=0, signinFlags=2, accessGate=0, signed-in=true, signed-online=false, game-in-progress=false i session-active=false. Dla wejścia w0=2 analiza gałęzi przy takim stanie przewiduje powód 7; native kontroli dostępu nie został wywołany. To aktualizuje niepewność wcześniejszego warunku opisaną powyżej, nie zastępuje rzeczywistego wywołania i nie dowodzi komunikacji z backendem.

## Kolejne bramki decyzji

| Etap | Wymagany dowód | Co nadal nie jest udowodnione |
| --- | --- | --- |
| Lokalny backend | Stan bazy, odpowiedzi API, własne testowe certyfikaty i konto | Klient Switch |
| Klient usług | Prawdziwe żądanie i zaakceptowany bilet, poprawny stan online | Sesja gry |
| Solo Online | Uruchomiony freemode, własny host sesji, postać, stabilny zapis/odczyt i powrót do SP | Multiplayer |
| Dwa Switche w LAN | Widoczne ruchy obu graczy, to samo auto i jego zajętość, utworzenie/usunięcie obiektów, poprawne rozłączenie | Internet, migracja hosta, crossplay |
| Internet | NAT/P2P lub zgodny relay, dołączenie ponowne, utrata pakietów i host migration | Zgodność z innymi platformami |

Solo Online wymaga usług i skryptów trybu Online, nawet bez innych graczy. Samo włączenie skryptu freemode albo zmiana flagi nie wystarcza. Zgodność 2699 na poziomie assetów nie gwarantuje wersji protokołu: port ARM64, patche i odmienne struktury mogą ją zmienić. To wnioski inżynierskie, nie potwierdzone usterki tego portu.

Alternatywą jest własny ograniczony co-op przez moduł klienta: początkowo zdalny gracz jako lokalny ped i synchronizacja pozycji przez własny protokół. To odrębny produkt, z własnym transportem, identyfikatorami, własnością encji i serializacją; nie GTA Online ani kompatybilny klient LSO. Warto rozważyć dopiero po ustaleniu, że oryginalna ścieżka sieciowa jest niekompletna.

## Artefakty do zachowania

Dokładny NSO Build ID i hash, raport flag runtime, lista osiągniętych funkcji sieciowych, zanonimizowana para request/response, profil platformy/protokołu, macierz endpointów potrzebnych do startu, logi sesji i manifest dostępnych DLC. Opcjonalne paczki odłożone z wariantu 64 GiB mogą być potrzebne konkretnym aktywnościom; przywracać według dowodów brakujących zależności, nie całość w ciemno. Dla dwóch klientów wymagane identyczne buildy i konfiguracja. Przed dystrybucją pochodnej LSO zachować licencję i spełnić wymagania udostępnienia odpowiednich źródeł wynikające z AGPL.

Najbliższa praca: diagnostyka klienta usług i jeden kontrolowany request. Uruchomienie całego LSO przed poznaniem tej ścieżki nie rozstrzygnie wykonalności i dołoży niezależne problemy konfiguracji.
