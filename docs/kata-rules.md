# Kata brief — rules and where they are enforced

The Kata brief (`_intake/00_kata-brief.md`) and build spec (`_intake/01_build-spec.md`)
are the contract. This file lists each rule the build must satisfy and the layer
that **enforces** it — not just documents it. "Enforced" means code fails, blocks,
or refuses when the rule is violated.

| # | Rule (from the brief) | Enforced by |
|---|---|---|
| R1 | A page lists all recipes from the back end; clicking one goes straight to "the page for the recipe". | `index.html` → `ingredients.html?id=` (no middle page) |
| R2 | That page lists the ingredients used in the recipe; **no interactive elements** in the listing. | `ingredients.html` — display only (no button/input/form/handler) |
| R3 | Input is untrusted: ingredient strings are parsed, never silently "fixed"; the raw string is preserved. | `js/parse.js` (carries `raw`, never throws) |
| R4 | Recipe units ≠ procurement units; conversion modeled once, keyed by name. | `js/convert.js` + `data/procurement.json` |
| R5 | Countables (eggs, tortillas, peppers) are ordered by the each, rounded up — no fractional units. | `convertToBuyUnit` (`ceil` for `each`) |
| R6 | Illustrative prices/conversions are labeled everywhere; never presented as real catalog data. | `priceNote: "illustrative"` rendered in UI; **CI fails** if any priced entry isn't labeled |
| R7 | The bundled `salt and pepper` line is split into two even-by-weight lines, priced separately, shown with a note on why (they cost very differently); never merged as one SKU. | `convert.js` split into `salt`/`pepper` lines + `order.html` caption; **CI fails** if the bundle/targets are missing |
| R8 | Nothing is "ordered" until a human approves. | `order.html` pending→approved gate (Approve button) |
| R9 | A changed order cannot inherit a stale approval. | `order.html` resets `approved` on any servings change |
| R10 | Recipe/price changes are reviewable: every data change flows through a PR and a checked gate. | `scripts/ci_checks.py` `check_data_meets_kata_rules()` runs in `.github/workflows/ci.yml` |

## Where the rules hold at the repo boundary

The brief's *data* rules (R6 illustrative labeling, R7 bundled salt/pepper modeling,
and recipe shape) are mirrored in Python — `scripts/ci_checks.py`
`check_data_meets_kata_rules()` — so a PR that breaks them fails CI before it can
deploy. The order page is intentionally simple: it scales, converts, prices, shows
the salt/pepper split with an explanatory note, and requires one human Approve
before the order reads as placed.
