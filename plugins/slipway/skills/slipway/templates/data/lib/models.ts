import 'server-only';
import mongoose, { Schema } from 'mongoose';

// Models in ONE file; every index declared here in code, never in the Atlas UI
// (BP §4). Use .lean() for read-only queries.
const exampleSchema = new Schema(
  {
    name: { type: String, required: true, index: true },
  },
  { timestamps: true },
);

export const ExampleModel =
  mongoose.models.Example ?? mongoose.model('Example', exampleSchema);
