# Frequently Asked Questions (FAQ)

## Table of Contents

1. [General Questions](#general-questions)
2. [Installation & Setup](#installation--setup)
3. [Configuration](#configuration)
4. [Usage & Features](#usage--features)
5. [Troubleshooting](#troubleshooting)
6. [Security & Privacy](#security--privacy)
7. [Integration & Compatibility](#integration--compatibility)
8. [Advanced Topics](#advanced-topics)

---

## General Questions

### What is PentAI-TUI?

PentAI-TUI is a terminal-based AI assistant specifically designed for penetration testing workflows. It integrates Large Language Model (LLM) capabilities directly into your terminal, providing intelligent assistance across various phases of security assessments including reconnaissance, exploitation, and reporting.

### Who should use PentAI-TUI?

- Penetration testers conducting authorized assessments
- Security researchers analyzing systems and applications
- Red team operators planning attack chains
- Security consultants performing security audits
- Students learning penetration testing techniques

### Is PentAI-TUI free to use?

Yes, PentAI-TUI is open source. However, you'll need access to an LLM API (like OpenAI), which may have associated costs. Alternatively, you can use free/local models like Ollama.

### What makes PentAI-TUI different from ChatGPT?

PentAI-TUI is specifically designed for penetration testing with:
- **Context awareness**: Automatically includes shell history, scan results, and target configs
- **Specialized modes**: Six modes optimized for different pentest phases
- **Session logging**: Complete audit trail for compliance
- **Terminal integration**: Works directly in your pentesting workflow
- **Security focus**: Built-in guardrails for authorized testing only

### Can I use PentAI-TUI for illegal activities?

**No. Absolutely not.** PentAI-TUI is designed exclusively for authorized penetration testing and security assessments. The tool includes ethical guardrails, and using it for unauthorized access is illegal and violates the project's intended use.

---

## Installation & Setup

### What are the system requirements?

- **Python**: 3.8 or higher (3.10+ recommended)
- **Operating System**: Linux, macOS, or Windows (WSL recommended for Windows)
- **Shell**: Zsh or Bash (Zsh recommended for full feature support)
- **Memory**: Minimal (~50MB)
- **Internet**: Required for cloud LLM APIs (optional for local models)

### How do I install PentAI-TUI?

```bash
# Clone the repository
git clone https://github.com/kain-ableton/pentai-tui.git
cd pentai-tui

# Run setup script
./setup.sh

# Set API key
export AI_API_KEY="your-api-key-here"

# Test installation
./pentai.py --mode cmd
```

### The setup script failed. What should I do?

Common causes and solutions:

1. **Python not found**:
   ```bash
   # Install Python 3
   sudo apt install python3 python3-pip  # Debian/Ubuntu
   brew install python3                  # macOS
   ```

2. **Permission denied**:
   ```bash
   chmod +x setup.sh pentai.py
   ```

3. **Virtual environment issues**:
   ```bash
   # Manual venv creation
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### How do I update PentAI-TUI?

```bash
cd pentai-tui
git pull origin main
pip install --upgrade -r requirements.txt
```

---

## Configuration

### How do I configure API keys?

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
export AI_API_KEY="sk-your-api-key-here"
```

For multiple environments:

```bash
# Development
export DEV_API_KEY="sk-dev-key"

# Production
export PROD_API_KEY="sk-prod-key"

# Switch based on context
export AI_API_KEY="$DEV_API_KEY"
```

### Can I use a local LLM instead of OpenAI?

Yes! PentAI-TUI supports any OpenAI-compatible API:

```bash
# Ollama (local)
export AI_BASE_URL="http://localhost:11434/v1"
export AI_MODEL="llama2"
export AI_API_KEY="ollama"  # Dummy key

# LM Studio
export AI_BASE_URL="http://localhost:1234/v1"
export AI_MODEL="local-model"
export AI_API_KEY="lm-studio"

# Azure OpenAI
export AI_BASE_URL="https://your-resource.openai.azure.com"
export AI_MODEL="gpt-4"
export AI_API_KEY="your-azure-key"
```

### How do I configure per-target settings?

```bash
# Create target config
pentai-init-target my-client

# Edit configuration
vim ~/.config/pentai/targets/my-client.json

# Example configuration
{
  "name": "my-client",
  "scope": "10.0.1.0/24, *.client.com, authorized by SOW-2025-001",
  "notes": "Web application pentest, focus on auth bypass",
  "loot_paths": [
    "./logs",
    "./scans",
    "./captures"
  ]
}

# Use the target
cd ~/pentests/my-client
echo "my-client" > .pentai-target
ai-recon
```

### Where are configuration files stored?

- **Target configs**: `~/.config/pentai/targets/*.json`
- **Session logs**: `~/.local/share/pentai/*.jsonl`
- **Environment vars**: `~/.zshrc` or `~/.bashrc`

You can override locations:
```bash
export PENTAI_CONFIG_DIR="~/my-pentai-configs"
export PENTAI_DATA_DIR="~/my-pentai-data"
```

---

## Usage & Features

### How do I switch between modes?

**In TUI**:
- Press **F2** to cycle through modes
- Current mode shown in header

**From command line**:
```bash
./pentai.py --mode cmd     # Command assistant
./pentai.py --mode chat    # General chat
./pentai.py --mode recon   # Reconnaissance planner
./pentai.py --mode loot    # Artifact finder
./pentai.py --mode report  # Report generator
./pentai.py --mode red     # Red team planner
```

**Using helpers**:
```bash
ai-cmd      # Command mode
ai-recon    # Recon mode
ai-loot file.txt  # Loot mode with file
ai-report   # Report mode
ai-red      # Red team mode
```

### What does each mode do?

| Mode | Purpose | Use When |
|------|---------|----------|
| **cmd** | Explain commands, diagnose errors | You have an error or unfamiliar command |
| **chat** | General pentest Q&A | You need methodology guidance |
| **recon** | Plan reconnaissance steps | You completed a scan and need next steps |
| **loot** | Find credentials/secrets | You have log files to analyze |
| **report** | Generate findings summary | You need to document your work |
| **red** | Plan attack chains | You need multi-step attack strategy |

### How does context detection work?

PentAI automatically gathers context from:

1. **Shell history** (last 10 commands)
   - Toggle with Ctrl+H in TUI
   - Helps AI understand your workflow

2. **File auto-detection**
   - Searches: `./nmap/`, `./logs/`, `./output/`, current dir
   - Extensions: `.nmap`, `.gnmap`, `.xml`, `.log`, `.txt`
   - Picks most recently modified file

3. **Target configuration**
   - Loads from `~/.config/pentai/targets/<name>.json`
   - Includes scope, notes, loot paths

4. **Explicit file** (highest priority)
   ```bash
   ai-recon --file specific-scan.nmap
   PENTAI_FILE_CONTEXT=/path/to/file ai-recon
   ```

### Can I use PentAI without shell history?

Yes! Press **Ctrl+H** in the TUI to toggle history on/off. Or set environment variable:

```bash
export PENTAI_INCLUDE_HISTORY=false
./pentai.py --mode cmd
```

### How do I view past sessions?

```bash
# View logs for current target
pentai-log-view

# View logs for specific target
pentai-log-view target-name

# View more entries
pentai-log-view target-name --last 50

# Export to file
cat ~/.local/share/pentai/target-name.jsonl > session-export.jsonl
```

### Can I prefill the input box?

Yes, using the `--prefill` option:

```bash
./pentai.py --mode cmd --prefill "Explain: nmap -sS -sV target.com"
```

This is useful for automation:
```bash
last_cmd=$(fc -ln -1)
./pentai.py --mode cmd --prefill "Explain: $last_cmd"
```

---

## Troubleshooting

### "AI_API_KEY not set in environment"

**Solution**: Export your API key:
```bash
export AI_API_KEY="sk-your-key-here"
# Or add to ~/.zshrc for persistence
```

### "Connection refused" or timeout errors

**Causes & Solutions**:

1. **Wrong API endpoint**:
   ```bash
   # Check your configuration
   echo $AI_BASE_URL
   # Should be: https://api.openai.com/v1
   ```

2. **Network issues**:
   ```bash
   # Test connectivity
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $AI_API_KEY"
   ```

3. **Invalid API key**:
   ```bash
   # Verify key format (starts with sk- for OpenAI)
   echo $AI_API_KEY | head -c 10
   ```

4. **Firewall/proxy**:
   ```bash
   # Set proxy if needed
   export HTTPS_PROXY="http://proxy.company.com:8080"
   ```

### Shell history not being detected

**Causes & Solutions**:

1. **Using Bash instead of Zsh**:
   ```bash
   # PentAI looks for ~/.zsh_history
   # For Bash, it needs modification (future feature)
   ```

2. **History file in different location**:
   ```bash
   # Check where your history is
   echo $HISTFILE
   # Symlink if needed
   ln -s $HISTFILE ~/.zsh_history
   ```

3. **History disabled**:
   ```bash
   # Enable history in Zsh
   echo "HISTFILE=~/.zsh_history" >> ~/.zshrc
   echo "HISTSIZE=10000" >> ~/.zshrc
   echo "SAVEHIST=10000" >> ~/.zshrc
   ```

### File auto-detection not working

**Debugging steps**:

```bash
# Check current directory
pwd

# Look for files PentAI would detect
ls -la *.{nmap,gnmap,xml,log,txt} 2>/dev/null
ls -la nmap/ logs/ output/ 2>/dev/null

# Use explicit file instead
ai-recon --file /full/path/to/scan.nmap
```

### TUI is not displaying correctly

**Solutions**:

1. **Terminal compatibility**:
   ```bash
   # Ensure terminal supports colors
   export TERM=xterm-256color
   ```

2. **Resize terminal**:
   - Make terminal window larger
   - Some elements need minimum width

3. **Update Textual**:
   ```bash
   pip install --upgrade textual
   ```

### "Model not found" error

**Solution**: Specify correct model:
```bash
# List available models (OpenAI)
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $AI_API_KEY" | jq '.data[].id'

# Set correct model
export AI_MODEL="gpt-4"  # or gpt-3.5-turbo, etc.
```

### Responses are slow or timing out

**Solutions**:

1. **Increase timeout** (edit `pentai.py`):
   ```python
   # Line ~396
   resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=300)
   ```

2. **Use faster model**:
   ```bash
   export AI_MODEL="gpt-3.5-turbo"  # Faster than gpt-4
   ```

3. **Reduce context size**:
   - Toggle history off (Ctrl+H)
   - Use smaller file snippets
   - Simplify queries

---

## Security & Privacy

### Is my data sent to OpenAI (or other providers)?

Yes, if you use cloud APIs:
- **Sent**: Your queries, context (shell history, file snippets), target info
- **Not sent**: Your API key is used for auth only
- **Stored**: Per provider's data retention policy

For maximum privacy, use local models (Ollama).

### How do I prevent sensitive data from being logged?

**Best practices**:

1. **Don't paste actual credentials**:
   ```
   ❌ "I found password: P@ssw0rd123"
   ✅ "I found valid admin credentials, how to use them?"
   ```

2. **Sanitize before querying**:
   ```bash
   # Store separately
   echo "admin:secret" > loot/creds.txt
   chmod 600 loot/creds.txt
   
   # Query without revealing
   "I found admin credentials, suggest lateral movement"
   ```

3. **Encrypt session logs**:
   ```bash
   # After engagement
   gpg -c ~/.local/share/pentai/sensitive-target.jsonl
   rm ~/.local/share/pentai/sensitive-target.jsonl
   ```

4. **Use local models** for sensitive engagements

### Can PentAI execute commands on my system?

**No.** PentAI only suggests commands. You must manually copy and execute them. This is a security feature.

### How do I securely store API keys?

**Best practices**:

1. **Use environment variables** (not config files):
   ```bash
   export AI_API_KEY="sk-..."
   ```

2. **Use secret management tools**:
   ```bash
   # AWS Secrets Manager
   export AI_API_KEY=$(aws secretsmanager get-secret-value \
     --secret-id pentai-key --query SecretString --output text)
   
   # HashiCorp Vault
   export AI_API_KEY=$(vault kv get -field=key secret/pentai)
   
   # 1Password CLI
   export AI_API_KEY=$(op item get "OpenAI API Key" --fields api_key)
   ```

3. **Restrict file permissions**:
   ```bash
   chmod 600 ~/.zshrc  # Only you can read
   ```

4. **Rotate keys regularly**

### What if I accidentally commit an API key to git?

**Immediate actions**:

1. **Revoke the key** in your provider dashboard
2. **Remove from git history**:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch file-with-key" \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. **Generate new key**
4. **Update environment variable**

---

## Integration & Compatibility

### Can I integrate PentAI with Metasploit?

Yes! Example workflow:

```bash
# In Metasploit
meterpreter> sysinfo > /tmp/target-info.txt
meterpreter> background

# Get AI suggestions
PENTAI_FILE_CONTEXT=/tmp/target-info.txt ai-red

# Back to Metasploit with AI recommendations
meterpreter> sessions -i 1
```

### Does PentAI work with Burp Suite?

Yes, analyze HTTP history:

```bash
# Export HTTP history from Burp
# Save as http-history.xml

# Analyze for interesting endpoints
ai-loot http-history.xml

# Get suggestions
ai-chat
"Given these endpoints, suggest authentication bypass techniques"
```

### Can I use PentAI with nmap?

Yes, this is a primary use case:

```bash
# Run nmap
nmap -sV -sC target.com -oA scans/target

# PentAI auto-detects scan in ./scans/
cd project-dir
ai-recon

# Or specify explicitly
ai-recon --file scans/target.nmap
```

### Does PentAI support Windows?

**Windows Subsystem for Linux (WSL)**: ✅ Fully supported
**Native Windows**: ⚠️ Partial support
- Python script runs
- No zsh helper functions (use bash or PowerShell alternatives)
- Manual command execution required

### Can I use PentAI in Docker?

Yes! Example Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt pentai.py ./
RUN pip install -r requirements.txt

# Set API key via environment
ENV AI_API_KEY=""

ENTRYPOINT ["python3", "pentai.py"]
```

Usage:
```bash
docker build -t pentai-tui .
docker run -it -e AI_API_KEY="$AI_API_KEY" pentai-tui --mode cmd
```

---

## Advanced Topics

### Can I add custom modes?

Yes! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guide.

Quick example:
```python
# In pentai.py, add:
FORENSICS_INSTRUCTIONS = """
Mode: Digital Forensics.
Analyze artifacts, timelines, and evidence...
"""

MODES.append("forensics")
MODE_INSTRUCTIONS["forensics"] = FORENSICS_INSTRUCTIONS
MODE_DEFAULT_PROMPTS["forensics"] = "Analyze this artifact..."
```

### How do I create custom prompt templates?

Modify system prompts in `pentai.py`:

```python
BASE_SYSTEM_PROMPT = """
You are an AI assistant for penetration testing.
Custom instruction: Always provide 3 alternatives for each command.
...
"""
```

Or use prefills to guide behavior:
```bash
ai-cmd --prefill "Explain this command in simple terms for a beginner: <command>"
```

### Can I chain multiple AI calls?

Yes, through scripting:

```bash
#!/bin/bash
# smart-recon.sh

# Initial recon
nmap -sV target.com -oA scans/initial
AI_OUTPUT=$(ai-recon --prefill "Analyze nmap and suggest top 3 next steps")

# Parse AI output (extract commands)
COMMANDS=$(echo "$AI_OUTPUT" | grep -oP '(?<=```bash\n).*?(?=\n```)')

# Execute with confirmation
echo "$COMMANDS" | while read cmd; do
  read -p "Run: $cmd? (y/n) " -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    eval "$cmd"
  fi
done
```

### How do I optimize for cost?

1. **Use cheaper models**:
   ```bash
   export AI_MODEL="gpt-3.5-turbo"  # vs gpt-4
   ```

2. **Reduce context**:
   - Toggle history off when not needed
   - Use smaller file snippets
   - Keep queries concise

3. **Cache responses**:
   ```bash
   # Implement caching layer
   # Same query + same context hash = cached response
   ```

4. **Use local models**:
   ```bash
   # Ollama is completely free
   export AI_BASE_URL="http://localhost:11434/v1"
   ```

### How can I contribute to PentAI-TUI?

See [CONTRIBUTING.md](CONTRIBUTING.md) for comprehensive guide.

Quick start:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

---

## Still Have Questions?

- **Documentation**: Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **GitHub Issues**: Search existing issues or create new one
- **GitHub Discussions**: Ask the community
- **Code**: Read through `pentai.py` - it's well-commented

---

**Last Updated**: 2025-11-15  
**Version**: 1.0
