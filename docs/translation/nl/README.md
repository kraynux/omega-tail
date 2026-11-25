<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**Beheertool voor TAILSCALE met geïntegreerde firewall voor FUNNEL**

OMEGA-TAIL is de tool van de OMEGA-suite die **Tailscale** op een machine aanstuurt en die machine **beschermt**
wanneer ze een dienst op internet publiceert via **Tailscale Funnel**.

> Ontwikkeld door [kraynux](https://github.com/kraynux) voor [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Officiële pagina](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/nl/) · [Schermafbeeldingen](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Interface, documentatie, exports en bezoekerspagina's beschikbaar in **17 talen** — zie [Talen van de interface](#talen-van-de-interface).  
**Talen:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** is een TUI-applicatie (Terminal User Interface) in Python, gebouwd met
[Textual](https://textual.textualize.io/). Hiermee beheert en regelt u **Tailscale** in geavanceerde modus vanuit
een interface, zonder ook maar één commando te hoeven onthouden. Ze voegt ook beschermingen toe (firewall,
inperking, overleven…) voor de **Funnel**-modus, die een dienst van de machine openstelt voor heel internet.

Elke actie die de machine wijzigt, toont eerst haar commando. Het sudo-wachtwoord wordt in de terminal ingevoerd,
actie per actie, en niets wordt zonder u op de achtergrond gestart.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-tail/F.png" width="32%" />
</p>

Het project is opgezet volgens de principes van de **Clean Architecture**, met `app/` als compositieroot: het
domein, de orkestratie, de infrastructuur en de interface zijn van elkaar gescheiden.

## Inhoud

- [Presentatie](#presentatie)
- [Tailscale en Funnel begrijpen](#tailscale-en-funnel-begrijpen)
- [Functies](#functies)
- [De beschermingen in detail](#de-beschermingen-in-detail)
- [Metingen](#metingen)
- [Architectuur](#architectuur)
- [Vereisten](#vereisten)
- [Installatie](#installatie)
- [Gebruik](#gebruik)
- [Thema's en terminals](#themas-en-terminals)
- [Bestanden, diensten en compatibiliteit](#bestanden-diensten-en-compatibiliteit)
- [Beveiliging](#beveiliging)
- [Tests en kwaliteit](#tests-en-kwaliteit)
- [Projectstatus](#projectstatus)
- [Verwijderen](#verwijderen)
- [Licentie](#licentie)

---

## Presentatie

### Waarom omega-tail

Tailscale Funnel publiceert een dienst van de machine op internet zonder een poort op de router te openen: de
bezoekers komen binnen via de relays van Tailscale. Dat is eenvoudig en veilig aan de netwerkkant, maar er blijft
een zwak punt.

- **De kosten van de versleuteling.** In de standaard-Funnel-modus voert de dienst `tailscaled` van de machine de
  TLS-handshake van elke bezoeker uit. Gemeten op een kleine machine is dat ongeveer **80 % van de kosten van een
  verbinding**. Enkele honderden nieuwe verbindingen per seconde volstaan om de processor te verzadigen: één gewone
  computer met een eenvoudig script kan de site en de machine platleggen.
- **Onzichtbare bezoekers.** De gebruikelijke firewalls (nftables, ufw, fail2ban) zien deze bezoekers niet: ze komen
  versleuteld binnen, via de tunnel van Tailscale, met het adres van een relay.
- **Verspreide instellingen.** De instellingen van Tailscale (operator, exitnode, routes, SSH, schild…) zijn
  talrijk, verdeeld over commando's en webconsole, en sommige kunnen de lopende sessie verbreken.

### Doelstellingen

- Tailscale volledig vanuit een interface aansturen, met een verklarende zin bij elke instelling.
- Misbruikende verbindingen **vóór** elke versleuteling weigeren, met zicht op het echte adres van elke bezoeker.
- De machine overeind houden tijdens een aanval: het beheer en de andere diensten blijven bereikbaar.
- Nooit iets opleggen: voorstellen, het commando tonen, vragen, en terug kunnen gaan.
- Werken op elke Linux-distributie, onder systemd, OpenRC of runit.

### Wat omega-tail doet

- Toont de toestand van Tailscale, van de machine en van wat gepubliceerd is, met waarschuwingen die naar het
  scherm leiden dat het probleem oplost.
- Start, stopt en herstart `tailscaled`, met een vangnet als uw sessie via Tailscale loopt.
- Beheert de verbinding, de accounts en alle instellingen van `tailscale set`, gecontroleerd voordat ze worden
  toegepast.
- Publiceert, verwijdert, schort op en test de diensten van Serve en Funnel, met back-ups en herstel.
- Toont de apparaten van het tailnet, hun pad (direct of via een relay), een netwerkdiagnose en de logs.
- Plaatst een HAProxy-**slagboom** tussen Funnel en uw site: regels per adres, per prefix, globaal budget,
  vertrouwens- en blokkeerlijst, groeperingen op JA4-vingerafdruk, herkomstnetwerk (AS) en land, automatische
  aanvalsmodus.
- Perkt `tailscaled` in, schakelt Funnel tijdelijk of volledig uit, en kan dat zelfstandig doen dankzij een
  automatische bewaking.
- Beschermt de WireGuard-poort van `tailscaled` met een nftables-tabel (schild).
- Maakt een rapport van de machine en van de aanvallen van de laatste 7 dagen, in TXT, HTML of JSON.

### Wat het project niet doet

- Het vervangt Tailscale niet: het stuurt het aan.
- Het beschermt niet tegen een volumetrische aanval die de internetlijn zelf verzadigt (de router, de verbinding).
- Het beheert de webbeheerconsole van Tailscale niet (toegangsbeleid, goedkeuring van exitnodes, activering van
  Funnel voor het tailnet).
- Het beschermt geen dienst die anders dan via Funnel is gepubliceerd: voor die poorten is er omega-fire.
- Het draait nooit als root en start niets op de achtergrond zonder uw toestemming.
- Het werkt niet onder Windows en niet onder macOS.

[↑ Inhoud](#inhoud)

---

## Tailscale en Funnel begrijpen

omega-tail veronderstelt enkele begrippen van Tailscale. Dit deel brengt ze samen, zonder verder iets te
veronderstellen.

### De woordenlijst

| Term | Wat het is |
|---|---|
| **Tailnet** | Uw privé-Tailscale-netwerk: alle machines die met hetzelfde account (of dezelfde organisatie) verbonden zijn. Elke machine krijgt daarin een adres in `100.x.y.z` (bereik 100.64.0.0/10) en een IPv6-adres in `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | De dienst (daemon) die op de machine draait: hij onderhoudt de versleutelde WireGuard-tunnel, de netwerkstack van Tailscale en, voor Serve en Funnel, het doorsturen naar uw diensten. |
| **`tailscale`** | Het commando dat `tailscaled` aanstuurt (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail gebruikt het voor u. |
| **WireGuard** | Het protocol van de versleutelde tunnel tussen de machines. `tailscaled` luistert daarvoor op een UDP-poort (standaard 41641), vaak geopend door de router (UPnP). |
| **DERP-relay** | Servers van Tailscale die het verkeer doorgeven wanneer twee machines elkaar niet rechtstreeks kunnen bereiken (lastige NAT). Het „directe” pad is sneller. |
| **MagicDNS** | De namen van de machines van het tailnet, in de vorm `machine.naam-van-het-tailnet.ts.net`. |
| **Serve** | Een lokale dienst (een site, een API…) **alleen voor het tailnet** publiceren, via HTTPS met een geldig `*.ts.net`-certificaat. |
| **Funnel** | Een lokale dienst **voor heel internet** publiceren, op het adres `https://machine.naam-van-het-tailnet.ts.net`. Alleen de poorten 443, 8443 en 10000 kunnen worden geopend. |
| **Funnel-relay** | De servers van Tailscale die de bezoekers van internet ontvangen en in uw tailnet binnenlaten (ze verschijnen als „funnel-ingress-node”). |
| **Operator** | Een Linux-account dat Tailscale zonder sudo mag instellen (`tailscale set --operator=…`). omega-tail stelt het één keer voor, via sudo. |
| **Exitnode (exit node)** | Een machine van het tailnet waarlangs een andere machine al haar internetverkeer leidt (zoals een VPN). Ze moet in de console van Tailscale worden goedgekeurd. |
| **Aangekondigd subnet (subnet router)** | Een lokaal netwerk (bijvoorbeeld `192.168.1.0/24`) dat een machine bereikbaar maakt voor de rest van het tailnet. |
| **Schild (shields up)** | Instelling van Tailscale die alle inkomende verbindingen vanuit het tailnet weigert. |
| **Tailscale SSH** | Een SSH-server die Tailscale levert, toegestaan door het beleid van het tailnet. |
| **PROXY-v2-header** | Een korte header aan het begin van een verbinding, die het echte adres van de bezoeker doorgeeft aan wie de verbinding ontvangt. |
| **JA4-vingerafdruk** | Een handtekening van de manier waarop software een TLS-verbinding opent: een browser en een aanvalstool hebben niet dezelfde. |
| **AS (autonoom systeem)** | Het herkomstnetwerk van een adres: internetprovider, hostingbedrijf, cloud. |

### Het pad van een bezoeker

**Funnel standaard, zonder omega-tail.** `tailscaled` doet alles: het ontsleutelt de WireGuard-tunnel, voert de
TLS-handshake van de bezoeker uit en stuurt het verzoek daarna via HTTP door naar uw site. Geen enkele firewall van
de machine ziet de bezoeker, en elke nieuwe verbinding kost `tailscaled` veel.

```text
Bezoeker ──HTTPS──▶ Funnel-relais ──WireGuard──▶ tailscaled (TLS + HTTP-relay) ──HTTP──▶ uw site
                    (Tailscale)                  └── alle kosten liggen hier
```

**Funnel met de slagboom van omega-tail.** Funnel schakelt over naar TCP-modus: `tailscaled` doet geen TLS meer,
het geeft de nog versleutelde stroom door aan de slagboom, voorafgegaan door het echte adres van de bezoeker
(PROXY-v2-header). De slagboom beslist **vóór** elke versleuteling: een geweigerde verbinding kost bijna niets, en
alleen toegelaten verbindingen worden ontsleuteld, door OpenSSL, sneller dan de TLS van `tailscaled`.

```text
Bezoeker ──HTTPS──▶ Funnel-relais ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                      │
                                                      ▼
                                       Slagboom omega-tail (HAProxy, 127.0.0.1)
                                       ├── geweigerd vóór TLS: blokkeerlijst, rate, budget, doelnaam, groeperingen
                                       └── toegelaten: TLS (certificaat *.ts.net) ──HTTP──▶ uw site
```

De slagboom luistert alleen op de lokale loopback van de machine en draait onder uw account. De machines van uw
tailnet worden er altijd toegelaten, vóór elke regel: alleen de bezoekers van Funnel worden gefilterd.

### Wat Tailscale moet toestaan (beheerconsole)

Deze instellingen worden één keer gedaan, in de webconsole van Tailscale; omega-tail wijzigt ze niet.

- **MagicDNS** en de **HTTPS-certificaten** ingeschakeld voor het tailnet (nodig voor Serve, voor Funnel en voor het
  certificaat van de slagboom).
- **Funnel toegestaan** voor de machine in het toegangsbeleid van het tailnet (attribuut `funnel`).
- Voor een exitnode of aangekondigde subnetten: hun **goedkeuring** in de console.

[↑ Inhoud](#inhoud)

---

## Functies

Het hoofdmenu heeft twee kolommen van zes: **TAILSCALE** om aan te sturen, **BESCHERMING** om te verdedigen.

### TAILSCALE

#### 1. Dashboard

- **Tailscale**: dienst, verbindingstoestand, draaiende en geïnstalleerde versie, naam van de machine, adressen,
  account, apparaten online, verloop van de sleutel, operator, aangeboden en gebruikte exitnode, aangekondigde
  subnetten.
- **Machine**: CPU van de hele machine, belasting per kern, temperatuur, geheugen, CPU en geheugen van `tailscaled`,
  inperking, en daarna de toestand van de beschermingen (Funnel, firewall en aanvalsmodus, blokkeerlijst, bewaking,
  schild).
- **Publicatie**: elke gepubliceerde poort, voor internet (Funnel) of voor het tailnet (Serve), de modus en het doel.
- **Waarschuwingen**, van de ernstigste naar de minst ernstige, met „Oplossen” dat het betreffende scherm opent.
  Bijvoorbeeld: dienst gestopt, update geïnstalleerd maar niet toegepast, sleutel die verloopt, Funnel gepubliceerd
  zonder bescherming, hoge temperatuur, `tailscaled` te veeleisend of niet ingeperkt, groeiende blokkeerlijst.
- Waarden in groen, oranje of rood volgens drempels (CPU, belasting, temperatuur, geheugen, `tailscaled`).

#### 2. Dienst tailscaled

- Toestand volgens het init-systeem, draaiende en geïnstalleerde versie, startcommando, aanvullende bestanden
  (drop-ins), inperking.
- **Starten**, **Stoppen**, **Herstarten** (bijvoorbeeld om een al geïnstalleerde update toe te passen).
- **Vangnet**: als uw sessie via Tailscale loopt (SSH via het tailnet), vraagt Stoppen om een tweede bevestiging,
  want u zou de dienst niet meer opnieuw kunnen starten.
- **Opstart herstellen**: spoort een aanvullend bestand op dat bij het opstarten `tailscale up` uitvoert en de
  machine bij de eerste wijziging van een instelling uit het tailnet kan zetten; de correctie wordt getoond en het
  origineel bewaard.

#### 3. Verbinding en instellingen

- **Aanmelden**, **Afmelden**, **Account toevoegen**, **Van account wisselen**, **Definitief afmelden** (naam van de
  machine intypen).
- **Alle instellingen van `tailscale set`**, elk met een verklarende zin: naam en bijnaam van de machine, routes,
  DNS van het tailnet, schild, stateful filtering, netfilter-modus, exitnode, toegang tot het lokale netwerk, de
  machine aanbieden als exitnode, aangekondigde subnetten, Tailscale SSH, webinterface, updates, peer-relay,
  operator.
- Tijdens het invoeren toont een kader **vóór → na** en het commando; na het toepassen wordt elke opnieuw gelezen
  waarde gemarkeerd met ✔ (overgenomen) of ✖ (niet overgenomen).
- Een waarschuwing meldt wanneer een wijziging een sessie via Tailscale kan verbreken.
- **IP-doorsturing**: met één knop ingeschakeld wanneer de machine als exitnode dient of subnetten aankondigt.

#### 4. Publicatie

- Alles wat de machine publiceert: poort, openbaar (Funnel) of tailnet (Serve), modus, pad, doel, bescherming.
- Een lokale dienst **publiceren** via HTTPS, HTTP, TCP of afgesloten TLS; **Verwijderen**; **Funnel opschorten** en
  **Funnel herstellen** (ongewijzigd).
- **End-to-end-test**: een echte verbinding, zoals een bezoeker (antwoord, tijd, certificaat, TLS-versie).
- **Back-ups**: de toestand vóór elke wijziging (de 50 meest recente), herstelbaar.
- Elke wijziging wordt gecontroleerd; bij een afwijking wordt de publicatie opnieuw opgebouwd, anders wordt de
  vorige toestand teruggezet.

#### 5. Netwerk en apparaten

- **Apparaten** van het tailnet: systeem, online of niet, pad (direct of via een relay), laatst gezien, adres,
  uitgewisseld verkeer; de Funnel-relays van Tailscale zijn standaard verborgen.
- **Tailscale-ping** (pad en latentie), **Wie is dit?** (van wie een adres van het tailnet is).
- **Netwerkdiagnose**: UDP, IPv4 / IPv6, NAT-type, openen van poorten door de router (UPnP, NAT-PMP, PCP),
  dichtstbijzijnde relay en latenties.
- **DNS**, **tailnet-slot** en **interne tellers** van Tailscale.
- Alleen-lezen: niets op dit scherm wijzigt een instelling.

#### 6. Logs

- De log van `tailscaled` (journalctl, of buiten systemd de bestanden van de dienst) en die van de slagboom,
  filterbaar en exporteerbaar.
- Elk gegeven heeft zijn eigen kleur uit het thema: datum, proces, categorie van het bericht (besturing, netwerk, DNS,
  WireGuard-engine), adressen vet, fouten in rood, waarschuwingen in oranje; voor de slagboom reden van weigering,
  groepering, AS en land.

### BESCHERMING

#### 7. Funnel-firewall

- **HAProxy installeren** via de pakketbeheerder van de distributie (pacman, apt, dnf, zypper, apk, xbps, emerge).
- **Bescherming activeren**: certificaat `*.ts.net`, lijsten, gecontroleerde configuratie, dienst van de slagboom,
  omschakelen van Funnel en daarna een test vanaf internet; bij een mislukking wordt de oorspronkelijke publicatie
  meteen teruggezet.
- **Bescherming deactiveren**: Funnel wordt exact teruggezet zoals voorheen, gecontroleerd.
- **Regels** die live worden toegepast, **observatiemodus** om de drempels zonder risico af te stellen,
  **groeperingen** (zie [De beschermingen in detail](#de-beschermingen-in-detail)).
- **Database bijwerken** voor AS / land (DB-IP Lite), in een apart proces.

#### 8. Overleven

- **Inperking van `tailscaled`**: CPU-plafond, gewicht en prioriteit, optie om SSH-toegang voorrang te geven.
- **Funnel-stroomonderbreker**: drempels voor CPU en temperatuur, uitschakeling van 10 minuten (automatisch weer
  ingeschakeld) of volledig.
- **Automatische bewaking**: hetzelfde, zonder dat er iemand achter het scherm zit.
- **Schild van de WireGuard-poort**: knop naar het eigen scherm (observatie, actief, plaatsen, opnieuw plaatsen,
  verwijderen, overdragen).

#### 9. Aanvallen en beslissingen

- Tellers van de slagboom (ontvangen, geweigerd vóór versleuteling, toegelaten, lopend) en de actiefste adressen,
  elke 2 seconden opnieuw gelezen, met land, AS en toestand van elk adres.
- **Blokkeren**, **Blokkeerlijst**, **Deblokkeren**, **Vertrouwen**: meteen toegepast, zonder de slagboom te
  herstarten; de melding geeft in één regel de actie en de plaats van het adres.
- Weergaven **Vingerafdrukken**, **AS** en **Landen**; toestand van de aanvalsmodus en verbindingen geweigerd door
  de groeperingen.
- **Beheer van de blokkeerlijst**: volledige lijst met datum van toevoeging en herkomst, toevoegen, verwijderen,
  importeren van een TXT-bestand (dubbele items, al gedekte netwerken en adressen van het tailnet worden
  uitgesloten), opschoningen met voorbeeld (op ouderdom, de N oudste, een reeks regels, een herkomst, alles),
  exports in TXT (opnieuw importeerbaar), HTML en JSON. Plafond van 50 000 items.

#### 10. Rapport

- Alles wat omega-tail over de machine weet, in feiten: Tailscale, publicatie, machine, firewall, overleven,
  waarschuwingen, en de **aanvallen van de laatste 7 dagen**, gelezen in de log van de slagboom.
- **Privacy**: standaard zonder het Tailscale-account en zonder de namen en adressen van de apparaten van het
  tailnet, zodat u het naar iemand kunt sturen.
- Exports in **TXT**, **HTML** (thema naar keuze) en **JSON**; **Exports bekijken** opent de map in de browser.

#### 11. Instellingen

- Taal van de interface en van de exports, thema van de interface en van de exports, mappen voor de exports en de
  schermafbeeldingen, en het opschonen ervan.

#### 12. Help

- Een sectie per scherm, de sneltoetsen, de opdrachtregel en **Contact en ondersteuning**.

[↑ Inhoud](#inhoud)

---

## De beschermingen in detail

Elke bescherming beantwoordt een specifieke dreiging; geen enkele wordt opgelegd.

| Bescherming | Waartegen | Waar |
|---|---|---|
| Slagboom (regels) | Salvo's vanaf één of enkele adressen, verbindingen die niet op de site gericht zijn | Funnel-firewall |
| Groeperingen | Aanvallen vanaf verspreide adressen (duizenden adressen, elk één verbinding) | Funnel-firewall |
| Blokkeerlijst | Adressen en netwerken waarvan bekend is dat ze aanvallen, langdurig bewaard | Aanvallen en beslissingen |
| Inperking | `tailscaled` dat tijdens een aanval de hele machine zou opeisen | Overleven |
| Stroomonderbreker | Machine ondanks alles verzadigd: Funnel tijdelijk uitschakelen | Overleven |
| Automatische bewaking | Hetzelfde, zonder iemand achter het scherm | Overleven |
| WireGuard-schild | Stroom van UDP-pakketten op de poort van `tailscaled`, of Funnel nu open is of niet | Overleven |

### De slagboom (Funnel-firewall)

De regels gelden in deze volgorde, allemaal vóór de versleuteling:

1. **Machines van het tailnet** (100.64.0.0/10, fd7a:115c:a1e0::/48): altijd toegelaten.
2. **Vertrouwenslijst**: nooit beperkt. **Blokkeerlijst**: geweigerd tot verwijdering.
3. **Rate per adres** (standaard 40 verbindingen / 10 s): daarboven wordt het adres geblokkeerd voor de gekozen duur
   (standaard 60 min).
4. **Rate per prefix**, /24 in IPv4, /64 in IPv6.
5. **Globaal budget** van toegelaten verbindingen per seconde: de processor raakt nooit overbelast.
6. **Doelnaam**: een verbinding die niet op de naam van de machine gericht is, wordt geweigerd.

Het `*.ts.net`-certificaat van de slagboom wordt bij Tailscale aangevraagd, elke dag gecontroleerd en 30 dagen vóór
het verloopt live vernieuwd. De **observatiemodus** telt alles zonder iets te weigeren.

### De groeperingen (vingerafdrukken, AS, landen)

Bij een aanval vanaf verspreide adressen zien de regels per adres elk adres maar één keer. De slagboom deelt daarom
elke client ook in op zijn **JA4-vingerafdruk**, zijn **AS** en zijn **land**, en telt de rate van elke groep.

- **Automatische aanvalsmodus**: boven 80 inkomende verbindingen per seconde (instelbaar) schakelt de slagboom
  zelf over naar de aanvalsmodus, en verlaat die na 5 minuten rust.
- Alleen in de aanvalsmodus: een onbekende vingerafdruk die explodeert, een AS van een hostingbedrijf of cloud (lijst
  aanpasbaar) of een land uit uw lijst (standaard leeg) dat zijn rate overschrijdt, wordt geweigerd.
- **Gangbare browsers** (Chrome, Edge, Firefox) worden nooit door deze regels geraakt; **bekende clients**
  (toegelaten in de laatste 24 uur) gaan vóór het globale budget.
- **Leerfase**: gedurende 7 dagen leert de slagboom de gebruikelijke vingerafdrukken van uw site (nooit tijdens een
  aanval); de groeperingen blijven tot dan in observatiemodus.
- Buiten een aanval wordt één op de tien verbindingen ingedeeld; tijdens een aanval allemaal.
- De AS- / landendatabase is **DB-IP Lite**, één keer per maand gedownload en bijgewerkt.

### Het overleven

- **Inperking**: een apart aanvullend bestand begrenst `tailscaled` (bijvoorbeeld tot één volle kern op een machine
  met 4 threads) en verlaagt zijn prioriteit. Uw eigen configuratie wordt nooit gewijzigd.
- **Stroomonderbreker**: wanneer `tailscaled` boven de CPU-drempel blijft (standaard 80 % van een kern gedurende
  60 s) of de temperatuur 85 °C bereikt, stelt omega-tail voor om Funnel 10 minuten uit te schakelen (automatisch
  weer ingeschakeld, ongewijzigd, ook als omega-tail gesloten is), het volledig uit te schakelen, of te wachten. Het
  tailnet wordt nooit verbroken.
- **Automatische bewaking** (standaard uitgeschakeld): een dienst onder uw account schakelt Funnel zelf uit na drie
  overschrijdingen, de eerste keer 15 minuten, de tweede keer 30, daarna een uur, en schakelt het zelf weer in.

### Het schild van de WireGuard-poort

`tailscaled` verbruikt ongeveer één processorkern per 100 000 pakketten per seconde die op zijn UDP-poort binnenkomen,
zelfs als ze ongeldig zijn. Het schild is een nftables-tabel die ervoor wordt geplaatst, op de netwerkkaarten:

- **bekende peers** (degenen naar wie `tailscaled` schrijft) worden nooit beperkt;
- handshakes worden beperkt tot 20 per seconde per bron;
- de andere bronnen hebben een budget (elk 500 pakketten per seconde, 5 000 in totaal);
- pakketten die geen WireGuard zijn, worden geweigerd.

Het wordt eerst in **observatie** geplaatst, daarna **actief**. Als het via omega-connect gekoppeld is, kan
**omega-fire** (3.7.0 of nieuwer) het in plaats van omega-tail plaatsen en beheren: het is dezelfde tabel, die van
eigenaar wisselt zonder te worden aangeraakt.

[↑ Inhoud](#inhoud)

---

## Metingen

De keuzes van omega-tail zijn gebaseerd op metingen, op machines van dezelfde generatie als de machines die het
beschermt (processors van 2010 tot 2016, meestal zonder AES-versnelling).

| Meting | Resultaat |
|---|---|
| Aandeel van TLS in de kosten van een verbinding via standaard-Funnel | ongeveer 80 % |
| Kosten van een door de slagboom **geweigerde** verbinding, vergeleken met standaard-Funnel | **4,6 keer minder** |
| Kosten van een door de slagboom **toegelaten** verbinding, vergeleken met standaard-Funnel | **2 keer minder** |
| Doorvoer met de slagboom, verbindingen open gehouden (vergeleken met een TLS in Go zoals die van `tailscaled`) | **+15 %** verzoeken, −20 % CPU |
| WireGuard-schild: stroom die een hele kern van `tailscaled` kostte | **1 %** van een kern |
| Geheugen van de diensten (slagboom, bewaking, schild) | ongeveer 67 MB |

De slagboom verslechtert de doorvoer van een site dus niet: op deze machines is het de versleuteling zelf die
begrenst, met of zonder omega-tail, en in productie loopt Funnel sowieso via de relays van Tailscale en via de router.

[↑ Inhoud](#inhoud)

---

## Architectuur

```text
src/omega_tail/
├── app/              Compositieroot: voegt de lagen samen, startpunt (interface, opdrachtregel)
├── core/             Gedeelde constanten
├── domain/           Pure domeinlogica: regels van de slagboom, waarschuwingen, stroomonderbreker, bewaking, blokkeerlijst…
├── application/      Use cases: publicatie, firewall, overleven, rapport, instellingen
├── ports/            Contracten (Protocol) die de applicatie verwacht
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, logs, exports, Lua-scripts
├── interfaces/       tui/ (Textual), cli/ (opdrachtregel), shared/ (help, rapport, presentatie)
└── shared/           Talen (gettext)
```

### Ontwerpprincipes

- `domain/` bevat geen lees- of schrijfbewerkingen: alles daarin is zonder machine testbaar.
- `application/` orkestreert de use cases via het domein en de ports; de interface en de opdrachtregel roepen
  dezelfde use cases aan.
- Alleen `infrastructure.commands` en `infrastructure.privileged` voeren commando's uit; de interface doet dat nooit
  rechtstreeks. Deze regels worden automatisch gecontroleerd (import-linter).
- De interface steunt op [omega-lib](https://github.com/kraynux), de bibliotheek die de hele OMEGA-suite deelt
  (thema's, terminaldetectie, talen, contact en ondersteuning, WireGuard-schild). Ze is niet op PyPI gepubliceerd:
  ze wordt meegeleverd in het archief (`vendor/omega-lib/`).
- Elke trage aanroep (Tailscale, HAProxy, schijf, netwerk) draait als achtergrondtaak: de interface bevriest nooit.

[↑ Inhoud](#inhoud)

---

## Vereisten

### Systeem

- Linux, elke distributie (getest op Arch Linux en afgeleiden).
- Python 3.10 of hoger, met de module `venv`.
- Een init-systeem: **systemd**, **OpenRC** of **runit**.
- `sudo` voor de acties die de machine wijzigen (per actie gevraagd, nooit bij het starten).
- Een terminal van minstens 80×24 (zie [Thema's en terminals](#themas-en-terminals)).

### Tailscale

- **Tailscale** geïnstalleerd en verbonden (client `tailscale` en dienst `tailscaled`); getest met versie 1.104.
- Voor Funnel: MagicDNS, HTTPS-certificaten en Funnel toegestaan in de console van Tailscale (zie
  [Wat Tailscale moet toestaan](#wat-tailscale-moet-toestaan-beheerconsole)).

### Python-afhankelijkheden

Door `install.sh` geïnstalleerd in een virtuele omgeving:

- `textual`: de interface.
- `omega-lib`: gedeelde bibliotheek van de OMEGA-suite, meegeleverd in het archief.

### Verplichte en optionele componenten

omega-tail detecteert wat aanwezig is en activeert alleen wat bruikbaar is.

| Component | Rol | Status |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Alles wat omega-tail aanstuurt | **Verplicht** |
| Python 3.10+, `textual`, `omega-lib` | De applicatie | **Verplicht** |
| systemd, OpenRC of runit | Diensten van de slagboom, de bewaking, het schild | **Verplicht** (een van de drie) |
| HAProxy 3.x | De slagboom van de Funnel-firewall | Optioneel (te installeren vanuit omega-tail) |
| HAProxy met Lua | De groeperingen (vingerafdrukken, AS, landen) | Optioneel (het geval bij gangbare distributies) |
| nftables (kernel met `nft_limit`) | Het schild van de WireGuard-poort | Optioneel |
| Lezen van het systeemjournaal (groep `systemd-journal`, `adm` of `wheel`) | Logs, rapport van de aanvallen | Aanbevolen |
| Browser en bureaublad | „Exports bekijken” in de browser (anders weergave in omega-tail) | Optioneel |
| omega-connect | Register, synchronisatie, updates van de suite | Optioneel |
| omega-fire 3.7.0+ | Beheer van het WireGuard-schild vanuit omega-fire | Optioneel |

[↑ Inhoud](#inhoud)

---

## Installatie

Het officiële archief wordt geleverd in `.tar.gz`-formaat. Controleer vóór de installatie de integriteit ervan met
het bestand `sha.txt` dat ernaast is gepubliceerd:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Deze drie methoden zijn bedoeld voor een eerste installatie.** Als `~/omega-tail` al bestaat, gebruik dan de
> sectie [Bijwerken](#bijwerken). Voer deze commando's nooit opnieuw uit vanuit een bestaande map
> `omega-tail`: `tar` zou een geneste `omega-tail/omega-tail/` aanmaken.

Geen enkele installatiestap vraagt om rootrechten: omega-tail wordt als gewone gebruiker gestart.

### Methode 1 — installatiescript

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ U lijkt zich al in een omega-tail-map te bevinden — zie de sectie Bijwerken in de README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Hier al uitgepakt, stap overgeslagen." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail bestaat al, verplaatsen overgeslagen." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

Het script maakt de virtuele omgeving aan, installeert de afhankelijkheden (eerst de meegeleverde omega-lib), maakt
de starters uitvoerbaar, schrijft het installatietoken dat omega-connect leest en stelt de alias `omega-tail` voor.
Het kan zonder risico opnieuw worden uitgevoerd.

### Methode 2 — robuuste volledige installatie

Dit commando kan opnieuw worden uitgevoerd: het slaat stappen over die al zijn uitgevoerd.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ U lijkt zich al in een omega-tail-map te bevinden — zie de sectie Bijwerken in de README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail bestaat al, uitpakken overgeslagen." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv bestaat al, stap overgeslagen." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail geïnstalleerd. Start ./omega-tail.sh."
```

### Methode 3 — gedetailleerde installatie

```bash
# 0. Controleren dat er niet vanuit een bestaande omega-tail wordt gestart
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ U lijkt zich al in een omega-tail-map te bevinden — zie de sectie Bijwerken in de README." >&2; exit 1; }

# 1. Uitpakken
[ -d omega-tail ] && echo "ℹ️ Hier al uitgepakt, stap overgeslagen." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Naar de homemap verplaatsen
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail bestaat al, verplaatsen overgeslagen." || mv omega-tail ~/

# 3. Het project openen
cd ~/omega-tail/

# 4. De virtuele omgeving aanmaken
[ -f .venv/bin/activate ] && echo "ℹ️ .venv bestaat al, aanmaken overgeslagen." || python3 -m venv .venv

# 5. De afhankelijkheden installeren (eerst de meegeleverde omega-lib)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. De starters uitvoerbaar maken
chmod +x omega-tail.sh install.sh

# 7. Het installatietoken schrijven (gelezen door omega-connect; optioneel)
./omega-tail.sh synchro jeton

# 8. Starten
./omega-tail.sh
```

Op Debian, Ubuntu en afgeleiden wordt de module `venv` niet altijd met Python meegeïnstalleerd:
`sudo apt install python3-venv`.

### Bijwerken

De diensten van omega-tail (slagboom, bewaking) gebruiken de bestanden in `~/omega-tail/var/`. Een update moet deze
map dus **op zijn plaats laten**: het archief bevat geen `var/` en wordt over de bestaande installatie heen
uitgepakt.

Vanuit de map die het archief bevat, **niet `~/omega-tail`**:

```bash
# 1. De huidige installatie back-uppen (inclusief var/)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. De nieuwe versie eroverheen uitpakken (var/ blijft behouden)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Opnieuw installeren (afhankelijkheden, starters, installatietoken)
cd ~/omega-tail
./install.sh

# 4. omega-tail opnieuw starten
./omega-tail.sh
```

Als de slagboom actief is, genereert **Funnel-firewall → „Regels toepassen”** de configuratie live opnieuw met de
nieuwe versie. Als de automatische bewaking is ingeschakeld, herstart **Overleven → „Bewaking activeren”** haar met
de nieuwe code. omega-connect kan de update ook uitvoeren (scherm Updater).

### Bash- of Zsh-alias

`install.sh` stelt de alias voor. Om hem met de hand toe te voegen:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

De alias heet `omega-tail`, en niet `tail`, om het systeemcommando `tail` niet te verbergen.

[↑ Inhoud](#inhoud)

---

## Gebruik

### Starten

```bash
cd ~/omega-tail
./omega-tail.sh

# of eenvoudig, als de alias is aangemaakt:
omega-tail
```

De starter vraagt geen verhoogde rechten: omega-tail draait onder uw account, en sudo wordt alleen gevraagd door de
acties die het nodig hebben, in de terminal, met het commando vooraf getoond.

### Aanbevolen eerste stappen

Om een via Funnel gepubliceerde site te beschermen, in deze volgorde:

1. **Dashboard**: de waarschuwingen lezen; **Operator worden** (één keer, via sudo) om Tailscale zonder sudo in te
   stellen.
2. **Overleven → Inperking toepassen**: `tailscaled` kan niet meer de hele machine opeisen.
3. **Publicatie**: de site publiceren via **HTTPS op poort 443**, pad `/`, en daarna de **end-to-end-test** doen.
4. **Funnel-firewall → HAProxy installeren**, daarna **Bescherming activeren**, eerst in **observatiemodus**.
5. Enkele dagen later, **Aanvallen en beslissingen**: als de tellers alleen misbruik tonen, de slagboom in de modus
   **normaal** zetten.
6. De **groeperingen** 7 dagen laten leren in observatiemodus, en ze daarna op **toegepast** zetten.
7. **Overleven → Schild van de WireGuard-poort**: in observatie plaatsen, daarna op actief zetten.
8. Voor een machine zonder iemand achter het scherm: **Overleven → Bewaking activeren**.

### Talen van de interface

17 talen: Frans, Engels, Spaans, Portugees (Brazilië), Italiaans, Duits, Nederlands, Pools, Russisch, Chinees,
Vietnamees, Thai, Indonesisch, Japans, Koreaans, Hindi, Arabisch.

- Keuze in de instellingen (toets `s`, « Langue / Language », een label dat nooit wordt vertaald), toegepast door
  alleen de interface opnieuw te starten.
- Eenmalig: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- In de Linux-tekstconsole (TTY) worden talen waarvan het schrift in de consolelettertypen ontbreekt, voor de sessie
  in het Engels weergegeven; Arabisch wordt van rechts naar links weergegeven.
- De **taal van de exports** (rapport, blokkeerlijst, logs) wordt apart ingesteld, standaard „Zoals de interface”.

### Contact en ondersteuning

De help (toets `a`) biedt een scherm **Contact en ondersteuning**:

- *Trakteer op een koffie* (PayPal-pagina van de ontwikkelaar);
- *Contact opnemen met ondersteuning* (e-mailadres en formulier van de website, leesbaar weergegeven);
- *Mij aanmelden als gebruiker (anoniem)*;
- *Updates controleren*.

De aanmelding is vrijwillig, standaard uitgeschakeld en wordt maar één keer verzonden. Ze dient alleen om de
gebruikers te tellen en, als u dat wilt, hun continent of land (gesloten lijsten, nooit vrije tekst). Ze verstuurt
een willekeurig gekozen sleutel, de naam van de software (`omega-tail`) en de versie ervan, nooit een naam, een
machinenaam, een instelling of een adres van het tailnet. Intrekken kan op elk moment vanuit hetzelfde scherm (*Mij
niet meer aanmelden*). De controle op updates leest alleen de lijst van de op de website gepubliceerde versies, en
nooit zonder klik.

### Koppelingen met de andere omega-tools

- **omega-connect**: `install.sh` schrijft een installatietoken (`var/omega-jeton.json`) dat de tool en de versie
  ervan beschrijft, zonder iets uit te voeren. omega-connect gebruikt het voor het Register, de synchronisatie, de
  reparatie, de updates en de installatie. `./omega-tail.sh synchro jeton` schrijft het met de hand opnieuw.
- **omega-fire** (3.7.0 of nieuwer), gekoppeld via omega-connect, kan het schild van de WireGuard-poort plaatsen en
  beheren; de regellijst van omega-fire toont het met de herkomst omega-tail.

### Opdrachtregel

Alle commando's worden geschreven als `./omega-tail.sh …` (of `omega-tail …` met de alias):

| Commando | Rol |
|---|---|
| `omega-tail` | De interface |
| `omega-tail etat [--format json]` | Toestand van Tailscale, van de machine en waarschuwingen, als tekst of voor een script |
| `omega-tail aide` | De volledige help als tekst |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | Het rapport, weergegeven of opgeslagen |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Funnel uitschakelen of weer inschakelen |
| `omega-tail veille etat` | Toestand van de automatische bewaking en de laatste regels ervan |
| `omega-tail porte etat` | Toestand van de slagboom en tellers |
| `omega-tail porte certificat [--si-besoin]` | Het `*.ts.net`-certificaat van de slagboom vernieuwen |
| `omega-tail porte groupes` | Groeperingen: aanvalsmodus, vingerafdrukken, AS, landen |
| `omega-tail porte base` | De AS- / landendatabase bijwerken |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Een adres of netwerk blokkeren (blokkeerlijst met `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Deblokkeren |
| `omega-tail porte confiance ADRESSE` | Als vertrouwd markeren |
| `omega-tail synchro jeton` | Het installatietoken schrijven (omega-connect) |
| `omega-tail --version` | De versie |

### Algemeen verloop

1. Opstartscherm, daarna het hoofdmenu in twee kolommen (TAILSCALE en BESCHERMING).
2. Onder de titel van elk scherm vat de **statusbalk** alles samen: dienst, CPU van de machine en van `tailscaled`,
   temperatuur, geheugen, Funnel, firewall, bewaking, verbinding. Hij wordt elke 5 seconden opnieuw gelezen.
3. Elke actie die de machine wijzigt, toont haar commando en vraagt daarna om bevestiging; sudo wordt in de terminal
   ingevoerd, waarna de interface terugkeert.
4. Gevoelige acties (definitief afmelden, volledig opschonen van de blokkeerlijst) vragen om een woord in te typen.
5. Het resultaat wordt in één regel getoond, gecontroleerd aan de hand van de opnieuw gelezen toestand.

### Navigatie

- Pijltjes omhoog / omlaag: van het ene element naar het andere gaan (regels van een tabel, knoppen).
- Tab / Shift+Tab: van de ene zone van het scherm naar de andere gaan.
- Enter of klik: de gekozen knop activeren; in de tabel met waarschuwingen „Oplossen”.
- `Esc`: terug naar het vorige scherm (in het menu: afsluiten).
- `a`: de help, vanuit elk scherm.
- `s`: de instellingen, vanuit elk scherm.
- `t`: volgend thema (opgeslagen).
- `r`: het scherm opnieuw tekenen, de grootte van de terminal tonen en de toestand opnieuw lezen.
- `q`: afsluiten, met bevestiging.
- `Ctrl+P`: commando's (thema, schermafbeelding als SVG in de map voor schermafbeeldingen, afsluiten).

[↑ Inhoud](#inhoud)

---

## Thema's en terminals

Tien `omega-*`-thema's worden gedeeld met de rest van de OMEGA-suite:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Wissel tussen de thema's met `t`, of kies er een in de instellingen (`s`); de keuze wordt bewaard.
- De HTML-exports hebben hun eigen thema's: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail past de visuele complexiteit aan de gedetecteerde terminal aan via een **weergaveprofiel**: Volledig,
  Standaard, Beperkt of Mono (alleen ASCII).

| Minimale grootte | Profiel | Typische terminals |
|---|---|---|
| 120×32 of meer | Volledig | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 of meer | Standaard | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 of meer | Beperkt | urxvt, xterm, moderne SSH |
| kleiner dan 80×24 | Mono (alleen ASCII) | Linux-TTY, oude SSH |

Na het wijzigen van de grootte leest `r` de grootte van de terminal opnieuw; die wordt bovenaan getoond, naast het
thema.

[↑ Inhoud](#inhoud)

---

## Bestanden, diensten en compatibiliteit

### In de map van omega-tail

De hele toestand van omega-tail staat in `~/omega-tail/var/`, wordt bij het starten opnieuw aangemaakt en nooit
gepubliceerd:

```text
var/
├── settings.json         instellingen (taal, thema's, mappen, drempels, regels van de slagboom)
├── omega-jeton.json      installatietoken (omega-connect)
├── porte/                configuratie van de slagboom, certificaat, vertrouwens- en blokkeerlijst, AS- / landendatabase
├── veille/               log van de automatische bewaking
├── survie/               originelen van de gewijzigde bestanden, toestand van de stroomonderbreker
├── funnel/sauvegardes/   publicatie vóór elke wijziging (de 50 meest recente)
├── exports/              geëxporteerde rapporten, logs en lijsten
└── screenshots/          schermafbeeldingen (Ctrl+P)
```

### Op het systeem (alleen als u de betreffende bescherming activeert)

Elk bestand wordt via sudo geplaatst, met het commando getoond, en verwijderd door de omgekeerde actie in
omega-tail.

| Bestand of dienst | Geplaatst door | Verwijderd door |
|---|---|---|
| Dienst `omega-tail-porte` (systemd, OpenRC of runit) en `omega-tail-porte-certificat` (systemd-timer, of een gemarkeerde regel in uw crontab) | Bescherming activeren | Bescherming deactiveren |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (of een controlegroep buiten systemd) | Inperking toepassen | Inperking verwijderen |
| Timers `omega-tail-retablir-*` (weer inschakelen na een uitschakeling) | Stroomonderbreker | Einde van de uitschakeling |
| Dienst `omega-tail-veille` | Bewaking activeren | Bewaking deactiveren |
| Dienst `omega-bouclier-wg`, nftables-tabel, `/etc/omega-bouclier-wg/` | Schild: Plaatsen | Schild: Verwijderen |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | IP-doorsturing activeren | Verwijdering van het bestand |

Het bestand `override.conf` van `tailscaled` wordt, als het bestaat, nooit gewijzigd.

### Init-systemen

| | systemd | OpenRC | runit |
|---|---|---|---|
| Dienst `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Logs | `journalctl` | bestanden van de dienst | `svlogd`, `socklog` |
| Inperking | aanvullend systemd-bestand | controlegroep (cgroup v2) | controlegroep (cgroup v2) |
| Tijdelijke uitschakeling | systemd-timer | losgekoppeld proces onder uw account | losgekoppeld proces onder uw account |
| Slagboom, bewaking, schild | systemd-diensten | OpenRC-diensten | runit-diensten |

Buiten systemd gaat de inperking via een controlegroep verloren als `tailscaled` herstart: een waarschuwing stelt
dan voor om haar opnieuw toe te passen.

### IPv4 en IPv6

De slagboom, de lijsten, de groeperingen en het schild behandelen beide families. De getelde prefixen zijn /24 in
IPv4 en /64 in IPv6; een IPv4-adres in de vorm `::ffff:a.b.c.d` wordt behandeld als het IPv4-adres.

[↑ Inhoud](#inhoud)

---

## Beveiliging

omega-tail grijpt in op een dienst die aan internet is blootgesteld; het is ontworpen om de situatie nooit te
verergeren.

- **Nooit root**: de applicatie, de HAProxy-slagboom en de bewaking draaien onder uw account; sudo wordt alleen
  gevraagd om een dienst te plaatsen of te verwijderen, met het commando vooraf getoond.
- **Privékanalen**: de beheersockets van de slagboom hebben modus 600 in een map met 700; de synchronisatie van
  zijn tabellen loopt via een socket in dezelfde map.
- **Terugdraaien**: elke omschakeling van Funnel wordt geback-upt en gecontroleerd, en bij een mislukking wordt de
  vorige toestand teruggezet.
- **Eerst observeren**: de slagboom, de groeperingen en het schild worden in observatie geplaatst; niets wordt
  geweigerd voordat u dat hebt besloten.
- **Het tailnet wordt nooit verbroken**: de slagboom laat uw machines altijd toe, en de stroomonderbreker schakelt
  alleen Funnel uit.
- **Gecontroleerde invoer**: alleen adressen of netwerken in canonieke vorm bereiken HAProxy; de namen die de
  machines van het tailnet opgeven, worden opgeschoond voordat ze worden weergegeven.
- **Audit**: de code is geaudit (claude-security, 2026-11-25); de 7 gevonden punten, waarvan geen enkele op afstand
  door een bezoeker uitbuitbaar was, zijn dezelfde dag nog gecorrigeerd.
- Test eerst op een testmachine of in observatiemodus, en gebruik voor IPv4-tests de documentatienetwerken
  RFC 5737: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Inhoud](#inhoud)

---

## Tests en kwaliteit

De testsuite telt **179 tests**: domein, use cases, infrastructuur (met een gesimuleerde Funnel), Textual-schermen
met de echte stylesheets, init-systemen, beveiliging. De code wordt gecontroleerd door `ruff`, `mypy` en
`import-linter` (regels van de lagen). De map `tests/` zit in het archief.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

De meeste tests hebben geen Tailscale, geen HAProxy en geen root nodig.

[↑ Inhoud](#inhoud)

---

## Projectstatus

### Operationele punten

- Volledige aansturing van Tailscale: dienst, verbinding, instellingen, publicatie, netwerk, logs.
- HAProxy-slagboom vóór TLS, in productie sinds 2026-11-23, met regels, lijsten, groeperingen en aanvalsmodus.
- Overleven: inperking, stroomonderbreker, automatische bewaking.
- Schild van de WireGuard-poort, in productie sinds 2026-11-24.
- Rapport en exports in TXT, HTML, JSON.
- Compatibel met omega-connect en omega-fire.

### Bekende beperkingen

- De diensten onder OpenRC en runit zijn door de tests gedekt, maar nog niet op een echte machine gevalideerd.
- De slagboom beschermt een Funnel die via HTTPS op één enkele poort is gepubliceerd, met het pad `/`.
- De groeperingen vereisen een HAProxy die met Lua is gecompileerd; zonder Lua werkt de slagboom zonder ze.
- Het schild kan niet worden geplaatst op een kernel die is bijgewerkt zonder herstart (ontbrekende modules): het
  scherm meldt het.
- Een aanval die de internetlijn zelf verzadigt, blijft buiten het bereik van een tool die op de machine is
  geïnstalleerd.
- De doorvoer van een via Funnel gepubliceerde site blijft beperkt door de relays van Tailscale en door de router.

[↑ Inhoud](#inhoud)

---

## Verwijderen

Verwijder eerst, vanuit omega-tail, wat op het systeem is geplaatst, in deze volgorde:

1. **Funnel-firewall → Bescherming deactiveren** (Funnel wordt teruggezet zoals voorheen).
2. **Overleven → Bewaking deactiveren**.
3. **Overleven → Schild van de WireGuard-poort → Verwijderen**.
4. **Overleven → Inperking verwijderen**.

Verwijder daarna de map:

```bash
rm -rf ~/omega-tail
```

Verwijder met de hand de exports die elders zijn geplaatst, de alias `omega-tail` uit `~/.bashrc` of `~/.zshrc`,
en, als u die had geactiveerd, het bestand `/etc/sysctl.d/99-omega-tail-forwarding.conf`. Het operatorrecht van
Tailscale trekt u in met `sudo tailscale set --operator=`.

[↑ Inhoud](#inhoud)

---

## Licentie

Omega-Tail wordt verspreid onder de **MIT**-licentie. Raadpleeg het bestand [`LICENSE`](../../../LICENSE) voor de
volledige tekst.

De AS- / landendatabase gebruikt IP Geolocation by [DB-IP](https://db-ip.com), onder de licentie
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Inhoud](#inhoud)

---

> **Omega-Tail — Tailscale aansturen, Funnel beschermen.**
>
> Een TUI-interface voor Tailscale, en een slagboom die misbruik weigert vóór elke versleuteling.
