// parse.js — ingredient string -> structured object (ES module)
//
// The recipe JSON stores ingredients exactly as written ("100g large eggs").
// This module is the layer that structures them at boot. It never mutates the
// source; it always carries the original `raw` string forward so any parsed
// value can be audited against what was actually written.

/**
 * Parse a single raw ingredient string into a structured object.
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

/**
 * Parse every ingredient on a recipe and join each to the procurement table.
 * A missing procurement match adds a flag; it never throws.
 * @param {{ingredients:string[]}} recipe
 * @param {Record<string, any>} procurement
 */
export function parseRecipeIngredients(recipe, procurement = {}) {
  return recipe.ingredients.map((raw) => {
    const ing = parseIngredient(raw);
    if (procurement[ing.name] === undefined) {
      ing.flags = [...ing.flags, "no procurement mapping, review"];
    }
    return ing;
  });
}
