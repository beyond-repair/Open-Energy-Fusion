# Audit — 2026-09-15

## Scope

Autonomous architecture review of the Open Energy Fusion brief against
the `beyond-repair` GitHub organization, public prior art, and a
deterministic simulation of the proposed dispatcher.

## Repository finding

- No Energy Fusion / Energy Accounting Bench / EnergyOS repository
  existed under `beyond-repair` at audit time (org search + code search
  for CAL-0001, EnergyOS, Stirling).
- The firmware named **Energy Accounting Bench V1.0.0-RC2** is a
  specification in the project brief, not an inspectable tree.
- Therefore: there was no raw experimental data, no analysis scripts
  tied to hardware, and no git history to reconstruct. The “existing
  project” is the brief itself.

## Falsification results

| Question | Result |
|---|---|
| Does hybrid architecture always improve useful energy? | **No.** Electricity-only: tie. High-grade electric deficit: proposed can lose. |
| Does the control layer beat conventional EMS? | **Sometimes.** Wins when threshold-Stirling burns needed heat. |
| Does Stirling earn mass and losses? | **Not at low-grade water temperatures under A4 efficiencies.** Optional only. |
| Could PV+battery outperform the full stack? | **Yes, for electricity-only useful energy.** Thermal hardware is justified only when heat is a real load. |
| Can it run offline / be repaired / be built cheaply? | Architecturally yes, if the core stays small and modules are optional. |
| Is there a genuine technical contribution? | Discipline + explicit net-benefit gate + measurement contract. Not a new physics. |

## Verdict

**YELLOW — INVESTIGATE**

The mechanism is coherent and the open-source mission is worthwhile.
It is not GREEN because:

1. Claimed firmware does not exist.
2. Simulation benefit is conditional, not general.
3. Hardware η, parasitics, and cost/mass have not been measured.
4. Prior art already covers energy hubs, EMS, and self-describing DERs.

Safe work that proceeds under YELLOW: publish the contract, the
dispatcher, the simulation campaign, and the calibration sequence.
Do not ship a Stirling-centric product narrative.
