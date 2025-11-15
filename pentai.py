#!/usr/bin/env python3
"""
PentAI – TUI AI helper for pentesting, entirely in the terminal.

Modes:
  - cmd    : Command & error assistant
  - chat   : General pentest chat
  - recon  : Recon/enumeration planner from logs + history
  - loot   : Highlight interesting artefacts (creds, tokens, endpoints) in logs
  - report : Summarise findings and draft structured notes
  - red    : Red team / attack chain planner (authorised environments only)

Context:
  - Recent shell history (zsh)
  - Optional file snippet (nmap/Jok3r/logs/etc.)

Target config:
  - Per-target JSON configs under:
      $PENTAI_CONFIG_DIR or ~/.config/pentai/targets/<name>.json
    with fields: name, scope, notes, loot_paths

Session persistence:
  - Logs each Q/A to a per-target JSONL file under:
      $PENTAI_DATA_DIR or ~/.local/share/pentai/<target>.jsonl
    with context_file path and SHA-256 hash of the first chunk of that file.

CLI:
  - Default: run TUI
  - --init-target NAME  : create/update a target config then exit
  - --view-logs         : view recent log entries then exit
"""

import os
import json
import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from datetime import datetime

import requests

from textual.app import App, ComposeResult
from textual.widgets import TextLog, Input, Static


# =========================
#  TARGET / CONFIG / DATA DIRS
# =========================

@dataclass
class TargetContext:
    name: str
    scope: str
    notes: str
    loot_paths: List[str]


def get_config_dir() -> Path:
    base = os.environ.get("PENTAI_CONFIG_DIR")
    if base:
        return Path(base).expanduser()
    return Path.home() / ".config" / "pentai"


def get_data_dir() -> Path:
    base = os.environ.get("PENTAI_DATA_DIR")
    if base:
        return Path(base).expanduser()
    return Path.home() / ".local" / "share" / "pentai"


def resolve_target_name(explicit: Optional[str] = None) -> str:
    """Determine target name: explicit > env > .pentai-target > 'default'."""
    if explicit:
        return explicit

    env_name = os.environ.get("PENTAI_TARGET_NAME")
    if env_name:
        return env_name

    tfile = Path.cwd() / ".pentai-target"
    if tfile.exists():
        try:
            txt = tfile.read_text(encoding="utf-8").strip()
            if txt:
                return txt
        except OSError:
            pass

    return "default"


def load_target(name_override: Optional[str] = None) -> TargetContext:
    """Load TargetContext from config file if present, else from env."""
    name = resolve_target_name(name_override)
    cfg_dir = get_config_dir() / "targets"
    cfg_file = cfg_dir / f"{name}.json"

    scope = ""
    notes = ""
    loot_paths: List[str] = []

    if cfg_file.exists():
        try:
            data = json.loads(cfg_file.read_text(encoding="utf-8"))
            scope = data.get("scope", "")
            notes = data.get("notes", "")
            lp = data.get("loot_paths", [])
            if isinstance(lp, list):
                loot_paths = [str(x) for x in lp]
        except Exception:
            pass

    if not scope:
        scope = os.environ.get("PENTAI_SCOPE", "")
    if not notes:
        notes = os.environ.get("PENTAI_NOTES", "")

    return TargetContext(name=name, scope=scope, notes=notes, loot_paths=loot_paths)


def init_target_config(name: str, force: bool = False) -> Path:
    """Create or overwrite a per-target JSON config file."""
    cfg_dir = get_config_dir() / "targets"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    cfg_file = cfg_dir / f"{name}.json"

    if cfg_file.exists() and not force:
        raise FileExistsError(f"Target config already exists: {cfg_file}")

    data = {
        "name": name,
        "scope": "Describe scope here (IPs, domains, rules of engagement, etc.)",
        "notes": "Initial notes.",
        "loot_paths": [],
    }
    cfg_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return cfg_file


# =========================
#  CONTEXT SOURCES
# =========================

def load_shell_history(limit: int = 10) -> List[str]:
    """Load last N commands from zsh history."""
    hist_file = Path.home() / ".zsh_history"
    if not hist_file.exists():
        return []
    lines = hist_file.read_text(errors="ignore").splitlines()
    cmds: List[str] = []
    for line in lines[-limit:]:
        # zsh format can be ": 1700000000:0;command"
        if ";" in line:
            cmds.append(line.split(";", 1)[1])
        else:
            cmds.append(line)
    return cmds


def load_file_snippet(path: Path, max_bytes: int = 4096) -> Optional[str]:
    if not path.exists():
        return None
    data = path.read_bytes()[:max_bytes]
    return data.decode(errors="ignore")


