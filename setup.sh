#!/usr/bin/env bash
set -euo pipefail

# Root of this repo
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python / venv settings
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-"$REPO_ROOT/.venv"}"

echo "======================================"
echo "  PentAI TUI v2.0 Setup"
echo "======================================"
echo ""
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

# Create config directories
CONFIG_DIR="$HOME/.config/pentai"
DATA_DIR="$HOME/.local/share/pentai"

mkdir -p "$CONFIG_DIR/targets"
mkdir -p "$DATA_DIR"
echo "[*] Created config directories"

# Create default target config
DEFAULT_CONFIG="$CONFIG_DIR/targets/default.json"
if [ ! -f "$DEFAULT_CONFIG" ]; then
    cat > "$DEFAULT_CONFIG" << EOF
{
  "name": "default",
  "scope": "Define your target scope here (IP ranges, domains, etc.)",
  "notes": "Default target configuration. Use --init-target to create specific targets.",
  "loot_paths": [],
  "tags": ["default"],
  "hosts": [],
  "credentials": {},
  "findings": []
}
EOF
    echo "[*] Created default target config"
fi

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

======================================"
  ✅ Setup Complete!
======================================"

Environment:
  Venv:   $VENV_DIR
  Script: $REPO_ROOT/pentai.py
  Config: $CONFIG_DIR
  Data:   $DATA_DIR

Next steps:

1) Export your API key (e.g. in ~/.zshrc or ~/.zprofile):
   export AI_API_KEY="your_real_key_here"

2) Start a new zsh session (or: source ~/.zshrc) to load helpers:
   exec zsh
   # or
   source ~/.zshrc

3) From anywhere, you can now run:
   ai-cmd      # explain last command
   ai-chat     # general chat
   ai-recon    # recon planner
   ai-loot F   # loot finder on file F
   ai-report   # report notes
   ai-red      # red team attack-chain planner
   ai-exploit  # exploit development
   ai-osint    # OSINT guidance
   ai-privesc  # privilege escalation

Or run directly:
   "$VENV_DIR/bin/python" "$REPO_ROOT/pentai.py" --mode cmd

Documentation:
  - README.md   : Overview and quick start
  - USAGE.md    : Complete usage guide
  - FEATURES.md : Feature documentation
  - EXAMPLES.md : Real-world scenarios

Create a target:
  pentai.py --init-target my-project

View help:
  pentai.py --help
  Press F1 inside the TUI for shortcuts
EOF
