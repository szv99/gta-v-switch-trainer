# NX Trainer framework 0.1

Framework do testowania trainera GTA V na Switchu przez debugger Atmosphere.
Menu i spawn Addera potwierdzil uzytkownik. Framework dodatkowo potwierdzil
spawn Sultana przez niezerowy uchwyt pojazdu i licznik utworzonych pojazdow.
Nie zmienia plikow GTA na karcie. Po zamknieciu gry trzeba ponownie uruchomic trainer.

## Uruchamianie

GTA musi byc w Story Mode, konsola w tej samej sieci Wi-Fi, a w Atmosphere
aktywny standalone GDB stub na porcie 22225. FTP nie jest potrzebne.

W PowerShell, w tym katalogu:

```powershell
C:\Python314\python.exe trainer.py discover
C:\Python314\python.exe trainer.py install
C:\Python314\python.exe trainer.py status
C:\Python314\python.exe trainer.py spawn sultan
C:\Python314\python.exe trainer.py heal
C:\Python314\python.exe trainer.py wanted-clear
C:\Python314\python.exe trainer.py repair
C:\Python314\python.exe trainer.py invincible on
C:\Python314\python.exe trainer.py invincible off
C:\Python314\python.exe trainer.py reload
C:\Python314\python.exe trainer.py stop
```

Domyslny adres: 192.168.0.122. Inny adres: `trainer.py --host ADRES install`.
Menu otwiera sie automatycznie. Krzyzak wybiera opcje/model, potwierdzenie
z GTA wykonuje akcje, anulowanie zamyka menu. Skrot ponownego otwarcia
wykorzystuje kontrolki GTA cover + pickup; fizyczne mapowanie L/R wymaga
potwierdzenia na ustawieniach konkretnego kontrolera.

Model mozna podac jako nazwe przez CLI. Gra sprawdza, czy jest dostepny
w faktycznie zainstalowanych assetach. W menu sa Adder, Sultan, Blista,
Zentorno, Buffalo, Baller, Bati, Sanchez i Bifta. Pozostale modele nie byly
jeszcze testowane. Brak modelu, timeout i blad tworzenia maja osobne statusy.

`Stop trainer` w menu sprzata efekty i usypia skrypt. `trainer.py stop`
dodatkowo przywraca oryginalny cheat_controller. Trainer tymczasowo zajmuje
ten skrypt, wiec jego fabryczna obsluga kodow nie dziala do przywrocenia.
Nie zostawiamy celowo wlaczonej niesmiertelnosci przy stop/reload. Utworzone
pojazdy sa oddane pod zarzadzanie gry; stop nie usuwa ich ani nie cofa leczenia.

## Budowa i aktualizacja

```powershell
C:\Python314\python.exe build.py
C:\Python314\python.exe -m unittest discover -s tests -v
C:\Python314\python.exe trainer.py reload
```

Kompilator SC-CL oraz mapowanie natywnych funkcji pozostaja w nadrzednym
trainer-dev. Brak PC_Natives.bin to oczekiwane ostrzezenie: build.py uruchamia
map2699.py, ktory wykonuje jawne mapowanie i walidacje instrukcji VM.

## Podzial odpowiedzialnosci

- `nxtrainer/transport.py`: protokol GDB, fragmentacja pakietow, sumy kontrolne,
  porcjowany odczyt/zapis, weryfikacja zapisu i odpinanie procesu w finally.
- `nxtrainer/runtime.py`: profil konkretnego buildu, wyszukanie procesu,
  skryptu i programu, kontrola pojemnosci, plan zmian, trwaly dziennik i rollback.
- `trainer.py`: polecenia, blokada przed rownoczesnymi zapisami, cykl
  install/status/stop/reload oraz oczekiwanie na potwierdzenie sprzatania.
- `script/trainer.c`: menu, logika pojazdow/postaci i skrzynka polecen z PC.
- `build/manifest.json`: SHA payloadu i zrodla, profil executable, rozmiary,
  wyliczony budzet stosu i rzeczywiste sloty zmiennych nadane przez kompilator.
- `state/`: kopie oryginalnej pamieci i dzienniki sesji. Nie usuwac aktywnego
  dziennika przed stop/recovery. Kopie zostaja po zakonczeniu sesji.

Mailbox ABI 1 zawiera numer polecenia, argument, numer sekwencji,
potwierdzenie, heartbeat, status pracy, wynik, uchwyt auta i licznik spawnow.
Adresy PID, modulu, programu, watku i stosu sa wykrywane ponownie przy
instalacji. Stale offsety nalezy traktowac jako profil tylko buildu
6E3E9B3AF5746E74B615BD981080C9271BC226620. Runtime porownuje fragmenty
kodu i kazda uzywana funkcje z lokalnym executable, nie zgaduje adresow.

## Odzyskiwanie i ograniczenia

`recover` sluzy tylko do dziennika przerwanego zapisu, po sprawdzeniu tej
samej sesji. Aktywny trainer wymaga `stop`, aby najpierw posprzatal efekty.
Gdy gra nie wykonuje petli i nie potwierdza cleanup, narzedzie nie wymusza
cofniecia pamieci. Zamkniecie gry usuwa zmiany RAM; po kolejnym starcie
`install` rozpoznaje nowy PID/baze i archiwizuje poprzednia sesje.

To framework developerski dla pojedynczego potwierdzonego buildu, nie
samodzielny plugin konsoli. Nie ma autostartu z karty, teleportacji, Online
ani ogolnego ladowania dowolnych skryptow. Testy smierci, zmiany bohatera,
wczytania zapisu i dlugiej sesji pozostaja do wykonania na konsoli.

## Kolejne etapy

1. Potwierdzic nawigacje nowego menu i cykl smierc/zmiana bohatera/zapis.
2. Dodac podzial spawnera na kategorie, opcjonalne wejscie do auta i bezpieczne
   usuwanie tylko pojazdu utworzonego przez trainer.
3. Rozdzielic kod menu i funkcji po ustabilizowaniu ABI; dodac wersjonowane
   rozszerzenia zamiast zaleznosci od kolejnosci slotow kompilatora.
4. Zbadac maly loader na konsoli, zachowujac mozliwosc przywrocenia oryginalu.
   Wsparcie takiego loadera w porcie nie jest jeszcze potwierdzone.
