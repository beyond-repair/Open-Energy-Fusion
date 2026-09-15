# Simulation campaign v0.1

PROVENANCE: SIMULATION / MODEL (A4). Not hardware.
Identical exogenous PV/wind/solar-thermal/load profiles per scenario.

## elec_only_cabin
- input_kWh: 10.308
- useful_kWh baseline/proposed/delta: 3.739 / 3.739 / +0.000
- useful_elec_kWh baseline/proposed: 3.739 / 3.739
- useful_heat_kWh baseline/proposed: 0.000 / 0.000
- unmet_elec_kWh baseline/proposed: 0.000 / 0.000
- unmet_heat_kWh baseline/proposed: 0.000 / 0.000
- curtailed_kWh baseline/proposed: 5.918 / 6.018
- parasitic_kWh baseline/proposed: 0.000 / 0.000
- stirling_hours baseline/proposed: 0.00 / 0.00
- proposed_wins_useful: False

## cold_cabin_heat_demand
- input_kWh: 17.491
- useful_kWh baseline/proposed/delta: 12.686 / 12.686 / +0.000
- useful_elec_kWh baseline/proposed: 3.739 / 3.739
- useful_heat_kWh baseline/proposed: 8.947 / 8.947
- unmet_elec_kWh baseline/proposed: 0.000 / 0.000
- unmet_heat_kWh baseline/proposed: 0.000 / 0.000
- curtailed_kWh baseline/proposed: 5.918 / 0.000
- parasitic_kWh baseline/proposed: 0.000 / 0.000
- stirling_hours baseline/proposed: 0.00 / 0.00
- proposed_wins_useful: False

## high_grade_heat_electric_deficit
- input_kWh: 16.055
- useful_kWh baseline/proposed/delta: 8.337 / 8.206 / -0.131
- useful_elec_kWh baseline/proposed: 6.236 / 6.105
- useful_heat_kWh baseline/proposed: 2.101 / 2.101
- unmet_elec_kWh baseline/proposed: 0.237 / 0.367
- unmet_heat_kWh baseline/proposed: 0.000 / 0.000
- curtailed_kWh baseline/proposed: 0.013 / 0.000
- parasitic_kWh baseline/proposed: 0.205 / 0.101
- stirling_hours baseline/proposed: 13.67 / 7.20
- proposed_wins_useful: False

## low_grade_thermal_trap
- input_kWh: 12.360
- useful_kWh baseline/proposed/delta: 4.955 / 4.955 / +0.000
- useful_elec_kWh baseline/proposed: 3.739 / 3.739
- useful_heat_kWh baseline/proposed: 1.216 / 1.216
- unmet_elec_kWh baseline/proposed: 0.000 / 0.000
- unmet_heat_kWh baseline/proposed: 0.000 / 0.000
- curtailed_kWh baseline/proposed: 3.866 / 1.713
- parasitic_kWh baseline/proposed: 0.000 / 0.000
- stirling_hours baseline/proposed: 0.00 / 0.00
- proposed_wins_useful: False

## baseline_burns_needed_heat
- input_kWh: 5.188
- useful_kWh baseline/proposed/delta: 10.115 / 10.586 / +0.471
- useful_elec_kWh baseline/proposed: 2.030 / 2.000
- useful_heat_kWh baseline/proposed: 8.086 / 8.586
- unmet_elec_kWh baseline/proposed: 0.057 / 0.086
- unmet_heat_kWh baseline/proposed: 6.928 / 6.428
- curtailed_kWh baseline/proposed: 0.000 / 0.000
- parasitic_kWh baseline/proposed: 0.036 / 0.000
- stirling_hours baseline/proposed: 2.40 / 0.00
- proposed_wins_useful: True

## Interpretation (locked)
- The proposed controller is NOT universally better.
- It wins when threshold-Stirling would consume heat that loads still need.
- It can lose useful electrical energy when it withholds high-grade heat from conversion during an electric deficit.
- Low-grade water-temperature Stirling is refused by both the physics and the net-benefit gate.
- Electricity-only cabins: proposed matches baseline useful energy; extra conversion hardware is unjustified.
