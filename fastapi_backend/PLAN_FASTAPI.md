# Flask to FastAPI Migration Plan

## Overview

**Project**: SolarHub IoT Dashboard API
**Source**: `/home/datavan/react_solar/_solar_frontend` (Flask)
**Target**: `/home/datavan/react_solar/fastapi` (FastAPI)
**Goal**: Complete migration with identical API spec, async performance, and automatic OpenAPI docs

---

## Current Flask Architecture Analysis

### Tech Stack (Flask)
| Component | Current | Target |
|-----------|---------|--------|
| Framework | Flask 2.x | FastAPI 0.115+ |
| ORM | SQLAlchemy (sync) | SQLAlchemy 2.0 (async) |
| Auth | Flask-Security | FastAPI Security + JWT |
| Docs | Flasgger (Swagger 2.0) | FastAPI (OpenAPI 3.1) |
| Validation | Manual | Pydantic v2 |
| Redis | redis-py (sync) | redis-py (async) |
| Server | Flask dev / Gunicorn | Uvicorn (ASGI) |

### Database Architecture
```
8 MySQL Databases:
├── ess          → Users, Roles, Permissions, Alerts, Time mappings
├── schedule     → Schedule events (energy trading)
├── Meter        → MMAIN, MAUX (power meters)
├── PCS          → PCS status/control data
├── Inverter     → INVERTER_1 readings
├── BaseLine     → Frequency baseline
├── BESS1-12     → Individual BESS rack data
└── GTR (remote) → GTR server data
```

### Redis Architecture
```
2 Redis Instances:
├── Main (localhost:6379)     → Meter data, real-time monitoring
└── GTR (192.168.10.46:6379)  → BESS/PCS data, energy trading
```

---

## API Endpoints Inventory

### System & Health (3 endpoints)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| `/api/health` | GET | `/api/v1/health` | `HealthResponse` |
| `/api/system_overview` | GET | `/api/v1/system/overview` | `SystemOverviewResponse` |
| `/api/topology` | GET | `/api/v1/system/topology` | `TopologyResponse` |

### BESS - Battery Storage (2 endpoints)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| `/api/bams_info/<bess_number>` | GET | `/api/v1/bess/{bess_number}` | `BessInfoResponse` |
| `/api/alert/rack/<rack_number>` | GET | `/api/v1/bess/alert/rack/{rack_number}` | `RackAlertResponse` |

### PCS - Power Conversion (2 endpoints)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| `/api/pcs_info/<pcs_number>` | GET | `/api/v1/pcs/{pcs_number}` | `PcsInfoResponse` |
| `/api/alert/pcs` | GET | `/api/v1/pcs/alert` | `PcsAlertResponse` |

### Meters & Power (3 endpoints)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| `/api/meter_info` | GET | `/api/v1/meters` | `MeterInfoResponse` |
| `/api/converter` | GET | `/api/v1/inverter` | `InverterResponse` |
| `/api/aux_meter` | GET | `/api/v1/meters/aux` | `AuxMeterResponse` |

### Energy Trading & Schedule (4 endpoints)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| `/api/schedule` | GET | `/api/v1/schedule` | `ScheduleResponse` |
| `/api/income/day` | GET | `/api/v1/income/daily` | `DailyIncomeResponse` |
| `/api/income/month` | GET | `/api/v1/income/monthly` | `MonthlyIncomeResponse` |
| `/api/exec_rate` | GET | `/api/v1/execution-rate` | `ExecRateResponse` |

### Energy Analysis (3 endpoints)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| `/api/power_loss` | GET | `/api/v1/analysis/power-loss` | `PowerLossResponse` |
| `/api/power_io` | GET | `/api/v1/analysis/power-io` | `PowerIOResponse` |
| `/api/freq_power` | GET | `/api/v1/analysis/freq-power` | `FreqPowerResponse` |

### Configuration (2 endpoints)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| `/api/sidebar_info` | GET | `/api/v1/config/sidebar` | `SidebarInfoResponse` |
| `/api/header_info` | GET | `/api/v1/config/header` | `HeaderInfoResponse` |

