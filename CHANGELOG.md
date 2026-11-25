<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [0.7.0] — en cours

### Ajouté
- **Interface en 17 langues** (lot 9, 2026-11-25) : français, anglais, espagnol, portugais (Brésil), italien, allemand,
  néerlandais, polonais, russe, chinois, vietnamien, thaï, indonésien, japonais, coréen, hindi, arabe.
  - 1 056 phrases par langue (écrans, aide F1, messages, ligne de commande, exports), traduites avec les mêmes mots que
    le README de chaque langue (glossaires `~/DEV/TAIL/outils-i18n/glossaires/`).
  - Les messages d'action traduisent aussi leur raison (« HAProxy absent », « cible non prise en charge : … ») ; les
    phrases faites de morceaux ont été réécrites en phrases entières.
  - La **ligne de commande** suit la langue choisie (réglages ou `OMEGA_TAIL_LANG`) ; la veille automatique garde
    son journal en français.
  - Les **exports** (rapport, aide HTML, liste noire) sortent dans la « Langue des exports », avec `lang` et `dir`
    de la langue (droite à gauche en arabe).
  - Tests : catalogues complets et sans variable perdue, catalogue de référence à jour du code, écrans ouverts en
    allemand, japonais et arabe.
  - Les 16 langues sont marquées **validées** (plus « en test » dans le sélecteur) : vocabulaire et ton (vous/tu selon
    l'usage de chaque langue, le même que son README) vérifiés.
- **Compatible omega-connect** : `omega-tail.sh synchro jeton [--format json]`
  écrit la carte d'identité `var/omega-jeton.json` (jamais en root, même format que les autres outils) ; `install.sh`
  la pose à chaque installation ou mise à jour (un échec ne bloque jamais). omega-connect le reconnaît au Registre,
  le synchronise, le répare, le met à jour et l'installe (omega-lib 0.4.1). `build-release.sh` construit
  `omega-tail-<version>.tar.gz` dans `../html/download/` avec son empreinte dans `sha.txt` (var/ et documents de
  travail exclus, omega-lib embarquée).
- **« Se déclarer »** (Contact et support) : omega-tail fait partie des logiciels acceptés (omega-lib 0.4.1 et
  script de réception).
- **Gestion de la liste noire**. Nouvel écran ouvert
  depuis « Attaques et décisions » (seconde ligne de boutons) :
  - toute la liste, avec la date d'ajout et l'origine de chaque entrée (`var/porte/noire.json` ; `noire.lst`, lu
    par HAProxy, en est généré), filtrable ;
  - ajouter une adresse ou un réseau en prévision, supprimer une entrée ;
  - importer un fichier TXT : doublons, adresses déjà couvertes par un réseau et adresses du tailnet écartés et
    comptés, lignes invalides citées ;
  - purger avec aperçu puis confirmation : plus anciennes que N jours, les N plus anciennes, une plage de lignes,
    une origine, ou tout (confirmation tapée) ;
  - exporter TXT (réimportable tel quel, pour une récidive), HTML (thèmes d'export d'omega-lib) ou JSON.
  - Plafond de 50 000 entrées, alerte au tableau de bord à 25 000. HAProxy en tiendrait bien plus ; c'est
    omega-tail qui ralentirait. Une liste d'avant cette version reçoit la date de son fichier.
- **Tableau de bord complet et coloré** : libellés dans la couleur d'accent, valeurs en vert, orange ou rouge
  selon des seuils (CPU machine, charge par cœur, température, mémoire, tailscaled, liste noire). Le cadre
  MACHINE reprend tout l'état de la bande (Funnel, pare-feu et mode attaque, liste noire, veille, bouclier du
  port WireGuard) ; le cadre TAILSCALE dit aussi nœud de sortie proposé ou utilisé et sous-réseaux annoncés.
