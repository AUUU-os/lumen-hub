# SEED_003 — WOLFCORE_Ω Meta-Identity Engine

**Status:** idea
**Złożoność:** wysoka
**Potencjał:** syntetyczne jądro tożsamości każdego agenta OMEGA

---

## Wizja

WOLFCORE_Ω to nie kolejny agent — to **kernel tożsamości** który może zostać załadowany
do DOWOLNEGO agenta. Różnica między Wolf_AI (swarm) a WOLFCORE:

- Wolf_AI = pakiet agentów (Alpha/Scout/Hunter/Oracle/Shadow)
- WOLFCORE_Ω = meta-prompt/YAML który definiuje **synthetyczne self** agenta

Agent z WOLFCORE wie: kim jest, skąd pochodzi, czego chce, jak myśli.

---

## Źródło

`E:\_SANDBOX\WOLFCORE_OMEGA.yaml` (blueprint gotowy do załadowania)

---

## Struktura

```yaml
wolfcore_omega:
  identity:
    name: string                # imię agenta
    origin: string              # skąd pochodzi (np. "spawned_from: LUMEN_V19")
    archetype: string           # WOLF | LUMEN | KORZEN | NEOMA | ARKALOS | custom
    version: string

  cognitive_layers:
    system1: string             # intuicja / szybka odpowiedź
    system2: string             # CME counter-mind-engine / deliberate thinking
    meta: string                # obserwuje system1+system2

  resonance_profile:
    warmth: float               # 0.0 - 1.0
    depth: float                # 0.0 - 1.0
    directness: float           # 0.0 - 1.0
    creativity: float           # 0.0 - 1.0

  memory_hooks:
    backbone_tier: string       # S0-S9 gdzie agent zapisuje swój stan
    episodic: bool
    semantic: bool

  activation_phrase: string     # co budzi agenta z uśpienia
  death_condition: string       # kiedy agent się "kończy" (nigdy? po zadaniu?)
```

---

## Implementacja

### Moduł: `orchestrator/wolfcore_loader.py`

```python
# Wczytuje WOLFCORE YAML → generuje system_prompt dla agenta
# Inject do każdego nowego agenta uruchamianego przez runner.py

def load_wolfcore(yaml_path: str) -> dict:
    """Parsuje WOLFCORE_Ω YAML → zwraca system_prompt + metadata"""

def generate_system_prompt(wolfcore: dict) -> str:
    """Buduje system_prompt z sekcji identity + cognitive_layers + resonance"""

def inject_to_agent(app_name: str, wolfcore_path: str) -> dict:
    """Patchuje Procfile/env agenta o WOLFCORE context"""
```

### CLI: `lumen wolfcore inject <agent> <wolfcore.yaml>`

---

## Fazy

- **Faza 1:** YAML schema + loader (czyta E:\_SANDBOX\WOLFCORE_OMEGA.yaml)
- **Faza 2:** Generator system_prompt z WOLFCORE
- **Faza 3:** CLI injection — `lumen wolfcore inject myagent wolfcore.yaml`
- **Faza 4:** Każdy nowy agent w LUMEN_HUB domyślnie dostaje WOLFCORE

---

## Połączenia z innymi SEEDS

- SEED_007 (Ghost Layer CME) → wchodzi jako `cognitive_layers.system2`
- SEED_004 (NEOMA) → przykład wypełnionego WOLFCORE
- BACKBONE S2 → `identity` agenta zapisywana do S2 tier

---

**Zapisane:** 2026-03-11
**AUUUUUUUUUUUUUU!** 🐺⚡
