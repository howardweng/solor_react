# SolarHub API Specification

**Version:** 1.0.0
**Framework:** FastAPI (Python 3.11+)
**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Authentication](#authentication)
5. [API Endpoints](#api-endpoints)
   - [Health Check](#health-check-endpoints)
   - [Authentication](#authentication-endpoints)
   - [System](#system-endpoints)
   - [BESS (Battery)](#bess-endpoints)
   - [PCS (Power Conversion)](#pcs-endpoints)
   - [Meters](#meter-endpoints)
   - [Inverter](#inverter-endpoints)
   - [Schedule & Income](#schedule--income-endpoints)
   - [Analysis](#analysis-endpoints)
   - [Configuration](#configuration-endpoints)
6. [Data Models](#data-models)
7. [Database Architecture](#database-architecture)
8. [Error Handling](#error-handling)
9. [Environment Configuration](#environment-configuration)
10. [Testing](#testing)

---

## Overview

SolarHub API is an IoT Dashboard backend for monitoring and managing Solar Energy Storage Systems. It provides real-time data access for:

- **BESS** (Battery Energy Storage System) - 12 units with 12 racks each
- **PCS** (Power Conversion System) - 12 units
- **Inverters** - Solar inverter monitoring with MPPT data
- **Meters** - Power meter readings and analytics
- **Schedule** - Energy trading schedule management
- **Analysis** - Power loss, efficiency, and frequency analysis

### Key Features

- Async/await architecture for high performance
- Multi-database support (18 MySQL databases)
- Dual Redis instances (Main + GTR)
- JWT-based authentication
- Graceful degradation when services are unavailable
- Comprehensive health checks for Kubernetes

---

## Project Structure

```
fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── api/
│   │   ├── deps.py             # Dependency injection
│   │   └── v1/
│   │       ├── router.py       # API router
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── system.py       # System overview/topology
│   │       ├── bess.py         # BESS endpoints
│   │       ├── pcs.py          # PCS endpoints
│   │       ├── meters.py       # Meter endpoints
│   │       ├── inverter.py     # Inverter endpoints
│   │       ├── schedule.py     # Schedule/income endpoints
│   │       ├── analysis.py     # Analysis endpoints
│   │       └── config.py       # Configuration endpoints
│   ├── core/
│   │   ├── config.py           # Pydantic settings
│   │   ├── security.py         # JWT utilities
│   │   └── exceptions.py       # Custom exceptions
│   ├── db/
│   │   ├── base.py             # SQLAlchemy base
│   │   ├── session.py          # Database manager
│   │   └── redis.py            # Redis manager
│   ├── models/                 # SQLAlchemy ORM models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   └── utils/                  # Utilities
├── tests/
│   ├── conftest.py             # Test fixtures
│   ├── pytest_md_report.py     # Custom report plugin
│   ├── reports/                # Test reports
│   └── test_*.py               # Test files
├── pyproject.toml              # Project configuration
├── .env.example                # Environment template
└── SPEC.md                     # This file
```

---

## Quick Start

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -e ".[dev]"

# 3. Copy and configure environment
cp .env.example .env
# Edit .env with your database credentials

# 4. Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Access API docs
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## Authentication

### JWT Token Flow

1. **Login** - POST `/api/v1/auth/login` with username/password
2. **Receive Tokens** - Get `access_token` (30min) and `refresh_token` (7 days)
3. **Use Token** - Include in header: `Authorization: Bearer <access_token>`
4. **Refresh** - POST `/api/v1/auth/refresh` when access token expires

### Token Structure

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## API Endpoints

### Health Check Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | Service info and docs link | No |
| `GET` | `/health` | Basic health check (always returns healthy if API is running) | No |
| `GET` | `/health/detailed` | Full infrastructure status (DB + Redis) | No |
| `GET` | `/health/live` | Kubernetes liveness probe | No |
| `GET` | `/health/ready` | Kubernetes readiness probe (503 if no DB) | No |

#### Response Examples

**GET /**
```json
{
  "service": "SolarHub API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

**GET /health/detailed**
```json
{
  "status": "healthy",
  "service": "SolarHub API",
  "version": "1.0.0",
  "infrastructure": {
    "databases": {
      "status": "healthy",
      "connections": {
        "ess": true,
        "schedule": true,
        "meter": true,
        "pcs": true,
        "inverter": true,
        "baseline": true
      }
    },
    "redis": {
      "status": "healthy",
      "connections": {
        "main": true,
        "gtr": true
      }
    }
  },
  "message": "All systems operational"
}
```

---

### Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/auth/login` | OAuth2 form-based login | No |
| `POST` | `/api/v1/auth/login/json` | JSON-based login | No |
| `POST` | `/api/v1/auth/refresh` | Refresh access token | No |
| `GET` | `/api/v1/auth/me` | Get current user info | Yes |
| `POST` | `/api/v1/auth/logout` | Logout (client-side token discard) | Yes |

#### Request/Response Examples

**POST /api/v1/auth/login** (Form)
```
Content-Type: application/x-www-form-urlencoded

username=admin&password=secret
```

**POST /api/v1/auth/login/json**
```json
{
  "username": "admin",
  "password": "secret"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**GET /api/v1/auth/me**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "active": true,
  "confirmed_at": "2024-01-01T00:00:00",
  "roles": [
    {"id": 1, "name": "admin", "description": "Administrator"}
  ]
}
```

---

### System Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/system/overview` | System overview data | No |
| `GET` | `/api/v1/system/topology` | Infrastructure topology graph | No |

#### Response Examples

**GET /api/v1/system/topology**
```json
{
  "nodes": [
    {
      "id": "main_server",
      "name": "Main Server",
      "type": "server",
      "status": "online",
      "ip": "localhost"
    },
    {
      "id": "main_mysql",
      "name": "Main MySQL",
      "type": "database",
      "status": "online",
      "ip": "localhost",
      "port": 3306
    },
    {
      "id": "main_redis",
      "name": "Main Redis",
      "type": "redis",
      "status": "online",
      "ip": "localhost",
      "port": 6379
    }
  ],
  "links": [
    {
      "source": "main_server",
      "target": "main_mysql",
      "status": "connected"
    }
  ],
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### BESS Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/bess/{bess_number}` | Get BESS unit info (1-12) | No |
| `GET` | `/api/v1/bess/alert/rack/{rack_number}` | Get rack alerts (rack01-rack12) | No |

#### Parameters

- `bess_number`: Integer 1-12
- `rack_number`: String pattern `rack01` to `rack12`

#### Response Examples

**GET /api/v1/bess/1**
```json
{
  "bess_number": 1,
  "table_head": ["Rack 01", "Rack 02", ..., "Rack 12"],
  "data": [
    {
      "metric": "Mode",
      "Rack 01": "Standby",
      "Rack 02": "Charging",
      ...
    },
    {
      "metric": "Voltage (V)",
      "Rack 01": "750.5",
      "Rack 02": "748.2",
      ...
    },
    {
      "metric": "SOC (%)",
      "Rack 01": "85.2",
      "Rack 02": "72.1",
      ...
    }
  ],
  "status": "success"
}
```

**GET /api/v1/bess/alert/rack/rack01**
```json
{
  "rack_number": "rack01",
  "battery_alerts": {
    "battery_1_protection": "正常",
    "battery_1_alarm": "正常",
    "battery_1_warning": "正常",
    ...
  },
  "bams_alerts": {
    "bams_64_status": "正常",
    "bams_65_status": "正常",
    ...
  },
  "status": "success"
}
```

---

### PCS Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/pcs/{pcs_number}` | Get PCS unit info (1-12) | No |
| `GET` | `/api/v1/pcs/alert` | Get PCS alert status (16-bit binary) | No |

#### Response Examples

**GET /api/v1/pcs/1**
```json
{
  "pcs_number": 1,
  "status": "success"
}
```

**GET /api/v1/pcs/alert**
```json
{
  "inverter_status": "0000000000000000",
  "inverter_inhibits1_status": "0000000000000000",
  "environment_status": "0000000000000000",
  "warning_status": "0000000000000000",
  "grid_status": "0000000000000000",
  "fault_status1": "0000000000000000",
  "fault_status2": "0000000000000000",
  "status": "success"
}
```

---

### Meter Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/meters` | Get all meter info | No |
| `GET` | `/api/v1/meters/aux` | Get auxiliary meter data | No |

#### Query Parameters (aux endpoint)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `time` | date | today | Date filter (YYYY-MM-DD) |
| `data_type` | string | "chart" | Response type: `chart` or `summary` |

#### Response Examples

**GET /api/v1/meters**
```json
{
  "meters": [
    {
      "meter_id": 1,
      "phase_a_current": 125.5,
      "phase_b_current": 124.8,
      "phase_c_current": 126.2,
      "phase_a_voltage": 220.1,
      "phase_b_voltage": 219.8,
      "phase_c_voltage": 220.5,
      "active_power": 82.5,
      "reactive_power": 12.3,
      "apparent_power": 83.4,
      "frequency": 60.01,
      "power_factor": 0.98
    }
  ],
  "meter_count": 1,
  "total_power": 82.5,
  "status": "success"
}
```

**GET /api/v1/meters/aux?data_type=summary**
```json
{
  "data": {
    "total_energy": 1250.5,
    "avg_power": 52.1,
    "max_power": 98.5,
    "min_power": 12.3
  },
  "data_type": "summary",
  "status": "success"
}
```

---

### Inverter Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/inverter` | Get inverter data (MPPT, strings, phases) | No |

#### Response Example

**GET /api/v1/inverter**
```json
{
  "inverter_data": {
    "nominal_active_power": 500.0,
    "total_active_power": 425.5,
    "total_apparent_power": 432.1,
    "total_reactive_power": 45.2,
    "daily_power_yields": 2850.5,
    "total_power_yields": 125000.0,
    "internal_temperature": 45.2,
    "bus_voltage": 650.5,
    "dc_power": 430.2
  },
  "mppt_data": [
    {"mppt_id": 1, "voltage": 580.5, "current": 12.5, "power": 7256.25},
    {"mppt_id": 2, "voltage": 575.2, "current": 12.3, "power": 7074.96},
    ...
  ],
  "string_currents": [
    {"string_id": 1, "current": 6.25},
    {"string_id": 2, "current": 6.15},
    ...
  ],
  "phase_data": [
    {"phase": "A", "voltage": 220.5, "current": 125.5},
    {"phase": "B", "voltage": 219.8, "current": 124.8},
    {"phase": "C", "voltage": 220.2, "current": 126.2}
  ],
  "status": "success"
}
```

---

### Schedule & Income Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/schedule` | Get schedule events | No |
| `GET` | `/api/v1/schedule/income/daily` | Get daily income breakdown | No |
| `GET` | `/api/v1/schedule/income/monthly` | Get monthly income summary | No |
| `GET` | `/api/v1/schedule/exec-rate` | Get execution rate time-series | No |

#### Query Parameters

**GET /api/v1/schedule**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | string | "all" | Filter: all, dreg, edreg, test_mode, step, scan, full_power |
| `weeks` | int | 1 | Number of weeks to fetch (1-52) |

**GET /api/v1/schedule/income/daily**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_time` | datetime | today | Start time (YYYY-MM-DD HH:MM:SS) |

**GET /api/v1/schedule/income/monthly**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_time` | string | Yes | Month (YYYY-MM format) |

**GET /api/v1/schedule/exec-rate**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date` | datetime | Yes | Date (YYYY-MM-DD HH:MM:SS) |
| `data_type` | string | No | exec_rate, roll_exec_rate, hour_exec_rate |

#### Response Examples

**GET /api/v1/schedule**
```json
{
  "events": [
    {
      "index": 1,
      "mode": "dreg",
      "time_number": 15,
      "time_start": "2024-01-01T14:00:00",
      "time_end": "2024-01-01T15:00:00",
      "time_date": "2024-01-01T00:00:00",
      "is_get": true,
      "interrupt": false,
      "quote_capacity": 5.0,
      "power": 4.5,
      "price": 850.0,
      "quote_price": 900.0,
      "quote_code": "QC001",
      "title": "D-Reg Dispatch",
      "description": "Frequency regulation"
    }
  ],
  "mode": "all",
  "weeks": 1,
  "total_count": 1
}
```

**GET /api/v1/schedule/income/daily**
```json
{
  "date": "2024-01-01",
  "hourly_data": [
    {
      "hour": 0,
      "capacity_fee": 125.50,
      "efficiency_fee": 45.25,
      "exec_rate": 0.95,
      "performance_index": 1.02
    }
  ],
  "total_capacity_fee": 3012.00,
  "total_efficiency_fee": 1085.50,
  "total_income": 4097.50,
  "avg_exec_rate": 0.92,
  "avg_performance_index": 0.98
}
```

---

### Analysis Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/analysis/power-loss` | Get power loss and efficiency | No |
| `GET` | `/api/v1/analysis/power-io` | Get charge/discharge energy data | No |
| `GET` | `/api/v1/analysis/freq-power` | Get frequency-power chart data | No |

#### Query Parameters

**GET /api/v1/analysis/power-loss**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_time` | datetime | Yes | Start time (YYYY-MM-DD HH:MM:SS) |

**GET /api/v1/analysis/power-io**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `select_time` | date | Yes | Date (YYYY-MM-DD) |
| `data_type` | string | No | daily or monthly |

**GET /api/v1/analysis/freq-power**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date_period` | int | Yes | Period in minutes |
| `select_time` | datetime | No | Specific time |
| `select_mode` | string | No | normalMode or selectTimeMode |

#### Response Examples

**GET /api/v1/analysis/power-loss?start_time=2024-01-01%2000:00:00**
```json
{
  "start_date": "2024-01-01",
  "daily_data": [
    {
      "date": "2024-01-01",
      "discharge_energy": 450.5,
      "charge_energy": 480.2,
      "loss": 29.7,
      "efficiency": 93.8,
      "aux_consumption": 15.2
    }
  ],
  "total_discharge": 450.5,
  "total_charge": 480.2,
  "total_loss": 29.7,
  "avg_efficiency": 93.8,
  "total_aux": 15.2
}
```

**GET /api/v1/analysis/freq-power?date_period=60**
```json
{
  "date_period": 60,
  "select_time": null,
  "select_mode": "normalMode",
  "frequency_data": [[1704067200000, 60.01], [1704070800000, 59.98], ...],
  "power_data": [[1704067200000, 125.5], [1704070800000, 128.2], ...],
  "baseline_data": [[1704067200000, 60.0], [1704070800000, 60.0], ...]
}
```

---

### Configuration Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/config/sidebar` | Get sidebar configuration | No |
| `GET` | `/api/v1/config/header` | Get header alert summary | No |

#### Response Examples

**GET /api/v1/config/sidebar**
```json
{
  "bess_type": "BESS",
  "bess_number": 2,
  "pcs_number": 2,
  "inverter_number": 2,
  "rack_number": 12,
  "number_of_devices": 18,
  "cctv_url": "http://cctv.example.com/stream",
  "status": "success"
}
```

**GET /api/v1/config/header**
```json
{
  "protection_info": {
    "count": 0,
    "items": []
  },
  "warning_info": {
    "count": 2,
    "items": ["BESS1: High Temperature", "PCS2: Communication Delay"]
  },
  "fault_info": {
    "count": 0,
    "items": []
  },
  "status": "success"
}
```

---

## Data Models

### Common Response Fields

All API responses include:
```json
{
  "status": "success",
  ...data fields...
}
```

### User Model

| Field | Type | Description |
|-------|------|-------------|
| id | int | User ID |
| username | string | Username (3-80 chars) |
| email | string | Email address |
| active | bool | Account active status |
| confirmed_at | datetime | Email confirmation timestamp |
| roles | Role[] | Assigned roles |

### Topology Node

| Field | Type | Description |
|-------|------|-------------|
| id | string | Node identifier |
| name | string | Display name |
| type | string | server, database, redis |
| status | string | online, offline |
| ip | string | IP address |
| port | int | Port number (optional) |

---

## Database Architecture

### MySQL Databases

| Database | Purpose |
|----------|---------|
| ess | User accounts, roles, alerts |
| schedule | Energy trading schedules |
| Meter | Power meter readings |
| PCS | Power conversion system data |
| Inverter | Inverter telemetry |
| BaseLine | Frequency baseline data |
| BESS1-12 | Battery system data (per unit) |

### Redis Instances

| Instance | Purpose |
|----------|---------|
| Main | Real-time sensor data cache |
| GTR | GTR server data synchronization |

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid/missing token |
| 403 | Forbidden - Inactive user or insufficient permissions |
| 404 | Not Found |
| 422 | Validation Error - Invalid input format |
| 503 | Service Unavailable - Database connection failed |

### Error Response Format

```json
{
  "detail": "Error message description"
}
```

### Validation Error Format (422)

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["query", "pcs_number"],
      "msg": "Input should be greater than or equal to 1",
      "input": 0
    }
  ]
}
```

---

## Environment Configuration

Create `.env` file from `.env.example`:

```bash
# Application
APP_ENV=development          # development, staging, production
DEBUG=true
SECRET_KEY=your-secret-key

# Main Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME_ESS=ess
DB_NAME_SCHEDULE=schedule
DB_NAME_METER=Meter
DB_NAME_PCS=PCS
DB_NAME_INVERTER=Inverter
DB_NAME_BASELINE=BaseLine

# BESS Databases (1-12)
DB_NAME_BESS1=BESS1
...
DB_NAME_BESS12=BESS12

# GTR Database
DB_HOST_GTR=192.168.10.46
DB_USER_GTR=root
DB_PASSWORD_GTR=

# Redis - Main
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Redis - GTR
REDIS_HOST_GTR=192.168.10.46
REDIS_PORT_GTR=6379
REDIS_PASSWORD_GTR=

# System Configuration
BESS_NUMBER=2
PCS_NUMBER=2
RACK_NUMBER=12
INVERTER_NUMBER=2
BESS_TYPE=BESS
PCS_TYPE=PCS

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## Testing

### Run Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests with verbose output
pytest tests/ -v

# Run with markdown report (auto-generated timestamp)
pytest tests/ -p tests.pytest_md_report --md-report-auto

# Run specific test file
pytest tests/test_bess.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Report Location

Reports are generated in `tests/reports/`:
- Latest report: `tests/reports/test_report_YYYY-MM-DD_HH-MM-SS.md`
- Archived reports: `tests/reports/archive/`

### Test Categories

| Test File | Endpoints Covered |
|-----------|-------------------|
| test_health.py | Health check endpoints |
| test_auth.py | Authentication endpoints |
| test_bess.py | BESS unit and rack alerts |
| test_pcs.py | PCS unit and alerts |
| test_meters.py | Meter info and aux data |
| test_inverter.py | Inverter data |
| test_schedule.py | Schedule and income |
| test_analysis.py | Power analysis |
| test_config.py | Sidebar and header config |
| test_system.py | System overview and topology |

### Graceful Test Skipping

Tests that require database connectivity will be **skipped** (not failed) when:
- Database returns 503 (Service Unavailable)
- Database connection timeout

This allows CI/CD pipelines to pass even when databases are unavailable.

---

## Frontend Integration Notes

### CORS

CORS is enabled for all origins in development. Configure for production:

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication Header

```javascript
// Frontend fetch example
const response = await fetch('/api/v1/bess/1', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});
```

### WebSocket (Future)

Real-time updates will be available via WebSocket at `/ws` (not yet implemented).

---

## API Documentation URLs

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

*Last Updated: 2025-11-28*
