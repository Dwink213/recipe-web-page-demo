// rules.js — the Kata brief's logic, encoded as ENFORCEABLE rules.
//
// The brief is the contract, not a design note. These rules are applied at
// runtime so the order page *enforces* the brief instead of merely displaying
// flags. The core rule: "the system suggests and surfaces doubt; the human
// commits." That only holds if the code cannot reach an approved order while a
// flagged line is unresolved.

// Every flag a recipe line can carry, classified by how strongly it gates an
// order. A "blocker" must be resolved by a human before the order can be
// approved; an "info" flag is advisory and never blocks.
export const FLAG_SEVERITY = {
  "suggested even-split placeholder, NEEDS APPROVAL": "blocker",
  "no procurement mapping, review": "blocker",
  "no quantity, cannot scale, review": "blocker",
  "unparseable, review": "blocker",
  "bundled, multiple SKUs, review": "info",
  "no quantity, review": "info",
};

export function flagSeverity(flag) {
  return FLAG_SEVERITY[flag] ?? "info";
}

/** A line blocks approval if it carries any blocker-severity flag. */
export function isBlocking(flags) {
  return flags.some((f) => flagSeverity(f) === "blocker");
}

/**
 * The brief's approval gate, as a pure rule.
 * @param {Array<{id:any, flags:string[]}>} lines  the built order lines
 * @param {(id:any)=>boolean} isSettled  has the human resolved this line id?
 * @returns {boolean} true only when every blocking line has been settled
 */
export function canApprove(lines, isSettled) {
  return lines.every((l) => !isBlocking(l.flags) || isSettled(l.id));
}

/** How many blocking lines still need a human decision. */
export function unresolvedCount(lines, isSettled) {
  return lines.filter((l) => isBlocking(l.flags) && !isSettled(l.id)).length;
}
