# Changelog

All notable releases of the SVIE powertrain monorepo are recorded here.

## [1.3.1] — 2026-09-23

### Interactive physics lab

- Coupled live lab: RPM ηv map, BTE, torque/power, HEX, injector duty
- Portal **`/lab`** — drag controls + power/torque/fuel curves (works offline on Pages)
- `svie_physics.physics_lab` + API `/calc/lab` · `/calc/lab/sweep`
- Calculators WOT tab live-recomputation on slider drag

## [1.3.0] — 2026-09-23

### Live demo + production-ready acquisition package

- **GitHub Pages live demo** — static portal export + Actions workflow (`.github/workflows/pages.yml`)
- Guided `/demo` tour works offline via `public/demo/golden.json`
- Docs: [`docs/LIVE-DEMO.md`](docs/LIVE-DEMO.md) · https://theworker02.github.io/SVIE-concept/
- **Claim:** acquisition monorepo is production-ready; hardware TRL remains **3** (honest)
- Acquisition suite: readiness scorecard, deal structures, data-room index (`svie_physics.acquisition_suite`)
- Compliance packs: homologation, ISO 26262 SENTINEL map, ISO 21434 AETHER, OTA policy, durability gates
- Supply-chain Tier-1 critical-path map (`svie_physics.supply_chain`)
- Deal room docs: TERM-SHEET, DEAL-STRUCTURES, DATA-ROOM, CLOSING-CHECKLIST, PRODUCTION-READINESS
- Licensing packages **COMPLIANCE** + **ACQUIRE** (14 total)
- Portal **`/acquisition`** live desk; demo step `06-acquire`; validate gates for readiness
- Acquisition.md / EXECUTIVE-BRIEF / VALUE-THESIS rewritten for 1.3 close posture

## [1.6.0] — 2026-09-23

### AETHER-OS — analog-first luxury HMI + CarPlay Ultra

- AETHER-OS design package: kernel / safety / analog / guest modules
- Apple CarPlay Ultra as **guest** layer — physical controls win conflicts
- Specs: `aether_os.yaml`, `carplay_ultra.yaml`, `analog_hmi.yaml` + cabin update
- `svie_physics.aether_os` models + golden tests; API `/calc/aether`
- Portal `/hmi` interactive luxury mock (analog gauges, coverable glass, stack)
- Design renders: analog cabin + milled control stack
- DESIGN licensing package now includes HMI / Ultra policy

## [1.5.0] — 2026-09-23

### Vehicle design system (parallel design package)

- Production-ready design docs: exterior, lighting, cabin, packaging, wiring harness
- Specs + `svie_physics.design_system` + golden tests
- Concept renders in `design/renders/` and portal `/design`
- Licensing package **DESIGN** — does not replace main powertrain Acquisition plan

## [1.4.0] — 2026-09-23

### Validation + add-ons

- Full validation report (`docs/validation-report.md`) with literature grounding (PTWA 150 µm Ford precedent, EMVT power∝RPM, DCT interrupt context vs FLUX 8 ms *design target*)
- Cross-spec harness: `python -m svie_physics.validate` (8 consistency checks)
- Add-ons: DRY-SUMP-X, PULSE-EGR, SILK-MOUNT, RANGE-BRIDGE, KERS-BLEND
- Portal calculators: Add-ons + Validate tabs; licensing package ADDONS

## [1.3.0] — 2026-09-23

### Engine · transmission · body · manufacturing

- Engine+: CRYO-RAIL, RING-ZERO, OIL-SPINE, AETHER-IGN (specs + models + docs)
- Transmission+: FLUX-SHIFT, GEAR-MESH-AM, JET-BEARING
- Body+: NODE-CAST, AERO-SKIN, CELL-VAULT, THERMAL-SKIN
- Manufacturing master plan (15 process routes, PTWA/LPBF/CFRP cells) + `svie_physics.manufacturing`
- Portal calculators: Platform+ and Manufacturing tabs; 10 licensing packages; 35 YAML specs

## [1.2.0] — 2026-09-23

### Viewer & acquisition polish

- Added `/pitch` acquisition pitch page with audience paths and deal framing
- Added `docs/VIEWER-GUIDE.md`, `VALUE-THESIS.md`, `COMPETITIVE-MATRIX.md`, `brand/MEDIA-KIT.md`
- Header API live/offline status badge; richer home and specs (package filters + offline catalog)
- Portal README route map; Acquisition.md / INDEX updated for viewer entry points

## [1.1.1] — 2026-09-23

### Package thickness (acquisition)

- Diligence library under `docs/acquisition/`
- `svie_physics.inventory`, `/diligence`, `/package`, live `/demo`
- Expanded Acquisition.md with modular licensing

## [1.1.0] — 2026-09-23

### Acquisition readiness

- Acquisition.md, brand kit, CLI demo, README badges, version alignment

## [0.1.0] — 2026-09

Initial engineering monorepo scaffold.
