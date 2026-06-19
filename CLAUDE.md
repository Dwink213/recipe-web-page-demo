# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static, multi-page recipe app (vanilla HTML + ES-module JavaScript, no build step) that deploys to Azure Static Web Apps on every push to `main`. There is no framework, package manager, bundler, or server. **The repo is the data store**: JSON files in `/data` are fetched at runtime with `fetch()` and all logic runs client-side. Built from the kata spec in `_intake/01_build-spec.md` (the authoritative build instruction; read it with `_intake/00_kata-brief.md` before changing app behavior).

## Commands

- Run the validation gate locally before pushing: `python3 scripts/ci_checks.py` (exits 1 on failure, prints each error). Same script CI runs; it catches failures in milliseconds. There is no JS test framework; this script *is* the test suite.
- **Preview must be over HTTP, not `file://`** — the pages `fetch()` the JSON, which fails on `file://`. Use `swa start` or VS Code Live Server. Opening an `.html` by double-clicking will show empty pages.

## Architecture

Four pages at the repo root, two ES modules in `/js`, three data files in `/data`. Pages link to each other with normal `<a>` and query strings (`recipe.html?id=chicken-stir-fry`) — no SPA router, no client-side routing.

Pages — clicking a recipe goes **straight to its ingredients** (no middle page); the advanced pages are linked from there, not required:
- `index.html` — recipe list (the graded deliverable). Fetches `data/recipes.json`, links each title straight to `ingredients.html?id=`.
- `ingredients.html` — "the page for the recipe": a **plain list** of the recipe's ingredients (the raw strings), title, and yield, plus links to the advanced pages. Deliberately simple — no data-quality flags, no parser artifacts. **No interactive elements** in the listing (no button/input/form/handler) — that constraint is load-bearing; keep it display-only (plain nav `<a>`s are fine). There is intentionally no separate recipe-hub page.
- `order.html` — (advanced) scale to target servings, convert to procurement units, illustrative pricing, and a simple pending→**approved** gate (re-scaling resets it). Ambiguous lines — the `salt and pepper` split (shown as two lines with a caption) and any flagged line — get an editable grams input that live-reprices that line and the total in place (class `.qty-edit` + `data-idx`, updated without a full re-render so the input keeps focus). Don't reintroduce whitespace `id`s or per-keystroke re-render here — both were bugs.
- `data.html` — (advanced) pretty-prints both JSON files and renders `data/conversion-logic.md` via a tiny inline markdown function (zero CDN dependencies).

All pages share one stylesheet, **`styles.css`** (static asset, fetched once). Keep each page's `<head>` to a `<title>` + `<link rel="stylesheet" href="styles.css">` — don't re-inline per-page `<style>` blocks. Page-width variant: `<main class="wide">` (used by `data.html`).

Modules (`/js`, faithful to the pseudocode in `_intake/01_build-spec.md`):
- `parse.js` — `parseIngredient(raw)` turns `"100g large eggs"` into `{raw, amount, unit, name, note, flags}`. Always preserves `raw`; never throws.
- `convert.js` — `buildOrder(recipe, targetServings, procurement)` scales, joins to procurement by normalized name, and builds order lines. `convertToBuyUnit` rounds `each` up (no fractional eggs), `ml` to 0.1, `g` as-is. The bundled `salt and pepper` line splits into two even-by-weight lines tagged `bundle` so `order.html` can caption them.

**The brief is the contract.** When changing app behavior, treat `_intake/00_kata-brief.md` + `_intake/01_build-spec.md` as binding and keep `docs/kata-rules.md` in sync. The brief's *data* rules (illustrative pricing, bundled salt/pepper modeling, recipe shape) are enforced at the repo boundary by `scripts/ci_checks.py` (`check_data_meets_kata_rules`), which fails a non-compliant PR before deploy.

**Data join contract:** ingredients join to `procurement.json` by the lowercased, trimmed `name`. A missing match adds a `"no procurement mapping, review"` flag — it never throws. Flags are *additive* across `parse.js` and `convert.js`; they mark unresolved ambiguity, not every transformation.

Deploy/CI:
- `.github/workflows/deploy.yml` — deploys to Azure SWA. **Plain static files only** (`skip_app_build: true`, `app_location: "/"`, `output_location: "/"`). Gives PRs a staging environment, torn down on PR close.
- `.github/workflows/ci.yml` + `scripts/ci_checks.py` — validation gate. On PRs it blocks merge; on direct pushes to `main` it runs alongside deploy as a loud detector.

The only link between GitHub and Azure is the `AZURE_STATIC_WEB_APPS_API_TOKEN` repo secret.

## Data-change discipline (the architecture's point)

Recipe and price changes flow through `recipes.json` / `procurement.json` via PR — every change is reviewed before it ships. Two non-negotiables from the spec:
- **Never edit the *meaning* of an ingredient line in `recipes.json`** — clean JSON syntax only. The parser does the structuring at runtime so the raw source stays auditable.
- **Illustrative prices/conversions must be labeled everywhere; the salt/pepper even-split is a flagged placeholder, never committed as fact.** Nothing reads as "ordered" until the approval gate flips.

`_intake/` holds the kata source-of-truth docs (brief + build spec). The app's live data is `/data`, not `_intake`.

## Things that will bite you

- **Don't move or rename `index.html`.** Moving it off the root breaks both the deploy (serves a blank site) and the CI gate.
- **Switching to a framework with a build step (React/Vue/Vite/Next/Astro) requires editing `deploy.yml`:** set `skip_app_build: false`, point `app_location` at the source dir, and `output_location` at the build output dir. Otherwise raw source deploys instead of the built bundle.
- **`check_no_leaked_secrets()` in `ci_checks.py` scans committed files** for `api_key=`/`secret=`/`password=` and the SWA token shape. Use repo secrets, never inline literals.
- **Adding SPA client-side routing?** Add `staticwebapp.config.json` at the root with a navigation fallback to `/index.html`, or deep links 404.
- **`check_recipe_quality()` in `ci_checks.py` is an intentional no-op with a TODO** — it's the designated spot to assert what a valid recipe page must contain (e.g. an `<h1>`, an ingredients section). Implement there if you want content gating.

## Azure environment

- Resource group: `rg-recipe-web-page-demo` · Static Web App: `recipe-web-page-demo` (Free SKU, East US 2) · Subscription: Personal Portfolio
