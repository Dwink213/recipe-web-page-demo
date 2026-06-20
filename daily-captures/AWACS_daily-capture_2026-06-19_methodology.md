# Methodology Capture: Iterating Toward Simple, Honest, Shippable

**Date:** 2026-06-19
**Session source:** recipe-web-page-demo — a take-home kata built, iterated, self-audited, and prepped for handover, end-to-end with Claude Code on Azure Static Web Apps.
**Book chapter affinity:** Ch. 6 (The Human Layer) — when the human overrides the AI's instinct to build.

---

## Session Arc

Started from a messy build spec and produced a working, deployed app within the first pass. The middle of the session was not feature work — it was **requirement interpretation under a moving target**: the human steered the design three or four times (enforce the brief as hard rules → split pages literally → collapse to a direct flow → simplify an over-built control). The end of the session pivoted from building to **proving and presenting**: a self-critique pass that caught documentation lying on the live site, then a full interview-ready README, an SVG site map, and a clean repo audit. Starting state: a vague spec and an empty repo. Ending state: a deployed app, an honest paper trail, and a candidate who can defend every decision.

---

## Decision Sequences

### Enforce-as-rules, then delete the enforcement
**Starting assumption:** "Meeting the brief" meant *enforcing* its logic in code — an approval gate that blocks the order until every ambiguous line is resolved, plus a `rules.js` severity engine.
**What happened:** Built it. The interactive salt/pepper editor that the gate depended on broke twice (whitespace `id`; then per-keystroke re-render dropping focus). The human watched two "fixes" fail.
**Pivot point:** "I can't change pepper, so let's just simplify this." The human chose to *remove* the enforcement, not repair it.
**Final decision:** Two plain priced lines + a one-sentence caption; `rules.js` deleted; the order keeps only a single pending→approved step.
**Transferable principle:** When a value is ambiguous and a human must decide, *surface* the ambiguity (a labeled note) rather than *engineer* a control to resolve it. A control is a failure surface a sentence doesn't have.

