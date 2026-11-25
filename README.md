<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**Gestionnaire de pilotage TAILSCALE avec pare-feu intégré pour FUNNEL**

OMEGA-TAIL est l'outil de la suite OMEGA qui pilote **Tailscale** sur une machine et la **protège** quand elle
publie un service sur Internet par **Tailscale Funnel**.

> Élaboré par [kraynux](https://github.com/kraynux) pour [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Page officielle](https://kraynux.snake-mackarel.ts.net/omega-tail/) · [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🌐 Interface, documentation, exports et pages visiteurs disponibles en **17 langues** — voir [Langues de l'interface](#langues-de-linterface).  
**Langues :**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](docs/translation/en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](docs/translation/es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](docs/translation/pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](docs/translation/it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](docs/translation/de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](docs/translation/nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](docs/translation/pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](docs/translation/ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](docs/translation/zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](docs/translation/vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](docs/translation/th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](docs/translation/id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](docs/translation/ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](docs/translation/ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](docs/translation/hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](docs/translation/ar/README.md)

---

**OMEGA-TAIL** est une application TUI (Terminal User Interface) Python construite avec
[Textual](https://textual.textualize.io/). Elle permet de gérer et de régler **Tailscale** en mode avancé depuis une
interface, sans retenir une seule commande. Elle ajoute aussi des protections (pare-feu, confinement, survie…) pour
le mode **Funnel**, qui ouvre un service de la machine à tout Internet.

Chaque action qui change la machine montre d'abord sa commande. Le mot de passe sudo se saisit dans le terminal,
action par action, et rien n'est lancé en arrière-plan sans vous.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail/F.png" width="32%" />
</p>

Le projet est conçu selon les principes de la **Clean Architecture**, avec `app/` comme racine de composition : le
domaine métier, l'orchestration, l'infrastructure et l'interface sont séparés.

## Sommaire

- [Présentation](#présentation)
- [Comprendre Tailscale et Funnel](#comprendre-tailscale-et-funnel)
- [Fonctionnalités](#fonctionnalités)
- [Les protections en détail](#les-protections-en-détail)
- [Mesures](#mesures)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Thèmes et terminaux](#thèmes-et-terminaux)
- [Fichiers, services et compatibilité](#fichiers-services-et-compatibilité)
- [Sécurité](#sécurité)
- [Tests et qualité](#tests-et-qualité)
- [État du projet](#état-du-projet)
- [Désinstallation](#désinstallation)
- [Licence](#licence)

---

## Présentation

### Pourquoi omega-tail

Tailscale Funnel publie un service de la machine sur Internet sans ouvrir de port sur la box : les visiteurs
passent par les relais de Tailscale. C'est simple et sûr côté réseau, mais une faiblesse reste.

- **Le coût du chiffrement.** En mode Funnel par défaut, c'est le service `tailscaled` de la machine qui fait la
  poignée de main TLS de chaque visiteur. Mesuré sur une petite machine, c'est environ **80 % du coût d'une
  connexion**. Quelques centaines de nouvelles connexions par seconde suffisent à saturer le processeur : un seul
  ordinateur ordinaire, avec un simple script, peut faire tomber le site et la machine.
- **Des visiteurs invisibles.** Les pare-feu habituels (nftables, ufw, fail2ban) ne voient pas ces visiteurs : ils
  arrivent chiffrés, par le tunnel de Tailscale, avec l'adresse d'un relais.
- **Des réglages éparpillés.** Les réglages de Tailscale (opérateur, nœud de sortie, routes, SSH, bouclier…) sont
  nombreux, répartis entre commandes et console web, et certains peuvent couper la session en cours.

### Objectifs

- Piloter Tailscale entièrement depuis une interface, avec une phrase d'explication pour chaque réglage.
- Refuser les connexions abusives **avant** tout chiffrement, en voyant l'adresse réelle de chaque visiteur.
- Garder la machine debout sous attaque : l'administration et les autres services restent joignables.
- Ne jamais rien imposer : proposer, montrer la commande, demander, et pouvoir revenir en arrière.
- Fonctionner sur toute distribution Linux, sous systemd, OpenRC ou runit.

### Ce que fait omega-tail

- Affiche l'état de Tailscale, de la machine et de ce qui est publié, avec des alertes qui mènent à l'écran qui
  corrige.
- Démarre, arrête et redémarre `tailscaled`, avec un garde-fou si votre session passe par Tailscale.
- Gère la connexion, les comptes et tous les réglages de `tailscale set`, vérifiés avant d'être appliqués.
- Publie, retire, suspend et essaie les services de Serve et de Funnel, avec sauvegardes et restauration.
- Montre les appareils du tailnet, leur chemin (direct ou relayé), un diagnostic réseau et les journaux.
- Place une **porte** HAProxy entre Funnel et votre site : règles par adresse, par préfixe, budget global, listes
  de confiance et noire, regroupements par empreinte JA4, réseau d'origine (AS) et pays, mode attaque automatique.
- Confine `tailscaled`, coupe Funnel un moment ou totalement, et peut le faire seul grâce à une veille automatique.
- Protège le port WireGuard de `tailscaled` par une table nftables (bouclier).
- Produit un rapport de la machine et des attaques des 7 derniers jours, en TXT, HTML ou JSON.

### Ce que le projet ne fait pas

- Il ne remplace pas Tailscale : il le pilote.
- Il ne protège pas contre une attaque volumétrique qui sature la ligne Internet elle-même (la box, le lien).
- Il ne gère pas la console d'administration web de Tailscale (politique d'accès, approbation des nœuds de sortie,
  activation de Funnel pour le tailnet).
- Il ne protège pas un service publié autrement que par Funnel : pour ces ports-là, il y a omega-fire.
- Il ne tourne jamais en root et ne lance rien en arrière-plan sans votre accord.
- Il ne fonctionne ni sous Windows ni sous macOS.

[↑ Sommaire](#sommaire)

---

## Comprendre Tailscale et Funnel

omega-tail suppose quelques notions de Tailscale. Cette partie les rassemble, sans rien supposer d'autre.

### Le vocabulaire

| Terme | Ce que c'est |
|---|---|
| **Tailnet** | Votre réseau privé Tailscale : toutes les machines connectées au même compte (ou à la même organisation). Chaque machine y reçoit une adresse en `100.x.y.z` (plage 100.64.0.0/10) et une adresse IPv6 en `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | Le service (démon) qui tourne sur la machine : il tient le tunnel chiffré WireGuard, la pile réseau de Tailscale et, pour Serve et Funnel, le relais vers vos services. |
| **`tailscale`** | La commande qui pilote `tailscaled` (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail l'utilise pour vous. |
| **WireGuard** | Le protocole de tunnel chiffré utilisé entre les machines. `tailscaled` écoute pour cela sur un port UDP (41641 par défaut), souvent ouvert par la box (UPnP). |
| **Relais DERP** | Des serveurs de Tailscale qui relaient le trafic quand deux machines ne peuvent pas se joindre directement (NAT difficile). Le chemin « direct » est plus rapide. |
| **MagicDNS** | Les noms des machines du tailnet, sous la forme `machine.nom-du-tailnet.ts.net`. |
| **Serve** | Publier un service local (un site, une API…) **pour le tailnet seul**, en HTTPS avec un certificat `*.ts.net` valide. |
| **Funnel** | Publier un service local **pour tout Internet**, à l'adresse `https://machine.nom-du-tailnet.ts.net`. Seuls les ports 443, 8443 et 10000 peuvent être ouverts. |
| **Relais Funnel** | Les serveurs de Tailscale qui reçoivent les visiteurs d'Internet et les font entrer dans votre tailnet (ils apparaissent comme « funnel-ingress-node »). |
| **Opérateur** | Un compte Linux autorisé à régler Tailscale sans sudo (`tailscale set --operator=…`). omega-tail le propose une fois, par sudo. |
| **Nœud de sortie** | Une machine du tailnet par laquelle une autre fait passer tout son trafic Internet (comme un VPN). Il doit être approuvé dans la console de Tailscale. |
| **Sous-réseau annoncé** | Un réseau local (par exemple `192.168.1.0/24`) qu'une machine rend joignable au reste du tailnet. |
| **Bouclier (shields up)** | Réglage de Tailscale qui refuse toutes les connexions entrantes venant du tailnet. |
| **SSH Tailscale** | Un serveur SSH fourni par Tailscale, autorisé par la politique du tailnet. |
| **En-tête PROXY v2** | Une courte entête ajoutée au début d'une connexion pour transmettre l'adresse réelle du visiteur à celui qui la reçoit. |
| **Empreinte JA4** | Une signature de la façon dont un logiciel ouvre une connexion TLS : un navigateur et un outil d'attaque n'ont pas la même. |
| **AS (système autonome)** | Le réseau d'origine d'une adresse : fournisseur d'accès, hébergeur, nuage. |

### Le chemin d'un visiteur

**Funnel par défaut, sans omega-tail.** `tailscaled` fait tout : il déchiffre le tunnel WireGuard, fait la poignée
de main TLS du visiteur, puis relaie la requête en HTTP vers votre site. Aucun pare-feu de la machine ne voit le
visiteur, et chaque nouvelle connexion coûte cher à `tailscaled`.

```text
Visiteur ──HTTPS──▶ Relais Funnel ──WireGuard──▶ tailscaled (TLS + relais HTTP) ──HTTP──▶ votre site
                    (Tailscale)                  └── tout le coût est ici
```

**Funnel avec la porte d'omega-tail.** Funnel passe en mode TCP : `tailscaled` ne fait plus de TLS, il transmet le
flux encore chiffré à la porte, précédé de l'adresse réelle du visiteur (en-tête PROXY v2). La porte décide
**avant** tout chiffrement : une connexion refusée ne coûte presque rien, et seules les connexions admises sont
déchiffrées, par OpenSSL, plus rapide que le TLS de `tailscaled`.

```text
Visiteur ──HTTPS──▶ Relais Funnel ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                      │
                                                      ▼
                                       Porte omega-tail (HAProxy, 127.0.0.1)
                                       ├── refus avant TLS : liste noire, débit, budget, nom visé, regroupements
                                       └── admis : TLS (certificat *.ts.net) ──HTTP──▶ votre site
```

La porte n'écoute que sur la boucle locale de la machine et tourne sous votre compte. Les machines de votre tailnet
y sont toujours admises, avant toute règle : seuls les visiteurs de Funnel sont filtrés.

### Ce que Tailscale doit permettre (console d'administration)

Ces réglages se font une fois, dans la console web de Tailscale ; omega-tail ne les change pas.

- **MagicDNS** et les **certificats HTTPS** activés pour le tailnet (nécessaires à Serve, à Funnel et au certificat
  de la porte).
- **Funnel autorisé** pour la machine dans la politique d'accès du tailnet (attribut `funnel`).
- Pour un nœud de sortie ou des sous-réseaux annoncés : leur **approbation** dans la console.

[↑ Sommaire](#sommaire)

---

## Fonctionnalités

Le menu principal a deux colonnes de six : **TAILSCALE** pour piloter, **PROTECTION** pour défendre.

### TAILSCALE

#### 1. Tableau de bord

- **Tailscale** : service, état de la connexion, version en marche et installée, nom de la machine, adresses,
  compte, appareils en ligne, expiration de la clé, opérateur, nœud de sortie proposé et utilisé, sous-réseaux
  annoncés.
- **Machine** : CPU de toute la machine, charge par cœur, température, mémoire, CPU et mémoire de `tailscaled`,
  confinement, puis l'état des protections (Funnel, pare-feu et mode attaque, liste noire, veille, bouclier).
- **Publication** : chaque port publié, pour Internet (Funnel) ou pour le tailnet (Serve), son mode et sa cible.
- **Alertes**, de la plus grave à la moins grave, avec « Corriger » qui ouvre l'écran concerné. Par exemple :
  service arrêté, mise à jour installée mais pas appliquée, clé qui expire, Funnel publié sans protection,
  température élevée, `tailscaled` trop gourmand ou non confiné, liste noire qui grossit.
- Valeurs en vert, orange ou rouge selon des seuils (CPU, charge, température, mémoire, `tailscaled`).

#### 2. Service tailscaled

- État vu par le système d'init, version en marche et installée, commande de lancement, fichiers d'ajout,
  confinement.
- **Démarrer**, **Arrêter**, **Redémarrer** (par exemple pour appliquer une mise à jour déjà installée).
- **Garde-fou** : si votre session passe par Tailscale (SSH par le tailnet), Arrêter demande une seconde
  confirmation, car vous ne pourriez plus relancer.
- **Corriger le démarrage** : repère un fichier d'ajout qui lance `tailscale up` au démarrage et risque de faire
  sortir la machine du tailnet au premier changement de réglage ; la correction est montrée et l'original gardé.

#### 3. Connexion et réglages

- **Se connecter**, **Se déconnecter**, **Ajouter un compte**, **Changer de compte**, **Déconnexion définitive**
  (nom de la machine à taper).
- **Tous les réglages de `tailscale set`**, chacun avec sa phrase d'explication : nom et surnom de la machine,
  routes, DNS du tailnet, bouclier, filtrage avec état, mode netfilter, nœud de sortie, accès au réseau local,
  proposer la machine comme nœud de sortie, sous-réseaux annoncés, SSH Tailscale, interface web, mises à jour,
  relais pair, opérateur.
- Pendant la saisie, un cadre montre **avant → après** et la commande ; après application, chaque valeur relue est
  marquée ✔ (prise en compte) ou ✖ (non).
- Un avertissement prévient quand un changement peut couper une session passée par Tailscale.
- **Transfert IP** : activé en un bouton quand la machine sert de nœud de sortie ou annonce des sous-réseaux.

#### 4. Publication

- Tout ce que la machine publie : port, public (Funnel) ou tailnet (Serve), mode, chemin, cible, protection.
- **Publier** un service local en HTTPS, HTTP, TCP ou TLS terminé ; **Retirer** ; **Suspendre Funnel** et
  **Rétablir Funnel** (à l'identique).
- **Essai de bout en bout** : une vraie connexion, comme un visiteur (réponse, temps, certificat, version de TLS).
- **Sauvegardes** : l'état d'avant chaque changement (les 50 plus récentes), restaurables.
- Chaque changement est vérifié ; en cas d'écart, la publication est reconstruite, sinon l'état d'avant est remis.

#### 5. Réseau et appareils

- **Appareils** du tailnet : système, en ligne ou non, chemin (direct ou par relais), dernière fois vu, adresse,
  trafic échangé ; les relais Funnel de Tailscale sont cachés par défaut.
- **Ping Tailscale** (chemin et latence), **Qui est-ce ?** (à qui appartient une adresse du tailnet).
- **Diagnostic réseau** : UDP, IPv4 / IPv6, type de NAT, ouverture de port par la box (UPnP, NAT-PMP, PCP), relais le
  plus proche et latences.
- **DNS**, **verrou du tailnet** et **compteurs internes** de Tailscale.
- Lecture seule : rien dans cet écran ne change un réglage.

#### 6. Journaux

- Le journal de `tailscaled` (journalctl, ou les fichiers du service hors systemd) et celui de la porte, filtrables
  et exportables.
- Chaque information a sa couleur, prise dans le thème : date, processus, catégorie du message (contrôle, réseau,
  DNS, moteur WireGuard), adresses en gras, erreurs en rouge, avertissements en orange ; pour la porte, motif de
  refus, regroupement, AS et pays.

### PROTECTION

#### 7. Pare-feu Funnel

- **Installer HAProxy** par le gestionnaire de paquets de la distribution (pacman, apt, dnf, zypper, apk, xbps,
  emerge).
- **Activer la protection** : certificat `*.ts.net`, listes, configuration vérifiée, service de la porte, bascule de
  Funnel puis essai depuis Internet ; en cas d'échec, la publication d'origine est remise aussitôt.
- **Désactiver la protection** : Funnel est remis exactement comme avant, vérifié.
- **Règles** appliquées à chaud, mode **observation** pour régler les seuils sans risque, **regroupements** (voir
  [Les protections en détail](#les-protections-en-détail)).
- **Mettre à jour la base** AS / pays (DB-IP Lite), dans un processus à part.

#### 8. Survie

- **Confinement de `tailscaled`** : plafond CPU, poids et priorité, option de priorité à l'accès SSH.
- **Disjoncteur Funnel** : seuils CPU et température, coupure de 10 minutes (remise en route automatique) ou totale.
- **Veille automatique** : la même chose sans personne devant l'écran.
- **Bouclier du port WireGuard** : bouton vers son écran (observation, actif, poser, reposer, retirer, confier).

#### 9. Attaques et décisions

- Compteurs de la porte (reçues, refusées avant chiffrement, admises, en cours) et adresses les plus actives,
  relus toutes les 2 secondes, avec pays, AS et état de chaque adresse.
- **Bloquer**, **Liste noire**, **Débloquer**, **Confiance** : appliqué tout de suite, sans redémarrer la porte ; la
  notification dit en une ligne l'action et la place de l'adresse.
- Vues **Empreintes**, **AS** et **Pays** ; état du mode attaque et connexions refusées par les regroupements.
- **Gestion de la liste noire** : liste complète avec date d'ajout et origine, ajout, suppression, import d'un
  fichier TXT (doublons, réseaux déjà couverts et adresses du tailnet écartés), purges avec aperçu (par ancienneté,
  les N plus anciennes, une plage de lignes, une origine, tout), exports TXT (réimportable), HTML et JSON.
  Plafond de 50 000 entrées.

#### 10. Rapport

- Tout ce qu'omega-tail sait de la machine, en faits : Tailscale, publication, machine, pare-feu, survie, alertes,
  et les **attaques des 7 derniers jours** lues dans le journal de la porte.
- **Vie privée** : par défaut, sans le compte Tailscale ni les noms et adresses des appareils du tailnet, pour
  pouvoir l'envoyer à quelqu'un.
- Exports **TXT**, **HTML** (thème au choix) et **JSON** ; **Voir les exports** ouvre le dossier dans le navigateur.

#### 11. Réglages

- Langue de l'interface et des exports, thème de l'interface et des exports, dossiers des exports et des captures
  d'écran, et leur purge.

#### 12. Aide

- Une section par écran, les raccourcis, la ligne de commande, et **Contact et support**.

[↑ Sommaire](#sommaire)

---

## Les protections en détail

Chaque protection répond à une menace précise ; aucune n'est imposée.

| Protection | Contre quoi | Où |
|---|---|---|
| Porte (règles) | Rafales depuis une ou quelques adresses, connexions qui ne visent pas le site | Pare-feu Funnel |
| Regroupements | Attaques à adresses dispersées (des milliers d'adresses, une connexion chacune) | Pare-feu Funnel |
| Liste noire | Adresses et réseaux connus pour attaquer, gardés dans la durée | Attaques et décisions |
| Confinement | `tailscaled` qui prendrait toute la machine sous attaque | Survie |
| Disjoncteur | Machine saturée malgré tout : couper Funnel un moment | Survie |
| Veille automatique | Même chose, sans personne devant l'écran | Survie |
| Bouclier WireGuard | Flot de paquets UDP sur le port de `tailscaled`, Funnel ouvert ou non | Survie |

### La porte (Pare-feu Funnel)

Les règles s'appliquent dans cet ordre, toutes avant le chiffrement :

1. **Machines du tailnet** (100.64.0.0/10, fd7a:115c:a1e0::/48) : toujours admises.
2. **Liste de confiance** : jamais limitée. **Liste noire** : refusée jusqu'à son retrait.
3. **Débit par adresse** (40 connexions / 10 s par défaut) : au-delà, l'adresse est bloquée pour la durée choisie
   (60 min par défaut).
4. **Débit par préfixe** /24 en IPv4, /64 en IPv6.
5. **Budget global** de connexions admises par seconde : le processeur n'est jamais débordé.
6. **Nom visé** : une connexion qui ne vise pas le nom de la machine est refusée.

Le certificat `*.ts.net` de la porte est demandé à Tailscale, vérifié chaque jour et renouvelé à chaud 30 jours avant
son échéance. Le mode **observation** compte tout sans rien refuser.

### Les regroupements (empreintes, AS, pays)

Contre une attaque à adresses dispersées, les règles par adresse ne voient chaque adresse qu'une fois. La porte
classe donc aussi chaque client par son **empreinte JA4**, son **AS** et son **pays**, et compte le débit de chaque
groupe.

- **Mode attaque automatique** : au-delà de 80 connexions entrantes par seconde (réglable), la porte passe seule en
  mode attaque, et en sort après 5 minutes de calme.
- En mode attaque seulement : une empreinte inconnue qui explose, un AS d'hébergeur ou de nuage (liste modifiable)
  ou un pays de votre liste (vide par défaut) qui dépasse son débit est refusé.
- Les **navigateurs courants** (Chrome, Edge, Firefox) ne sont jamais touchés par ces règles ; les **clients connus**
  (admis dans les dernières 24 h) passent avant le budget global.
- **Apprentissage** : pendant 7 jours, la porte apprend les empreintes habituelles de votre site (jamais pendant une
  attaque) ; les regroupements restent en observation jusque-là.
- Hors attaque, une connexion sur dix est classée ; en attaque, toutes.
- La base AS / pays est **DB-IP Lite**, téléchargée et mise à jour une fois par mois.

### La survie

- **Confinement** : un fichier d'ajout à part plafonne `tailscaled` (par exemple un cœur entier sur une machine à
  4 fils) et baisse sa priorité. Votre propre configuration n'est jamais modifiée.
- **Disjoncteur** : quand `tailscaled` reste au-dessus du seuil CPU (80 % d'un cœur pendant 60 s par défaut) ou que
  la température atteint 85 °C, omega-tail propose de couper Funnel 10 minutes (remise en route automatique, à
  l'identique, même omega-tail fermé), de le couper totalement, ou d'attendre. Le tailnet n'est jamais coupé.
- **Veille automatique** (désactivée par défaut) : un service sous votre compte coupe Funnel seul après trois
  dépassements, 15 minutes la première fois, 30 la deuxième, puis une heure, et le remet en route seul.

### Le bouclier du port WireGuard

`tailscaled` dépense environ un cœur de processeur pour 100 000 paquets par seconde reçus sur son port UDP, même
invalides. Le bouclier est une table nftables posée devant lui, sur les cartes réseau :

- les **pairs connus** (ceux à qui `tailscaled` écrit) ne sont jamais limités ;
- les poignées de main sont limitées à 20 par seconde et par source ;
- les autres sources ont un budget (500 paquets par seconde chacune, 5 000 en tout) ;
- les paquets qui ne sont pas du WireGuard sont refusés.

Il se pose d'abord en **observation**, puis en **actif**. S'il est relié par omega-connect, **omega-fire** (3.7.0 ou
plus récent) peut le poser et le gérer à la place d'omega-tail : c'est la même table, qui change de mains sans être
touchée.

[↑ Sommaire](#sommaire)

---

## Mesures

Les choix d'omega-tail viennent de mesures, sur des machines de la même génération que celles qu'il protège
(processeurs de 2010 à 2016, sans accélération AES pour la plupart).

| Mesure | Résultat |
|---|---|
| Part du TLS dans le coût d'une connexion Funnel par défaut | environ 80 % |
| Coût d'une connexion **refusée** par la porte, comparé à Funnel par défaut | **4,6 fois moins** |
| Coût d'une connexion **admise** par la porte, comparé à Funnel par défaut | **2 fois moins** |
| Débit avec la porte, connexions gardées ouvertes (comparé à un TLS en Go comme celui de `tailscaled`) | **+15 %** de requêtes, −20 % de CPU |
| Bouclier WireGuard : flot qui prenait un cœur entier à `tailscaled` | **1 %** d'un cœur |
| Mémoire des services (porte, veille, bouclier) | environ 67 Mo |

La porte ne dégrade donc pas le débit d'un site : sur ces machines, c'est le chiffrement lui-même qui limite, avec
ou sans omega-tail, et en production Funnel passe de toute façon par les relais de Tailscale et par la box.

[↑ Sommaire](#sommaire)

---

## Architecture

```text
src/omega_tail/
├── app/              Racine de composition : assemble les couches, point d'entrée (interface, ligne de commande)
├── core/             Constantes partagées
├── domain/           Logique métier pure : règles de la porte, alertes, disjoncteur, veille, liste noire…
├── application/      Cas d'usage : publication, pare-feu, survie, rapport, réglages
├── ports/            Contrats (Protocol) attendus par l'application
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, journaux, exports, scripts Lua
├── interfaces/       tui/ (Textual), cli/ (ligne de commande), shared/ (aide, rapport, présentation)
└── shared/           Langues (gettext)
```

### Principes de conception

- `domain/` ne contient ni lecture ni écriture : tout y est testable sans machine.
- `application/` orchestre les cas d'usage par le domaine et les ports ; l'interface et la ligne de commande
  appellent les mêmes cas d'usage.
- Seuls `infrastructure.commands` et `infrastructure.privileged` lancent des commandes ; l'interface n'en lance
  jamais directement. Ces règles sont vérifiées automatiquement (import-linter).
- L'interface s'appuie sur [omega-lib](https://github.com/kraynux), la bibliothèque partagée par toute la suite
  OMEGA (thèmes, détection du terminal, langues, contact et support, bouclier WireGuard). Elle n'est pas publiée sur
  PyPI : elle est embarquée dans l'archive (`vendor/omega-lib/`).
- Tout appel lent (Tailscale, HAProxy, disque, réseau) tourne en tâche de fond : l'interface ne se fige jamais.

[↑ Sommaire](#sommaire)

---

## Prérequis

### Système

- Linux, toute distribution (testé sur Arch Linux et dérivées).
- Python 3.10 ou supérieur, avec le module `venv`.
- Un système d'init : **systemd**, **OpenRC** ou **runit**.
- `sudo` pour les actions qui changent la machine (demandé action par action, jamais au lancement).
- Un terminal d'au moins 80×24 (voir [Thèmes et terminaux](#thèmes-et-terminaux)).

### Tailscale

- **Tailscale** installé et connecté (client `tailscale` et service `tailscaled`) ; testé avec la version 1.104.
- Pour Funnel : MagicDNS, certificats HTTPS et Funnel autorisés dans la console de Tailscale (voir
  [Ce que Tailscale doit permettre](#ce-que-tailscale-doit-permettre-console-dadministration)).

### Dépendances Python

Installées par `install.sh` dans un environnement virtuel :

- `textual` : l'interface.
- `omega-lib` : bibliothèque partagée de la suite OMEGA, embarquée dans l'archive.

### Composants obligatoires et optionnels

omega-tail détecte ce qui est présent et n'active que ce qui est utilisable.

| Composant | Rôle | Statut |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Tout ce qu'omega-tail pilote | **Obligatoire** |
| Python 3.10+, `textual`, `omega-lib` | L'application | **Obligatoire** |
| systemd, OpenRC ou runit | Services de la porte, de la veille, du bouclier | **Obligatoire** (un des trois) |
| HAProxy 3.x | La porte du Pare-feu Funnel | Optionnel (installable depuis omega-tail) |
| HAProxy avec Lua | Les regroupements (empreintes, AS, pays) | Optionnel (cas des distributions courantes) |
| nftables (noyau avec `nft_limit`) | Le bouclier du port WireGuard | Optionnel |
| Lecture du journal système (groupe `systemd-journal`, `adm` ou `wheel`) | Journaux, rapport des attaques | Recommandé |
| Navigateur et bureau | « Voir les exports » dans le navigateur (sinon, lecture dans omega-tail) | Optionnel |
| omega-connect | Registre, synchronisation, mises à jour de la suite | Optionnel |
| omega-fire 3.7.0+ | Gestion du bouclier WireGuard depuis omega-fire | Optionnel |

[↑ Sommaire](#sommaire)

---

## Installation

L'archive officielle est fournie au format `.tar.gz`. Vérifiez son intégrité avant installation, avec le fichier
`sha.txt` publié à côté :

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Ces trois méthodes servent à une première installation.** Si `~/omega-tail` existe déjà, utilisez la
> section [Mise à jour](#mise-à-jour). Ne relancez jamais ces commandes depuis l'intérieur d'un dossier
> `omega-tail` existant : `tar` créerait un `omega-tail/omega-tail/` imbriqué.

Aucune étape de l'installation ne demande les droits root : omega-tail se lance en utilisateur normal.

### Méthode 1 — script d'installation

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Vous semblez déjà être dans un dossier omega-tail — voir la section Mise à jour du README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Déjà extrait ici, étape ignorée." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail existe déjà, déplacement ignoré." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

Le script crée l'environnement virtuel, installe les dépendances (omega-lib embarquée d'abord), rend les lanceurs
exécutables, écrit le jeton d'installation lu par omega-connect et propose l'alias `omega-tail`. Il peut être
relancé sans risque.

### Méthode 2 — installation complète résiliente

Cette commande peut être relancée : elle ignore les étapes déjà réalisées.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Vous semblez déjà être dans un dossier omega-tail — voir la section Mise à jour du README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail existe déjà, extraction ignorée." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv existe déjà, étape ignorée." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail installé. Lancez ./omega-tail.sh."
```

### Méthode 3 — installation détaillée

```bash
# 0. Vérifier qu'on ne relance pas depuis l'intérieur d'un omega-tail existant
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Vous semblez déjà être dans un dossier omega-tail — voir la section Mise à jour du README." >&2; exit 1; }

# 1. Extraire
[ -d omega-tail ] && echo "ℹ️ Déjà extrait ici, étape ignorée." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Déplacer dans le home
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail existe déjà, déplacement ignoré." || mv omega-tail ~/

# 3. Entrer dans le projet
cd ~/omega-tail/

# 4. Créer l'environnement virtuel
[ -f .venv/bin/activate ] && echo "ℹ️ .venv existe déjà, création ignorée." || python3 -m venv .venv

# 5. Installer les dépendances (omega-lib embarquée d'abord)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Rendre les lanceurs exécutables
chmod +x omega-tail.sh install.sh

# 7. Écrire le jeton d'installation (lu par omega-connect ; facultatif)
./omega-tail.sh synchro jeton

# 8. Lancer
./omega-tail.sh
```

Sur Debian, Ubuntu et dérivées, le module `venv` n'est pas toujours installé avec Python :
`sudo apt install python3-venv`.

### Mise à jour

Les services d'omega-tail (porte, veille) utilisent les fichiers de `~/omega-tail/var/`. Une mise à jour doit donc
**garder ce dossier en place** : l'archive ne contient pas de `var/`, et s'extrait par-dessus l'installation
existante.

Depuis le dossier qui contient l'archive, **autre que `~/omega-tail`** :

```bash
# 1. Sauvegarder l'installation actuelle (var/ compris)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Extraire la nouvelle version par-dessus (var/ est conservé)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Réinstaller (dépendances, lanceurs, jeton d'installation)
cd ~/omega-tail
./install.sh

# 4. Relancer omega-tail
./omega-tail.sh
```

Si la porte est active, **Pare-feu Funnel → « Appliquer les règles »** régénère sa configuration avec la nouvelle
version, à chaud. Si la veille automatique est activée, **Survie → « Activer la veille »** la relance avec le
nouveau code. omega-connect peut aussi faire la mise à jour (écran Updater).

### Alias Bash ou Zsh

`install.sh` propose l'alias. Pour l'ajouter à la main :

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

L'alias s'appelle `omega-tail`, et non `tail`, pour ne pas masquer la commande système `tail`.

[↑ Sommaire](#sommaire)

---

## Utilisation

### Lancement

```bash
cd ~/omega-tail
./omega-tail.sh

# ou simplement, si l'alias a été créé :
omega-tail
```

Le lanceur ne demande aucune élévation : omega-tail tourne sous votre compte, et sudo n'est demandé que par les
actions qui en ont besoin, dans le terminal, avec la commande affichée avant.

### Premiers pas recommandés

Pour protéger un site publié par Funnel, dans cet ordre :

1. **Tableau de bord** : lire les alertes ; **Devenir opérateur** (une fois, par sudo) pour régler Tailscale sans sudo.
2. **Survie → Appliquer le confinement** : `tailscaled` ne pourra plus prendre toute la machine.
3. **Publication** : publier le site en **HTTPS sur le port 443**, chemin `/`, puis faire l'**essai de bout en bout**.
4. **Pare-feu Funnel → Installer HAProxy**, puis **Activer la protection**, d'abord en mode **observation**.
5. Quelques jours plus tard, **Attaques et décisions** : si les compteurs ne montrent que des abus, passer la porte en
   mode **normal**.
6. Laisser les **regroupements** apprendre 7 jours en observation, puis les passer en **appliqués**.
7. **Survie → Bouclier du port WireGuard** : poser en observation, puis passer en actif.
8. Pour une machine sans personne devant l'écran : **Survie → Activer la veille**.

### Langues de l'interface

17 langues : français, anglais, espagnol, portugais (Brésil), italien, allemand, néerlandais, polonais, russe,
chinois, vietnamien, thaï, indonésien, japonais, coréen, hindi, arabe.

- Choix dans les réglages (touche `s`, « Langue / Language », libellé jamais traduit), appliqué en redémarrant
  seulement l'interface.
- Ponctuellement : `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- Dans la console texte Linux (TTY), les langues dont l'écriture n'existe pas dans les polices de la console
  s'affichent en anglais pour la session ; l'arabe s'affiche de droite à gauche.
- La **langue des exports** (rapport, liste noire, journaux) se règle à part, « Comme l'interface » par défaut.

### Contact et support

L'aide (touche `a`) propose un écran **Contact et support** :

- *Payer un café* (page PayPal du développeur) ;
- *Contacter le support* (adresse mail et formulaire du site, affichés en clair) ;
- *Se déclarer utilisateur (anonyme)* ;
- *Vérifier les mises à jour*.

La déclaration est volontaire, désactivée par défaut et envoyée une seule fois. Elle sert seulement à compter les
utilisateurs et, si on le souhaite, leur continent ou leur pays (listes fermées, jamais de texte libre). Elle envoie
une clé tirée au hasard, le nom du logiciel (`omega-tail`) et sa version, jamais de nom, de nom de machine, de
réglage ni d'adresse du tailnet. Retrait à tout moment depuis le même écran (*Ne plus me déclarer*). La vérification
des mises à jour lit seulement la liste des versions publiées sur le site, et jamais sans clic.

### Liens avec les autres outils omega

- **omega-connect** : `install.sh` écrit un jeton d'installation (`var/omega-jeton.json`) qui décrit l'outil et sa
  version, sans rien exécuter. omega-connect l'utilise pour le Registre, la synchronisation, la réparation, les
  mises à jour et l'installation. `./omega-tail.sh synchro jeton` le réécrit à la main.
- **omega-fire** (3.7.0 ou plus récent), relié par omega-connect, peut poser et gérer le bouclier du port WireGuard ;
  sa liste des règles l'affiche avec l'origine omega-tail.

### Ligne de commande

Toutes les commandes s'écrivent `./omega-tail.sh …` (ou `omega-tail …` avec l'alias) :

| Commande | Rôle |
|---|---|
| `omega-tail` | L'interface |
| `omega-tail etat [--format json]` | État de Tailscale, de la machine et alertes, en texte ou pour un script |
| `omega-tail aide` | L'aide complète en texte |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | Le rapport, affiché ou enregistré |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Couper ou remettre Funnel |
| `omega-tail veille etat` | État de la veille automatique et ses dernières lignes |
| `omega-tail porte etat` | État de la porte et compteurs |
| `omega-tail porte certificat [--si-besoin]` | Renouveler le certificat `*.ts.net` de la porte |
| `omega-tail porte groupes` | Regroupements : mode attaque, empreintes, AS, pays |
| `omega-tail porte base` | Mettre à jour la base AS / pays |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Bloquer une adresse ou un réseau (liste noire avec `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Débloquer |
| `omega-tail porte confiance ADRESSE` | Mettre en confiance |
| `omega-tail synchro jeton` | Écrire le jeton d'installation (omega-connect) |
| `omega-tail --version` | La version |

### Parcours général

1. Écran de démarrage, puis le menu principal en deux colonnes (TAILSCALE et PROTECTION).
2. Sous le titre de chaque écran, la **bande d'état** résume tout : service, CPU de la machine et de `tailscaled`,
   température, mémoire, Funnel, pare-feu, veille, connexion. Elle est relue toutes les 5 secondes.
3. Chaque action qui change la machine montre sa commande, puis demande confirmation ; sudo se saisit dans le
   terminal et l'interface revient ensuite.
4. Les actions sensibles (déconnexion définitive, purge complète de la liste noire) demandent de taper un mot.
5. Le résultat s'affiche en une ligne, vérifié sur l'état relu.

### Navigation

- Flèches haut / bas : passer d'un élément à l'autre (lignes d'un tableau, boutons).
- Tab / Maj+Tab : passer d'une zone de l'écran à l'autre.
- Entrée ou clic : activer le bouton choisi ; dans le tableau des alertes, « Corriger ».
- `Échap` : revenir à l'écran précédent (au menu : quitter).
- `a` : l'aide, depuis n'importe quel écran.
- `s` : les réglages, depuis n'importe quel écran.
- `t` : thème suivant (enregistré).
- `r` : redessiner l'écran, afficher la taille du terminal et relire l'état.
- `q` : quitter, avec confirmation.
- `Ctrl+P` : commandes (thème, capture d'écran en SVG dans le dossier des captures, quitter).

[↑ Sommaire](#sommaire)

---

## Thèmes et terminaux

Dix thèmes `omega-*` sont partagés avec le reste de la suite OMEGA :

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Basculez entre les thèmes avec `t`, ou choisissez-en un dans les réglages (`s`) ; le choix est gardé.
- Les exports HTML ont leurs propres thèmes : `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail adapte la complexité visuelle au terminal détecté par un **profil de rendu** : Complet, Standard,
  Réduit ou Mono (ASCII seul).

| Taille minimale | Profil | Terminaux typiques |
|---|---|---|
| 120×32 ou plus | Complet | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 ou plus | Standard | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 ou plus | Réduit | urxvt, xterm, SSH moderne |
| en dessous de 80×24 | Mono (ASCII seul) | Linux TTY, SSH ancien |

Après un redimensionnement, `r` relit la taille du terminal ; elle est affichée en haut, à côté du thème.

[↑ Sommaire](#sommaire)

---

## Fichiers, services et compatibilité

### Dans le dossier d'omega-tail

Tout l'état d'omega-tail est dans `~/omega-tail/var/`, recréé au démarrage et jamais publié :

```text
var/
├── settings.json         réglages (langue, thèmes, dossiers, seuils, règles de la porte)
├── omega-jeton.json      jeton d'installation (omega-connect)
├── porte/                configuration de la porte, certificat, listes de confiance et noire, base AS / pays
├── veille/               journal de la veille automatique
├── survie/               originaux des fichiers modifiés, état du disjoncteur
├── funnel/sauvegardes/   publication d'avant chaque changement (les 50 plus récentes)
├── exports/              rapports, journaux et listes exportés
└── screenshots/          captures d'écran (Ctrl+P)
```

### Sur le système (seulement si vous activez la protection concernée)

Chaque fichier est posé par sudo, commande montrée, et retiré par l'action inverse dans omega-tail.

| Fichier ou service | Posé par | Retiré par |
|---|---|---|
| Service `omega-tail-porte` (systemd, OpenRC ou runit) et `omega-tail-porte-certificat` (minuterie systemd, ou une ligne marquée de votre crontab) | Activer la protection | Désactiver la protection |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (ou un groupe de contrôle hors systemd) | Appliquer le confinement | Retirer le confinement |
| Minuteries `omega-tail-retablir-*` (remise en route après une coupure) | Disjoncteur | Fin de la coupure |
| Service `omega-tail-veille` | Activer la veille | Désactiver la veille |
| Service `omega-bouclier-wg`, table nftables, `/etc/omega-bouclier-wg/` | Bouclier : Poser | Bouclier : Retirer |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | Activer le transfert IP | Suppression du fichier |

Le fichier `override.conf` de `tailscaled`, s'il existe, n'est jamais modifié.

### Systèmes d'init

| | systemd | OpenRC | runit |
|---|---|---|---|
| Service `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Journaux | `journalctl` | fichiers du service | `svlogd`, `socklog` |
| Confinement | fichier d'ajout systemd | groupe de contrôle (cgroup v2) | groupe de contrôle (cgroup v2) |
| Coupure momentanée | minuterie systemd | processus détaché sous votre compte | processus détaché sous votre compte |
| Porte, veille, bouclier | services systemd | services OpenRC | services runit |

Hors systemd, le confinement par groupe de contrôle est perdu si `tailscaled` redémarre : une alerte propose alors
de le remettre.

### IPv4 et IPv6

La porte, les listes, les regroupements et le bouclier traitent les deux familles. Les préfixes comptés sont /24 en
IPv4 et /64 en IPv6 ; une adresse IPv4 vue sous la forme `::ffff:a.b.c.d` est traitée comme l'adresse IPv4.

[↑ Sommaire](#sommaire)

---

## Sécurité

omega-tail agit sur un service exposé à Internet ; il a été conçu pour ne jamais aggraver la situation.

- **Jamais root** : l'application, la porte HAProxy et la veille tournent sous votre compte ; sudo n'est demandé que
  pour poser ou retirer un service, commande montrée avant.
- **Canaux privés** : les sockets d'administration de la porte sont en mode 600 dans un dossier 700 ; la
  synchronisation de ses tables passe par un socket du même dossier.
- **Retour arrière** : chaque bascule de Funnel est sauvegardée, vérifiée, et l'état d'avant est remis en cas
  d'échec.
- **Observation d'abord** : la porte, les regroupements et le bouclier se posent en observation ; rien n'est refusé
  avant que vous l'ayez décidé.
- **Le tailnet n'est jamais coupé** : la porte admet toujours vos machines, et le disjoncteur ne coupe que Funnel.
- **Entrées vérifiées** : seules des adresses ou réseaux sous forme canonique atteignent HAProxy ; les noms déclarés
  par les machines du tailnet sont nettoyés avant d'être affichés.
- **Audit** : le code a été audité (claude-security, 2026-11-25) ; les 7 points relevés, dont aucun exploitable à
  distance par un visiteur, ont été corrigés le jour même.
- Testez d'abord sur une machine de test ou en mode observation, et utilisez les réseaux de documentation RFC 5737
  pour les essais IPv4 : `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Sommaire](#sommaire)

---

## Tests et qualité

La suite compte **179 tests** : domaine, cas d'usage, infrastructure (avec un Funnel simulé), écrans Textual avec les
vraies feuilles de style, systèmes d'init, sécurité. Le code est vérifié par `ruff`, `mypy` et `import-linter`
(règles des couches). Le dossier `tests/` est inclus dans l'archive.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

La plupart des tests n'ont besoin ni de Tailscale, ni d'HAProxy, ni de root.

[↑ Sommaire](#sommaire)

---

## État du projet

### Points opérationnels

- Pilotage complet de Tailscale : service, connexion, réglages, publication, réseau, journaux.
- Porte HAProxy avant TLS, en production depuis le 2026-11-23, avec règles, listes, regroupements et mode attaque.
- Survie : confinement, disjoncteur, veille automatique.
- Bouclier du port WireGuard, en production depuis le 2026-11-24.
- Rapport et exports TXT, HTML, JSON.
- Compatible omega-connect et omega-fire.

### Limites connues

- Les services sous OpenRC et runit sont couverts par les tests, mais pas encore validés sur une vraie machine.
- La porte protège un Funnel publié en HTTPS sur un seul port, avec le chemin `/`.
- Les regroupements demandent un HAProxy compilé avec Lua ; sans Lua, la porte fonctionne sans eux.
- Le bouclier ne peut pas être posé sur un noyau mis à jour sans redémarrage (modules absents) : l'écran le dit.
- Une attaque qui sature la ligne Internet elle-même reste hors de portée d'un outil installé sur la machine.
- Le débit d'un site publié par Funnel reste limité par les relais de Tailscale et par la box.

[↑ Sommaire](#sommaire)

---

## Désinstallation

Retirez d'abord, depuis omega-tail, ce qui a été posé sur le système, dans cet ordre :

1. **Pare-feu Funnel → Désactiver la protection** (Funnel est remis comme avant).
2. **Survie → Désactiver la veille**.
3. **Survie → Bouclier du port WireGuard → Retirer**.
4. **Survie → Retirer le confinement**.

Puis supprimez le dossier :

```bash
rm -rf ~/omega-tail
```

Supprimez à la main les exports placés ailleurs, l'alias `omega-tail` de `~/.bashrc` ou `~/.zshrc`, et, si vous
l'aviez activé, le fichier `/etc/sysctl.d/99-omega-tail-forwarding.conf`. Le droit d'opérateur de Tailscale se retire
par `sudo tailscale set --operator=`.

[↑ Sommaire](#sommaire)

---

## Licence

Omega-Tail est distribué sous licence **MIT**. Consultez le fichier [`LICENSE`](LICENSE) pour le texte complet.

La base AS / pays utilise IP Geolocation by [DB-IP](https://db-ip.com), sous licence
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Sommaire](#sommaire)

---

> **Omega-Tail — Piloter Tailscale, protéger Funnel.**
>
> Une interface TUI pour Tailscale, et une porte qui refuse les abus avant tout chiffrement.
