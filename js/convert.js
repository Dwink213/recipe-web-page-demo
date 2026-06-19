// convert.js — scaling + procurement conversion + order build (ES module)
//
// Turns a parsed recipe into a procurement order: scale every ingredient to the
// target servings, convert recipe grams into the unit the item is actually
// bought in, attach an illustrative line cost, and surface every ambiguity as a
// flag. Nothing here decides anything a human shouldn't — bundled lines split
// into a flagged placeholder that requires approval.

import { parseIngredient } from "./parse.js";

/**
 * @param {{yield:number, ingredients:string[]}} recipe
 * @param {number} targetServings
 * @param {Record<string, any>} procurement
 */
export function buildOrder(recipe, targetServings, procurement) {
  const scale = targetServings / recipe.yield;
  const lines = [];

  for (const ing of recipe.ingredients.map(parseIngredient)) {
    const baseFlags = [...ing.flags];

    // No quantity -> we can't scale. Carry the line and its flags, skip math.
    if (ing.amount === null || Number.isNaN(ing.amount)) {
      lines.push({
        name: ing.name,
        grams: null,
        note: ing.note,
        flags: [...baseFlags, "no quantity, cannot scale, review"],
      });
      continue;
    }

    const grams = ing.amount * scale;
    const p = procurement[ing.name];

    // Bundled (salt and pepper): split into two clean lines, even by weight,
    // each priced on its own. They are shown with a note explaining the split —
    // salt and pepper cost very differently, so the kitchen orders them
    // separately. No interactive approval on these lines.
    if (p && p.bundled) {
      for (const half of p.splitInto) {
        const line = makeLine(half, grams / 2, procurement[half], ing.note, []);
        // Tag the split so the order page can group the pair and caption it.
        line.bundle = { group: ing.name, role: half, totalGrams: grams };
        lines.push(line);
      }
      continue;
    }

    // No procurement mapping: keep grams, flag for review, never throw.
    if (!p) {
      lines.push({
        name: ing.name,
        grams,
        note: ing.note,
        flags: [...baseFlags, "no procurement mapping, review"],
      });
      continue;
    }

    lines.push(makeLine(ing.name, grams, p, ing.note, baseFlags));
  }

  return { scale, targetServings, recipeYield: recipe.yield, lines };
}

/** Build one priced order line from scaled grams and a procurement entry. */
function makeLine(name, grams, p, note, flags) {
  if (!p) {
    return {
      name,
      grams,
      note,
      flags: [...flags, "no procurement mapping, review"],
    };
  }
  const qty = convertToBuyUnit(grams, p);
  const lineCost = qty * p.pricePerBuyUnit;
  return {
    name,
    grams,
    qty,
    buyUnit: p.buyUnit,
    buyUnitLabel: p.buyUnitLabel || p.buyUnit,
    lineCost,
    priceNote: "illustrative",
    note,
    flags,
  };
}

/**
 * Convert scaled grams into the unit the item is bought in.
 *   each -> ceil (no fractional eggs)   ml -> round to 0.1   g -> grams as-is
 */
export function convertToBuyUnit(grams, p) {
  if (p.buyUnit === "each") return Math.ceil(grams / p.gramsPerUnit);
  if (p.buyUnit === "ml") return Math.round((grams / p.gramsPerMl) * 10) / 10;
  return grams; // "g"
}
