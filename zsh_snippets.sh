# PentAI TUI v2.0 - Zsh/Bash Helper Functions
# Source this file in your ~/.zshrc or ~/.bashrc:
#   source /path/to/pentai-tui/zsh_snippets.sh

# Determine script location
PENTAI_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PENTAI_VENV="$PENTAI_SCRIPT_DIR/.venv/bin/python"

# Use venv python if available, otherwise system python3
if [[ -x "$PENTAI_VENV" ]]; then
  PENTAI_PYTHON="$PENTAI_VENV"
else
  PENTAI_PYTHON="python3"
fi

PENTAI_SCRIPT="$PENTAI_SCRIPT_DIR/pentai.py"

# Main pentai command
pentai() {
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" "$@"
}

# --- Mode-specific helpers ---

# CMD mode - Explain last command
ai-cmd() {
  local last
  last=$(fc -ln -1)
  
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode cmd \
    --prefill "Explain this command in detail, including risks and safer variants. Then suggest improvements:\n\n$last"
}

# CHAT mode - General pentesting questions
ai-chat() {
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode chat \
    --prefill "${1:-}"
}

# ERROR helper - Analyze errors from log file
ai-err() {
  local log="${1:-/tmp/err.log}"
  if [[ ! -s "$log" ]]; then
    echo "No error log at $log (or file is empty)."
    echo "Usage: ai-err [logfile]  (default: /tmp/err.log)"
    return 1
  fi

  PENTAI_FILE_CONTEXT="$log" "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode cmd \
    --prefill "Explain these errors and suggest concrete fixes. Focus on root cause and relevant commands."
}

# RECON mode - Reconnaissance planning
ai-recon() {
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode recon \
    --prefill "Using the available logs and current recon output, summarise what has been done so far and propose phased recon/enumeration next steps with specific commands."
}

# LOOT mode - Find credentials and secrets
ai-loot() {
  if [[ -z "$1" ]]; then
    echo "Usage: ai-loot <file>"
    echo "Analyzes file for credentials, tokens, API keys, and secrets"
    return 1
  fi
  local f="$1"
  if [[ ! -f "$f" ]]; then
    echo "No such file: $f"
    return 1
  fi

  PENTAI_FILE_CONTEXT="$f" "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode loot \
    --prefill "Scan this context for potentially sensitive artefacts (credentials, tokens, secrets, interesting endpoints). Summarise and prioritise findings."
}

# REPORT mode - Generate report notes
ai-report() {
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode report \
    --prefill "From this context, draft concise pentest notes: scope, key findings, interesting services, and recommended next steps, grouped logically."
}

# RED mode - Red team attack planning
ai-red() {
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode red \
    --prefill "Using the current authorised scope and the available logs/recon, propose a realistic red team attack chain: initial access, privilege escalation, lateral movement, and impact. For each step, include objective, example commands/tools, evidence to collect, and how defenders might detect it."
}

# EXPLOIT mode - Exploit development assistance
ai-exploit() {
  local vuln="${1:-}"
  if [[ -n "$vuln" ]]; then
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
      --mode exploit \
      --prefill "Help with exploiting: $vuln"
  else
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" --mode exploit
  fi
}

# OSINT mode - Intelligence gathering
ai-osint() {
  local target="${1:-}"
  if [[ -n "$target" ]]; then
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
      --mode osint \
      --prefill "Provide OSINT methodology for target: $target"
  else
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" --mode osint
  fi
}

# PRIVESC mode - Privilege escalation
ai-privesc() {
  local file="${1:-}"
  if [[ -n "$file" && -f "$file" ]]; then
    PENTAI_FILE_CONTEXT="$file" "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
      --mode privesc \
      --prefill "Analyze this enumeration output for privilege escalation vectors"
  else
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" --mode privesc
  fi
}

# --- Target management helpers ---

# Initialize new target configuration
pentai-init-target() {
  if [[ -z "$1" ]]; then
    echo "Usage: pentai-init-target <name>"
    echo "Creates a new target configuration"
    return 1
  fi
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" --init-target "$1"
}

# Set current directory target
pentai-set-target() {
  if [[ -z "$1" ]]; then
    echo "Usage: pentai-set-target <name>"
    echo "Creates .pentai-target file in current directory"
    return 1
  fi
  echo "$1" > .pentai-target
  echo "Set current directory target to: $1"
}

