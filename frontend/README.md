# LaudatorAI Frontend

Next.js frontend for the LaudatorAI application.

## Features

- Modern React with Next.js 14 (App Router)
- TypeScript for type safety
- Tailwind CSS for styling
- shadcn/ui components
- Responsive design
- Beautiful and intuitive UI

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your configuration.

### Running the Application

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Code Formatting

The project uses Prettier for code formatting. You can format code by:

1. Installing the Prettier extension in your editor
2. Running `npx prettier --write .` to format all files

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   └── ui/               # shadcn/ui components
├── lib/                  # Utility functions
└── types/                # TypeScript type definitions
```

## UI Components

The project uses shadcn/ui components which are built on top of Radix UI primitives. All components are located in `src/components/ui/`.

## Styling

The project uses Tailwind CSS for styling with a custom design system defined in `tailwind.config.js`. The design system includes:

- Custom color palette
- Typography scale
- Spacing system
- Component variants

## API Integration

The frontend communicates with the backend API. The API URL is configured via the `NEXT_PUBLIC_API_URL` environment variable.
