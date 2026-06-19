# Brutal Project Critique & Improvement Plan

_Audit date: 2026-06-19. Scope: full repo — math, breadcrumbs, simplicity, docs._

## Executive Summary

The **math is sound** and the **architecture is appropriately simple** — a static,
no-build, repo-as-data-store app. Every conversion, price, and total was verified
computationally across all three recipes and is internally consistent; all
cross-page links resolve. The project's real failure is **documentation rot**: six
iterations changed behavior, and the prose that describes that behavior was not
kept in lockstep. The single most serious issue is that **`conversion-logic.md`,
which is rendered live on Page 3 as the app's "self-documenting" view, now
describes a system that no longer exists** (it claims salt/pepper are flagged
"NEEDS APPROVAL" and gated — that machinery was deleted). A self-documenting page
that misdescribes itself is worse than no documentation, because it's presented as
authoritative to the interviewer.

Health: **code B+, documentation D.** None of the critical issues are math or
logic; all are truth-in-documentation. They are cheap to fix and high-impact.

## Critical Issues (Fix Immediately)

1. **Page 3 lies about the system.** `data/conversion-logic.md` §5/§6 and the
   say-out-loud summary describe salt/pepper as "flagged and marked NEEDS
   APPROVAL," "Suggested and flagged lines are visibly marked," and "require human
   approval before it can be ordered [for the split]." The code (`convert.js`
   line 43 passes `flags: []`; `rules.js` was deleted) no longer does any of this.
   This renders on the live site.
2. **`README.md` describes a different app.** It says "A single static HTML page
   (`index.html`)" and its file table omits `ingredients.html`, `order.html`,
   `data.html`, `/data`, `/js`, `styles.css`, `parse.js`, `convert.js`. Point #6
   references `check_recipe_quality()` — a function that was **renamed/replaced**
   by `check_data_meets_kata_rules()` and is no longer a no-op.

## Dimension Analysis

### 1. STRUCTURE

#### High Priority
- **Issue:** `CLAUDE.md` contradicts itself. The updated section correctly cites
  `check_data_meets_kata_rules()`, but the older "Things that will bite you" bullet
  (line ~54) still says `check_recipe_quality()` is "an intentional no-op with a
  TODO." One of these is false.
  - **Fix:** Delete/replace the stale bullet; point it at the real CI gate.
  - **Priority:** HIGH **Effort:** 10 min
  - **Fixer Prompt:** The no-op became a real gate three changes ago — should the
    "bite you" list now warn that the gate *fails the build* on bad data, instead
    of inviting someone to implement a TODO that's already done?

#### Medium Priority
- **Issue:** `order.html` still carries flag machinery (`baseFlags`,
  `"no procurement mapping, review"`, `"no quantity, cannot scale, review"`,
  `editable()` testing `l.flags.length`) that no current recipe can trigger — every
  ingredient maps and parses. It's defensive but it's untested surface area in a
  file you want "as simple as possible."
  - **Fix:** Either (a) keep it and add a one-line comment that it's defensive for
    future data, or (b) strip the unreachable branches. Recommend (a) — it's cheap
    insurance and the brief warned the input was dirty.
  - **Priority:** MEDIUM **Effort:** 15 min
  - **Fixer Prompt:** Do we expect future recipes with unmapped ingredients? If
    yes, keep the no-mapping path and test it with a deliberately-unmapped fixture;
    if no, delete it and let `convert.js` be the only place that reasons about flags.

### 2. USEFULNESS

#### Verified Clean
- **Math:** scaling (`targetServings / yield`), `convertToBuyUnit` (`ceil` for
  each, round-0.1 for ml, identity for g), per-line cost, and totals all recompute
  correctly. Garlic 10g→4 cloves (`ceil(10/3)`), bell pepper 250g→3 each
  (`ceil(250/120)`), olive oil 30g→32.6 ml all correct.
- **Edge handling:** unparseable strings and missing quantities are flagged, not
  thrown; missing procurement mapping is flagged, not thrown. Good.

