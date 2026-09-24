# SVIE Term Sheet (Indicative)

**Release:** 1.3.0  
**Status:** Indicative commercial outline — **not** an offer, LOI, or binding agreement.  
**Counsel required** before circulation outside NDA.

---

## Parties

| Role | Placeholder |
|------|-------------|
| Seller / Licensor | SVIE Advanced Engineering (update legal entity) |
| Buyer / Licensee | [OEM / Tier-1 / strategic acquirer] |

## Preferred structure

**Exclusive automotive field-of-use license + buyout option** (see `specs/deal_structure.yaml`).

| Term | Indicative |
|------|------------|
| Field of use | Automotive propulsion (ICE / H₂ ICE / hybrid) |
| Exclusivity | Automotive FOU exclusive; non-auto reserved or separately priced |
| Territory | Worldwide unless carved |
| Term | 10 years + renewal / buyout |
| Source escrow | Required at close (`v1.3.*` golden tag) |
| Earnout | Optional gates G1 spray · G2 single-cyl · patent filings |

## Price architecture (framing only)

1. **Upfront** — license / asset fee for the monorepo + brand + diligence pack  
2. **Modules** — optional uplift for packages beyond core (DESIGN, COMPLIANCE, ACQUIRE already in 1.3 base map)  
3. **Earnout** — payable on hardware / IP milestones, not on unverified BTE claims  

Exact numbers are commercial and live outside this repo.

## Closing deliverables

- Tagged archive `v1.3.0` (or negotiated patch)  
- Passing `pytest` + `svie_physics.acquisition_suite` gates  
- Data-room index complete (`specs/data_room_index.yaml`)  
- Assignment / license instruments (counsel drafts)  
- Brand assets + NOTICE / LICENSE transfer schedule  

## Explicit exclusions at close

Dyno certificates, EPA/WLTP homologation, production tooling, firm supplier quotes, third-party trademarks.

## Next step

NDA → data room (tier `nda_full`) → 2-day technical walkthrough → mark-up of this sheet.
