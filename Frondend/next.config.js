/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // 👇 Дозволяємо підключення до Next із локальної мережі
  experimental: {
    allowedDevOrigins: [
      'http://192.168.1.108:3000',  // твоя локальна адреса
      'http://localhost:3000',
    ],
  },
};

module.exports = nextConfig;
