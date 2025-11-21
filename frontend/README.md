# Frontend

React + TypeScript frontend for the hackathon project.

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Make sure `.env` file exists (it should be created automatically)

3. Run the development server:
```bash
npm run dev
```

4. Visit http://localhost:5173

## Available Scripts

- `npm run dev` - Start development server with HMR
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint TypeScript/React code

## Structure

- `src/main.tsx` - Application entry point
- `src/App.tsx` - Main app component with routing
- `src/models/` - TypeScript type definitions
- `src/services/` - API client and utilities
- `src/components/` - Reusable React components
- `src/pages/` - Page components

## Building for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

