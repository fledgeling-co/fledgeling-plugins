// Single source of truth for entity shapes (BP §4): TS types here, Zod at
// boundaries, Mongoose schemas mirror them — keep all three in sync in ONE edit.
export type User = {
  _id: string;
  email: string;
  createdAt: Date;
  pushTokens?: string[];
};