#### Medium Priority
- **Issue:** The order-page total includes salt+pepper but a deliberately edited
  "0 g" line is allowed (clamps to ≥0). That's fine, but there's no guard that the
  salt+pepper edited grams still sum to the original line weight — a user can set
  both to 0 or both high. Per the simplification that's acceptable (illustrative),
  but it's worth a comment so nobody mistakes it for an enforced invariant.
  - **Fix:** One-line comment in `order.html` that edited amounts are independent
    and intentionally NOT reconciled to the source weight.
  - **Priority:** MEDIUM **Effort:** 5 min
  - **Fixer Prompt:** Is independent salt/pepper editing the intent (yes, per the
    last decision), or should the two re-balance against the 6 g source line?

### 3. AESTHETICS (code quality & docs)

#### Critical
- **Issue:** No file has a header comment describing what the page is and its
  inbound/outbound links; function-level comments are inconsistent (some JSDoc,
  some none). This is the documentation standard the owner asked for.
  - **Fix:** Apply `docs/STYLE_GUIDE.md` to every file: page header block (WHAT /
    DISPLAYS / DATA / IN / OUT / MODULES) and a WHAT+WHY on every function.
  - **Priority:** CRITICAL (explicit ask) **Effort:** 1.5–2 h (parallelizable)
  - **Fixer Prompt:** Apply the STYLE_GUIDE header to all four pages + both JS
    modules + the Python gate; one agent per file, then a consistency pass.

#### High Priority
- **Issue:** `convert.js` file header (lines 1–7) contradicts its own code: "surface
  every ambiguity as a flag … bundled lines split into a flagged placeholder that
  requires approval." Bundled lines are no longer flagged and nothing requires
  approval in this module.
  - **Fix:** Rewrite the banner to match: bundled lines split even-by-weight into
    two clean priced lines; the order page captions them.
  - **Priority:** HIGH **Effort:** 10 min
  - **Fixer Prompt:** Same rewrite the moment the behavior changed — should the
    banner now say the module *never* flags bundles, only splits + prices them?

### 4. END-USER FRIENDLINESS

#### Medium Priority
- **Issue:** Decision docs form a supersession chain but only forward. A reader
  landing on `enforce-kata-brief-as-rules.md` or `split-recipe-and-ingredients-
  pages.md` has no signal those decisions were reversed.
  - **Fix:** Add a top `> Superseded by <file> (date).` line to each reversed doc
    (standard now codified in `STYLE_GUIDE.md`).
  - **Priority:** MEDIUM **Effort:** 10 min
  - **Fixer Prompt:** Want superseded decisions kept (with a back-reference) for
    the audit trail, or collapsed into a single current-state decision log?

## Quick Wins (High Impact, Low Effort)

1. Rewrite `data/conversion-logic.md` §5/§6/summary to match the current
   split-and-caption behavior (CRITICAL, ~20 min, fixes the live Page 3).
2. Rewrite `README.md` to the 4-page app + correct the `ci_checks.py` description
   and the dead `check_recipe_quality()` reference (CRITICAL, ~20 min).
3. Fix the `convert.js` banner and the `CLAUDE.md` self-contradiction (HIGH, ~20 min).

## Strategic Improvements (Foundational)

1. Adopt `docs/STYLE_GUIDE.md` as the standard; apply page headers + WHAT/WHY
   function comments everywhere (the owner's core ask).
2. Add the breadcrumb-discipline rule to the PR habit: behavior change ⇒ update
   conversion-logic.md / README / CLAUDE.md / kata-rules.md in the same PR. (A CI
   check could later assert, e.g., that `conversion-logic.md` doesn't contain
   "NEEDS APPROVAL" while `convert.js` emits no such flag — a doc/code drift gate.)

## Implementation Roadmap

### Phase 1: Critical truth fixes (now)
- conversion-logic.md, README.md to match reality; convert.js banner; CLAUDE.md
  contradiction.

### Phase 2: Documentation standard (this session)
- Apply STYLE_GUIDE page headers + function WHAT/WHY to all pages, JS, Python.
- Add superseded back-references to reversed decision docs.

### Phase 3: Drift prevention (optional)
- A lightweight doc/code-drift check in `ci_checks.py`.

## Positive Aspects Worth Preserving

- The math layer (`parse.js` / `convert.js`) is clean, single-responsibility, and
  correct; the conversion table lives in one place and can't drift.
- The static, no-build, repo-as-data-store architecture is the right call for this
  demo and deploys in ~1 minute.
- The CI data gate (`check_data_meets_kata_rules`) genuinely fails on bad data —
  verified with a negative test.
- Cross-page navigation is consistent and correct in both directions.
