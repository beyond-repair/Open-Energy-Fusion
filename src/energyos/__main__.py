"""`python -m energyos` — run the simulation campaign and print the report.

SIMULATION / MODEL output only. Not hardware evidence.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .report import render_json, render_markdown, write_results
from .simulate import campaign


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="energyos",
        description="Run the baseline vs net-benefit EnergyOS simulation campaign (simulation only, not hardware).",
    )
    ap.add_argument("--json", action="store_true", help="print raw campaign rows as JSON instead of Markdown")
    ap.add_argument("--out", type=Path, metavar="DIR", help="also write campaign_v0.1.json and campaign_v0.1.md into DIR")
    ap.add_argument("--version", action="version", version=f"energyos {__version__}")
    args = ap.parse_args(argv)

    rows = campaign()
    sys.stdout.write(render_json(rows) if args.json else render_markdown(rows) + "\n")
    if args.out is not None:
        raw, md = write_results(args.out, rows)
        print(f"wrote {raw}", file=sys.stderr)
        print(f"wrote {md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
