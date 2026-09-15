"""Deterministic campaign. MODEL (A4). Not hardware evidence."""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from .controller import BaselineController, NetBenefitController, Decision
from .graph import Domain, GraphState, Node, NodeKind

DT_S, CP_WATER = 60.0, 4186.0

def _diurnal(hour, peak, sunrise=6.5, sunset=18.5):
    if hour < sunrise or hour > sunset:
        return 0.0
    x = (hour - sunrise) / (sunset - sunrise)
    return peak * math.sin(math.pi * x) ** 1.4

def _wind(hour, day, peak):
    return max(0.0, peak * (0.35 + 0.45 * math.sin(2 * math.pi * (hour / 24.0 + day * 0.17))))

@dataclass
class Scenario:
    name: str
    days: int = 3
    pv_peak_w: float = 400.0
    wind_peak_w: float = 80.0
    elec_base_w: float = 40.0
    elec_evening_w: float = 90.0
    heat_base_w: float = 0.0
    heat_night_w: float = 0.0
    batt_wh: float = 1200.0
    tank_kg: float = 80.0
    t_amb_k: float = 283.15
    t_tank_init_k: float = 320.0
    t_tank_max_k: float = 368.15
    solar_thermal_peak_w: float = 0.0
    quality: float = 0.35

@dataclass
class Totals:
    useful_elec_j: float = 0.0
    useful_heat_j: float = 0.0
    unmet_elec_j: float = 0.0
    unmet_heat_j: float = 0.0
    curtailed_j: float = 0.0
    conversion_loss_j: float = 0.0
    parasitic_j: float = 0.0
    pv_in_j: float = 0.0
    wind_in_j: float = 0.0
    solar_thermal_in_j: float = 0.0
    batt_throughput_j: float = 0.0
    stirling_runtime_s: float = 0.0
    stirling_heat_in_j: float = 0.0
    stirling_elec_out_j: float = 0.0
    pv_to_thermal_j: float = 0.0
    steps: int = 0
    @property
    def useful_total_j(self):
        return self.useful_elec_j + self.useful_heat_j
    @property
    def input_j(self):
        return self.pv_in_j + self.wind_in_j + self.solar_thermal_in_j

def build_state(sc: Scenario) -> GraphState:
    g = GraphState()
    cap = sc.tank_kg * CP_WATER * (sc.t_tank_max_k - sc.t_amb_k)
    e0 = sc.tank_kg * CP_WATER * max(0.0, sc.t_tank_init_k - sc.t_amb_k)
    g.add(Node("pv", Domain.ELECTRICAL, NodeKind.SOURCE))
    g.add(Node("wind", Domain.ELECTRICAL, NodeKind.SOURCE))
    g.add(Node("solar_thermal", Domain.THERMAL, NodeKind.SOURCE))
    g.add(Node("battery", Domain.ELECTRICAL, NodeKind.STORAGE, capacity_j=sc.batt_wh*3600.0, energy_j=sc.batt_wh*3600.0*0.45, p_max_charge_w=300.0, p_max_discharge_w=300.0, eta_charge=0.95, eta_discharge=0.95))
    g.add(Node("thermal", Domain.THERMAL, NodeKind.STORAGE, capacity_j=cap, energy_j=e0, p_max_charge_w=800.0, p_max_discharge_w=600.0, t_k=sc.t_tank_init_k, self_discharge_frac_per_s=1.5e-6))
    g.add(Node("elec_load", Domain.ELECTRICAL, NodeKind.LOAD))
    g.add(Node("heat_load", Domain.THERMAL, NodeKind.LOAD))
    return g

