**Decision:** (1) Extract the duplicated per-page inline `<style>` blocks into one shared `styles.css`; each page's `<head>` is now just a `<title>` + `<link>`. (2) Make ambiguous order lines editable: salt, pepper, and any flagged line get a grams input that live-reprices that line and the order total in place (no full re-render, so focus is kept).

**Why:** User direction: "there's like 150 lines of just class … something we can collapse in CSS … stupid simple headers"; and "you should allow modification on each salt and pepper or any other ambiguous things." A static site is the right place for a shared stylesheet (fetched once, cached). The earlier inline editor failed because of a whitespace `id` and per-keystroke re-render that dropped focus; the in-place update via `.qty-edit` + `data-idx` selectors fixes both.

**Alternatives considered:** Keep inline styles per page (rejected: ~150 lines duplicated four times). Re-render on every keystroke (rejected: that was the focus-loss bug). A single combined salt/pepper slider (rejected earlier: the user wants each amount independently editable).

**Date:** 2026-06-19
