# Deal Structures

**Release:** 1.3.0 · **SoT:** [`specs/deal_structure.yaml`](../../specs/deal_structure.yaml)

---

## Preferred: Exclusive FOU + buyout option

Best fit when the buyer wants speed and staged capital. License the monorepo exclusively for automotive propulsion; retain a negotiated option to purchase remaining rights after hardware gates.

**Why preferred:** aligns with modular packages; preserves earnout leverage; escrow protects continuity.

## Alternative A: Full asset purchase

Cleaner for strategic buyers who want brand + IP + code outright. Longer counsel cycle; higher upfront.

## Alternative B: Staged modular license

Buyer takes `SFV-CORE` then `AXIOM-DRIVE` then ops/design modules. Fastest first close; less exclusivity leverage.

## Escrow & earnout

| Control | Rule |
|---------|------|
| Escrow | Source + specs + golden tests at close |
| Tag | `v1.3.*` reproducible |
| Earnout G1 | Spray-rig / HEX evidence |
| Earnout G2 | Single-cylinder combustion |
| Earnout G3 | Patent filings from claim charts |

## Honesty clause

Hardware TRL remains **3** at package close. Valuation should price **diligence reproducibility**, not dyno certificates.
