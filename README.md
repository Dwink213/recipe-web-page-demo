# recipe-web-page-demo

A small static web app — a recipe list, an ingredients page, and two advanced
pages (order builder, self-documenting data view) — deployed to Azure Static Web
Apps via CI/CD on every push to `main`. Vanilla HTML + ES-module JavaScript,
**no build step**: the repo is the data store and all logic runs client-side.

Built for an interview kata; the brief and build spec live in `_intake/`
(gitignored — interview material), distilled into `docs/kata-rules.md`.

## Pages and flow

Clicking a recipe goes straight to its ingredients; the advanced pages are linked
from there.

| Page | What it is |
|---|---|
| `index.html` | Lists the recipes from the back end (`data/recipes.json`). Click one → its ingredients. |
| `ingredients.html` | "The page for the recipe" — a plain list of its ingredients. No interactive elements. |
| `order.html` | (advanced) Scales a recipe to a serving count, converts to procurement units, prices (illustrative), with editable ambiguous lines and a human **Approve** step. |
| `data.html` | (advanced) Pretty-prints the JSON the app runs on and renders `data/conversion-logic.md` — machine- and human-readable, side by side. |

## How it's wired

| Piece | What it does |
|---|---|
| `data/*.json` | The back end: `recipes.json` (cleaned meal plan) + `procurement.json` (unit conversions, illustrative prices). Fetched at runtime. |
| `data/conversion-logic.md` | Plain-English logic, rendered into `data.html`. Must match the code. |
| `js/parse.js` | Parses raw ingredient strings into `{amount, unit, name, note, flags}`; preserves the raw string. |
| `js/convert.js` | Scales, joins to procurement by name, and builds priced order lines. |
| `styles.css` | One shared stylesheet for every page (static asset, fetched once). |
| `.github/workflows/deploy.yml` | Deploys to Azure SWA on push to `main`; PRs get a staging environment, closed on PR close. |
| `.github/workflows/ci.yml` | Validation gate — runs `scripts/ci_checks.py` on pushes and PRs. |
| `scripts/ci_checks.py` | Checks `index.html` exists and isn't empty, scans for leaked secrets, and enforces the kata data rules (`check_data_meets_kata_rules`). |
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

The deploy loop is simple: **edit, commit, push to `main`, live in ~1 minute.**
Watch-outs:

1. **Keep `index.html` at the repo root.** Both the SWA (`output_location: "/"`)
   and the CI gate expect it there. Moving it fails CI and/or serves a blank site.
2. **Preview over HTTP, not `file://`.** Pages `fetch()` the JSON, which fails on
   `file://`. Use `swa start` or VS Code Live Server.
3. **Plain static files only.** `deploy.yml` has `skip_app_build: true`. Moving to
   a framework with a build step means updating `app_location` / `output_location`
   / `skip_app_build` in `deploy.yml`, or raw source deploys instead of the bundle.
4. **Don't commit secrets.** The CI gate scans committed files for `api_key=` /
   `secret=` / `password=` literals and fails on a hit. Use repo secrets.
5. **Keep docs in sync with behavior.** `data/conversion-logic.md` renders on the
   live site, and `README.md` / `CLAUDE.md` / `docs/kata-rules.md` describe the
   app — when you change behavior, update them in the same change. See
   `docs/STYLE_GUIDE.md`.
6. **The CI gate enforces the kata data rules** (`check_data_meets_kata_rules` in
   `scripts/ci_checks.py`): recipe shape, illustrative pricing labels, and the
   bundled salt/pepper modeling. A non-compliant data change fails the build.
