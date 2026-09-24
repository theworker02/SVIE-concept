import type { NextConfig } from "next";

const isPages =
  process.env.GITHUB_PAGES === "true" ||
  process.env.npm_lifecycle_event === "build:pages";

const repoName = (process.env.GITHUB_REPOSITORY || "theworker02/SVIE-concept").split(
  "/",
)[1];

const basePath = isPages ? `/${repoName}` : "";

const nextConfig: NextConfig = {
  ...(isPages
    ? {
        output: "export" as const,
        basePath,
        assetPrefix: `${basePath}/`,
        trailingSlash: true,
      }
    : {}),
  images: {
    unoptimized: true,
  },
  env: {
    NEXT_PUBLIC_BASE_PATH: basePath,
    NEXT_PUBLIC_SVIE_VERSION: "1.3.0",
  },
  transpilePackages: [],
  ...(!isPages
    ? {
        async rewrites() {
          const api = process.env.SVIE_API_URL || "http://127.0.0.1:8000";
          return [
            {
              source: "/api/physics/:path*",
              destination: `${api}/:path*`,
            },
          ];
        },
      }
    : {}),
};

export default nextConfig;
