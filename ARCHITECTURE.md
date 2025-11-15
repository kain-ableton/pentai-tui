# PentAI-TUI Architecture Documentation

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
├─────────────────────────────────────────────────────────────┤
│  Textual TUI App (PentAIApp)    │   Zsh Helper Functions   │
│  - Mode management              │   - Wrapper scripts      │
│  - Input handling               │   - Context prefilling   │
│  - Display rendering            │   - Quick commands       │
└─────────────────┬───────────────┴──────────────┬────────────┘
                  │                               │
                  v                               v
┌─────────────────────────────────────────────────────────────┐
│                    Application Logic Layer                   │
├─────────────────────────────────────────────────────────────┤
│  Context Manager          │  Mode System                     │
│  - Shell history          │  - cmd, chat, recon             │
│  - File detection         │  - loot, report, red            │
│  - Target config          │  - Mode-specific prompts        │
│                           │                                  │
│  Prompt Builder           │  LLM Client                      │
│  - System prompts         │  - API abstraction              │
│  - Context injection      │  - Request/response handling    │
│  - Message formatting     │  - Error handling               │
└─────────────────┬───────────────────────────────┬───────────┘
                  │                               │
                  v                               v
┌─────────────────────────────────────────────────────────────┐
│                    Data & Storage Layer                      │
├─────────────────────────────────────────────────────────────┤
│  Configuration Storage    │  Session Logger                  │
│  ~/.config/pentai/        │  ~/.local/share/pentai/         │
│  - Target configs (JSON)  │  - Session logs (JSONL)         │
│  - Scope definitions      │  - Query/response history       │
│  - Loot paths             │  - Context hashes               │
└─────────────────┬───────────────────────────────┬───────────┘
                  │                               │
                  v                               v
┌─────────────────────────────────────────────────────────────┐
│                     External Services                        │
├─────────────────────────────────────────────────────────────┤
│  LLM API (OpenAI-compatible)  │  File System               │
│  - Chat completions           │  - Log files               │
│  - Configurable endpoint      │  - Scan outputs            │
│  - Model selection            │  - Tool results            │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Target & Configuration Management

#### TargetContext
```python
@dataclass
class TargetContext:
    name: str         # Target identifier
    scope: str        # Authorized scope description
    notes: str        # Assessment notes
    loot_paths: List[str]  # Paths to monitor for artifacts
```

#### Configuration Resolution Strategy
1. **Explicit target name** (--target CLI arg)
2. **Environment variable** (PENTAI_TARGET_NAME)
3. **Local marker file** (.pentai-target in CWD)
4. **Default fallback** ("default")

#### Storage Locations
- **Config directory**: `$PENTAI_CONFIG_DIR` or `~/.config/pentai/`
- **Data directory**: `$PENTAI_DATA_DIR` or `~/.local/share/pentai/`

### 2. Context Gathering System

#### Context Sources

**Shell History**
- Source: `~/.zsh_history`
- Format: `: timestamp:duration;command`
- Default limit: 10 most recent commands
- Purpose: Understand pentester's workflow and recent actions

**File Snippets**
- Detection strategy:
  1. Explicit path (--file argument)
  2. Environment variable (PENTAI_FILE_CONTEXT)
  3. Auto-detection in priority directories:
     - `./nmap/`, `./logs/`, `./output/`, `./` (CWD)
  4. Extensions: `.nmap`, `.gnmap`, `.xml`, `.log`, `.txt`
- Selection: Most recently modified file
- Read limit: 4096 bytes (configurable)
- Hash: SHA-256 of first 64KB for correlation

**Target Configuration**
- Loaded from JSON config files
- Merged with environment variables
- Includes scope, notes, and loot paths

#### Context Block Structure
```
Target name: <name>
Scope:
<scope details>

Notes:
<assessment notes>

--- CONTEXT SEPARATOR ---

Recent shell commands:
<command 1>
<command 2>
...

--- CONTEXT SEPARATOR ---

File snippet from <path>:
<first 4096 bytes>
```

### 3. Mode System Architecture

#### Mode Components
Each mode consists of:
1. **Mode identifier**: String key ("cmd", "chat", etc.)
2. **System instructions**: Specialized prompt for the mode
3. **Default prefill**: Suggested user input for the mode
4. **Keyboard shortcut**: F2 to cycle through modes

#### Mode Prompting Strategy

**Base System Prompt** (shared across all modes):
- Identity: Technical assistant for pentesting
- Constraints: Authorized targets only, no execution
- Style: Concise, precise, command-focused

**Mode-Specific Instructions** (appended to base):
- **cmd**: Command explanation + error diagnosis
- **chat**: General Q&A with methodology focus
- **recon**: Phased enumeration planning
- **loot**: Artifact extraction and prioritization
- **report**: Structured note generation
- **red**: Attack chain planning with OPSEC

