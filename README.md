# SolarHub - IoT Dashboard for Solar Energy Systems

A full-stack IoT dashboard for monitoring solar energy storage systems including BESS (Battery Energy Storage System), PCS (Power Conversion System), inverters, and power meters.

## Project Structure

```
react_solar/
├── react_frontend/     # React + Vite + TypeScript frontend
├── fastapi_backend/    # FastAPI + SQLAlchemy backend
├── CLAUDE.md           # Development guide for AI assistants
└── README.md           # This file
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- MySQL database
- Redis server

### Frontend (React)

```bash
cd react_frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

### Backend (FastAPI)

```bash
cd fastapi_backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env       # Edit with your database credentials
uvicorn app.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Tech Stack

### Frontend
- **React 19** with TypeScript
- **Vite 7** for build tooling
- **Tailwind CSS v4** for styling
- **shadcn/ui** component library
- **Recharts** for data visualization
- **React Router DOM v7** for routing

### Backend
- **FastAPI** for REST API
- **SQLAlchemy 2.0** (async) for ORM
- **MySQL** (aiomysql) for databases
- **Redis** for real-time data caching
- **JWT** for authentication
- **Pydantic** for data validation

## Features

- Real-time monitoring of solar energy systems
- Battery storage system (BESS) management
- Power conversion system (PCS) alerts
- Inverter MPPT and string monitoring
- Power meter readings and analytics
- Energy trading schedule management
- Power loss and efficiency analysis
- User authentication and authorization
- System topology visualization

## API Documentation

See [fastapi_backend/SPEC.md](fastapi_backend/SPEC.md) for complete API documentation including:
- 28 REST endpoints
- Request/response examples
- Authentication flow
- Database architecture

## Development

### Run Tests (Backend)

```bash
cd fastapi_backend
source .venv/bin/activate
pytest tests/ -v
```

### Generate Test Report

```bash
pytest tests/ -p tests.pytest_md_report --md-report-auto
```

Reports saved to: `fastapi_backend/tests/reports/`

## License

MIT
