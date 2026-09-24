# SVIE Portal — Viewer & Diligence Surface

Next.js 15 client over the SVIE physics FastAPI. Does **not** re-implement thermodynamics.

## Routes

| Path | Purpose |
|------|---------|
| `/` | Brand overview + audience paths |
| `/pitch` | Acquisition pitch for executives / BD |
| `/demo` | Guided live walkthrough |
| `/diligence` | Inventory, checklist, licensing modules |
| `/package` | Six licensing packages |
| `/calculators` | Interactive physics calculators |
| `/specs` | YAML browser (filter by package) |
| `/architecture` | System diagrams |

## Run

```bash
# From monorepo root — API first
npm run dev:api

# Then portal
npm run dev:portal
```

- Portal: http://localhost:3000  
- API health badge in the header turns green when `:8000` is up  

Set `NEXT_PUBLIC_SVIE_API_URL` if the API is not on `http://127.0.0.1:8000`.

## First-time viewers

Follow [`docs/VIEWER-GUIDE.md`](../../docs/VIEWER-GUIDE.md) — Path A for non-technical (8 min).
