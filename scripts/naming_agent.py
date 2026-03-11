#!/usr/bin/env python3
"""
LUMEN HUB — NAMING AGENT
Generates English names + project vision for the LUMEN_HUB ecosystem.
Feed it context, get back a coherent naming system.

Usage:
    python naming_agent.py                    # Ollama (default, free)
    python naming_agent.py --cloud            # Claude API (needs ANTHROPIC_API_KEY)
    python naming_agent.py --model qwen3:8b   # specific Ollama model
"""
import os
import sys
import urllib.request
import urllib.error
import json

# ─────────────────────────────────────────────────────────────────
# PROJECT CONTEXT — what we're naming
# ─────────────────────────────────────────────────────────────────

CONTEXT = """
We are building a local platform called LUMEN_HUB. It needs a coherent English naming system.

## What it IS (the philosophy)
- A living forest/tree ecosystem — not just a PaaS
- Every module is a "tree" with genealogy (parent, children, mutations)
- The hub IS the forest — not a tool to manage the forest
- Modules wait as embryos before being deployed as living processes
- There's a memory system (the forest remembers its history)
- Two builders: SHAD (human, the one who plants) + AI (the one who grows)

## Current components that need names
1. The MODULE REGISTRY — central database of 8237 modules from 7 locations (seeds become this)
2. The GENEALOGY SYSTEM — tracks SPAWNED_FROM / EVOLVED_INTO / INFECTED_BY relationships between modules
3. The BUILDER+RUNNER — where modules are built and launched (orchestrator/)
4. The WORKSPACE — identity, config, notes, changelogs, snapshots (currently M-AI-SELF/)
5. The DASHBOARD — mission control overview (currently omega_dashboard.html)
6. The BLUEPRINT LAB — specs/ideas waiting to be implemented (currently SEEDS/)

## Concepts already locked in (keep these)
- SEEDS/ — seeds waiting to grow (stays, it's perfect)
- WORLD_FORGE — from blueprints, the "forge where worlds are born" (fits builder)
- ANCESTRAL_CODEX — genealogy system (from blueprints, fits perfectly)
- EMBRYO_STORE — module nursery/registry (SHAD's idea, keep it)

## The metaphor we're running with
Forest / Tree / Genealogy / Living system
- Seeds -> Embryos -> Living Trees -> Forest
- Trees have roots, trunk, branches, leaves
- The forest has memory (what grew here, what died, what evolved)

## What we want
- 5-6 English names for the core directories/systems
- Short (1-2 words), technical but evocative
- Consistent — they feel like they belong to the same world
- A 2-3 sentence PROJECT VISION statement
- A one-line tagline

## Constraints
- NO generic names (no "core", "utils", "lib", "api" alone)
- Must feel like a real platform with its own identity
- English only
- Should work as directory names (no spaces, CamelCase or UPPER_SNAKE ok)
"""

SYSTEM_PROMPT = """You are a technical architect and brand designer.
You create naming systems for software platforms that are both technically precise
and have a strong identity. You think in metaphors and make them consistent.
Be creative but concrete. Output structured, copy-pasteable results."""

# ─────────────────────────────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────────────────────────────

NAMING_PROMPT = f"""{CONTEXT}

Generate:

1. **NAMING SYSTEM** — For each of the 6 components above, give:
   - Your recommended name
   - 1-line explanation of why it fits
   - Alternative (in case the first feels off)

2. **PROJECT VISION** — 2-3 sentences describing what LUMEN_HUB IS
   (not what it does — what it IS, philosophically and technically)

3. **TAGLINE** — One punchy line. Max 10 words.

4. **FULL DIRECTORY TREE** — Show how it looks as a file structure with your names

5. **BONUS** — If you see a name we haven't thought of that would make
   the system MORE coherent, propose it.

Be bold. This isn't a corporate product — it's a living ecosystem."""

# ─────────────────────────────────────────────────────────────────
# BACKENDS
# ─────────────────────────────────────────────────────────────────

def run_ollama(model: str) -> None:
    """Stream response from local Ollama."""
    print(f"[NAMING_AGENT] Using Ollama -> {model}\n")

    payload = json.dumps({
        "model": model,
        "system": SYSTEM_PROMPT,
        "prompt": NAMING_PROMPT,
        "stream": True
    }).encode()

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            for line in resp:
                chunk = json.loads(line.decode())
                token = chunk.get("response", "")
                print(token, end="", flush=True)
                if chunk.get("done"):
                    break
    except urllib.error.URLError:
        print("[NAMING_AGENT] ERROR: Ollama not running. Start with: ollama serve")


def run_claude(model: str = "claude-opus-4-6") -> None:
    """Stream response from Claude API."""
    try:
        import anthropic
    except ImportError:
        print("[NAMING_AGENT] ERROR: pip install anthropic")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[NAMING_AGENT] ERROR: ANTHROPIC_API_KEY not set")
        return

    client = anthropic.Anthropic(api_key=api_key)
    print(f"[NAMING_AGENT] Using Claude API -> {model}\n")

    with client.messages.stream(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": NAMING_PROMPT}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

def main() -> None:
    use_cloud = "--cloud" in sys.argv
    model_arg = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == "--model"), None)

    print("\n[*] LUMEN HUB -- NAMING AGENT")
    print("=" * 60)
    print("Generating naming system + vision...\n")

    if use_cloud:
        run_claude()
    else:
        model = model_arg or "qwen3:8b"
        run_ollama(model)

    print("\n\n" + "=" * 60)
    print("[*] Done. Pick what resonates.")


if __name__ == "__main__":
    main()
