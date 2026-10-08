<div align="center">

[![Lifecycle](https://img.shields.io/badge/●_RESEARCH-a855f7?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_≤1-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)
[![Governance](https://img.shields.io/badge/ADL--Governance-7c3aed?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)

```
LIFECYCLE   RESEARCH
CLAIM       ≤1
NOT CLAIMED thrust · energy extraction · AGI · production autonomy
```

</div>

---

# Open Energy Fusion

**Verdict: YELLOW — INVESTIGATE**  
**Version: 0.1.0**  
**Provenance: specification + simulation. No hardware results.**

An open, hardware-independent energy operating layer that coordinates
whatever sources, stores, and loads a site actually has — and that
**refuses a conversion** when the conversion does not pay.

This is not a perpetual-motion project. External energy must enter.
No subsystem ships because it sounds like fusion, CHP, or "AI EMS."

```
ENVIRONMENT → MODULES → ENERGYOS CORE → ENERGY GRAPH → USEFUL OUTPUT
                                              ├ electrical loads / storage
                                              ├ thermal loads / storage
                                              └ curtail / reserve
```

## What is actually being built

1. A **measurement-first** accounting contract (raw logs ≠ optimizer).
2. A **net-useful-benefit dispatcher** over a multi-domain energy graph.
3. A **module capability report** so the core does not special-case PV vs
   wind vs Stirling.
4. A digital campaign that compares that dispatcher to a conventional
   priority EMS **before** any expensive integration.

Stirling, PCM, thermoelectrics, wind, and hydro are optional modules.
Each must earn its place with measurements.

## Simulation (v0.1, model A4)

Identical input profiles. Useful energy = served electrical load + served
heat load. See `sim/results/campaign_v0.1.md`.

| Scenario | Result |
|---|---|
| Electricity-only cabin | Tie on useful energy. Stirling off. Extra converters unjustified. |
| Cold cabin with heat | Tie on useful energy. Proposed stores surplus as heat instead of curtailing. |
| High-grade heat + electric deficit | Proposed **loses** some electrical service by withholding Stirling. |
| Low-grade thermal trap (~75 °C) | Stirling refused. Conversion does not pay. |
| Baseline burns needed heat | Proposed **wins** (~+0.47 kWh useful / 3 days in this model) by keeping heat for the load. |

The dispatcher is not universally better. That is the point of measuring.

## Repository layout

```
src/energyos/     graph, dispatcher, simulation
tests/            physics bounds + campaign invariants
sim/              campaign runner + committed results (md + json)
docs/             architecture, prior art, safety, claims, audit
protocols/        calibration sequence
firmware/         placeholder — RC2 was not found
```

## Run

Python 3.10+; the core has no runtime dependencies.

Install and run the campaign (prints the Markdown report):

```
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
energyos                 # same as: python -m energyos
energyos --json          # raw rows as JSON
energyos --out /tmp/oef  # also write campaign_v0.1.{json,md} there
python -m pytest -q
```

Without installing (what CI runs):

```
pip install -r requirements.txt
PYTHONPATH=src python3 -m pytest tests -q
PYTHONPATH=src python3 sim/run_campaign.py   # regenerates sim/results/campaign_v0.1.{json,md}
```

The committed `sim/results/` files are checked against a fresh run by
`tests/test_cli.py`, so a model change that moves the numbers fails the
tests until the results are regenerated and re-read.

## Claims

See `docs/CLAIM_CAP.md`. Do not quote this README as hardware evidence.

## License

MIT. Open protocols, offline-first, no vendor lock-in in the architecture.


---

<div align="center">

**REWRITE · BUILD · TRANSCEND**

Governing source: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) · [Claim levels 0–5](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)

</div>
