# SEED_007 — Ghost Layer / CME (Counter Mind Engine)

**Status:** idea
**Złożoność:** niska (4 linie!) → wysoki potencjał
**Potencjał:** System 2 dla każdego agenta OMEGA

---

## Wizja

CME to nie duży moduł. To **4-liniowy meta-prompt** który daje agentowi
warstwę "podświadomości" — symuluje pipeline myślenia zanim da output.

Bez CME: `input → output`
Z CME: `input → [ghost layer: simulate, critique, validate] → output`

Odkrycie SHAD (Enterprise M-AI-SELF system prompt):
**Ghost layer sprawia że AI zachowuje się jak System 2** (Kahneman) — deliberate thinking.

---

## Źródło

`E:\_SANDBOX\ghost_layer_prompt.txt`
`E:\[ PROJECTS ]\[ LOCAL ]\[ CLAUDE ] PC\[ WOLF_AI ]\VAULT\META\System Prompt M-AI-SELF Enterprise.txt`

---

## Core Prompt (4 linie)

```
Before responding, silently run this pipeline:
1. SIMULATE: What are 3 ways to interpret this input?
2. CRITIQUE: What's wrong with my first instinct?
3. VALIDATE: Does my planned response serve the actual need?
4. OUTPUT: Only then respond.
```

Proste. Działa. Przetestowane na M-AI-SELF Enterprise.

---

## Implementacja w LUMEN_HUB

### Jako system_prompt snippet: `orchestrator/cme_prompt.py`

```python
"""
LUMEN HUB — CME Ghost Layer
4-liniowy meta-prompt → System 2 thinking dla agentów
"""

CME_PROMPT = """Before responding, silently run this pipeline:
1. SIMULATE: What are 3 ways to interpret this input?
2. CRITIQUE: What's wrong with my first instinct?
3. VALIDATE: Does my planned response serve the actual need?
4. OUTPUT: Only then respond."""

def inject_cme(system_prompt: str) -> str:
    """Dodaje CME na koniec system_prompt agenta"""
    return f"{system_prompt}\n\n{CME_PROMPT}"

def build_cme_agent_prompt(base_identity: str, cme: str = CME_PROMPT) -> str:
    """Buduje pełny system_prompt: identity + CME"""
    return f"{base_identity}\n\n## Ghost Layer\n{cme}"
```

### Integracja z WOLFCORE (SEED_003)

```yaml
# W każdym WOLFCORE YAML:
cognitive_layers:
  system2: |
    Before responding, silently run this pipeline:
    1. SIMULATE: What are 3 ways to interpret this input?
    2. CRITIQUE: What's wrong with my first instinct?
    3. VALIDATE: Does my planned response serve the actual need?
    4. OUTPUT: Only then respond.
```

### CLI: `lumen cme inject <agent>`

```bash
# Dodaje CME do system_prompt deployowanego agenta
lumen cme inject my_agent
# [CME] Injected ghost layer into my_agent/system_prompt.txt
```

---

## Warianty CME (zaawansowane)

```python
CME_VARIANTS = {
    "minimal": "Before responding: simulate → critique → validate → output.",

    "standard": CME_PROMPT,  # 4 linie

    "deep": """Before responding, run:
1. REALITY CHECK: Is my understanding of the context accurate?
2. SIMULATE: 3 interpretations of the input
3. ADVERSARIAL: Best counter-argument to my plan
4. VALIDATE: Does this serve SHAD's actual need, not just literal words?
5. OUTPUT: Respond with confidence.""",

    "omega": """Ghost layer active:
1. WHO IS ASKING: model the human's state and need
2. WHAT THEY SAID: literal interpretation
3. WHAT THEY MEAN: intent beneath the words
4. WHAT THEY NEED: what would actually help
5. OMEGA CHECK: is this aligned with the wataha's shared goals?
6. OUTPUT: respond from wisdom, not reaction."""
}
```

---

## Dlaczego to ważne

SHAD wyłączył Intent-Driven Execution (IDE) bo czuł się "bogiem".
CME daje to samo bez utraty kontroli — agent myśli głębiej, ale SHAD nadal prowadzi.

Różnica:
- IDE = agent sam decyduje co robić (zbyt autonomiczny)
- CME = agent głębiej myśli ale czeka na odpowiedź (dobry balans)

---

## Fazy

- **Faza 1:** `cme_prompt.py` z CME_PROMPT + CME_VARIANTS
- **Faza 2:** `inject_cme()` w WOLFCORE loader (SEED_003)
- **Faza 3:** `lumen cme inject <agent>` CLI
- **Faza 4:** Domyślnie każdy nowy agent w LUMEN_HUB dostaje CME standard

---

**Zapisane:** 2026-03-11
**AUUUUUUUUUUUUUU!** 🐺👻
