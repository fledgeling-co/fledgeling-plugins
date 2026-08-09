import type { MetadataRoute } from "next";
import { getSkills } from "@/lib/skills";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://skills.fledgeling.app";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: SITE_URL, changeFrequency: "weekly", priority: 1 },
    { url: `${SITE_URL}/install`, changeFrequency: "monthly", priority: 0.6 },
    ...getSkills().map((skill) => ({
      url: `${SITE_URL}/skills/${skill.name}`,
      changeFrequency: "weekly" as const,
      priority: 0.8,
    })),
  ];
}
