# PentAI zsh helpers

pentai() {
  python3 "$HOME/bin/pentai.py" "$@"
}

ai-cmd() {
  local last
  last=$(fc -ln -1)

  python3 "$HOME/bin/pentai.py" \
    --mode cmd \
    --prefill "Explain this command in detail, including risks and safer variants. Then suggest improvements:\n\n$last"
}

ai-err() {
  local log="/tmp/err.log"
  if [[ ! -s "$log" ]]; then
    echo "No error log at $log (or file is empty)."
    return 1
  fi

  PENTAI_FILE_CONTEXT="$log" python3 "$HOME/bin/pentai.py" \
    --mode cmd \
    --prefill "Explain these errors and suggest concrete fixes. Focus on root cause and relevant commands."
}

ai-recon() {
  python3 "$HOME/bin/pentai.py" \
    --mode recon \
    --prefill "Using the available logs and current recon output, summarise what has been done so far and propose phased recon/enumeration next steps with specific commands."
}

ai-loot() {
  if [[ -z "$1" ]]; then
    echo "Usage: ai-loot <file>"
    return 1
  fi
  local f="$1"
  if [[ ! -f "$f" ]]; then
    echo "No such file: $f"
    return 1
  fi

  PENTAI_FILE_CONTEXT="$f" python3 "$HOME/bin/pentai.py" \
    --mode loot \
    --prefill "Scan this context for potentially sensitive artefacts (credentials, tokens, secrets, interesting endpoints). Summarise and prioritise findings."
}

ai-report() {
  python3 "$HOME/bin/pentai.py" \
    --mode report \
    --prefill "From this context, draft concise pentest notes: scope, key findings, interesting services, and recommended next steps, grouped logically."
}

ai-red() {
  python3 "$HOME/bin/pentai.py" \
    --mode red \
    --prefill "Using the current authorised scope and the available logs/recon, propose a realistic red team attack chain: initial access, privilege escalation, lateral movement, and impact. For each step, include objective, example commands/tools, evidence to collect, and how defenders might detect it."
}

pentai-init-target() {
  if [[ -z "$1" ]]; then
    echo "Usage: pentai-init-target <name>"
    return 1
  fi
  python3 "$HOME/bin/pentai.py" --init-target "$1"
}

pentai-log-view() {
  local target="${1:-}"
  if [[ -n "$target" ]]; then
    python3 "$HOME/bin/pentai.py" --target "$target" --view-logs --last 20
  else
    python3 "$HOME/bin/pentai.py" --view-logs --last 20
  fi
}
