# Menyoo na Switch: baza i granice pełnego portu

Stan sprawdzenia: 13 września 2026. Badanie publicznych repozytoriów; bez zmian na konsoli. Repo Menyoo sklonowane obok raportu wyłącznie do przeglądu, bez uruchamiania dołączonych binariów.

## Rekomendacja

**Menyoo jest najlepszą bazą dla zamierzonego zakresu: rozbudowany trainer, tuning, postacie, sceny i zapisy XML.** To ocena dopasowania do potrzeb, nie uniwersalny ranking. Warto portować jego funkcje i formaty danych do własnego runtime NX. Nie ma podstaw, żeby obiecać 100% zgodności z najnowszym Menyoo PC: brakuje nie tylko loadera, ale również części zasobów gry i usług Windows.

Docelowy projekt powinien rozdzielać: stabilny loader NX, adapter gry 2699/9b485eb8, przenośne moduły gameplay, UI na kontrolerze, pliki i diagnostykę. Obecny trainer VM pozostaje świetnym narzędziem do sprawdzania natives. Według lokalnego audytu przekazanego przez agenta głównego host cheat_controller ma około 15 830 bajtów kodu, 151 natives, 95 statics i 1551 bajtów stringów. Nie jest pojemnym hostem pełnego Menyoo.

## Fakty ze źródeł

| Kandydat | Potwierdzony stan i zależności | Ocena dla NX |
|---|---|---|
| Menyoo, itsjustcurtis | Utrzymywany fork wskazany przez autora oryginału. README wymaga Legacy **3095.0 lub nowszego**, albo Enhanced. Większość kodu GPLv3, fragmenty innych projektów z osobnymi oznaczeniami. | Główna baza funkcjonalna; trzeba osobno mapować 2699. |
| Menyoo, MAFINS | Repo archiwalne od 6 II 2025; odsyła do itsjustcurtis. Wydania historyczne dostępne. | Warto porównać starszą rewizję bez nowych zależności renderera; nie zakładać zgodności tylko na podstawie daty wydania. |
| Enhanced Native Trainer | Publiczny rozwijany kod; PC C++, repo oznaczone GPL-2.0. Automatyczne listy załadowanych pojazdów/broni, konfiguracja kontrolera. | Dobra referencja szczegółowych opcji, nie eliminuje potrzeby adaptera NX. Nie mieszać kodu z Menyoo bez sprawdzenia dokładnych deklaracji licencji konkretnych plików. |
| NativeUI | MIT, C#, ScriptHookVDotNet; archiwalne od 30 I 2024, projekt poleca LemonUI. | Biblioteka UI, nie kompletne menu. Wprowadzanie środowiska .NET nie jest skrótem do portu C++/NX. |

