# PentAI TUI - Quick Reference Card

## Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `F1` | Show help and mode documentation |
| `F2` | Cycle through modes |
| `F3` | Display target information |
| `F4` | Load quick command templates |
| `Ctrl+H` | Toggle shell history context |
| `Ctrl+L` | Clear chat log |
| `Ctrl+S` | Save session to file |
| `Ctrl+C` | Exit application |

## Nine Modes
| Mode | Purpose | Shell Helper |
|------|---------|--------------|
| **CMD** | Command & error analysis | `ai-cmd` |
| **CHAT** | General Q&A | `ai-chat` |
| **RECON** | Reconnaissance planning | `ai-recon` |
| **LOOT** | Credential/secret finding | `ai-loot <file>` |
| **REPORT** | Report generation | `ai-report` |
| **RED** | Red team attack planning | `ai-red` |
| **EXPLOIT** | Exploit development | `ai-exploit [vuln]` |
| **OSINT** | Intelligence gathering | `ai-osint [target]` |
| **PRIVESC** | Privilege escalation | `ai-privesc [file]` |

## Quick Commands
```bash
# Start TUI
pentai                              # Default mode
pentai --mode recon                 # Specific mode
pentai --target webapp --mode loot  # With target

# Analyze last command
nmap -sV target.com
ai-cmd

# Find secrets
ai-loot burp-output.xml

# Analyze enumeration
ai-nmap scan.xml
ai-privesc linpeas.txt

# Quick question
ai-ask "How to bypass WAF?"

# Target management
pentai-init-target webapp-test
pentai-set-target webapp-test
pentai-log-view webapp-test 50
pentai-export webapp-test
```

## Configuration
```bash
# Required
export AI_API_KEY="sk-your-key"

# Optional
export AI_BASE_URL="https://api.openai.com/v1"
export AI_MODEL="gpt-4o-mini"
export PENTAI_TARGET_NAME="default"
```

## File Locations
```
~/.config/pentai/targets/    # Target configs
~/.local/share/pentai/       # Session logs
.pentai-target               # Per-directory target
```

## Common Workflows

### Initial Recon
```bash
nmap -sC -sV -oA scan target.com
ai-nmap scan.nmap
ai-recon  # Get next steps
```

### Loot Hunting
```bash
ai-loot access.log
ai-loot burp-proxy.xml
ai-loot jok3r-output.txt
```

### Privilege Escalation
```bash
./linpeas.sh > linpeas.txt
ai-privesc linpeas.txt
```

### Report Writing
```bash
ai-report
pentai-log-view > session.txt
```

## Help Resources
- `pentai --help` - CLI options
- `pentai-help` - Shell functions
- `F1` in TUI - Keyboard shortcuts
- `README.md` - Overview
- `USAGE.md` - Detailed guide
- `EXAMPLES.md` - Real scenarios

## Quick Tips
1. Press `F2` to cycle modes without restarting
2. Use `F4` for mode-specific command templates
3. Toggle history with `Ctrl+H` if too noisy
4. Create `.pentai-target` in project directories
5. Use `ai-cmd` after any command for explanation
6. `ai-nmap` auto-finds most recent scan
7. Export sessions regularly with `Ctrl+S`
8. Check logs with `pentai-log-view` for review

## Getting Help
```bash
pentai --help              # CLI help
pentai-help                # Shell functions
ai-ask "your question"     # Quick AI answer
```

Inside TUI:
- Press `F1` for interactive help
- Press `F3` for target details
- Type questions naturally

## Emergency Aliases
```bash
alias pai='pentai'
alias paic='ai-cmd'
alias pair='ai-recon'
alias pail='ai-loot'
alias paix='ai-exploit'
```

---
**PentAI TUI v2.0** | Made for security professionals
For full documentation: README.md, USAGE.md, EXAMPLES.md
