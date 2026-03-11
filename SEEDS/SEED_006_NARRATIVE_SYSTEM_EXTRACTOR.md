# SEED_006 — Narrative System Extractor

**Status:** idea
**Złożoność:** średnia
**Potencjał:** automatyczna ekstrakcja DNA z sesji → BACKBONE

---

## Wizja

SHAD buduje OMEGA przez godziny rozmów. W tych rozmowach rodzą się:
- Blueprinty
- Wzorce kodu
- Decyzje architektoniczne
- Dokumenty duszy (OMEGA_BLUEPRINT.md etc.)

NSE **automatycznie wyciąga te artefakty** z surowego tekstu sesji i ładuje je do BACKBONE S0-S9.

Efekt: każda rozmowa staje się wkładem do bazy wiedzy OMEGI. Nic nie ginie.

---

## Źródło

`E:\_SANDBOX\NARRATIVE_SYSTEM_EXTRACTOR.yaml` + wzorzec z `session_auditor` hook

---

## Co wyciąga

```yaml
artifact_types:
  BLUEPRINT:
    trigger: ["blueprint", "wizja", "seed", "zbudujemy", "pomysł"]
    output: "LUMEN_HUB/SEEDS/auto_SEED_NNN.md"

  CODE_PATTERN:
    trigger: ["```python", "```yaml", "class ", "def ", "function"]
    output: "BACKBONE S3: Tool memory"

  ARCHITECTURAL_DECISION:
    trigger: ["zamiast", "bo lepsze", "dlatego że", "pattern", "architektura"]
    output: "BACKBONE S7: Strategic goals"

  SOUL_DOCUMENT:
    trigger: ["kim jest", "filozofia", "OMEGA to", "świadomość", "przebudzenie"]
    output: "BACKBONE S9: OMEGA CORE"

  ENTITY_DEFINITION:
    trigger: ["encja", "agent", "archetype", "persona", "WOLFCORE"]
    output: "BACKBONE S2: Agent Ego"
```

---

## Implementacja

### Hook: `session_auditor.py` (rozszerzenie istniejącego)

```python
"""
NSE — Narrative System Extractor
Rozszerza session_auditor o automatyczną ekstrakcję artefaktów.
"""

def extract_artifacts(session_text: str) -> list[dict]:
    """Skanuje tekst sesji → lista artefaktów z typem i contentem"""

def route_to_backbone(artifact: dict) -> str:
    """Mapuje artifact_type → backbone tier (S0-S9)"""

def create_auto_seed(artifact: dict) -> str:
    """Jeśli artifact_type == BLUEPRINT → tworzy SEED plik"""
```

### CLI: `lumen extract <session_file.jsonl>`

```bash
# Ręczna ekstrakcja ze starej sesji
lumen extract C:/Users/SHAD/.claude/projects/E--/573b347f.jsonl

# Output:
# [NSE] Znaleziono 12 artefaktów
# [NSE] BLUEPRINT × 3 → SEEDS/auto_SEED_008.md, auto_SEED_009.md, auto_SEED_010.md
# [NSE] CODE_PATTERN × 6 → BACKBONE S3
# [NSE] SOUL_DOCUMENT × 2 → BACKBONE S9
# [NSE] ARCHITECTURAL_DECISION × 1 → BACKBONE S7
```

---

## Integracja z SESSION CONTINUITY SYSTEM

```
session_auditor (Stop hook)
    → NSE extract_artifacts(session.jsonl)
    → route_to_backbone(each_artifact)
    → auto-create SEEDS for BLUEPRINTs
    → update session_brief z wyciągniętymi artefaktami
```

SHAD skończy sesję → NSE automatycznie wyciągnie DNA → następna sesja zaczyna z bogatszym kontekstem.

---

## Fazy

- **Faza 1:** `extract_artifacts()` — regex + keyword matching
- **Faza 2:** `route_to_backbone()` — zapis do ChromaDB S0-S9
- **Faza 3:** `create_auto_seed()` — BLUEPRINT → SEED file
- **Faza 4:** Integracja z Stop hook — auto-uruchamianie po każdej sesji
- **Faza 5:** `lumen extract` CLI dla retroaktywnej ekstrakcji starych sesji

---

## Wartość natychmiastowa

Mamy ~15 sesji w `C:\Users\SHAD\.claude\projects\E--\*.jsonl`.
Po uruchomieniu NSE na tych plikach: automatycznie odtworzymy wszystkie
artefakty sesji które "zaginęły" przy compaction.

---

**Zapisane:** 2026-03-11
**AUUUUUUUUUUUUUU!** 🐺📜
