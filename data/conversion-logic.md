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

## 5. Salt and pepper: ambiguous, so it's suggested, not decided

The line "3g Salt and pepper (to taste)" is two distinct SKUs sharing one weight. You cannot order "3g of salt and pepper" as a single item, and the recipe doesn't say how to split it. The catalog reality is that salt and pepper are separate purchases at very different price points, and pepper costs many times what salt does, so a wrong split is a real money error.

The system does not guess silently. When this line is scaled, it splits into two separate order lines, salt and pepper, with an even split by weight as a neutral placeholder. Both lines are flagged and marked NEEDS APPROVAL. The even split is a starting point that forces a human to look, not a recommendation. Nothing is ordered until a person confirms or corrects the split.

## 6. Nothing commits without human approval

Every order on Page 2 renders in a pending state. Suggested and flagged lines are visibly marked. A single approval step is required before anything is treated as ordered. For facility procurement, where a wrong quantity costs real money, the system's job is to propose and surface doubt, and the human's job is to commit. The system never commits a number it guessed.

---

### Say-out-loud summary (the 20-second version)

"I treat the input as untrusted and parse it before I compute. Recipe units aren't procurement units, so I model a conversion layer in one place. Scaling falls out of that for free. Where a line is ambiguous, like salt and pepper bundled together, I split it, pre-fill a neutral placeholder, flag it, and require human approval before it can be ordered. The system suggests and surfaces doubt. It never silently guesses a value into an order."
