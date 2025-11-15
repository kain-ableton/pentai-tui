# PentAI TUI v2.0 Enhanced – Professional Terminal AI for Pentesting

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Textual](https://img.shields.io/badge/TUI-Textual-purple.svg)](https://textual.textualize.io/)

**PentAI TUI** is a world-class terminal-based AI assistant for penetration testers and security researchers. With a professional, feature-rich interface rivaling GUI applications, it provides intelligent guidance across all phases of security assessments.

## ✨ Latest Updates (v2.0)

### 🎨 Major UI Overhaul
- **150+ lines of CSS styling** - Professional design with rich colors
- **Box-drawing borders** - Clean message formatting and visual hierarchy  
- **Mode-specific themes** - 9 color-coded modes with emoji indicators
- **Live status bar** - Real-time session info with icons (📜📄💬🎯)
- **Modal dialogs** - Target info screen with complete details

### ⌨️ Enhanced Keyboard Shortcuts
- **F1** - Comprehensive help screen with full documentation
- **F3** - Target information modal (scope, hosts, findings, credentials)
- **F4** - Mode-specific quick command suggestions
- **F5** - Detailed session statistics
- **Ctrl+L** - Clear log with confirmation
- **Ctrl+S** - Save session with visual feedback

### 💡 New Interactive Features
- Welcome screen with ASCII art
- Formatted message boxes (user/AI)
- Visual mode switching feedback
- Context file information display
- Success/error styled messages
- Message counter tracking

## 🎯 Nine Specialized Modes

| Mode | Emoji | Description |
|------|-------|-------------|
| **CMD** | ⚡ | Command explanation and error troubleshooting |
| **CHAT** | 💬 | General pentesting methodology and Q&A |
| **RECON** | 🔍 | Reconnaissance and enumeration planning |
| **LOOT** | 💰 | Credential and artifact discovery from logs |
| **REPORT** | 📋 | Structured report and note generation |
| **RED** | 🎯 | Red team attack chain planning |
| **EXPLOIT** | 💣 | Exploit development and vulnerability analysis |
| **OSINT** | 🌐 | Open-source intelligence gathering |
| **PRIVESC** | ⬆️ | Privilege escalation guidance |

## 🚀 Key Features

### 🎨 Professional UI
- **Rich CSS styling** with 150+ lines of custom theming
- **Box-drawing characters** for clean message borders
- **Full color palette** with mode-specific themes
- **Status bar** with live emoji icons
- **Modal screens** for detailed information
- **Formatted messages** with visual hierarchy

### ⌨️ Extensive Keyboard Shortcuts
- **10 shortcuts** (F1-F5, Ctrl+H/L/S/T/C)
- Context-sensitive help (F1)
- Quick commands per mode (F4)
- Session statistics (F5)
- Target information modal (F3)

### 🎯 Smart Features
- 📁 **Auto-detection** of scan results and log files
- 💾 **Session logging** with full context tracking
- 🔄 **Streaming responses** from AI models
- 🌐 **Custom API endpoints** (OpenAI, local LLMs)
- 🏷️ **Target management** - tags, hosts, credentials, findings
- 📊 **Message tracking** with counters and history

### 🤖 AI Integration

## 📦 Installation

### Quick Install
```bash
# Clone or download
git clone https://github.com/yourusername/pentai-tui.git
cd pentai-tui

# Install dependencies
python3 -m pip install --user -r requirements.txt

# Make executable
chmod +x pentai.py

# Optional: Link to PATH
sudo ln -s $(pwd)/pentai.py /usr/local/bin/pentai
```

### Requirements
- Python 3.8+
- OpenAI API key or compatible endpoint  
- Terminal with 256 color support (most modern terminals)
- Textual 6.6.0+ (installed via requirements.txt)

## 📸 Screenshots

### Welcome Screen
```
╔══════════════════════════════════════════════════════════════╗
║           Welcome to PentAI TUI v2.0 Enhanced                ║
║        AI-Powered Penetration Testing Assistant              ║
╚══════════════════════════════════════════════════════════════╝

Press F1 for help | F2 to cycle modes | F3 for stats | F4 for quick commands

Current Mode: ⚡ Command Analysis
```

### Message Display
```
╭─ You
│ How do I enumerate SMB shares?
╰────────────────────────────────────────────────────────

╭─ AI Assistant  
│ To enumerate SMB shares, use these tools:
│ 
│ 1. smbclient:  smbclient -L //target -N
│ 2. enum4linux: enum4linux -S target
│ 3. smbmap:     smbmap -H target
╰────────────────────────────────────────────────────────
Context: scan.xml (hash: a3f2b8c9...)
```

### Status Bar
```
📜 History: ON | 📄 Context: scan.xml | 💬 Messages: 15 | 🎯 Target: webapp-test
```

## ⚙️ Configuration

### Essential Setup
```bash
# Required: Set your API key
export AI_API_KEY="sk-your-openai-key-here"

# Optional: Custom settings
export AI_BASE_URL="https://api.openai.com/v1"
export AI_MODEL="gpt-4o-mini"
export PENTAI_TARGET_NAME="default-project"

# Add to shell profile for persistence
echo 'export AI_API_KEY="sk-..."' >> ~/.bashrc
```

### Target Configuration
```bash
# Create a new target
pentai --init-target webapp-pentest

# Edit target details
vim ~/.config/pentai/targets/webapp-pentest.json

# Set as current target (per-directory)
echo "webapp-pentest" > .pentai-target
```

## 🎮 Usage

### Basic Usage
```bash
# Start with default mode
pentai

# Start in specific mode
pentai --mode recon

# Use with context file
pentai --mode loot --file burp-output.txt

# Work with specific target
pentai --target webapp-pentest --mode report
```

### Keyboard Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| **F1** | Help | Show comprehensive help screen |
| **F2** | Cycle Modes | Switch between 9 specialized modes |
| **F3** | Target Info | Display target details modal |
| **F4** | Quick Commands | Mode-specific command suggestions |
| **F5** | Statistics | View session and target stats |
| **Ctrl+H** | Toggle History | Shell history context on/off |
| **Ctrl+L** | Clear Log | Clear chat with confirmation |
| **Ctrl+S** | Save Session | Export session to file |
| **Ctrl+T** | Theme | Toggle color theme (coming soon) |
| **Ctrl+C** | Exit | Quit application |

### Mode Examples
| **Ctrl+L** | Clear chat log |
| **Ctrl+S** | Save session to file |
| **Ctrl+C** | Exit application |

### Mode Examples

#### Command Analysis (CMD)
```bash
pentai --mode cmd
> nmap -sS -p- -T4 192.168.1.1
# AI explains each flag, suggests improvements
```

#### Recon Planning (RECON)
```bash
# Auto-loads recent nmap scans
pentai --mode recon --file nmap/scan.xml
> "What should I enumerate next?"
# AI analyzes results, suggests next steps
```

#### Credential Hunting (LOOT)
```bash
pentai --mode loot --file app-logs/*.log
> "Find secrets and credentials"
# AI extracts API keys, passwords, tokens
```

#### Exploit Development (EXPLOIT)
```bash
pentai --mode exploit
> "Help with CVE-2021-44228 exploitation"
# AI provides payloads, tools, techniques
```

#### Privilege Escalation (PRIVESC)
```bash
pentai --mode privesc --file linpeas.txt
> "Identify escalation vectors"
# AI prioritizes findings, suggests exploits
```

## 📚 Documentation

### Core Documentation
- **[README.md](README.md)** - This file (overview and quick start)
- **[USAGE.md](USAGE.md)** - Complete usage guide (400+ lines)
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world scenarios (500+ lines)
- **[QUICKREF.md](QUICKREF.md)** - Quick reference card

### Feature Documentation  
- **[FEATURES.md](FEATURES.md)** - Detailed feature list
- **[UI_ENHANCEMENTS.md](UI_ENHANCEMENTS.md)** - UI/UX improvements
- **[VISUAL_COMPARISON.md](VISUAL_COMPARISON.md)** - Before/after comparison
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

### Technical Documentation
- **[FIXED.md](FIXED.md)** - Import error resolution
- **[ENHANCEMENTS.md](ENHANCEMENTS.md)** - Technical enhancement details

## 🗂️ Project Structure

```
pentai-tui/
├── pentai.py              # Main application (~1150 lines)
├── requirements.txt       # Python dependencies
├── setup.sh              # Automated setup script
├── zsh_snippets.sh       # Shell integration (~250 lines)
│
├── README.md             # Overview (you are here)
├── FEATURES.md           # Feature documentation
├── USAGE.md              # Usage guide (400+ lines)
├── EXAMPLES.md           # Practical examples (500+ lines)
├── QUICKREF.md           # Quick reference
├── CHANGELOG.md          # Version history
├── UI_ENHANCEMENTS.md    # UI enhancement details
├── VISUAL_COMPARISON.md  # Before/after visuals
└── LICENSE               # MIT license

Configuration & Data:
~/.config/pentai/targets/  # Target configurations
~/.local/share/pentai/     # Session logs (JSONL)
.pentai-target             # Per-directory target file
```

## 🎨 UI Features

### Visual Design
- ✨ **150+ lines of CSS** - Professional styling
- 📦 **Box-drawing borders** - Clean message formatting
- 🎨 **9 color themes** - Mode-specific palettes
- 📊 **Status indicators** - Live session info
- 💬 **Formatted messages** - User/AI distinction

### Interactive Elements
- 🆘 **Help system (F1)** - Comprehensive in-app docs
- 📊 **Statistics (F5)** - Session and target metrics
- 🎯 **Target modal (F3)** - Complete project details
- ⚡ **Quick commands (F4)** - Mode-specific suggestions
- 🔄 **Visual feedback** - All actions confirmed

## 🔧 Advanced Features

### Local LLM Support
```bash
# Use with LM Studio
export AI_BASE_URL="http://localhost:1234/v1"
export AI_API_KEY="not-needed"

# Use with Ollama
export AI_BASE_URL="http://localhost:11434/v1"
```

### Shell Integration
```bash
# Add to ~/.bashrc or ~/.zshrc
pai() {
    pentai --mode "${1:-cmd}" --prefill "$(fc -ln -1)"
}

# Usage: run a command, then analyze it
nmap -sV target.com
pai cmd
```

### Session Management
```bash
# View recent activity
pentai --view-logs --last 20

# Export session
pentai --view-logs --target webapp-pentest > session-export.txt

# Save current chat
# Press Ctrl+S during session
```

## 🎯 Use Cases

- **Penetration Testing** - Real-time AI guidance during assessments
- **Bug Bounty Hunting** - Rapid vulnerability analysis and exploitation
- **Red Team Operations** - Attack chain planning with OPSEC advice
- **CTF Competitions** - Quick hints and methodology guidance
- **Security Research** - Vulnerability analysis and exploit development
- **Learning & Training** - Interactive pentesting education
- **Report Writing** - Automated documentation generation
- **Tool Troubleshooting** - Command explanation and error resolution

## 📈 Performance & Metrics

### UI Improvements (v2.0)
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| UI Code Lines | ~50 | ~450 | **+800%** |
| CSS Styling | 0 | 150+ | **∞** |
| Key Bindings | 3 | 10 | **+233%** |
| Visual Elements | 1 | 20+ | **+1900%** |
| Help Screens | 0 | 3 | **∞** |
| Color Usage | None | Full palette | **∞** |

### Features
- **9 specialized modes** for different pentesting phases
- **10 keyboard shortcuts** for efficient navigation
- **150+ lines of CSS** for professional styling
- **3 help screens** with comprehensive documentation
- **Multi-target support** with persistent configurations
- **Session logging** with full context tracking

## 🔒 Security & Privacy

- API keys never logged or transmitted except to configured endpoint
- Session logs stored locally only
- No telemetry or external data collection
- All analysis happens via your AI API
- Credentials in target configs are local-only

## ⚠️ Legal Notice

**PentAI TUI is designed for authorized security testing only.**

Users must:
- Obtain proper authorization before testing any systems
- Comply with all applicable laws and regulations
- Use the tool ethically and responsibly
- Respect scope limitations and rules of engagement

The authors assume no liability for misuse of this tool.

## 🤝 Contributing

Contributions welcome! We're looking for:
- **Additional modes** - New specialized pentesting modes
- **Tool parsers** - Parse output from security tools
- **Report templates** - Generate formatted reports
- **Integration plugins** - Connect with other tools
- **UI improvements** - Enhance visual design
- **Documentation** - Improve guides and examples
- **Bug fixes** - Report and fix issues

## 🏆 Comparison with Other TUIs

| Feature | PentAI v2.0 | htop | lazygit | k9s |
|---------|-------------|------|---------|-----|
| Rich Colors | ✅ | ✅ | ✅ | ✅ |
| Box Borders | ✅ | ✅ | ✅ | ✅ |
| Modal Dialogs | ✅ | ❌ | ✅ | ✅ |
| Status Bar | ✅ | ✅ | ✅ | ✅ |
| Help System | ✅ | ✅ | ✅ | ✅ |
| CSS Styling | ✅ | N/A | N/A | N/A |
| Context-Aware | ✅ | ❌ | ❌ | ✅ |
| Multi-Mode | ✅ (9) | ❌ | ❌ | ✅ |
| AI Integration | ✅ | ❌ | ❌ | ❌ |

**PentAI TUI ranks among best-in-class terminal applications!**

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [Textual](https://textual.textualize.io/) - Modern TUI framework
- Powered by OpenAI API (or compatible alternatives)
- Inspired by modern pentesting workflows and tools
- Community feedback and contributions

## 📞 Support & Community

- **Issues**: Report bugs or request features
- **Discussions**: Ask questions and share tips
- **Documentation**: Extensive guides and examples included
- **Updates**: Check CHANGELOG.md for latest changes

## 🚀 Quick Start Checklist

- [ ] Install dependencies: `./setup.sh`
- [ ] Set API key: `export AI_API_KEY="sk-..."`
- [ ] Create target: `pentai --init-target myproject`
- [ ] Run app: `pentai --mode recon`
- [ ] Press F1 for help inside the app
- [ ] Read USAGE.md for detailed guide
- [ ] Check EXAMPLES.md for real scenarios

---

<div align="center">

**PentAI TUI v2.0 Enhanced**

*Where terminal meets excellence*

[![Made with ❤️ by security professionals](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/yourusername/pentai-tui)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/pentai-tui/pulls)

</div>