def _profiles(sc, step):
    t_s = step * DT_S
    hour, day = (t_s / 3600.0) % 24.0, int(t_s // 86400)
    eve = sc.elec_evening_w * math.sin(math.pi * (hour - 17.0) / 5.0) if 17.0 <= hour <= 22.0 else 0.0
    heat = sc.heat_base_w + (sc.heat_night_w if (hour >= 20.0 or hour <= 7.0) else 0.0)
    return _diurnal(hour, sc.pv_peak_w), _wind(hour, day, sc.wind_peak_w), _diurnal(hour, sc.solar_thermal_peak_w), sc.elec_base_w + eve, heat

def apply_decision(g, d: Decision, sc, st_w):
    dt = DT_S
    acc = {k: 0.0 for k in ("useful_elec_j","useful_heat_j","unmet_elec_j","unmet_heat_j","curtailed_j","conversion_loss_j","parasitic_j","pv_in_j","wind_in_j","solar_thermal_in_j","batt_throughput_j","stirling_runtime_s","stirling_heat_in_j","stirling_elec_out_j","pv_to_thermal_j")}
    batt, tank = g.node("battery"), g.node("thermal")
    e_need, h_need = g.node("elec_load").p_available_w, g.node("heat_load").p_available_w
    acc["pv_in_j"], acc["wind_in_j"], acc["solar_thermal_in_j"] = g.node("pv").p_available_w*dt, g.node("wind").p_available_w*dt, st_w*dt
    extra = max(0.0, d.stirling_elec_out_w - d.stirling_parasitic_w)
    useful_e = min(e_need, d.pv_to_elec_load_w + d.wind_to_elec_load_w + d.batt_to_elec_load_w + extra)
    acc["useful_elec_j"], acc["unmet_elec_j"] = useful_e*dt, max(0.0, e_need-useful_e)*dt
    if d.batt_to_elec_load_w > 0:
        batt.energy_j = max(0.0, batt.energy_j - d.batt_to_elec_load_w*dt/batt.eta_discharge)
        acc["batt_throughput_j"] += d.batt_to_elec_load_w*dt
    charge_w = d.pv_to_batt_w + d.wind_to_batt_w
    leftover_s = max(0.0, extra - max(0.0, e_need - (d.pv_to_elec_load_w + d.wind_to_elec_load_w + d.batt_to_elec_load_w)))
    if leftover_s > 0 and batt.headroom_j > 0:
        charge_w += leftover_s
    if charge_w > 0:
        added = charge_w*dt*batt.eta_charge
        room = batt.headroom_j
        batt.energy_j += min(added, room)
        acc["batt_throughput_j"] += charge_w*dt
        if added > room:
            acc["curtailed_j"] += (added-room)/max(batt.eta_charge, 1e-9)
    if d.pv_to_thermal_w > 0 and tank.headroom_j > 0:
        q = min(d.pv_to_thermal_w*dt, tank.headroom_j)
        tank.energy_j += q
        acc["pv_to_thermal_j"] += q
    if d.thermal_to_heat_load_w > 0:
        q = min(d.thermal_to_heat_load_w*dt, tank.energy_j)
        tank.energy_j -= q
        acc["useful_heat_j"] += q
    if st_w > 0 and tank.headroom_j > 0:
        q = min(st_w*dt, tank.headroom_j)
        tank.energy_j += q
        if st_w*dt > q:
            acc["curtailed_j"] += st_w*dt - q
    if d.stirling_heat_in_w > 0:
        q = min(d.stirling_heat_in_w*dt, tank.energy_j)
        tank.energy_j -= q
        acc["stirling_heat_in_j"] += q
        acc["stirling_elec_out_j"] += d.stirling_elec_out_w*dt
        acc["stirling_runtime_s"] += dt
        acc["parasitic_j"] += d.stirling_parasitic_w*dt
        acc["conversion_loss_j"] += max(0.0, q - d.stirling_elec_out_w*dt)
    acc["curtailed_j"] += d.curtailed_w*dt
    acc["unmet_heat_j"] += max(0.0, h_need*dt - acc["useful_heat_j"])
    if tank.energy_j > 0 and tank.self_discharge_frac_per_s > 0:
        leak = tank.energy_j * tank.self_discharge_frac_per_s * dt
        tank.energy_j = max(0.0, tank.energy_j - leak)
        acc["conversion_loss_j"] += leak
    cap_span = sc.tank_kg * CP_WATER
    tank.t_k = min(sc.t_tank_max_k, sc.t_amb_k + tank.energy_j/cap_span if cap_span else sc.t_amb_k)
    return acc

def run(sc: Scenario, controller_name: str) -> Totals:
    g = build_state(sc)
    ctl = BaselineController(quality=sc.quality) if controller_name == "baseline" else NetBenefitController(quality=sc.quality)
    tot = Totals()
    for i in range(int(sc.days * 86400 / DT_S)):
        pv, wind, st, elec, heat = _profiles(sc, i)
        g.node("pv").p_available_w, g.node("wind").p_available_w = pv, wind
        g.node("solar_thermal").p_available_w = st
        g.node("elec_load").p_available_w, g.node("heat_load").p_available_w = elec, heat
        acc = apply_decision(g, ctl.decide(g, sc.t_amb_k), sc, st)
        for k, v in acc.items():
            setattr(tot, k, getattr(tot, k) + v)
        tot.steps += 1
    return tot

SCENARIOS = [
    Scenario(name="elec_only_cabin", t_tank_init_k=290.0),
    Scenario(name="cold_cabin_heat_demand", heat_base_w=60.0, heat_night_w=140.0, solar_thermal_peak_w=350.0, t_tank_init_k=330.0, t_amb_k=273.15),
    Scenario(name="high_grade_heat_electric_deficit", pv_peak_w=180.0, elec_base_w=70.0, elec_evening_w=150.0, heat_base_w=20.0, heat_night_w=20.0, solar_thermal_peak_w=500.0, t_tank_init_k=360.0, t_tank_max_k=420.0, tank_kg=60.0, quality=0.40, t_amb_k=288.15),
    Scenario(name="low_grade_thermal_trap", pv_peak_w=300.0, heat_base_w=10.0, heat_night_w=15.0, solar_thermal_peak_w=200.0, t_tank_init_k=330.0, t_tank_max_k=348.15, t_amb_k=293.15, quality=0.30),
    Scenario(name="baseline_burns_needed_heat", pv_peak_w=80.0, wind_peak_w=10.0, elec_base_w=25.0, elec_evening_w=30.0, heat_base_w=80.0, heat_night_w=280.0, solar_thermal_peak_w=160.0, batt_wh=600.0, tank_kg=35.0, t_amb_k=268.15, t_tank_init_k=410.0, t_tank_max_k=430.0, quality=0.38),
]

def _pack(t: Totals):
    d = asdict(t)
    d["useful_total_j"], d["input_j"] = t.useful_total_j, t.input_j
    d["useful_frac_of_input"] = t.useful_total_j / t.input_j if t.input_j else 0.0
    return d

def campaign():
    rows = []
    for sc in SCENARIOS:
        base, prop = run(sc, "baseline"), run(sc, "net_benefit")
        rows.append({"scenario": sc.name, "days": sc.days, "baseline": _pack(base), "net_benefit": _pack(prop),
                     "delta_useful_j": prop.useful_total_j-base.useful_total_j,
                     "delta_unmet_elec_j": prop.unmet_elec_j-base.unmet_elec_j,
                     "delta_unmet_heat_j": prop.unmet_heat_j-base.unmet_heat_j,
                     "delta_curtailed_j": prop.curtailed_j-base.curtailed_j,
                     "delta_parasitic_j": prop.parasitic_j-base.parasitic_j,
                     "proposed_wins_useful": prop.useful_total_j > base.useful_total_j})
    return rows
