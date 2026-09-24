# SVIE Diligence FAQ

## Product & readiness

**Q: Is this dyno-proven?**  
A: No. In-repo thermo models are TRL-3 (analytical + golden-locked). Hardware is TRL-1–2 concept. See TRL roadmap spec and [HARDWARE-ROADMAP.md](HARDWARE-ROADMAP.md).

**Q: What can we verify tomorrow morning?**  
A: Clone → `pip install -e "./packages/physics-engine[dev]"` → `pytest` → `python -m svie_physics.demo` → start API + portal → `/demo` and `/calculators`.

**Q: Are the 48–52% BTE numbers measured?**  
A: No. They are design *targets*. White paper and README both state this explicitly.

**Q: Why two V8 concepts (5.2 L and 3.57 L)?**  
A: 5.2 L is the gasoline SFV WOT golden baseline. 3.57 L V8-HR is a Honda-evolved high-RPM H₂ DI architecture. They share brand and monorepo tooling but are separate YAML families.

## IP & commercial

**Q: What IP is assignable?**  
A: Copyrights in code/docs/specs/brand created for this package; know-how embodied in models; candidate trademarks. Patents require separate filing strategy — none asserted as granted here.

**Q: Suggested deal structure?**  
A: Exclusive automotive field-of-use license with buyout option, or full asset purchase. See [Acquisition.md](../../Acquisition.md).

**Q: Can we license only AXIOM / anti-CVT?**  
A: Yes — licensing packages are defined in inventory (`AXIOM-DRIVE`, `SFV-CORE`, etc.). Pricing is commercial negotiation.

**Q: Is Honda affiliated?**  
A: No. Honda names appear only for public comparative diligence.

## Technical

**Q: Source of truth for numbers?**  
A: `specs/*.yaml` + pytest. Docs that disagree with YAML should be treated as stale.

**Q: How do we extend a model?**  
A: Edit YAML → update module → add/adjust golden test → re-run portal calculator. Handoff guide: [OEM-HANDOFF.md](OEM-HANDOFF.md).

**Q: Can the portal run without the API?**  
A: Calculators need FastAPI on `:8000`. Static pages (`/`, `/demo` narrative, `/architecture`) render without it; live metric panels need the API.

**Q: Export control?**  
A: Treat as dual-use engineering data under your jurisdiction’s rules. See [SECURITY.md](../../SECURITY.md). Buyer compliance team owns classification.
