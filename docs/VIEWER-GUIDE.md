# Viewer Guide — 15 Minutes to Conviction

For executives, BD, and engineers opening this package for the first time.

---

## Path A — Non-technical (8 minutes)

1. Skim [`EXECUTIVE-BRIEF.md`](acquisition/EXECUTIVE-BRIEF.md) (1 min)  
2. Skim [`VALUE-THESIS.md`](acquisition/VALUE-THESIS.md) (2 min)  
3. Open the portal → **`/pitch`** then **`/demo`** (4 min)  
4. Glance at **`/diligence`** checklist (1 min)  

You should leave able to say: *what it is, what’s proven in software, what’s not hardware yet, and which six modules you might buy.*

## Path B — Technical reviewer (15 minutes)

```bash
python -m pip install -e "./packages/physics-engine[dev]"
python -m pytest packages/physics-engine/tests -q
python -m svie_physics.demo
python -m svie_physics.inventory
npm install
npm run dev:api          # terminal A
npm run dev:portal       # terminal B
```

Then open:

| URL | Why |
|-----|-----|
| `/demo` | Live walkthrough metrics |
| `/calculators` | Interrogate WOT / HEX / AXIOM |
| `/specs` | YAML SoT browser |
| `/diligence` | Inventory + checklist |
| `/package` | Licensing modules |

## Path C — Counsel / IP (20 minutes)

1. [`claim-charts.md`](claim-charts.md)  
2. [`IP-INVENTORY.md`](acquisition/IP-INVENTORY.md)  
3. [`RISK-REGISTER.md`](acquisition/RISK-REGISTER.md) R07 (FTO)  
4. Map claim sets → `specs/` via evidence tables  

## What “good” looks like after viewing

- [ ] You can name the six licensing packages  
- [ ] You know ṁ_fuel 28.28 g/s and AXIOM RBI 0 are **test-locked**  
- [ ] You know BTE 48–52% is a **target**, not a measurement  
- [ ] You know the next paid work is **hardware G1**, not more slides  

Master index: [`INDEX.md`](INDEX.md) · Commercial: [`../Acquisition.md`](../Acquisition.md)
