import 'server-only';
import mongoose, { Schema, type InferSchemaType, type Model } from 'mongoose';

// Models in ONE file; every index declared here in code, never in the Atlas UI
// (BP §4). Use .lean() for read-only queries.
const exampleSchema = new Schema(
  {
    name: { type: String, required: true, index: true },
  },
  { timestamps: true },
);

export type ExampleDoc = InferSchemaType<typeof exampleSchema>;

export const ExampleModel: Model<ExampleDoc> =
  (mongoose.models.Example as Model<ExampleDoc> | undefined) ?? mongoose.model<ExampleDoc>('Example', exampleSchema);
