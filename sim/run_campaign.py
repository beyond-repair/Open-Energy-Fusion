#!/usr/bin/env python3
"""Run the baseline vs net-benefit campaign. Writes JSON + text report
into sim/results/ and prints the report.

Output is SIMULATION, not hardware evidence.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from energyos.report import write_results  # noqa: E402


def main() -> int:
    raw_path, report = write_results(ROOT / "sim" / "results")
    print(report.read_text())
    print(f"wrote {raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
