/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Serve /public images directly instead of via the /_next/image optimizer,
  // which was failing on the Vercel deployment (broken logo and screenshots).
  images: { unoptimized: true },
};

export default nextConfig;
