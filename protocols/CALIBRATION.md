# Calibration and characterization sequence

Do not invent pass/fail limits before measuring the actual instrument
noise and reference agreement.

## Order (frozen intent)

| ID | Name | Intent |
|---|---|---|
| CAL-0001 | ZERO-STATE | 30 min, no heater, no Stirling, no solar, no load. Noise floor. |
| CAL-0002 | ISOTHERMAL | Thermocouples in a common thermal environment. Offsets. |
| CAL-0003 | DMM-REF | Voltage/current vs a reference instrument. |
| CAL-0004 | TACH-REF | RPM vs a reference tachometer (if a rotating converter exists). |
| CAL-0005 | STRESS-TEST | Long-duration logging, clock stability, storage integrity. |

Only after these produce files:

| ID | Name | Intent |
|---|---|---|
| A-001 | HEATER-ONLY | Known electrical heat into the thermal mass. Close Q_in vs ΔE + E_loss. |

## Accounting identities (to be tested, not assumed)

Stirling (when present):

- `P_net = P_e - P_aux`
- `η_el = P_e / Q_in`  (electrical only)
- Useful thermal rejected to a load is accounted separately, never
  added into `η_el`.

Solar thermal:

- `Q_stored = m c_p ΔT`
- `P_solar = G A`
- `η_collector = Q_thermal / (G A)`
- `E_solar,in = ΔE_stored + E_loss`  (losses explicit)

## Acquisition rules

- Raw files contain samples, timestamps, sequence numbers, experiment
  id, configuration id, provenance.
- No calibration correction baked into raw.
- No destructive filter.
- Failed experiments are kept and marked, not deleted.
- Processing is a separate program from acquisition.
