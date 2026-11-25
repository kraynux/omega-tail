<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**TAILSCALE-Steuerung mit integrierter Firewall für FUNNEL**

OMEGA-TAIL ist das Werkzeug der OMEGA-Suite, das **Tailscale** auf einem Rechner steuert und ihn **schützt**, wenn er
über **Tailscale Funnel** einen Dienst im Internet veröffentlicht.

> Entwickelt von [kraynux](https://github.com/kraynux) für [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Offizielle Seite](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/de/) · [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Oberfläche, Dokumentation, Exporte und Besucherseiten in **17 Sprachen** verfügbar — siehe [Sprachen der Oberfläche](#sprachen-der-oberfläche).  
**Sprachen:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** ist eine TUI-Anwendung (Terminal User Interface) in Python, gebaut mit
[Textual](https://textual.textualize.io/). Sie ermöglicht es, **Tailscale** im erweiterten Modus über eine
Oberfläche zu verwalten und einzustellen, ohne sich einen einzigen Befehl merken zu müssen. Außerdem fügt sie
Schutzmaßnahmen (Firewall, Eindämmung, Überleben…) für den **Funnel**-Modus hinzu, der einen Dienst des Rechners für
das gesamte Internet öffnet.

Jede Aktion, die den Rechner verändert, zeigt zuerst ihren Befehl. Das sudo-Passwort wird im Terminal eingegeben,
Aktion für Aktion, und nichts wird ohne Ihr Zutun im Hintergrund gestartet.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-tail/F.png" width="32%" />
</p>

Das Projekt folgt den Prinzipien der **Clean Architecture**, mit `app/` als Kompositionswurzel: Fachdomäne,
Orchestrierung, Infrastruktur und Oberfläche sind voneinander getrennt.

## Inhalt

- [Vorstellung](#vorstellung)
- [Tailscale und Funnel verstehen](#tailscale-und-funnel-verstehen)
- [Funktionen](#funktionen)
- [Die Schutzmaßnahmen im Detail](#die-schutzmaßnahmen-im-detail)
- [Messungen](#messungen)
- [Architektur](#architektur)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Themes und Terminals](#themes-und-terminals)
- [Dateien, Dienste und Kompatibilität](#dateien-dienste-und-kompatibilität)
- [Sicherheit](#sicherheit)
- [Tests und Qualität](#tests-und-qualität)
- [Projektstatus](#projektstatus)
- [Deinstallation](#deinstallation)
- [Lizenz](#lizenz)

---

## Vorstellung

### Warum omega-tail

Tailscale Funnel veröffentlicht einen Dienst des Rechners im Internet, ohne einen Port am Router zu öffnen: Die
Besucher kommen über die Relais von Tailscale. Das ist einfach und auf Netzwerkseite sicher, doch eine Schwachstelle
bleibt.

- **Die Kosten der Verschlüsselung.** Im Standard-Funnel-Modus führt der Dienst `tailscaled` des Rechners den
  TLS-Handshake jedes Besuchers durch. Auf einem kleinen Rechner gemessen sind das etwa **80 % der Kosten einer
  Verbindung**. Einige hundert neue Verbindungen pro Sekunde genügen, um den Prozessor auszulasten: Ein einziger
  gewöhnlicher Computer mit einem einfachen Skript kann die Website und den Rechner lahmlegen.
- **Unsichtbare Besucher.** Die üblichen Firewalls (nftables, ufw, fail2ban) sehen diese Besucher nicht: Sie kommen
  verschlüsselt durch den Tunnel von Tailscale, mit der Adresse eines Relais.
- **Verstreute Einstellungen.** Die Einstellungen von Tailscale (Operator, Ausgangsknoten, Routen, SSH, Schutzschild…)
  sind zahlreich, auf Befehle und Webkonsole verteilt, und manche können die laufende Sitzung trennen.

### Ziele

- Tailscale vollständig über eine Oberfläche steuern, mit einem erklärenden Satz zu jeder Einstellung.
- Missbräuchliche Verbindungen **vor** jeder Verschlüsselung ablehnen und dabei die echte Adresse jedes Besuchers
  sehen.
- Den Rechner unter Angriff am Laufen halten: Die Administration und die anderen Dienste bleiben erreichbar.
- Nie etwas aufzwingen: vorschlagen, den Befehl zeigen, nachfragen und rückgängig machen können.
- Auf jeder Linux-Distribution funktionieren, unter systemd, OpenRC oder runit.

### Was omega-tail leistet

- Zeigt den Zustand von Tailscale, des Rechners und der Veröffentlichungen an, mit Warnungen, die zum Bildschirm
  führen, der das Problem behebt.
- Startet, stoppt und startet `tailscaled` neu, mit einer Schutzvorrichtung, falls Ihre Sitzung über Tailscale läuft.
- Verwaltet die Verbindung, die Konten und alle Einstellungen von `tailscale set`, die vor dem Anwenden geprüft
  werden.
- Veröffentlicht, entfernt, setzt aus und testet die Dienste von Serve und Funnel, mit Sicherungen und
  Wiederherstellung.
- Zeigt die Geräte des Tailnets, ihren Pfad (direkt oder über Relais), eine Netzwerkdiagnose und die Logs.
- Setzt ein HAProxy-**Tor** zwischen Funnel und Ihre Website: Regeln pro Adresse, pro Präfix, globales Budget,
  Vertrauens- und Sperrliste, Gruppierungen nach JA4-Fingerabdruck, Herkunftsnetz (AS) und Land, automatischer
  Angriffsmodus.
- Dämmt `tailscaled` ein, schaltet Funnel vorübergehend oder vollständig ab und kann dies dank einer automatischen
  Überwachung selbstständig tun.
- Schützt den WireGuard-Port von `tailscaled` durch eine nftables-Tabelle (Schutzschild).
- Erstellt einen Bericht über den Rechner und die Angriffe der letzten 7 Tage, als TXT, HTML oder JSON.

### Was das Projekt nicht leistet

- Es ersetzt Tailscale nicht: Es steuert es.
- Es schützt nicht vor einem volumetrischen Angriff, der die Internetleitung selbst (den Router, die Verbindung)
  auslastet.
- Es verwaltet nicht die Web-Administrationskonsole von Tailscale (Zugriffsrichtlinie, Genehmigung von
  Ausgangsknoten, Aktivierung von Funnel für das Tailnet).
- Es schützt keinen Dienst, der anders als über Funnel veröffentlicht wird: Für diese Ports gibt es omega-fire.
- Es läuft nie als root und startet nichts ohne Ihre Zustimmung im Hintergrund.
- Es funktioniert weder unter Windows noch unter macOS.

[↑ Inhalt](#inhalt)

---

## Tailscale und Funnel verstehen

omega-tail setzt einige Kenntnisse über Tailscale voraus. Dieser Teil fasst sie zusammen, ohne weiteres Wissen
vorauszusetzen.

### Das Vokabular

| Begriff | Was es ist |
|---|---|
| **Tailnet** | Ihr privates Tailscale-Netz: alle Rechner, die mit demselben Konto (oder derselben Organisation) verbunden sind. Jeder Rechner erhält darin eine Adresse der Form `100.x.y.z` (Bereich 100.64.0.0/10) und eine IPv6-Adresse in `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | Der Dienst (Daemon), der auf dem Rechner läuft: Er hält den verschlüsselten WireGuard-Tunnel, den Netzwerkstack von Tailscale und, für Serve und Funnel, die Weiterleitung zu Ihren Diensten. |
| **`tailscale`** | Der Befehl, der `tailscaled` steuert (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail verwendet ihn für Sie. |
| **WireGuard** | Das Protokoll des verschlüsselten Tunnels zwischen den Rechnern. `tailscaled` lauscht dafür auf einem UDP-Port (standardmäßig 41641), der oft vom Router geöffnet wird (UPnP). |
| **DERP-Relais** | Server von Tailscale, die den Verkehr weiterleiten, wenn zwei Rechner sich nicht direkt erreichen können (schwieriges NAT). Der „direkte“ Pfad ist schneller. |
| **MagicDNS** | Die Namen der Rechner des Tailnets, in der Form `rechner.name-des-tailnets.ts.net`. |
| **Serve** | Einen lokalen Dienst (eine Website, eine API…) **nur für das Tailnet** veröffentlichen, per HTTPS mit einem gültigen `*.ts.net`-Zertifikat. |
| **Funnel** | Einen lokalen Dienst **für das gesamte Internet** veröffentlichen, unter der Adresse `https://rechner.name-des-tailnets.ts.net`. Nur die Ports 443, 8443 und 10000 können geöffnet werden. |
| **Funnel-Relais** | Die Server von Tailscale, die die Besucher aus dem Internet empfangen und in Ihr Tailnet einlassen (sie erscheinen als „funnel-ingress-node“). |
| **Operator** | Ein Linux-Konto, das Tailscale ohne sudo einstellen darf (`tailscale set --operator=…`). omega-tail schlägt es einmalig vor, per sudo. |
| **Ausgangsknoten (exit node)** | Ein Rechner des Tailnets, über den ein anderer seinen gesamten Internetverkehr leitet (wie ein VPN). Er muss in der Tailscale-Konsole genehmigt werden. |
| **Angekündigtes Subnetz (subnet router)** | Ein lokales Netz (zum Beispiel `192.168.1.0/24`), das ein Rechner für den Rest des Tailnets erreichbar macht. |
| **Schutzschild (shields up)** | Einstellung von Tailscale, die alle eingehenden Verbindungen aus dem Tailnet ablehnt. |
| **Tailscale SSH** | Ein von Tailscale bereitgestellter SSH-Server, freigegeben durch die Richtlinie des Tailnets. |
| **PROXY-v2-Header** | Ein kurzer Header am Anfang einer Verbindung, der die echte Adresse des Besuchers an den Empfänger übermittelt. |
| **JA4-Fingerabdruck** | Eine Signatur der Art, wie eine Software eine TLS-Verbindung aufbaut: Ein Browser und ein Angriffswerkzeug haben nicht dieselbe. |
| **AS (autonomes System)** | Das Herkunftsnetz einer Adresse: Internetanbieter, Hoster, Cloud. |

### Der Weg eines Besuchers

**Funnel im Standardmodus, ohne omega-tail.** `tailscaled` erledigt alles: Es entschlüsselt den WireGuard-Tunnel,
führt den TLS-Handshake des Besuchers durch und leitet die Anfrage dann per HTTP an Ihre Website weiter. Keine
Firewall des Rechners sieht den Besucher, und jede neue Verbindung kostet `tailscaled` viel.

```text
Besucher ──HTTPS──▶ Funnel-Relais ──WireGuard──▶ tailscaled (TLS + HTTP-Relais) ──HTTP──▶ Ihre Website
                    (Tailscale)                  └── alle Kosten entstehen hier
```

**Funnel mit dem Tor von omega-tail.** Funnel wechselt in den TCP-Modus: `tailscaled` macht kein TLS mehr, sondern
reicht den noch verschlüsselten Datenstrom an das Tor weiter, eingeleitet von der echten Adresse des Besuchers
(PROXY-v2-Header). Das Tor entscheidet **vor** jeder Verschlüsselung: Eine abgelehnte Verbindung kostet fast nichts,
und nur zugelassene Verbindungen werden entschlüsselt, von OpenSSL, schneller als das TLS von `tailscaled`.

```text
Besucher ──HTTPS──▶ Funnel-Relais ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                      │
                                                      ▼
                                       omega-tail-Tor (HAProxy, 127.0.0.1)
                                       ├── Ablehnung vor TLS: Sperrliste, Rate, Budget, Zielname, Gruppierungen
                                       └── zugelassen: TLS (Zertifikat *.ts.net) ──HTTP──▶ Ihre Website
```

Das Tor lauscht nur auf der lokalen Schleife (Loopback) des Rechners und läuft unter Ihrem Konto. Die Rechner Ihres
Tailnets werden immer zugelassen, vor jeder Regel: Nur die Funnel-Besucher werden gefiltert.

### Was Tailscale erlauben muss (Administrationskonsole)

Diese Einstellungen werden einmalig in der Webkonsole von Tailscale vorgenommen; omega-tail ändert sie nicht.

- **MagicDNS** und die **HTTPS-Zertifikate** für das Tailnet aktiviert (erforderlich für Serve, für Funnel und für
  das Zertifikat des Tors).
- **Funnel erlaubt** für den Rechner in der Zugriffsrichtlinie des Tailnets (Attribut `funnel`).
- Für einen Ausgangsknoten oder angekündigte Subnetze: deren **Genehmigung** in der Konsole.

[↑ Inhalt](#inhalt)

---

## Funktionen

Das Hauptmenü hat zwei Spalten mit je sechs Einträgen: **TAILSCALE** zum Steuern, **SCHUTZ** zum Verteidigen.

### TAILSCALE

#### 1. Dashboard

- **Tailscale**: Dienst, Verbindungszustand, laufende und installierte Version, Name des Rechners, Adressen, Konto,
  Geräte online, Ablauf des Schlüssels, Operator, angebotener und genutzter Ausgangsknoten, angekündigte Subnetze.
- **Rechner**: CPU des gesamten Rechners, Last pro Kern, Temperatur, Arbeitsspeicher, CPU und Arbeitsspeicher von
  `tailscaled`, Eindämmung, dann der Zustand der Schutzmaßnahmen (Funnel, Firewall und Angriffsmodus, Sperrliste,
  Überwachung, Schutzschild).
- **Veröffentlichung**: jeder veröffentlichte Port, für das Internet (Funnel) oder für das Tailnet (Serve), sein
  Modus und sein Ziel.
- **Warnungen**, von der schwersten zur leichtesten, mit „Beheben“, das den betreffenden Bildschirm öffnet. Zum
  Beispiel: Dienst gestoppt, Update installiert, aber nicht angewendet, ablaufender Schlüssel, Funnel ohne Schutz
  veröffentlicht, hohe Temperatur, `tailscaled` zu ressourcenhungrig oder nicht eingedämmt, wachsende Sperrliste.
- Werte in Grün, Orange oder Rot je nach Schwellenwerten (CPU, Last, Temperatur, Arbeitsspeicher, `tailscaled`).

#### 2. Dienst tailscaled

- Zustand aus Sicht des Init-Systems, laufende und installierte Version, Startbefehl, Ergänzungsdateien
  (Drop-ins), Eindämmung.
- **Starten**, **Stoppen**, **Neu starten** (zum Beispiel, um ein bereits installiertes Update anzuwenden).
- **Schutzvorrichtung**: Läuft Ihre Sitzung über Tailscale (SSH über das Tailnet), verlangt Stoppen eine zweite
  Bestätigung, da Sie den Dienst danach nicht mehr neu starten könnten.
- **Start korrigieren**: erkennt eine Ergänzungsdatei, die beim Start `tailscale up` ausführt und den Rechner bei der
  ersten Einstellungsänderung aus dem Tailnet werfen könnte; die Korrektur wird angezeigt und das Original
  aufbewahrt.

#### 3. Verbindung und Einstellungen

- **Anmelden**, **Abmelden**, **Konto hinzufügen**, **Konto wechseln**, **Endgültig abmelden** (Name des Rechners
  ist einzutippen).
- **Alle Einstellungen von `tailscale set`**, jede mit ihrem erklärenden Satz: Name und Spitzname des Rechners,
  Routen, DNS des Tailnets, Schutzschild, zustandsbehaftete Filterung, netfilter-Modus, Ausgangsknoten, Zugriff auf
  das lokale Netz, den Rechner als Ausgangsknoten anbieten, angekündigte Subnetze, Tailscale SSH, Weboberfläche,
  Updates, Peer-Relais, Operator.
- Während der Eingabe zeigt ein Rahmen **vorher → nachher** und den Befehl; nach dem Anwenden wird jeder neu gelesene
  Wert mit ✔ (übernommen) oder ✖ (nicht übernommen) markiert.
- Ein Hinweis warnt, wenn eine Änderung eine über Tailscale laufende Sitzung trennen kann.
- **IP-Weiterleitung**: mit einem Knopf aktiviert, wenn der Rechner als Ausgangsknoten dient oder Subnetze ankündigt.

#### 4. Veröffentlichung

- Alles, was der Rechner veröffentlicht: Port, öffentlich (Funnel) oder Tailnet (Serve), Modus, Pfad, Ziel, Schutz.
- Einen lokalen Dienst **veröffentlichen** per HTTPS, HTTP, TCP oder terminiertem TLS; **Entfernen**; **Funnel
  aussetzen** und **Funnel wiederherstellen** (unverändert).
- **Ende-zu-Ende-Test**: eine echte Verbindung, wie ein Besucher (Antwort, Zeit, Zertifikat, TLS-Version).
- **Sicherungen**: der Zustand vor jeder Änderung (die 50 neuesten), wiederherstellbar.
- Jede Änderung wird geprüft; bei einer Abweichung wird die Veröffentlichung neu aufgebaut, andernfalls wird der
  vorherige Zustand wiederhergestellt.

#### 5. Netzwerk und Geräte

- **Geräte** des Tailnets: System, online oder nicht, Pfad (direkt oder über Relais), zuletzt gesehen, Adresse,
  ausgetauschter Verkehr; die Funnel-Relais von Tailscale sind standardmäßig ausgeblendet.
- **Tailscale-Ping** (Pfad und Latenz), **Wer ist das?** (wem eine Adresse des Tailnets gehört).
- **Netzwerkdiagnose**: UDP, IPv4 / IPv6, NAT-Typ, Portöffnung durch den Router (UPnP, NAT-PMP, PCP), nächstes Relais
  und Latenzen.
- **DNS**, **Tailnet-Sperre** und **interne Zähler** von Tailscale.
- Nur lesend: Nichts auf diesem Bildschirm ändert eine Einstellung.

#### 6. Logs

- Das Log von `tailscaled` (journalctl oder außerhalb von systemd die Dateien des Dienstes) und das des Tors,
  filterbar und exportierbar.
- Jede Information hat ihre eigene Farbe aus dem Theme: Datum, Prozess, Kategorie der Meldung (Steuerung, Netzwerk,
  DNS, WireGuard-Engine), Adressen fett, Fehler in Rot, Warnungen in Orange; für das Tor Ablehnungsgrund, Gruppierung,
  AS und Land.

### SCHUTZ

#### 7. Funnel-Firewall

- **HAProxy installieren** über den Paketmanager der Distribution (pacman, apt, dnf, zypper, apk, xbps, emerge).
- **Schutz aktivieren**: Zertifikat `*.ts.net`, Listen, geprüfte Konfiguration, Dienst des Tors, Umschalten von Funnel
  und anschließender Test aus dem Internet; bei einem Fehlschlag wird die ursprüngliche Veröffentlichung sofort
  wiederhergestellt.
- **Schutz deaktivieren**: Funnel wird geprüft genau so wiederhergestellt wie zuvor.
- **Regeln**, im laufenden Betrieb angewendet, **Beobachtungsmodus**, um die Schwellenwerte risikolos einzustellen,
  **Gruppierungen** (siehe [Die Schutzmaßnahmen im Detail](#die-schutzmaßnahmen-im-detail)).
- **Datenbank aktualisieren** für AS / Länder (DB-IP Lite), in einem eigenen Prozess.

#### 8. Überleben

- **Eindämmung von `tailscaled`**: CPU-Obergrenze, Gewichtung und Priorität, Option für Vorrang des SSH-Zugangs.
- **Funnel-Schutzschalter**: Schwellenwerte für CPU und Temperatur, Abschaltung für 10 Minuten (automatische
  Wiederinbetriebnahme) oder vollständig.
- **Automatische Überwachung**: dasselbe, ohne dass jemand vor dem Bildschirm sitzt.
- **Schutzschild des WireGuard-Ports**: Knopf zu seinem Bildschirm (Beobachtung, aktiv, setzen, neu setzen,
  entfernen, übergeben).

#### 9. Angriffe und Entscheidungen

- Zähler des Tors (empfangen, vor der Verschlüsselung abgelehnt, zugelassen, laufend) und die aktivsten Adressen,
  alle 2 Sekunden neu gelesen, mit Land, AS und Zustand jeder Adresse.
- **Sperren**, **Sperrliste**, **Entsperren**, **Vertrauen**: sofort angewendet, ohne das Tor neu zu starten; die
  Benachrichtigung nennt in einer Zeile die Aktion und den Platz der Adresse.
- Ansichten **Fingerabdrücke**, **AS** und **Länder**; Zustand des Angriffsmodus und durch die Gruppierungen
  abgelehnte Verbindungen.
- **Verwaltung der Sperrliste**: vollständige Liste mit Datum der Aufnahme und Herkunft, Hinzufügen, Löschen, Import
  einer TXT-Datei (Duplikate, bereits abgedeckte Netze und Adressen des Tailnets werden aussortiert), Bereinigungen
  mit Vorschau (nach Alter, die N ältesten, ein Zeilenbereich, eine Herkunft, alles), Exporte als TXT
  (wieder importierbar), HTML und JSON. Obergrenze von 50 000 Einträgen.

#### 10. Bericht

- Alles, was omega-tail über den Rechner weiß, in Fakten: Tailscale, Veröffentlichung, Rechner, Firewall, Überleben,
  Warnungen und die **Angriffe der letzten 7 Tage**, gelesen aus dem Log des Tors.
- **Privatsphäre**: standardmäßig ohne das Tailscale-Konto und ohne die Namen und Adressen der Geräte des Tailnets,
  damit er an jemanden weitergegeben werden kann.
- Exporte als **TXT**, **HTML** (Theme nach Wahl) und **JSON**; **Exporte anzeigen** öffnet den Ordner im Browser.

#### 11. Einstellungen

- Sprache der Oberfläche und der Exporte, Theme der Oberfläche und der Exporte, Ordner für Exporte und
  Bildschirmfotos sowie deren Bereinigung.

#### 12. Hilfe

- Ein Abschnitt pro Bildschirm, die Tastenkürzel, die Befehlszeile und **Kontakt und Support**.

[↑ Inhalt](#inhalt)

---

## Die Schutzmaßnahmen im Detail

Jede Schutzmaßnahme antwortet auf eine bestimmte Bedrohung; keine wird aufgezwungen.

| Schutzmaßnahme | Wogegen | Wo |
|---|---|---|
| Tor (Regeln) | Salven von einer oder wenigen Adressen, Verbindungen, die nicht auf die Website zielen | Funnel-Firewall |
| Gruppierungen | Angriffe von verstreuten Adressen (Tausende Adressen, je eine Verbindung) | Funnel-Firewall |
| Sperrliste | Adressen und Netze, die für Angriffe bekannt sind, dauerhaft gespeichert | Angriffe und Entscheidungen |
| Eindämmung | `tailscaled`, das unter Angriff den ganzen Rechner beanspruchen würde | Überleben |
| Schutzschalter | Trotz allem ausgelasteter Rechner: Funnel vorübergehend abschalten | Überleben |
| Automatische Überwachung | Dasselbe, ohne dass jemand vor dem Bildschirm sitzt | Überleben |
| WireGuard-Schutzschild | Flut von UDP-Paketen auf dem Port von `tailscaled`, ob Funnel offen ist oder nicht | Überleben |

### Das Tor (Funnel-Firewall)

Die Regeln gelten in dieser Reihenfolge, alle vor der Verschlüsselung:

1. **Rechner des Tailnets** (100.64.0.0/10, fd7a:115c:a1e0::/48): immer zugelassen.
2. **Vertrauensliste**: nie begrenzt. **Sperrliste**: abgelehnt bis zur Entfernung.
3. **Rate pro Adresse** (standardmäßig 40 Verbindungen / 10 s): Darüber hinaus wird die Adresse für die gewählte
   Dauer gesperrt (standardmäßig 60 min).
4. **Rate pro Präfix**, /24 bei IPv4, /64 bei IPv6.
5. **Globales Budget** an zugelassenen Verbindungen pro Sekunde: Der Prozessor wird nie überlastet.
6. **Zielname**: Eine Verbindung, die nicht auf den Namen des Rechners zielt, wird abgelehnt.

Das `*.ts.net`-Zertifikat des Tors wird bei Tailscale angefordert, täglich geprüft und 30 Tage vor Ablauf im
laufenden Betrieb erneuert. Der **Beobachtungsmodus** zählt alles, ohne etwas abzulehnen.

### Die Gruppierungen (Fingerabdrücke, AS, Länder)

Bei einem Angriff von verstreuten Adressen sehen die Regeln pro Adresse jede Adresse nur einmal. Das Tor ordnet
deshalb jeden Client zusätzlich nach seinem **JA4-Fingerabdruck**, seinem **AS** und seinem **Land** ein und zählt
die Rate jeder Gruppe.

- **Automatischer Angriffsmodus**: Ab 80 eingehenden Verbindungen pro Sekunde (einstellbar) wechselt das Tor
  selbstständig in den Angriffsmodus und verlässt ihn nach 5 ruhigen Minuten wieder.
- Nur im Angriffsmodus: Ein unbekannter Fingerabdruck, der stark ansteigt, ein AS eines Hosters oder einer Cloud
  (Liste änderbar) oder ein Land Ihrer Liste (standardmäßig leer), das seine Rate überschreitet, wird abgelehnt.
- **Gängige Browser** (Chrome, Edge, Firefox) sind von diesen Regeln nie betroffen; **bekannte Clients** (in den
  letzten 24 h zugelassen) gehen dem globalen Budget vor.
- **Lernphase**: 7 Tage lang lernt das Tor die üblichen Fingerabdrücke Ihrer Website (nie während eines Angriffs);
  die Gruppierungen bleiben bis dahin im Beobachtungsmodus.
- Außerhalb eines Angriffs wird eine von zehn Verbindungen eingeordnet; bei einem Angriff alle.
- Die AS- / Länderdatenbank ist **DB-IP Lite**, einmal im Monat heruntergeladen und aktualisiert.

### Das Überleben

- **Eindämmung**: Eine eigene Ergänzungsdatei begrenzt `tailscaled` (zum Beispiel auf einen ganzen Kern bei einem
  Rechner mit 4 Threads) und senkt seine Priorität. Ihre eigene Konfiguration wird nie verändert.
- **Schutzschalter**: Bleibt `tailscaled` über der CPU-Schwelle (standardmäßig 80 % eines Kerns während 60 s) oder
  erreicht die Temperatur 85 °C, schlägt omega-tail vor, Funnel für 10 Minuten abzuschalten (automatische
  Wiederinbetriebnahme, unverändert, auch bei geschlossenem omega-tail), ihn vollständig abzuschalten oder abzuwarten.
  Das Tailnet wird nie getrennt.
- **Automatische Überwachung** (standardmäßig deaktiviert): Ein Dienst unter Ihrem Konto schaltet Funnel nach drei
  Überschreitungen selbstständig ab, beim ersten Mal 15 Minuten, beim zweiten 30, danach eine Stunde, und schaltet
  ihn selbstständig wieder ein.

### Das Schutzschild des WireGuard-Ports

`tailscaled` verbraucht etwa einen Prozessorkern für 100 000 Pakete pro Sekunde, die auf seinem UDP-Port eingehen,
selbst wenn sie ungültig sind. Das Schutzschild ist eine nftables-Tabelle, die ihm auf den Netzwerkkarten
vorgeschaltet wird:

- **bekannte Peers** (diejenigen, an die `tailscaled` schreibt) werden nie begrenzt;
- Handshakes werden auf 20 pro Sekunde und Quelle begrenzt;
- die anderen Quellen haben ein Budget (je 500 Pakete pro Sekunde, insgesamt 5 000);
- Pakete, die kein WireGuard sind, werden abgelehnt.

Es wird zuerst im **Beobachtungsmodus** gesetzt, dann **aktiv**. Ist es über omega-connect verbunden, kann
**omega-fire** (3.7.0 oder neuer) es anstelle von omega-tail setzen und verwalten: Es ist dieselbe Tabelle, die den
Besitzer wechselt, ohne angetastet zu werden.

[↑ Inhalt](#inhalt)

---

## Messungen

Die Entscheidungen von omega-tail beruhen auf Messungen auf Rechnern derselben Generation wie jene, die es schützt
(Prozessoren von 2010 bis 2016, größtenteils ohne AES-Beschleunigung).

| Messung | Ergebnis |
|---|---|
| Anteil von TLS an den Kosten einer Verbindung über Standard-Funnel | etwa 80 % |
| Kosten einer vom Tor **abgelehnten** Verbindung, verglichen mit Standard-Funnel | **4,6-mal weniger** |
| Kosten einer vom Tor **zugelassenen** Verbindung, verglichen mit Standard-Funnel | **2-mal weniger** |
| Durchsatz mit dem Tor, offen gehaltene Verbindungen (verglichen mit einem TLS in Go wie dem von `tailscaled`) | **+15 %** Anfragen, −20 % CPU |
| WireGuard-Schutzschild: Flut, die `tailscaled` einen ganzen Kern kostete | **1 %** eines Kerns |
| Arbeitsspeicher der Dienste (Tor, Überwachung, Schutzschild) | etwa 67 MB |

Das Tor verschlechtert also den Durchsatz einer Website nicht: Auf diesen Rechnern begrenzt die Verschlüsselung
selbst, mit oder ohne omega-tail, und im Produktivbetrieb läuft Funnel ohnehin über die Relais von Tailscale und über
den Router.

[↑ Inhalt](#inhalt)

---

## Architektur

```text
src/omega_tail/
├── app/              Kompositionswurzel: fügt die Schichten zusammen, Einstiegspunkt (Oberfläche, Befehlszeile)
├── core/             Gemeinsame Konstanten
├── domain/           Reine Fachlogik: Regeln des Tors, Warnungen, Schutzschalter, Überwachung, Sperrliste…
├── application/      Anwendungsfälle: Veröffentlichung, Firewall, Überleben, Bericht, Einstellungen
├── ports/            Von der Anwendung erwartete Verträge (Protocol)
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, Logs, Exporte, Lua-Skripte
├── interfaces/       tui/ (Textual), cli/ (Befehlszeile), shared/ (Hilfe, Bericht, Darstellung)
└── shared/           Sprachen (gettext)
```

### Gestaltungsprinzipien

- `domain/` enthält weder Lese- noch Schreibzugriffe: Alles darin ist ohne Rechner testbar.
- `application/` orchestriert die Anwendungsfälle über die Domäne und die Ports; Oberfläche und Befehlszeile rufen
  dieselben Anwendungsfälle auf.
- Nur `infrastructure.commands` und `infrastructure.privileged` führen Befehle aus; die Oberfläche tut das nie
  direkt. Diese Regeln werden automatisch geprüft (import-linter).
- Die Oberfläche stützt sich auf [omega-lib](https://github.com/kraynux), die gemeinsame Bibliothek der gesamten
  OMEGA-Suite (Themes, Terminalerkennung, Sprachen, Kontakt und Support, WireGuard-Schutzschild). Sie ist nicht auf
  PyPI veröffentlicht: Sie ist im Archiv enthalten (`vendor/omega-lib/`).
- Jeder langsame Aufruf (Tailscale, HAProxy, Festplatte, Netzwerk) läuft als Hintergrundaufgabe: Die Oberfläche
  friert nie ein.

[↑ Inhalt](#inhalt)

---

## Voraussetzungen

### System

- Linux, jede Distribution (getestet unter Arch Linux und Derivaten).
- Python 3.10 oder höher, mit dem Modul `venv`.
- Ein Init-System: **systemd**, **OpenRC** oder **runit**.
- `sudo` für die Aktionen, die den Rechner verändern (Aktion für Aktion abgefragt, nie beim Start).
- Ein Terminal von mindestens 80×24 (siehe [Themes und Terminals](#themes-und-terminals)).

### Tailscale

- **Tailscale** installiert und verbunden (Client `tailscale` und Dienst `tailscaled`); getestet mit Version 1.104.
- Für Funnel: MagicDNS, HTTPS-Zertifikate und Funnel in der Tailscale-Konsole erlaubt (siehe
  [Was Tailscale erlauben muss](#was-tailscale-erlauben-muss-administrationskonsole)).

### Python-Abhängigkeiten

Von `install.sh` in einer virtuellen Umgebung installiert:

- `textual`: die Oberfläche.
- `omega-lib`: gemeinsame Bibliothek der OMEGA-Suite, im Archiv enthalten.

### Pflicht- und optionale Komponenten

omega-tail erkennt, was vorhanden ist, und aktiviert nur, was nutzbar ist.

| Komponente | Rolle | Status |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Alles, was omega-tail steuert | **Pflicht** |
| Python 3.10+, `textual`, `omega-lib` | Die Anwendung | **Pflicht** |
| systemd, OpenRC oder runit | Dienste des Tors, der Überwachung, des Schutzschilds | **Pflicht** (eines der drei) |
| HAProxy 3.x | Das Tor der Funnel-Firewall | Optional (aus omega-tail installierbar) |
| HAProxy mit Lua | Die Gruppierungen (Fingerabdrücke, AS, Länder) | Optional (Regelfall bei gängigen Distributionen) |
| nftables (Kernel mit `nft_limit`) | Das Schutzschild des WireGuard-Ports | Optional |
| Lesen des Systemjournals (Gruppe `systemd-journal`, `adm` oder `wheel`) | Logs, Angriffsbericht | Empfohlen |
| Browser und Desktop | „Exporte anzeigen“ im Browser (sonst Anzeige in omega-tail) | Optional |
| omega-connect | Registry, Synchronisation, Updates der Suite | Optional |
| omega-fire 3.7.0+ | Verwaltung des WireGuard-Schutzschilds aus omega-fire | Optional |

[↑ Inhalt](#inhalt)

---

## Installation

Das offizielle Archiv wird im Format `.tar.gz` bereitgestellt. Prüfen Sie vor der Installation seine Integrität mit
der daneben veröffentlichten Datei `sha.txt`:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Diese drei Methoden dienen einer Erstinstallation.** Existiert `~/omega-tail` bereits, verwenden Sie den
> Abschnitt [Aktualisierung](#aktualisierung). Führen Sie diese Befehle nie aus einem bestehenden
> `omega-tail`-Ordner heraus aus: `tar` würde ein verschachteltes `omega-tail/omega-tail/` erzeugen.

Kein Installationsschritt erfordert root-Rechte: omega-tail wird als normaler Benutzer gestartet.

### Methode 1 — Installationsskript

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Sie scheinen sich bereits in einem omega-tail-Ordner zu befinden — siehe den Abschnitt Aktualisierung im README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Hier bereits entpackt, Schritt übersprungen." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail existiert bereits, Verschieben übersprungen." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

Das Skript erstellt die virtuelle Umgebung, installiert die Abhängigkeiten (zuerst die enthaltene omega-lib), macht
die Starter ausführbar, schreibt das von omega-connect gelesene Installations-Token und schlägt den Alias
`omega-tail` vor. Es kann gefahrlos erneut ausgeführt werden.

### Methode 2 — robuste Komplettinstallation

Dieser Befehl kann erneut ausgeführt werden: Er überspringt bereits erledigte Schritte.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Sie scheinen sich bereits in einem omega-tail-Ordner zu befinden — siehe den Abschnitt Aktualisierung im README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail existiert bereits, Entpacken übersprungen." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv existiert bereits, Schritt übersprungen." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail installiert. Starten Sie ./omega-tail.sh."
```

### Methode 3 — ausführliche Installation

```bash
# 0. Prüfen, dass nicht aus einem bestehenden omega-tail heraus gestartet wird
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Sie scheinen sich bereits in einem omega-tail-Ordner zu befinden — siehe den Abschnitt Aktualisierung im README." >&2; exit 1; }

# 1. Entpacken
[ -d omega-tail ] && echo "ℹ️ Hier bereits entpackt, Schritt übersprungen." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. In das Home-Verzeichnis verschieben
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail existiert bereits, Verschieben übersprungen." || mv omega-tail ~/

# 3. In das Projekt wechseln
cd ~/omega-tail/

# 4. Die virtuelle Umgebung erstellen
[ -f .venv/bin/activate ] && echo "ℹ️ .venv existiert bereits, Erstellung übersprungen." || python3 -m venv .venv

# 5. Die Abhängigkeiten installieren (zuerst die enthaltene omega-lib)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Die Starter ausführbar machen
chmod +x omega-tail.sh install.sh

# 7. Das Installations-Token schreiben (von omega-connect gelesen; optional)
./omega-tail.sh synchro jeton

# 8. Starten
./omega-tail.sh
```

Unter Debian, Ubuntu und Derivaten wird das Modul `venv` nicht immer mit Python installiert:
`sudo apt install python3-venv`.

### Aktualisierung

Die Dienste von omega-tail (Tor, Überwachung) verwenden die Dateien in `~/omega-tail/var/`. Eine Aktualisierung muss
diesen Ordner daher **an Ort und Stelle belassen**: Das Archiv enthält kein `var/` und wird über die bestehende
Installation entpackt.

Aus dem Ordner, der das Archiv enthält, **nicht aus `~/omega-tail`**:

```bash
# 1. Die aktuelle Installation sichern (einschließlich var/)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Die neue Version darüber entpacken (var/ bleibt erhalten)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Neu installieren (Abhängigkeiten, Starter, Installations-Token)
cd ~/omega-tail
./install.sh

# 4. omega-tail neu starten
./omega-tail.sh
```

Ist das Tor aktiv, erzeugt **Funnel-Firewall → „Regeln anwenden“** seine Konfiguration mit der neuen Version im
laufenden Betrieb neu. Ist die automatische Überwachung aktiviert, startet **Überleben → „Überwachung aktivieren“** sie
mit dem neuen Code neu. omega-connect kann die Aktualisierung ebenfalls durchführen (Bildschirm Updater).

### Bash- oder Zsh-Alias

`install.sh` schlägt den Alias vor. Um ihn von Hand hinzuzufügen:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

Der Alias heißt `omega-tail` und nicht `tail`, um den Systembefehl `tail` nicht zu verdecken.

[↑ Inhalt](#inhalt)

---

## Verwendung

### Start

```bash
cd ~/omega-tail
./omega-tail.sh

# oder einfach, wenn der Alias erstellt wurde:
omega-tail
```

Der Starter verlangt keine Rechteerhöhung: omega-tail läuft unter Ihrem Konto, und sudo wird nur von den Aktionen
verlangt, die es benötigen, im Terminal, mit vorher angezeigtem Befehl.

### Empfohlene erste Schritte

Um eine über Funnel veröffentlichte Website zu schützen, in dieser Reihenfolge:

1. **Dashboard**: die Warnungen lesen; **Operator werden** (einmalig, per sudo), um Tailscale ohne sudo einzustellen.
2. **Überleben → Eindämmung anwenden**: `tailscaled` kann nicht mehr den ganzen Rechner beanspruchen.
3. **Veröffentlichung**: die Website per **HTTPS auf Port 443** veröffentlichen, Pfad `/`, dann den
   **Ende-zu-Ende-Test** durchführen.
4. **Funnel-Firewall → HAProxy installieren**, dann **Schutz aktivieren**, zunächst im **Beobachtungsmodus**.
5. Einige Tage später, **Angriffe und Entscheidungen**: Zeigen die Zähler nur Missbrauch, das Tor in den Modus
   **normal** schalten.
6. Die **Gruppierungen** 7 Tage im Beobachtungsmodus lernen lassen, dann auf **angewendet** umstellen.
7. **Überleben → Schutzschild des WireGuard-Ports**: im Beobachtungsmodus setzen, dann auf aktiv umstellen.
8. Für einen Rechner, vor dem niemand sitzt: **Überleben → Überwachung aktivieren**.

### Sprachen der Oberfläche

17 Sprachen: Französisch, Englisch, Spanisch, Portugiesisch (Brasilien), Italienisch, Deutsch, Niederländisch,
Polnisch, Russisch, Chinesisch, Vietnamesisch, Thailändisch, Indonesisch, Japanisch, Koreanisch, Hindi, Arabisch.

- Auswahl in den Einstellungen (Taste `s`, « Langue / Language », eine nie übersetzte Beschriftung), angewendet durch
  einen Neustart nur der Oberfläche.
- Einmalig: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- In der Linux-Textkonsole (TTY) werden Sprachen, deren Schrift in den Konsolenschriften fehlt, für die Sitzung auf
  Englisch angezeigt; Arabisch wird von rechts nach links angezeigt.
- Die **Sprache der Exporte** (Bericht, Sperrliste, Logs) wird getrennt eingestellt, standardmäßig „Wie die
  Oberfläche“.

### Kontakt und Support

Die Hilfe (Taste `a`) bietet einen Bildschirm **Kontakt und Support**:

- *Einen Kaffee spendieren* (PayPal-Seite des Entwicklers);
- *Support kontaktieren* (E-Mail-Adresse und Kontaktformular der Website, im Klartext angezeigt);
- *Mich als Nutzer melden (anonym)*;
- *Updates prüfen*.

Die Meldung ist freiwillig, standardmäßig deaktiviert und wird nur ein einziges Mal gesendet. Sie dient nur dazu, die
Nutzer zu zählen und, falls gewünscht, ihren Kontinent oder ihr Land (geschlossene Listen, nie Freitext). Sie sendet
einen zufällig erzeugten Schlüssel, den Namen der Software (`omega-tail`) und ihre Version, nie einen Namen, einen
Rechnernamen, eine Einstellung oder eine Adresse des Tailnets. Rücknahme jederzeit über denselben Bildschirm (*Mich
nicht mehr melden*). Die Update-Prüfung liest nur die Liste der auf der Website veröffentlichten Versionen, und nie
ohne Klick.

### Verbindungen zu den anderen omega-Werkzeugen

- **omega-connect**: `install.sh` schreibt ein Installations-Token (`var/omega-jeton.json`), das das Werkzeug und
  seine Version beschreibt, ohne etwas auszuführen. omega-connect verwendet es für die Registry, die Synchronisation,
  die Reparatur, die Updates und die Installation. `./omega-tail.sh synchro jeton` schreibt es von Hand neu.
- **omega-fire** (3.7.0 oder neuer), über omega-connect verbunden, kann das Schutzschild des WireGuard-Ports setzen
  und verwalten; seine Regelliste zeigt es mit der Herkunft omega-tail an.

### Befehlszeile

Alle Befehle werden als `./omega-tail.sh …` geschrieben (oder `omega-tail …` mit dem Alias):

| Befehl | Rolle |
|---|---|
| `omega-tail` | Die Oberfläche |
| `omega-tail etat [--format json]` | Zustand von Tailscale, des Rechners und Warnungen, als Text oder für ein Skript |
| `omega-tail aide` | Die vollständige Hilfe als Text |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | Der Bericht, angezeigt oder gespeichert |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Funnel abschalten oder wieder einschalten |
| `omega-tail veille etat` | Zustand der automatischen Überwachung und ihre letzten Zeilen |
| `omega-tail porte etat` | Zustand des Tors und Zähler |
| `omega-tail porte certificat [--si-besoin]` | Das `*.ts.net`-Zertifikat des Tors erneuern |
| `omega-tail porte groupes` | Gruppierungen: Angriffsmodus, Fingerabdrücke, AS, Länder |
| `omega-tail porte base` | Die AS- / Länderdatenbank aktualisieren |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Eine Adresse oder ein Netz sperren (Sperrliste mit `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Entsperren |
| `omega-tail porte confiance ADRESSE` | Als vertrauenswürdig markieren |
| `omega-tail synchro jeton` | Das Installations-Token schreiben (omega-connect) |
| `omega-tail --version` | Die Version |

### Allgemeiner Ablauf

1. Startbildschirm, danach das Hauptmenü in zwei Spalten (TAILSCALE und SCHUTZ).
2. Unter dem Titel jedes Bildschirms fasst die **Statusleiste** alles zusammen: Dienst, CPU des Rechners und von
   `tailscaled`, Temperatur, Arbeitsspeicher, Funnel, Firewall, Überwachung, Verbindung. Sie wird alle 5 Sekunden
   neu gelesen.
3. Jede Aktion, die den Rechner verändert, zeigt ihren Befehl und bittet dann um Bestätigung; sudo wird im Terminal
   eingegeben, danach kehrt die Oberfläche zurück.
4. Sensible Aktionen (endgültiges Abmelden, vollständige Bereinigung der Sperrliste) verlangen das Eintippen eines
   Wortes.
5. Das Ergebnis wird in einer Zeile angezeigt, geprüft anhand des neu gelesenen Zustands.

### Navigation

- Pfeiltasten auf / ab: von einem Element zum nächsten wechseln (Tabellenzeilen, Knöpfe).
- Tab / Umschalt+Tab: von einem Bereich des Bildschirms zum nächsten wechseln.
- Eingabe oder Klick: den gewählten Knopf auslösen; in der Warnungstabelle „Beheben“.
- `Esc`: zum vorherigen Bildschirm zurückkehren (im Menü: beenden).
- `a`: die Hilfe, von jedem Bildschirm aus.
- `s`: die Einstellungen, von jedem Bildschirm aus.
- `t`: nächstes Theme (gespeichert).
- `r`: den Bildschirm neu zeichnen, die Terminalgröße anzeigen und den Zustand neu lesen.
- `q`: beenden, mit Bestätigung.
- `Ctrl+P`: Befehle (Theme, Bildschirmfoto als SVG im Ordner der Bildschirmfotos, beenden).

[↑ Inhalt](#inhalt)

---

## Themes und Terminals

Zehn `omega-*`-Themes werden mit dem Rest der OMEGA-Suite geteilt:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Wechseln Sie mit `t` zwischen den Themes oder wählen Sie eines in den Einstellungen (`s`); die Wahl wird gespeichert.
- Die HTML-Exporte haben eigene Themes: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail passt die visuelle Komplexität über ein **Darstellungsprofil** an das erkannte Terminal an:
  Vollständig, Standard, Reduziert oder Mono (nur ASCII).

| Mindestgröße | Profil | Typische Terminals |
|---|---|---|
| 120×32 oder mehr | Vollständig | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 oder mehr | Standard | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 oder mehr | Reduziert | urxvt, xterm, modernes SSH |
| unter 80×24 | Mono (nur ASCII) | Linux-TTY, altes SSH |

Nach einer Größenänderung liest `r` die Terminalgröße neu; sie wird oben neben dem Theme angezeigt.

[↑ Inhalt](#inhalt)

---

## Dateien, Dienste und Kompatibilität

### Im Ordner von omega-tail

Der gesamte Zustand von omega-tail liegt in `~/omega-tail/var/`, wird beim Start neu angelegt und nie veröffentlicht:

```text
var/
├── settings.json         Einstellungen (Sprache, Themes, Ordner, Schwellenwerte, Regeln des Tors)
├── omega-jeton.json      Installations-Token (omega-connect)
├── porte/                Konfiguration des Tors, Zertifikat, Vertrauens- und Sperrliste, AS- / Länderdatenbank
├── veille/               Log der automatischen Überwachung
├── survie/               Originale der geänderten Dateien, Zustand des Schutzschalters
├── funnel/sauvegardes/   Veröffentlichung vor jeder Änderung (die 50 neuesten)
├── exports/              exportierte Berichte, Logs und Listen
└── screenshots/          Bildschirmfotos (Ctrl+P)
```

### Auf dem System (nur wenn Sie die betreffende Schutzmaßnahme aktivieren)

Jede Datei wird per sudo angelegt, mit angezeigtem Befehl, und durch die Gegenaktion in omega-tail wieder entfernt.

| Datei oder Dienst | Angelegt durch | Entfernt durch |
|---|---|---|
| Dienst `omega-tail-porte` (systemd, OpenRC oder runit) und `omega-tail-porte-certificat` (systemd-Timer oder eine markierte Zeile in Ihrer crontab) | Schutz aktivieren | Schutz deaktivieren |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (oder eine Kontrollgruppe außerhalb von systemd) | Eindämmung anwenden | Eindämmung entfernen |
| Timer `omega-tail-retablir-*` (Wiederinbetriebnahme nach einer Abschaltung) | Schutzschalter | Ende der Abschaltung |
| Dienst `omega-tail-veille` | Überwachung aktivieren | Überwachung deaktivieren |
| Dienst `omega-bouclier-wg`, nftables-Tabelle, `/etc/omega-bouclier-wg/` | Schutzschild: Setzen | Schutzschild: Entfernen |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | IP-Weiterleitung aktivieren | Löschen der Datei |

Die Datei `override.conf` von `tailscaled` wird, falls vorhanden, nie verändert.

### Init-Systeme

| | systemd | OpenRC | runit |
|---|---|---|---|
| Dienst `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Logs | `journalctl` | Dateien des Dienstes | `svlogd`, `socklog` |
| Eindämmung | systemd-Ergänzungsdatei | Kontrollgruppe (cgroup v2) | Kontrollgruppe (cgroup v2) |
| Vorübergehende Abschaltung | systemd-Timer | abgekoppelter Prozess unter Ihrem Konto | abgekoppelter Prozess unter Ihrem Konto |
| Tor, Überwachung, Schutzschild | systemd-Dienste | OpenRC-Dienste | runit-Dienste |

Außerhalb von systemd geht die Eindämmung per Kontrollgruppe verloren, wenn `tailscaled` neu startet: Eine Warnung
schlägt dann vor, sie wieder anzuwenden.

### IPv4 und IPv6

Tor, Listen, Gruppierungen und Schutzschild behandeln beide Familien. Die gezählten Präfixe sind /24 bei IPv4 und /64
bei IPv6; eine IPv4-Adresse in der Form `::ffff:a.b.c.d` wird als IPv4-Adresse behandelt.

[↑ Inhalt](#inhalt)

---

## Sicherheit

omega-tail wirkt auf einen dem Internet ausgesetzten Dienst; es wurde so entworfen, dass es die Lage nie
verschlimmert.

- **Nie root**: Die Anwendung, das HAProxy-Tor und die Überwachung laufen unter Ihrem Konto; sudo wird nur verlangt,
  um einen Dienst anzulegen oder zu entfernen, mit vorher angezeigtem Befehl.
- **Private Kanäle**: Die Administrations-Sockets des Tors haben den Modus 600 in einem Ordner mit 700; die
  Synchronisation seiner Tabellen läuft über einen Socket im selben Ordner.
- **Rückweg**: Jedes Umschalten von Funnel wird gesichert und geprüft, und bei einem Fehlschlag wird der vorherige
  Zustand wiederhergestellt.
- **Zuerst beobachten**: Tor, Gruppierungen und Schutzschild werden im Beobachtungsmodus gesetzt; nichts wird
  abgelehnt, bevor Sie es entschieden haben.
- **Das Tailnet wird nie getrennt**: Das Tor lässt Ihre Rechner immer zu, und der Schutzschalter schaltet nur Funnel
  ab.
- **Geprüfte Eingaben**: Nur Adressen oder Netze in kanonischer Form erreichen HAProxy; die von den Rechnern des
  Tailnets gemeldeten Namen werden vor der Anzeige bereinigt.
- **Audit**: Der Code wurde auditiert (claude-security, 2026-11-25); die 7 gefundenen Punkte, von denen keiner von
  einem Besucher aus der Ferne ausnutzbar war, wurden noch am selben Tag behoben.
- Testen Sie zuerst auf einem Testrechner oder im Beobachtungsmodus, und verwenden Sie für IPv4-Tests die
  Dokumentationsnetze RFC 5737: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Inhalt](#inhalt)

---

## Tests und Qualität

Die Testsuite umfasst **179 Tests**: Domäne, Anwendungsfälle, Infrastruktur (mit einem simulierten Funnel),
Textual-Bildschirme mit den echten Stylesheets, Init-Systeme, Sicherheit. Der Code wird mit `ruff`, `mypy` und
`import-linter` (Schichtregeln) geprüft. Der Ordner `tests/` ist im Archiv enthalten.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

Die meisten Tests benötigen weder Tailscale noch HAProxy noch root.

[↑ Inhalt](#inhalt)

---

## Projektstatus

### Einsatzbereite Punkte

- Vollständige Steuerung von Tailscale: Dienst, Verbindung, Einstellungen, Veröffentlichung, Netzwerk, Logs.
- HAProxy-Tor vor TLS, im Produktivbetrieb seit dem 2026-11-23, mit Regeln, Listen, Gruppierungen und Angriffsmodus.
- Überleben: Eindämmung, Schutzschalter, automatische Überwachung.
- Schutzschild des WireGuard-Ports, im Produktivbetrieb seit dem 2026-11-24.
- Bericht und Exporte als TXT, HTML, JSON.
- Kompatibel mit omega-connect und omega-fire.

### Bekannte Einschränkungen

- Die Dienste unter OpenRC und runit sind durch die Tests abgedeckt, aber noch nicht auf einem echten Rechner
  validiert.
- Das Tor schützt einen per HTTPS auf einem einzigen Port veröffentlichten Funnel, mit dem Pfad `/`.
- Die Gruppierungen erfordern ein mit Lua kompiliertes HAProxy; ohne Lua funktioniert das Tor ohne sie.
- Das Schutzschild kann nicht auf einem aktualisierten Kernel ohne Neustart gesetzt werden (fehlende Module): Der
  Bildschirm weist darauf hin.
- Ein Angriff, der die Internetleitung selbst auslastet, bleibt außerhalb der Reichweite eines auf dem Rechner
  installierten Werkzeugs.
- Der Durchsatz einer über Funnel veröffentlichten Website bleibt durch die Relais von Tailscale und durch den Router
  begrenzt.

[↑ Inhalt](#inhalt)

---

## Deinstallation

Entfernen Sie zuerst aus omega-tail heraus, was auf dem System angelegt wurde, in dieser Reihenfolge:

1. **Funnel-Firewall → Schutz deaktivieren** (Funnel wird wie zuvor wiederhergestellt).
2. **Überleben → Überwachung deaktivieren**.
3. **Überleben → Schutzschild des WireGuard-Ports → Entfernen**.
4. **Überleben → Eindämmung entfernen**.

Löschen Sie dann den Ordner:

```bash
rm -rf ~/omega-tail
```

Löschen Sie von Hand die anderswo abgelegten Exporte, den Alias `omega-tail` aus `~/.bashrc` oder `~/.zshrc` und,
falls Sie sie aktiviert hatten, die Datei `/etc/sysctl.d/99-omega-tail-forwarding.conf`. Das Operator-Recht von
Tailscale wird mit `sudo tailscale set --operator=` entzogen.

[↑ Inhalt](#inhalt)

---

## Lizenz

Omega-Tail wird unter der **MIT**-Lizenz vertrieben. Den vollständigen Text finden Sie in der Datei
[`LICENSE`](../../../LICENSE).

Die AS- / Länderdatenbank verwendet IP Geolocation by [DB-IP](https://db-ip.com), unter der Lizenz
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Inhalt](#inhalt)

---

> **Omega-Tail — Tailscale steuern, Funnel schützen.**
>
> Eine TUI-Oberfläche für Tailscale und ein Tor, das Missbrauch vor jeder Verschlüsselung ablehnt.
