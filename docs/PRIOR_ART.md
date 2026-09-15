# Prior art (investigation, not a patentability opinion)

Nothing here is a novelty or patent claim.

## Already known

1. **Energy hubs / multi-carrier OPF** — Geidl & Andersson, 2005–2007
   (ETH Vision of Future Energy Networks). Coupling of electricity, gas,
   and heat; operational and structural optimization.
2. **Home / site EMS** — OpenEMS, FENECON FEMS, EMHASS, HOMER, vendor
   hybrid inverters. PV + battery + load priority is commodity logic.
3. **CHP / Stirling micro-CHP** — WhisperGen, Microgen, Qnergy, solar-dish
   Stirling CCHP literature. PVT + Stirling + storage papers exist
   (e.g. Zhu et al., Energy Conversion and Management 284, 2023).
4. **Cascade / waste-heat dispatch** — MILP models that grade heat
   quality and refuse low-value recovery paths.
5. **Self-describing electrical modules** — SunSpec Modbus, IEC 61850,
   IEEE 1547 / 2030.5. Hardware-independent electrical telemetry is
   standardized.
6. **Parasitic-aware conversion** — industrial WHR and CHP controllers
   already subtract auxiliary power before declaring a unit "on."

## Obvious combination

"AI / rules that coordinate solar, wind, batteries, and a heat engine"
is an obvious combination of (2) and (3). Shipping that as the headline
is not a contribution.

## Potentially differentiated (needs deeper search, not a claim)

1. An explicit **net-useful-benefit gate** as the *only* activation law
   for every conversion edge, with parasitics and domain opportunity
   cost first-class, implemented as an offline open protocol for
   heterogeneous DIY / field systems — not a campus MILP.
2. A **measurement-first acquisition contract** that refuses to optimize
   before CAL-0001…0005 pass, and that keeps raw logs immutable and
   provenance-tagged (SIMULATION vs HARDWARE).
3. A **cross-domain module capability report** that covers electrical,
   thermal, and mechanical state in one contract simple enough for
   cheap microcontrollers — SunSpec-class, but not electricity-only.

These are "investigate," not "we invented this."

## Genuinely unusual? Not on current evidence

No mechanism in the brief requires a new physical law or a new converter
topology. The unusual part, if any, is discipline: do not ship a Stirling
(or PCM, or TEG) unless the bench says it pays.
