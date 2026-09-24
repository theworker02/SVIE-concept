# Closing Checklist

**Release:** 1.3.0 · Target: production-ready **acquisition package** close

---

## Technical gates (must be green)

- [ ] `python -m pytest packages/physics-engine/tests -q` — all pass  
- [ ] `python -m svie_physics.demo` — exits 0  
- [ ] `python -m svie_physics.inventory` — counts meet gates  
- [ ] `python -m svie_physics.validate` — all checks ok  
- [ ] `python -m svie_physics.acquisition_suite` — `production_ready_acquisition: true`  
- [ ] `python -m svie_physics.compliance` — compliance pack emits  
- [ ] Portal `npm run build` — `/acquisition` `/hmi` `/pitch` present  
- [ ] Git tag `v1.3.0` (or negotiated) matches `VERSION`

## Commercial / counsel gates

- [ ] NDA executed  
- [ ] Term sheet mark-up agreed (indicative → binding instruments)  
- [ ] IP assignment / license schedules attached  
- [ ] Source escrow instructions signed  
- [ ] Earnout schedule (if any) referenced to G1–G3  
- [ ] Brand transfer schedule (SVG/PNG + MEDIA-KIT)  
- [ ] Export / security acknowledgment (`SECURITY.md`)

## Honesty confirmation (buyer initials)

- [ ] Buyer acknowledges **hardware TRL-3** — no dyno certificates in this close  
- [ ] Buyer acknowledges CarPlay Ultra / Apple marks are third-party; integration is design policy  
- [ ] Buyer acknowledges homologation / ISO packs are **design intent**, not certificates

## Day-0 handoff

- [ ] Deliver tagged archive + checksum  
- [ ] Walk `/acquisition` scorecard with buyer eng lead  
- [ ] Schedule OEM-HANDOFF 30-day plan kickoff
