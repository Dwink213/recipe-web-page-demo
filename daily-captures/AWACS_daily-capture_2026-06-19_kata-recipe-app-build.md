# Daily Capture: Building a Recipe Kata as a Static Web App

**Date:** 2026-06-19
**Session source:** recipe-web-page-demo — a take-home kata for an AI Engineer role, built end-to-end with Claude Code and deployed to Azure Static Web Apps.

---

## What Happened

Took a deliberately messy meal-plan spec (malformed JSON, unstructured ingredient strings) and built a static, no-build web app from it: a recipe list, an ingredients page, and two advanced pages (an order builder that scales recipes into costed procurement orders, and a self-documenting data view). All logic runs client-side in two ES modules; the "back end" is JSON files committed to the repo and fetched at runtime. A Python CI gate enforces the data rules and runs on every push.

---

## Social Potential

**LinkedIn viable:** Maybe
**Hook angle:** "The interview said 'in-memory dictionaries will do.' I read that as 'the repo is the data store' — and shipped a real deployment in an afternoon."
**Target audience:** AI practitioners, hiring engineers, junior devs prepping for take-homes
**Post type:** Proof / Behind-the-scenes
**Emotional driver:** Recognition (everyone's done a take-home), curiosity (the architecture choice)
**Priority:** Medium

**Draft hook options:**
1. "A take-home kata said 'no database needed.' Here's the architecture that turned that constraint into a feature."
2. "Static site, no build step, deploys in a minute — and it still does unit conversion and procurement pricing. The repo is the database."
3. "How I turned a messy meal-plan JSON into a deployed app — and why I didn't reach for a framework."

**Viral levers present:**
- [ ] Confession arc
- [ ] Villain-vindication
- [ ] Memeable phrase: "The repo is the data store."
- [ ] All-caps emotional pivot
- [x] Specific technical mechanism: static SWA + repo-as-data-store + a CI data gate
- [ ] Self-incriminating AI quote
- [ ] Comment-bait question with stored answers
- [x] Universal unnamed pain: over-engineering take-homes / reaching for a framework when static would do

**Lever count:** 2 / 8
**Viral candidate?:** Normal (0-2)

**Notes:** Sanitize — no interviewer name, company, or schedule. The repo is public; the architecture is the story, not the assignment.

---

## Training Material

**Training potential:** High
**Could become:** Case study / Live demo
**Which course it fits:** Course 1 (AI-Assisted Infrastructure)
**Teaching point:** How to translate a vague constraint ("in-memory dictionaries are fine") into a clean static architecture, and how to put a real validation gate on data that has no schema.
**Prerequisite knowledge:** Basic HTML/JS, what a static host is, GitHub Actions basics.

**Notes:** Pairs well with a "when NOT to use a framework" module.

---

## Technical Reproduction

**Steps to recreate:**
1. Clean the supplied JSON to valid syntax only (never alter the meaning of a line); add a slug `id` per recipe.
2. Write `parse.js` to structure ingredient strings (`"100g large eggs"` → `{amount, unit, name, note, flags}`), preserving the raw string.
3. Write `convert.js` to scale by `targetServings / yield`, join to a `procurement.json` table by normalized name, convert grams to buy units (`ceil` for countables, density for ml), and price.
4. Build four plain HTML pages that `fetch()` the JSON and render client-side.
5. Add `ci_checks.py` to assert recipe shape, illustrative-price labels, and bundled-line modeling; wire it into CI.
6. Deploy via Azure SWA GitHub Action (`skip_app_build: true`, root `app_location`).

**Dependencies:** GitHub, Azure Static Web Apps (Free SKU), Python 3 (for the gate), a modern browser (ES modules).

**Environment:** Windows dev box; Azure East US 2; static hosting.

**Gotchas:**
- Pages `fetch()` JSON — serve over HTTP, not `file://`, or the fetch fails silently.
- Countables (eggs, tortillas) must round *up*; you can't order 2.1 eggs.

**Code/commands to preserve:**
```
python3 scripts/ci_checks.py   # the validation gate (also runs in CI)
python3 -m http.server 8080    # local preview over HTTP
```

**Related files:** `js/parse.js`, `js/convert.js`, `data/*.json`, `scripts/ci_checks.py`, `.github/workflows/*.yml`

---

## Product Extraction

**Standalone potential:** No
**What it is:** A reference template for "static site + repo-as-data-store + CI data gate."
**Who would use it:** Devs who want a deployable demo without a backend.
**What it needs for GitHub:** Already public and documented.
**MVP scope:** The repo itself is the MVP.
**Monetization angle:** Open-source credibility / teaching asset.
**Competitors/alternatives:** Every static-site starter; this one's differentiator is the CI data gate.
**Verdict:** Not a product — teaching/portfolio asset.

---

## Content War Chest Category

- [x] **Proof content** — a deployed, working app with verified math
- [x] **Teaching content** — the architecture translation lesson
- [ ] **Methodology content**
- [ ] **Product content**

**Primary category:** Proof content

---

## Raw Material

- "No need for a full database (in memory dictionaries will do)" → interpreted as flat JSON fetched at runtime.
- Verified math (all recipes): eggs 100g→2 each, garlic 10g→4 cloves, bell pepper 250g→3 each, olive oil 30g→32.6 ml.
- Live: https://yellow-field-01e27460f.7.azurestaticapps.net/

---

## Next Actions

- [ ] If posting: write the "repo is the data store" proof post (Medium priority).
- [ ] Consider a generic template extraction (strip the kata specifics).

---

## Cross-References

- **Related captures:** `_methodology.md` (this session), `_brutal-critic-doc-audit.md`
- **Related project files:** `README.md`, `docs/kata-rules.md`
- **Builds on:** prior static-SWA deploy patterns
- **Feeds into:** Course 1 case study