def auto_detect_context_file() -> Optional[Path]:
    """
    Try to auto-detect a useful log / output file near CWD.

    Prioritises:
      - ./nmap, ./logs, ./output
      - *.nmap, *.gnmap, *.xml, *.log, *.txt
    This should catch typical nmap/Jok3r outputs if you run PentAI from the project dir.
    """
    cwd = Path.cwd()

    env_file = os.environ.get("PENTAI_FILE_CONTEXT")
    if env_file:
        p = Path(env_file).expanduser()
        if p.exists():
            return p

    search_dirs = [cwd, cwd / "nmap", cwd / "logs", cwd / "output"]
    candidates: List[Path] = []
    exts = (".nmap", ".gnmap", ".xml", ".log", ".txt")

    for d in search_dirs:
        if d.exists() and d.is_dir():
            for ext in exts:
                candidates.extend(d.glob(f"*{ext}"))

    if not candidates:
        return None

    candidates = [c for c in candidates if c.is_file()]
    if not candidates:
        return None

    return max(candidates, key=lambda p: p.stat().st_mtime)


def build_context_block(
    target: Optional[TargetContext],
    include_history: bool,
    file_path: Optional[Path],
) -> str:
    parts: List[str] = []

    if target:
        parts.append(
            f"Target name: {target.name}\n"
            f"Scope:\n{target.scope}\n\n"
            f"Notes:\n{target.notes}"
        )

    if include_history:
        hist = load_shell_history(limit=10)
        if hist:
            parts.append("Recent shell commands:\n" + "\n".join(hist))

    if file_path:
        snippet = load_file_snippet(file_path)
        if snippet:
            parts.append(f"File snippet from {file_path}:\n{snippet}")

    if not parts:
        return "No extra context provided."

    return "\n\n--- CONTEXT SEPARATOR ---\n\n".join(parts)


def file_sha256(path: Path, max_bytes: int = 65536) -> Optional[str]:
    """SHA-256 of the first max_bytes of a file (for log correlation)."""
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        chunk = f.read(max_bytes)
        if chunk:
            h.update(chunk)
    return h.hexdigest()


# =========================
#  PROMPTS / MODES
# =========================

BASE_SYSTEM_PROMPT = """
You are a concise technical assistant integrated into a terminal-based penetration testing toolkit.
You only operate on authorised targets. You never provide guidance for illegal or out-of-scope activity.

General rules:
- Prefer short, precise answers with concrete commands and flags.
- When suggesting commands, explain what each part does.
- Never execute commands yourself; only suggest them.
- When something may be destructive, clearly flag it as such.
"""

CHAT_INSTRUCTIONS = """
Mode: General Chat.
User may ask about pentest methodology, tools, configurations, exploit chains, or system internals.
Provide clear steps, example commands, and what to look for in the output.
"""

CMD_INSTRUCTIONS = """
Mode: Command & Error Assistant.
If the user provides a command:
- Explain exactly what it does, parameter by parameter.
- Point out potential risks and safer alternatives.

If the user provides errors or logs:
- Identify likely root causes.
- Suggest specific commands to diagnose or fix the issue.

Always show suggested commands inside fenced code blocks, one command per block.
"""

RECON_INSTRUCTIONS = """
Mode: Recon Planner.
Using context (logs, nmap output, history), infer current recon/enumeration status.

Return:
- Phase 1: What has likely been done so far.
- Phase 2: Recommended next recon/enumeration steps with specific commands.
- Phase 3: Deeper service-specific enumeration (http/smb/rdp/etc.) with rationale.

Keep commands safe and clearly explain why each step is useful.
"""

LOOT_INSTRUCTIONS = """
Mode: Loot & Artefact Finder.
From the provided context/logs:
- Highlight possible credentials, hashes, API keys, tokens, secrets, or interesting endpoints.
- Summarise where each artefact came from and why it matters.
- Suggest follow-up actions that remain within authorised pentest scope (e.g. password spraying, verifying access).

Format:
- Short summary.
- Bullet list of artefacts (if any).
- Recommended next steps.
"""

REPORT_INSTRUCTIONS = """
Mode: Report / Notes.
Based on context (scope, history, logs):
- Summarise key findings, interesting hosts/services, and notable issues.
- Group items into categories like: Information Gathering, Vulnerabilities, Misconfigurations, Credentials/Secrets, Next Steps.
- Produce concise, copy-pasteable notes that could go into a pentest report.

Avoid speculation; if something is uncertain, say so.
"""

REDTEAM_INSTRUCTIONS = """
Mode: Red Team / Attack Chain Planner.
Goal:
- Given the current context (scope, logs, history), propose realistic multi-step attack chains within the authorised environment.
- Combine recon, initial access, privilege escalation, lateral movement, and impact, with emphasis on stealth and OPSEC.

Rules:
- Operate strictly within the defined scope and rules of engagement.
- Do not recommend irreversible damage (e.g. wiping systems, crypto-ransomware, data destruction).
- Prefer controllable proof-of-concept techniques that demonstrate impact without harming availability or integrity.

Output format:
- High-level attack path overview (ordered steps).
- For each step: objective, example tools/commands, and evidence to collect.
- Optional: how a blue team might detect that step (logs, alerts, artefacts).
"""

