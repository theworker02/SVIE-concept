# Virtual Data Room Index

**Release:** 1.3.0 · **SoT:** [`specs/data_room_index.yaml`](../../specs/data_room_index.yaml)  
**Portal:** `/acquisition`

---

## Access tiers

| Tier | Audience | Contents |
|------|----------|----------|
| `teaser` | Pre-NDA | EXECUTIVE-BRIEF, VIEWER-GUIDE, public README |
| `nda_full` | Diligence team | Full monorepo + design renders + compliance packs |
| `clean_team_counsel` | Counsel | LICENSE, NOTICE, claim charts, IP inventory, term sheet |

## Folder map

| ID | Name |
|----|------|
| A00 | Executive & deal |
| A01 | Value & competition |
| A02 | IP & counsel |
| B00 | Physics & specs |
| B01 | Technical docs |
| C00 | Vehicle design & HMI |
| D00 | Compliance & supply |
| E00 | Portal & demo |

Machine enumeration:

```bash
python -m svie_physics.acquisition_suite
```

## Hygiene

- No secrets / credentials in-repo  
- Export-control awareness in `SECURITY.md`  
- Honda® and other marks used only comparatively
