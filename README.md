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
sim/              campaign runner + results
docs/             architecture, prior art, safety, claims, audit
protocols/        calibration sequence
firmware/         placeholder — RC2 was not found
```

## Run

```
PYTHONPATH=src python3 -m pytest tests -q
PYTHONPATH=src python3 sim/run_campaign.py
```

## Claims

See `docs/CLAIM_CAP.md`. Do not quote this README as hardware evidence.

## License

MIT. Open protocols, offline-first, no vendor lock-in in the architecture.
