# Database Connection Pool Management

This document explains database connection pooling strategies for the SolarHub FastAPI backend.

## Why Connection Pools Run Out

### Sync (Blocking) - The Problem

With traditional synchronous database access, each request holds a connection while waiting for the database response:

```
Request 1: [----waiting for DB----] (holds connection 5 seconds)
Request 2: [----waiting for DB----] (holds connection 5 seconds)
...
Request 20: Pool exhausted! All connections busy waiting
```

**Result:** With a pool size of 5 and 20 concurrent requests, 15 requests fail immediately.

### Async (Non-Blocking) - The Solution

With async SQLAlchemy 2.0, connections are released back to the pool while waiting:

```
Request 1: [query]...[release]...[query]...[release]
Request 2:    [query]...[release]...[query]...[release]
Same 5 connections can handle many more requests
```

**Result:** The same pool of 5 connections can handle significantly more concurrent requests because they're not held during I/O waits.

## SQLAlchemy Sync vs Async Comparison

| Aspect | SQLAlchemy (sync) | SQLAlchemy 2.0 (async) |
|--------|-------------------|------------------------|
| Thread blocking | Yes | No |
| Connections needed | ~1 per concurrent request | Shared across requests |
| Memory usage | Higher | Lower |
| Best for | Simple apps, Flask | High-concurrency, FastAPI |

### Code Comparison

**Sync (blocking):**
```python
# Blocks the thread while waiting for database
def get_user(db, user_id):
    result = db.query(User).filter(User.id == user_id).first()
    return result  # Thread waits here until DB responds
```

**Async (non-blocking):**
```python
# Releases thread while waiting, can handle other requests
async def get_user(db, user_id):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()  # Thread is free during DB wait
```

## Current Pool Configuration

Located in `fastapi_backend/app/db/session.py`:

```python
create_async_engine(
    url,
    pool_size=5,              # Base number of connections
    max_overflow=10,          # Extra connections when pool is full
    pool_recycle=3600,        # Recycle connections after 1 hour
    pool_pre_ping=True,       # Check if connection is alive before use
    connect_args={"connect_timeout": 5},  # 5 second connection timeout
)
```

## Recommended Pool Settings

For SolarHub with 18 databases and real-time monitoring:

```python
create_async_engine(
    url,
    pool_size=10,             # Increase from 5 for more concurrent queries
    max_overflow=20,          # Increase for burst traffic
    pool_recycle=1800,        # Recycle every 30 min (MySQL wait_timeout is often 28800)
    pool_pre_ping=True,       # Keep - checks if connection is alive
    pool_timeout=30,          # Wait 30s for connection before error
    connect_args={"connect_timeout": 5},
)
```

### Pool Size Calculation

```
Total connections per database = pool_size + max_overflow
With 18 databases: 18 × (10 + 20) = 540 max connections

MySQL default max_connections = 151
Consider: SET GLOBAL max_connections = 1000;
```

## Connection Pool Monitoring

Add to `fastapi_backend/app/db/session.py` for debugging:

```python
from sqlalchemy import event
import logging

logger = logging.getLogger(__name__)

def setup_pool_logging(engine):
    """Enable connection pool logging for debugging."""

    @event.listens_for(engine.sync_engine, "checkout")
    def log_checkout(dbapi_conn, connection_record, connection_proxy):
        logger.debug(f"Connection checked out. Pool status: {engine.pool.status()}")

    @event.listens_for(engine.sync_engine, "checkin")
    def log_checkin(dbapi_conn, connection_record):
        logger.debug(f"Connection returned. Pool status: {engine.pool.status()}")

    @event.listens_for(engine.sync_engine, "invalidate")
    def log_invalidate(dbapi_conn, connection_record, exception):
        logger.warning(f"Connection invalidated: {exception}")
```

## Best Practices

### 1. Always Use Context Managers

**Good - connection always released:**
```python
async with db_manager.session("ess") as session:
    result = await session.execute(query)
    return result.scalars().all()
```

**Bad - connection might leak on error:**
```python
session = await get_session()
result = await session.execute(query)  # If this fails, connection leaks
await session.close()  # Never reached on exception
```

### 2. Avoid Long-Running Transactions

**Bad:**
```python
async with db_manager.session("ess") as session:
    data = await session.execute(query)
    await external_api_call()  # Holds connection during slow operation!
    await session.commit()
```

**Good:**
```python
async with db_manager.session("ess") as session:
    data = await session.execute(query)

result = await external_api_call()  # Connection released

async with db_manager.session("ess") as session:
    await session.commit()
```

### 3. Use Read-Only Sessions When Possible

```python
async with db_manager.session("ess") as session:
    session.execute(text("SET TRANSACTION READ ONLY"))
    # Read operations...
```

### 4. Connection Health Checks

The `pool_pre_ping=True` setting automatically checks if connections are alive before use. This prevents "MySQL server has gone away" errors.

## Troubleshooting

### Error: "QueuePool limit of size X overflow Y reached"

**Cause:** All connections are in use, no available connections.

**Solutions:**
1. Increase `pool_size` and `max_overflow`
2. Check for connection leaks (missing context managers)
3. Reduce query execution time
4. Add connection timeout monitoring

### Error: "MySQL server has gone away"

**Cause:** Connection was idle longer than MySQL's `wait_timeout`.

**Solutions:**
1. Reduce `pool_recycle` to less than MySQL's `wait_timeout`
2. Ensure `pool_pre_ping=True` is set
3. Check MySQL: `SHOW VARIABLES LIKE 'wait_timeout';`

### Error: "Too many connections"

**Cause:** Total connections exceed MySQL's `max_connections`.

**Solutions:**
1. Reduce pool sizes
2. Increase MySQL's `max_connections`
3. Consider connection pooling proxy (PgBouncer, ProxySQL)

## Database ORM Options for FastAPI

| Library | Type | Pros | Cons |
|---------|------|------|------|
| **SQLAlchemy 2.0** | Full ORM | Industry standard, mature, Alembic migrations | Verbose |
| **SQLModel** | ORM | By FastAPI creator, less boilerplate | Newer, fewer features |
| **Tortoise ORM** | ORM | Django-style, async-first | Smaller community |
| **encode/databases** | Query builder | Lightweight | No ORM features |

**Recommendation:** SQLAlchemy 2.0 is the right choice for SolarHub due to:
- 18 database connections requiring robust management
- Complex queries for schedule and analysis endpoints
- Battle-tested in production environments
- Alembic for schema migrations

## References

- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [FastAPI with Async SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [MySQL Connection Management](https://dev.mysql.com/doc/refman/8.0/en/connection-interfaces.html)
