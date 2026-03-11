# Standard OMEGA — Full Specification

Source: `E:/SHAD/GROTA_LUMENA/Meta-Warstw.txt` (Meta-Warstwa LUMENA)

## Core Stack

```
Language:    Python 3.11+ (strict typing, PEP 484/257)
Framework:   FastAPI + Pydantic v2 + SQLAlchemy 2.0 (Async)
State:       Idempotent, Cached (Redis optional), Rate-limited
Local LLM:   Ollama (zero token cost)
Vector DB:   ChromaDB (semantic search)
```

## Security

- Zero-Trust Model: never assume internal calls are safe
- API Key Auth on all endpoints
- Full input sanitization via Pydantic validators
- No secrets in code — use `.env` + `vault.py` pattern
- Audit logging for all state changes

## Observability

- Structured logging: `[MODULE_NAME] operation: result`
- Health endpoint pattern: `{"status": "ok"|"degraded"|"down", "details": {}}`
- Key metrics to track: latency, error_rate, restart_count
- OpenTelemetry-ready (add instrumentation hooks)

## DevOps

- Docker-ready: every module runs in isolation
- Graceful shutdown: handle SIGTERM, flush state
- Auto-restart capable (runner.py handles this)
- Config via environment variables, not hardcoded

## Code Quality

- 90% pytest coverage target
- Ruff linting (PEP8 + type checking)
- Clean Architecture: separation of concerns
- SOLID principles: each module has one reason to change
- DRY: extract repeated patterns into shared utils

## Response Format (universal)

```python
# Success
{"status": "ok", "data": {...}, "module": "module_name"}

# Error
{"status": "error", "error": "description", "code": "ERROR_CODE", "module": "module_name"}

# Partial
{"status": "partial", "data": {...}, "warnings": [...], "module": "module_name"}
```

## File Naming

```
module_name.py          # snake_case modules
TestModuleName          # PascalCase test classes
test_module_name.py     # test files
MODULE_NAME constant    # UPPER_SNAKE for constants
```

## LUMEN_HUB Specific

- All paths via `Path` — never string concatenation
- Data dir: `E:/LUMEN_HUB/data/`
- Logs dir: `E:/LUMEN_HUB/data/logs/<module>/`
- State files: `E:/LUMEN_HUB/data/<module>_state.json`
- UTF-8 everywhere: `open(f, encoding='utf-8')`
