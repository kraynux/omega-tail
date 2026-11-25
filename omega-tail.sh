#!/usr/bin/env bash
# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
# ==============================================================================
# Lanceur - OMEGA-TAIL
# Aucune élévation au lancement : les lectures se font sous votre compte ;
# sudo est demandé action par action, dans le terminal,
# avec la commande affichée avant.
# Pas de bannière : la sortie (texte ou --format json) doit rester exploitable.
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
    echo "❌ Environnement virtuel introuvable : $SCRIPT_DIR/.venv" >&2
    echo "Lancez d'abord : $SCRIPT_DIR/install.sh" >&2
    exit 1
fi

exec "$VENV_PYTHON" -m omega_tail "$@"
