**Decision:** Treat the Kata brief as a binding contract and enforce its rules in code — the order page blocks approval while any flagged line is unresolved (`js/rules.js` `canApprove`), the salt/pepper split is a required human decision, and a Python CI gate (`check_data_meets_kata_rules`) fails any PR whose data violates the brief.

**Why:** The brief's requirements were being represented (flags shown as colored chips) but not enforced — "Approve" worked straight past a NEEDS-APPROVAL line. The brief's principle "the system suggests and surfaces doubt; the human commits" only holds if the code cannot reach an approved/ordered state while doubt is unresolved. User direction: "take those in as rules" / "the order page needs to also function as requested in the Kata brief" — selected "Enforce brief as real rules."

**Alternatives considered:** Leave flags as display-only (rejected: doesn't meet the brief); auto-resolve the salt/pepper split to even (rejected: the brief explicitly forbids committing the split as fact — it must force a human to look).

**Date:** 2026-06-19
