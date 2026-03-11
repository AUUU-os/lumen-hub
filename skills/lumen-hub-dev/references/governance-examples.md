# Governance Examples — LUMEN_MASTER_ARCHITECT

## PATCH Example — small fix to gateway.py

```json
{
  "change_request": "Fix 404 response to include JSON format instead of plain HTML",
  "affected_layers": ["L4"],
  "modules_involved": ["orchestrator/gateway.py"],
  "diff_summary": "Change _send_html to _send_json in 404 handler",
  "context": "LUMEN_HUB module"
}
```

**Decision:**
```json
{
  "change_type": "PATCH",
  "risk_level": "LOW",
  "snapshot_required": false,
  "decision": "APPROVED",
  "conditions": []
}
```

---

## MINOR Example — new seed_executor.py module

```json
{
  "change_request": "Add seed_executor.py — reads SEED .md files and calls LUMEN to implement them",
  "affected_layers": ["L0", "L1", "L3"],
  "modules_involved": ["orchestrator/runner.py", "SEEDS/"],
  "diff_summary": "New file orchestrator/seed_executor.py, new CLI command in lumen.py",
  "context": "LUMEN_HUB module"
}
```

**Decision:**
```json
{
  "change_type": "MINOR",
  "risk_level": "MEDIUM",
  "snapshot_required": false,
  "decision": "CONDITIONAL",
  "conditions": [
    "seed_executor must not modify existing SEED files — read-only",
    "Must handle LLM unavailable gracefully",
    "Add tests/test_seed_executor.py with mock LLM"
  ]
}
```

---

## MAJOR Example — live SHARED_STATE.json integration in dashboard

```json
{
  "change_request": "Connect omega_dashboard.html to live LIVE_BRIDGE/SHARED_STATE.json via polling API",
  "affected_layers": ["L1", "L2", "L3", "L6"],
  "modules_involved": ["orchestrator/gateway.py", "omega_dashboard.html", "LIVE_BRIDGE/"],
  "diff_summary": "New /api/state endpoint in gateway, JS polling in dashboard, reads external file",
  "context": "LUMEN_HUB module"
}
```

**Decision:**
```json
{
  "change_type": "MAJOR",
  "risk_level": "MEDIUM",
  "snapshot_required": true,
  "decision": "APPROVED",
  "conditions": []
}
```
→ Take git snapshot before implementing.

---

## BREAKING Example — change runner.py state format

```json
{
  "change_request": "Migrate runner_state.json from flat dict to nested schema with history",
  "affected_layers": ["L1", "L2", "L4", "L5"],
  "modules_involved": ["orchestrator/runner.py", "orchestrator/gateway.py", "data/runner_state.json"],
  "diff_summary": "State schema change — all consumers of runner_state.json break",
  "context": "LUMEN_HUB module"
}
```

**Decision:**
```json
{
  "change_type": "BREAKING",
  "risk_level": "HIGH",
  "snapshot_required": true,
  "rollback_complexity": "MEDIUM",
  "decision": "CONDITIONAL",
  "conditions": [
    "Write migration script: migrate_state_v1_to_v2.py",
    "Add backward-compat reader for old format",
    "Git tag v1.0 before migration",
    "Update gateway.py simultaneously"
  ]
}
```
