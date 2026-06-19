#!/usr/bin/env python3
"""ci_checks.py - lightweight validation gate for the recipe web page demo.

Modeled on the AWACS site CI gate, trimmed to checks that make sense for a
single-page static demo. Each check appends human-readable strings to a shared
`errors` list; a non-empty list means the gate fails (exit 1).

Run locally with:  python3 scripts/ci_checks.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check_index_exists(errors):
    """The deploy serves repo root, so index.html must exist there."""
    if not (ROOT / "index.html").is_file():
        errors.append("index.html is missing from the repo root.")


def check_index_not_empty(errors):
    """A blank page deploys 'successfully' but is a broken demo - catch it."""
    index = ROOT / "index.html"
    if not index.is_file():
        return  # already reported by check_index_exists
    text = index.read_text(encoding="utf-8", errors="replace")
    if len(text) < 200 or "<html" not in text.lower():
        errors.append("index.html exists but looks empty or is not valid HTML.")


def check_no_leaked_secrets(errors):
    """Scan tracked text files for obvious credential patterns.

    This is a coarse safety net, not a full secret scanner. It looks for a few
    high-signal shapes so a copy-pasted token never ships to a public site.
    """
    patterns = {
        "Azure SWA deployment token assignment": re.compile(
            r"AZURE_STATIC_WEB_APPS_API_TOKEN\s*[:=]\s*['\"]?[A-Za-z0-9]{20,}"
        ),
        "generic api key literal": re.compile(
            r"(api[_-]?key|secret|password)\s*[:=]\s*['\"][A-Za-z0-9/+]{16,}['\"]",
            re.IGNORECASE,
        ),
    }
    scan_exts = {".html", ".js", ".css", ".json", ".md", ".py", ".yml", ".yaml"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in scan_exts:
            continue
        if ".git" in path.parts:
            continue
        if path.name == "ci_checks.py":
            continue  # this file legitimately names the token variable
        content = path.read_text(encoding="utf-8", errors="replace")
        for label, rx in patterns.items():
            if rx.search(content):
                rel = path.relative_to(ROOT)
                errors.append(f"Possible {label} found in {rel}.")


def check_recipe_quality(errors):
    """OPTIONAL content gate - your design choice.

    This is the one place where what the gate enforces is a real decision rather
    than boilerplate. Decide what a 'valid' recipe page must contain and assert
    it here. Returning without appending anything = the check passes.

    Ideas to consider (pick what matters to you):
      - require an <h1> title so every page has a headline
      - require an Ingredients section and a Method/Steps section
      - require a serving size / time so the demo always shows metadata
    Trade-off: stricter checks catch broken pages earlier, but a too-rigid gate
    blocks legitimate variations of the template.
    """
    # TODO(you): implement 5-10 lines asserting the recipe page's required shape.
    # Left as a no-op so CI passes until you decide the rules.
    return


def main():
    errors = []
    check_index_exists(errors)
    check_index_not_empty(errors)
    check_no_leaked_secrets(errors)
    check_recipe_quality(errors)

    if errors:
        print("Site validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("Site validation passed.")


if __name__ == "__main__":
    main()
