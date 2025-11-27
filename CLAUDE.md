# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SolarHub is a full-stack IoT dashboard for monitoring solar energy systems. It consists of:
- **react_frontend/** - React-based dashboard UI
- **fastapi_backend/** - FastAPI REST API server

## Repository Structure

```
react_solar/
├── react_frontend/     # React + Vite frontend
│   ├── src/
│   ├── package.json
│   └── ...
├── fastapi_backend/    # FastAPI backend
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   └── SPEC.md         # API specification
└── CLAUDE.md           # This file
```

---

## React Frontend (react_frontend/)

### Commands

```bash
cd react_frontend
npm run dev      # Start development server (Vite) - http://localhost:5173
npm run build    # TypeScript check + production build
npm run lint     # Run ESLint
npm run preview  # Preview production build
```

### Tech Stack

- **Framework**: React 19 with TypeScript
- **Build**: Vite 7
- **Routing**: React Router DOM v7
- **Styling**: Tailwind CSS v4 with CSS variables (oklch color space)
- **UI Components**: shadcn/ui (new-york style)
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod validation
- **Icons**: Lucide React

### Architecture

#### Path Aliases
`@/*` maps to `./src/*` (configured in tsconfig.json and vite.config.ts)

#### Layout Structure
- `src/App.tsx` - Route definitions with React Router
- `src/components/dashboard-layout.tsx` - Main layout wrapper using SidebarProvider
- `src/components/app-sidebar.tsx` - Navigation sidebar with menu data
- `src/components/header.tsx` - Top header with search and theme toggle

#### Key Directories
- `src/pages/` - Page components (dashboard, devices, analytics, energy, battery, users, alerts, settings, login)
- `src/components/ui/` - shadcn/ui primitives (do not edit directly, use `npx shadcn add <component>`)
- `src/components/` - Custom components (nav-main, nav-user, nav-projects, team-switcher)
- `src/lib/` - Utilities and mock data
- `src/hooks/` - Custom React hooks

#### Theming
Theme colors defined in `src/index.css` using CSS variables with oklch color space. Sidebar has separate color variables (`--sidebar-*`). Theme toggle via `src/components/theme-provider.tsx`.

### Adding shadcn Components

```bash
cd react_frontend
npx shadcn add <component-name>
```

Components install to `src/components/ui/`. The project uses `new-york` style with `neutral` base color.

---

## FastAPI Backend (fastapi_backend/)

### Commands

```bash
cd fastapi_backend
source .venv/bin/activate

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests with markdown report
pytest tests/ -p tests.pytest_md_report --md-report-auto

# API Documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: MySQL (async via aiomysql)
- **Cache**: Redis (async)
- **Auth**: JWT tokens
- **ORM**: SQLAlchemy 2.0 (async)

### Architecture

#### Key Directories
- `app/api/v1/` - API route handlers
- `app/models/` - SQLAlchemy ORM models
- `app/schemas/` - Pydantic request/response schemas
- `app/services/` - Business logic
- `app/db/` - Database and Redis connection management
- `app/core/` - Configuration, security, exceptions
- `tests/` - Pytest test suite with auto-generated reports

### API Endpoints

See `fastapi_backend/SPEC.md` for complete API documentation including:
- 28 REST endpoints
- Request/response examples
- Authentication flow
- Database architecture

### Environment Setup

```bash
cd fastapi_backend
cp .env.example .env
# Edit .env with database credentials
```
