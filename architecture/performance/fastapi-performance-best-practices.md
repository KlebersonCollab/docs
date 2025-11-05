# FastAPI Performance Best Practices

**Versão em Português**: [Melhores Práticas de Performance FastAPI (PT-BR)](pt-br/fastapi-performance-best-practices.md)

## Overview

This document outlines proven performance optimization practices for FastAPI applications. These practices are based on real-world experience and focus on actual bottlenecks rather than premature optimization.

## ⚠️ Important Disclaimer

**The bottleneck is NOT in the language or framework.** When building APIs and systems that deliver information to users, the real bottlenecks are:

1. **Database communications** - Query execution, connection pooling
2. **HTTP requests** - External API calls, network latency
3. **I/O operations** - File operations, network I/O

Performance measurements show that:
- CPU operations in memory are measured in **nanoseconds**
- HTTP requests are measured in **milliseconds**
- This is a **1000x difference** in magnitude

**Reference**: "Numbers Every Programmer Should Know" by Jeff Dean (Google)

### When to Apply These Practices

These optimizations should be applied:
- ✅ For specific performance-critical cases
- ✅ When you have identified actual bottlenecks
- ✅ As part of curiosity-driven learning
- ❌ NOT as premature optimization
- ❌ NOT as a substitute for proper database/API optimization

## Best Practices

### 1. Use Async/Await Throughout

**Why it matters:**
- Synchronous routes can block execution
- Sequential code waits for each operation to complete
- Async operations can run independently
- Significantly improves throughput

**Implementation:**

```python
# ❌ BAD: Synchronous route
@app.get("/users")
def get_users():
    users = db.query(User).all()  # Blocks until complete
    return users

# ✅ GOOD: Async route
@app.get("/users")
async def get_users():
    users = await db.query(User).all()  # Non-blocking
    return users
```

**Key Points:**
- Python now has a mature async ecosystem
- Use async-compatible libraries:
  - `asyncpg` instead of `psycopg2` (PostgreSQL)
  - `aiosqlite` instead of `sqlite3` (SQLite)
  - `aiomysql` instead of `mysql-connector` (MySQL)
  - `motor` for MongoDB async operations

**Performance Gain:**
- Can handle 3-5x more concurrent requests
- Better resource utilization
- Lower latency under load

---

### 2. Use UVLoop for Event Loop

**Why it matters:**
- Default Uvicorn uses `asyncio` (standard Python event loop)
- UVLoop is a high-performance event loop implementation
- Based on `libuv` (same library used by Node.js)
- **4-5x faster** than standard `asyncio`

**Installation:**

```bash
# ❌ Standard installation (uses asyncio)
pip install uvicorn

# ✅ With UVLoop (optimized)
pip install uvicorn[standard]
```

**What you get:**
- `uvloop` - Optimized event loop
- `httptools` - Faster HTTP parsing
- Other performance-optimized dependencies

**Important Considerations:**

1. **Platform Compatibility:**
   - ✅ Works great on **Unix-like systems** (Linux, macOS)
   - ❌ **Does NOT work on Windows**
   - Best for production Linux deployments

2. **Compatibility:**
   - Works seamlessly with `asyncio` imports
   - No code changes required
   - Automatically uses UVLoop when available

**Performance Gain:**
- 4-5x faster event loop processing
- Lower CPU usage
- Better handling of concurrent connections

**Common Mistake:**
Many developers think they're using UVLoop with standard `pip install uvicorn`, but they're not. Always use `uvicorn[standard]`.

---

### 3. Optimal Server Configuration

**Best Practice:** FastAPI running in async mode with Uvicorn workers managed by Gunicorn.

**Why this configuration:**
- **Gunicorn**: Process manager and load balancer
- **Uvicorn workers**: Handle async requests efficiently
- Best performance for production deployments

**Installation:**

```bash
pip install gunicorn uvicorn[standard]
```

**Configuration:**

Create `gunicorn_config.py`:

```python
# gunicorn_config.py
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
# Formula: (2 × CPU cores) + 1
workers = (2 * multiprocessing.cpu_count()) + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Worker configuration
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "fastapi-app"
```

**Worker Count Calculation:**

```python
# Formula: (2 × CPU cores) + 1
workers = (2 * multiprocessing.cpu_count()) + 1

# Optional: Add 1 more worker if you have hyperthreading
# workers = (2 * multiprocessing.cpu_count()) + 2
```

**Running the Server:**

```bash
gunicorn -c gunicorn_config.py main:app
```

**Architecture:**
```
Gunicorn (Master Process)
    ├── Uvicorn Worker 1
    ├── Uvicorn Worker 2
    ├── Uvicorn Worker 3
    └── ... (N workers)
```

