> Superseded by `2026-06-19-index-links-straight-to-ingredients.md` (2026-06-19): the middle `recipe.html` hub was removed; the index now links straight to `ingredients.html`.

**Decision:** Split the single recipe-detail page into two literal pages — `recipe.html` ("the page for the recipe") and `ingredients.html` ("a page listing the ingredients used in the recipe") — so the required flow matches the Kata brief's two bullets exactly as written. The advanced pages (`order.html`, `data.html`) remain, reached via links.

**Why:** User direction: "I need one of them to work exactly as written and then the advanced ones can be there as links." The brief lists the recipe page and the ingredients page as two separate bullets; the earlier build merged them (a defensible but non-literal reading). The ingredients page is kept strictly display-only to honor "this page doesn't need to have any interactive elements."

**Alternatives considered:** Keep the merged single detail page (rejected: not literal to the brief). Hide the advanced pages entirely (rejected: user wants them present as links).

**Date:** 2026-06-19
