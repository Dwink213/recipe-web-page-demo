# 02 — Conversion Logic (renders into Page 3)

This file is read by humans and rendered into the app's Page 3. It explains, in plain language, every decision the system makes between a recipe line and a procurement order. If you can read this page, you can audit the system.

---

## 1. We don't trust the input until we've read it

The meal plan arrived as malformed JSON with unstructured ingredient strings. Before computing anything, we clean the JSON syntax (only the syntax, never the meaning) and parse each ingredient string into a structured object: amount, unit, name, an optional chef note, and any data-quality flags. We keep the original raw string on every line so any parsed value can be checked against what was actually written.

## 2. Recipe units are not procurement units

A recipe says "100g large eggs." You do not buy eggs by the gram. You buy them by the each. So the system holds a separate procurement table, keyed by ingredient name, that maps recipe weight to how the item is actually purchased. Eggs convert at roughly 50g each, so 100g becomes 2 eggs. Olive oil converts by density to millilitres. Bulk items like oats and chicken stay in weight. This conversion layer lives in one place, not copied into each recipe, so it can't drift. Olive oil appears in two recipes and is defined once.

## 3. Scaling is trivial once conversion is modeled

To scale a recipe, multiply every ingredient by `targetServings / recipe.yield`, then run each scaled weight through the procurement conversion. Countable items round up to whole units, because you can't order a fraction of an egg or a tortilla. The hard part was never the multiplication. It was noticing that the units have to change.

## 4. Some values are illustrative, and we say so

The gram-per-unit conversions and the prices in this build are placeholders, labeled illustrative everywhere they appear. Real values would come from the supplier catalog. We never let a placeholder render as if it were authoritative data.

## 5. Salt and pepper: one line, two SKUs the kitchen prices differently

The line "3g Salt and pepper (to taste)" is two distinct SKUs sharing one weight. You cannot order "3g of salt and pepper" as a single item. Salt and pepper are separate purchases at very different price points — pepper costs many times what salt does — so the kitchen does not treat them as one line.

When this line is scaled, the system splits it into two separate order lines, salt and pepper, using an even split by weight as a neutral starting point. Each line is priced on its own, and either amount can be adjusted by hand on the order page. The even split is a default, not a recommendation — a caption on the order page explains why the two are separated.

## 6. Nothing counts as ordered without human approval

Every order on Page 2 renders in a pending state and is not treated as placed until a person clicks Approve; changing the serving count returns it to pending. Prices and unit conversions are illustrative and labeled as such. The system's job is to scale, convert, and show the cost of every line — including each side of the salt/pepper split — and the human's job is to review and approve.

---

### Say-out-loud summary (the 20-second version)

"I treat the input as untrusted and parse it before I compute. Recipe units aren't procurement units, so I model a conversion layer in one place, and scaling falls out of that for free. Where one line bundles two SKUs, like salt and pepper, I split it even-by-weight into two separately-priced lines you can adjust by hand, because the kitchen doesn't treat them as equal. Prices are illustrative and labeled, and nothing counts as ordered until a human approves."
