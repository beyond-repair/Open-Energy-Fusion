# Safety (non-negotiable)

Safety is not an optimization variable. A higher NET(P) never overrides
an interlock.

## Electrical

- Overcurrent protection on every source and storage branch.
- Battery: cell-level or pack BMS, over/under voltage, over-temp,
  charge-current limit. No pack without a BMS in any hardware build.
- Isolation and disconnects for PV, generator, and grid (if present).
- No "smart" firmware path that can weld a contactor closed without a
  manual mechanical disconnect.

## Thermal

- Open, unpressurized thermal storage only for early experiments
  (vented water tanks).
- **Do not** build sealed heated-liquid pressure vessels as casual
  bench experiments.
- Hot-side temperature limits, dry-run heater cutout, and a thermal
  fuse independent of the controller.

## Mechanical

- Stirling / rotating machinery: guards, emergency stop, overspeed.
- Moving parts are not a software problem.

## Fire / environment

- Battery chemistry isolation from heaters.
- Outdoor-rated enclosures or indoor placement rules.
- Emergency shutdown: hardware switch that drops all converters and
  heaters, independent of the EnergyOS process.

## Firmware / control

- Fail-safe default = all conversion edges OFF.
- Watchdog on the controller. If the dispatcher dies, outputs de-assert.
- Provenance flag must not be writable by the control loop.
