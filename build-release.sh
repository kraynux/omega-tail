#!/usr/bin/env bash
# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
# ==============================================================================
# Construit l'archive distribuable omega-tail-<version>.tar.gz dans ../html/download/ (dossier publie du site,
# /omega-tail/download/) et ajoute son empreinte a sha.txt (meme mise en page qu'omega-serv). Copie le projet sans
# artefacts de developpement ni etat local (var/ ENTIER exclu : porte, veille, survie, Funnel, bouclier, reglages, exports, declaration, jeton ;
# documents de travail et banc d'essai exclus aussi),
# embarque omega-lib (non publiee sur PyPI) depuis sa source, compile les langues (msgfmt --check ; .po et .pot non
# livres). Outil de maintenance, jamais inclus dans l'archive.
# ==============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${CYAN}ℹ️  $1${NC}"; }
ok()   { echo -e "${GREEN}✅ $1${NC}"; }
err()  { echo -e "${RED}❌ $1${NC}"; }

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OMEGA_LIB_SRC="${OMEGA_LIB_SRC:-$HOME/DEV/LIB/omega-lib}"
DIST_DIR="${DIST_DIR:-$PROJECT_ROOT/../html/download}"
VERSION="$(sed -n 's/^version = "\(.*\)"$/\1/p' "$PROJECT_ROOT/pyproject.toml" | head -n1)"
if [ -z "$VERSION" ]; then
    err "Version introuvable dans pyproject.toml."
    exit 1
fi
ARCHIVE_NAME="omega-tail-$VERSION.tar.gz"
SHA_FILE="$DIST_DIR/sha.txt"

if [ ! -d "$OMEGA_LIB_SRC" ]; then
    err "omega-lib introuvable : $OMEGA_LIB_SRC (definissez OMEGA_LIB_SRC si le chemin differe)."
    exit 1
fi

STAGING_DIR="$(mktemp -d)"
trap 'rm -rf "$STAGING_DIR"' EXIT
DEST="$STAGING_DIR/omega-tail"
mkdir -p "$DEST"

info "Copie du projet omega-tail $VERSION..."
rsync -a \
    --exclude='.venv/' --exclude='venv/' --exclude='.venv.casse-*/' \
    --exclude='__pycache__/' --exclude='*.pyc' \
    --exclude='.pytest_cache/' --exclude='.mypy_cache/' --exclude='.ruff_cache/' \
    --exclude='.import_linter_cache/' --exclude='*.egg-info/' \
    --exclude='.git/' --exclude='.claude/' \
    --exclude='docs/assets/' \
    --exclude='var/' \
    --exclude='vendor/' \
    --exclude='*~' --exclude='*.bak' --exclude='*.swp' \
    --exclude='.coverage' --exclude='htmlcov/' \
    --exclude='build-release.sh' --exclude='*.tar.gz' --exclude='dist/' \
    --exclude='sauvegardes/' --exclude='banc-lot0/' --exclude='banc-debit/' --exclude='/CLAUDE-SECURITY-*/' \
    --exclude='/ETUDE_OMEGA-TAIL.md' --exclude='/PLAN_*.md' --exclude='/OMEGA-TAIL_A_FAIRE.md' \
    --exclude='/MESURES_LOT0.md' --exclude='/MESURES_DEBIT_MEMOIRE.md' --exclude='/PROPOSITION_MENU_FONCTIONS.md' --exclude='/reflexion.txt' \
    --exclude='/a faire.txt' --exclude='/ascii.txt' \
    "$PROJECT_ROOT/" "$DEST/"

info "omega-lib embarquee (dependance obligatoire, non publiee sur PyPI)..."
mkdir -p "$DEST/vendor/omega-lib"
rsync -a \
    --exclude='.venv/' --exclude='__pycache__/' --exclude='*.pyc' \
    --exclude='.pytest_cache/' --exclude='.mypy_cache/' --exclude='.ruff_cache/' \
    --exclude='*.egg-info/' --exclude='.git/' --exclude='tests/' --exclude='*~' --exclude='sauvegardes/' \
    "$OMEGA_LIB_SRC/" "$DEST/vendor/omega-lib/"

if find "$DEST" -name '*.po' -path '*/LC_MESSAGES/*' | grep -q .; then
    if ! command -v msgfmt > /dev/null; then
        err "msgfmt introuvable (paquet gettext) : impossible de compiler les langues."
        exit 1
    fi
    info "Compilation des langues..."
    while IFS= read -r po; do
        msgfmt --check -o "${po%.po}.mo" "$po" || { err "Catalogue invalide : $po"; exit 1; }
        rm -f "$po"
    done < <(find "$DEST" -name '*.po' -path '*/LC_MESSAGES/*')
    find "$DEST" -name '*.pot' -path '*/locale/*' -delete
fi

info "Archivage..."
mkdir -p "$DIST_DIR"
tar -C "$STAGING_DIR" -czf "$DIST_DIR/$ARCHIVE_NAME" omega-tail

SHA_LINE="$(cd "$DIST_DIR" && sha256sum "$ARCHIVE_NAME")"
SHA_LINE="$SHA_LINE" ARCHIVE_NAME="$ARCHIVE_NAME" VERSION="$VERSION" python3 - "$SHA_FILE" <<'PY'
import os, sys
path = sys.argv[1]
line, name, version = os.environ["SHA_LINE"], os.environ["ARCHIVE_NAME"], os.environ["VERSION"]
sep = "=" * 89
lines = open(path, encoding="utf-8").read().splitlines() if os.path.exists(path) else []
if not any(l.strip() for l in lines):
    lines = ["", sep, "Controle d integrite des archives OMEGA-TAIL", "", sep, ""]
if any(l.endswith("  " + name) for l in lines):
    lines = [line if l.endswith("  " + name) else l for l in lines]
elif f"version {version} :" in lines:
    i = lines.index(f"version {version} :")
    lines[i + 1:i + 1] = ["", line]
else:
    first = next((i for i, l in enumerate(lines) if l.startswith("version ")), len(lines))
    lines[first:first] = [f"version {version} :", "", line, "", sep, ""]
open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
PY

ok "Archive generee : $DIST_DIR/$ARCHIVE_NAME"
echo "sha256sum (ajoute a $SHA_FILE) :"
echo "$SHA_LINE"
