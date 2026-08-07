// Single source of truth for entity shapes (BP §4): define TS types here, derive
// Zod schemas from them at boundaries, mirror them in Mongoose schemas — keep all
// three in sync in ONE edit.
export type Example = {
  _id: string;
  name: string;
  createdAt: Date;
};
