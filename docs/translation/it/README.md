<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**Gestore di pilotaggio di TAILSCALE con firewall integrato per FUNNEL**

OMEGA-TAIL è lo strumento della suite OMEGA che pilota **Tailscale** su una macchina e la **protegge** quando
pubblica un servizio su Internet tramite **Tailscale Funnel**.

> Realizzato da [kraynux](https://github.com/kraynux) per [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Pagina ufficiale](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/it/) · [Screenshot](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Interfaccia, documentazione, esportazioni e pagine per i visitatori disponibili in **17 lingue** — vedi [Lingue dell'interfaccia](#lingue-dellinterfaccia).  
**Lingue:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** è un'applicazione TUI (Terminal User Interface) in Python costruita con
[Textual](https://textual.textualize.io/). Permette di gestire e configurare **Tailscale** in modalità avanzata da
un'interfaccia, senza dover ricordare un solo comando. Aggiunge anche delle protezioni (firewall, confinamento,
sopravvivenza…) per la modalità **Funnel**, che apre un servizio della macchina a tutta Internet.

Ogni azione che modifica la macchina mostra prima il suo comando. La password di sudo si digita nel terminale,
azione per azione, e nulla viene avviato in background senza di te.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/it/omega-tail/F.png" width="32%" />
</p>

Il progetto è concepito secondo i principi della **Clean Architecture**, con `app/` come radice di composizione:
il dominio applicativo, l'orchestrazione, l'infrastruttura e l'interfaccia sono separati.

## Sommario

- [Presentazione](#presentazione)
- [Capire Tailscale e Funnel](#capire-tailscale-e-funnel)
- [Funzionalità](#funzionalità)
- [Le protezioni nel dettaglio](#le-protezioni-nel-dettaglio)
- [Misurazioni](#misurazioni)
- [Architettura](#architettura)
- [Prerequisiti](#prerequisiti)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Temi e terminali](#temi-e-terminali)
- [File, servizi e compatibilità](#file-servizi-e-compatibilità)
- [Sicurezza](#sicurezza)
- [Test e qualità](#test-e-qualità)
- [Stato del progetto](#stato-del-progetto)
- [Disinstallazione](#disinstallazione)
- [Licenza](#licenza)

---

## Presentazione

### Perché omega-tail

Tailscale Funnel pubblica un servizio della macchina su Internet senza aprire alcuna porta sul router: i visitatori
passano attraverso i relay di Tailscale. È semplice e sicuro dal lato della rete, ma resta una debolezza.

- **Il costo della cifratura.** Nella modalità Funnel predefinita, è il servizio `tailscaled` della macchina a
  eseguire l'handshake TLS di ogni visitatore. Misurato su una piccola macchina, rappresenta circa l'**80 % del
  costo di una connessione**. Qualche centinaio di nuove connessioni al secondo basta a saturare il processore: un
  solo computer comune, con un semplice script, può far cadere il sito e la macchina.
- **Visitatori invisibili.** I firewall abituali (nftables, ufw, fail2ban) non vedono questi visitatori: arrivano
  cifrati, attraverso il tunnel di Tailscale, con l'indirizzo di un relay.
- **Impostazioni sparse.** Le impostazioni di Tailscale (operatore, nodo di uscita, rotte, SSH, scudo…) sono
  numerose, suddivise tra comandi e console web, e alcune possono interrompere la sessione in corso.

### Obiettivi

- Pilotare Tailscale interamente da un'interfaccia, con una frase di spiegazione per ogni impostazione.
- Rifiutare le connessioni abusive **prima** di qualsiasi cifratura, vedendo l'indirizzo reale di ogni visitatore.
- Tenere in piedi la macchina sotto attacco: l'amministrazione e gli altri servizi restano raggiungibili.
- Non imporre mai nulla: proporre, mostrare il comando, chiedere e poter tornare indietro.
- Funzionare su qualsiasi distribuzione Linux, con systemd, OpenRC o runit.

### Cosa fa omega-tail

- Mostra lo stato di Tailscale, della macchina e di ciò che è pubblicato, con avvisi che portano alla schermata
  che risolve il problema.
- Avvia, arresta e riavvia `tailscaled`, con una protezione se la tua sessione passa da Tailscale.
- Gestisce la connessione, gli account e tutte le impostazioni di `tailscale set`, verificate prima di essere
  applicate.
- Pubblica, rimuove, sospende e prova i servizi di Serve e di Funnel, con backup e ripristino.
- Mostra i dispositivi del tailnet, il loro percorso (diretto o tramite relay), una diagnostica di rete e i log.
- Colloca un **varco** HAProxy tra Funnel e il tuo sito: regole per indirizzo, per prefisso, budget globale, liste
  di fiducia e nera, raggruppamenti per impronta JA4, rete di origine (AS) e paese, modalità attacco automatica.
- Confina `tailscaled`, interrompe Funnel per un momento o del tutto, e può farlo da solo grazie a una
  sorveglianza automatica.
- Protegge la porta WireGuard di `tailscaled` con una tabella nftables (scudo).
- Produce un report della macchina e degli attacchi degli ultimi 7 giorni, in TXT, HTML o JSON.

### Cosa non fa il progetto

- Non sostituisce Tailscale: lo pilota.
- Non protegge da un attacco volumetrico che satura la linea Internet stessa (il router, il collegamento).
- Non gestisce la console di amministrazione web di Tailscale (criteri di accesso, approvazione dei nodi di uscita,
  attivazione di Funnel per il tailnet).
- Non protegge un servizio pubblicato in altro modo che tramite Funnel: per quelle porte c'è omega-fire.
- Non gira mai come root e non avvia nulla in background senza il tuo consenso.
- Non funziona né su Windows né su macOS.

[↑ Sommario](#sommario)

---

## Capire Tailscale e Funnel

omega-tail presuppone alcune nozioni di Tailscale. Questa parte le raccoglie, senza presupporre altro.

### Il vocabolario

| Termine | Che cos'è |
|---|---|
| **Tailnet** | La tua rete privata Tailscale: tutte le macchine collegate allo stesso account (o alla stessa organizzazione). Ogni macchina vi riceve un indirizzo in `100.x.y.z` (intervallo 100.64.0.0/10) e un indirizzo IPv6 in `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | Il servizio (demone) che gira sulla macchina: mantiene il tunnel cifrato WireGuard, lo stack di rete di Tailscale e, per Serve e Funnel, l'inoltro verso i tuoi servizi. |
| **`tailscale`** | Il comando che pilota `tailscaled` (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail lo usa al posto tuo. |
| **WireGuard** | Il protocollo di tunnel cifrato usato tra le macchine. Per questo `tailscaled` resta in ascolto su una porta UDP (41641 per impostazione predefinita), spesso aperta dal router (UPnP). |
| **Relay DERP (DERP relay)** | Server di Tailscale che inoltrano il traffico quando due macchine non riescono a raggiungersi direttamente (NAT difficile). Il percorso « diretto » è più veloce. |
| **MagicDNS** | I nomi delle macchine del tailnet, nella forma `machine.nom-du-tailnet.ts.net`. |
| **Serve** | Pubblicare un servizio locale (un sito, un'API…) **solo per il tailnet**, in HTTPS con un certificato `*.ts.net` valido. |
| **Funnel** | Pubblicare un servizio locale **per tutta Internet**, all'indirizzo `https://machine.nom-du-tailnet.ts.net`. Possono essere aperte solo le porte 443, 8443 e 10000. |
| **Relay Funnel (Funnel relay)** | I server di Tailscale che ricevono i visitatori da Internet e li fanno entrare nel tuo tailnet (compaiono come « funnel-ingress-node »). |
| **Operatore (operator)** | Un account Linux autorizzato a configurare Tailscale senza sudo (`tailscale set --operator=…`). omega-tail lo propone una volta, tramite sudo. |
| **Nodo di uscita (exit node)** | Una macchina del tailnet attraverso cui un'altra fa passare tutto il suo traffico Internet (come una VPN). Deve essere approvato nella console di Tailscale. |
| **Sottorete annunciata (subnet router)** | Una rete locale (per esempio `192.168.1.0/24`) che una macchina rende raggiungibile dal resto del tailnet. |
| **Scudo (shields up)** | Impostazione di Tailscale che rifiuta tutte le connessioni in entrata provenienti dal tailnet. |
| **SSH Tailscale** | Un server SSH fornito da Tailscale, autorizzato dai criteri del tailnet. |
| **Intestazione PROXY v2** | Una breve intestazione aggiunta all'inizio di una connessione per trasmettere l'indirizzo reale del visitatore a chi la riceve. |
| **Impronta JA4 (JA4 fingerprint)** | Una firma del modo in cui un software apre una connessione TLS: un browser e uno strumento di attacco non hanno la stessa. |
| **AS (sistema autonomo)** | La rete di origine di un indirizzo: fornitore di accesso, hosting, cloud. |

### Il percorso di un visitatore

**Funnel predefinito, senza omega-tail.** `tailscaled` fa tutto: decifra il tunnel WireGuard, esegue l'handshake
TLS del visitatore, poi inoltra la richiesta in HTTP verso il tuo sito. Nessun firewall della macchina vede il
visitatore, e ogni nuova connessione costa cara a `tailscaled`.

```text
Visitatore ──HTTPS──▶ Relay Funnel ──WireGuard──▶ tailscaled (TLS + inoltro HTTP) ──HTTP──▶ il tuo sito
                      (Tailscale)                 └── tutto il costo è qui
```

**Funnel con il varco di omega-tail.** Funnel passa in modalità TCP: `tailscaled` non fa più TLS, trasmette il
flusso ancora cifrato al varco, preceduto dall'indirizzo reale del visitatore (intestazione PROXY v2). Il varco
decide **prima** di qualsiasi cifratura: una connessione rifiutata non costa quasi nulla, e solo le connessioni
ammesse vengono decifrate, da OpenSSL, più veloce del TLS di `tailscaled`.

```text
Visitatore ──HTTPS──▶ Relay Funnel ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                       │
                                                       ▼
                                        Varco omega-tail (HAProxy, 127.0.0.1)
                                        ├── rifiuto prima del TLS: lista nera, frequenza, budget, nome richiesto, raggruppamenti
                                        └── ammesso: TLS (certificato *.ts.net) ──HTTP──▶ il tuo sito
```

Il varco ascolta solo sull'interfaccia di loopback della macchina e gira con il tuo account. Le macchine del tuo
tailnet vi sono sempre ammesse, prima di qualsiasi regola: vengono filtrati solo i visitatori di Funnel.

### Cosa deve consentire Tailscale (console di amministrazione)

Queste impostazioni si fanno una volta, nella console web di Tailscale; omega-tail non le modifica.

- **MagicDNS** e i **certificati HTTPS** attivati per il tailnet (necessari a Serve, a Funnel e al certificato
  del varco).
- **Funnel autorizzato** per la macchina nei criteri di accesso del tailnet (attributo `funnel`).
- Per un nodo di uscita o delle sottoreti annunciate: la loro **approvazione** nella console.

[↑ Sommario](#sommario)

---

## Funzionalità

Il menu principale ha due colonne da sei: **TAILSCALE** per pilotare, **PROTEZIONE** per difendere.

### TAILSCALE

#### 1. Pannello di controllo

- **Tailscale**: servizio, stato della connessione, versione in esecuzione e installata, nome della macchina,
  indirizzi, account, dispositivi online, scadenza della chiave, operatore, nodo di uscita offerto e usato,
  sottoreti annunciate.
- **Macchina**: CPU dell'intera macchina, carico per core, temperatura, memoria, CPU e memoria di `tailscaled`,
  confinamento, poi lo stato delle protezioni (Funnel, firewall e modalità attacco, lista nera, sorveglianza, scudo).
- **Pubblicazione**: ogni porta pubblicata, per Internet (Funnel) o per il tailnet (Serve), la sua modalità e la sua
  destinazione.
- **Avvisi**, dal più grave al meno grave, con « Correggi » che apre la schermata interessata. Per esempio:
  servizio arrestato, aggiornamento installato ma non applicato, chiave in scadenza, Funnel pubblicato senza
  protezione, temperatura elevata, `tailscaled` troppo esigente o non confinato, lista nera che cresce.
- Valori in verde, arancione o rosso secondo delle soglie (CPU, carico, temperatura, memoria, `tailscaled`).

#### 2. Servizio tailscaled

- Stato visto dal sistema di init, versione in esecuzione e installata, comando di avvio, file aggiuntivi
  (drop-in), confinamento.
- **Avvia**, **Arresta**, **Riavvia** (per esempio per applicare un aggiornamento già installato).
- **Protezione**: se la tua sessione passa da Tailscale (SSH tramite il tailnet), Arresta chiede una seconda
  conferma, perché non potresti più riavviarlo.
- **Correggi l'avvio**: individua un file aggiuntivo che lancia `tailscale up` all'avvio e rischia di far uscire
  la macchina dal tailnet al primo cambio di impostazione; la correzione viene mostrata e l'originale conservato.

#### 3. Connessione e impostazioni

- **Connetti**, **Disconnetti**, **Aggiungi un account**, **Cambia account**, **Disconnessione definitiva**
  (nome della macchina da digitare).
- **Tutte le impostazioni di `tailscale set`**, ognuna con la sua frase di spiegazione: nome e soprannome della
  macchina, rotte, DNS del tailnet, scudo, filtraggio con stato, modalità netfilter, nodo di uscita, accesso alla rete
  locale, offrire la macchina come nodo di uscita, sottoreti annunciate, SSH Tailscale, interfaccia web,
  aggiornamenti, relay tra pari, operatore.
- Durante l'inserimento, un riquadro mostra **prima → dopo** e il comando; dopo l'applicazione, ogni valore riletto
  è contrassegnato con ✔ (applicato) o ✖ (no).
- Un avvertimento segnala quando una modifica può interrompere una sessione che passa da Tailscale.
- **Inoltro IP**: attivato con un pulsante quando la macchina fa da nodo di uscita o annuncia delle sottoreti.

#### 4. Pubblicazione

- Tutto ciò che la macchina pubblica: porta, pubblico (Funnel) o tailnet (Serve), modalità, percorso, destinazione,
  protezione.
- **Pubblica** un servizio locale in HTTPS, HTTP, TCP o TLS terminato; **Rimuovi**; **Sospendi Funnel** e
  **Ripristina Funnel** (in modo identico).
- **Prova end-to-end**: una vera connessione, come un visitatore (risposta, tempo, certificato, versione di TLS).
- **Backup**: lo stato precedente a ogni modifica (i 50 più recenti), ripristinabili.
- Ogni modifica viene verificata; in caso di differenza, la pubblicazione viene ricostruita, altrimenti viene
  rimesso lo stato precedente.

#### 5. Rete e dispositivi

- **Dispositivi** del tailnet: sistema, online o no, percorso (diretto o tramite relay), ultima volta visto,
  indirizzo, traffico scambiato; i relay Funnel di Tailscale sono nascosti per impostazione predefinita.
- **Ping Tailscale** (percorso e latenza), **Chi è?** (a chi appartiene un indirizzo del tailnet).
- **Diagnostica di rete**: UDP, IPv4 / IPv6, tipo di NAT, apertura di porte da parte del router (UPnP, NAT-PMP,
  PCP), relay più vicino e latenze.
- **DNS**, **blocco del tailnet** (tailnet lock) e **contatori interni** di Tailscale.
- Sola lettura: nulla in questa schermata modifica un'impostazione.

#### 6. Log

- Il log di `tailscaled` (journalctl, o i file del servizio fuori da systemd) e quello del varco, filtrabili ed
  esportabili.
- Ogni informazione ha il suo colore, preso dal tema: data, processo, categoria del messaggio (controllo, rete, DNS,
  motore WireGuard), indirizzi in grassetto, errori in rosso, avvertimenti in arancione; per il varco, motivo del
  rifiuto, raggruppamento, AS e paese.

### PROTEZIONE

#### 7. Firewall Funnel

- **Installa HAProxy** tramite il gestore di pacchetti della distribuzione (pacman, apt, dnf, zypper, apk, xbps,
  emerge).
- **Attiva la protezione**: certificato `*.ts.net`, liste, configurazione verificata, servizio del varco,
  commutazione di Funnel poi prova da Internet; in caso di errore, la pubblicazione di origine viene rimessa
  subito.
- **Disattiva la protezione**: Funnel viene rimesso esattamente com'era prima, verificato.
- **Regole** applicate a caldo, modalità **osservazione** per regolare le soglie senza rischi, **raggruppamenti**
  (vedi [Le protezioni nel dettaglio](#le-protezioni-nel-dettaglio)).
- **Aggiorna il database** AS / paesi (DB-IP Lite), in un processo separato.

#### 8. Sopravvivenza

- **Confinamento di `tailscaled`**: tetto di CPU, peso e priorità, opzione di priorità all'accesso SSH.
- **Interruttore automatico Funnel**: soglie di CPU e temperatura, interruzione di 10 minuti (riattivazione
  automatica) o totale.
- **Sorveglianza automatica**: la stessa cosa senza nessuno davanti allo schermo.
- **Scudo della porta WireGuard**: pulsante verso la sua schermata (osservazione, attivo, applica, riapplica,
  rimuovi, affida).

#### 9. Attacchi e decisioni

- Contatori del varco (ricevute, rifiutate prima della cifratura, ammesse, in corso) e indirizzi più attivi,
  riletti ogni 2 secondi, con paese, AS e stato di ogni indirizzo.
- **Blocca**, **Lista nera**, **Sblocca**, **Fiducia**: applicato subito, senza riavviare il varco; la
  notifica indica in una riga l'azione e la posizione dell'indirizzo.
- Viste **Impronte**, **AS** e **Paesi**; stato della modalità attacco e connessioni rifiutate dai raggruppamenti.
- **Gestione della lista nera**: elenco completo con data di aggiunta e origine, aggiunta, eliminazione,
  importazione di un file TXT (duplicati, reti già coperte e indirizzi del tailnet scartati), pulizie con anteprima
  (per anzianità, le N più vecchie, un intervallo di righe, un'origine, tutto), esportazioni TXT (reimportabile),
  HTML e JSON. Tetto di 50 000 voci.

#### 10. Report

- Tutto ciò che omega-tail sa della macchina, in fatti: Tailscale, pubblicazione, macchina, firewall,
  sopravvivenza, avvisi, e gli **attacchi degli ultimi 7 giorni** letti nel log del varco.
- **Privacy**: per impostazione predefinita, senza l'account Tailscale né i nomi e gli indirizzi dei dispositivi
  del tailnet, per poterlo inviare a qualcuno.
- Esportazioni **TXT**, **HTML** (tema a scelta) e **JSON**; **Vedi le esportazioni** apre la cartella nel browser.

#### 11. Impostazioni

- Lingua dell'interfaccia e delle esportazioni, tema dell'interfaccia e delle esportazioni, cartelle delle
  esportazioni e degli screenshot, e la loro pulizia.

#### 12. Aiuto

- Una sezione per schermata, le scorciatoie, la riga di comando e **Contatti e supporto**.

[↑ Sommario](#sommario)

---

## Le protezioni nel dettaglio

Ogni protezione risponde a una minaccia precisa; nessuna è imposta.

| Protezione | Contro cosa | Dove |
|---|---|---|
| Varco (regole) | Raffiche da uno o pochi indirizzi, connessioni che non puntano al sito | Firewall Funnel |
| Raggruppamenti | Attacchi da indirizzi dispersi (migliaia di indirizzi, una connessione ciascuno) | Firewall Funnel |
| Lista nera | Indirizzi e reti noti per attaccare, conservati nel tempo | Attacchi e decisioni |
| Confinamento | `tailscaled` che si prenderebbe tutta la macchina sotto attacco | Sopravvivenza |
| Interruttore automatico | Macchina satura nonostante tutto: interrompere Funnel per un momento | Sopravvivenza |
| Sorveglianza automatica | La stessa cosa, senza nessuno davanti allo schermo | Sopravvivenza |
| Scudo WireGuard | Flusso di pacchetti UDP sulla porta di `tailscaled`, con Funnel aperto o no | Sopravvivenza |

### Il varco (Firewall Funnel)

Le regole si applicano in quest'ordine, tutte prima della cifratura:

1. **Macchine del tailnet** (100.64.0.0/10, fd7a:115c:a1e0::/48): sempre ammesse.
2. **Lista di fiducia**: mai limitata. **Lista nera**: rifiutata fino alla rimozione.
3. **Frequenza per indirizzo** (40 connessioni / 10 s per impostazione predefinita): oltre questa soglia,
   l'indirizzo viene bloccato per la durata scelta (60 min per impostazione predefinita).
4. **Frequenza per prefisso** /24 in IPv4, /64 in IPv6.
5. **Budget globale** di connessioni ammesse al secondo: il processore non viene mai sopraffatto.
6. **Nome richiesto**: una connessione che non punta al nome della macchina viene rifiutata.

Il certificato `*.ts.net` del varco viene richiesto a Tailscale, verificato ogni giorno e rinnovato a caldo 30
giorni prima della scadenza. La modalità **osservazione** conta tutto senza rifiutare nulla.

### I raggruppamenti (impronte, AS, paesi)

Contro un attacco da indirizzi dispersi, le regole per indirizzo vedono ogni indirizzo una sola volta. Il varco
classifica quindi ogni client anche in base alla sua **impronta JA4**, al suo **AS** e al suo **paese**, e conta
la frequenza di ogni gruppo.

- **Modalità attacco automatica**: oltre 80 connessioni in entrata al secondo (regolabile), il varco passa da solo
  in modalità attacco, e ne esce dopo 5 minuti di calma.
- Solo in modalità attacco: un'impronta sconosciuta che esplode, un AS di hosting o di cloud (elenco modificabile)
  o un paese del tuo elenco (vuoto per impostazione predefinita) che supera la sua frequenza viene rifiutato.
- I **browser comuni** (Chrome, Edge, Firefox) non sono mai toccati da queste regole; i **client noti** (ammessi
  nelle ultime 24 h) passano prima del budget globale.
- **Apprendimento**: per 7 giorni, il varco impara le impronte abituali del tuo sito (mai durante un attacco); i
  raggruppamenti restano in osservazione fino ad allora.
- Fuori dagli attacchi, una connessione su dieci viene classificata; durante un attacco, tutte.
- Il database AS / paesi è **DB-IP Lite**, scaricato e aggiornato una volta al mese.

### La sopravvivenza

- **Confinamento**: un file aggiuntivo separato pone un tetto a `tailscaled` (per esempio un core intero su una
  macchina a 4 thread) e ne abbassa la priorità. La tua configurazione non viene mai modificata.
- **Interruttore automatico**: quando `tailscaled` resta sopra la soglia di CPU (80 % di un core per 60 s per
  impostazione predefinita) o la temperatura raggiunge 85 °C, omega-tail propone di interrompere Funnel per 10
  minuti (riattivazione automatica, in modo identico, anche con omega-tail chiuso), di interromperlo del tutto, o
  di attendere. Il tailnet non viene mai interrotto.
- **Sorveglianza automatica** (disattivata per impostazione predefinita): un servizio con il tuo account interrompe
  Funnel da solo dopo tre superamenti, 15 minuti la prima volta, 30 la seconda, poi un'ora, e lo riattiva da solo.

### Lo scudo della porta WireGuard

`tailscaled` consuma circa un core del processore ogni 100 000 pacchetti al secondo ricevuti sulla sua porta UDP,
anche se non validi. Lo scudo è una tabella nftables posta davanti a esso, sulle schede di rete:

- i **peer noti** (quelli a cui `tailscaled` scrive) non vengono mai limitati;
- gli handshake sono limitati a 20 al secondo per origine;
- le altre origini hanno un budget (500 pacchetti al secondo ciascuna, 5 000 in totale);
- i pacchetti che non sono WireGuard vengono rifiutati.

Si applica prima in **osservazione**, poi in **attivo**. Se è collegato tramite omega-connect, **omega-fire**
(3.7.0 o più recente) può applicarlo e gestirlo al posto di omega-tail: è la stessa tabella, che cambia di mano
senza essere toccata.

[↑ Sommario](#sommario)

---

## Misurazioni

Le scelte di omega-tail derivano da misurazioni, su macchine della stessa generazione di quelle che protegge
(processori dal 2010 al 2016, per la maggior parte senza accelerazione AES).

| Misurazione | Risultato |
|---|---|
| Quota del TLS nel costo di una connessione Funnel predefinita | circa 80 % |
| Costo di una connessione **rifiutata** dal varco, rispetto a Funnel predefinito | **4,6 volte inferiore** |
| Costo di una connessione **ammessa** dal varco, rispetto a Funnel predefinito | **2 volte inferiore** |
| Throughput con il varco, connessioni tenute aperte (rispetto a un TLS in Go come quello di `tailscaled`) | **+15 %** di richieste, −20 % di CPU |
| Scudo WireGuard: flusso che occupava un core intero di `tailscaled` | **1 %** di un core |
| Memoria dei servizi (varco, sorveglianza, scudo) | circa 67 MB |

Il varco quindi non degrada il throughput di un sito: su queste macchine, è la cifratura stessa a limitare, con o
senza omega-tail, e in produzione Funnel passa comunque attraverso i relay di Tailscale e il router.

[↑ Sommario](#sommario)

---

## Architettura

```text
src/omega_tail/
├── app/              Radice di composizione: assembla i livelli, punto di ingresso (interfaccia, riga di comando)
├── core/             Costanti condivise
├── domain/           Logica applicativa pura: regole del varco, avvisi, interruttore automatico, sorveglianza, lista nera…
├── application/      Casi d'uso: pubblicazione, firewall, sopravvivenza, report, impostazioni
├── ports/            Contratti (Protocol) attesi dall'applicazione
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, log, esportazioni, script Lua
├── interfaces/       tui/ (Textual), cli/ (riga di comando), shared/ (aiuto, report, presentazione)
└── shared/           Lingue (gettext)
```

### Principi di progettazione

- `domain/` non contiene né letture né scritture: tutto vi è testabile senza macchina.
- `application/` orchestra i casi d'uso tramite il dominio e le porte (ports); l'interfaccia e la riga di comando
  chiamano gli stessi casi d'uso.
- Solo `infrastructure.commands` e `infrastructure.privileged` lanciano comandi; l'interfaccia non ne lancia mai
  direttamente. Queste regole sono verificate automaticamente (import-linter).
- L'interfaccia si appoggia su [omega-lib](https://github.com/kraynux), la libreria condivisa da tutta la suite
  OMEGA (temi, rilevamento del terminale, lingue, contatti e supporto, scudo WireGuard). Non è pubblicata su
  PyPI: è inclusa nell'archivio (`vendor/omega-lib/`).
- Ogni chiamata lenta (Tailscale, HAProxy, disco, rete) gira in background: l'interfaccia non si blocca mai.

[↑ Sommario](#sommario)

---

## Prerequisiti

### Sistema

- Linux, qualsiasi distribuzione (testato su Arch Linux e derivate).
- Python 3.10 o superiore, con il modulo `venv`.
- Un sistema di init: **systemd**, **OpenRC** o **runit**.
- `sudo` per le azioni che modificano la macchina (richiesto azione per azione, mai all'avvio).
- Un terminale di almeno 80×24 (vedi [Temi e terminali](#temi-e-terminali)).

### Tailscale

- **Tailscale** installato e connesso (client `tailscale` e servizio `tailscaled`); testato con la versione 1.104.
- Per Funnel: MagicDNS, certificati HTTPS e Funnel autorizzati nella console di Tailscale (vedi
  [Cosa deve consentire Tailscale](#cosa-deve-consentire-tailscale-console-di-amministrazione)).

### Dipendenze Python

Installate da `install.sh` in un ambiente virtuale:

- `textual`: l'interfaccia.
- `omega-lib`: libreria condivisa della suite OMEGA, inclusa nell'archivio.

### Componenti obbligatori e opzionali

omega-tail rileva ciò che è presente e attiva solo ciò che è utilizzabile.

| Componente | Ruolo | Stato |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Tutto ciò che omega-tail pilota | **Obbligatorio** |
| Python 3.10+, `textual`, `omega-lib` | L'applicazione | **Obbligatorio** |
| systemd, OpenRC o runit | Servizi del varco, della sorveglianza, dello scudo | **Obbligatorio** (uno dei tre) |
| HAProxy 3.x | Il varco del Firewall Funnel | Opzionale (installabile da omega-tail) |
| HAProxy con Lua | I raggruppamenti (impronte, AS, paesi) | Opzionale (caso delle distribuzioni comuni) |
| nftables (kernel con `nft_limit`) | Lo scudo della porta WireGuard | Opzionale |
| Lettura del log di sistema (gruppo `systemd-journal`, `adm` o `wheel`) | Log, report degli attacchi | Consigliato |
| Browser e ambiente desktop | « Vedi le esportazioni » nel browser (altrimenti, lettura in omega-tail) | Opzionale |
| omega-connect | Registro, sincronizzazione, aggiornamenti della suite | Opzionale |
| omega-fire 3.7.0+ | Gestione dello scudo WireGuard da omega-fire | Opzionale |

[↑ Sommario](#sommario)

---

## Installazione

L'archivio ufficiale è fornito in formato `.tar.gz`. Verificane l'integrità prima dell'installazione, con il file
`sha.txt` pubblicato accanto:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Questi tre metodi servono per una prima installazione.** Se `~/omega-tail` esiste già, usa la
> sezione [Aggiornamento](#aggiornamento). Non rilanciare mai questi comandi dall'interno di una cartella
> `omega-tail` esistente: `tar` creerebbe un `omega-tail/omega-tail/` annidato.

Nessun passaggio dell'installazione richiede i diritti di root: omega-tail si avvia come utente normale.

### Metodo 1 — script di installazione

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Sembri già trovarti in una cartella omega-tail — vedi la sezione Aggiornamento del README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Già estratto qui, passaggio ignorato." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail esiste già, spostamento ignorato." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

Lo script crea l'ambiente virtuale, installa le dipendenze (prima omega-lib inclusa), rende eseguibili i
lanciatori, scrive il token di installazione letto da omega-connect e propone l'alias `omega-tail`. Può essere
rilanciato senza rischi.

### Metodo 2 — installazione completa resiliente

Questo comando può essere rilanciato: ignora i passaggi già eseguiti.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Sembri già trovarti in una cartella omega-tail — vedi la sezione Aggiornamento del README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail esiste già, estrazione ignorata." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv esiste già, passaggio ignorato." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail installato. Avvia ./omega-tail.sh."
```

### Metodo 3 — installazione dettagliata

```bash
# 0. Verificare di non rilanciare dall'interno di un omega-tail esistente
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Sembri già trovarti in una cartella omega-tail — vedi la sezione Aggiornamento del README." >&2; exit 1; }

# 1. Estrarre
[ -d omega-tail ] && echo "ℹ️ Già estratto qui, passaggio ignorato." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Spostare nella home
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail esiste già, spostamento ignorato." || mv omega-tail ~/

# 3. Entrare nel progetto
cd ~/omega-tail/

# 4. Creare l'ambiente virtuale
[ -f .venv/bin/activate ] && echo "ℹ️ .venv esiste già, creazione ignorata." || python3 -m venv .venv

# 5. Installare le dipendenze (prima omega-lib inclusa)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Rendere eseguibili i lanciatori
chmod +x omega-tail.sh install.sh

# 7. Scrivere il token di installazione (letto da omega-connect; facoltativo)
./omega-tail.sh synchro jeton

# 8. Avviare
./omega-tail.sh
```

Su Debian, Ubuntu e derivate, il modulo `venv` non è sempre installato con Python:
`sudo apt install python3-venv`.

### Aggiornamento

I servizi di omega-tail (varco, sorveglianza) usano i file di `~/omega-tail/var/`. Un aggiornamento deve quindi
**lasciare questa cartella al suo posto**: l'archivio non contiene `var/` e si estrae sopra l'installazione
esistente.

Dalla cartella che contiene l'archivio, **diversa da `~/omega-tail`**:

```bash
# 1. Salvare l'installazione attuale (var/ compresa)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Estrarre la nuova versione sopra (var/ viene conservata)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Reinstallare (dipendenze, lanciatori, token di installazione)
cd ~/omega-tail
./install.sh

# 4. Riavviare omega-tail
./omega-tail.sh
```

Se il varco è attivo, **Firewall Funnel → « Applica le regole »** ne rigenera la configurazione con la nuova
versione, a caldo. Se la sorveglianza automatica è attivata, **Sopravvivenza → « Attiva la sorveglianza »** la
riavvia con il nuovo codice. Anche omega-connect può eseguire l'aggiornamento (schermata Updater).

### Alias Bash o Zsh

`install.sh` propone l'alias. Per aggiungerlo a mano:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

L'alias si chiama `omega-tail`, e non `tail`, per non nascondere il comando di sistema `tail`.

[↑ Sommario](#sommario)

---

## Utilizzo

### Avvio

```bash
cd ~/omega-tail
./omega-tail.sh

# o semplicemente, se l'alias è stato creato:
omega-tail
```

Il lanciatore non chiede alcuna elevazione: omega-tail gira con il tuo account, e sudo viene chiesto solo dalle
azioni che ne hanno bisogno, nel terminale, con il comando mostrato prima.

### Primi passi consigliati

Per proteggere un sito pubblicato tramite Funnel, in quest'ordine:

1. **Pannello di controllo**: leggere gli avvisi; **Diventa operatore** (una volta, tramite sudo) per configurare
   Tailscale senza sudo.
2. **Sopravvivenza → Applica il confinamento**: `tailscaled` non potrà più prendersi tutta la macchina.
3. **Pubblicazione**: pubblicare il sito in **HTTPS sulla porta 443**, percorso `/`, poi eseguire la **prova
   end-to-end**.
4. **Firewall Funnel → Installa HAProxy**, poi **Attiva la protezione**, prima in modalità **osservazione**.
5. Qualche giorno dopo, **Attacchi e decisioni**: se i contatori mostrano solo abusi, passare il varco in
   modalità **normale**.
6. Lasciare che i **raggruppamenti** imparino per 7 giorni in osservazione, poi passarli ad **applicati**.
7. **Sopravvivenza → Scudo della porta WireGuard**: applicarlo in osservazione, poi passarlo ad attivo.
8. Per una macchina senza nessuno davanti allo schermo: **Sopravvivenza → Attiva la sorveglianza**.

### Lingue dell'interfaccia

17 lingue: francese, inglese, spagnolo, portoghese (Brasile), italiano, tedesco, olandese, polacco, russo,
cinese, vietnamita, thailandese, indonesiano, giapponese, coreano, hindi, arabo.

- Scelta nelle impostazioni (tasto `s`, « Langue / Language », etichetta mai tradotta), applicata riavviando
  solo l'interfaccia.
- Puntualmente: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- Nella console testuale di Linux (TTY), le lingue la cui scrittura non esiste nei font della console vengono
  mostrate in inglese per la sessione; l'arabo viene mostrato da destra a sinistra.
- La **lingua delle esportazioni** (report, lista nera, log) si regola a parte, « Come l'interfaccia » per
  impostazione predefinita.

### Contatti e supporto

L'aiuto (tasto `a`) propone una schermata **Contatti e supporto**:

- *Offrire un caffè* (pagina PayPal dello sviluppatore);
- *Contattare il supporto* (indirizzo e-mail e modulo del sito, mostrati in chiaro);
- *Dichiararmi utente (anonimo)*;
- *Verifica aggiornamenti*.

La dichiarazione è volontaria, disattivata per impostazione predefinita e inviata una sola volta. Serve solo a
contare gli utenti e, se lo si desidera, il loro continente o paese (elenchi chiusi, mai testo libero). Invia una
chiave estratta a caso, il nome del software (`omega-tail`) e la sua versione, mai un nome, un nome di macchina,
un'impostazione o un indirizzo del tailnet. Ritiro in qualsiasi momento dalla stessa schermata (*Non dichiararmi
più*). La verifica degli aggiornamenti legge solo l'elenco delle versioni pubblicate sul sito, e mai senza un clic.

### Collegamenti con gli altri strumenti omega

- **omega-connect**: `install.sh` scrive un token di installazione (`var/omega-jeton.json`) che descrive lo
  strumento e la sua versione, senza eseguire nulla. omega-connect lo usa per il Registro, la sincronizzazione, la
  riparazione, gli aggiornamenti e l'installazione. `./omega-tail.sh synchro jeton` lo riscrive a mano.
- **omega-fire** (3.7.0 o più recente), collegato tramite omega-connect, può applicare e gestire lo scudo della
  porta WireGuard; il suo elenco delle regole lo mostra con l'origine omega-tail.

### Riga di comando

Tutti i comandi si scrivono `./omega-tail.sh …` (o `omega-tail …` con l'alias):

| Comando | Ruolo |
|---|---|
| `omega-tail` | L'interfaccia |
| `omega-tail etat [--format json]` | Stato di Tailscale, della macchina e avvisi, in testo o per uno script |
| `omega-tail aide` | L'aiuto completo in testo |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | Il report, mostrato o salvato |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Interrompere o riattivare Funnel |
| `omega-tail veille etat` | Stato della sorveglianza automatica e le sue ultime righe |
| `omega-tail porte etat` | Stato del varco e contatori |
| `omega-tail porte certificat [--si-besoin]` | Rinnovare il certificato `*.ts.net` del varco |
| `omega-tail porte groupes` | Raggruppamenti: modalità attacco, impronte, AS, paesi |
| `omega-tail porte base` | Aggiornare il database AS / paesi |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Bloccare un indirizzo o una rete (lista nera con `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Sbloccare |
| `omega-tail porte confiance ADRESSE` | Mettere in fiducia |
| `omega-tail synchro jeton` | Scrivere il token di installazione (omega-connect) |
| `omega-tail --version` | La versione |

### Percorso generale

1. Schermata di avvio, poi il menu principale in due colonne (TAILSCALE e PROTEZIONE).
2. Sotto il titolo di ogni schermata, la **barra di stato** riassume tutto: servizio, CPU della macchina e di
   `tailscaled`, temperatura, memoria, Funnel, firewall, sorveglianza, connessione. Viene riletta ogni 5 secondi.
3. Ogni azione che modifica la macchina mostra il suo comando, poi chiede conferma; sudo si digita nel terminale e
   poi l'interfaccia ritorna.
4. Le azioni sensibili (disconnessione definitiva, pulizia completa della lista nera) chiedono di digitare una
   parola.
5. Il risultato viene mostrato in una riga, verificato sullo stato riletto.

### Navigazione

- Frecce su / giù: passare da un elemento all'altro (righe di una tabella, pulsanti).
- Tab / Maiusc+Tab: passare da una zona della schermata all'altra.
- Invio o clic: attivare il pulsante scelto; nella tabella degli avvisi, « Correggi ».
- `Esc`: tornare alla schermata precedente (nel menu: uscire).
- `a`: l'aiuto, da qualsiasi schermata.
- `s`: le impostazioni, da qualsiasi schermata.
- `t`: tema successivo (salvato).
- `r`: ridisegnare la schermata, mostrare la dimensione del terminale e rileggere lo stato.
- `q`: uscire, con conferma.
- `Ctrl+P`: comandi (tema, screenshot in SVG nella cartella degli screenshot, uscire).

[↑ Sommario](#sommario)

---

## Temi e terminali

Dieci temi `omega-*` sono condivisi con il resto della suite OMEGA:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Passa da un tema all'altro con `t`, o scegline uno nelle impostazioni (`s`); la scelta viene conservata.
- Le esportazioni HTML hanno i propri temi: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail adatta la complessità visiva al terminale rilevato tramite un **profilo di rendering**: Completo,
  Standard, Ridotto o Mono (solo ASCII).

| Dimensione minima | Profilo | Terminali tipici |
|---|---|---|
| 120×32 o più | Completo | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 o più | Standard | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 o più | Ridotto | urxvt, xterm, SSH moderno |
| sotto 80×24 | Mono (solo ASCII) | Linux TTY, SSH datato |

Dopo un ridimensionamento, `r` rilegge la dimensione del terminale; viene mostrata in alto, accanto al tema.

[↑ Sommario](#sommario)

---

## File, servizi e compatibilità

### Nella cartella di omega-tail

Tutto lo stato di omega-tail si trova in `~/omega-tail/var/`, ricreato all'avvio e mai pubblicato:

```text
var/
├── settings.json         impostazioni (lingua, temi, cartelle, soglie, regole del varco)
├── omega-jeton.json      token di installazione (omega-connect)
├── porte/                configurazione del varco, certificato, liste di fiducia e nera, database AS / paesi
├── veille/               log della sorveglianza automatica
├── survie/               originali dei file modificati, stato dell'interruttore automatico
├── funnel/sauvegardes/   pubblicazione precedente a ogni modifica (le 50 più recenti)
├── exports/              report, log ed elenchi esportati
└── screenshots/          screenshot (Ctrl+P)
```

### Sul sistema (solo se attivi la protezione corrispondente)

Ogni file viene installato tramite sudo, con il comando mostrato, e rimosso dall'azione inversa in omega-tail.

| File o servizio | Installato da | Rimosso da |
|---|---|---|
| Servizio `omega-tail-porte` (systemd, OpenRC o runit) e `omega-tail-porte-certificat` (timer systemd, o una riga contrassegnata del tuo crontab) | Attiva la protezione | Disattiva la protezione |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (o un gruppo di controllo fuori da systemd) | Applica il confinamento | Rimuovi il confinamento |
| Timer `omega-tail-retablir-*` (riattivazione dopo un'interruzione) | Interruttore automatico | Fine dell'interruzione |
| Servizio `omega-tail-veille` | Attiva la sorveglianza | Disattiva la sorveglianza |
| Servizio `omega-bouclier-wg`, tabella nftables, `/etc/omega-bouclier-wg/` | Scudo: Applica | Scudo: Rimuovi |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | Attiva l'inoltro IP | Eliminazione del file |

Il file `override.conf` di `tailscaled`, se esiste, non viene mai modificato.

### Sistemi di init

| | systemd | OpenRC | runit |
|---|---|---|---|
| Servizio `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Log | `journalctl` | file del servizio | `svlogd`, `socklog` |
| Confinamento | file aggiuntivo systemd | gruppo di controllo (cgroup v2) | gruppo di controllo (cgroup v2) |
| Interruzione temporanea | timer systemd | processo distaccato con il tuo account | processo distaccato con il tuo account |
| Varco, sorveglianza, scudo | servizi systemd | servizi OpenRC | servizi runit |

Fuori da systemd, il confinamento tramite gruppo di controllo si perde se `tailscaled` si riavvia: un avviso
propone allora di riapplicarlo.

### IPv4 e IPv6

Il varco, le liste, i raggruppamenti e lo scudo trattano le due famiglie. I prefissi conteggiati sono /24 in IPv4
e /64 in IPv6; un indirizzo IPv4 visto nella forma `::ffff:a.b.c.d` viene trattato come l'indirizzo IPv4.

[↑ Sommario](#sommario)

---

## Sicurezza

omega-tail agisce su un servizio esposto a Internet; è stato progettato per non peggiorare mai la situazione.

- **Mai root**: l'applicazione, il varco HAProxy e la sorveglianza girano con il tuo account; sudo viene chiesto
  solo per installare o rimuovere un servizio, con il comando mostrato prima.
- **Canali privati**: i socket di amministrazione del varco sono in modalità 600 in una cartella 700; la
  sincronizzazione delle sue tabelle passa da un socket della stessa cartella.
- **Ritorno indietro**: ogni commutazione di Funnel viene salvata, verificata, e lo stato precedente viene
  rimesso in caso di errore.
- **Prima l'osservazione**: il varco, i raggruppamenti e lo scudo si applicano in osservazione; nulla viene
  rifiutato prima che tu l'abbia deciso.
- **Il tailnet non viene mai interrotto**: il varco ammette sempre le tue macchine, e l'interruttore automatico
  interrompe solo Funnel.
- **Input verificati**: solo indirizzi o reti in forma canonica raggiungono HAProxy; i nomi dichiarati dalle
  macchine del tailnet vengono ripuliti prima di essere mostrati.
- **Audit**: il codice è stato sottoposto ad audit (claude-security, 2026-11-25); i 7 punti rilevati, nessuno dei
  quali sfruttabile a distanza da un visitatore, sono stati corretti il giorno stesso.
- Prova prima su una macchina di test o in modalità osservazione, e usa le reti di documentazione RFC 5737
  per le prove IPv4: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Sommario](#sommario)

---

## Test e qualità

La suite conta **179 test**: dominio, casi d'uso, infrastruttura (con un Funnel simulato), schermate Textual con i
veri fogli di stile, sistemi di init, sicurezza. Il codice è verificato da `ruff`, `mypy` e `import-linter` (regole
dei livelli). La cartella `tests/` è inclusa nell'archivio.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

La maggior parte dei test non ha bisogno né di Tailscale, né di HAProxy, né di root.

[↑ Sommario](#sommario)

---

## Stato del progetto

### Punti operativi

- Pilotaggio completo di Tailscale: servizio, connessione, impostazioni, pubblicazione, rete, log.
- Varco HAProxy prima del TLS, in produzione dal 2026-11-23, con regole, liste, raggruppamenti e modalità attacco.
- Sopravvivenza: confinamento, interruttore automatico, sorveglianza automatica.
- Scudo della porta WireGuard, in produzione dal 2026-11-24.
- Report ed esportazioni TXT, HTML, JSON.
- Compatibile con omega-connect e omega-fire.

### Limiti noti

- I servizi con OpenRC e runit sono coperti dai test, ma non ancora convalidati su una macchina reale.
- Il varco protegge un Funnel pubblicato in HTTPS su una sola porta, con il percorso `/`.
- I raggruppamenti richiedono un HAProxy compilato con Lua; senza Lua, il varco funziona senza di essi.
- Lo scudo non può essere applicato su un kernel aggiornato senza riavvio (moduli assenti): la schermata lo
  segnala.
- Un attacco che satura la linea Internet stessa resta fuori dalla portata di uno strumento installato sulla
  macchina.
- Il throughput di un sito pubblicato tramite Funnel resta limitato dai relay di Tailscale e dal router.

[↑ Sommario](#sommario)

---

## Disinstallazione

Rimuovi prima, da omega-tail, ciò che è stato installato sul sistema, in quest'ordine:

1. **Firewall Funnel → Disattiva la protezione** (Funnel viene rimesso com'era prima).
2. **Sopravvivenza → Disattiva la sorveglianza**.
3. **Sopravvivenza → Scudo della porta WireGuard → Rimuovi**.
4. **Sopravvivenza → Rimuovi il confinamento**.

Poi elimina la cartella:

```bash
rm -rf ~/omega-tail
```

Elimina a mano le esportazioni collocate altrove, l'alias `omega-tail` da `~/.bashrc` o `~/.zshrc` e, se l'avevi
attivato, il file `/etc/sysctl.d/99-omega-tail-forwarding.conf`. Il diritto di operatore di Tailscale si ritira
con `sudo tailscale set --operator=`.

[↑ Sommario](#sommario)

---

## Licenza

Omega-Tail è distribuito con licenza **MIT**. Consulta il file [`LICENSE`](../../../LICENSE) per il testo completo.

Il database AS / paesi usa IP Geolocation by [DB-IP](https://db-ip.com), con licenza
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Sommario](#sommario)

---

> **Omega-Tail — Pilotare Tailscale, proteggere Funnel.**
>
> Un'interfaccia TUI per Tailscale, e un varco che rifiuta gli abusi prima di qualsiasi cifratura.
