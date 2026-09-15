# Architecture — EnergyOS 0.1 (contract)

## What this is

A **hardware-independent energy operating layer** that:

1. Accounts for energy in the domain it actually exists in (electrical, thermal, mechanical).
2. Activates a conversion edge only when estimated **net useful benefit** is positive.
3. Treats every device as a **capability report**, not as a brand or source type.

It is not a generator. It is not a perpetual-motion machine.
External energy must enter. The first law is an invariant.

## Layers

```
ENVIRONMENT (irradiance, wind, hydro head, ambient, waste heat)
        |
 SOURCE / MODULE INTERFACES   <- capability reports only
        |
 ENERGYOS CORE
   • energy graph (nodes + conversion edges)
   • safety interlocks (hard, not optimized away)
   • net-benefit dispatcher
   • provenance: SIMULATION | HARDWARE
        |
    USEFUL OUTPUTS
   electrical loads | thermal loads | mechanical work | stored reserve | curtail
```

## Energy graph

- **Node:** domain, kind (source|storage|load|bus|sink), capacity, energy, power limits, idle parasitic, safety flag.
- **Edge:** src → dst, η(state), active parasitic, P_max, enable, min_net.

No coupling-matrix coefficient is allowed to hide parasitics.

## Decision function

For a candidate path P at time t:

```
NET(P) = E_useful_elec(P) + E_useful_heat(P) + E_useful_mech(P)
         - E_conversion_loss(P)
         - E_parasitic(P)
         - E_opportunity(P)
```

Activate P only if NET(P) ≥ min_net (physical watts/joules, not a fitted score).

**Opportunity cost** is domain-correct, not a free weight:

- Thermal energy reserved for an unmet or imminent heat load has opportunity
  cost equal to the thermal joules that would otherwise serve that load.
- Electrical energy stored in a nearly full battery has low option value
  relative to a useful thermal dump if heat demand exists.

No hidden coefficients are used to make a campaign look good.

## Default policy (0.1)

1. Serve each load from the matching domain first (no conversion).
2. Store residual electrical energy in the battery if headroom exists.
3. Dump residual electrical energy to thermal storage only if a heat load
   exists or is reserved.
4. Run a heat→electric converter only if:
   - net electrical watts after parasitics ≥ min_net
   - heat is not scarce on the reservation horizon
   - the thermal store is near overflow **or** heat load is ~0
   - an electrical deficit or low battery exists
5. Curtail when no beneficial destination exists.

## What is core vs module

**Core (must exist):** DC bus concept, battery interface, telemetry,
safety, controller, module contract, offline operation.

**Modules (must earn their place):** PV, wind, hydro, solar thermal,
Stirling, generator, thermal store, grid, others.

Stirling is **not** part of the core. It is an optional conversion edge.

## Graceful degradation

If a module fails or reports `safe=false`, the core continues with the
remaining graph. Missing modules are absent edges, not exceptions.

## Complexity rule

A subsystem ships only if it increases measured useful energy, resilience,
controllability, or recoverability enough to justify its losses, cost,
mass, and complexity. Until measured, it stays optional and off by default.
