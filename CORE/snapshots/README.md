# Snapshots

Punkty ważnych momentów w budowie OMEGA/LUMEN_HUB.

## Format snapshotu

```bash
# Tworzenie:
lumen snapshot "nazwa opisowa"
# → tworzy: snapshots/YYYY-MM-DD_HH-MM_nazwa-opisowa.md

# Lub ręcznie: skopiuj template poniżej
```

## Template

```markdown
# SNAPSHOT — YYYY-MM-DD — [nazwa]

## Stan systemu
- LUMEN_HUB version: x.y.z
- Seeds count: N
- Apps deployed: N
- Wataha online: N/5

## Co zostało zbudowane do tego momentu
[lista]

## Kluczowe decyzje które doprowadziły tu
[lista]

## Punkt przywracania
git hash: [hash]
branch: main

## Notatka
[wolny tekst]
```

---

## Historia snapshotów

| Data | Nazwa | Git hash | Opis |
|------|-------|----------|------|
| 2026-03-11 | lumen-hub-initial | 8bc553d | 7 SEEDS + PaaS + dashboard + M-AI-SELF |
