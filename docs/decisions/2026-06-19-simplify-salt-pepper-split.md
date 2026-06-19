**Decision:** Replace the interactive salt/pepper split editor and per-line approval-blocking with a simple display: `convert.js` splits the bundled line into two even-by-weight lines (salt, pepper), each priced on its own, and `order.html` shows them with a caption explaining the split. The order keeps a single pending→approved gate. `js/rules.js` (flag-severity / `canApprove` blocking) was deleted as no longer used.

**Why:** User direction: "I can't change pepper, so let's just simplify this. For that one, just put salt and amount, and then pepper, and then you can note this was split since salt and pepper cost very dramatically [differently] and the kitchen does not treat them as equal." The interactive editor was buggy (whitespace-id lookup, then input not committing) and added fragile DOM wiring to make a point a one-line note makes better.

**Alternatives considered:** Keep fixing the inline editor (rejected: repeated breakage, and the interaction wasn't wanted). Keep `rules.js` for hypothetical unmapped lines (rejected: no current consumer — dead code; the Python CI gate still enforces the data rules at the repo boundary).

**Supersedes:** the approval-blocking parts of `2026-06-19-enforce-kata-brief-as-rules.md` (the order-level Approve gate and the Python CI data gate remain).

**Date:** 2026-06-19
