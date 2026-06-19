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
