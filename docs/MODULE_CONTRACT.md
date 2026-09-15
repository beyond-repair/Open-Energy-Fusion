# Module capability contract v0.1

The core does not need to know that a watt came from PV, wind, hydro,
Stirling, a generator, or the grid. It needs a capability report.

## Report (minimum)

| Field | Unit | Notes |
|---|---|---|
| module_id | string | stable identity |
| domain | enum | electrical / thermal / mechanical |
| safe | bool | hard interlock |
| p_available | W | signed: +source / −load |
| p_min, p_max | W | operating envelope |
| energy_stored | J | 0 if not storage |
| energy_capacity | J | 0 if not storage |
| eta_est | 0–1 | last measured, not catalog |
| p_parasitic | W | idle + active if on |
| t | K | if thermal |
| response_s | s | time to useful output |
| soh | 0–1 | optional |
| provenance | enum | SIMULATION / HARDWARE |
| seq | int | monotonic per module |

## Rules

- Catalog efficiency is not an acceptable substitute for `eta_est`
  after the module has been characterized.
- `safe=false` removes every edge incident on the module.
- The core may only command within `[p_min, p_max]`.
- Transport can be UART/Modbus/CAN. The contract is the schema,
  not the wire. Prefer existing electrical models (SunSpec) where
  they already cover a field; extend only for thermal/mechanical
  fields those models lack.

## Non-goals for v0.1

- Cloud telemetry.
- Vendor lock-in authentication schemes.
- A new world-standard competing with IEEE 1547.