### Authentication (NEW - Enhanced)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| N/A (Flask-Security) | POST | `/api/v1/auth/login` | `TokenResponse` |
| N/A | POST | `/api/v1/auth/logout` | `MessageResponse` |
| N/A | GET | `/api/v1/auth/me` | `UserResponse` |
| N/A | POST | `/api/v1/auth/refresh` | `TokenResponse` |

### Admin (NEW - Optional)
| Flask Route | Method | FastAPI Route | Pydantic Model |
|-------------|--------|---------------|----------------|
| Flask-Admin | GET | `/api/v1/admin/users` | `UserListResponse` |
| Flask-Admin | POST | `/api/v1/admin/users` | `UserResponse` |
| Flask-Admin | PUT | `/api/v1/admin/users/{id}` | `UserResponse` |
| Flask-Admin | DELETE | `/api/v1/admin/users/{id}` | `MessageResponse` |

**Total: 25+ endpoints**

---

## Project Structure

```
fastapi/
├── pyproject.toml              # Dependencies & project config
├── .env.example                # Environment template
├── .env                        # Local environment (gitignored)
├── README.md                   # Project documentation
├── PLAN_FASTAPI.md            # This migration plan
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   │
│   ├── core/                   # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py           # Pydantic Settings (env vars)
│   │   ├── security.py         # JWT, password hashing
│   │   └── exceptions.py       # Custom exception handlers
│   │
│   ├── db/                     # Database layer
│   │   ├── __init__.py
│   │   ├── session.py          # Async session factory (multi-DB)
│   │   ├── base.py             # SQLAlchemy base classes
│   │   └── redis.py            # Async Redis client
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py             # User, Role, Permission
│   │   ├── schedule.py         # schedule_events
│   │   ├── alert.py            # alert_log, rack alerts
│   │   ├── meter.py            # MMAIN, MAUX
│   │   ├── pcs.py              # pcs0_data
│   │   ├── inverter.py         # INVERTER_1
│   │   └── baseline.py         # base_line
│   │
│   ├── schemas/                # Pydantic models
│   │   ├── __init__.py
│   │   ├── common.py           # Base schemas, responses
│   │   ├── auth.py             # Token, Login, User schemas
│   │   ├── bess.py             # BESS info, alerts
│   │   ├── pcs.py              # PCS info, alerts
│   │   ├── meter.py            # Meter data schemas
│   │   ├── schedule.py         # Schedule, income schemas
│   │   ├── analysis.py         # Power loss, IO, freq schemas
│   │   └── config.py           # Sidebar, header schemas
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── bess.py             # BESS service (from services.py)
│   │   ├── pcs.py              # PCS service
│   │   ├── meter.py            # Meter service
│   │   ├── schedule.py         # Schedule/income service
│   │   ├── analysis.py         # Power analysis service
│   │   ├── system.py           # System overview, topology
│   │   └── auth.py             # Authentication service
│   │
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependency injection
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Main API router
│   │       ├── auth.py         # /auth endpoints
│   │       ├── bess.py         # /bess endpoints
│   │       ├── pcs.py          # /pcs endpoints
│   │       ├── meters.py       # /meters endpoints
│   │       ├── schedule.py     # /schedule endpoints
│   │       ├── analysis.py     # /analysis endpoints
│   │       ├── system.py       # /system endpoints
│   │       └── admin.py        # /admin endpoints
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── timezone.py         # UTC+8 conversion
│       ├── redis_scan.py       # Redis scan utility (async)
│       └── notifications.py    # LINE, ZMQ notifications
│
└── tests/
    ├── __init__.py
    ├── conftest.py             # Pytest fixtures
    ├── test_auth.py
    ├── test_bess.py
    ├── test_pcs.py
    ├── test_meters.py
    ├── test_schedule.py
    └── test_analysis.py
```

---

## Implementation Phases

### Phase 1: Foundation (Core Setup)
**Files to create:**
- [ ] `app/main.py` - FastAPI app with CORS, exception handlers
- [ ] `app/core/config.py` - Pydantic Settings for all env vars
- [ ] `app/core/security.py` - JWT creation/validation, password hashing
- [ ] `app/core/exceptions.py` - Custom HTTP exceptions

