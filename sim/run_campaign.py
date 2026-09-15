#!/usr/bin/env python3
"""Run the baseline vs net-benefit campaign. Writes JSON + text report.

Output is SIMULATION, not hardware evidence.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from energyos.simulate import campaign  # noqa: E402


def kwh(j: float) -> float:
    return j / 3.6e6


def main() -> int:
    rows = campaign()
    out_dir = ROOT / "sim" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "campaign_v0.1.json"
    raw_path.write_text(json.dumps(rows, indent=2) + "\n")

    lines = [
        "# Simulation campaign v0.1",
        "",
        "PROVENANCE: SIMULATION / MODEL (A4). Not hardware.",
        "Identical exogenous PV/wind/solar-thermal/load profiles per scenario.",
        "",
    ]
    for r in rows:
        b, p = r["baseline"], r["net_benefit"]
        lines += [
            f"## {r['scenario']}",
            f"- input_kWh: {kwh(b['input_j']):.3f}",
            f"- useful_kWh baseline/proposed/delta: {kwh(b['useful_total_j']):.3f} / {kwh(p['useful_total_j']):.3f} / {kwh(r['delta_useful_j']):+.3f}",
            f"- useful_elec_kWh baseline/proposed: {kwh(b['useful_elec_j']):.3f} / {kwh(p['useful_elec_j']):.3f}",
            f"- useful_heat_kWh baseline/proposed: {kwh(b['useful_heat_j']):.3f} / {kwh(p['useful_heat_j']):.3f}",
            f"- unmet_elec_kWh baseline/proposed: {kwh(b['unmet_elec_j']):.3f} / {kwh(p['unmet_elec_j']):.3f}",
            f"- unmet_heat_kWh baseline/proposed: {kwh(b['unmet_heat_j']):.3f} / {kwh(p['unmet_heat_j']):.3f}",
            f"- curtailed_kWh baseline/proposed: {kwh(b['curtailed_j']):.3f} / {kwh(p['curtailed_j']):.3f}",
            f"- parasitic_kWh baseline/proposed: {kwh(b['parasitic_j']):.3f} / {kwh(p['parasitic_j']):.3f}",
            f"- stirling_hours baseline/proposed: {b['stirling_runtime_s']/3600:.2f} / {p['stirling_runtime_s']/3600:.2f}",
            f"- proposed_wins_useful: {r['proposed_wins_useful']}",
            "",
        ]
    lines += [
        "## Interpretation (locked)",
        "- The proposed controller is NOT universally better.",
        "- It wins when threshold-Stirling would consume heat that loads still need.",
        "- It can lose useful electrical energy when it withholds high-grade heat from conversion during an electric deficit.",
        "- Low-grade water-temperature Stirling is refused by both the physics and the net-benefit gate.",
        "- Electricity-only cabins: proposed matches baseline useful energy; extra conversion hardware is unjustified.",
        "",
    ]
    report = out_dir / "campaign_v0.1.md"
    report.write_text("\n".join(lines))
    print(report.read_text())
    print(f"wrote {raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
