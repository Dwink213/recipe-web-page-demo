// parse.js — ingredient string -> structured object (ES module)
//
// The recipe JSON stores ingredients exactly as written ("100g large eggs").
// This module is the layer that structures them at boot. It never mutates the
// source; it always carries the original `raw` string forward so any parsed
// value can be audited against what was actually written.

/**
 * WHAT: Parse one raw ingredient string into {raw, amount, unit, name, note, flags}.
 * WHY:  The recipe JSON keeps ingredients exactly as written; computing on them
 *       needs structure. Unparseable input is flagged, never thrown, so a dirty
 *       meal plan can't crash the page.
 * @param {string} raw e.g. "100g large eggs" or "3g Salt and pepper (to taste)"
 * @returns {{raw:string, amount:number|null, unit:string|null, name:string, note:string|null, flags:string[]}}
 */
export function parseIngredient(raw) {
  // ^  amount  optional-unit  name  $
  const match = raw.match(/^\s*([\d.]+)\s*([a-zA-Z]+)?\s+(.+)$/);

  if (!match) {
    return {
      raw,
      amount: null,
      unit: null,
      name: raw.trim(),
      note: null,
      flags: ["unparseable, review"],
    };
  }

  const amount = Number(match[1]);
  const unit = match[2] || null;
  let name = match[3];

  // Pull any "(...)" chef note out of the name and strip it.
  let note = null;
  const noteMatch = name.match(/\(([^)]*)\)/);
  if (noteMatch) {
    note = noteMatch[1].trim();
    name = name.replace(/\([^)]*\)/, "");
  }

  name = name.toLowerCase().trim();

  const flags = [];
  if (name.includes(" and ")) flags.push("bundled, multiple SKUs, review");
  if (amount === null || Number.isNaN(amount)) flags.push("no quantity, review");

  return { raw, amount, unit, name, note, flags };
}
