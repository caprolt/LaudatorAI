import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'LaudatorAI - AI-Powered Job Application Assistant',
  description: 'Your AI advocate in the job market, automating resume tailoring and cover letter generation.',
  keywords: 'AI, resume, cover letter, job application, career, employment',
  authors: [{ name: 'LaudatorAI Team' }],
  robots: 'index, follow',
  icons: {
    icon: [
      { url: '/favicon.png', sizes: '144x144', type: 'image/png' },
      { url: '/favicon.svg', type: 'image/svg+xml' },
    ],
    shortcut: '/favicon.png',
    apple: '/favicon.png',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full antialiased`}>
        {children}
      </body>
    </html>
  )
}
