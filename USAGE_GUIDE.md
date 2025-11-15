# PentAI-TUI Usage Patterns & Best Practices

## Table of Contents
1. [Quick Start Workflows](#quick-start-workflows)
2. [Mode-Specific Usage Patterns](#mode-specific-usage-patterns)
3. [Best Practices](#best-practices)
4. [Advanced Techniques](#advanced-techniques)
5. [Common Pitfalls & Solutions](#common-pitfalls--solutions)
6. [Integration Patterns](#integration-patterns)
7. [Security & Compliance](#security--compliance)

---

## Quick Start Workflows

### Workflow 1: Single-Target Assessment

```bash
# Initial setup
cd ~/pentests/acme-webapp
echo "acme-webapp" > .pentai-target
pentai-init-target acme-webapp

# Edit target config with scope
vim ~/.config/pentai/targets/acme-webapp.json
# Add: "scope": "10.0.1.0/24, *.acme.com, authorized by ticket #12345"

# Run initial recon
nmap -sV -sC 10.0.1.0/24 -oA scans/initial
ai-recon

# Follow AI suggestions, then analyze errors
some-command 2>&1 | tee /tmp/err.log
ai-err

# Extract credentials from captured files
ai-loot scans/http-enum.txt

# Generate report
ai-report
```

### Workflow 2: Multi-Target Red Team Engagement

```bash
# Setup multiple targets
pentai-init-target dmz-servers
pentai-init-target internal-workstations
pentai-init-target domain-controllers

# Work on DMZ
cd ~/redteam/dmz
echo "dmz-servers" > .pentai-target
# ... perform recon ...
ai-recon

# Switch to internal
cd ~/redteam/internal
echo "internal-workstations" > .pentai-target
# ... perform lateral movement ...
ai-red

# View all logs
pentai-log-view dmz-servers
pentai-log-view internal-workstations
```

### Workflow 3: Quick Command Assistance

```bash
# Just ran a complex command and want explanation
nmap -sS -sV -p- --script vuln target.com
ai-cmd

# Or use command prefill
./pentai.py --mode cmd --prefill "Explain: nmap -sS -sV -p- --script vuln target.com"
```

---

## Mode-Specific Usage Patterns

### CMD Mode: Command & Error Assistant

**Use Cases:**
- Explain unfamiliar commands before running them
- Diagnose cryptic error messages
- Find safer alternatives to risky commands
- Learn about command flags and options

**Example Queries:**

```
"Explain this command: sqlmap -u http://target/page?id=1 --dbs --threads 10"

"I got error: 'Connection refused on port 443'. I'm testing HTTPS services. What could cause this?"

"What's the difference between 'nmap -sS' and 'nmap -sT'? Which is stealthier?"

"How can I make this curl command follow redirects and save cookies?"
```

**Best Practices:**
- Paste full error messages (not just "it doesn't work")
- Include relevant context from shell history
- Ask about risks before running destructive commands
- Request safer alternatives when AI flags concerns

### CHAT Mode: General Pentest Q&A

**Use Cases:**
- Methodology questions
- Tool recommendations
- Technique explanations
- Protocol deep-dives

**Example Queries:**

```
"What's the typical SMB enumeration workflow after finding port 445 open?"

"Explain how Kerberoasting works and when it's useful"

"I found an XXE vulnerability. What are the exploitation steps and how do I demo impact safely?"

"Recommend tools for subdomain enumeration. Which are most reliable?"
```

**Best Practices:**
- Start broad, then narrow down
- Ask for concrete examples and commands
- Request methodology phases (recon → exploit → post-exploit)
- Follow up with specific clarifications

### RECON Mode: Reconnaissance Planner

**Use Cases:**
- Analyze scan results and suggest next steps
- Create phased enumeration plans
- Identify missed services or attack vectors
- Optimize recon workflow

**Example Queries:**

```
"Based on the nmap results and commands I've run, what recon phase am I in and what should I do next?"

"I found HTTP on ports 80, 443, 8080, and 8443. Prioritize enumeration steps."

"Nmap shows 'filtered' on many ports. How should I proceed?"

"I've completed basic recon. What deeper service-specific enumeration should I do?"
```

**Best Practices:**
- Run mode after each major recon tool completes
- Include scan outputs as files (--file parameter)
- Let AI see your command history (keep Ctrl+H on)
- Follow phased approach: discovery → service enumeration → vulnerability scanning

### LOOT Mode: Artifact & Credential Finder

**Use Cases:**
- Extract credentials from tool outputs
- Find API keys in logs
- Identify interesting endpoints
- Prioritize findings

**Example Queries:**

```
"Scan this Hydra output for successful logins and summarize credentials"

"Find any potentially sensitive data in this HTTP response log"

"Extract all usernames, passwords, and hashes from this file"

"Which of these findings are most valuable for lateral movement?"
```

**Best Practices:**
- Use with specific log files: `ai-loot captured-traffic.txt`
- Review loot paths in target config regularly
- Ask for prioritization when many artifacts found
- Request follow-up actions for each finding

### REPORT Mode: Finding Summarization

**Use Cases:**
- Draft client-facing reports
- Organize findings by severity
- Generate executive summaries
- Create remediation recommendations

**Example Queries:**

```
"Summarize key findings from this assessment in report format"

"Group these vulnerabilities by risk level with CVSS scores"

"Draft an executive summary for non-technical stakeholders"

"What are the top 5 most critical findings and why?"
```

**Best Practices:**
- Use after completing major assessment phases
- Include all relevant logs and notes as context
- Request specific report sections (e.g., "Executive Summary", "Technical Findings")
- Ask for remediation priority recommendations

### RED Mode: Attack Chain Planning

**Use Cases:**
- Plan multi-step attack paths
- Optimize for OPSEC and stealth
- Identify detection opportunities for blue team
- Design proof-of-concept scenarios

**Example Queries:**

```
"Given domain user credentials, plan an attack chain to domain admin"

"I have code execution on a web server. Design a lateral movement strategy"

"How would a blue team detect each step of this attack chain?"

"Plan a stealthy privilege escalation path on this Linux system"
```

**Best Practices:**
- Clearly define starting position (e.g., "low-priv user", "external attacker")
- Request OPSEC considerations for each step
- Ask about detection/alerting for blue team perspective
- Emphasize proof-of-concept over actual damage

---

## Best Practices

### Context Management

**Maximize Context Quality:**
```bash
# Set up target config thoroughly
pentai-init-target project-alpha
vim ~/.config/pentai/targets/project-alpha.json

# Add detailed scope and notes:
{
  "name": "project-alpha",
  "scope": "10.20.30.0/24, *.alpha.internal, authorized by SOW dated 2025-01-15",
  "notes": "Web app pentest focusing on auth bypass and IDOR. Test account: testuser:TestPass123",
  "loot_paths": [
    "./logs/",
    "./scans/",
    "./captures/"
  ]
}
```

**Use File Context Effectively:**
```bash
# Explicit file
ai-recon --file nmap-full-scan.xml

# Auto-detection (searches ./nmap, ./logs, ./output)
cd project-dir
mkdir nmap logs
# PentAI will auto-find most recent file

# Environment variable
export PENTAI_FILE_CONTEXT=/path/to/important-log.txt
ai-recon
```

**Shell History Tips:**
```bash
# Keep history on (Ctrl+H) for context-aware responses
# AI sees your recent commands and can suggest next steps

# Clean history before sensitive operations
history -c  # If you don't want AI to see something

# Toggle history mid-session with Ctrl+H
```

### Session Management

**Organize by Target:**
```bash
# Use project directory structure
~/pentests/
├── client-a/
│   ├── .pentai-target (contains "client-a")
│   ├── nmap/
│   ├── logs/
│   └── loot/
├── client-b/
│   ├── .pentai-target (contains "client-b")
│   └── ...
└── internal-test/
    ├── .pentai-target (contains "internal-test")
    └── ...
```

**Log Management:**
```bash
# View recent sessions
pentai-log-view client-a

# Export session logs for report
cat ~/.local/share/pentai/client-a.jsonl | jq -r '.reply' > findings-summary.txt

# Archive logs after engagement
mkdir -p ~/pentests/client-a/pentai-logs
cp ~/.local/share/pentai/client-a.jsonl ~/pentests/client-a/pentai-logs/

# Clean up after engagement
rm ~/.local/share/pentai/old-target.jsonl
```

### API Key Security

**Secure Key Management:**
```bash
# In ~/.zshrc or ~/.bashrc
export AI_API_KEY="sk-..."

# Or use environment-specific keys
case "$PROJECT" in
  client-a)
    export AI_API_KEY="$CLIENT_A_API_KEY"
    ;;
  client-b)
    export AI_API_KEY="$CLIENT_B_API_KEY"
    ;;
esac

# For cloud-hosted keys (avoid committing to git)
export AI_API_KEY=$(aws secretsmanager get-secret-value --secret-id pentai-key --query SecretString --output text)
```

**Key Rotation:**
```bash
# Rotate keys regularly
# Update in password manager or secrets service
# Never commit to git or store in plain text files
```

---

## Advanced Techniques

### Custom Modes via Prompt Engineering

**Create Mode-Like Behavior:**
```bash
# Start in chat mode
./pentai.py --mode chat

# Use system-like prompts
You are a Linux privilege escalation expert. For each query:
1. Identify the current privilege level
2. List enumeration steps to find privesc vectors
3. Provide concrete exploit commands
4. Explain how to verify success

Now analyze: [paste linpeas output]
```

### Chaining Commands with Shell Integration

**Example 1: Automated Workflow**
```bash
#!/bin/bash
# pentest-workflow.sh

TARGET="$1"
echo "$TARGET" > .pentai-target

# Run nmap
echo "[*] Running nmap..."
nmap -sV -sC "$TARGET" -oA "scans/${TARGET}"

# Get AI recommendations
echo "[*] Getting recon recommendations..."
ai-recon > "reports/${TARGET}-next-steps.txt"

# Run recommended commands
echo "[*] Review: cat reports/${TARGET}-next-steps.txt"
```

**Example 2: Error-Driven Development**
```bash
# Try command, auto-diagnose errors
run_and_diagnose() {
  local cmd="$1"
  echo "[*] Running: $cmd"
  
  if ! eval "$cmd" 2>/tmp/err.log; then
    echo "[!] Command failed, asking AI..."
    ai-err
  fi
}

run_and_diagnose "hydra -L users.txt -P pass.txt ssh://target.com"
```

### Integrating with Other Tools

**Metasploit Integration:**
```bash
# After Metasploit session
msf6> sessions -i 1
meterpreter> sysinfo > /tmp/target-info.txt
meterpreter> background

# Get privesc suggestions
PENTAI_FILE_CONTEXT=/tmp/target-info.txt ai-red
```

**Burp Suite Integration:**
```bash
# Export HTTP history from Burp
# Save as http-history.xml

# Analyze for interesting endpoints/params
ai-loot http-history.xml
```

**OSINT Integration:**
```bash
# TheHarvester output
theHarvester -d target.com -b all > osint-results.txt

# Analyze OSINT for recon planning
PENTAI_FILE_CONTEXT=osint-results.txt ai-recon
```

### Custom LLM Backends

**Use Local Ollama:**
```bash
# In ~/.zshrc
export AI_BASE_URL="http://localhost:11434/v1"
export AI_MODEL="llama2"
export AI_API_KEY="ollama"  # Dummy key for local

# Run PentAI with local model
ai-recon
```

**Use Azure OpenAI:**
```bash
export AI_BASE_URL="https://your-resource.openai.azure.com"
export AI_MODEL="gpt-4"
export AI_API_KEY="your-azure-key"
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Incomplete Context

**Problem:**
```
Query: "What should I do next?"
AI: "I need more context about your current assessment phase..."
```

**Solution:**
```bash
# Ensure .pentai-target is set
ls .pentai-target || echo "my-target" > .pentai-target

# Keep shell history on (Ctrl+H should show "on")
# Provide explicit file if auto-detect fails
ai-recon --file nmap-output.xml
```

### Pitfall 2: Vague Queries

**Problem:**
```
Query: "Help"
AI: "I can assist with: command explanation, error diagnosis, ..."
```

**Solution:**
```
# Be specific
❌ "Help with nmap"
✅ "Explain nmap flags: -sS, -sV, -O. Which requires root?"

❌ "SQL injection"
✅ "I found SQLi in parameter 'id'. Show manual exploitation steps with sqlmap."
```

### Pitfall 3: Ignoring Mode-Specific Prompts

**Problem:**
```
# Using default mode (cmd) for recon planning
Query: "What recon should I do?"
AI: [Gives generic answer without analyzing context]
```

**Solution:**
```bash
# Use appropriate mode
ai-recon  # Automatically uses recon mode + context

# Or switch modes in TUI (F2)
```

### Pitfall 4: Sensitive Data in Logs

**Problem:**
```
# AI session logs contain real credentials
~/.local/share/pentai/target.jsonl:
{"user": "Found password: SuperSecret123", ...}
```

**Solution:**
```bash
# Sanitize queries before submission
❌ "I found password 'SuperSecret123', how to use it?"
✅ "I found a valid password, how to use it for lateral movement?"

# Encrypt logs after engagement
gpg -c ~/.local/share/pentai/sensitive-target.jsonl
rm ~/.local/share/pentai/sensitive-target.jsonl

# Set restrictive permissions
chmod 600 ~/.local/share/pentai/*.jsonl
```

### Pitfall 5: Over-Reliance on AI

**Problem:**
```
# Blindly following AI suggestions without understanding
[AI suggests complex exploit]
[User runs without understanding risks]
[Crashes target system]
```

**Solution:**
```
# Always understand before executing
1. Ask AI to explain each command component
2. Test in lab environment first
3. Verify AI suggestions with documentation
4. Use your professional judgment

# Ask follow-up questions
"What are the risks of this command?"
"Is there a safer way to verify the vulnerability?"
"Will this trigger IDS/IPS?"
```

---

## Integration Patterns

### Pattern 1: Continuous Feedback Loop

```bash
#!/bin/bash
# smart-scan.sh

while true; do
  # Run incremental scan
  ./run-next-scan.sh
  
  # Get AI analysis
  ai-recon > next-actions.txt
  
  # Present to user
  cat next-actions.txt
  read -p "Run suggested commands? (y/n) " -n 1 -r
  echo
  
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Extract and run commands
    grep '```' next-actions.txt | sed 's/```//g' | bash
  else
    break
  fi
done
```

### Pattern 2: Report Generation Pipeline

```bash
#!/bin/bash
# generate-report.sh

TARGET="$1"
OUTPUT="report-${TARGET}-$(date +%Y%m%d).md"

echo "# Penetration Test Report: $TARGET" > "$OUTPUT"
echo "" >> "$OUTPUT"

# Executive summary
echo "## Executive Summary" >> "$OUTPUT"
PENTAI_TARGET_NAME="$TARGET" ai-report --prefill "Generate executive summary" >> "$OUTPUT"

# Technical findings
echo "" >> "$OUTPUT"
echo "## Technical Findings" >> "$OUTPUT"
PENTAI_TARGET_NAME="$TARGET" ai-report --prefill "List all vulnerabilities found" >> "$OUTPUT"

# Recommendations
echo "" >> "$OUTPUT"
echo "## Recommendations" >> "$OUTPUT"
PENTAI_TARGET_NAME="$TARGET" ai-report --prefill "Prioritize remediation steps" >> "$OUTPUT"

echo "[*] Report generated: $OUTPUT"
```

### Pattern 3: Multi-Tool Correlation

```bash
#!/bin/bash
# correlate-findings.sh

TARGET="$1"

# Gather all tool outputs
cat scans/nmap-${TARGET}.nmap \
    logs/nikto-${TARGET}.txt \
    logs/dirbuster-${TARGET}.txt \
    > /tmp/all-findings-${TARGET}.txt

# Get AI correlation
PENTAI_FILE_CONTEXT="/tmp/all-findings-${TARGET}.txt" \
  ai-report --prefill "Correlate findings from nmap, nikto, and dirbuster. Identify critical attack paths."
```

---

## Security & Compliance

### Data Handling

**Sensitive Data Guidelines:**

1. **Target Scope Documents:**
   ```bash
   # Store in target config (not logs)
   {
     "scope": "10.0.1.0/24, authorized by SOW-2025-001",
     "notes": "Rules: No DoS, no social engineering, working hours only"
   }
   ```

2. **Credentials Found:**
   ```bash
   # Don't paste real credentials in queries
   ❌ "I found admin:P@ssw0rd123, how to use?"
   ✅ "I found valid admin credentials, how to use for privilege escalation?"
   
   # Store separately
   echo "admin:P@ssw0rd123" >> loot/credentials.txt
   chmod 600 loot/credentials.txt
   ```

3. **Client Data:**
   ```bash
   # Never include PII in queries
   ❌ "Found user John Doe, SSN 123-45-6789 in database"
   ✅ "Found PII in database, how to report this finding?"
   ```

### Compliance Considerations

**GDPR/Data Protection:**
- Don't send PII to AI APIs
- Use data minimization (only send necessary context)
- Document what data is shared with AI provider
- Inform client if using cloud AI services

**Industry Standards:**
```bash
# For regulated environments
# Use local LLM (Ollama) instead of cloud APIs
export AI_BASE_URL="http://localhost:11434/v1"
export AI_MODEL="llama2"

# Or use client-approved AI services
export AI_BASE_URL="https://client-approved-ai.internal"
```

### Audit Trail

**Maintaining Evidence:**
```bash
# Session logs are evidence of testing methodology
# Keep intact for client deliverables

# Archive entire pentai state
mkdir ~/deliverables/client-a/pentai-artifacts
cp ~/.config/pentai/targets/client-a.json ~/deliverables/client-a/pentai-artifacts/
cp ~/.local/share/pentai/client-a.jsonl ~/deliverables/client-a/pentai-artifacts/

# Include in final report
echo "## Testing Methodology" >> report.md
echo "AI-assisted testing was used for:" >> report.md
echo "- Command optimization and error diagnosis" >> report.md
echo "- Reconnaissance planning" >> report.md
echo "- Finding correlation and prioritization" >> report.md
```

### Provider Trust

**Choosing AI Providers:**

| Provider Type | Trust Level | Use Case |
|---------------|-------------|----------|
| Local (Ollama) | Highest | Highly sensitive assessments, regulated industries |
| Client-hosted | High | Client has their own AI infrastructure |
| Azure OpenAI | Medium-High | Enterprise clients with Azure agreements |
| OpenAI API | Medium | General pentests with non-sensitive context |

**Risk Assessment:**
```bash
# Questions to ask before using cloud AI:
# 1. Does client contract allow 3rd party tools?
# 2. What data retention policy does AI provider have?
# 3. Is the assessment in a regulated industry (healthcare, finance)?
# 4. Are you sending actual credentials/PII to the AI?

# If uncertain, use local model or sanitize all inputs
```

---

## Summary

**Key Takeaways:**

1. **Context is King**: Better context = better responses. Use target configs, shell history, and file snippets.

2. **Right Mode for Right Task**: Don't use cmd mode for everything. Each mode is optimized for specific workflows.

3. **Iterative Approach**: Run AI after each major step. Let it guide your next actions.

4. **Security First**: Never compromise engagement security for convenience. Sanitize sensitive data.

5. **Human Judgment**: AI is an assistant, not a replacement. Always understand and verify suggestions.

6. **Document Everything**: Session logs are valuable for methodology documentation and lessons learned.

**Anti-Patterns to Avoid:**
- ❌ Blind command execution
- ❌ Sending raw credentials in queries
- ❌ Using wrong mode for task
- ❌ Ignoring context setup
- ❌ Not reading AI warnings about risks

**Success Patterns:**
- ✅ Set up target configs properly
- ✅ Use mode-specific workflows
- ✅ Iterate: scan → analyze → act → repeat
- ✅ Sanitize sensitive data
- ✅ Maintain audit trail
- ✅ Verify AI suggestions independently

Happy (authorized) hacking! 🎯🔒