**Key conversions:**
```python
# Flask
from flask import Flask
app = Flask(__name__)
cors = CORS(app)

# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SolarHub API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```

### Phase 2: Database Layer (Async SQLAlchemy)
**Files to create:**
- [ ] `app/db/session.py` - Multi-database async session factory
- [ ] `app/db/base.py` - Declarative base, mixins
- [ ] `app/db/redis.py` - Async Redis connection pool

**Key conversions:**
```python
# Flask-SQLAlchemy (sync)
db = SQLAlchemy(app)
result = Model.query.filter_by(id=1).first()

# SQLAlchemy 2.0 (async)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("mysql+aiomysql://...")
async_session = async_sessionmaker(engine)

async with async_session() as session:
    result = await session.execute(select(Model).where(Model.id == 1))
    row = result.scalar_one_or_none()
```

**Multi-database handling:**
```python
# Create engines for each database
engines = {
    "ess": create_async_engine(f"mysql+aiomysql://{user}:{pwd}@{host}/ess"),
    "schedule": create_async_engine(f"mysql+aiomysql://{user}:{pwd}@{host}/schedule"),
    "meter": create_async_engine(f"mysql+aiomysql://{user}:{pwd}@{host}/Meter"),
    # ... etc
}
```

### Phase 3: Models (SQLAlchemy ORM)
**Files to create:**
- [ ] `app/models/user.py` - User, Role, Permission
- [ ] `app/models/schedule.py` - schedule_events
- [ ] `app/models/alert.py` - alert_log
- [ ] `app/models/meter.py` - MMAIN, MAUX
- [ ] `app/models/pcs.py` - pcs0_data
- [ ] `app/models/inverter.py` - INVERTER_1
- [ ] `app/models/baseline.py` - base_line

**Key conversions:**
```python
# Flask-SQLAlchemy
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

# SQLAlchemy 2.0
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True)
```

### Phase 4: Pydantic Schemas
**Files to create:**
- [ ] `app/schemas/common.py` - Base response models
- [ ] `app/schemas/auth.py` - Token, Login, User
- [ ] `app/schemas/bess.py` - BessInfo, RackAlert
- [ ] `app/schemas/pcs.py` - PcsInfo, PcsAlert
- [ ] `app/schemas/meter.py` - MeterInfo, AuxMeter
- [ ] `app/schemas/schedule.py` - Schedule, Income
- [ ] `app/schemas/analysis.py` - PowerLoss, PowerIO, FreqPower

**Example schemas:**
```python
from pydantic import BaseModel, Field
from datetime import datetime

class MeterData(BaseModel):
    I_a: float = Field(..., description="Phase A current (A)")
    I_b: float = Field(..., description="Phase B current (A)")
    I_c: float = Field(..., description="Phase C current (A)")
    Vll_ab: float = Field(..., description="Line voltage AB (V)")
    KW_tot: float = Field(..., description="Total active power (kW)")

class MeterInfoResponse(BaseModel):
    meters: list[MeterData]
    meter_count: int
    total_power: float
    status: str
```

### Phase 5: Services (Business Logic)
**Files to create:**
- [ ] `app/services/bess.py` - get_bess_info, get_rack_alert_data
- [ ] `app/services/pcs.py` - get_pcs_info, get_pcs_alert_data
- [ ] `app/services/meter.py` - get_meter_data, get_aux_meter_data
- [ ] `app/services/schedule.py` - get_schedule_data, get_income_data
- [ ] `app/services/analysis.py` - get_power_loss_data, get_power_io_data
- [ ] `app/services/system.py` - get_system_overview, get_topology
- [ ] `app/services/auth.py` - authenticate_user, create_token

**Key pattern:**
```python
# Convert sync to async
# Flask (sync)
def get_meter_data():
    data = RedisScan(db=0, data_name='meter_*', ...)
    return process_data(data)

# FastAPI (async)
async def get_meter_data(redis: Redis) -> MeterInfoResponse:
    data = await redis_scan_async(redis, pattern='meter_*')
    return MeterInfoResponse(**process_data(data))
```

