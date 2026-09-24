# Production-Ready Acquisition Posture

**Release:** 1.3.0  
**Claim:** The **acquisition package** is production-ready. The **powertrain hardware** remains TRL-3.

---

## What “production-ready” means here

| Ready | Not yet ready |
|-------|----------------|
| Reproducible physics + golden tests | Dyno certificates |
| Diligence library + data room | EPA / WLTP / RDE approvals |
| Modular licensing map | Firm Tier-1 quotes |
| Deal structures + term sheet outline | Binding SPA without counsel |
| Design / HMI / compliance *paths* | ASIL / 21434 certificates |
| Portal walkthrough for OEM teams | Fleet OTA in production vehicles |

## Scorecard

Weighted dimensions live in `specs/acquisition_readiness.yaml` and are computed by:

```bash
python -m svie_physics.acquisition_suite
```

Gate: weighted score ≥ 85 and inventory/test/route minima.

## Buyer message

You can **close on the IP monorepo** with the same rigor you close on software diligence: clone, verify, interrogate, escrow. Hardware programs start at G1 after close — see [HARDWARE-ROADMAP.md](HARDWARE-ROADMAP.md).
