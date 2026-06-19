# Style Guide — recipe-web-page-demo

The one documented standard for every kind of code in this repo. It exists so a
stranger (or a future you at 2 AM) can open any file and, in ten seconds, know
what it is, what it talks to, and why each block exists. Vanilla HTML + ES-module
JS + a small Python gate; **no build step, no dependencies** — keep it that way.

## Golden rules

1. **The repo is the data store.** Data lives in `/data/*.json` and is fetched at
   runtime. Never hard-code recipe/price data into a page.
2. **Docs must match code.** A comment or doc that describes behavior the code no
   longer has is a bug. When you change behavior, update — in the same PR — every
   place that describes it (see *Breadcrumb discipline* below).
3. **Simplest thing that works.** No framework, no abstraction without a second
   caller. Delete dead code rather than commenting it out.
4. **Every function says WHAT and WHY**, not how (the code is the how).

## Breadcrumb discipline (the footnote trail)

These describe the app's behavior and MUST stay mutually consistent. Changing
behavior means updating all that apply, in the same change:

- `data/conversion-logic.md` — **rendered live on `data.html` (Page 3)**. If it
  describes the order logic, it must match `js/convert.js` and `order.html`
  exactly. This is user-facing; a stale claim here is a lie to the interviewer.
- `README.md` — the outside view. Page list, what each file does, how to run.
- `CLAUDE.md` — the maintainer's map. Page/module descriptions, gotchas.
- `docs/kata-rules.md` — rule → enforcement map (R1…Rn).
- `docs/decisions/*.md` — one decision per file. When a decision reverses an
  earlier one, the **new** doc adds `**Supersedes:** <file>` AND the **old** doc
  gets a top line `> Superseded by <file> (YYYY-MM-DD).`

## File header comments (top of every file)

### HTML pages — comment as the first child of `<body>`

```html
<!--
  PAGE:     order.html
  WHAT:     Advanced order builder for one recipe — scale, convert to
            procurement units, price (illustrative), and a human Approve step.
  DISPLAYS: editable order lines (incl. the salt/pepper split), running total,
            pending/approved status.
  DATA:     fetches data/recipes.json + data/procurement.json at runtime.
  IN  (linked from): ingredients.html
  OUT (links to):    index.html, ingredients.html, data.html
  MODULES:  js/convert.js
-->
```

`IN`/`OUT` are the breadcrumb trail — keep them accurate both directions. If you
add or remove a link, fix the header on both pages.

### JS modules — file banner + JSDoc per function

```js
// convert.js — <one-line purpose>.
//
// <2-4 lines: what this module is responsible for and why it exists as its own
// unit. Note key invariants (e.g. "never throws; flags instead").>

/**
 * WHAT: <what the function returns/does>.
 * WHY:  <why it exists / the decision it encodes>.
 * @param {Type} name <meaning>
 * @returns {Type} <meaning>
 */
export function buildOrder(recipe, targetServings, procurement) { … }
```

Internal (non-exported) helpers get at minimum a one-line `// WHAT / WHY` comment
directly above them.

### Python — module docstring + function docstrings

```python
"""ci_checks.py — <one-line purpose>.

<what it gates and why; how to run: python scripts/ci_checks.py>.
"""

def check_data_meets_kata_rules(errors):
    """WHAT: <assertions made>. WHY: <which brief rule this enforces>."""
```

### CSS — section banners

```css
/* ─── order ─────────────────────────────── */
```
Group rules by the page/feature they serve; one banner per group.

### JSON data — a `_meta` object

Carry provenance and caveats in a leading `"_meta": { "note": "…" }` (already used
in `procurement.json`). Never put prose in data values.

## Formatting

- 2-space indentation; double quotes in JS/HTML attributes; semicolons in JS.
- Escape user/data-derived strings before inserting into HTML (`esc()` helper).
- Money formatted to 2 decimals; grams rounded to 0.1 for display only — never
  round the value you compute the next step from.
- Filenames: lowercase. Slugs: `[a-z0-9-]`. Match the CI gate in `ci_checks.py`.

## When you touch the order math

`js/convert.js` is the single source of conversion truth. If a number changes,
re-run `node`-side spot checks against `data/conversion-logic.md`'s worked
examples (eggs 100g→2 each; olive oil 30g→32.6 ml) and update the prose if the
rule changed.
