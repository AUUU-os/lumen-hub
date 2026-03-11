#!/usr/bin/env python3
"""
LUMEN HUB — MCP Server
Exposes LUMEN_HUB capabilities as MCP tools for Claude Code.

Tools:
  - ollama_generate   : Run any prompt through local Ollama (zero Claude tokens)
  - list_seeds        : List all SEEDS blueprints
  - read_seed         : Read a SEED file content
  - create_seed       : Write a new SEED blueprint
  - hub_status        : Current state of LUMEN_HUB (apps, modules count, etc.)
  - list_apps         : List deployed apps via runner
  - read_file         : Read any file in LUMEN_HUB
  - write_file        : Write a file in LUMEN_HUB (safe path only)
  - run_lumen         : Run `lumen <command>` CLI

Usage:
  python lumen_mcp_server.py

Configure in .mcp.json:
  {
    "lumen-hub": {
      "command": "python",
      "args": ["E:/LUMEN_HUB/servers/lumen_mcp_server.py"]
    }
  }
"""

import json
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ─────────────────────────────────────────────────────────────────
HUB_ROOT = Path("E:/LUMEN_HUB")
SEEDS_DIR = HUB_ROOT / "SEEDS"
DATA_DIR = HUB_ROOT / "data"
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen3:8b"
# ─────────────────────────────────────────────────────────────────

mcp = FastMCP("lumen-hub")


# ─── OLLAMA ───────────────────────────────────────────────────────

@mcp.tool()
def ollama_generate(text: str, model: str = DEFAULT_MODEL, system: str = "") -> str:
    """
    Run a task through local Ollama. Zero Claude token cost.
    Use this for heavy generation tasks: naming, brainstorming, writing code drafts.

    Args:
        text: The text/task to send to Ollama
        model: Ollama model (default: qwen3:8b). Options: phi4, deepseek-r1:8b, qwen2.5-coder:7b
        system: Optional system prompt for Ollama
    """
    payload = {"model": model, "prompt": text, "stream": False}
    if system:
        payload["system"] = system

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result.get("response", "")
    except Exception as e:
        return f"ERROR: Ollama unavailable — {e}"


# ─── SEEDS ────────────────────────────────────────────────────────

@mcp.tool()
def list_seeds() -> str:
    """List all SEED blueprints in LUMEN_HUB/SEEDS/."""
    seeds = sorted(SEEDS_DIR.glob("SEED_*.md"))
    if not seeds:
        return "No seeds found."
    lines = []
    for s in seeds:
        first_line = s.read_text(encoding="utf-8").split("\n")[0].lstrip("# ")
        lines.append(f"{s.stem}: {first_line}")
    return "\n".join(lines)


@mcp.tool()
def read_seed(name: str) -> str:
    """
    Read a SEED blueprint file.

    Args:
        name: Filename like SEED_001_AI_NATIVE_PAAS.md or partial match like SEED_001
    """
    # exact match
    exact = SEEDS_DIR / name
    if exact.exists():
        return exact.read_text(encoding="utf-8")

    # partial match
    matches = list(SEEDS_DIR.glob(f"*{name}*"))
    if not matches:
        return f"ERROR: No seed matching '{name}'"
    return matches[0].read_text(encoding="utf-8")


@mcp.tool()
def create_seed(filename: str, content: str) -> str:
    """
    Write a new SEED blueprint to LUMEN_HUB/SEEDS/.

    Args:
        filename: e.g. SEED_008_MY_NEW_IDEA.md
        content: Full markdown content of the seed
    """
    if not filename.endswith(".md"):
        filename += ".md"
    path = SEEDS_DIR / filename
    if path.exists():
        return f"ERROR: {filename} already exists. Use a different name."
    path.write_text(content, encoding="utf-8")
    return f"Created: {path}"


# ─── HUB ──────────────────────────────────────────────────────────

@mcp.tool()
def hub_status() -> str:
    """Get current LUMEN_HUB status: apps, seeds, git hash."""
    seeds_count = len(list(SEEDS_DIR.glob("SEED_*.md")))

    state_file = DATA_DIR / "runner_state.json"
    apps_running = 0
    apps_list = []
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
            apps = state.get("apps", {})
            apps_running = sum(1 for a in apps.values() if a.get("status") == "running")
            apps_list = list(apps.keys())
        except Exception:
            pass

    git_hash = "unknown"
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=HUB_ROOT, capture_output=True, text=True, timeout=5
        )
        git_hash = result.stdout.strip()
    except Exception:
        pass

    return json.dumps({
        "hub_root": str(HUB_ROOT),
        "seeds": seeds_count,
        "apps_running": apps_running,
        "apps": apps_list,
        "git_hash": git_hash,
        "ollama_model": DEFAULT_MODEL
    }, indent=2)


@mcp.tool()
def list_apps() -> str:
    """List all apps known to the runner with their status and port."""
    state_file = DATA_DIR / "runner_state.json"
    if not state_file.exists():
        return "No runner state found. No apps deployed yet."
    state = json.loads(state_file.read_text(encoding="utf-8"))
    apps = state.get("apps", {})
    if not apps:
        return "No apps deployed."
    lines = []
    for name, info in apps.items():
        status = info.get("status", "unknown")
        port = info.get("port", "?")
        lines.append(f"{name}: {status} (port {port})")
    return "\n".join(lines)


# ─── FILES ────────────────────────────────────────────────────────

@mcp.tool()
def read_file(path: str) -> str:
    """
    Read any file inside LUMEN_HUB.

    Args:
        path: Relative to HUB_ROOT, e.g. 'M-AI-SELF/CHANGELOG.md' or 'SEEDS/SEED_001_AI_NATIVE_PAAS.md'
    """
    target = HUB_ROOT / path
    if not target.resolve().is_relative_to(HUB_ROOT.resolve()):
        return "ERROR: Path outside LUMEN_HUB not allowed."
    if not target.exists():
        return f"ERROR: {path} not found."
    return target.read_text(encoding="utf-8")


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    Write a file inside LUMEN_HUB.
    Safe paths only: M-AI-SELF/, SEEDS/, docs/, data/.

    Args:
        path: Relative to HUB_ROOT
        content: File content
    """
    safe_prefixes = ["M-AI-SELF/", "SEEDS/", "docs/", "data/", "scripts/"]
    if not any(path.startswith(p) for p in safe_prefixes):
        return f"ERROR: Only {safe_prefixes} paths allowed for safety."

    target = HUB_ROOT / path
    if not target.resolve().is_relative_to(HUB_ROOT.resolve()):
        return "ERROR: Path traversal not allowed."

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Written: {target}"


# ─── CLI ──────────────────────────────────────────────────────────

@mcp.tool()
def run_lumen(command: str) -> str:
    """
    Run a lumen CLI command: status, monitor, deploy <app>, start <app>, stop <app>.

    Args:
        command: e.g. 'status', 'monitor', 'deploy myapp'
    """
    allowed = ["status", "monitor", "deploy", "start", "stop", "gateway"]
    cmd_parts = command.strip().split()
    if not cmd_parts or cmd_parts[0] not in allowed:
        return f"ERROR: Allowed commands: {allowed}"

    try:
        result = subprocess.run(
            [sys.executable, str(HUB_ROOT / "lumen.py")] + cmd_parts,
            cwd=HUB_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"ERROR: {e}"


# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
