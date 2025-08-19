export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'https://laudatorai-production.up.railway.app',
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT || 'development',
  isProduction: process.env.NODE_ENV === 'production',
  isDevelopment: process.env.NODE_ENV === 'development',
} as const;

export const apiConfig = {
  baseUrl: config.apiUrl,
  endpoints: {
    health: '/health',
    jobs: '/api/v1/jobs',
    resumes: '/api/v1/resumes',
    applications: '/api/v1/applications',
    coverLetters: '/api/v1/cover-letters',
  },
} as const;
