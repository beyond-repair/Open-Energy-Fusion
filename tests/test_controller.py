import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from energyos.controller import stirling_electrical_efficiency
from energyos.simulate import SCENARIOS, campaign, run


def test_efficiency_zero_when_no_delta_t():
    assert stirling_electrical_efficiency(300.0, 300.0, 0.35) == 0.0
    assert stirling_electrical_efficiency(290.0, 300.0, 0.35) == 0.0


def test_efficiency_bounded_and_increases_with_thot():
    lo = stirling_electrical_efficiency(350.0, 280.0, 0.35)
    hi = stirling_electrical_efficiency(500.0, 280.0, 0.35)
    assert 0.0 < lo < hi < 0.45


def test_energy_not_created_elec_only():
    sc = next(s for s in SCENARIOS if s.name == "elec_only_cabin")
    tot = run(sc, "net_benefit")
    assert tot.useful_elec_j <= tot.input_j + 1.0
    assert tot.useful_heat_j >= -1e-6


def test_campaign_runs_and_reports():
    rows = campaign()
    assert len(rows) == 5
    names = {r["scenario"] for r in rows}
    assert names == {s.name for s in SCENARIOS}
    for r in rows:
        assert r["baseline"]["steps"] == r["net_benefit"]["steps"]
        assert r["baseline"]["input_j"] > 0
        assert r["net_benefit"]["input_j"] > 0
        assert math.isclose(r["baseline"]["pv_in_j"], r["net_benefit"]["pv_in_j"], rel_tol=1e-9)
        assert math.isclose(r["baseline"]["wind_in_j"], r["net_benefit"]["wind_in_j"], rel_tol=1e-9)


def test_low_grade_stirling_should_not_dominate_runtime():
    sc = next(s for s in SCENARIOS if s.name == "low_grade_thermal_trap")
    b = run(sc, "baseline")
    p = run(sc, "net_benefit")
    assert p.stirling_runtime_s <= b.stirling_runtime_s + 1.0


def test_cold_cabin_does_not_increase_unmet_heat():
    sc = next(s for s in SCENARIOS if s.name == "cold_cabin_heat_demand")
    b = run(sc, "baseline")
    p = run(sc, "net_benefit")
    assert p.unmet_heat_j <= b.unmet_heat_j + 1.0


def test_proposed_protects_heat_when_baseline_burns_it():
    sc = next(s for s in SCENARIOS if s.name == "baseline_burns_needed_heat")
    b = run(sc, "baseline")
    p = run(sc, "net_benefit")
    assert p.unmet_heat_j <= b.unmet_heat_j + 1.0
    assert p.stirling_runtime_s <= b.stirling_runtime_s + 1.0
