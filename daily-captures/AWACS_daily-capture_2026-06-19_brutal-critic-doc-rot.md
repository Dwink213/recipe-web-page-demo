# Daily Capture: The Self-Documenting Page That Lied

**Date:** 2026-06-19
**Session source:** recipe-web-page-demo — a brutal-critic pass auditing math, breadcrumbs, and docs.

---

## What Happened

Ran a deliberate self-critique pass over the project. The math was clean and every cross-page link resolved — but the documentation had rotted across six iterations. The worst case: `conversion-logic.md`, which **renders live on the app's "self-documenting" Page 3**, still described a salt/pepper approval-gate ("flagged and marked NEEDS APPROVAL") that had been deleted three changes earlier. The page meant to let a reviewer audit the system was describing a *different* system. Also found a stale README (described a single-page app + a renamed function) and a `convert.js` banner contradicting its own code. Fixed all of them, wrote a `STYLE_GUIDE.md`, added a page-header comment to every page and a WHAT/WHY to every function, and encoded a "breadcrumb discipline" rule (behavior change ⇒ update the docs that describe it, same change).

---

## Social Potential

**LinkedIn viable:** Yes
**Hook angle:** "My app had a page whose whole job was to document itself. It was lying — describing a feature I'd deleted three commits earlier."
**Target audience:** Engineers, technical writers, AI practitioners
**Post type:** Confession / Teaching
**Emotional driver:** Recognition (doc rot is universal), mild dread
**Priority:** High

**Draft hook options:**
1. "The most dangerous documentation isn't missing docs — it's a 'self-documenting' page that confidently describes a system you already deleted."
2. "I ran a brutal self-critique on my own project. The math was perfect. The docs were a D. Here's the one that scared me."
3. "Doc rot has a half-life of about six pull requests. Mine described an approval gate I'd ripped out. On the live site."

**Viral levers present:**
- [x] Confession arc — the live page was lying; I'd shipped it
- [x] Villain-vindication — villain is doc rot; fix is a same-PR discipline + a self-critique pass
- [x] Memeable phrase: "A self-documenting page that documents a different system is worse than no docs."
- [ ] All-caps emotional pivot
- [x] Specific technical mechanism: a self-critique pass + a "behavior change ⇒ update its docs in the same PR" rule
- [ ] Self-incriminating AI quote
- [x] Comment-bait question with stored answers: "What's the worst stale-doc-on-prod you've shipped?"
- [x] Universal unnamed pain: docs drifting silently out of sync with code

**Lever count:** 5 / 8
**Viral candidate?:** Yes (5+) — viral candidate. Add the before/after of the rendered Page 3; write carefully.

**Notes:** Strong because the "self-documenting page lies" image is concrete and a little frightening.

---

## Training Material

**Training potential:** High
**Could become:** Module / War story
**Which course it fits:** Course 2 (Methodology)
**Teaching point:** Build self-correction into the workflow: (1) run a critic pass that *verifies claims* rather than asserting quality; (2) make "behavior change ⇒ update the docs that describe it" a same-PR rule, not a later chore; (3) the most dangerous doc is the authoritative one that's wrong.
**Prerequisite knowledge:** Basic git/PR workflow; what "self-documenting" usually means (and why it's a trap if unmaintained).

---

## Technical Reproduction

**Steps to recreate (the audit):**
1. Verify the math independently (recompute every conversion/total).
2. Build the inbound link graph from actual `href`s; compare to documented IN/OUT claims.
3. Grep the prose docs for terms describing behavior (e.g., "NEEDS APPROVAL") and check they still exist in the code.
4. Fix the drift; write a style guide; add a same-PR doc-sync rule.

**Gotchas:**
- A "self-documenting" artifact rendered on the live site is the highest-stakes doc — drift there is user-facing.
- A passing CI gate doesn't catch prose drift; consider a check that asserts code/doc agreement (e.g., fail if `conversion-logic.md` says "NEEDS APPROVAL" while the code emits no such flag).

**Code/commands to preserve:**
```
git grep -niE 'NEEDS APPROVAL|check_recipe_quality|single static HTML page'   # hunt stale prose
```

**Related files:** `data/conversion-logic.md`, `README.md`, `js/convert.js` banner, `docs/STYLE_GUIDE.md`, `docs/Brutal_Improvements.md`.

---

## Product Extraction

**Standalone potential:** Maybe
**What it is:** A "doc/code drift" CI check — assert that named behaviors in prose still exist in code.
**Who would use it:** Teams with living docs (READMEs, runbooks) that drift.
**MVP scope:** A linter with a small map of `phrase → must-exist-in-file`.
**Verdict:** Explore further — niche but real.

---

## Content War Chest Category

- [ ] Proof content
- [x] **Teaching content**
- [x] **Methodology content**
- [ ] Product content

**Primary category:** Methodology content

---

## Raw Material

- Stale line (was live on Page 3): "Both lines are flagged and marked NEEDS APPROVAL ... Nothing is ordered until a person confirms or corrects the split." — describing deleted machinery.
- First pass grade: "code B+, docs D." Second (final) pass: no critical/high issues.
- New rule encoded in `STYLE_GUIDE.md` + `CLAUDE.md`: behavior change ⇒ update `conversion-logic.md` / README / CLAUDE.md / kata-rules.md in the same change.

---

## Next Actions

- [ ] Draft the "self-documenting page that lied" post (High; before/after screenshot).
- [ ] Prototype the doc/code-drift CI check.

---

## Cross-References

- **Related captures:** `_methodology.md`, `_salt-pepper-over-engineering.md` (the deleted feature whose docs lingered)
- **Builds on:** the existing "feedback loop / self-audit" methodology thread
- **Feeds into:** Book Ch. 4 (The Feedback Loop), Ch. 3 (Formalize While Fresh)
