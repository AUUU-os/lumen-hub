---
name: lumen-hub-dev
description: This skill should be used when the user asks to "add a module to LUMEN_HUB", "implement a new seed", "build a new module", "implement seed executor", "add feature to lumen hub", "new lumen module", or starts implementing any new component for the LUMEN_HUB project. Enforces OMEGA governance pipeline before writing any code.
version: 0.1.0
---

# LUMEN HUB Development Standard

Every new module or feature in LUMEN_HUB passes through a three-stage governance pipeline before any code is written. No exceptions.

```
AI_OS_ARCHITECT (L0-L6 analysis)
        ↓
LUMEN_MASTER_ARCHITECT (governance approval)
        ↓
Standard OMEGA (implementation)
```

---

## Stage 1 — AI_OS_ARCHITECT Analysis

Before proposing any code, analyze the module through 7 layers. Output each layer explicitly.

```
L0 – Clarity       → What exactly are we building? (1-2 sentences, no ambiguity)
L1 – Architecture  → Modules, boundaries, dependencies
L2 – Memory        → Where does state live? How does it persist?
L3 – Orchestration → How do modules communicate? (LIVE_BRIDGE? file? API?)
L4 – Execution     → How is it started/stopped? Entry point?
L5 – CI/CD         → Rollback strategy, snapshots, versioning
L6 – Observability → How do we see what's happening? Logs, metrics, health?
```

**Rules:**
- Never skip to code before completing L0-L6
- If any layer is unclear → ask SHAD before continuing
- Map dependencies to existing LUMEN_HUB modules (builder.py, runner.py, gateway.py)
- Flag cyclic risks and failure modes

---

## Stage 2 — LUMEN_MASTER_ARCHITECT Governance

After L0-L6, classify the change and output a governance decision.

**Input format:**
```json
{
  "change_request": "<what is being added/changed>",
  "affected_layers": ["<L0-L6 layers impacted>"],
  "modules_involved": ["<existing files touched>"],
  "diff_summary": "<what changes in the codebase>",
  "context": "LUMEN_HUB module"
}
```

**Classification:**
| Type | Criteria |
|------|----------|
| `PATCH` | No new deps, no layer crossing, isolated change |
| `MINOR` | New module in existing layer |
| `MAJOR` | Cross-layer, new public API, changes memory model |
| `BREAKING` | Kernel change, snapshot logic, security model |

**Output decision before writing any code:**
```json
{
  "change_type": "PATCH|MINOR|MAJOR|BREAKING",
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "snapshot_required": true/false,
  "decision": "APPROVED|CONDITIONAL|REJECTED",
  "conditions": ["<if CONDITIONAL — what must be met>"]
}
```

**Rules:**
- `CRITICAL` risk → automatic `REJECTED`, redesign required
- `MAJOR` → snapshot of current state before implementing
- `BREAKING` → full snapshot + rollback plan in writing
- `CONDITIONAL` → list conditions, get SHAD approval before continuing

---

## Stage 3 — Standard OMEGA Implementation

Only after `APPROVED` or `CONDITIONAL` (with conditions met) — write code to OMEGA standard.

**Stack:**
- Python 3.11+ with strict type hints (PEP 484)
- Async/await for all I/O
- Pydantic v2 for validation and schemas
- Return format: `{"status": "...", "data": {...}}`

**Structure per module:**
```python
# module_name.py
"""
LUMEN HUB — MODULE_NAME
One-line description.
"""
from pathlib import Path
from typing import Any
import asyncio

# Constants at top
# Typed functions
# No global mutable state
# Explicit error handling — never silent except
```

**Quality gates (non-negotiable):**
- Every public function has type hints
- Every module has a docstring
- Error paths return structured dicts, never raise unhandled
- No hardcoded paths — use `Path` constants
- Logging via `print(f"[MODULE_NAME] ...")` until proper logger added

**Test requirement:**
- At minimum: one happy path test + one error path test per function
- File: `tests/test_<module_name>.py`
- Run: `python -m pytest tests/test_<module_name>.py -v`

---

## LUMEN_HUB Module Map (current)

```
E:/LUMEN_HUB/
├── orchestrator/
│   ├── builder.py    ← MINOR to modify, MAJOR to change interface
│   ├── runner.py     ← MAJOR to modify (manages live processes)
│   └── gateway.py    ← MINOR to modify
├── lumen.py          ← CLI entry point — MAJOR to change
├── SEEDS/            ← append-only, never modify existing seeds
├── skills/           ← this skill lives here
└── omega_dashboard.html ← PATCH-level changes OK
```

**Next modules in queue (from SEEDS):**
- `orchestrator/seed_executor.py` — MINOR (new module, uses runner.py)
- `orchestrator/healer.py` — MAJOR (AI log analysis, cross-layer)
- `registry.json` + scanner — MINOR (read-only archaeology)

---

## Quick Checklist

Before writing first line of code:

- [ ] L0-L6 analysis complete and written out
- [ ] Governance JSON produced
- [ ] Decision is APPROVED (or CONDITIONAL with conditions met)
- [ ] MAJOR/BREAKING → snapshot taken
- [ ] Test file planned

---

## Additional Resources

- **`references/omega-standard.md`** — Full Standard OMEGA spec (stack, security, observability)
- **`references/architecture-layers.md`** — Detailed L0-L6 examples and failure modes
- **`references/governance-examples.md`** — Example governance JSONs for PATCH/MINOR/MAJOR/BREAKING

---

*The forest grows one module at a time. Each module knows its place. 🐺*
