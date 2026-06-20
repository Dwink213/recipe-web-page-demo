# Brutal Project Critique & Improvement Plan

_Final-check pass: 2026-06-19. Scope: whole repo, as it will be handed to interviewers._

## Executive Summary

This is the **second** brutal pass. The first found clean math but rotted
documentation ("code B+, docs D"). That gap is closed: the docs now match the code,
every page has a header comment and every function a WHAT/WHY, the breadcrumb trails
are complete and verified against the real link graph, the README is rewritten for
the actual app with two render-verified diagrams and an honest evolution timeline,
and `data.html` carries a hand-authored SVG site map.

**Verdict: interview-ready. No critical or high issues remain.** Everything below is
polish — the kind of thing a fair critic still names but that wouldn't embarrass the
author in front of an interviewer. The single most defensible gap is the missing
`LICENSE` on a public repo. Verified this pass: all five README live links return
200 on production; the data-flow diagram's worked example (`100g eggs → 2`) is
correct; no leftover `TODO`/`FIXME`; the README file tree matches the tracked files;
no secrets or PII in any tracked file.

## Critical Issues (Fix Immediately)

None. (Stated plainly because the job of a final check is to say so when it's true,
not to manufacture severity.)

## Dimension Analysis

### 1. STRUCTURE

#### Medium Priority
- **Issue:** No `LICENSE` file. This is a public repo being handed to interviewers;
  the absence leaves reuse rights undefined and reads as an unfinished edge.
  - **Fix:** Add an MIT `LICENSE` (or your preference) with your name and 2026.
  - **Priority:** MEDIUM **Effort:** 2 min
  - **Fixer Prompt:** MIT is the safe portfolio default — any reason to prefer
    Apache-2.0 (patent grant) or "all rights reserved"? If unsure, MIT.

#### Low Priority
- **Issue:** `order.html` and `convert.js` carry flag branches (`no procurement
  mapping`, `no quantity, cannot scale`) that no current recipe can trigger — every
  ingredient maps and parses. Defensive, but it's untested surface in the most
  complex file.
  - **Fix:** Keep it (the brief warned the input was dirty) but it's already
    commented; optionally add a fixture recipe with an unmapped ingredient so the
    path is exercised, or leave as documented dead-ish defense.
  - **Priority:** LOW **Effort:** 20 min if exercised
  - **Fixer Prompt:** Do you want to demo the "unmapped ingredient → flagged, not
    crashed" behavior live? If yes, add a fixture; if not, the comment is enough.

### 2. USEFULNESS

#### Verified Clean
- All conversion math, pricing, and totals recompute correctly (re-verified this
  pass). Edge cases handled without throwing: unparseable strings, missing
  quantities, no-`id` on order (picker) and ingredients (graceful link). All live
  links 200.

#### Low Priority
- **Issue:** Editable salt/pepper amounts are independent and not reconciled to the
  source line weight (you can set both to 0). Intentional per the last decision, and
  now commented — noting it only so a reviewer doesn't mistake it for a bug.
  - **Fix:** None needed; the inline comment covers it.
  - **Priority:** LOW **Effort:** 0
  - **Fixer Prompt:** Leave as-is unless an interviewer asks "shouldn't those sum to
    the original?" — then it's a 2-line clamp.

### 3. AESTHETICS

#### Low Priority
- **Issue:** The README's **structure** Mermaid diagram is visually busy (crossing
  fetch arrows) — the hand-authored SVG on `data.html` says the same thing more
  cleanly. Two diagrams of the same graph, one tangled.
  - **Fix:** Either simplify the README Mermaid (drop the fetch edges, keep page
    nav + the data-flow diagram), or replace it with a link/reference to the SVG.
  - **Priority:** LOW **Effort:** 15 min
  - **Fixer Prompt:** Is the README Mermaid earning its space next to the cleaner
    SVG, or should it be the simple nav-only version with the data flow shown once?

### 4. END-USER FRIENDLINESS

#### Low Priority
- **Issue:** The README lists internal Azure topology (resource group, subscription
  name). Harmless for a throwaway demo, but it's detail an interviewer doesn't need
  and a habit worth not forming.
  - **Fix:** Optional — trim to "Azure Static Web Apps, Free SKU" without the RG /
    subscription name.
  - **Priority:** LOW **Effort:** 2 min
  - **Fixer Prompt:** Keep the resource names as proof it's really deployed, or trim
    for tidiness? Your call — both are defensible.
- **Issue:** 11 commits carry a personal `Claude-Session: https://claude.ai/...`
  trailer. The `Co-Authored-By: Claude` line is good method-transparency; the
  session URL is a dead personal link that adds nothing for a reader.
  - **Fix:** Leave it (removing means a history rewrite + force-push, not worth the
    risk on a repo you're about to hand over). Just be aware it's there.
  - **Priority:** LOW **Effort:** N/A (don't rewrite history pre-interview)
  - **Fixer Prompt:** Only worth touching if you were starting the repo fresh — not
    now.

## Quick Wins (High Impact, Low Effort)

1. Add a `LICENSE` (MIT). 2 minutes; closes the only non-polish gap.

## Strategic Improvements (Foundational)

None outstanding. The breadcrumb-discipline practice (behavior change ⇒ update the
docs that describe it, in the same change) is now encoded in `docs/STYLE_GUIDE.md`
and `CLAUDE.md`; that's the foundational thing, and it's done.

## Implementation Roadmap

### Phase 1: Before handing it over
- Add `LICENSE`. Optionally trim Azure topology in the README.

### Phase 2: Only if asked / time permits
- Simplify the README structure Mermaid; add an unmapped-ingredient fixture.

### Phase 3: N/A
- Nothing load-bearing remains.

## Positive Aspects Worth Preserving

- **The process is the portfolio.** `docs/decisions/` (dated, with supersession
  back-references), `docs/kata-rules.md` (rule → enforcement), `docs/STYLE_GUIDE.md`,
  and this critique itself show disciplined, self-correcting work — rare in a kata.
- **Math lives in one place** (`convert.js`) and is correct; the conversion table
  can't drift.
- **Real CI gate** that fails on bad data (negative-tested), not a rubber stamp.
- **Honest documentation** that now matches the code, including the live Page 3.
- **Clean separation:** data / logic / pages / process docs, no framework, deploys
  in ~1 minute. Appropriate restraint for the problem.
