<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**Menedżer sterowania TAILSCALE ze zintegrowaną zaporą dla FUNNEL**

OMEGA-TAIL to narzędzie z pakietu OMEGA, które steruje **Tailscale** na maszynie i **chroni** ją, gdy
publikuje usługę w Internecie przez **Tailscale Funnel**.

> Stworzony przez [kraynux](https://github.com/kraynux) dla [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Strona oficjalna](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/pl/) · [Zrzuty ekranu](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Interfejs, dokumentacja, eksporty i strony dla odwiedzających dostępne w **17 językach** — zobacz [Języki interfejsu](#języki-interfejsu).  
**Języki:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** to aplikacja TUI (Terminal User Interface) w Pythonie, zbudowana z
[Textual](https://textual.textualize.io/). Pozwala zarządzać **Tailscale** i dostrajać go w trybie zaawansowanym z
poziomu interfejsu, bez zapamiętywania choćby jednego polecenia. Dodaje też zabezpieczenia (zapora, ograniczenie
zasobów, przetrwanie…) dla trybu **Funnel**, który otwiera usługę maszyny na cały Internet.

Każda akcja zmieniająca maszynę najpierw pokazuje swoje polecenie. Hasło sudo wpisuje się w terminalu, akcja po
akcji, i nic nie jest uruchamiane w tle bez twojej wiedzy.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pl/omega-tail/F.png" width="32%" />
</p>

Projekt jest zbudowany zgodnie z zasadami **Clean Architecture**, z `app/` jako korzeniem kompozycji: domena
biznesowa, orkiestracja, infrastruktura i interfejs są od siebie oddzielone.

## Spis treści

- [Prezentacja](#prezentacja)
- [Zrozumieć Tailscale i Funnel](#zrozumieć-tailscale-i-funnel)
- [Funkcje](#funkcje)
- [Zabezpieczenia w szczegółach](#zabezpieczenia-w-szczegółach)
- [Pomiary](#pomiary)
- [Architektura](#architektura)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Użytkowanie](#użytkowanie)
- [Motywy i terminale](#motywy-i-terminale)
- [Pliki, usługi i zgodność](#pliki-usługi-i-zgodność)
- [Bezpieczeństwo](#bezpieczeństwo)
- [Testy i jakość](#testy-i-jakość)
- [Stan projektu](#stan-projektu)
- [Odinstalowanie](#odinstalowanie)
- [Licencja](#licencja)

---

## Prezentacja

### Dlaczego omega-tail

Tailscale Funnel publikuje usługę maszyny w Internecie bez otwierania portu na routerze: odwiedzający przechodzą
przez przekaźniki Tailscale. Od strony sieci jest to proste i bezpieczne, ale pozostaje jedna słabość.

- **Koszt szyfrowania.** W domyślnym trybie Funnel to usługa `tailscaled` na maszynie wykonuje uzgadnianie TLS
  (handshake) każdego odwiedzającego. Zmierzone na małej maszynie: to około **80 % kosztu połączenia**. Kilkaset
  nowych połączeń na sekundę wystarczy, by wysycić procesor: jeden zwykły komputer z prostym skryptem może położyć
  stronę i maszynę.
- **Niewidoczni odwiedzający.** Zwykłe zapory (nftables, ufw, fail2ban) nie widzą tych odwiedzających: docierają
  zaszyfrowani, tunelem Tailscale, z adresem przekaźnika.
- **Rozproszone ustawienia.** Ustawień Tailscale (operator, węzeł wyjściowy, trasy, SSH, osłona…) jest wiele, są
  rozdzielone między polecenia a konsolę WWW, a niektóre mogą zerwać bieżącą sesję.

### Cele

- Sterować Tailscale w całości z poziomu interfejsu, z jednozdaniowym wyjaśnieniem każdego ustawienia.
- Odrzucać nadużywające połączenia **przed** jakimkolwiek szyfrowaniem, widząc rzeczywisty adres każdego
  odwiedzającego.
- Utrzymać maszynę na nogach podczas ataku: administracja i inne usługi pozostają osiągalne.
- Niczego nie narzucać: proponować, pokazywać polecenie, pytać i móc się wycofać.
- Działać na każdej dystrybucji Linuksa, pod systemd, OpenRC lub runit.

### Co robi omega-tail

- Wyświetla stan Tailscale, maszyny i tego, co jest opublikowane, z alertami prowadzącymi do ekranu, który
  pozwala to poprawić.
- Uruchamia, zatrzymuje i restartuje `tailscaled`, z zabezpieczeniem, jeśli twoja sesja przechodzi przez Tailscale.
- Zarządza połączeniem, kontami i wszystkimi ustawieniami `tailscale set`, sprawdzanymi przed zastosowaniem.
- Publikuje, wycofuje, wstrzymuje i testuje usługi Serve i Funnel, z kopiami zapasowymi i przywracaniem.
- Pokazuje urządzenia tailnetu, ich ścieżkę (bezpośrednią lub przez przekaźnik), diagnostykę sieci i logi.
- Umieszcza **bramę** HAProxy między Funnel a twoją stroną: reguły na adres, na prefiks, budżet globalny, listy
  zaufanych i czarną listę, grupowanie według odcisku JA4, sieci pochodzenia (AS) i kraju, automatyczny tryb ataku.
- Ogranicza zasoby `tailscaled`, odcina Funnel na chwilę lub całkowicie i potrafi zrobić to sam dzięki
  automatycznemu nadzorowi.
- Chroni port WireGuard usługi `tailscaled` tabelą nftables (osłona).
- Tworzy raport o maszynie i atakach z ostatnich 7 dni, w formacie TXT, HTML lub JSON.

### Czego projekt nie robi

- Nie zastępuje Tailscale: steruje nim.
- Nie chroni przed atakiem wolumetrycznym, który wysyca samo łącze internetowe (router, łącze).
- Nie obsługuje webowej konsoli administracyjnej Tailscale (polityka dostępu, zatwierdzanie węzłów wyjściowych,
  włączanie Funnel dla tailnetu).
- Nie chroni usługi opublikowanej inaczej niż przez Funnel: dla takich portów jest omega-fire.
- Nigdy nie działa jako root i nie uruchamia niczego w tle bez twojej zgody.
- Nie działa ani pod Windows, ani pod macOS.

[↑ Spis treści](#spis-treści)

---

## Zrozumieć Tailscale i Funnel

omega-tail zakłada znajomość kilku pojęć Tailscale. Ta część je zbiera, nie zakładając niczego więcej.

### Słownictwo

| Termin | Co to jest |
|---|---|
| **Tailnet** | Twoja prywatna sieć Tailscale: wszystkie maszyny połączone z tym samym kontem (lub tą samą organizacją). Każda maszyna otrzymuje w niej adres `100.x.y.z` (zakres 100.64.0.0/10) i adres IPv6 w `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | Usługa (demon) działająca na maszynie: utrzymuje szyfrowany tunel WireGuard, stos sieciowy Tailscale oraz, dla Serve i Funnel, przekazywanie ruchu do twoich usług. |
| **`tailscale`** | Polecenie sterujące `tailscaled` (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail używa go za ciebie. |
| **WireGuard** | Protokół szyfrowanego tunelu używany między maszynami. `tailscaled` nasłuchuje w tym celu na porcie UDP (domyślnie 41641), często otwieranym przez router (UPnP). |
| **Przekaźnik DERP** (DERP relay) | Serwery Tailscale, które przekazują ruch, gdy dwie maszyny nie mogą połączyć się bezpośrednio (trudny NAT). Ścieżka „bezpośrednia” jest szybsza. |
| **MagicDNS** | Nazwy maszyn tailnetu w postaci `machine.nom-du-tailnet.ts.net`. |
| **Serve** | Publikowanie lokalnej usługi (strony, API…) **tylko dla tailnetu**, przez HTTPS z ważnym certyfikatem `*.ts.net`. |
| **Funnel** | Publikowanie lokalnej usługi **dla całego Internetu**, pod adresem `https://machine.nom-du-tailnet.ts.net`. Można otworzyć tylko porty 443, 8443 i 10000. |
| **Przekaźnik Funnel** (Funnel relay) | Serwery Tailscale, które przyjmują odwiedzających z Internetu i wprowadzają ich do twojego tailnetu (widoczne jako „funnel-ingress-node”). |
| **Operator** | Konto Linuksa uprawnione do zmiany ustawień Tailscale bez sudo (`tailscale set --operator=…`). omega-tail proponuje to raz, przez sudo. |
| **Węzeł wyjściowy** (exit node) | Maszyna tailnetu, przez którą inna maszyna przepuszcza cały swój ruch internetowy (jak VPN). Musi zostać zatwierdzona w konsoli Tailscale. |
| **Rozgłaszana podsieć** (subnet router) | Sieć lokalna (na przykład `192.168.1.0/24`), którą maszyna udostępnia reszcie tailnetu. |
| **Osłona** (shields up) | Ustawienie Tailscale, które odrzuca wszystkie połączenia przychodzące z tailnetu. |
| **SSH Tailscale** | Serwer SSH dostarczany przez Tailscale, dopuszczany przez politykę tailnetu. |
| **Nagłówek PROXY v2** | Krótki nagłówek dodawany na początku połączenia, by przekazać rzeczywisty adres odwiedzającego temu, kto je odbiera. |
| **Odcisk JA4** (JA4 fingerprint) | Sygnatura sposobu, w jaki program otwiera połączenie TLS: przeglądarka i narzędzie do ataku mają różne. |
| **AS (system autonomiczny)** | Sieć pochodzenia adresu: dostawca internetu, hosting, chmura. |

### Droga odwiedzającego

**Domyślny Funnel, bez omega-tail.** `tailscaled` robi wszystko: odszyfrowuje tunel WireGuard, wykonuje
uzgadnianie TLS odwiedzającego, po czym przekazuje żądanie przez HTTP do twojej strony. Żadna zapora maszyny nie
widzi odwiedzającego, a każde nowe połączenie drogo kosztuje `tailscaled`.

```text
Odwiedzający ──HTTPS──▶ Przekaźnik Funnel ──WireGuard──▶ tailscaled (TLS + przekazywanie HTTP) ──HTTP──▶ twoja strona
                        (Tailscale)                      └── tu jest cały koszt
```

**Funnel z bramą omega-tail.** Funnel przechodzi w tryb TCP: `tailscaled` nie wykonuje już TLS, tylko przekazuje
wciąż zaszyfrowany strumień do bramy, poprzedzony rzeczywistym adresem odwiedzającego (nagłówek PROXY v2). Brama
decyduje **przed** jakimkolwiek szyfrowaniem: odrzucone połączenie nie kosztuje prawie nic, a odszyfrowywane są
tylko wpuszczone połączenia, przez OpenSSL, szybszy niż TLS w `tailscaled`.

```text
Odwiedzający ──HTTPS──▶ Przekaźnik Funnel ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                              │
                                                              ▼
                                               Brama omega-tail (HAProxy, 127.0.0.1)
                                               ├── odmowa przed TLS: czarna lista, częstotliwość, budżet, docelowa nazwa, grupowanie
                                               └── wpuszczone: TLS (certyfikat *.ts.net) ──HTTP──▶ twoja strona
```

Brama nasłuchuje tylko na lokalnej pętli zwrotnej maszyny i działa na twoim koncie. Maszyny twojego tailnetu są
zawsze wpuszczane, przed jakąkolwiek regułą: filtrowani są tylko odwiedzający z Funnel.

### Co musi umożliwiać Tailscale (konsola administracyjna)

Te ustawienia wykonuje się raz, w konsoli WWW Tailscale; omega-tail ich nie zmienia.

- **MagicDNS** i **certyfikaty HTTPS** włączone dla tailnetu (potrzebne do Serve, Funnel i certyfikatu bramy).
- **Funnel dozwolony** dla maszyny w polityce dostępu tailnetu (atrybut `funnel`).
- Dla węzła wyjściowego lub rozgłaszanych podsieci: ich **zatwierdzenie** w konsoli.

[↑ Spis treści](#spis-treści)

---

## Funkcje

Menu główne ma dwie kolumny po sześć pozycji: **TAILSCALE** do sterowania, **OCHRONA** do obrony.

### TAILSCALE

#### 1. Pulpit

- **Tailscale**: usługa, stan połączenia, wersja działająca i zainstalowana, nazwa maszyny, adresy, konto,
  urządzenia online, wygaśnięcie klucza, operator, węzeł wyjściowy oferowany i używany, rozgłaszane podsieci.
- **Maszyna**: CPU całej maszyny, obciążenie na rdzeń, temperatura, pamięć, CPU i pamięć `tailscaled`, ograniczenie
  zasobów, a następnie stan zabezpieczeń (Funnel, zapora i tryb ataku, czarna lista, nadzór, osłona).
- **Publikacja**: każdy opublikowany port, dla Internetu (Funnel) lub dla tailnetu (Serve), jego tryb i cel.
- **Alerty**, od najpoważniejszego do najmniej poważnego, z przyciskiem „Popraw”, który otwiera odpowiedni ekran.
  Na przykład: zatrzymana usługa, aktualizacja zainstalowana, ale niezastosowana, wygasający klucz, Funnel
  opublikowany bez ochrony, wysoka temperatura, zbyt zachłanny lub nieograniczony `tailscaled`, rosnąca czarna
  lista.
- Wartości na zielono, pomarańczowo lub czerwono według progów (CPU, obciążenie, temperatura, pamięć, `tailscaled`).

#### 2. Usługa tailscaled

- Stan widziany przez system init, wersja działająca i zainstalowana, polecenie uruchomienia, pliki nakładek
  (drop-in), ograniczenie zasobów.
- **Uruchom**, **Zatrzymaj**, **Uruchom ponownie** (na przykład, by zastosować już zainstalowaną aktualizację).
- **Zabezpieczenie**: jeśli twoja sesja przechodzi przez Tailscale (SSH przez tailnet), Zatrzymaj prosi o drugie
  potwierdzenie, bo nie mógłbyś już ponownie uruchomić usługi.
- **Popraw uruchamianie**: wykrywa plik nakładki, który uruchamia `tailscale up` przy starcie i grozi wyrzuceniem
  maszyny z tailnetu przy pierwszej zmianie ustawień; poprawka jest pokazywana, a oryginał zachowywany.

#### 3. Połączenie i ustawienia

- **Zaloguj się**, **Wyloguj się**, **Dodaj konto**, **Zmień konto**, **Trwałe wylogowanie** (trzeba wpisać nazwę
  maszyny).
- **Wszystkie ustawienia `tailscale set`**, każde z jednozdaniowym wyjaśnieniem: nazwa i przydomek maszyny, trasy,
  DNS tailnetu, osłona, filtrowanie stanowe, tryb netfilter, węzeł wyjściowy, dostęp do sieci lokalnej, oferowanie
  maszyny jako węzła wyjściowego, rozgłaszane podsieci, SSH Tailscale, interfejs WWW, aktualizacje, przekaźnik
  równorzędny (peer relay), operator.
- Podczas wpisywania ramka pokazuje **przed → po** i polecenie; po zastosowaniu każda ponownie odczytana wartość
  jest oznaczana ✔ (uwzględniona) lub ✖ (nie).
- Ostrzeżenie informuje, gdy zmiana może zerwać sesję przechodzącą przez Tailscale.
- **Przekazywanie IP**: włączane jednym przyciskiem, gdy maszyna służy jako węzeł wyjściowy lub rozgłasza podsieci.

#### 4. Publikacja

- Wszystko, co maszyna publikuje: port, publicznie (Funnel) lub w tailnecie (Serve), tryb, ścieżka, cel, ochrona.
- **Opublikuj** lokalną usługę przez HTTPS, HTTP, TCP lub terminowany TLS; **Wycofaj**; **Wstrzymaj Funnel** i
  **Przywróć Funnel** (w identycznej postaci).
- **Test end-to-end**: prawdziwe połączenie, jak od odwiedzającego (odpowiedź, czas, certyfikat, wersja TLS).
- **Kopie zapasowe**: stan sprzed każdej zmiany (50 najnowszych), możliwy do przywrócenia.
- Każda zmiana jest sprawdzana; w razie rozbieżności publikacja jest odbudowywana, a jeśli to się nie uda,
  przywracany jest stan poprzedni.

#### 5. Sieć i urządzenia

- **Urządzenia** tailnetu: system, online lub nie, ścieżka (bezpośrednia lub przez przekaźnik), ostatnio widziane,
  adres, wymieniony ruch; przekaźniki Funnel Tailscale są domyślnie ukryte.
- **Ping Tailscale** (ścieżka i opóźnienie), **Kto to?** (do kogo należy adres tailnetu).
- **Diagnostyka sieci**: UDP, IPv4 / IPv6, typ NAT, otwieranie portów przez router (UPnP, NAT-PMP, PCP), najbliższy
  przekaźnik i opóźnienia.
- **DNS**, **blokada tailnetu** (tailnet lock) i **wewnętrzne liczniki** Tailscale.
- Tylko do odczytu: nic na tym ekranie nie zmienia ustawień.

#### 6. Logi

- Log `tailscaled` (journalctl lub pliki usługi poza systemd) i log bramy, z filtrowaniem i eksportem.
- Każda informacja ma swój kolor, wzięty z motywu: data, proces, kategoria komunikatu (sterowanie, sieć, DNS, silnik
  WireGuard), adresy pogrubione, błędy na czerwono, ostrzeżenia na pomarańczowo; dla bramy powód odmowy, grupowanie,
  AS i kraj.

### OCHRONA

#### 7. Zapora Funnel

- **Zainstaluj HAProxy** menedżerem pakietów dystrybucji (pacman, apt, dnf, zypper, apk, xbps, emerge).
- **Włącz ochronę**: certyfikat `*.ts.net`, listy, sprawdzona konfiguracja, usługa bramy, przełączenie Funnel, a
  następnie test z Internetu; w razie niepowodzenia pierwotna publikacja jest natychmiast przywracana.
- **Wyłącz ochronę**: Funnel zostaje przywrócony dokładnie do stanu sprzed, ze sprawdzeniem.
- **Reguły** stosowane na gorąco, tryb **obserwacji**, by bez ryzyka dostroić progi, **grupowanie** (zobacz
  [Zabezpieczenia w szczegółach](#zabezpieczenia-w-szczegółach)).
- **Aktualizuj bazę** AS / krajów (DB-IP Lite), w osobnym procesie.

#### 8. Przetrwanie

- **Ograniczenie zasobów `tailscaled`**: limit CPU, waga i priorytet, opcja pierwszeństwa dla dostępu SSH.
- **Bezpiecznik Funnel**: progi CPU i temperatury, odcięcie na 10 minut (automatyczne przywrócenie) lub całkowite.
- **Automatyczny nadzór**: to samo, gdy nikogo nie ma przed ekranem.
- **Osłona portu WireGuard**: przycisk prowadzący do jej ekranu (obserwacja, aktywna, załóż, załóż ponownie, zdejmij,
  przekaż).

#### 9. Ataki i decyzje

- Liczniki bramy (odebrane, odrzucone przed szyfrowaniem, wpuszczone, w toku) i najaktywniejsze adresy, odczytywane
  co 2 sekundy, z krajem, AS i stanem każdego adresu.
- **Zablokuj**, **Czarna lista**, **Odblokuj**, **Zaufaj**: stosowane od razu, bez restartu bramy; powiadomienie
  w jednym wierszu podaje akcję i miejsce adresu.
- Widoki **Odciski**, **AS** i **Kraje**; stan trybu ataku i połączenia odrzucone przez grupowanie.
- **Zarządzanie czarną listą**: pełna lista z datą dodania i pochodzeniem, dodawanie, usuwanie, import pliku TXT
  (duplikaty, sieci już objęte i adresy tailnetu są pomijane), czyszczenie z podglądem (według wieku, N
  najstarszych, zakres wierszy, pochodzenie, wszystko), eksport TXT (do ponownego importu), HTML i JSON.
  Limit 50 000 wpisów.

#### 10. Raport

- Wszystko, co omega-tail wie o maszynie, w postaci faktów: Tailscale, publikacja, maszyna, zapora, przetrwanie,
  alerty oraz **ataki z ostatnich 7 dni** odczytane z logu bramy.
- **Prywatność**: domyślnie bez konta Tailscale ani nazw i adresów urządzeń tailnetu, aby można go było komuś
  wysłać.
- Eksport **TXT**, **HTML** (motyw do wyboru) i **JSON**; **Pokaż eksporty** otwiera katalog w przeglądarce.

#### 11. Ustawienia

- Język interfejsu i eksportów, motyw interfejsu i eksportów, katalogi eksportów i zrzutów ekranu oraz ich
  czyszczenie.

#### 12. Pomoc

- Jedna sekcja na ekran, skróty klawiszowe, wiersz poleceń oraz **Kontakt i wsparcie**.

[↑ Spis treści](#spis-treści)

---

## Zabezpieczenia w szczegółach

Każde zabezpieczenie odpowiada na konkretne zagrożenie; żadne nie jest narzucone.

| Zabezpieczenie | Przed czym | Gdzie |
|---|---|---|
| Brama (reguły) | Serie połączeń z jednego lub kilku adresów, połączenia, które nie są kierowane do strony | Zapora Funnel |
| Grupowanie | Ataki z rozproszonych adresów (tysiące adresów, po jednym połączeniu z każdego) | Zapora Funnel |
| Czarna lista | Adresy i sieci znane z ataków, przechowywane długoterminowo | Ataki i decyzje |
| Ograniczenie zasobów | `tailscaled`, który pod atakiem zająłby całą maszynę | Przetrwanie |
| Bezpiecznik | Maszyna mimo wszystko wysycona: odciąć Funnel na chwilę | Przetrwanie |
| Automatyczny nadzór | To samo, gdy nikogo nie ma przed ekranem | Przetrwanie |
| Osłona WireGuard | Zalew pakietów UDP na port `tailscaled`, przy otwartym Funnel lub nie | Przetrwanie |

### Brama (Zapora Funnel)

Reguły są stosowane w tej kolejności, wszystkie przed szyfrowaniem:

1. **Maszyny tailnetu** (100.64.0.0/10, fd7a:115c:a1e0::/48): zawsze wpuszczane.
2. **Lista zaufanych**: nigdy nie ograniczana. **Czarna lista**: odrzucana aż do usunięcia z listy.
3. **Częstotliwość na adres** (domyślnie 40 połączeń / 10 s): po jej przekroczeniu adres jest blokowany na wybrany
   czas (domyślnie 60 min).
4. **Częstotliwość na prefiks** /24 w IPv4, /64 w IPv6.
5. **Budżet globalny** wpuszczanych połączeń na sekundę: procesor nigdy nie zostaje przeciążony.
6. **Docelowa nazwa**: połączenie, które nie jest kierowane do nazwy maszyny, jest odrzucane.

Certyfikat `*.ts.net` bramy jest pobierany z Tailscale, sprawdzany codziennie i odnawiany na gorąco 30 dni przed
wygaśnięciem. Tryb **obserwacji** liczy wszystko, niczego nie odrzucając.

### Grupowanie (odciski, AS, kraje)

Przy ataku z rozproszonych adresów reguły na adres widzą każdy adres tylko raz. Dlatego brama klasyfikuje też
każdego klienta według jego **odcisku JA4**, **AS** i **kraju** i liczy częstotliwość połączeń każdej grupy.

- **Automatyczny tryb ataku**: powyżej 80 połączeń przychodzących na sekundę (wartość regulowana) brama sama
  przechodzi w tryb ataku i wychodzi z niego po 5 minutach spokoju.
- Tylko w trybie ataku: nieznany odcisk, którego liczba gwałtownie rośnie, AS hostingu lub chmury (lista
  modyfikowalna) albo kraj z twojej listy (domyślnie pustej), który przekracza swoją częstotliwość, jest odrzucany.
- **Popularne przeglądarki** (Chrome, Edge, Firefox) nigdy nie są objęte tymi regułami; **znani klienci**
  (wpuszczeni w ciągu ostatnich 24 h) mają pierwszeństwo przed budżetem globalnym.
- **Uczenie się**: przez 7 dni brama uczy się zwykłych odcisków twojej strony (nigdy podczas ataku); do tego czasu
  grupowanie pozostaje w trybie obserwacji.
- Poza atakiem klasyfikowane jest jedno połączenie na dziesięć; podczas ataku — wszystkie.
- Baza AS / krajów to **DB-IP Lite**, pobierana i aktualizowana raz w miesiącu.

### Przetrwanie

- **Ograniczenie zasobów**: osobny plik nakładki ogranicza `tailscaled` (na przykład do jednego pełnego rdzenia na
  maszynie z 4 wątkami) i obniża jego priorytet. Twoja własna konfiguracja nigdy nie jest modyfikowana.
- **Bezpiecznik**: gdy `tailscaled` utrzymuje się powyżej progu CPU (domyślnie 80 % rdzenia przez 60 s) albo
  temperatura osiąga 85 °C, omega-tail proponuje odcięcie Funnel na 10 minut (automatyczne przywrócenie, w
  identycznej postaci, nawet przy zamkniętym omega-tail), całkowite odcięcie albo czekanie. Tailnet nigdy nie jest
  odcinany.
- **Automatyczny nadzór** (domyślnie wyłączony): usługa działająca na twoim koncie sama odcina Funnel po trzech
  przekroczeniach — na 15 minut za pierwszym razem, 30 za drugim, potem na godzinę — i sama go przywraca.

### Osłona portu WireGuard

`tailscaled` zużywa około jednego rdzenia procesora na 100 000 pakietów na sekundę odebranych na jego porcie UDP,
nawet nieprawidłowych. Osłona to tabela nftables umieszczona przed nim, na kartach sieciowych:

- **znani partnerzy** (peers, do których `tailscaled` pisze) nigdy nie są ograniczani;
- uzgadnianie połączenia (handshake) jest ograniczone do 20 na sekundę na źródło;
- pozostałe źródła mają budżet (po 500 pakietów na sekundę każde, łącznie 5 000);
- pakiety, które nie są ruchem WireGuard, są odrzucane.

Najpierw jest zakładana w trybie **obserwacji**, potem w trybie **aktywnym**. Jeśli maszyny są połączone przez
omega-connect, **omega-fire** (3.7.0 lub nowszy) może ją założyć i zarządzać nią zamiast omega-tail: to ta sama
tabela, która zmienia właściciela, pozostając nietknięta.

[↑ Spis treści](#spis-treści)

---

## Pomiary

Wybory omega-tail wynikają z pomiarów, na maszynach tej samej generacji co te, które chroni (procesory z lat
2010–2016, w większości bez akceleracji AES).

| Pomiar | Wynik |
|---|---|
| Udział TLS w koszcie połączenia przy domyślnym Funnel | około 80 % |
| Koszt połączenia **odrzuconego** przez bramę w porównaniu z domyślnym Funnel | **4,6 razy mniej** |
| Koszt połączenia **wpuszczonego** przez bramę w porównaniu z domyślnym Funnel | **2 razy mniej** |
| Przepustowość z bramą, połączenia utrzymywane otwarte (w porównaniu z TLS w Go, takim jak w `tailscaled`) | **+15 %** żądań, −20 % CPU |
| Osłona WireGuard: zalew, który zajmował `tailscaled` cały rdzeń | **1 %** rdzenia |
| Pamięć usług (brama, nadzór, osłona) | około 67 MB |

Brama nie pogarsza więc przepustowości strony: na tych maszynach ogranicza samo szyfrowanie, z omega-tail czy bez,
a w środowisku produkcyjnym Funnel i tak przechodzi przez przekaźniki Tailscale i przez router.

[↑ Spis treści](#spis-treści)

---

## Architektura

```text
src/omega_tail/
├── app/              Korzeń kompozycji: składa warstwy, punkt wejścia (interfejs, wiersz poleceń)
├── core/             Wspólne stałe
├── domain/           Czysta logika biznesowa: reguły bramy, alerty, bezpiecznik, nadzór, czarna lista…
├── application/      Przypadki użycia: publikacja, zapora, przetrwanie, raport, ustawienia
├── ports/            Kontrakty (Protocol) oczekiwane przez aplikację
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, logi, eksporty, skrypty Lua
├── interfaces/       tui/ (Textual), cli/ (wiersz poleceń), shared/ (pomoc, raport, prezentacja)
└── shared/           Języki (gettext)
```

### Zasady projektowe

- `domain/` nie zawiera ani odczytu, ani zapisu: wszystko jest w nim testowalne bez maszyny.
- `application/` orkiestruje przypadki użycia za pomocą domeny i portów; interfejs i wiersz poleceń wywołują te
  same przypadki użycia.
- Tylko `infrastructure.commands` i `infrastructure.privileged` uruchamiają polecenia; interfejs nigdy nie robi
  tego bezpośrednio. Te reguły są sprawdzane automatycznie (import-linter).
- Interfejs opiera się na [omega-lib](https://github.com/kraynux), bibliotece współdzielonej przez cały pakiet
  OMEGA (motywy, wykrywanie terminala, języki, kontakt i wsparcie, osłona WireGuard). Nie jest publikowana w PyPI:
  jest dołączona do archiwum (`vendor/omega-lib/`).
- Każde wolne wywołanie (Tailscale, HAProxy, dysk, sieć) działa jako zadanie w tle: interfejs nigdy się nie
  zawiesza.

[↑ Spis treści](#spis-treści)

---

## Wymagania

### System

- Linux, dowolna dystrybucja (testowane na Arch Linux i pochodnych).
- Python 3.10 lub nowszy, z modułem `venv`.
- System init: **systemd**, **OpenRC** lub **runit**.
- `sudo` dla akcji zmieniających maszynę (wymagane akcja po akcji, nigdy przy uruchomieniu).
- Terminal o rozmiarze co najmniej 80×24 (zobacz [Motywy i terminale](#motywy-i-terminale)).

### Tailscale

- **Tailscale** zainstalowany i połączony (klient `tailscale` i usługa `tailscaled`); testowane z wersją 1.104.
- Dla Funnel: MagicDNS, certyfikaty HTTPS i Funnel dozwolone w konsoli Tailscale (zobacz
  [Co musi umożliwiać Tailscale](#co-musi-umożliwiać-tailscale-konsola-administracyjna)).

### Zależności Pythona

Instalowane przez `install.sh` w środowisku wirtualnym:

- `textual`: interfejs.
- `omega-lib`: współdzielona biblioteka pakietu OMEGA, dołączona do archiwum.

### Składniki obowiązkowe i opcjonalne

omega-tail wykrywa, co jest obecne, i włącza tylko to, czego można użyć.

| Składnik | Rola | Status |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Wszystko, czym steruje omega-tail | **Obowiązkowy** |
| Python 3.10+, `textual`, `omega-lib` | Aplikacja | **Obowiązkowy** |
| systemd, OpenRC lub runit | Usługi bramy, nadzoru, osłony | **Obowiązkowy** (jeden z trzech) |
| HAProxy 3.x | Brama Zapory Funnel | Opcjonalny (do zainstalowania z poziomu omega-tail) |
| HAProxy z Lua | Grupowanie (odciski, AS, kraje) | Opcjonalny (przypadek popularnych dystrybucji) |
| nftables (jądro z `nft_limit`) | Osłona portu WireGuard | Opcjonalny |
| Odczyt dziennika systemowego (grupa `systemd-journal`, `adm` lub `wheel`) | Logi, raport ataków | Zalecany |
| Przeglądarka i środowisko graficzne | „Pokaż eksporty” w przeglądarce (w przeciwnym razie odczyt w omega-tail) | Opcjonalny |
| omega-connect | Rejestr, synchronizacja, aktualizacje pakietu | Opcjonalny |
| omega-fire 3.7.0+ | Zarządzanie osłoną WireGuard z poziomu omega-fire | Opcjonalny |

[↑ Spis treści](#spis-treści)

---

## Instalacja

Oficjalne archiwum jest dostarczane w formacie `.tar.gz`. Przed instalacją sprawdź jego integralność za pomocą
pliku `sha.txt` opublikowanego obok:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Te trzy metody służą do pierwszej instalacji.** Jeśli `~/omega-tail` już istnieje, skorzystaj z sekcji
> [Aktualizacja](#aktualizacja). Nigdy nie uruchamiaj tych poleceń ponownie z wnętrza istniejącego katalogu
> `omega-tail`: `tar` utworzyłby zagnieżdżony `omega-tail/omega-tail/`.

Żaden krok instalacji nie wymaga uprawnień roota: omega-tail uruchamia się jako zwykły użytkownik.

### Metoda 1 — skrypt instalacyjny

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Wygląda na to, że jesteś już w katalogu omega-tail — zobacz sekcję Aktualizacja w README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Już tu rozpakowano, krok pominięty." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail już istnieje, przeniesienie pominięte." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

Skrypt tworzy środowisko wirtualne, instaluje zależności (najpierw dołączoną omega-lib), nadaje programom
startowym prawo wykonywania, zapisuje token instalacji odczytywany przez omega-connect i proponuje alias
`omega-tail`. Można go bezpiecznie uruchamiać ponownie.

### Metoda 2 — odporna pełna instalacja

To polecenie można uruchamiać ponownie: pomija kroki już wykonane.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Wygląda na to, że jesteś już w katalogu omega-tail — zobacz sekcję Aktualizacja w README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail już istnieje, rozpakowanie pominięte." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv już istnieje, krok pominięty." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail zainstalowany. Uruchom ./omega-tail.sh."
```

### Metoda 3 — szczegółowa instalacja

```bash
# 0. Sprawdzić, że nie uruchamiamy z wnętrza istniejącego omega-tail
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Wygląda na to, że jesteś już w katalogu omega-tail — zobacz sekcję Aktualizacja w README." >&2; exit 1; }

# 1. Rozpakować
[ -d omega-tail ] && echo "ℹ️ Już tu rozpakowano, krok pominięty." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Przenieść do katalogu domowego
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail już istnieje, przeniesienie pominięte." || mv omega-tail ~/

# 3. Wejść do projektu
cd ~/omega-tail/

# 4. Utworzyć środowisko wirtualne
[ -f .venv/bin/activate ] && echo "ℹ️ .venv już istnieje, tworzenie pominięte." || python3 -m venv .venv

# 5. Zainstalować zależności (najpierw dołączona omega-lib)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Nadać programom startowym prawo wykonywania
chmod +x omega-tail.sh install.sh

# 7. Zapisać token instalacji (odczytywany przez omega-connect; opcjonalnie)
./omega-tail.sh synchro jeton

# 8. Uruchomić
./omega-tail.sh
```

W Debianie, Ubuntu i pochodnych moduł `venv` nie zawsze jest instalowany razem z Pythonem:
`sudo apt install python3-venv`.

### Aktualizacja

Usługi omega-tail (brama, nadzór) korzystają z plików w `~/omega-tail/var/`. Aktualizacja musi więc **pozostawić
ten katalog na miejscu**: archiwum nie zawiera `var/` i rozpakowuje się na istniejącą instalację.

Z katalogu zawierającego archiwum, **innego niż `~/omega-tail`**:

```bash
# 1. Wykonać kopię zapasową bieżącej instalacji (łącznie z var/)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Rozpakować nową wersję na istniejącą (var/ zostaje zachowany)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Zainstalować ponownie (zależności, programy startowe, token instalacji)
cd ~/omega-tail
./install.sh

# 4. Ponownie uruchomić omega-tail
./omega-tail.sh
```

Jeśli brama jest aktywna, **Zapora Funnel → „Zastosuj reguły”** odtwarza jej konfigurację w nowej wersji, na
gorąco. Jeśli automatyczny nadzór jest włączony, **Przetrwanie → „Włącz nadzór”** uruchamia go ponownie z nowym
kodem. Aktualizację może też przeprowadzić omega-connect (ekran Updater).

### Alias Bash lub Zsh

`install.sh` proponuje alias. Aby dodać go ręcznie:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

Alias nazywa się `omega-tail`, a nie `tail`, aby nie przesłaniać systemowego polecenia `tail`.

[↑ Spis treści](#spis-treści)

---

## Użytkowanie

### Uruchamianie

```bash
cd ~/omega-tail
./omega-tail.sh

# lub po prostu, jeśli alias został utworzony:
omega-tail
```

Program startowy nie wymaga podniesienia uprawnień: omega-tail działa na twoim koncie, a o sudo proszą tylko
akcje, które go potrzebują, w terminalu, z poleceniem wyświetlonym wcześniej.

### Zalecane pierwsze kroki

Aby chronić stronę opublikowaną przez Funnel, w tej kolejności:

1. **Pulpit**: przeczytaj alerty; **Zostań operatorem** (raz, przez sudo), aby zmieniać ustawienia Tailscale bez sudo.
2. **Przetrwanie → Zastosuj ograniczenie**: `tailscaled` nie będzie już mógł zająć całej maszyny.
3. **Publikacja**: opublikuj stronę przez **HTTPS na porcie 443**, ścieżka `/`, a następnie wykonaj **test
   end-to-end**.
4. **Zapora Funnel → Zainstaluj HAProxy**, potem **Włącz ochronę**, najpierw w trybie **obserwacji**.
5. Kilka dni później, **Ataki i decyzje**: jeśli liczniki pokazują wyłącznie nadużycia, przełącz bramę w tryb
   **normalny**.
6. Pozwól **grupowaniu** uczyć się przez 7 dni w trybie obserwacji, a potem przełącz je na **stosowane**.
7. **Przetrwanie → Osłona portu WireGuard**: załóż w trybie obserwacji, potem przełącz na aktywny.
8. Dla maszyny, przed której ekranem nikt nie siedzi: **Przetrwanie → Włącz nadzór**.

### Języki interfejsu

17 języków: francuski, angielski, hiszpański, portugalski (Brazylia), włoski, niemiecki, niderlandzki, polski,
rosyjski, chiński, wietnamski, tajski, indonezyjski, japoński, koreański, hindi, arabski.

- Wybór w ustawieniach (klawisz `s`, « Langue / Language », etykieta nigdy nietłumaczona), stosowany przez ponowne
  uruchomienie samego interfejsu.
- Jednorazowo: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- W konsoli tekstowej Linuksa (TTY) języki, których pisma brakuje w czcionkach konsoli, są wyświetlane po
  angielsku na czas sesji; arabski jest wyświetlany od prawej do lewej.
- **Język eksportów** (raport, czarna lista, logi) ustawia się osobno, domyślnie „Jak interfejs”.

### Kontakt i wsparcie

Pomoc (klawisz `a`) oferuje ekran **Kontakt i wsparcie**:

- *Postaw kawę* (strona PayPal dewelopera);
- *Skontaktuj się ze wsparciem* (adres e-mail i formularz strony, wyświetlane jawnie);
- *Zgłoś mnie jako użytkownika (anonimowo)*;
- *Sprawdź aktualizacje*.

Zgłoszenie jest dobrowolne, domyślnie wyłączone i wysyłane tylko raz. Służy wyłącznie do liczenia użytkowników
oraz, jeśli tego chcesz, ich kontynentu lub kraju (zamknięte listy, nigdy dowolny tekst). Wysyła losowo
wygenerowany klucz, nazwę programu (`omega-tail`) i jego wersję; nigdy imienia i nazwiska, nazwy maszyny,
ustawienia ani adresu tailnetu. Wycofanie w dowolnym momencie z tego samego ekranu (*Nie zgłaszaj mnie więcej*).
Sprawdzanie aktualizacji odczytuje jedynie listę wersji opublikowanych na stronie, i nigdy bez kliknięcia.

### Powiązania z innymi narzędziami omega

- **omega-connect**: `install.sh` zapisuje token instalacji (`var/omega-jeton.json`), który opisuje narzędzie i
  jego wersję, niczego nie wykonując. omega-connect używa go do Rejestru, synchronizacji, naprawy, aktualizacji i
  instalacji. `./omega-tail.sh synchro jeton` zapisuje go ponownie ręcznie.
- **omega-fire** (3.7.0 lub nowszy), połączony przez omega-connect, może założyć osłonę portu WireGuard i nią
  zarządzać; jego lista reguł pokazuje ją z pochodzeniem omega-tail.

### Wiersz poleceń

Wszystkie polecenia zapisuje się jako `./omega-tail.sh …` (lub `omega-tail …` z aliasem):

| Polecenie | Rola |
|---|---|
| `omega-tail` | Interfejs |
| `omega-tail etat [--format json]` | Stan Tailscale, maszyny i alerty, jako tekst lub dla skryptu |
| `omega-tail aide` | Pełna pomoc w formie tekstowej |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | Raport, wyświetlony lub zapisany |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Odciąć lub przywrócić Funnel |
| `omega-tail veille etat` | Stan automatycznego nadzoru i jego ostatnie wiersze |
| `omega-tail porte etat` | Stan bramy i liczniki |
| `omega-tail porte certificat [--si-besoin]` | Odnowić certyfikat `*.ts.net` bramy |
| `omega-tail porte groupes` | Grupowanie: tryb ataku, odciski, AS, kraje |
| `omega-tail porte base` | Zaktualizować bazę AS / krajów |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Zablokować adres lub sieć (czarna lista z `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Odblokować |
| `omega-tail porte confiance ADRESSE` | Dodać do zaufanych |
| `omega-tail synchro jeton` | Zapisać token instalacji (omega-connect) |
| `omega-tail --version` | Wersja |

### Ogólny przebieg

1. Ekran startowy, a następnie menu główne w dwóch kolumnach (TAILSCALE i OCHRONA).
2. Pod tytułem każdego ekranu **pasek stanu** podsumowuje wszystko: usługę, CPU maszyny i `tailscaled`,
   temperaturę, pamięć, Funnel, zaporę, nadzór, połączenie. Jest odczytywany co 5 sekund.
3. Każda akcja zmieniająca maszynę pokazuje swoje polecenie, a następnie prosi o potwierdzenie; sudo wpisuje się w
   terminalu, po czym interfejs wraca.
4. Akcje wrażliwe (trwałe wylogowanie, pełne czyszczenie czarnej listy) wymagają wpisania słowa.
5. Wynik jest wyświetlany w jednym wierszu, sprawdzony na ponownie odczytanym stanie.

### Nawigacja

- Strzałki w górę / w dół: przechodzenie między elementami (wiersze tabeli, przyciski).
- Tab / Shift+Tab: przechodzenie między obszarami ekranu.
- Enter lub kliknięcie: aktywacja wybranego przycisku; w tabeli alertów — „Popraw”.
- `Esc`: powrót do poprzedniego ekranu (w menu: wyjście).
- `a`: pomoc, z dowolnego ekranu.
- `s`: ustawienia, z dowolnego ekranu.
- `t`: następny motyw (zapisywany).
- `r`: odświeżenie ekranu, wyświetlenie rozmiaru terminala i ponowny odczyt stanu.
- `q`: wyjście, z potwierdzeniem.
- `Ctrl+P`: polecenia (motyw, zrzut ekranu w SVG do katalogu zrzutów, wyjście).

[↑ Spis treści](#spis-treści)

---

## Motywy i terminale

Dziesięć motywów `omega-*` jest współdzielonych z resztą pakietu OMEGA:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Przełączaj motywy klawiszem `t` lub wybierz jeden w ustawieniach (`s`); wybór jest zapamiętywany.
- Eksporty HTML mają własne motywy: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail dostosowuje złożoność wizualną do wykrytego terminala za pomocą **profilu renderowania**: Pełny,
  Standardowy, Zredukowany lub Mono (tylko ASCII).

| Minimalny rozmiar | Profil | Typowe terminale |
|---|---|---|
| 120×32 lub więcej | Pełny | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 lub więcej | Standardowy | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 lub więcej | Zredukowany | urxvt, xterm, nowoczesne SSH |
| poniżej 80×24 | Mono (tylko ASCII) | Linux TTY, starsze SSH |

Po zmianie rozmiaru okna `r` ponownie odczytuje rozmiar terminala; jest on wyświetlany u góry, obok motywu.

[↑ Spis treści](#spis-treści)

---

## Pliki, usługi i zgodność

### W katalogu omega-tail

Cały stan omega-tail znajduje się w `~/omega-tail/var/`, odtwarzanym przy uruchomieniu i nigdy niepublikowanym:

```text
var/
├── settings.json         ustawienia (język, motywy, katalogi, progi, reguły bramy)
├── omega-jeton.json      token instalacji (omega-connect)
├── porte/                konfiguracja bramy, certyfikat, lista zaufanych i czarna lista, baza AS / krajów
├── veille/               log automatycznego nadzoru
├── survie/               oryginały zmodyfikowanych plików, stan bezpiecznika
├── funnel/sauvegardes/   publikacja sprzed każdej zmiany (50 najnowszych)
├── exports/              wyeksportowane raporty, logi i listy
└── screenshots/          zrzuty ekranu (Ctrl+P)
```

### W systemie (tylko jeśli włączysz dane zabezpieczenie)

Każdy plik jest instalowany przez sudo, z pokazanym poleceniem, i usuwany odwrotną akcją w omega-tail.

| Plik lub usługa | Instalowany przez | Usuwany przez |
|---|---|---|
| Usługa `omega-tail-porte` (systemd, OpenRC lub runit) i `omega-tail-porte-certificat` (timer systemd lub oznaczony wiersz w twoim crontabie) | Włącz ochronę | Wyłącz ochronę |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (lub grupa kontrolna poza systemd) | Zastosuj ograniczenie | Usuń ograniczenie |
| Timery `omega-tail-retablir-*` (przywrócenie po odcięciu) | Bezpiecznik | Koniec odcięcia |
| Usługa `omega-tail-veille` | Włącz nadzór | Wyłącz nadzór |
| Usługa `omega-bouclier-wg`, tabela nftables, `/etc/omega-bouclier-wg/` | Osłona: Załóż | Osłona: Zdejmij |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | Włącz przekazywanie IP | Usunięcie pliku |

Plik `override.conf` usługi `tailscaled`, jeśli istnieje, nigdy nie jest modyfikowany.

### Systemy init

| | systemd | OpenRC | runit |
|---|---|---|---|
| Usługa `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Logi | `journalctl` | pliki usługi | `svlogd`, `socklog` |
| Ograniczenie zasobów | plik nakładki systemd | grupa kontrolna (cgroup v2) | grupa kontrolna (cgroup v2) |
| Chwilowe odcięcie | timer systemd | odłączony proces na twoim koncie | odłączony proces na twoim koncie |
| Brama, nadzór, osłona | usługi systemd | usługi OpenRC | usługi runit |

Poza systemd ograniczenie przez grupę kontrolną jest tracone, gdy `tailscaled` się restartuje: alert proponuje
wtedy jego ponowne zastosowanie.

### IPv4 i IPv6

Brama, listy, grupowanie i osłona obsługują obie rodziny. Liczone prefiksy to /24 w IPv4 i /64 w IPv6; adres IPv4
widziany w postaci `::ffff:a.b.c.d` jest traktowany jak adres IPv4.

[↑ Spis treści](#spis-treści)

---

## Bezpieczeństwo

omega-tail działa na usłudze wystawionej do Internetu; został zaprojektowany tak, by nigdy nie pogarszać sytuacji.

- **Nigdy root**: aplikacja, brama HAProxy i nadzór działają na twoim koncie; o sudo prosi się tylko przy
  instalowaniu lub usuwaniu usługi, z poleceniem pokazanym wcześniej.
- **Prywatne kanały**: gniazda administracyjne bramy mają tryb 600 w katalogu 700; synchronizacja jej tabel
  przechodzi przez gniazdo w tym samym katalogu.
- **Wycofanie zmian**: każde przełączenie Funnel jest zapisywane w kopii zapasowej, sprawdzane, a w razie
  niepowodzenia przywracany jest stan poprzedni.
- **Najpierw obserwacja**: brama, grupowanie i osłona są zakładane w trybie obserwacji; nic nie jest odrzucane,
  zanim tego nie zdecydujesz.
- **Tailnet nigdy nie jest odcinany**: brama zawsze wpuszcza twoje maszyny, a bezpiecznik odcina tylko Funnel.
- **Sprawdzane dane wejściowe**: do HAProxy trafiają wyłącznie adresy lub sieci w postaci kanonicznej; nazwy
  zgłaszane przez maszyny tailnetu są oczyszczane przed wyświetleniem.
- **Audyt**: kod przeszedł audyt (claude-security, 2026-11-25); 7 wykrytych problemów, z których żaden nie był
  zdalnie wykorzystywalny przez odwiedzającego, zostało poprawionych tego samego dnia.
- Testuj najpierw na maszynie testowej lub w trybie obserwacji, a do prób IPv4 używaj sieci dokumentacyjnych
  RFC 5737: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Spis treści](#spis-treści)

---

## Testy i jakość

Zestaw liczy **179 testów**: domena, przypadki użycia, infrastruktura (z symulowanym Funnel), ekrany Textual z
prawdziwymi arkuszami stylów, systemy init, bezpieczeństwo. Kod jest sprawdzany przez `ruff`, `mypy` i
`import-linter` (reguły warstw). Katalog `tests/` jest dołączony do archiwum.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

Większość testów nie wymaga ani Tailscale, ani HAProxy, ani roota.

[↑ Spis treści](#spis-treści)

---

## Stan projektu

### Elementy działające

- Pełne sterowanie Tailscale: usługa, połączenie, ustawienia, publikacja, sieć, logi.
- Brama HAProxy przed TLS, w środowisku produkcyjnym od 2026-11-23, z regułami, listami, grupowaniem i trybem
  ataku.
- Przetrwanie: ograniczenie zasobów, bezpiecznik, automatyczny nadzór.
- Osłona portu WireGuard, w środowisku produkcyjnym od 2026-11-24.
- Raport i eksporty TXT, HTML, JSON.
- Zgodność z omega-connect i omega-fire.

### Znane ograniczenia

- Usługi pod OpenRC i runit są objęte testami, ale nie zostały jeszcze sprawdzone na prawdziwej maszynie.
- Brama chroni Funnel opublikowany przez HTTPS na jednym porcie, ze ścieżką `/`.
- Grupowanie wymaga HAProxy skompilowanego z Lua; bez Lua brama działa bez niego.
- Osłony nie można założyć na jądrze zaktualizowanym bez ponownego uruchomienia (brak modułów): ekran o tym
  informuje.
- Atak, który wysyca samo łącze internetowe, pozostaje poza zasięgiem narzędzia zainstalowanego na maszynie.
- Przepustowość strony opublikowanej przez Funnel pozostaje ograniczona przez przekaźniki Tailscale i przez router.

[↑ Spis treści](#spis-treści)

---

## Odinstalowanie

Najpierw usuń z poziomu omega-tail to, co zostało zainstalowane w systemie, w tej kolejności:

1. **Zapora Funnel → Wyłącz ochronę** (Funnel zostaje przywrócony do stanu sprzed).
2. **Przetrwanie → Wyłącz nadzór**.
3. **Przetrwanie → Osłona portu WireGuard → Zdejmij**.
4. **Przetrwanie → Usuń ograniczenie**.

Następnie usuń katalog:

```bash
rm -rf ~/omega-tail
```

Usuń ręcznie eksporty umieszczone gdzie indziej, alias `omega-tail` z `~/.bashrc` lub `~/.zshrc` oraz, jeśli go
włączyłeś, plik `/etc/sysctl.d/99-omega-tail-forwarding.conf`. Uprawnienie operatora Tailscale odbiera się
poleceniem `sudo tailscale set --operator=`.

[↑ Spis treści](#spis-treści)

---

## Licencja

Omega-Tail jest rozpowszechniany na licencji **MIT**. Pełny tekst znajdziesz w pliku [`LICENSE`](../../../LICENSE).

Baza AS / krajów korzysta z IP Geolocation by [DB-IP](https://db-ip.com), na licencji
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Spis treści](#spis-treści)

---

> **Omega-Tail — Sterować Tailscale, chronić Funnel.**
>
> Interfejs TUI dla Tailscale i brama, która odrzuca nadużycia przed jakimkolwiek szyfrowaniem.