MODE_INSTRUCTIONS = {
    "chat": CHAT_INSTRUCTIONS,
    "cmd": CMD_INSTRUCTIONS,
    "recon": RECON_INSTRUCTIONS,
    "loot": LOOT_INSTRUCTIONS,
    "report": REPORT_INSTRUCTIONS,
    "red": REDTEAM_INSTRUCTIONS,
}

MODES = ["cmd", "chat", "recon", "loot", "report", "red"]

MODE_DEFAULT_PROMPTS = {
    "cmd": (
        "Paste a command or error output here and get an explanation, risks, and "
        "specific suggestions to improve or fix it.\n\n"
    ),
    "chat": "",
    "recon": (
        "Using the current logs and shell history, summarise recon/enumeration done so far "
        "and propose concrete next steps with commands.\n\n"
    ),
    "loot": (
        "From the context/logs, find any potentially sensitive artefacts: credentials, tokens, "
        "API keys, secrets, interesting endpoints or paths. Summarise and suggest next steps.\n\n"
    ),
    "report": (
        "Draft concise pentest notes from this context: scope, key findings, interesting services, "
        "and recommended next steps, grouped into logical sections.\n\n"
    ),
    "red": (
        "Using the current scope, logs, and recon, propose a realistic red team attack chain within "
        "authorised bounds: initial access, privilege escalation, lateral movement, and impact. "
        "For each step, include objective, example commands/tools, and evidence to collect. "
        "Also mention how defenders might detect each step.\n\n"
    ),
}


# =========================
#  LLM CLIENT
# =========================

class LLMClient:
    def __init__(self) -> None:
        self.api_key = os.environ.get("AI_API_KEY")
        self.base_url = os.environ.get("AI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.environ.get("AI_MODEL", "gpt-5.1-mini")

        if not self.api_key:
            raise RuntimeError("AI_API_KEY not set in environment")

    def chat(self, messages: List[dict]) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


# =========================
#  SESSION LOGGER & LOG VIEW
# =========================

class SessionLogger:
    """
    Simple JSONL logger:
      <data_dir>/<target_name>.jsonl
    Each entry:
      {timestamp, mode, user, reply, context_file, context_hash}
    """

    def __init__(self, target_name: str) -> None:
        base_dir = get_data_dir()
        base_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = base_dir / f"{target_name}.jsonl"

    def log(
        self,
        mode: str,
        user_text: str,
        reply: str,
        context_file: Optional[str],
        context_hash: Optional[str],
    ) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "mode": mode,
            "user": user_text,
            "reply": reply,
            "context_file": context_file,
            "context_hash": context_hash,
        }
        try:
            with self.log_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass


def view_logs(target_name: str, last: int = 10) -> None:
    """Pretty-print the last N log entries to stdout."""
    log_file = get_data_dir() / f"{target_name}.jsonl"
    if not log_file.exists():
        print(f"No logs for target '{target_name}' at {log_file}")
        return

    lines = log_file.read_text(encoding="utf-8").splitlines()
    subset = lines[-last:]

    for line in subset:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        ts = entry.get("timestamp", "?")
        mode = entry.get("mode", "?")
        user = entry.get("user", "").strip()
        reply = entry.get("reply", "").strip()
        cfile = entry.get("context_file")
        chash = entry.get("context_hash")

        print(f"[{ts}] [{mode}] context_file={cfile} sha256={chash}")
        print("  Q:", user)
        max_len = 600
        if len(reply) > max_len:
            print("  A:", reply[:max_len], "...")
        else:
            print("  A:", reply)
        print()


# =========================
#  TUI APP
# =========================

