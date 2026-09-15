"""Baseline priority EMS vs measured-benefit / cross-domain arbitration."""
from __future__ import annotations
from dataclasses import dataclass
from .graph import GraphState

@dataclass
class Decision:
    pv_to_elec_load_w: float = 0.0
    batt_to_elec_load_w: float = 0.0
    pv_to_batt_w: float = 0.0
    pv_to_thermal_w: float = 0.0
    thermal_to_heat_load_w: float = 0.0
    stirling_heat_in_w: float = 0.0
    stirling_elec_out_w: float = 0.0
    stirling_parasitic_w: float = 0.0
    wind_to_elec_load_w: float = 0.0
    wind_to_batt_w: float = 0.0
    curtailed_w: float = 0.0
    reason: str = ""

def stirling_electrical_efficiency(t_hot_k: float, t_cold_k: float, quality: float) -> float:
    if t_hot_k <= t_cold_k + 1.0:
        return 0.0
    return max(0.0, min(0.45, quality * (1.0 - t_cold_k / t_hot_k)))

class BaselineController:
    def __init__(self, stirling_t_on_k: float = 373.15, quality: float = 0.35):
        self.stirling_t_on_k = stirling_t_on_k
        self.quality = quality
    def decide(self, g: GraphState, t_cold_k: float) -> Decision:
        pv, wind = g.node("pv").p_available_w, g.node("wind").p_available_w
        e_load, h_load = g.node("elec_load").p_available_w, g.node("heat_load").p_available_w
        batt, tank, d = g.node("battery"), g.node("thermal"), Decision(reason="baseline")
        need = e_load
        d.pv_to_elec_load_w = min(pv, need); pv -= d.pv_to_elec_load_w; need -= d.pv_to_elec_load_w
        d.wind_to_elec_load_w = min(wind, need); wind -= d.wind_to_elec_load_w; need -= d.wind_to_elec_load_w
        if need > 0 and batt.energy_j > 0:
            d.batt_to_elec_load_w = min(need, batt.p_max_discharge_w)
        if pv > 0 and batt.headroom_j > 0:
            d.pv_to_batt_w = min(pv, batt.p_max_charge_w); pv -= d.pv_to_batt_w
        if wind > 0 and batt.headroom_j > 0:
            d.wind_to_batt_w = min(wind, max(0.0, batt.p_max_charge_w - d.pv_to_batt_w)); wind -= d.wind_to_batt_w
        d.curtailed_w = pv + wind
        d.thermal_to_heat_load_w = min(h_load, tank.p_max_discharge_w if tank.energy_j > 0 else 0.0)
        th = tank.t_k or t_cold_k
        if th >= self.stirling_t_on_k and batt.soc < 0.95 and tank.energy_j > 0:
            heat_in = max(0.0, min(tank.p_max_discharge_w - d.thermal_to_heat_load_w, 400.0))
            d.stirling_heat_in_w = heat_in
            d.stirling_elec_out_w = stirling_electrical_efficiency(th, t_cold_k, self.quality) * heat_in
            d.stirling_parasitic_w = 15.0 if heat_in > 0 else 0.0
        return d

class NetBenefitController:
    def __init__(self, quality: float = 0.35, min_net_stirling_w: float = 5.0, heat_horizon_s: float = 3600.0, controller_draw_w: float = 2.0):
        self.quality, self.min_net_stirling_w = quality, min_net_stirling_w
        self.heat_horizon_s, self.controller_draw_w = heat_horizon_s, controller_draw_w
    def decide(self, g: GraphState, t_cold_k: float) -> Decision:
        pv, wind = g.node("pv").p_available_w, g.node("wind").p_available_w
        e_load, h_load = g.node("elec_load").p_available_w, g.node("heat_load").p_available_w
        batt, tank, d = g.node("battery"), g.node("thermal"), Decision(reason="net_benefit")
        need = e_load
        d.pv_to_elec_load_w = min(pv, need); pv -= d.pv_to_elec_load_w; need -= d.pv_to_elec_load_w
        d.wind_to_elec_load_w = min(wind, need); wind -= d.wind_to_elec_load_w; need -= d.wind_to_elec_load_w
        if need > 0 and batt.energy_j > 0:
            d.batt_to_elec_load_w = min(need, batt.p_max_discharge_w); need -= d.batt_to_elec_load_w
        surplus = pv + wind
        d.thermal_to_heat_load_w = min(h_load, tank.p_max_discharge_w if tank.energy_j > 0 else 0.0)
        heat_unmet = h_load - d.thermal_to_heat_load_w
        heat_is_scarce = tank.energy_j < h_load * self.heat_horizon_s or heat_unmet > 1.0
        if surplus > 0 and batt.headroom_j > 0 and batt.soc < 0.92:
            take = min(surplus, batt.p_max_charge_w)
            d.pv_to_batt_w = min(pv, take); pv -= d.pv_to_batt_w
            d.wind_to_batt_w = take - d.pv_to_batt_w; wind -= d.wind_to_batt_w
            surplus = pv + wind
        if surplus > 0 and (heat_unmet > 0 or (tank.headroom_j > 0 and h_load > 0)):
            take = min(surplus, tank.p_max_charge_w)
            d.pv_to_thermal_w = min(pv, take); pv -= min(pv, take)
            leftover = take - d.pv_to_thermal_w
            if leftover > 0:
                used = min(wind, leftover); wind -= used; d.pv_to_thermal_w += used
            surplus = pv + wind
        d.curtailed_w = max(0.0, pv + wind)
        th = tank.t_k or t_cold_k
        eta = stirling_electrical_efficiency(th, t_cold_k, self.quality)
        heat_avail = min(400.0, max(0.0, tank.p_max_discharge_w - d.thermal_to_heat_load_w))
        parasitic = 12.0 + self.controller_draw_w
        gross, net = eta * heat_avail, eta * heat_avail - parasitic
        electric_value = need > 1.0 or batt.soc < 0.35
        thermal_ok = (not heat_is_scarce) and (tank.soc >= 0.85 or h_load < 1.0)
        if heat_avail > 20.0 and net >= self.min_net_stirling_w and electric_value and thermal_ok and tank.energy_j > 0:
            d.stirling_heat_in_w, d.stirling_elec_out_w, d.stirling_parasitic_w = heat_avail, gross, parasitic
            d.reason = "net_benefit:stirling_on"
        else:
            d.reason = "net_benefit:stirling_off"
        return d