### Phase 6: API Routes
**Files to create:**
- [ ] `app/api/deps.py` - Dependency injection (DB sessions, auth)
- [ ] `app/api/v1/router.py` - Main router combining all routes
- [ ] `app/api/v1/auth.py` - Authentication endpoints
- [ ] `app/api/v1/bess.py` - BESS endpoints
- [ ] `app/api/v1/pcs.py` - PCS endpoints
- [ ] `app/api/v1/meters.py` - Meter endpoints
- [ ] `app/api/v1/schedule.py` - Schedule endpoints
- [ ] `app/api/v1/analysis.py` - Analysis endpoints
- [ ] `app/api/v1/system.py` - System endpoints

**Key conversions:**
```python
# Flask
@api.route('/api/meter_info', methods=['GET'])
def meter_info():
    """
    Get meter info
    ---
    responses:
      200:
        description: Meter data
    """
    return jsonify(get_meter_data())

# FastAPI
@router.get("/meters", response_model=MeterInfoResponse)
async def get_meters(
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
) -> MeterInfoResponse:
    """Get all meter data with 3-phase readings."""
    return await meter_service.get_meter_data(redis)
```

### Phase 7: Utilities
**Files to create:**
- [ ] `app/utils/timezone.py` - UTC to UTC+8 conversion
- [ ] `app/utils/redis_scan.py` - Async Redis scan utility
- [ ] `app/utils/notifications.py` - LINE Notify, ZMQ

**Timezone conversion:**
```python
from datetime import datetime, timedelta, timezone

TZ_UTC8 = timezone(timedelta(hours=8))

def utc_to_local(dt: datetime) -> datetime:
    """Convert UTC datetime to UTC+8."""
    return dt.replace(tzinfo=timezone.utc).astimezone(TZ_UTC8)
```

### Phase 8: Testing
**Files to create:**
- [ ] `tests/conftest.py` - Test fixtures, test DB
- [ ] `tests/test_*.py` - Unit tests for each endpoint

