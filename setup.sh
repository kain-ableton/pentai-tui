#!/usr/bin/env bash
set -euo pipefail

# Root of this repo
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python / venv settings
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-"$REPO_ROOT/.venv"}"

echo "[*] Using repo root: $REPO_ROOT"
echo "[*] Using Python:   $PYTHON_BIN"
echo "[*] Venv dir:       $VENV_DIR"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "[!] python3 not found (override with PYTHON_BIN=/path/to/python3)" >&2
  exit 1
fi

# Create venv if missing
if [[ ! -d "$VENV_DIR" ]]; then
  echo "[*] Creating virtualenv..."
  "$PYTHON_BIN" -m venv "$VENV_DIR"
else
  echo "[*] Virtualenv already exists."
fi

# Activate venv
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "[*] Upgrading pip and installing requirements..."
pip install --upgrade pip
pip install -r "$REPO_ROOT/requirements.txt"

# Ensure pentai.py is executable
chmod +x "$REPO_ROOT/pentai.py"

# Wire zsh helpers
ZSHRC="$HOME/.zshrc"
SNIPPET_LINE="source \"$REPO_ROOT/zsh_snippets.sh\""

echo "[*] Ensuring zsh helpers are loaded from: $ZSHRC"
touch "$ZSHRC"

if ! grep -Fq "$SNIPPET_LINE" "$ZSHRC"; then
  {
    echo ""
    echo "# PentAI TUI helpers"
    echo "$SNIPPET_LINE"
  } >> "$ZSHRC"
  echo "[*] Added PentAI helpers to $ZSHRC"
else
  echo "[*] PentAI helpers already referenced in $ZSHRC"
fi

cat <<EOF

[*] Setup complete.

Environment:
  Venv:   $VENV_DIR
  Script: $REPO_ROOT/pentai.py

Next steps:

1) Export your API key (e.g. in ~/.zshrc or ~/.zprofile):
   export AI_API_KEY="your_real_key_here"

2) Start a new zsh session (or: source ~/.zshrc) to load helpers:
   exec zsh
   # or
   source ~/.zshrc

3) From anywhere, you can now run:
   ai-cmd      # explain last command
   ai-recon    # recon planner
   ai-loot F   # loot finder on file F
   ai-report   # report notes
   ai-red      # red team attack-chain planner

Or run directly:
   "$VENV_DIR/bin/python" "$REPO_ROOT/pentai.py" --mode cmd
EOF
