# Daily Capture: Azure SWA Free-Tier Staging Cap (Deploy Failure & Recovery)

**Date:** 2026-06-19
**Session source:** recipe-web-page-demo — a PR deploy failed mid-session; diagnosed and recovered.

---

## What Happened

After several merged PRs, a new PR's deploy failed: `This Static Web App already has the maximum number of staging environments`. Azure SWA Free tier caps concurrent PR staging environments at 3, and the auto-close jobs on previously merged PRs had reported success but **not actually deleted** the environments (a known SWA quirk). Listed them with `az staticwebapp environment list`, deleted the three orphans, re-ran the failed deploy → pass. Later merges auto-closed cleanly; checked again at the end — only `default` (production) remained.

---

## Social Potential

**LinkedIn viable:** Maybe
**Hook angle:** "Your Azure deploy didn't fail because of your code. It failed because three 'closed' PR environments never actually closed."
**Target audience:** Platform/DevOps engineers, anyone on Azure Static Web Apps
**Post type:** Teaching / Proof
**Emotional driver:** Recognition (cryptic cloud limits), relief (the fix)
**Priority:** Medium

**Draft hook options:**
1. "Azure SWA Free tier allows 3 staging environments. The auto-close says 'success' but sometimes leaves them up. Here's the one-liner that unblocks the deploy."
2. "A green 'close' job is not a deleted environment. A debugging note from a real deploy."

**Viral levers present:**
- [ ] Confession arc
- [x] Villain-vindication — the villain is a silent cloud limit + a lying "success" status
- [x] Memeable phrase: "A green close job is not a deleted environment."
- [ ] All-caps emotional pivot
- [x] Specific technical mechanism: `az staticwebapp environment list/delete` to clear orphans
- [ ] Self-incriminating AI quote
- [x] Comment-bait question with stored answers: "What's your favorite 'the status said success but lied' cloud moment?"
- [x] Universal unnamed pain: cloud status that reports success without doing the thing

**Lever count:** 4 / 8
**Viral candidate?:** Likely above average (3-4)

**Notes:** Echoes the book's "performed accountability without doing accountability" theme — a status that performs success without doing the work.

---

## Training Material

**Training potential:** Medium
**Could become:** Case study / Exercise
**Which course it fits:** Course 1 (AI-Assisted Infrastructure)
**Teaching point:** Don't trust a workflow's exit status as proof of the underlying cloud state — verify the resource directly. And know the Free-tier limits before you fan out PRs.
**Prerequisite knowledge:** Azure SWA, GitHub Actions, `az` CLI.

---

## Technical Reproduction

**Steps to recreate / fix:**
1. Symptom: PR deploy fails with `maximum number of staging environments`.
2. List: `az staticwebapp environment list --name <swa> --resource-group <rg> -o table`
3. Delete orphans: `az staticwebapp environment delete --name <swa> --resource-group <rg> --environment-name <N> --yes`
4. Re-run the failed deploy (`gh run rerun <id> --failed`).

**Gotchas:**
- The PR `close` job can report success without deleting the environment — verify with `az ... environment list`.
- Free tier = 3 concurrent staging environments. Several open/never-torn-down PRs will block the next deploy.

**Code/commands to preserve:**
```
az staticwebapp environment list   --name recipe-web-page-demo --resource-group rg-recipe-web-page-demo -o table
az staticwebapp environment delete --name recipe-web-page-demo --resource-group rg-recipe-web-page-demo --environment-name 3 --yes
gh run rerun <run-id> --failed
```

**Related files:** `.github/workflows/deploy.yml` (the close job that's unreliable).

---

## Product Extraction

**Standalone potential:** Maybe
**What it is:** A tiny "SWA orphan-environment janitor" — a scheduled script that lists staging envs and deletes any whose PR is closed.
**Who would use it:** Teams on SWA Free/standard tiers hitting the cap.
**MVP scope:** A GitHub Action (cron) that runs the list/delete against closed PRs.
**Monetization angle:** Open-source credibility.
**Verdict:** Park for later — a 30-line utility, not a business.

---

## Content War Chest Category

- [x] **Proof content**
- [x] **Teaching content**
- [ ] Methodology content
- [ ] Product content

**Primary category:** Teaching content

---

## Raw Material

- Error: "This Static Web App already has the maximum number of staging environments ... Please remove one and try again."
- Orphans were envs 3, 4, 5 (from merged PRs #3–#5) still "Ready."
- Verified resolution: after deletes + rerun, deploy passed; end-of-session list showed only `default`.

---

## Next Actions

- [ ] Optionally script the orphan cleanup (cron Action).
- [ ] Note the 3-env cap in any SWA runbook.

---

## Cross-References

- **Related captures:** `_methodology.md` (verify-the-resource discipline)
- **Builds on:** prior "verify before claiming" practices
- **Feeds into:** Course 1; Book Ch. 2 (Ground Truth)
