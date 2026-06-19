#!/usr/bin/env python3
"""ci_checks.py - lightweight validation gate for the recipe web page demo.

WHAT: runs a few cheap checks over the repo (page present, not empty, no leaked
      secrets, data obeys the kata rules) and exits non-zero if any fail.
WHY:  it runs in CI on every push/PR AND locally before pushing, so the same
      command catches a broken or non-compliant deploy in milliseconds.

Each check appends human-readable strings to a shared `errors` list; a non-empty
list means the gate fails (exit 1). Run locally:  python3 scripts/ci_checks.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check_index_exists(errors):
    """WHAT: assert index.html is at the repo root. WHY: the SWA serves the root,
    so a missing/moved index.html means a blank site."""
    if not (ROOT / "index.html").is_file():
        errors.append("index.html is missing from the repo root.")


def check_index_not_empty(errors):
    """WHAT: assert index.html has real HTML content. WHY: a blank page deploys
    'successfully' but is a broken demo - catch it before it ships."""
    index = ROOT / "index.html"
    if not index.is_file():
        return  # already reported by check_index_exists
    text = index.read_text(encoding="utf-8", errors="replace")
    if len(text) < 200 or "<html" not in text.lower():
        errors.append("index.html exists but looks empty or is not valid HTML.")


def check_no_leaked_secrets(errors):
    """WHAT: scan text files for obvious credential patterns. WHY: the repo is
    public, so a copy-pasted token must never ship to the live site.

    A coarse safety net, not a full secret scanner — a few high-signal shapes.
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


def check_data_meets_kata_rules(errors):
    """WHAT: assert data/recipes.json + data/procurement.json obey the kata's data
    rules (recipe shape + unique slug ids, illustrative price labels, and the
    bundled salt/pepper modeling). WHY: the brief is the contract, so the data
    can't drift out of compliance through an unreviewed PR. See docs/kata-rules.md.
    """
    data = ROOT / "data"
    recipes_path, proc_path = data / "recipes.json", data / "procurement.json"

    try:
        recipes = json.loads(recipes_path.read_text(encoding="utf-8"))
        procurement = json.loads(proc_path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        errors.append(f"Required data file missing: {e.filename}")
        return
    except json.JSONDecodeError as e:
        errors.append(f"Data JSON is malformed (the brief warns the source was): {e}")
        return

    # Rule: recipes is a non-empty list of well-shaped recipes with unique slug ids.
    if not isinstance(recipes, list) or not recipes:
        errors.append("recipes.json must be a non-empty list.")
        recipes = []
    seen_ids = set()
    for i, r in enumerate(recipes):
        where = f"recipes[{i}]"
        if not isinstance(r.get("id"), str) or not re.fullmatch(r"[a-z0-9-]+", r.get("id", "")):
            errors.append(f"{where}: 'id' must be a non-empty slug (lowercase, digits, hyphens).")
        elif r["id"] in seen_ids:
            errors.append(f"{where}: duplicate id '{r['id']}' — ids must be unique for routing.")
        else:
            seen_ids.add(r["id"])
        if not isinstance(r.get("title"), str) or not r.get("title", "").strip():
            errors.append(f"{where}: 'title' must be a non-empty string.")
        if not isinstance(r.get("yield"), (int, float)) or r.get("yield", 0) <= 0:
            errors.append(f"{where}: 'yield' must be a positive number (scaling divides by it).")
        ings = r.get("ingredients")
        if not isinstance(ings, list) or not ings or not all(isinstance(s, str) and s.strip() for s in ings):
            errors.append(f"{where}: 'ingredients' must be a non-empty list of non-empty strings.")

    # Rule (brief #4): every priced procurement entry is labeled illustrative,
    # has a known buy unit, and carries the conversion factor that unit needs.
    valid_units = {"g": "gramsPerUnit", "each": "gramsPerUnit", "ml": "gramsPerMl"}
    for name, p in procurement.items():
        if name == "_meta" or not isinstance(p, dict):
            continue
        if p.get("bundled"):
            continue  # bundled entries are validated below, not priced directly
        unit = p.get("buyUnit")
        if unit not in valid_units:
            errors.append(f"procurement['{name}']: buyUnit must be one of g/ml/each, got {unit!r}.")
            continue
        if not isinstance(p.get(valid_units[unit]), (int, float)):
            errors.append(f"procurement['{name}']: '{unit}' unit requires a numeric {valid_units[unit]}.")
        if not isinstance(p.get("pricePerBuyUnit"), (int, float)):
            errors.append(f"procurement['{name}']: missing numeric pricePerBuyUnit.")
        if p.get("priceNote") != "illustrative":
            errors.append(f"procurement['{name}']: priceNote must be 'illustrative' (brief: never present placeholders as real).")

    # Rule (brief #5): the bundled salt-and-pepper line must be modeled as an
    # approval-gated split whose targets actually exist. This is the ambiguity
    # the system must never resolve silently.
    bundled = procurement.get("salt and pepper")
    if not isinstance(bundled, dict) or not bundled.get("bundled"):
        errors.append("procurement['salt and pepper'] must exist and be marked bundled (brief #5).")
    else:
        if not bundled.get("requiresApproval"):
            errors.append("procurement['salt and pepper'] must set requiresApproval: true.")
        targets = bundled.get("splitInto") or []
        if not targets:
            errors.append("procurement['salt and pepper'] must list splitInto targets.")
        for t in targets:
            if t not in procurement:
                errors.append(f"procurement['salt and pepper'] splits into '{t}', but '{t}' has no procurement entry.")


def main():
    errors = []
    check_index_exists(errors)
    check_index_not_empty(errors)
    check_no_leaked_secrets(errors)
    check_data_meets_kata_rules(errors)

    if errors:
        print("Site validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("Site validation passed.")


if __name__ == "__main__":
    main()