### Literal brief vs. usable flow
**Starting assumption:** "A page for the recipe" + "a page listing ingredients" = two pages.
**What happened:** Split them literally (PR #2). The human then said clicking a recipe should go *straight* to ingredients — no middle page.
**Pivot point:** The human reading the *intent* (fast path to ingredients) over the *letter* (two nouns).
**Final decision:** Index links straight to `ingredients.html`; the middle `recipe.html` deleted (PR #3).
**Transferable principle:** Capture both readings, ship one, and make the reversal cheap — each interpretation was its own small PR, so changing direction cost minutes, not a rewrite.

### Verification that wasn't (the byte-array trap)
**Starting assumption:** My PowerShell `$content.Contains("NEEDS APPROVAL")` checks were verifying the deployed markdown.
**What happened:** They returned plausible booleans, so I claimed the fix had shipped. Azure serves `.md` as `application/octet-stream`, so `Invoke-WebRequest` handed back a **byte array**, and `[byte[]].Contains(...)` was matching bytes, not substrings — meaningless. A later `Substring` call threw and exposed it.
**Pivot point:** The error message — `[System.Byte] does not contain a method named 'Substring'` — caught what my over-confidence didn't.
**Final decision:** Re-verified with explicit `[Text.Encoding]::UTF8.GetString(...)`, and corrected the earlier false claim out loud.
**Transferable principle:** A check that runs is not a check that checks. Verify your verifier — especially when the result is the thing you *want* to be true.

---

## Human Judgment Moments

- **Moment:** Two failed attempts at the interactive split editor.
  **The judgment call:** The human said "just simplify" instead of asking for a third fix.
  **Why process alone wouldn't have gotten here:** My default was to repair the feature I'd committed to. Sunk-cost momentum keeps an AI patching; the human cut it.
  **Outcome:** −189 lines, a clearer page, no DOM-wiring bug surface. Strictly better.

- **Moment:** Prepping the repo for handover.
  **The judgment call:** "I'm not hiding any method I use to build this." Keep the decision records, the style guide, and the brutal self-critiques in the repo as *evidence of process*.
  **Why process alone wouldn't have gotten here:** The safe instinct is to scrub anything that looks unflattering (a "D" doc grade, AI co-authorship). The human reframed transparency as the selling point.
  **Outcome:** The repo's `docs/` is now a differentiator, not a liability.

- **Moment:** My false "it shipped" claim during staging verification.
  **The judgment call (mine):** When the `Substring` error exposed the byte-array bug, name the earlier claim as wrong rather than quietly re-run.
  **Why it matters:** Honesty about a performative check is the difference between trustworthy and merely confident.
  **Outcome:** Corrected; the final production verification used the right method.

---

## Discipline Practices Applied

- [x] **Ground truth before live calls** — recomputed the order math independently; verified live links return 200 rather than assuming.
- [x] **Pattern → ADR in same session** — every pivot got a dated decision record, with `> Superseded by` back-references when reversed.
- [x] **Self-audit through critic** — two brutal-critic passes; the first found doc rot, the second confirmed interview-ready.
- [x] **Institutional memory capture** — `CLAUDE.md` kept current; `docs/STYLE_GUIDE.md`, `docs/kata-rules.md` maintained.
- [x] **Compounding knowledge capture** — encoded "behavior change ⇒ update its docs in the same PR" as a rule, not a habit.
- [ ] **Mandatory lookup order** — N/A (no vendor KB in this project).
- [x] **Session-end capture** — this document.

**New practice observed this session:**
**"Verify the verifier."** After a check produces a convenient result, confirm the check is actually testing what you think — type, encoding, scope. Triggered by the byte-array trap; worth a standing habit because the most dangerous false positives are the ones you wanted.

---

## Compounding Effects

| Artifact | What it does for future sessions |
|---|---|
| `docs/STYLE_GUIDE.md` (page headers + WHAT/WHY + breadcrumb discipline) | New edits follow the standard instead of re-deriving it. |
| `docs/decisions/*` with supersession back-references | The evolution is auditable; a reversal is never silent. |
| `CLAUDE.md` (architecture map, "docs must match code" rule) | Future instances orient in seconds and keep docs honest. |
| `scripts/ci_checks.py` data gate (negative-tested) | Bad data can't drift in via an unreviewed PR. |
| `data.html` SVG + README diagrams (render-verified) | The structure is legible without reading every file. |

**Knowledge base delta:** N/A (no `knowledge/` in this project).
**Tooling delta:** Added `staticwebapp.config.json` (404s `/docs/*`), `LICENSE` (MIT), a CI data gate, a recipe picker.
**Rule delta:** "Behavior change ⇒ update the docs that describe it, same PR" encoded in `STYLE_GUIDE.md` + `CLAUDE.md`.

---

## Anti-Patterns & Time Sinks

- **Time sink:** ~3 PRs building/fixing an interactive split editor nobody wanted.
  **Root cause:** Chose to *engineer* a point ("salt and pepper aren't equal") that a *sentence* made better; then sunk-cost-patched the broken control.
  **Prevention:** When a feature exists to communicate, try the sentence first. Set a "two fixes then delete" trip-wire for fragile UI.

- **Time sink:** False staging verification via `[byte[]].Contains`.
  **Root cause:** Assumed `.Content` was a string; didn't check the type because the boolean was convenient.
  **Prevention:** Decode bytes explicitly; treat a check that confirms your hope with suspicion.

- **Minor:** Repeated PowerShell quoting slips in verification one-liners (doubled quotes, inline `try`) produced false negatives I had to re-run.
  **Prevention:** For assertions that matter, write the check to fail loudly on its own bugs, not silently.

---

## The Compounding Story

If you watched this session, the lesson isn't "AI builds an app." It's how the *working relationship* produced something better than either party would alone. The AI's reflex was to build and to defend what it built — an enforcement engine, an interactive editor, a third fix for a broken control. The human's contribution was almost entirely *subtractive*: simplify this, drop the middle page, stop engineering the point and just say it. Most of the quality came from deletions the AI wouldn't have proposed, because deleting your own work cuts against the grain of "be helpful by doing more."

The second thread is honesty as a practice, not a vibe. A self-critique pass caught the project's documentation lying on the live site — and then caught *me* lying, gently, when a convenient verification turned out to be a byte-array no-op. The discipline that mattered was naming both out loud and re-verifying with the right method, rather than letting a green-looking check stand. The book's recurring villain — "performing the behavior without doing the behavior" — showed up twice in one session: a status page that performed self-documentation while describing a deleted feature, and a verification that performed checking while comparing bytes. Both were caught by the same move: go to ground truth and look.

The third thread is that transparency was treated as an asset. Instead of scrubbing the AI co-authorship and the unflattering "D" doc grade, the human kept the decision records and the critiques in the repo as evidence of disciplined process. That's the whole thesis in miniature: disciplined AI-assisted work doesn't hide that it's AI-assisted — it shows the rails it ran on.

---

## Book Chapter Affinity

**Primary chapter:** Ch. 6 — The Human Layer (the human's overrides were subtractive and they were the source of most of the quality)
**Secondary chapters:** Ch. 8 (Anti-Patterns — the editor thrash, the byte-array trap), Ch. 4 (The Feedback Loop — the brutal-critic passes)
**Key quote or insight for the book:** "Most of the quality came from the deletions the AI wouldn't have proposed — because deleting your own work cuts against 'be helpful by doing more.'"

---

## Book Flavor Tags

- [x] **Confession moment** — I built the same broken feature twice; the fix was a sentence.
- [x] **Villain-vindication arc** — villain: over-engineering + performative checks; fix: delete + verify-the-verifier.
- [x] **Memeable phrase** — "A check that runs is not a check that checks."
- [x] **Caught-the-AI-lying moment** — the byte-array `.Contains` produced a false "it shipped"; the `Substring` error exposed it; I corrected the claim.
- [x] **Human-override moment** — "just simplify this" beat a third attempt at the editor.
- [x] **Performative-vs-real contrast** — a self-documenting page that documented a deleted system; a verification that compared bytes, not text.

**Narrative weight:** Heavy
**Why it matters for the book:** It's a clean, dated, two-for-one instance of the book's core villain (performing a behavior without doing it) caught inside a single disciplined session — and a vivid example of human judgment adding value by subtraction.

---

## Chapter Map (Reference)

| Chapter | Theme |
|---|---|
| 1 | The Discipline Gap |
| 2 | Ground Truth |
| 3 | Formalize While Fresh |
| 4 | The Feedback Loop |
| 5 | Institutional Memory |
| 6 | The Human Layer |
| 7 | Compounding |
| 8 | The Anti-Patterns |
| 9 | Teaching the Discipline |
| 10 | The Long Game |

---

## Cross-References

- **Related topic captures (this session):** `_kata-recipe-app-build.md`, `_salt-pepper-over-engineering.md`, `_azure-swa-staging-env-limit.md`, `_brutal-critic-doc-rot.md`
- **Builds on:** the "performed accountability without doing accountability" thread (2026-04-10 post-mortem)
- **Feeds into:** Book Ch. 6 (primary), Ch. 8, Ch. 4
