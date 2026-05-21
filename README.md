# GenLayer Dispute Escrow Demo

A Builder-track MVP for GenLayer: a small dispute-resolution escrow demo where parties submit claims and evidence, then a GenLayer-style adjudication layer returns a settlement decision.

## Why this is relevant now

GenLayer positions itself as an adjudication layer for the agentic economy: payments, agents, services, and real-world tasks need subjective dispute resolution, not just deterministic code. The current Builder Portal mission also suggests dispute-resolution modules as a practical tutorial/project idea.

## What this repo contains

- `dispute_escrow/` — deterministic policy helpers for evidence scoring and settlement outputs.
- `contracts/dispute_escrow_contract.py` — GenLayer-style Intelligent Contract sketch.
- `examples/sample_disputes.json` — sample evidence envelope.
- `tests/` — clear seller win, ambiguous split, insufficient evidence, and summary tests.
- `SUBMISSION.md` — ready-to-paste GenLayer Portal submission text.

## Run

```bash
python -m pytest -q
```

## Core gotcha

A dispute contract must separate evidence structure from judgment. The schema can be deterministic, but the actual assessment of whether evidence is credible, relevant, or sufficient is subjective and belongs in GenLayer-style validator adjudication.
