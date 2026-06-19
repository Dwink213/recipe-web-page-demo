# Kata brief — rules and where they are enforced

The Kata brief (`_intake/00_kata-brief.md`) and build spec (`_intake/01_build-spec.md`)
are the contract. This file lists each rule the build must satisfy and the layer
that **enforces** it — not just documents it. "Enforced" means code fails, blocks,
or refuses when the rule is violated.

| # | Rule (from the brief) | Enforced by |
|---|---|---|
| R1 | A page lists all recipes from the back end; clicking one routes to its page. | `index.html` → `recipe.html?id=` |
| R2 | The recipe page lists ingredients; no interactive elements required there. | `recipe.html` (display only) |
| R3 | Input is untrusted: ingredient strings are parsed, never silently "fixed"; the raw string is preserved. | `js/parse.js` (carries `raw`, never throws) |
| R4 | Recipe units ≠ procurement units; conversion modeled once, keyed by name. | `js/convert.js` + `data/procurement.json` |
| R5 | Countables (eggs, tortillas, peppers) are ordered by the each, rounded up — no fractional units. | `convertToBuyUnit` (`ceil` for `each`) |
| R6 | Illustrative prices/conversions are labeled everywhere; never presented as real catalog data. | `priceNote: "illustrative"` rendered in UI; **CI fails** if any priced entry isn't labeled |
| R7 | The bundled `salt and pepper` line is ambiguous: split, even-weight placeholder, flagged, gated behind approval; never committed as fact. | `convert.js` split + `js/rules.js` blocker + `order.html` editor; **CI fails** if the bundle/targets are missing |
| R8 | Nothing is "ordered" until a human approves. A flagged line must be resolved first. | `js/rules.js` `canApprove()` gates `order.html`'s Approve button |
| R9 | A changed order cannot inherit a stale approval. | `order.html` resets resolution state on any servings change |
| R10 | Recipe/price changes are reviewable: every data change flows through a PR and a checked gate. | `scripts/ci_checks.py` `check_data_meets_kata_rules()` runs in `.github/workflows/ci.yml` |

## The enforcement seam

`js/rules.js` classifies every flag as `blocker` or `info`. A `blocker` makes
`canApprove()` return `false`, so the order page's approved state is **unreachable**
until a human resolves the line (accept a salt/pepper split, exclude an unmappable
item, or explicitly acknowledge it). This is the difference between a flag that
*describes* doubt and a rule that *prevents* committing through it.

The same data rules (R6, R7, and recipe shape) are mirrored in Python so they hold
at the repo boundary too: a PR that breaks them fails CI before it can deploy.
