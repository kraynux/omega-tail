#!/usr/bin/env bash
# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
# ==============================================================================
# Script d'installation - OMEGA-TAIL TUI/CLI
# À lancer depuis le dossier extrait de l'archive : cd omega-tail && ./install.sh
# Résilient : peut être relancé sans erreur si une étape a déjà été faite.
# Aucune étape ne nécessite les privilèges root : Omega-Tail se lance en utilisateur normal
# (sudo est demandé action par action, dans le terminal, commande affichée avant).
# ==============================================================================

set -e

# Couleurs (mêmes conventions que les autres scripts de la suite omega-)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${CYAN}ℹ️  $1${NC}"; }
ok()   { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
err()  { echo -e "${RED}❌ $1${NC}"; }
tip()  { echo -e "${WHITE}💡 $1${NC}"; }

echo -e "${WHITE}    ░▒▓███████████████████████████████████████████████▓▒░${NC}"
echo -e "${WHITE}    ░▒▓ Ω M E G A - TAIL — I N S T A L L A T I O N    ▓▒░${NC}"
echo -e "${WHITE}    ░▒▓███████████████████████████████████████████████▓▒░${NC}"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# -------------------------------------------------------------------------
# 1. Environnement virtuel Python
# -------------------------------------------------------------------------
# .venv casse (creation interrompue : pas de bin/activate) : mis de cote, jamais supprime, puis recree
# (constate le 2026-11-11 sur une autre machine : l'installation echouait sur « activate »).
if [ -d ".venv" ] && [ ! -f ".venv/bin/activate" ]; then
    BROKEN=".venv.casse-$(date +%Y%m%d-%H%M%S)"
    mv .venv "$BROKEN"
    warn "Environnement Python incomplet mis de côté : $BROKEN"
fi
if [ -d ".venv" ]; then
    info ".venv existe déjà, création ignorée."
else
    # Journal d'erreur à nom imprévisible (mktemp), jamais un nom fixe sous /tmp qu'un autre compte pourrait
    # préparer (scan de sécurité 2026-11-25, F6)
    VENV_ERR="$(mktemp)"
    if ! python3 -m venv .venv 2>"$VENV_ERR"; then
        err "Échec de la création de l'environnement virtuel."
        warn "Sur Debian/Ubuntu (et dérivées), le module venv n'est pas toujours inclus avec python3 de base."
        tip "Installez-le puis relancez ce script : sudo apt install python3-venv"
        cat "$VENV_ERR" >&2
        rm -f "$VENV_ERR"
        exit 1
    fi
    rm -f "$VENV_ERR"
    ok "Environnement virtuel créé (.venv)."
fi

# -------------------------------------------------------------------------
# 2. Dépendances — pyproject.toml reste l'unique source de verite (pas de
#    requirements.txt separe a maintenir en double). omega-lib n'est pas
#    publie sur PyPI : embarque dans vendor/omega-lib/ (bibliotheque
#    partagee de la suite omega-, sans quoi `pip install -e .` echoue sur
#    une machine qui n'a pas ~/DEV/LIB/omega-lib).
# -------------------------------------------------------------------------
source .venv/bin/activate
pip install -q --upgrade pip
if [ -d "$SCRIPT_DIR/vendor/omega-lib" ]; then
    pip install -q -e "$SCRIPT_DIR/vendor/omega-lib"
fi
pip install -q -e .
ok "Dépendances installées."

# -------------------------------------------------------------------------
# 3. Scripts exécutables
# -------------------------------------------------------------------------
chmod +x omega-tail.sh
chmod +x "$SCRIPT_DIR/install.sh"
ok "Scripts rendus exécutables."

# -------------------------------------------------------------------------
# 4. Jeton d'installation (var/omega-jeton.json, compatibilite omega-connect
#    2026-11-25) : lu par omega-connect, sans rien exécuter. Écrit sous VOTRE
#    compte (jamais en root). Un échec ne bloque jamais l'installation.
# -------------------------------------------------------------------------
if "$SCRIPT_DIR/omega-tail.sh" synchro jeton >/dev/null 2>&1; then
    ok "Jeton d'installation à jour (var/omega-jeton.json)."
else
    warn "Jeton d'installation non écrit : omega-connect ne verra pas cette installation tant qu'il manque."
    tip "Créez-le avec : ${SCRIPT_DIR}/omega-tail.sh synchro jeton"
fi

# -------------------------------------------------------------------------
# 5. Alias (optionnel) — bash et zsh, quel que soit celui réellement utilisé.
#    Pas de sudo ici : l installation ne requiert aucun privilège root.
# -------------------------------------------------------------------------
ALIAS_LINE="alias omega-tail=\"${SCRIPT_DIR}/omega-tail.sh\""

for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    rc_name="$(basename "$rc")"
    if grep -qxF "$ALIAS_LINE" "$rc" 2>/dev/null; then
        info "Alias déjà présent dans $rc_name."
    elif echo "$ALIAS_LINE" >> "$rc" 2>/dev/null; then
        ok "Alias ajouté à $rc_name."
    else
        warn "Impossible d'ajouter l'alias à $rc_name."
    fi
done

echo ""
ok "Installation terminée."
tip "Lancez Omega-Tail avec : ${SCRIPT_DIR}/omega-tail.sh (ou 'omega-tail' dans un nouveau terminal si l'alias vient d'être ajouté)."