# View target session logs
pentai-log-view() {
  local target="${1:-}"
  local count="${2:-20}"
  if [[ -n "$target" ]]; then
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" --target "$target" --view-logs --last "$count"
  else
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" --view-logs --last "$count"
  fi
}

# Export session to file
pentai-export() {
  local target="${1:-}"
  local output="${2:-session-export-$(date +%Y%m%d-%H%M%S).txt}"
  
  if [[ -n "$target" ]]; then
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" --target "$target" --view-logs --last 9999 > "$output"
  else
    "$PENTAI_PYTHON" "$PENTAI_SCRIPT" --view-logs --last 9999 > "$output"
  fi
  
  echo "Session exported to: $output"
}

# --- Quick analysis helpers ---

# Analyze nmap output
ai-nmap() {
  local file="${1:-}"
  if [[ -z "$file" ]]; then
    # Try to find most recent nmap file
    file=$(find . -name "*.nmap" -o -name "*.xml" -o -name "*.gnmap" | xargs ls -t 2>/dev/null | head -1)
    if [[ -z "$file" ]]; then
      echo "Usage: ai-nmap <nmap-file>"
      echo "No nmap files found in current directory"
      return 1
    fi
    echo "Using most recent nmap file: $file"
  fi
  
  PENTAI_FILE_CONTEXT="$file" "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode recon \
    --prefill "Analyze this nmap scan and suggest detailed enumeration steps for each discovered service"
}

# Quick command explanation
ai-explain() {
  if [[ -z "$1" ]]; then
    echo "Usage: ai-explain <command>"
    echo "Explains what a command does"
    return 1
  fi
  
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode cmd \
    --prefill "Explain in detail what this command does: $*"
}

# Quick pentest question
ai-ask() {
  if [[ -z "$1" ]]; then
    echo "Usage: ai-ask <question>"
    return 1
  fi
  
  "$PENTAI_PYTHON" "$PENTAI_SCRIPT" \
    --mode chat \
    --prefill "$*"
}

# --- Convenience aliases ---
alias pai='pentai'
alias pai-cmd='ai-cmd'
alias pai-chat='ai-chat'
alias pai-recon='ai-recon'
alias pai-loot='ai-loot'
alias pai-report='ai-report'
alias pai-red='ai-red'
alias pai-exploit='ai-exploit'
alias pai-osint='ai-osint'
alias pai-privesc='ai-privesc'

# Show available helpers
pentai-help() {
  cat << 'EOF'
PentAI TUI v2.0 - Shell Helper Functions

Mode-Specific Commands:
  ai-cmd              Explain last command run
  ai-chat [text]      General pentesting chat
  ai-recon            Reconnaissance planning
  ai-loot <file>      Find credentials/secrets in file
  ai-report           Generate report notes
  ai-red              Red team attack planning
  ai-exploit [vuln]   Exploit development help
  ai-osint [target]   OSINT methodology
  ai-privesc [file]   Privilege escalation analysis

Quick Analysis:
  ai-nmap [file]      Analyze nmap output (auto-finds if no file)
  ai-explain <cmd>    Explain what a command does
  ai-ask <question>   Quick pentesting question
  ai-err [logfile]    Analyze error log (default: /tmp/err.log)

Target Management:
  pentai-init-target <name>      Create new target config
  pentai-set-target <name>       Set current directory target
  pentai-log-view [target] [n]   View session logs (default: 20 entries)
  pentai-export [target] [file]  Export session to file

Main Command:
  pentai [options]    Run PentAI TUI with options
  pentai --help       Show all CLI options

Shortcuts:
  pai                 Short alias for pentai
  pai-<mode>          Short aliases for all ai-<mode> commands

Environment Variables:
  AI_API_KEY          Required: Your API key
  AI_BASE_URL         Optional: Custom API endpoint
  AI_MODEL            Optional: Custom model (default: gpt-4o-mini)
  PENTAI_TARGET_NAME  Optional: Default target name
  PENTAI_FILE_CONTEXT Optional: Default context file

Examples:
  # Analyze last command
  nmap -sV target.com
  ai-cmd

  # Find secrets in logs
  ai-loot burp-output.xml

  # Analyze nmap results
  ai-nmap scan.xml

  # Quick question
  ai-ask "How to bypass WAF with SQLi?"

  # Privilege escalation help
  ai-privesc linpeas.txt

For more information, see:
  - README.md for overview
  - USAGE.md for detailed guide
  - EXAMPLES.md for real scenarios
EOF
}

# Show quick help on first load
echo "PentAI TUI v2.0 helpers loaded. Type 'pentai-help' for usage."
