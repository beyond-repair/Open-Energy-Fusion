# Firmware

The project brief referred to **Energy Accounting Bench V1.0.0-RC2** with:

- boot / clock / SD / sensor diagnostics
- immutable raw acquisition
- write/read-back verification
- sequence numbers
- SIMULATION vs HARDWARE provenance
- no hidden calibration in the raw path

**Audit finding:** that implementation is not present in this repository
and was not found under `beyond-repair` at review time.

This directory is the placeholder for a future acquisition firmware.
Until hardware logs exist:

- do not invent acceptance limits
- do not embed derived efficiencies in raw files
- do not label simulation traces as bench data

See `protocols/` for the intended calibration order (CAL-0001 … CAL-0005,
then A-001 heater-only).
