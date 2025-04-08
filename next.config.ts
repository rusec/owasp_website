import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    /* config options here */
    output: "export",

    distDir: "./src/server/static",
    async rewrites() {
        return [
            {
                source: "/api/:path*",
                destination: `${process.env.ORIGIN || "http://localhost:5000"}/api/:path*`,
            },
        ];
    },
};

export default nextConfig;
