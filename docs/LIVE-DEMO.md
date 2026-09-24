# Live Demo — GitHub Pages

**Release:** 1.3.0  
**URL (after first deploy):** https://theworker02.github.io/SVIE-concept/

---

## What it is

A **static** export of the OEM portal (`packages/web-portal`) hosted on GitHub Pages. The `/demo` tour plays golden locked metrics from `public/demo/golden.json` — no Python API required on Pages.

| Route | Purpose |
|-------|---------|
| `/` | Overview |
| `/demo` | Live guided tour (autoplay) |
| `/acquisition` | Readiness desk (offline snapshot if API down) |
| `/hmi` | AETHER-OS analog mock |
| `/pitch` | Acquisition pitch |
| `/design` | Vehicle design gallery |

## Enable Pages (one-time)

1. Push this repo to GitHub as `theworker02/SVIE-concept` (or update `GITHUB_REPOSITORY` / `next.config` repo default).  
2. **Settings → Pages → Build and deployment → Source: GitHub Actions**.  
3. Push to `main`/`master` or run **Actions → Deploy GitHub Pages live demo → Run workflow**.  
4. Open the environment URL printed by the deploy job.

## Local static preview

```bash
npm ci
npm run build:pages --workspace=packages/web-portal
npx --yes serve packages/web-portal/out
```

With `GITHUB_PAGES=true` the site is built under base path `/SVIE-concept/` (repo name). Serve tools that respect that path, or open the nested folder.

## Full local stack (API live)

```bash
npm run dev:api
npm run dev:portal
# http://localhost:3000/demo
```
