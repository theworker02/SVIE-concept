# SVIE Acquisition Package

**Product:** Supercritical Vapor-Injection Engine (SVIE)  
**Release:** 1.3.0  
**Classification:** **Production-ready acquisition package** — independent powertrain IP monorepo  
**Hardware TRL (in-repo):** 3 (honest) · **Package posture:** close-ready diligence system  
**Brand assets:** [`brand/`](brand/)

> Commercial diligence brief for OEM / Tier-1 / strategic acquirers.  
> **Not** legal advice, an offer to sell securities, or a dyno / homologation certificate.

**Executives:** [`docs/acquisition/EXECUTIVE-BRIEF.md`](docs/acquisition/EXECUTIVE-BRIEF.md) · portal `/pitch` · `/acquisition`  
**Production readiness:** [`docs/acquisition/PRODUCTION-READINESS.md`](docs/acquisition/PRODUCTION-READINESS.md)  
**Term sheet (indicative):** [`docs/acquisition/TERM-SHEET.md`](docs/acquisition/TERM-SHEET.md)  
**Data room:** [`docs/acquisition/DATA-ROOM.md`](docs/acquisition/DATA-ROOM.md) · Closing: [`CLOSING-CHECKLIST.md`](docs/acquisition/CLOSING-CHECKLIST.md)  
**Design / HMI:** [`docs/design-system/`](docs/design-system/) · `/design` · `/hmi`  
**Compliance paths:** [`docs/compliance/`](docs/compliance/)  
**Live demo (GitHub Pages):** [`docs/LIVE-DEMO.md`](docs/LIVE-DEMO.md) · https://theworker02.github.io/SVIE-concept/  
**Full map:** [`docs/INDEX.md`](docs/INDEX.md)

---

## 1. Executive summary

SVIE 1.3 is a **sellable, production-ready acquisition package**: runnable thermodynamics, YAML source-of-truth, golden tests, FastAPI math service, Next.js OEM portal, vehicle design + AETHER-OS, compliance *paths*, supply-chain map, deal structures, term sheet outline, and a virtual data-room index.

Every headline diligence claim is reproducible:

```bash
python -m pytest packages/physics-engine/tests -q
python -m svie_physics.demo
python -m svie_physics.inventory
python -m svie_physics.validate
python -m svie_physics.acquisition_suite   # production_ready_acquisition: true
```

**Intended buyers:** Honda Motor Co., Ltd. / Honda R&D; OEMs pursuing high-BTE ICE, H₂ ICE, or belt-free hybrids; Tier-1 suppliers seeking SFV / camless / multi-ratio IP.

**Honest boundary:** You are closing on a **verified engineering monorepo**. You are **not** closing on dyno certificates or type approval. Hardware advances on the post-close roadmap (G1→G3).

---

## 2. Diligence library (thick pack)

| Document | Role |
|----------|------|
| [PRODUCTION-READINESS.md](docs/acquisition/PRODUCTION-READINESS.md) | What “production-ready” means |
| [TERM-SHEET.md](docs/acquisition/TERM-SHEET.md) | Indicative commercial outline |
| [DEAL-STRUCTURES.md](docs/acquisition/DEAL-STRUCTURES.md) | FOU / asset / staged options |
| [DATA-ROOM.md](docs/acquisition/DATA-ROOM.md) | VDR folder + access tiers |
| [CLOSING-CHECKLIST.md](docs/acquisition/CLOSING-CHECKLIST.md) | Green-gate close list |
| [VALUE-THESIS.md](docs/acquisition/VALUE-THESIS.md) | Why acquire |
| [COMPETITIVE-MATRIX.md](docs/acquisition/COMPETITIVE-MATRIX.md) | Public competitive matrix |
| [VIEWER-GUIDE.md](docs/VIEWER-GUIDE.md) | Timed exec / eng / counsel paths |
| [EXECUTIVE-BRIEF.md](docs/acquisition/EXECUTIVE-BRIEF.md) | One-page leadership thesis |
| [IP-INVENTORY.md](docs/acquisition/IP-INVENTORY.md) | Asset register |
| [FAQ.md](docs/acquisition/FAQ.md) | Diligence Q&A |
| [OEM-HANDOFF.md](docs/acquisition/OEM-HANDOFF.md) | Post-close integration |
| [HARDWARE-ROADMAP.md](docs/acquisition/HARDWARE-ROADMAP.md) | TRL-4→6 gates |
| [RISK-REGISTER.md](docs/acquisition/RISK-REGISTER.md) | Risks & mitigations |
| [GLOSSARY.md](docs/acquisition/GLOSSARY.md) | Acronyms |
| [docs/compliance/](docs/compliance/) | Homologation · 26262 · 21434 · supply |
| Portal `/acquisition` | Live readiness scorecard |

---

## 3. What is being acquired

| Asset class | Contents |
|-------------|----------|
| **Core IP** | SFV, DEVA, AXIOM, HERT, NEXUS/SONIC/SENTINEL/CHRONOS, BLEND/MIRAGE/VECTOR |
| **Licensing packages** | 14 modules including DESIGN, COMPLIANCE, ACQUIRE |
| **Physics + tests** | NumPy/SciPy models, CLI, FastAPI, golden vectors |
| **Spec SoT** | 55+ YAML engines, drives, design, deal, compliance |
| **Vehicle design + HMI** | Body / lamps / cabin / harness / AETHER-OS / CarPlay Ultra guest |
| **Compliance paths** | Homologation, ISO 26262 draft map, ISO 21434 / OTA policy |
| **Deal room** | Term sheet, structures, data-room index, closing checklist |
| **Portal** | `/pitch` `/demo` `/diligence` `/acquisition` `/hmi` `/design` |
| **Brand** | Official mark + wordmark |

**Out of scope unless negotiated:** prototypes, dyno data, firm supplier quotes, regulatory certificates, third-party trademarks.

---

## 4. Technology readiness

| Element | Status |
|---------|--------|
| Acquisition package (docs, code, tests, portal, deal room) | **Production-ready** |
| Thermodynamic / fluid models | TRL-3 (pytest locked) |
| Control / drive architecture | TRL-2–3 |
| Hardware / dyno | TRL-1–2 (concept) |
| Homologation / ASIL / 21434 | Design-intent packs — **not** certificates |

---

## 5. Recommended deal

**Exclusive automotive FOU + buyout option**, source escrow at `v1.3.*`, optional earnout on G1/G2/patent gates. See [TERM-SHEET.md](docs/acquisition/TERM-SHEET.md) and [DEAL-STRUCTURES.md](docs/acquisition/DEAL-STRUCTURES.md).

---

## 6. Verify before lunch

```bash
python -m pip install -e "./packages/physics-engine[dev]"
python -m pytest packages/physics-engine/tests -q
python -m svie_physics.acquisition_suite
npm install && npm run dev --workspace=packages/web-portal
# open /acquisition · /pitch · /hmi
```

---

## 7. Version stamp

| Field | Value |
|-------|-------|
| Package version | **1.3.0** |
| Portal | `@svie/web-portal@1.3.0` |
| Physics | `svie-physics==1.3.0` |
| Acquisition doc | this file |

See [`CHANGELOG.md`](CHANGELOG.md).