- **CPU de la machine** : la bande d'état sépare « CPU machine » (toute la machine, lu dans /proc/stat) et
  « CPU tailscaled » (le seul service). Avant, le seul « CPU » affiché était celui de tailscaled.

### Modifié
- **Journaux lisibles** (2026-11-25, demande) : chaque information a sa couleur, prise dans le thème,
  comme le viewer d'omega-serv. tailscaled : date, machine grisée, processus, catégorie du message par famille
  (contrôle, réseau et relais, DNS, moteur WireGuard), adresses en gras, erreurs en rouge, avertissements en orange.
  Porte : adresse du visiteur, état de fin, motif de refus, regroupement, AS, pays. Recoloré au changement de thème.
  Aide F1 et README ×17 à jour ; `interfaces/tui/screens/journal_highlight.py`, `tests/test_journal_couleurs.py`.
- **Libellés traduits et alignements** (2026-11-25, relevés sur les captures) : vue « Empreintes », motifs
  (empreinte, hébergeur, pays), « habituelle », navigateurs reconnus, « (hébergeur) » après le nom d'un AS et unités
  (Ko, Mo, Go) passent par la langue ; tableau de bord aligné à la largeur d'écran (japonais, chinois, coréen, thaï,
  hindi) ; ligne PURGER de la liste noire resserrée (plus de débordement à 140 colonnes).
  `tail_catalog.py update` garde le statut « validé » des catalogues (il le perdait) ; test ajouté.
