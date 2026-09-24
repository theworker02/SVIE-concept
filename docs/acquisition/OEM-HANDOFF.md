# OEM Engineering Handoff

Post-close guide for integrating SVIE into an OEM / Tier-1 toolchain.

---

## 1. Day-0 environment

| Tool | Version |
|------|---------|
| Python | ≥ 3.11 |
| Node.js | ≥ 20 |
| npm | workspaces (pnpm optional) |

```bash
python -m pip install -e "./packages/physics-engine[dev]"
python -m pytest packages/physics-engine/tests -v
npm install
npm run demo
npm run dev:api    # :8000
npm run dev:portal # :3000
```

## 2. Mental model

```text
YAML specs  →  Python models  →  pytest golden  →  FastAPI  →  Portal
     ↑________________________________docs / claim charts____________|
```

Never change a published golden number without updating the YAML `golden:` block and the owning doc section in the same PR.

## 3. Adding a subsystem (checklist)

1. Create `specs/<name>.yaml` with `meta`, inputs, and `golden` where applicable  
2. Add `packages/physics-engine/src/svie_physics/<module>.py` + CLI `main`  
3. Register entry point in `pyproject.toml`  
4. Add `tests/test_<area>.py` locking golden  
5. Expose route in `api.py`  
6. Wire calculator tab or diligence card in portal  
7. Document in `docs/` + `docs/INDEX.md` + `specs/CATALOG.md`  
8. Bump `CHANGELOG.md` / `VERSION`

## 4. Suggested integration targets (OEM)

| OEM system | SVIE hook |
|------------|-----------|
| GT-POWER / WAVE | Export SFV boundary conditions from YAML |
| MATLAB/Simulink | Wrap FastAPI or call Python modules via pybind/COM |
| DoE / dyno cell | Treat golden vectors as pre-test acceptance gates |
| PLM | Attach YAML SHA to part revisions |
| Functional safety | Map SENTINEL sensing to HARA / FSC |

## 5. People map (roles to assign)

| Role | Owns |
|------|------|
| Physics owner | Models + golden tests |
| Spec librarian | YAML SoT integrity |
| Portal owner | Next.js + API contract |
| IP liaison | Claim charts vs filings |
| Hardware lead | TRL-4+ roadmap |

## 6. First 30 / 60 / 90 days

| Window | Outcome |
|--------|---------|
| 0–30 | Repo green CI; staff trained on demo + inventory; licensing package selection |
| 31–60 | Injector/HEX spray-rig SOW; DEVA actuator bench plan; AXIOM ratio freeze |
| 61–90 | Single-cylinder SFV or H₂ DI kickoff; patent landscape complete |

Detail: [HARDWARE-ROADMAP.md](HARDWARE-ROADMAP.md).
