# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SolarHub is a React-based IoT dashboard for monitoring solar energy systems. It displays real-time data for solar panels, inverters, batteries, and energy production/consumption.

## Commands

```bash
npm run dev      # Start development server (Vite)
npm run build    # TypeScript check + production build
npm run lint     # Run ESLint
npm run preview  # Preview production build
```

## Tech Stack

- **Framework**: React 19 with TypeScript
- **Build**: Vite 7
- **Routing**: React Router DOM v7
- **Styling**: Tailwind CSS v4 with CSS variables (oklch color space)
- **UI Components**: shadcn/ui (new-york style)
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod validation
- **Icons**: Lucide React

## Architecture

### Path Aliases
`@/*` maps to `./src/*` (configured in tsconfig.json and vite.config.ts)

### Layout Structure
- `src/App.tsx` - Route definitions with React Router
- `src/components/dashboard-layout.tsx` - Main layout wrapper using SidebarProvider
- `src/components/app-sidebar.tsx` - Navigation sidebar with menu data
- `src/components/header.tsx` - Top header with search and theme toggle

### Key Directories
- `src/pages/` - Page components (dashboard, devices, analytics, energy, battery, users, alerts, settings, login)
- `src/components/ui/` - shadcn/ui primitives (do not edit directly, use `npx shadcn add <component>`)
- `src/components/` - Custom components (nav-main, nav-user, nav-projects, team-switcher)
- `src/lib/` - Utilities and mock data
- `src/hooks/` - Custom React hooks

### Theming
Theme colors defined in `src/index.css` using CSS variables with oklch color space. Sidebar has separate color variables (`--sidebar-*`). Theme toggle via `src/components/theme-provider.tsx`.

### Sidebar Navigation
Navigation is defined in `src/components/app-sidebar.tsx` data object. Supports 3-level nested menus via collapsible components in `nav-main.tsx`.

## Adding shadcn Components

```bash
npx shadcn add <component-name>
```

Components install to `src/components/ui/`. The project uses `new-york` style with `neutral` base color.
