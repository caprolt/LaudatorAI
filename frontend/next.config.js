/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable experimental features for better logging
  experimental: {
    // Enable server actions for better error tracking
    serverActions: true,
  },
  
  // Configure logging for production
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
  
  // Add headers for better monitoring
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          // Add custom header for logging
          {
            key: 'X-LaudatorAI-Version',
            value: process.env.npm_package_version || '0.1.0',
          },
        ],
      },
    ];
  },
  
  // Configure environment variables for logging
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
    NODE_ENV: process.env.NODE_ENV,
    VERCEL_ENV: process.env.VERCEL_ENV,
    VERCEL_URL: process.env.VERCEL_URL,
  },
  
  // Enable source maps for better error tracking in production
  productionBrowserSourceMaps: true,
  
  // Configure webpack for better error reporting
  webpack: (config, { dev, isServer }) => {
    // Add source maps for better error tracking
    if (!dev && !isServer) {
      config.devtool = 'source-map';
    }
    
    return config;
  },
};

module.exports = nextConfig;
