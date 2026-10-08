import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from energyos.__main__ import main
from energyos.report import render_json, render_markdown
from energyos.simulate import campaign


def test_committed_report_matches_simulation():
    rows = campaign()
    committed = (ROOT / "sim" / "results" / "campaign_v0.1.md").read_text()
    assert render_markdown(rows) == committed


def test_committed_json_matches_simulation():
    committed = json.loads((ROOT / "sim" / "results" / "campaign_v0.1.json").read_text())
    fresh = json.loads(render_json(campaign()))
    assert [r["scenario"] for r in committed] == [r["scenario"] for r in fresh]
    for c, f in zip(committed, fresh):
        assert c["proposed_wins_useful"] == f["proposed_wins_useful"]
        assert abs(c["delta_useful_j"] - f["delta_useful_j"]) < 1.0


def test_cli_markdown(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "PROVENANCE: SIMULATION" in out
    assert "## baseline_burns_needed_heat" in out


def test_cli_json_and_out(tmp_path, capsys):
    assert main(["--json", "--out", str(tmp_path)]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert len(rows) == 5
    assert (tmp_path / "campaign_v0.1.json").exists()
    assert (tmp_path / "campaign_v0.1.md").exists()


def test_python_dash_m_entry():
    env_src = str(ROOT / "src")
    proc = subprocess.run(
        [sys.executable, "-m", "energyos", "--version"],
        capture_output=True, text=True, env={"PYTHONPATH": env_src, "PATH": "/usr/bin:/bin"},
    )
    assert proc.returncode == 0
    assert "energyos 0.1.0" in proc.stdout