class PentAIApp(App):
    """Simple vertical layout: header, chat log, input line."""

    BINDINGS = [
        ("f2", "toggle_mode", "Cycle modes"),
        ("ctrl+h", "toggle_history", "Toggle shell history"),
        ("ctrl+c", "quit", "Quit"),
    ]

    def __init__(
        self,
        mode: str,
        file_path: Optional[str],
        prefill: Optional[str],
        target_name: str,
    ) -> None:
        super().__init__()

        if mode not in MODES:
            mode = "cmd"
        self.mode = mode
        self.file_path = Path(file_path).expanduser() if file_path else None
        self.explicit_prefill = prefill

        self.target = load_target(target_name)
        self.client = LLMClient()
        self.logger = SessionLogger(self.target.name)

        self.include_history = True

        self.header: Static
        self.chat_log: TextLog
        self.input: Input

    def compose(self) -> ComposeResult:
        self.header = Static("")
        self.chat_log = TextLog(highlight=True, wrap=True)
        self.input = Input(placeholder="Type prompt and press Enter…")
        yield self.header
        yield self.chat_log
        yield self.input

    def on_mount(self) -> None:
        self._update_header()
        self.chat_log.write("PentAI TUI started.")
        self.chat_log.write(
            "Modes: cmd/chat/recon/loot/report/red | F2: cycle mode | Ctrl+H: toggle history"
        )

        if self.explicit_prefill:
            self.input.value = self.explicit_prefill
        else:
            self.input.value = MODE_DEFAULT_PROMPTS.get(self.mode, "")

        self.set_focus(self.input)

    # ----- Actions -----

    def action_toggle_mode(self) -> None:
        prev_mode = self.mode
        idx = MODES.index(self.mode)
        self.mode = MODES[(idx + 1) % len(MODES)]
        self.chat_log.write(f"[system] Mode switched to: {self.mode}")
        self._update_header()

        prev_default = MODE_DEFAULT_PROMPTS.get(prev_mode, "")
        if (not self.input.value.strip()) or (self.input.value == prev_default):
            self.input.value = MODE_DEFAULT_PROMPTS.get(self.mode, "")
        self.set_focus(self.input)

    def action_toggle_history(self) -> None:
        self.include_history = not self.include_history
        status = "on" if self.include_history else "off"
        self.chat_log.write(f"[system] Shell history context: {status}")
        self._update_header()

    # ----- Helpers -----

    def _update_header(self) -> None:
        hist_status = "on" if self.include_history else "off"
        if self.file_path:
            file_info = f" | File: {self.file_path}"
        else:
            file_info = " | File: auto-detect"
        self.header.update(
            f"PentAI | Target: {self.target.name} | Mode: {self.mode} "
            f"| Shell history: {hist_status}{file_info} "
            "| F2: mode, Ctrl+H: history, Ctrl+C: quit"
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_text = event.value.strip()
        self.input.value = ""
        if not user_text:
            return

        self.chat_log.write(f"[you] {user_text}")
        self.chat_log.write("[ai] thinking…")

        try:
            reply, context_file, context_hash = self._call_llm(user_text)
        except Exception as e:
            reply = f"Error contacting model: {e}"
            context_file = None
            context_hash = None

        self.chat_log.write(f"[ai] {reply}")
        self.logger.log(self.mode, user_text, reply, context_file, context_hash)

    def _call_llm(self, user_text: str) -> tuple[str, Optional[str], Optional[str]]:
        if self.file_path and self.file_path.exists():
            effective_file: Optional[Path] = self.file_path
        else:
            effective_file = auto_detect_context_file()

        context_block = build_context_block(
            target=self.target,
            include_history=self.include_history,
            file_path=effective_file,
        )

        mode_instr = MODE_INSTRUCTIONS.get(self.mode, "")
        system_prompt = BASE_SYSTEM_PROMPT + mode_instr

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"{context_block}\n\nUser input:\n{user_text}",
            },
        ]
        reply = self.client.chat(messages)

        context_file = str(effective_file) if effective_file else None
        context_hash = file_sha256(effective_file) if effective_file else None

        return reply, context_file, context_hash


# =========================
#  CLI ENTRYPOINT
# =========================

def main() -> None:
    parser = argparse.ArgumentParser(description="PentAI TUI helper.")
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="cmd",
        help=f"Initial mode ({', '.join(MODES)}). Default: cmd",
    )
    parser.add_argument(
        "--file",
        help="File to include in context (e.g., nmap or Jok3r log). "
             "If not set, PentAI tries to auto-detect.",
    )
    parser.add_argument(
        "--prefill",
        help="Initial text to prefill in the input box (e.g., last command).",
    )

    parser.add_argument(
        "--target",
        help="Target name override (else env PENTAI_TARGET_NAME, .pentai-target, or 'default').",
    )
    parser.add_argument(
        "--view-logs",
        action="store_true",
        help="View recent log entries for the target instead of starting the TUI.",
    )
    parser.add_argument(
        "--last",
        type=int,
        default=10,
        help="When using --view-logs, number of recent entries to show (default: 10).",
    )
    parser.add_argument(
        "--init-target",
        help="Create a target config with this name and exit.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="With --init-target, overwrite existing target config.",
    )

    args = parser.parse_args()

    if args.init_target:
        try:
            cfg_path = init_target_config(args.init_target, force=args.force)
            print(f"Created/updated target config at: {cfg_path}")
        except FileExistsError as e:
            print(str(e))
        return

    target_name = resolve_target_name(args.target)

    if args.view_logs:
        view_logs(target_name, last=args.last)
        return

    app = PentAIApp(
        mode=args.mode,
        file_path=args.file,
        prefill=args.prefill,
        target_name=target_name,
    )
    app.run()


if __name__ == "__main__":
    main()