Źródła: [Menyoo README](https://github.com/itsjustcurtis/MenyooSP), [oryginalny MAFINS](https://github.com/MAFINS/MenyooSP/blob/master/README.md), [ENT](https://github.com/FIying-Scotsman/GTAV-EnhancedNativeTrainer), [licencja ENT](https://github.com/FIying-Scotsman/GTAV-EnhancedNativeTrainer/blob/master/LICENSE.md), [NativeUI](https://github.com/Guad/NativeUI).

Przejrzany commit Menyoo: `c82d2321f4f4439d80f6d1c8c20abbe1f7b64e4d`, data 2026-09-10. Build definiuje C++20, x64, bibliotekę `.asi` oraz linkowanie ScriptHookV, d3d11, d3dcompiler, dxgi i Psapi. Obejmuje ImGui/ImGuizmo, backend Win32/DX11 oraz MinHook. To nie jest gotowy moduł ARM64. [Konfiguracja kompilacji](https://github.com/itsjustcurtis/MenyooSP/blob/c82d2321f4f4439d80f6d1c8c20abbe1f7b64e4d/premake5.lua).

`main.cpp` używa DllMain, Windows API, rejestruje dwa wątki ScriptHook i obsługę klawiatury. `Memory/GTAmemory.cpp` ma skanery i poprawki pamięci. Wszystkie te mechanizmy wymagają zastąpienia, a nie zmiany rozszerzenia pliku. [Punkt startu](https://github.com/itsjustcurtis/MenyooSP/blob/c82d2321f4f4439d80f6d1c8c20abbe1f7b64e4d/Solution/source/main.cpp), [integracja z pamięcią](https://github.com/itsjustcurtis/MenyooSP/blob/c82d2321f4f4439d80f6d1c8c20abbe1f7b64e4d/Solution/source/Memory/GTAmemory.cpp).

## Zakres portowania

| Moduł | Realna droga | Główna niewiadoma |
|---|---|---|
| Pojazdy, tuning, broń, postać | Przenoszenie logiki opartej o natives etapami; każdy model walidowany i ładowany z limitem czasu. | Różnice sygnatur natives i modele usunięte z zestawu 64 GB. |
| Teleport, pogoda, czas | Natives i zadania rozłożone na klatki; kontrola kolizji/podłoża. | Nieobecne DLC/interiory, zachowanie przy zmianie bohatera. |
| Modele pedów, ubrania, animacje, ochroniarze | Adapter encji + menedżer zasobów i sprzątania. | Nie wszystkie kombinacje są poprawne dla każdego modelu; RAM i streaming. |
| Spooner/sceny | Zachować model encji, transformacji, attachmentów i task sequences; budować UI kontrolera. | Pojemność sceny i stabilność całych sekwencji na NX. |
| Presety Menyoo XML | Zacząć od pojazdów, potem outfitów, następnie Spooner; raportować nieobsługiwane pola. | File I/O z procesu gry i zgodność wszystkich pól. |
| Nowy ImGui Spooner / renderowane podglądy | Osobny backend NX albo alternatywny interfejs oparty o natives. | Integracja renderera; DX11 nie istnieje jako kompatybilny interfejs w obecnym NX runtime. |

Źródła funkcji: katalog [Submenus](https://github.com/itsjustcurtis/MenyooSP/tree/c82d2321f4f4439d80f6d1c8c20abbe1f7b64e4d/Solution/source/Submenus), [Spooner FileManagement.cpp](https://github.com/itsjustcurtis/MenyooSP/blob/c82d2321f4f4439d80f6d1c8c20abbe1f7b64e4d/Solution/source/Submenus/Spooner/FileManagement.cpp), [VehicleSpawner.cpp](https://github.com/itsjustcurtis/MenyooSP/blob/c82d2321f4f4439d80f6d1c8c20abbe1f7b64e4d/Solution/source/Submenus/VehicleSpawner.cpp). XML obejmuje właściwości pedów i aut, attachmenty i task sequences; kod używa pugixml oraz odczytu/zapisu plików. Import samego XML nie dostarcza brakujących modeli ani assetów.

## Proponowana architektura i warunki zaliczenia

1. `platform_nx`: odrębny loader/autostart, alokacja pamięci, log, pliki SD; wyłączenie awaryjne. Istniejący SaltyNX może być kandydatem, ale załadowanie jego core nie dowodzi jeszcze możliwości uruchomienia naszego runtime.
2. `game_2699`: jeden adapter natives, scheduler na właściwym wątku gry, kontrola BuildID, uchwyty encji, wykrywanie dostępnych modeli. Brakujące funkcje wyłączone z widocznym powodem.
3. `core`: stabilne identyfikatory poleceń i ustawień, cykl enable/tick/disable, limity czasu i budżet pracy na klatkę. Reload zatrzymuje zadania i sprząta stan przed wymianą modułu.
4. `features`: vehicles, player, weapons, teleport/world, peds, spooner. Moduły korzystają wyłącznie z adapterów.
5. `storage`: wersjonowane ustawienia i importer Menyoo XML z wynikami per pole. Najpierw test import/eksport jednego auta bez utraty obsługiwanych właściwości.
6. Macierz zgodności: każda opcja ma status działa / częściowo / brak assetów / wymaga portu. Testy obejmują śmierć, zmianę bohatera, wczytanie zapisu, przeładowanie modułu, wielokrotny spawn/usuwanie i dłuższą sesję.

**100%** należy zdefiniować względem konkretnego commitu Menyoo i konkretnej listy funkcji. 100% najnowszych modeli i wszystkich rozszerzeń PC jest nieosiągalne samym portem menu do obecnych assetów2699/64 GB. Cel sensowny technicznie: maksymalna zgodność funkcji SP dostępnych w tym buildzie oraz formatów presetów, z jawną listą odstępstw.

Nie zweryfikowano: natywnego runtime ARM64, autostartu naszego menu, trwałego zapisu SD z procesu GTA, pełnego importu XML ani kompletnej zgodności jakiejkolwiek historycznej wersji Menyoo z portem NX. Ten raport nie oznacza wdrożenia tych elementów. Menyoo nie dostarcza backendu ani klienta GTA Online; to osobna ścieżka badań.
