**Decision:** Clicking a recipe on the index goes **straight to its ingredients page** — no intermediate recipe-hub page. `ingredients.html` is "the page for the recipe" and also lists the ingredients; the advanced order/data links live on it. `recipe.html` was deleted.

**Why:** User direction: "when we click on the index, any of the recipes, it should go straight to the ingredients, no middle page there" (and "the advanced for ordering link is not there"). Reads the brief's two bullets as one destination — "the page for the recipe" *is* the ingredients listing — which is the simpler, intended flow. The advanced ordering link was only reachable from the deleted hub, so it moved onto the ingredients page.

**Supersedes:** `2026-06-19-split-recipe-and-ingredients-pages.md` (the two-page split).

**Alternatives considered:** Keep `recipe.html` as a thin hub between index and ingredients (rejected: that's the "middle page" the user does not want).

**Date:** 2026-06-19
