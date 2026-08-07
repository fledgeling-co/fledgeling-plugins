import 'server-only';
import mongoose, { Schema, type InferSchemaType, type Model } from 'mongoose';

// Models in ONE file; every index declared in code (BP §4). .lean() for reads.
const userSchema = new Schema(
  {
    email: { type: String, required: true, unique: true, index: true, lowercase: true, trim: true },
    // APNs device tokens (push module); select:false keeps them out of default reads.
    pushTokens: { type: [String], default: [], select: false },
  },
  { timestamps: true },
);

export type UserDoc = InferSchemaType<typeof userSchema>;

export const UserModel: Model<UserDoc> =
  (mongoose.models.User as Model<UserDoc> | undefined) ?? mongoose.model<UserDoc>('User', userSchema);
