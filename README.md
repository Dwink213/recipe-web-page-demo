# recipe-web-page-demo

A demonstration of a rapid web page prototype using CI/CD and Azure Static Web Apps.

A single static HTML page (`index.html`) deploys to Azure Static Web Apps on every
push to `main`. Edit the HTML, push, and the change is live in about a minute — no
build step.

## How it works

| Piece | What it does |
|---|---|
| `index.html` | The site. Served from repo root (`app_location: "/"`). |
| `.github/workflows/deploy.yml` | Deploys to Azure SWA on push to `main`; gives PRs a staging environment and closes it on PR close. |
| `.github/workflows/ci.yml` | Validation gate — runs `scripts/ci_checks.py` on pushes and PRs. |
| `scripts/ci_checks.py` | Checks the page exists, isn't empty, and no secrets leaked. |
| `AZURE_STATIC_WEB_APPS_API_TOKEN` (repo secret) | The only link between GitHub and Azure — the SWA deployment token. |

## Azure environment

- **Resource group:** `rg-recipe-web-page-demo` (dedicated)
- **Static Web App:** `recipe-web-page-demo` (Free SKU, East US 2)
- **Subscription:** Personal Portfolio

## Run the validation locally

```
python3 scripts/ci_checks.py
```

## Working on the site — read before you build

The deploy loop is simple: **edit, commit, push to `main`, live in ~1 minute.** A
few things to watch out for:

1. **Keep `index.html` at the repo root.** Both the SWA (`output_location: "/"`)
   and the CI gate (`scripts/ci_checks.py`) expect it there. Moving or renaming it
   will fail CI and/or serve a blank site.

2. **This is configured for plain static files only.** `.github/workflows/deploy.yml`
   has `skip_app_build: true`. If you move to a framework with a build step
   (React, Vue, Vite, Next, Astro, etc.), you MUST update `deploy.yml`:
   - set `skip_app_build: false`
   - set `app_location` to your source dir (e.g. `/` or `/src`)
   - set `output_location` to the build output dir (e.g. `dist` or `build`)
   Otherwise your raw source deploys instead of the built bundle.

3. **Don't commit secrets.** The CI gate scans committed files for `api_key=`,
   `secret=`, `password=` style literals and fails on a hit. Use GitHub repo
   secrets (the SWA token is already stored as `AZURE_STATIC_WEB_APPS_API_TOKEN`).

4. **Run the gate before pushing:** `python3 scripts/ci_checks.py` catches failures
   in milliseconds instead of waiting on a CI runner.

5. **Adding client-side routing (a SPA)?** Add a `staticwebapp.config.json` at the
   root with a navigation fallback to `/index.html`, or deep links will 404.

6. **`scripts/ci_checks.py` has a `check_recipe_quality()` no-op** with a TODO —
   that's where you decide what a valid page must contain (an `<h1>`, an
   ingredients section, etc.). Optional, but it's the spot meant for your rules.

