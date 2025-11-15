# Contributing to PentAI-TUI

Thank you for your interest in contributing to PentAI-TUI! This document provides guidelines and information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Environment Setup](#development-environment-setup)
4. [Project Structure](#project-structure)
5. [Contribution Guidelines](#contribution-guidelines)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation Standards](#documentation-standards)
8. [Pull Request Process](#pull-request-process)
9. [Common Contribution Areas](#common-contribution-areas)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. This project is designed to support authorized security testing, and all contributions must align with ethical security practices.

### Expected Behavior

- Use respectful and inclusive language
- Focus on constructive feedback
- Accept responsibility for mistakes
- Prioritize security and ethical considerations
- Support authorized penetration testing only

### Unacceptable Behavior

- Contributions that enable unauthorized access or illegal activities
- Harassment, discrimination, or hostile behavior
- Sharing exploits without responsible disclosure
- Malicious code or backdoors

---

## Getting Started

### Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **Git** for version control
- **Zsh or Bash** shell
- **Virtual environment** (recommended)
- **OpenAI API key** or compatible LLM endpoint

### First-Time Setup

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pentai-tui.git
cd pentai-tui

# Add upstream remote
git remote add upstream https://github.com/kain-ableton/pentai-tui.git

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -r requirements-dev.txt  # If it exists

# Set up API key for testing
export AI_API_KEY="your-test-key"

# Run the application
./pentai.py --mode cmd
```

---

## Development Environment Setup

### Recommended Tools

1. **IDE/Editor**
   - VS Code with Python extension
   - PyCharm
   - Vim/Neovim with LSP

2. **Python Tools**
   - `black` - Code formatting
   - `flake8` - Linting
   - `mypy` - Type checking
   - `pytest` - Testing framework
   - `ipython` - Interactive testing

3. **Git Tools**
   - `git-flow` - Branch management
   - `pre-commit` - Git hooks

### Installing Development Tools

```bash
# Install development tools
pip install black flake8 mypy pytest pytest-cov ipython

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Configuration Files

Create these files in your local development environment:

**`.vscode/settings.json`** (VS Code users):
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true
}
```

**`.editorconfig`**:
```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_style = space
indent_size = 4
max_line_length = 100

[*.md]
trim_trailing_whitespace = false
```

---

## Project Structure

```
pentai-tui/
├── pentai.py              # Main application entry point
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies (if added)
├── setup.sh              # Installation script
├── zsh_snippets.sh       # Shell integration helpers
│
├── docs/                 # Documentation (if reorganized)
│   ├── ANALYSIS.md
│   ├── ARCHITECTURE.md
│   ├── USAGE_GUIDE.md
│   └── DOCUMENTATION_INDEX.md
│
├── tests/                # Test suite (to be added)
│   ├── __init__.py
│   ├── test_context.py
│   ├── test_modes.py
│   ├── test_logger.py
│   └── test_integration.py
│
├── examples/             # Example configurations (to be added)
│   ├── target_configs/
│   └── workflows/
│
└── .github/              # GitHub workflows
    └── workflows/
        └── ci.yml        # CI/CD pipeline
```

---

## Contribution Guidelines

### Branch Naming Convention

Use descriptive branch names following this pattern:

- `feature/add-new-mode` - New features
- `fix/context-loading-bug` - Bug fixes
- `docs/improve-readme` - Documentation updates
- `refactor/simplify-llm-client` - Code refactoring
- `test/add-mode-tests` - Test additions

### Commit Message Format

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(modes): add forensics mode for artifact analysis

- Implement forensics mode with timeline reconstruction
- Add file hash verification
- Include EXIF data extraction prompts

Closes #42
```

```
fix(context): handle missing zsh history gracefully

Previously crashed when .zsh_history was missing.
Now returns empty list and logs warning.

Fixes #38
```

### Code Style Guidelines

#### Python Style

Follow PEP 8 with these specifics:

```python
# Good: Clear naming, type hints, docstrings
def load_target(name_override: Optional[str] = None) -> TargetContext:
    """
    Load TargetContext from config file if present, else from env.
    
    Args:
        name_override: Optional explicit target name
        
    Returns:
        TargetContext with loaded configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    # Implementation
    pass

# Good: List comprehensions for simple transforms
valid_commands = [cmd.strip() for cmd in commands if cmd.strip()]

# Good: Context managers for file operations
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Avoid: Nested ternaries
# Bad
result = "a" if x else "b" if y else "c"
# Good
if x:
    result = "a"
elif y:
    result = "b"
else:
    result = "c"
```

#### Type Hints

Use type hints throughout:

```python
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

def build_context_block(
    target: Optional[TargetContext],
    include_history: bool,
    file_path: Optional[Path],
) -> str:
    """Build context block for LLM prompt."""
    pass
```

#### Documentation

All public functions need docstrings:

```python
def auto_detect_context_file() -> Optional[Path]:
    """
    Try to auto-detect a useful log/output file near CWD.

    Prioritizes:
      - ./nmap, ./logs, ./output
      - *.nmap, *.gnmap, *.xml, *.log, *.txt
    
    This should catch typical nmap/Jok3r outputs if you run 
    PentAI from the project dir.
    
    Returns:
        Path to most recently modified relevant file, or None
    """
    pass
```

---

## Testing Guidelines

### Test Structure

```python
# tests/test_context.py
import pytest
from pathlib import Path
from pentai import load_shell_history, auto_detect_context_file

class TestShellHistory:
    """Test shell history loading functionality."""
    
    def test_load_history_success(self, tmp_path):
        """Should load commands from zsh history."""
        hist_file = tmp_path / ".zsh_history"
        hist_file.write_text(": 1700000000:0;ls\n: 1700000001:0;pwd\n")
        
        # Mock Path.home() to return tmp_path
        with pytest.mock.patch('pathlib.Path.home', return_value=tmp_path):
            commands = load_shell_history(limit=2)
            
        assert len(commands) == 2
        assert commands[0] == "ls"
        assert commands[1] == "pwd"
    
    def test_load_history_missing_file(self, tmp_path):
        """Should return empty list when history file missing."""
        with pytest.mock.patch('pathlib.Path.home', return_value=tmp_path):
            commands = load_shell_history()
            
        assert commands == []

class TestFileDetection:
    """Test auto-detection of context files."""
    
    def test_detect_nmap_file(self, tmp_path):
        """Should detect nmap files in current directory."""
        nmap_file = tmp_path / "scan.nmap"
        nmap_file.write_text("# Nmap scan")
        
        with pytest.mock.patch('pathlib.Path.cwd', return_value=tmp_path):
            detected = auto_detect_context_file()
            
        assert detected == nmap_file
    
    def test_detect_most_recent(self, tmp_path):
        """Should return most recently modified file."""
        old_file = tmp_path / "old.log"
        new_file = tmp_path / "new.log"
        
        old_file.write_text("old")
        # Simulate time passing
        import time
        time.sleep(0.1)
        new_file.write_text("new")
        
        with pytest.mock.patch('pathlib.Path.cwd', return_value=tmp_path):
            detected = auto_detect_context_file()
            
        assert detected == new_file
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_context.py

# Run specific test
pytest tests/test_context.py::TestShellHistory::test_load_history_success

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

### Test Coverage Goals

- **Unit tests**: 80%+ coverage for core logic
- **Integration tests**: Key workflows end-to-end
- **Mock external dependencies**: API calls, file system

---

## Documentation Standards

### When to Update Documentation

Update documentation when you:

- Add a new mode
- Change configuration options
- Add or modify CLI arguments
- Change behavior of existing features
- Add integration with new tools
- Fix bugs that users might encounter

### Documentation Files to Update

1. **README.md** - Quick start and basic usage
2. **USAGE_GUIDE.md** - Detailed usage patterns
3. **ARCHITECTURE.md** - Technical changes
4. **ANALYSIS.md** - Design decisions
5. **Inline docstrings** - Function documentation

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Use proper markdown formatting
- Include cross-references

---

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run quality checks**
   ```bash
   # Format code
   black pentai.py
   
   # Run linter
   flake8 pentai.py
   
   # Type check
   mypy pentai.py
   
   # Run tests
   pytest
   ```

3. **Test manually**
   ```bash
   # Test each affected mode
   ./pentai.py --mode cmd
   ./pentai.py --mode recon
   # etc.
   ```

### PR Description Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tested manually with [describe scenarios]
- [ ] Added/updated unit tests
- [ ] Tested with real LLM API
- [ ] Tested with mock/local LLM

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated and passing

## Screenshots (if applicable)
[Add screenshots here]

## Related Issues
Closes #[issue number]
```

### Review Process

1. **Automated checks** run via GitHub Actions
2. **Maintainer review** - May request changes
3. **Discussion** - Engage constructively with feedback
4. **Approval** - Once approved, will be merged

---

## Common Contribution Areas

### 1. Adding a New Mode

**Steps:**

1. Define mode instructions in `pentai.py`:
   ```python
   NEWMODE_INSTRUCTIONS = """
   Mode: Your New Mode.
   Purpose: ...
   Rules: ...
   """
   ```

2. Register the mode:
   ```python
   MODES = ["cmd", "chat", "recon", "loot", "report", "red", "newmode"]
   
   MODE_INSTRUCTIONS = {
       # existing modes...
       "newmode": NEWMODE_INSTRUCTIONS,
   }
   
   MODE_DEFAULT_PROMPTS = {
       # existing modes...
       "newmode": "Default prompt for new mode...",
   }
   ```

3. Add zsh helper (optional):
   ```bash
   ai-newmode() {
     python3 "$HOME/bin/pentai.py" \
       --mode newmode \
       --prefill "Your default prompt here"
   }
   ```

4. Update documentation:
   - USAGE_GUIDE.md - Add usage section
   - ARCHITECTURE.md - Update mode list
   - README.md - Mention new mode

5. Add tests:
   ```python
   def test_newmode_instructions():
       """Verify newmode has proper instructions."""
       assert "newmode" in MODES
       assert "newmode" in MODE_INSTRUCTIONS
   ```

### 2. Improving Context Detection

**Example: Add Git context**

```python
def load_git_context(limit: int = 5) -> Optional[str]:
    """Load recent git commits and branch info."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "log", f"-n{limit}", "--oneline"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True
            ).stdout.strip()
            return f"Branch: {branch}\n{result.stdout}"
    except Exception:
        pass
    return None
```

### 3. Adding LLM Provider Support

**Example: Azure OpenAI**

```python
class AzureOpenAIClient:
    """Azure OpenAI client implementation."""
    
    def __init__(self):
        self.api_key = os.environ.get("AZURE_OPENAI_KEY")
        self.endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        
    def chat(self, messages: List[dict]) -> str:
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version=2023-05-15"
        # Implementation
```

### 4. Enhancing Session Logging

**Example: Add export functionality**

```python
def export_session_report(target_name: str, format: str = "markdown") -> str:
    """Export session logs as formatted report."""
    log_file = get_data_dir() / f"{target_name}.jsonl"
    
    if format == "markdown":
        return _export_markdown(log_file)
    elif format == "json":
        return _export_json(log_file)
    elif format == "html":
        return _export_html(log_file)
```

---

## Getting Help

### Resources

- **Documentation**: Read all docs in `DOCUMENTATION_INDEX.md`
- **Issues**: Check existing issues for similar problems
- **Discussions**: Use GitHub Discussions for questions
- **Code**: Read through `pentai.py` - it's well-commented

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions and reviews

### Quick Tips

1. **Start small**: Fix typos, improve docs, add tests
2. **Ask first**: Open an issue to discuss big changes
3. **Read code**: Understand existing patterns before adding new code
4. **Test thoroughly**: Manual testing is as important as automated tests
5. **Be patient**: Maintainers review PRs as time permits

---

## License

By contributing to PentAI-TUI, you agree that your contributions will be licensed under the same license as the project (check LICENSE file).

---

## Thank You!

Your contributions make PentAI-TUI better for the security community. Whether you're fixing a typo or adding a major feature, every contribution is valued.

**Happy contributing!** 🛠️🔒
