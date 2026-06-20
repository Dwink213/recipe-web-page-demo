# Daily Capture: The Editor Nobody Asked For (Salt & Pepper)

**Date:** 2026-06-19
**Session source:** recipe-web-page-demo — building the order page; the bundled "salt and pepper" line.

---

## What Happened

One recipe line — `"3g Salt and pepper (to taste)"` — is two SKUs at very different prices sharing one weight. I decided the right move was an interactive split editor: a slider/input to apportion salt vs pepper before approving the order. I built it. It broke (a whitespace `id` made `getElementById` return null). I "fixed" it with a scoped `querySelector`. It still didn't commit the value. The user said: "I can't change pepper, so let's just simplify this. Put salt and amount, then pepper, and note this was split because salt and pepper cost dramatically differently." I deleted the editor, rendered two plain priced lines plus a one-sentence caption, and deleted the now-orphaned rules module. The simple version was better in every way.

---

## Social Potential

**LinkedIn viable:** Yes
**Hook angle:** "I built the same broken feature twice to make a point a single sentence made better."
**Target audience:** Engineers, AI practitioners, anyone who's gold-plated a feature
**Post type:** Story / Confession
**Emotional driver:** Recognition, humor, relief
**Priority:** High

**Draft hook options:**
1. "I spent three pull requests building an interactive control nobody wanted. The fix was a one-line note. Here's how I knew I'd overbuilt it."
2. "The AI (me) kept 'fixing' a fragile editor. The human said two words — 'just simplify' — and the feature got better by getting smaller."
3. "A recipe said '3g salt and pepper.' I turned that into a DOM-wiring bug factory. The lesson: a note can beat a control."

**Viral levers present:**
- [x] Confession arc — leads with the failure (built the wrong thing twice)
- [x] Villain-vindication — the villain is over-engineering; the fix is deletion
- [x] Memeable phrase: "A note can beat a control."
- [ ] All-caps emotional pivot
- [x] Specific technical mechanism: an inline split editor vs. two priced lines + a caption
- [ ] Self-incriminating AI quote
- [x] Comment-bait question with stored answers: "What's the feature you over-built that should've been one sentence?"
- [x] Universal unnamed pain: the urge to make a point with a control instead of words

**Lever count:** 5 / 8
**Viral candidate?:** Yes (5+) — viral candidate. Consider timing; add a before/after screenshot of the two order-page versions; write carefully.

**Notes:** The honest framing (I overbuilt it; the human cut it) is the whole appeal. Don't sand off the failure.

---

## Training Material

**Training potential:** High
**Could become:** War story / Module
**Which course it fits:** Course 2 (Methodology)
**Teaching point:** "Communicate the constraint, don't engineer around it." When a value is ambiguous and a human must decide, surfacing the ambiguity (a labeled note) often beats building an interactive control to resolve it. Also: a control adds a DOM-wiring failure surface a note doesn't have.
**Prerequisite knowledge:** Basic web UI; the idea of human-in-the-loop.

**Notes:** Strong "simpler is more correct" exemplar. Pairs with the brutal-critic capture (self-audit as the counterweight to over-building).

---

## Technical Reproduction

**Steps to recreate (the failure, for teaching):**
1. Build an inline editor whose element `id` includes the ingredient name → `id="salt-salt and pepper"` (whitespace id = invalid).
2. Read it with `getElementById` → null in some browsers → click handler throws → value never commits.
3. "Fix" with `querySelector` but keep re-rendering on every keystroke → input loses focus.
4. Step back; replace the whole control with two priced lines + a caption.

**Gotchas:**
- Never put spaces (or the raw data value) into an HTML `id`. Scope with `closest()` + a class.
- Per-keystroke full re-render drops input focus; update the changed cell in place instead.

**Code/commands to preserve:**
```
# the simpler shape that won:
# render salt and pepper as two normal priced lines, plus:
<p class="splitnote">Split from "salt and pepper" — they cost very differently,
so the kitchen orders them separately.</p>
```

**Related files:** `order.html` (the rewrite), `js/convert.js` (the split into two clean lines), deleted `js/rules.js`.

---

## Product Extraction

**Standalone potential:** No
**Verdict:** Not a product — it's a lesson.

---

## Content War Chest Category

- [ ] Proof content
- [x] **Teaching content**
- [x] **Methodology content** — "communicate, don't engineer; delete to improve"
- [ ] Product content

**Primary category:** Methodology content

---

## Raw Material

- User, verbatim: "No, still the same problem. I can't change pepper, so let's just simplify this."
- The over-build was ~3 PRs: enforce-as-rules (added an approval gate + `rules.js`) → fix repricing bug → simplify (delete the editor and `rules.js`).
- Net of the simplification commit: **−189 lines** (order.html shrank ~160; rules.js deleted).
- The caption that replaced the feature is one sentence.

---

## Next Actions

- [ ] Draft the "a note can beat a control" post (High; add before/after screenshot).
- [ ] Use as the anchor war story for a "simpler is more correct" module.

---

## Cross-References

- **Related captures:** `_methodology.md` (human-override moment), `_brutal-critic-doc-audit.md`
- **Builds on:** prior "performative vs real" methodology threads
- **Feeds into:** Book Ch. 6 (The Human Layer), Ch. 8 (Anti-Patterns)