**Test pattern:**
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_meters(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/v1/meters", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "meters" in data
    assert "total_power" in data
```

---

## Key Migration Patterns

### 1. Route Parameters
```python
# Flask
@app.route('/api/bams_info/<int:bess_number>')
def bams_info(bess_number):
    ...

# FastAPI
@router.get("/bess/{bess_number}")
async def get_bess_info(bess_number: int = Path(..., ge=1, le=12)):
    ...
```

### 2. Query Parameters
```python
# Flask
mode = request.args.get('mode', 'all')
weeks = request.args.get('weeks', 1, type=int)

# FastAPI
@router.get("/schedule")
async def get_schedule(
    mode: str = Query("all", enum=["all", "dreg", "edreg"]),
    weeks: int = Query(1, ge=1, le=52)
):
    ...
```

### 3. Response Models
```python
# Flask (manual JSON)
return jsonify({
    'status': 'success',
    'data': data
})

# FastAPI (automatic serialization)
class SuccessResponse(BaseModel):
    status: str = "success"
    data: dict

@router.get("/data", response_model=SuccessResponse)
async def get_data():
    return SuccessResponse(data={"key": "value"})
```

### 4. Error Handling
```python
# Flask
if not data:
    return jsonify({'error': 'Not found'}), 404

# FastAPI
from fastapi import HTTPException

if not data:
    raise HTTPException(status_code=404, detail="Not found")
```

### 5. Dependency Injection
```python
# Flask (global)
from flask import g
def get_db():
    if 'db' not in g:
        g.db = connect_db()
    return g.db

# FastAPI (DI)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@router.get("/data")
async def get_data(db: AsyncSession = Depends(get_db)):
    ...
```

---

## Authentication Migration

### Current: Flask-Security
- Session-based authentication
- Role/permission model
- pbkdf2_sha512 password hashing

### Target: FastAPI + JWT
- Stateless JWT tokens
- Same role/permission model
- bcrypt password hashing (more secure)

```python
# app/core/security.py
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# app/api/deps.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

---

## Redis Migration (Async)

```python
# Flask (sync)
import redis
r = redis.Redis(host='localhost', port=6379)
data = r.hgetall('meter_1')

# FastAPI (async)
from redis.asyncio import Redis

async def get_redis() -> AsyncGenerator[Redis, None]:
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    try:
        yield redis
    finally:
        await redis.close()

# Async Redis scan
async def redis_scan_async(redis: Redis, pattern: str) -> list[dict]:
    keys = []
    async for key in redis.scan_iter(match=pattern):
        keys.append(key)

    results = []
    for key in keys:
        data = await redis.hgetall(key)
        results.append({k.decode(): v.decode() for k, v in data.items()})
    return results
```

---

## API Documentation

FastAPI automatically generates OpenAPI 3.1 docs:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

Enhanced documentation with:
```python
app = FastAPI(
    title="SolarHub API",
    description="IoT Dashboard API for Solar Energy Storage Systems",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "auth", "description": "Authentication operations"},
        {"name": "bess", "description": "Battery Energy Storage System"},
        {"name": "pcs", "description": "Power Conversion System"},
        {"name": "meters", "description": "Power meters and readings"},
        {"name": "schedule", "description": "Energy trading schedule"},
        {"name": "analysis", "description": "Power analysis and reporting"},
    ]
)
```

---

## Running the Application

### Development
```bash
cd /home/datavan/react_solar/fastapi
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your settings

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
# Or with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## Migration Checklist

### Pre-Migration
- [ ] Document all current Flask endpoints
- [ ] Export current OpenAPI spec from Flasgger
- [ ] Set up test environment with sample data
- [ ] Create `.env` file with all credentials

### Phase 1: Foundation
- [ ] Create FastAPI app with CORS
- [ ] Implement Pydantic Settings
- [ ] Set up JWT authentication
- [ ] Configure exception handlers

### Phase 2: Database
- [ ] Set up async SQLAlchemy engines (multi-DB)
- [ ] Create async session factory
- [ ] Set up async Redis connection
- [ ] Test database connections

### Phase 3: Models
- [ ] Convert User, Role, Permission models
- [ ] Convert schedule_events model
- [ ] Convert alert_log model
- [ ] Convert meter models (MMAIN, MAUX)
- [ ] Convert PCS model
- [ ] Convert inverter model
- [ ] Convert baseline model

### Phase 4: Schemas
- [ ] Create base response schemas
- [ ] Create auth schemas
- [ ] Create BESS schemas
- [ ] Create PCS schemas
- [ ] Create meter schemas
- [ ] Create schedule schemas
- [ ] Create analysis schemas

### Phase 5: Services
- [ ] Migrate BESS service functions
- [ ] Migrate PCS service functions
- [ ] Migrate meter service functions
- [ ] Migrate schedule service functions
- [ ] Migrate analysis service functions
- [ ] Migrate system service functions

### Phase 6: API Routes
- [ ] Create health/system endpoints
- [ ] Create auth endpoints
- [ ] Create BESS endpoints
- [ ] Create PCS endpoints
- [ ] Create meter endpoints
- [ ] Create schedule endpoints
- [ ] Create analysis endpoints
- [ ] Create admin endpoints

### Phase 7: Testing
- [ ] Set up pytest with async support
- [ ] Write tests for each endpoint
- [ ] Compare responses with Flask API
- [ ] Load testing with locust

### Post-Migration
- [ ] Compare OpenAPI specs (Flask vs FastAPI)
- [ ] Update frontend API calls if needed
- [ ] Deploy to staging environment
- [ ] Performance benchmarking
- [ ] Production deployment

---

## Performance Expectations

| Metric | Flask (sync) | FastAPI (async) |
|--------|--------------|-----------------|
| Requests/sec | ~500-1000 | ~2000-5000 |
| Latency (p50) | ~20ms | ~5ms |
| Latency (p99) | ~100ms | ~20ms |
| Memory usage | Higher | Lower |
| Concurrent connections | Limited by threads | Thousands |

---

## Next Steps

1. **Review this plan** - Confirm structure and approach
2. **Start Phase 1** - Create core FastAPI app
3. **Iterate** - Build each phase incrementally
4. **Test continuously** - Ensure API compatibility

Ready to proceed with implementation? Let me know which phase to start!