#### Mode Switching Behavior
- Preserves context (target, history, file)
- Updates input placeholder
- Maintains previous responses in chat log
- No state reset (continuous session)

### 4. LLM Client Architecture

#### Configuration
- **Endpoint**: `AI_BASE_URL` (default: OpenAI)
- **API Key**: `AI_API_KEY` (required)
- **Model**: `AI_MODEL` (default: "gpt-5.1-mini")
- **Temperature**: 0.2 (consistency over creativity)
- **Timeout**: 120 seconds

#### Message Flow
```
System Prompt (base + mode-specific)
    ↓
User Message (context block + user input)
    ↓
API Request (chat/completions)
    ↓
Response Processing
    ↓
Display + Logging
```

#### Error Handling
- Network errors: Caught and displayed in TUI
- API errors: HTTP status code handling
- Timeout: 120s allows for complex reasoning
- Malformed responses: JSON parsing errors caught

### 5. Session Logging System

#### Log Entry Format (JSONL)
```json
{
  "timestamp": "2025-11-15T01:30:00Z",
  "mode": "recon",
  "user": "user query text",
  "reply": "AI response text",
  "context_file": "/path/to/file",
  "context_hash": "sha256_hash"
}
```

#### Logging Benefits
1. **Audit trail**: Complete interaction history
2. **Reproducibility**: Context file + hash for verification
3. **Analytics**: Query patterns and mode usage
4. **Compliance**: Evidence of authorized activity
5. **Debugging**: Understand AI behavior over time

#### Log Viewing
```bash
pentai-log-view [target_name]
```
- Shows last 20 entries by default
- Truncates long responses (600 char limit)
- Includes context file information

### 6. TUI Architecture (Textual Framework)

#### Widget Hierarchy
```
PentAIApp
├── Static (header)
│   └── Status line (target, mode, history, file)
├── TextLog (chat_log)
│   └── Scrollable conversation history
└── Input (input)
    └── User prompt entry
```

#### Event Flow
```
User types in Input widget
    ↓
Presses Enter (Input.Submitted)
    ↓
on_input_submitted() handler
    ↓
_call_llm() builds context + calls API
    ↓
Response written to TextLog
    ↓
SessionLogger.log() persists entry
    ↓
Input widget cleared, focus restored
```

#### Key Bindings
- **F2**: `action_toggle_mode()` - Cycle through modes
- **Ctrl+H**: `action_toggle_history()` - Toggle shell history inclusion
- **Ctrl+C**: `action_quit()` - Exit application

### 7. Security Architecture

#### Trust Boundaries
```
┌─────────────────────────────────────────────┐
│  Trusted Zone (Local System)                │
│  - pentai.py execution                      │
│  - Config files                             │
│  - Session logs                             │
│  - Shell history                            │
└────────────┬────────────────────────────────┘
             │ HTTPS
             v
┌─────────────────────────────────────────────┐
│  Semi-Trusted Zone (LLM API)                │
│  - Receives: prompts + context              │
│  - Returns: text responses                  │
│  - Risk: Data retention, prompt injection   │
└─────────────────────────────────────────────┘
```

#### Security Mechanisms
1. **API Key Management**
   - Environment variable only (not in code/config)
   - Never logged or displayed
   - User responsibility for key rotation

2. **Command Execution Prevention**
   - AI never executes commands
   - Only suggests commands in text
   - User must manually execute

3. **Scope Enforcement**
   - System prompts emphasize authorized-only
   - Explicit scope in target configs
   - No technical enforcement (relies on AI compliance)

4. **Data Minimization**
   - File snippets limited to 4KB
   - Shell history limited to 10 commands
   - No full filesystem access

5. **Audit Trail**
   - All queries logged with timestamp
   - Context correlation via file hashes
   - Enables forensic analysis

#### Threat Model & Mitigations

| Threat | Mitigation |
|--------|-----------|
| API key exposure | Env vars, not hardcoded |
| Sensitive data in logs | User controls target configs |
| Prompt injection | System prompt constraints |
| Unintended command execution | No execution capability |
| Scope creep | Explicit scope definitions |
| Data exfiltration via API | User choice of LLM provider |

## Data Flow Diagrams

### Initialization Flow
```
main()
  ↓
Parse CLI arguments
  ↓
resolve_target_name()
  ↓
load_target() → TargetContext
  ↓
LLMClient.__init__() → Check API_KEY
  ↓
SessionLogger.__init__() → Open log file
  ↓
PentAIApp.__init__() → Initialize TUI
  ↓
app.run() → Start event loop
```

