# SolarHub FastAPI Backend

FastAPI-based IoT Dashboard API for Solar Energy Storage Systems.

This is a complete migration from the Flask backend with:
- Async SQLAlchemy 2.0 for database operations
- Async Redis for caching
- JWT authentication
- Automatic OpenAPI documentation
- Pydantic v2 for validation

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL databases (as configured in original Flask app)
- Redis instances (main + GTR)

### Installation

```bash
cd /home/datavan/react_solar/fastapi

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Copy and configure environment
cp .env.example .env
# Edit .env with your database credentials
```

### Running the Server

```bash
# Development (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Project Structure

```
fastapi/
├── app/
│   ├── main.py              # FastAPI application entry
│   ├── core/                # Configuration & security
│   │   ├── config.py        # Pydantic Settings
│   │   ├── security.py      # JWT & password utilities
│   │   └── exceptions.py    # Custom exceptions
│   ├── db/                  # Database layer
│   │   ├── session.py       # Multi-DB async sessions
│   │   ├── redis.py         # Async Redis client
│   │   └── base.py          # SQLAlchemy base
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic response models
│   ├── services/            # Business logic
│   ├── api/                 # API routes
│   │   ├── deps.py          # Dependency injection
│   │   └── v1/              # Version 1 endpoints
│   └── utils/               # Utilities
├── tests/                   # Pytest test suite
├── pyproject.toml           # Project dependencies
└── .env.example             # Environment template
```

## API Endpoints

### Health & System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Health check |
| GET | `/api/v1/system/overview` | System overview |
| GET | `/api/v1/system/topology` | Network topology |

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | OAuth2 login |
| POST | `/api/v1/auth/login/json` | JSON login |
| POST | `/api/v1/auth/refresh` | Refresh token |
| GET | `/api/v1/auth/me` | Current user info |
| POST | `/api/v1/auth/logout` | Logout |

### BESS (Battery Energy Storage)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/bess/{bess_number}` | BESS unit info |
| GET | `/api/v1/bess/alert/rack/{rack_number}` | Rack alerts |

### PCS (Power Conversion)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/pcs/{pcs_number}` | PCS unit info |
| GET | `/api/v1/pcs/alert` | PCS alert status |

### Meters
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/meters` | All meter data |
| GET | `/api/v1/meters/aux` | Auxiliary meter |

### Inverter
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/inverter` | Inverter data |

### Schedule & Income
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/schedule` | Schedule events |
| GET | `/api/v1/schedule/income/daily` | Daily income |
| GET | `/api/v1/schedule/income/monthly` | Monthly income |
| GET | `/api/v1/schedule/exec-rate` | Execution rate |

### Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/analysis/power-loss` | Power loss & efficiency |
| GET | `/api/v1/analysis/power-io` | Charge/discharge energy |
| GET | `/api/v1/analysis/freq-power` | Frequency & power chart |

### Configuration
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/config/sidebar` | Sidebar config |
| GET | `/api/v1/config/header` | Header alerts |

## Flask to FastAPI Mapping

| Flask Endpoint | FastAPI Endpoint |
|----------------|------------------|
| `/api/health` | `/health` |
| `/api/system_overview` | `/api/v1/system/overview` |
| `/api/topology` | `/api/v1/system/topology` |
| `/api/bams_info/<n>` | `/api/v1/bess/{n}` |
| `/api/alert/rack/<n>` | `/api/v1/bess/alert/rack/{n}` |
| `/api/pcs_info/<n>` | `/api/v1/pcs/{n}` |
| `/api/alert/pcs` | `/api/v1/pcs/alert` |
| `/api/meter_info` | `/api/v1/meters` |
| `/api/aux_meter` | `/api/v1/meters/aux` |
| `/api/converter` | `/api/v1/inverter` |
| `/api/schedule` | `/api/v1/schedule` |
| `/api/income/day` | `/api/v1/schedule/income/daily` |
| `/api/income/month` | `/api/v1/schedule/income/monthly` |
| `/api/exec_rate` | `/api/v1/schedule/exec-rate` |
| `/api/power_loss` | `/api/v1/analysis/power-loss` |
| `/api/power_io` | `/api/v1/analysis/power-io` |
| `/api/freq_power` | `/api/v1/analysis/freq-power` |
| `/api/sidebar_info` | `/api/v1/config/sidebar` |
| `/api/header_info` | `/api/v1/config/header` |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_health.py -v
```

## Development

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy app
```

## Environment Variables

See `.env.example` for all configuration options. Key variables:

- `DB_HOST`, `DB_USER`, `DB_PASSWORD` - Main database
- `DB_HOST_GTR` - GTR database host
- `REDIS_HOST`, `REDIS_PORT` - Main Redis
- `REDIS_HOST_GTR`, `REDIS_PORT_GTR` - GTR Redis
- `JWT_SECRET_KEY` - JWT signing key
- `BESS_NUMBER`, `PCS_NUMBER`, etc. - System configuration

## Migration Notes

### Key Changes from Flask

1. **Async/Await**: All database and Redis operations are async
2. **Pydantic**: Request/response validation with Pydantic v2
3. **JWT Auth**: Stateless JWT instead of Flask-Security sessions
4. **Type Hints**: Full type annotations throughout
5. **Dependency Injection**: FastAPI's DI system for database sessions
6. **Auto Documentation**: OpenAPI 3.1 generated automatically

### Database Connections

The app manages 8+ database connections:
- ESS, Schedule, Meter, PCS, Inverter, Baseline
- BESS1-12 (individual BESS unit databases)
- GTR server (remote)

All connections use async SQLAlchemy 2.0 with aiomysql driver.

### Redis Connections

Two Redis instances:
- **Main**: Real-time meter data, monitoring
- **GTR**: BESS/PCS data, energy trading

Both use async redis-py with connection pooling.

## License

Proprietary - SolarHub
