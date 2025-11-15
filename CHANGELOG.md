# Changelog

All notable changes to PentAI TUI will be documented in this file.

## [2.0.0] - 2024-11-15

### Added
- **Three new specialized modes:**
  - Exploit mode for vulnerability analysis and exploit development
  - OSINT mode for intelligence gathering guidance
  - Privesc mode for privilege escalation assistance

- **Enhanced UI/UX:**
  - Rich header with emoji indicators for better visual feedback
  - Footer bar with key binding hints
  - Target information screen (F3) showing detailed project data
  - Help screen (F1) with comprehensive documentation
  - Quick command templates (F4) per mode
  - CSS styling for improved visual hierarchy

- **Extended target context:**
  - Tags for target categorization
  - Host tracking for discovered systems
  - Credentials storage in target configs
  - Findings documentation within targets

- **New keyboard shortcuts:**
  - F1: Show help and documentation
  - F3: Display target information
  - F4: Load quick command templates
  - Ctrl+L: Clear chat log
  - Ctrl+S: Save session to file

- **API enhancements:**
  - Streaming support for real-time responses
  - Configurable temperature parameter
  - Increased max tokens to 4096
  - Extended timeout to 120 seconds
  - Model default changed to gpt-4o-mini

- **Additional features:**
  - Safe command execution helper with timeout
  - Expanded file snippet loading (8KB from 4KB)
  - Comprehensive setup script (setup.sh)
  - Extensive documentation (FEATURES.md, USAGE.md, EXAMPLES.md)

### Changed
- Improved header display with compact status indicators
- Enhanced mode instructions with more detailed guidance
- Better error handling and user feedback
- Updated default AI model to gpt-4o-mini
- Expanded context loading capabilities

### Fixed
- File snippet loading edge cases
- Target configuration parsing robustness
- Session logging reliability

## [1.0.0] - 2024-10-01

### Added
- Initial release with six core modes:
  - CMD: Command & error assistant
  - CHAT: General pentest chat
  - RECON: Recon/enumeration planner
  - LOOT: Credential/artefact finder
  - REPORT: Report generation
  - RED: Red team planning

- **Core features:**
  - Target configuration system
  - Session persistence with JSONL logging
  - Shell history integration
  - Auto-detection of scan results
  - Context-aware AI responses
  - Multi-target project support

- **Configuration:**
  - Environment variable support
  - Per-directory target files
  - Customizable API endpoints
  - Flexible model selection

- **CLI features:**
  - Target initialization
  - Log viewing
  - Mode selection
  - File context loading
  - Prefill support

### Documentation
- README.md with quick start guide
- Inline code documentation
- CLI help text
- zsh_snippets.sh for shell integration

---

## Roadmap

### Planned for 2.1.0
- [ ] Multi-target session support
- [ ] Export reports in multiple formats (MD, PDF, HTML)
- [ ] Built-in tool output parsers (nmap, sqlmap, etc.)
- [ ] Custom mode creation system
- [ ] Plugin architecture

### Planned for 2.2.0
- [ ] Collaborative session sharing
- [ ] Timeline view of activities
- [ ] Screenshot/evidence capture
- [ ] Integration with vulnerability databases
- [ ] Advanced filtering and search in logs

### Future Considerations
- [ ] Web interface option
- [ ] Mobile companion app
- [ ] Team collaboration features
- [ ] AI model fine-tuning for pentesting
- [ ] Integration with popular frameworks (Metasploit, Burp, etc.)

---

[2.0.0]: https://github.com/yourusername/pentai-tui/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/yourusername/pentai-tui/releases/tag/v1.0.0