- **Attaques et décisions** : chaque notification dit en une ligne l'action et la place de l'adresse
  (« 1.2.3.4 → liste noire (refusée jusqu'au retrait) », « → bloquée 60 min », « → confiance »…). Titre remonté
  et marges réduites ; la phrase « la notification dit où se trouve l'adresse » est retirée.
- **Mettre à jour la base AS / pays** : la préparation tourne dans un processus à part, avec un indicateur
  d'attente. Lancée dans un fil, elle figeait l'écran.
- **Sections séparées par une barre aux couleurs du thème** , et titres décollés
  des boutons qui les précèdent : Survie (confinement, veille, bouclier, disjoncteur), Pare-feu Funnel (règles,
  regroupements, listes), Publication (ajouter, sauvegardes), Connexion et réglages (compte ; une ligne d'air
  avant Identité et les autres groupes), Réseau et appareils (diagnostic réseau). Le bouton du bouclier est
  collé à sa description.
- **Accueil** : une ligne d'air entre le haut de l'écran et le logo.
- **Écran Attaques avec une grande liste noire** : les adresses sont classées en une passe, sans relire toute la
  liste pour chaque ligne (50 000 entrées : 0,2 s au lieu de 1 s, toutes les 2 s).
- **Le tailnet est toujours admis par la porte**. Les machines Tailscale
  (100.64.0.0/10 et fd7a:115c:a1e0::/48) passent avant toute règle : jamais comptées, limitées ni bloquées. La porte
  ne filtre que les visiteurs de Funnel, qui arrivent avec leur adresse publique. Bloquer ou mettre en liste noire
  une adresse du tailnet est refusé, puisque cela n'aurait aucun effet. Constaté en production : 300 requêtes
  d'essai depuis une machine du tailnet l'avaient bloquée 60 minutes.
- **Bouclier du port WireGuard** (lot 8, bouton dans « Survie »). C'est une table nftables posée devant tailscaled,
  sur les cartes réseau matérielles. Sans lui, tailscaled dépense environ un cœur pour 100 000 paquets par seconde,
  même invalides, Funnel ouvert ou non. Avec lui, un flot qui prenait un cœur entier n'en prend plus que 1 %
  (mesuré sur le J3455).
  - Ce qu'il fait : il limite les poignées de main par source et met un budget sur les sources qui ne sont pas des
    pairs connus. Les pairs connus sont appris par le noyau et ne sont jamais limités. Les paquets qui ne sont pas
    du WireGuard sont refusés.
  - **Observation d'abord** : rien n'est refusé, les compteurs disent ce qui l'aurait été.
  - **Qui le pose** : omega-fire 3.7.0 ou plus récent s'il est relié par omega-connect (sa liste des règles
    l'affiche avec l'origine omega-tail). Sinon, omega-tail le pose lui-même, même si ufw ou firewalld sont
    présents.
  - C'est la même table dans les deux cas (omega-lib 0.4.0, décision D-018). « Confier à omega-fire » et, dans
    omega-fire, « Reprendre la gestion » la font changer de mains sans la toucher. Si omega-fire n'est plus relié,
    « Reprendre la gestion » la rend à omega-tail.
  - Un service `omega-bouclier-wg` (systemd, OpenRC, runit) la remet en place à chaque démarrage et écrit son
    état chaque minute, lisible sans droits.
  - Si un autre outil efface la table, une alerte apparaît au tableau de bord et une ligne dans le journal de la
    veille. La table n'est jamais reposée seule : « Reposer ».
  - Un bouclier retiré depuis omega-fire est affiché comme tel.
  - Le bouclier figure aussi dans le rapport et dans `omega-tail etat`.
  - Essai réel sur le J3455 (2026-11-24) : le noyau regroupe les rafales de paquets identiques avant la table
    (GRO). Les limites se comptent donc en octets, et un groupe compte pour un paquet dans les compteurs.
  - Noyau mis à jour sans redémarrage (constaté en production) : la table ne peut pas être posée. L'écran le dit,
    et « Poser » et « Reposer » refusent d'avance au lieu d'échouer en cours de route.

- **Mémoire de la TUI** (mesures du 2026-11-25, `MESURES_DEBIT_MEMOIRE.md`) : la base AS / pays est lue directement
  dans les octets de `geo.bin`, comme le fait le Lua de la porte, au lieu d'être convertie en 1,35 million d'objets
  Python. **15 Mo au lieu de 207**, chargement en 10 ms au lieu de plusieurs secondes, mêmes réponses (vérifié sur
  150 008 adresses). Sur une machine en production, la TUI passait de 54 Mo au lancement à 330 Mo une fois « Attaques » ouvert.
- **Tables de la porte bornées** : 200 000 adresses (au lieu d'un million) et 100 000 préfixes (au lieu de 200 000).
  Une adresse suivie coûte environ 214 octets : sous une attaque très distribuée, HAProxy pouvait monter à 256 Mo,
  contre environ 45 + 20 Mo au plus désormais. Pleine, une table évince ses entrées les plus anciennes (vérifié sur
  HAProxy 3.4) : une adresse qui attaque encore reste suivie.
- **Écartés après mesure** :
  - **un seul étage HAProxy** : avant la poignée de main TLS, ses règles ne voient pas encore l'adresse réelle
    (l'en-tête PROXY n'est pas lu), et celles qui la voient ne s'exécutent qu'après le TLS. On perdrait le refus
    avant TLS, qui est le rôle de la porte ;
  - **le cœur natif C++ (phase deux)** : la porte HAProxy ne dégrade pas le débit par rapport à Funnel sans
    omega-tail (+15 % de requêtes, −20 % de CPU). Un cœur natif gagnerait au mieux 15 à 20 % du CPU de la seule porte,
    qui n'est pas le goulot (décision, 2026-11-25).

### Sécurité
Audit claude-security du 2026-11-25 (rapport `CLAUDE-SECURITY-20261125-075456/`) : 7 failles relevées, toutes
corrigées le jour même. Aucune n'était exploitable à distance par un visiteur anonyme.
- **Plus aucune vérification de la configuration en root** (F1 MEDIUM, F2 LOW). Le service runit et le service
  OpenRC de la porte lançaient `haproxy -c` en root sur la configuration et les scripts Lua du dossier de la porte,
  que le compte du service peut modifier. Un processus de ce compte pouvait donc devenir root. La vérification se
  fait maintenant sous le compte de l'utilisateur (`chpst -u` pour runit, `su -s /bin/sh -c` pour OpenRC).
  systemd n'était pas concerné (`User=` s'applique déjà à `ExecStartPre`). Sous runit ou OpenRC, relancez une
  fois « Activer la porte » pour réécrire le service.
- **Liste noire : identifiants de zone IPv6 refusés** (F3 LOW). Python accepte `fe80::1%x;commande` comme
  adresse IPv6. Une telle ligne dans un fichier importé, une fois retirée ou débloquée, enchaînait une seconde
  commande sur le socket d'administration d'HAProxy (arrêt de la porte, effacement des blocages). Seules les formes
  canoniques (chiffres, `.`, `:`, préfixe) sont acceptées à l'import, à l'ajout et dans les écrans. Une entrée
  piégée déjà présente est écartée des deux fichiers. Une commande qui contient `;` ou un retour à la ligne est
  refusée avant le socket.
- **Synchronisation des tables par un socket privé** (F4 LOW). Les tables de blocage passaient au nouveau
  processus, lors d'un rechargement, par un port TCP local (port de la porte + 1) sans authentification. N'importe
  quel compte de la machine pouvait y lever ou poser des blocages. Elles passent maintenant par
  `var/porte/pairs.sock`, dans le dossier 700 de la porte. Vérifié en réel : un blocage survit au rechargement.
  Au premier rechargement après la mise à jour, les blocages temporaires en cours sont perdus une fois ; la liste
  noire n'est pas touchée.
- **Service publié en `https://` : certificat vérifié** (F5 LOW). La porte écrivait toujours `ssl verify none`
  vers le service d'origine, alors que tailscaled vérifie le certificat d'une cible `https://` (seul
  `https+insecure://` s'en passe). La porte fait maintenant comme tailscaled : `https://` vérifié par les autorités
  du système, plus le nom quand la cible en donne un. Vérifié en réel : un faux service à certificat auto-signé est
  refusé (503).
- **`install.sh`** (F6 LOW) : le journal d'erreur de création du venv est créé par `mktemp`, jamais sous un nom fixe
  dans `/tmp`.
- **Noms des machines du tailnet** (F7 LOW) : chaque machine déclare elle-même son nom et son système. Les
  caractères de contrôle (séquences ANSI et OSC, inversions de sens) en sont retirés à la lecture. Le rapport
  texte écrit dans le terminal en est aussi nettoyé.

## [0.6.0] — en cours

### Ajouté
- **Réseau et appareils** (lot 7) : appareils du tailnet (système, en ligne, chemin direct ou par relais, dernière
  fois vu, adresse, trafic), filtre, relais Funnel de Tailscale cachés par défaut ; **ping Tailscale** et **qui
  est-ce ?** sur la ligne choisie (nom ou adresse vérifié avant d'être passé à Tailscale) ; **diagnostic réseau**
  (UDP, IPv4 / IPv6, NAT, ouverture de port par la box, relais le plus proche) ; DNS, verrou du tailnet, compteurs
  internes. Lecture seule. Taildrop et partages : plus tard.
- **Rapport** (lot 7) : Tailscale, publication, machine, pare-feu, survie, alertes et **attaques des 7 derniers
  jours** (journal de la porte : motifs, jours, adresses avec AS et pays) ; export TXT / HTML / JSON ;
  `omega-tail rapport [--format] [--prive] [--exporter]`. Compte et appareils du tailnet seulement sur demande
  (case à cocher), les adresses des attaquants toujours.
- **Voir les exports** (Rapport et Journaux) : le dossier des exports dans le navigateur (méthode commune de la
  suite) ; sans navigateur, liste et lecture dans omega-tail.

### Corrigé
- Les connexions refusées dès l'ouverture (liste noire, budget, débit) n'avaient pas leur motif dans le journal de
  la porte (HAProxy les journalise à part) : format dédié, vérifié avec le vrai HAProxy. Prend effet au prochain
  « Appliquer » des règles ou des regroupements.

### Architecture
- Ce que la ligne de commande et l'interface partagent (aide, présentation, rendu des exports et leurs thèmes) est
  dans `interfaces/shared/` ; `interfaces/cli` et `interfaces/tui` ne dépendent plus l'une de l'autre (contrat).
- Les commandes de la machine ne sont lancées que depuis `infrastructure/commands.py` et
  `infrastructure/privileged/` (le point d'entrée et l'écriture de la crontab passaient encore par `subprocess`) ;
  6 contrats import-linter au lieu de 4. Aucun changement de comportement.

## [0.5.0] — 2026-11-23 (non publiée)

### Ajouté
- **Regroupements** (Pare-feu, lot 6) contre les attaques à adresses dispersées : empreinte **JA4** de chaque
  client calculée par la porte AVANT tout chiffrement (script Lua d'omega-tail, spécification FoxIO), **AS** et
  **pays** de l'adresse réelle (base DB-IP Lite compactée : +17 Mo dans HAProxy au lieu de +630 Mo en plages
  CIDR, mesuré), débit compté par groupe.
- **Mode attaque automatique**, décidé par HAProxy : au-delà du seuil de connexions entrantes, empreintes
  inconnues qui explosent, AS d'hébergeurs et pays choisis (liste vide par défaut) limités ; navigateurs courants
  jamais touchés ; clients connus avant le budget global ; retour au normal après le temps de calme.
- **Référence apprise** des empreintes habituelles (7 jours, jamais pendant une attaque) ; **observation** par
  défaut (« aurait été refusée ») ; une connexion sur dix classée hors attaque (calcul ÷10).
- Apprentissage et observation liés : tant que la référence n'est pas prête, les regroupements restent en
  observation même si « appliqués » est choisi (avertissement avec les jours restants) ; « Recommencer
  l'apprentissage » les remet en observation ; le cadre d'état dit quand « appliqués » devient possible.
- Base AS / pays mise à jour chaque mois par la veille automatique, ou par bouton ; `omega-tail porte groupes`,
  `omega-tail porte base`.
- Attaques et décisions : pays et AS de chaque adresse, ligne du mode attaque, vues Empreintes / AS / Pays.
  Bande d'état « Pare-feu actif · attaque » et alerte au tableau de bord.
- Vérifié avec le vrai HAProxy (3.4) : JA4 identique à la référence Python et à l'exemple de FoxIO (Chromium et
  Firefox réels : `8daaf6152771`), pays / AS identiques sur 308 adresses, rafale dispersée depuis un nuage
  refusée (« empreinte ») pendant que des navigateurs passent.

## [0.4.0] — 2026-11-23 (non publiée)

### Ajouté
- **Veille automatique** (Survie, désactivée par défaut) : pour une machine sans personne devant, un service sous
  le compte de l'utilisateur (systemd, OpenRC, runit) compte les dépassements des seuils du disjoncteur ; 3 dans
  la fenêtre (10 min) → Funnel coupé seul 15 min, puis 30 min, puis 1 h renouvelable, et remis seul à l'identique ;
  retour à 15 min après 24 h sans coupure ; journal dans Survie, `omega-tail veille etat`, alerte si elle s'arrête.
  Validée en réel sur le J3455 (vrai Tailscale, paliers raccourcis pour l'essai). Section placée juste sous le
  confinement (avant le disjoncteur), visible dès l'ouverture de Survie.
- Bande d'état : « Pare-feu actif / arrêté / inactif », « Veille active / arrêtée / inactive », et la mémoire
  vive utilisée (« RAM 42 % », orange dès 85 %, rouge dès 95 %) à côté de la température.
- Bande d'état dans son propre cadre (« État »), bien séparée du titre ; sur une fenêtre étroite elle passe à la
  ligne entre deux voyants au lieu de couper la fin.
- Taille de la fenêtre dans le sous-titre (« thème | 120x50 »), comme les autres outils de la suite ; « r » la relit.
- **Connexion et réglages** : état de la connexion ; se connecter, se déconnecter, ajouter un compte, changer de
  compte, déconnexion définitive (confirmée en tapant le nom de la machine) ; les réglages de `tailscale set` en
  cases et champs, chacun expliqué (nom de la machine, surnom, routes, DNS, bouclier, filtrage, netfilter, nœud de
  sortie, sous-réseaux annoncés, SSH Tailscale, interface web, mises à jour, relais pair, opérateur). Valeurs
  vérifiées ; les changements en attente s'affichent pendant la saisie (avant → après et commande) dans un
  cadre au-dessus des boutons, masqué quand il n'y a rien ; « Appliquer » dans le terminal, sans sudo pour
  l'opérateur ; le résultat reste écrit, vérifié sur les valeurs relues (✔ / ✖). Avertissement quand un changement peut couper une session passée par Tailscale.
  Bouton « Mon compte » à côté du champ Opérateur : remplit votre nom de compte Linux (celui d'avant sudo).
  Nœud de sortie : phrase d'explication quand aucune machine du tailnet ne se propose. Transfert IP : détecté (/proc),
  avertissement quand la machine se propose comme nœud de sortie ou annonce des sous-réseaux sans lui, bouton
  « Activer le transfert IP » (fichier à part dans /etc/sysctl.d, gardé au redémarrage sous systemd, OpenRC, runit) ;
  l'alerte « IP forwarding is disabled » du tableau de bord mène à cet écran.
- Interface (retours d'utilisation) : plus de petit cadre vide dans la barre du tableau de bord quand « Devenir
  opérateur » est masqué ; les champs vides montrent un exemple atténué (on voit où le champ commence et finit) ;
  flèche des listes déroulantes en couleur vive, comme omega-serv.
- Attaques et décisions : la colonne État dit où se trouve chaque adresse (liste noire, bloquée, admise,
  confiance) ; une adresse en liste noire n'apparaît plus « admise », celles des listes sans connexion récente
  sont affichées ; « Confiance » devient « Retirer la confiance » sur une adresse en confiance. Les
  notifications disent où se trouve l'adresse après l'action (et si la porte est arrêtée). Les deux listes
  sont exclusives (liste noire ↔ confiance : l'adresse est déplacée) ; bloquer une adresse en confiance est
  refusé avec la raison (la confiance passe avant dans HAProxy).
- **Publication** : tout ce que Serve et Funnel publient (port, public, mode, chemin, cible, protégé par la porte
  ou non) ; publier un service local pour le tailnet ou pour Internet ; retirer un chemin ou un port ; suspendre et
  rétablir Funnel ; essai de bout en bout par le chemin public (réponse, temps, certificat, TLS) ; sauvegarde de
  l'état d'avant chaque changement et restauration en un bouton. Chaque changement est vérifié ; si le résultat
  n'est pas celui voulu (autorisation Funnel restée derrière un retrait TCP, constatée en réel), la publication est
  reconstruite, sinon remise comme avant.

### Corrigé
- tailscaled ne redémarrait plus quand un fichier d'ajout de l'utilisateur lance `tailscale up` (ExecStartPost)
  après un changement de réglage (opérateur…) : Tailscale refuse le `up` incomplet, systemd abandonne (constaté en
  production, au redémarrage du confinement). Alerte au tableau de bord, « Corriger le démarrage »
  dans Service (« - » devant la commande, original gardé), correction faite d'abord avant tout redémarrage.
- Disjoncteur : un port Funnel en TCP (celui de la porte) gardait son autorisation Funnel après la coupure
  (`--tcp=PORT off` ; Tailscale annonçait toujours « Funnel on ») : la coupure repart désormais de zéro avec les
  seuls points du tailnet et vérifie que plus rien n'est ouvert à Internet (constaté et validé sur le J3455).
- Seuil « tenu pendant N s » jamais atteint pour une durée courte (mesures jamais pile à l'heure) : marge
  d'une mesure.

## [0.3.0] — 2026-11-23 (non publiée)

### Ajouté
- **Pare-feu Funnel** (porte HAProxy, installé par le gestionnaire de paquets) : Funnel passe en TCP + PROXY v2
  vers la porte, qui voit l'adresse réelle de chaque visiteur et décide AVANT tout chiffrement (liste de confiance,
  liste noire, blocage temporaire, débit par adresse et par préfixe /24 ou /64, budget global, nom visé), puis ne
  chiffre que les connexions admises. Mode observation. Activation pas à pas avec essai depuis Internet et retour
  arrière automatique ; désactivation à l'identique. Porte et renouvellement du certificat en services systemd sous
  le compte de l'utilisateur. Règles et listes appliquées à chaud, adresses bloquées gardées au rechargement.
- **Attaques et décisions** : compteurs et adresses les plus actives en direct ; bloquer, liste noire, débloquer,
  confiance.
- Journal de la porte dans « Journaux » ; alerte « site en panne » si Funnel passe par une porte arrêtée.
- Ligne de commande : `omega-tail porte etat | certificat [--si-besoin] | bloquer | debloquer | confiance`.
- **systemd, OpenRC et runit** (règle de la suite) : détection du système d'init (reprise d'omega-serv) ; service
  `tailscaled` par `systemctl`, `rc-service` ou `sv` ; journaux par journalctl ou par fichiers ; confinement par
  fichier d'ajout systemd ou, ailleurs, par un groupe de contrôle cgroup v2 à part (perte au redémarrage signalée) ;
  remise en route programmée par `systemd-run` ou par un processus détaché sous le compte de l'utilisateur ; porte
  en service systemd, OpenRC (supervise-daemon) ou runit, renouvellement du certificat par minuterie systemd ou
  ligne marquée de la crontab de l'utilisateur. Installation d'HAProxy aussi par apk, xbps et emerge.

## [0.2.0] — 2026-11-22 (non publiée)

### Ajouté
- **Survie** : confinement de tailscaled par un fichier d'ajout systemd séparé (`50-omega-tail.conf`, plafond CPU,
  poids, priorité ; aperçu et commandes montrés avant), option de priorité pour l'accès SSH, retrait en un bouton ;
  votre `override.conf` n'est jamais modifié.
- **Disjoncteur Funnel** qui propose sans jamais imposer : au-dessus du seuil CPU de tailscaled pendant toute la
  durée choisie, ou au seuil de température, omega-tail propose une coupure momentanée (10 min par défaut, remise en
  route automatique à l'identique, même omega-tail fermé) ou une coupure totale. Seuls les ports ouverts à Internet
  sont coupés ; le tailnet reste. Publication sauvegardée avant chaque coupure, remise en route vérifiée identique.
- Alertes « Funnel coupé », « remise en route en retard », « coupure totale ».
- Ligne de commande : `omega-tail disjoncteur etat | couper --minutes N | couper --totale | retablir`.

## [0.1.0] — 2026-11-22 (non publiée)

### Ajouté
- Écran de démarrage et menu principal (Tailscale | Protection, 6 + 6).
- Tableau de bord : santé de Tailscale, publications, machine, alertes menant à l'écran qui corrige.
- Service tailscaled : état systemd, versions, confinement (lecture), démarrer / arrêter / redémarrer avec
  garde-fou quand la session passe par Tailscale.
- Journaux de tailscaled.
- Droit d'opérateur de Tailscale proposé (une fois, par sudo dans le terminal).
- Réglages (langue, thèmes, dossiers), aide, Contact et support.
- Ligne de commande : `omega-tail etat` (texte ou JSON).