**Benefits:**
- Process isolation (worker crash doesn't kill all)
- Load balancing across workers
- Graceful worker restart
- Production-ready configuration

---

### 4. Use Pydantic v2

**Why it matters:**
- Pydantic v2 has a **core written in Rust**
- Much faster validation than v1
- Significantly faster than alternatives:
  - `marshmallow`
  - `serpy`
  - Other Python validators

**Installation:**

```bash
pip install "pydantic>=2.0.0"
```

**Best Practice: Use at Application Boundaries**

```python
# ✅ GOOD: Validate at HTTP request/response boundaries
@app.post("/users")
async def create_user(user: UserCreate):  # Pydantic model
    # Validate input (fast with Pydantic v2)
    validated_data = user.model_dump()
    
    # Process with internal models (no validation overhead)
    result = await user_service.create(validated_data)
    
    return result  # Fast serialization with Pydantic v2
```

**When to Use:**
- ✅ **Input validation** - When receiving HTTP requests
- ✅ **Output serialization** - When returning HTTP responses
- ❌ **Avoid** - Internal data structures (unnecessary overhead)
- ❌ **Avoid** - Validating return values (validate only inputs)

**Performance Gain:**
- 5-10x faster validation than Pydantic v1
- 10-50x faster than other Python validators
- Lower memory usage

**Migration from v1:**
- Most code is compatible
- Some breaking changes in advanced features
- See [Pydantic v2 Migration Guide](https://docs.pydantic.dev/2.0/migration/)

---

### 5. Use orjson for JSON Serialization

**Why it matters:**
- Faster JSON serialization than standard library
- Written in Rust for performance
- Drop-in replacement for standard JSON

**Installation:**

```bash
pip install orjson
```

**Configuration in FastAPI:**

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    default_response_class=ORJSONResponse
)

# Or use per-route
@app.get("/users", response_class=ORJSONResponse)
async def get_users():
    return {"users": [...]}
```

**Performance Gain:**
- 2-3x faster JSON serialization
- Lower CPU usage
- Better handling of large payloads

**Compatibility:**
- Compatible with all FastAPI features
- Handles all standard JSON types
- Can be used alongside standard JSON where needed

---

## Performance Comparison Summary

| Practice | Performance Gain | Use Case |
|----------|-----------------|----------|
| Async/Await | 3-5x throughput | All I/O operations |
| UVLoop | 4-5x event loop | Unix-like systems (Linux/macOS) |
| Gunicorn + Uvicorn | Better concurrency | Production deployments |
| Pydantic v2 | 5-10x validation | Input/output boundaries |
| orjson | 2-3x serialization | All JSON responses |

## Implementation Checklist

- [ ] Convert all routes to async/await
- [ ] Use async-compatible database drivers
- [ ] Install `uvicorn[standard]` for UVLoop
- [ ] Configure Gunicorn with Uvicorn workers
- [ ] Calculate optimal worker count
- [ ] Upgrade to Pydantic v2
- [ ] Use Pydantic only at application boundaries
- [ ] Install and configure orjson
- [ ] Update FastAPI to use ORJSONResponse

## Testing Performance

### Benchmarking Tools

1. **TechEmpower Web Framework Benchmarks**
   - Compare FastAPI performance
   - See impact of optimizations

2. **Apache Bench (ab)**
   ```bash
   ab -n 10000 -c 100 http://localhost:8000/users
   ```

3. **wrk**
   ```bash
   wrk -t12 -c400 -d30s http://localhost:8000/users
   ```

### Metrics to Monitor

- **Response Time** (p50, p95, p99)
- **Throughput** (requests per second)
- **Error Rate** (percentage of failed requests)
- **CPU Usage** (should decrease with optimizations)
- **Memory Usage** (monitor for leaks)

## Common Mistakes to Avoid

1. ❌ **Using sync code in async routes**
   ```python
   # Don't do this
   @app.get("/users")
   async def get_users():
       users = db.query(User).all()  # Blocking!
       return users
   ```

2. ❌ **Installing standard uvicorn instead of uvicorn[standard]**
   ```bash
   # Wrong
   pip install uvicorn
   
   # Correct
   pip install uvicorn[standard]
   ```

3. ❌ **Using Pydantic for internal data structures**
   ```python
   # Don't validate everything
   def process_data(data: UserModel):  # Unnecessary validation
       ...
   ```

4. ❌ **Not optimizing database queries**
   - Remember: DB is usually the bottleneck
   - Optimize queries before optimizing framework

5. ❌ **Premature optimization**
   - Profile first, optimize second
   - Focus on actual bottlenecks

## Real-World Example

### Before Optimization

```python
from fastapi import FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users")
def get_users(db: Session):
    # Synchronous, blocking
    users = db.query(User).all()
    return users
```

**Performance:**
- ~100 requests/second
- High CPU usage
- Blocking operations

### After Optimization

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(default_response_class=ORJSONResponse)

@app.get("/users")
async def get_users(db: AsyncSession):
    # Asynchronous, non-blocking
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
```

**Configuration:**
```bash
# gunicorn_config.py
workers = (2 * multiprocessing.cpu_count()) + 1
worker_class = "uvicorn.workers.UvicornWorker"
```

**Performance:**
- ~500-1000 requests/second
- Lower CPU usage
- Non-blocking operations
- Better resource utilization

## Additional Resources

### Learning Resources

- [FastAPI Async Documentation](https://fastapi.tiangolo.com/async/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/2.0/)
- [UVLoop GitHub Repository](https://github.com/MagicStack/uvloop)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/settings.html)

### Performance References

- "Numbers Every Programmer Should Know" - Jeff Dean (Google)
- TechEmpower Web Framework Benchmarks
- FastAPI Performance Benchmarks

## Conclusion

These practices can significantly improve FastAPI performance, but remember:

1. **Profile first** - Identify actual bottlenecks
2. **Optimize database** - Usually the biggest bottleneck
3. **Measure impact** - Verify improvements with benchmarks
4. **Don't over-optimize** - Focus on real problems

The combination of async/await, UVLoop, proper server configuration, Pydantic v2, and orjson can provide substantial performance improvements, but always measure and verify the impact in your specific use case.

---

**Last Updated**: 2025-01-XX
**Maintainer**: Skynet Architecture Team
**Version**: 1.0