### Query Processing Flow
```
User Input (Enter pressed)
  ↓
on_input_submitted()
  ↓
_call_llm()
  ├─ Determine effective file path
  │  ├─ Explicit --file argument
  │  └─ auto_detect_context_file()
  │
  ├─ build_context_block()
  │  ├─ Format target info
  │  ├─ load_shell_history() if enabled
  │  └─ load_file_snippet() if file found
  │
  ├─ Construct prompt
  │  ├─ BASE_SYSTEM_PROMPT
  │  ├─ MODE_INSTRUCTIONS[mode]
  │  └─ Context + user input
  │
  ├─ LLMClient.chat()
  │  ├─ Build request payload
  │  ├─ POST to API
  │  └─ Parse response
  │
  └─ Return (reply, context_file, context_hash)
  ↓
Display in TextLog
  ↓
SessionLogger.log()
```

### Mode Switching Flow
```
F2 pressed
  ↓
action_toggle_mode()
  ↓
Calculate next mode (circular)
  ↓
Update self.mode
  ↓
Write mode change to chat log
  ↓
_update_header()
  ↓
Check if input matches previous mode's default
  ↓
If yes: Replace with new mode's default
  ↓
Set focus back to input
```

## Extension Points

### Adding a New Mode

**Step 1**: Define mode instructions
```python
NEWMODE_INSTRUCTIONS = """
Mode: New Mode.
Purpose: ...
Rules: ...
Output format: ...
"""
```

**Step 2**: Register the mode
```python
MODES = ["cmd", "chat", "recon", "loot", "report", "red", "newmode"]

MODE_INSTRUCTIONS = {
    # ... existing modes ...
    "newmode": NEWMODE_INSTRUCTIONS,
}

MODE_DEFAULT_PROMPTS = {
    # ... existing modes ...
    "newmode": "Default prompt for new mode...",
}
```

**Step 3**: Test
```bash
./pentai.py --mode newmode
```

### Adding a New Context Source

**Example**: Git repository analysis

```python
def load_git_context(limit: int = 10) -> Optional[str]:
    """Load recent git commits and diff stats."""
    try:
        result = subprocess.run(
            ["git", "log", f"-n{limit}", "--oneline", "--stat"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass
    return None

# Add to build_context_block()
if include_git:
    git_info = load_git_context()
    if git_info:
        parts.append(f"Git history:\n{git_info}")
```

### Custom LLM Backend

**Example**: Local Ollama integration

```python
class OllamaClient:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = os.environ.get("OLLAMA_MODEL", "llama2")
    
    def chat(self, messages: List[dict]) -> str:
        # Convert OpenAI format to Ollama format
        prompt = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in messages
        ])
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()["response"]
```

## Performance Considerations

### Bottlenecks
1. **LLM API latency**: 2-10 seconds typical
2. **File I/O**: Minimal (4KB snippets, 10 history lines)
3. **Context size**: Growing with large logs
4. **Network**: Depends on API endpoint location

### Optimizations
1. **Context caching**: Same file + same hash = cache response
2. **Streaming**: Use SSE for real-time token display
3. **Async I/O**: Non-blocking file reads
4. **History pruning**: Configurable limit

## Deployment Scenarios

### Scenario 1: Kali Linux VM
```bash
# Install on Kali
git clone https://github.com/user/pentai-tui.git
cd pentai-tui
./setup.sh

# Set API key in ~/.zshrc
echo 'export AI_API_KEY="sk-..."' >> ~/.zshrc
source ~/.zshrc

# Use during pentest
cd /pentest/target-project
echo "webapp-prod" > .pentai-target
pentai-init-target webapp-prod
ai-recon
```

### Scenario 2: Cloud Shell Environment
```bash
# Install dependencies
pip install --user textual requests

# Set API key (temporary session)
export AI_API_KEY="sk-..."

# Run without installation
python3 pentai.py --mode cmd
```

### Scenario 3: Docker Container
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY pentai.py .
ENTRYPOINT ["python3", "pentai.py"]
```

## Testing Strategy

### Unit Tests (Recommended)
- `test_context_gathering.py`: Shell history, file detection
- `test_target_config.py`: Config loading, resolution
- `test_session_logger.py`: JSONL writing, log viewing
- `test_llm_client.py`: Mock API responses

### Integration Tests
- `test_end_to_end.py`: Full TUI flow with mock LLM
- `test_mode_switching.py`: Mode transitions
- `test_context_injection.py`: Context in prompts

### Manual Testing Checklist
- [ ] All 6 modes render correctly
- [ ] F2 cycles through modes
- [ ] Ctrl+H toggles history
- [ ] File auto-detection works
- [ ] Target configs load/save
- [ ] Session logging persists
- [ ] Error handling graceful

## Conclusion

PentAI-TUI's architecture demonstrates:
- **Clean separation of concerns**: UI, logic, data, external services
- **Extensible design**: Easy to add modes, contexts, backends
- **Security-conscious**: Multiple layers of protection
- **User-centric**: Optimized for pentester workflows

The modular design allows for incremental enhancements without disrupting core functionality, making it a robust foundation for an AI-assisted penetration testing toolkit.
