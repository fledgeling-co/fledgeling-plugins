/**
 * Multi-currency. Half done: conversion works, rounding does not.
 */
export type Money = { amount: number; currency: string };

export async function convert(m: Money, to: string, rate: number): Promise<Money> {
  return { amount: m.amount * rate, currency: to };
}

// TODO: tax rounding. Three defensible rules and they disagree by cents on
// every multi-line invoice:
//   (a) round each line, then sum
//   (b) sum, then round the total
//   (c) round to the smallest unit of the *destination* currency
// (b) is what the ATO examples do for AUD. (a) is what Xero does. Nobody has
// said which one Kettle should do, and the difference is a real number on a
// real invoice, so this is not mine to pick.
export function roundTax(_m: Money): Money {
  throw new Error("not implemented");
}

// Live rates need a paid feed. Fixer's free tier is daily-only and does not
// cover AUD→NZD intraday. Their $29/mo plan does.
export async function fetchRate(_from: string, _to: string): Promise<number> {
  throw new Error("no rate provider configured");
}
