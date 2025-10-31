# Scalability Patterns - URL Shortener

## Overview

This document outlines the scalability patterns and architectural evolution required to handle high-volume traffic for a URL shortener system.

## Scaling Strategy

### Vertical vs Horizontal Scaling

#### Vertical Scaling (❌ Not Suitable)

**Definition**: Adding more resources (CPU, RAM) to a single server

**Limitations**:
- Maximum capacity limited by hardware
- Single point of failure
- Cannot handle 12,760 requests/second
- Expensive at scale

#### Horizontal Scaling (✅ Recommended)

**Definition**: Adding more servers/instances

**Benefits**:
- Linear scalability
- High availability (no single point of failure)
- Cost-effective (commodity hardware)
- Can scale to any capacity needed

## Load Balancing

### Purpose

Distribute incoming traffic across multiple backend instances.

### Architecture

```
                    ┌─────────────────┐
                    │ Load Balancer   │
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
        ┌───────▼──┐  ┌──────▼──┐  ┌──────▼──┐
        │ API-1    │  │ API-2    │  │ API-3    │
        └──────────┘  └──────────┘  └──────────┘
```

### Load Balancing Algorithms

#### 1. Round Robin
- Distributes requests sequentially
- Simple and fair
- Good for uniform server capacity

#### 2. Least Connections
- Routes to server with fewest active connections
- Better for varying request processing times
- **Recommended** for URL shortener

#### 3. Weighted Round Robin
- Adjusts for different server capacities
- Useful for heterogeneous infrastructure

### Health Checks

```python
# Load balancer configuration
health_check_interval = 30  # seconds
health_check_path = "/health"
unhealthy_threshold = 3  # consecutive failures
healthy_threshold = 2  # consecutive successes
```

## Database Scaling

### Why Cassandra?

#### 1. Horizontal Scalability

```
Traditional RDBMS:
- Single master node
- Vertical scaling only
- Limited write throughput

Cassandra:
- Multiple nodes (no master)
- Horizontal scaling
- Linear write scaling
```

#### 2. Write-Optimized

- **LSM-Tree** storage structure
- Append-only writes (no updates)
- Perfect for URL storage (mostly writes, occasional updates)

#### 3. Partitioning Strategy

```cql
-- Partition by short_code
CREATE TABLE url_shortener (
    short_code TEXT PRIMARY KEY,  -- Partition key
    long_url TEXT,
    created_at TIMESTAMP
);
```

**Benefits**:
- Each short_code maps to specific node
- Parallel reads across nodes
- No cross-node queries needed

#### 4. Replication Factor

```cql
CREATE KEYSPACE url_shortener
WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'datacenter1': 3  -- 3 copies of each record
};
```

**Benefits**:
- High availability (survive 1-2 node failures)
- Data durability
- Read from nearest replica

### Capacity Calculation

**Write Capacity**:
- 1,160 writes/sec required
- Cassandra: ~5,000 writes/sec per node
- Nodes needed: 1 (with 200% headroom)

**Read Capacity**:
- 11,600 reads/sec required
- Cache handles 85% = 9,860 cached/sec
- Database: 1,740 reads/sec
- Cassandra: ~10,000 reads/sec per node
- Nodes needed: 1

**Replication**:
- Replication factor 3
- **Minimum nodes**: 3
- **Recommended**: 5-7 nodes (for performance + redundancy)

## Caching Strategy

### Redis Cluster Setup

#### Architecture

```
                    ┌──────────────┐
                    │  API Server │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
    ┌───────▼───┐  ┌───────▼───┐  ┌───────▼───┐
    │ Redis-1   │  │ Redis-2   │  │ Redis-3   │
    │ (Master)  │  │ (Replica) │  │ (Replica) │
    └───────────┘  └───────────┘  └───────────┘
```

#### Dual Purpose

**1. ID Generation**

```python
# Atomic counter
next_id = redis.incr('url_counter')
```

**Requirements**:
- Must be atomic (no race conditions)
- Must be fast (every write needs ID)
- High availability critical

**Setup**:
- Redis Cluster (3-6 nodes)
- Or Redis Sentinel for auto-failover

**2. URL Caching**

**Strategy**: Cache Most Frequently Accessed URLs

```python
# Cache popular URLs
redis.setex(f"url:{short_code}", TTL=3600, value=long_url)
```

**Benefits**:
- Reduces database load by 80-90%
- Faster response times (memory vs disk)
- Handles read-heavy workload

#### Cache Population Strategy

**1. Lazy Loading** (Current)
- Cache on first read
- Simple implementation
- May cache unpopular URLs

**2. Write-Through**
- Cache immediately on write
- Guarantees cache for new URLs
- May waste cache on rarely-accessed URLs

**3. Hybrid Approach** (Recommended)
- Write-through for new URLs (TTL: 1 hour)
- Track access frequency
- Extend TTL for popular URLs (up to 24 hours)

```python
def get_url(short_code: str) -> str:
    # Check cache first
    cached = redis.get(f"url:{short_code}")
    if cached:
        # Increment access count
        redis.incr(f"url:{short_code}:hits")
        return cached
    
    # Query database
    url = cassandra.get(short_code)
    
    # Cache with initial TTL
    redis.setex(f"url:{short_code}", 3600, url)
    
    # If becomes popular, extend TTL
    hits = redis.get(f"url:{short_code}:hits")
    if hits and hits > 100:  # Popular threshold
        redis.expire(f"url:{short_code}", 86400)  # 24 hours
    
    return url
```

## Auto-Scaling

### Dynamic Instance Management

#### Metrics for Scaling

```python
# Scaling triggers
scale_up_thresholds = {
    'cpu_usage': 70,  # %
    'request_latency_p95': 200,  # ms
    'request_queue_length': 100,
    'error_rate': 1  # %
}

scale_down_thresholds = {
    'cpu_usage': 30,  # %
    'request_latency_p95': 50,  # ms
    'request_queue_length': 10,
    'error_rate': 0.1  # %
}
```

#### Scaling Policy

```yaml
# Auto-scaling configuration
min_instances: 3
max_instances: 20
target_cpu_utilization: 60%
scale_up_cooldown: 300  # seconds
scale_down_cooldown: 600  # seconds
```

### Benefits

1. **Cost Optimization**: Scale down during low traffic
2. **Performance**: Scale up during peak traffic
3. **Reliability**: Maintain service during traffic spikes

## Multi-Region Deployment

### Architecture

```
Region 1 (US-East)          Region 2 (EU-West)
┌──────────────┐           ┌──────────────┐
│ Load Balancer│           │ Load Balancer│
│ API Servers  │           │ API Servers  │
│ Redis Cluster│           │ Redis Cluster│
│ Cassandra    │◄──────────►│ Cassandra    │
└──────────────┘           └──────────────┘
      │                            │
      └──────── Cross-Region ──────┘
            Replication
```

### Benefits

1. **Geographic Distribution**
   - Lower latency (route to nearest region)
   - Better user experience

2. **Disaster Recovery**
   - If one region fails, others continue
   - Automatic failover

3. **Compliance**
   - Data residency requirements
   - Regional regulations

### Challenges

1. **Data Consistency**
   - Cross-region replication latency
   - Eventual consistency model

2. **ID Generation**
   - Must be globally unique
   - Cannot use same counter in all regions

**Solution**: Region-aware ID generation

```python
# Region 1: IDs starting 14,000,000
# Region 2: IDs starting 20,000,000
# Region 3: IDs starting 30,000,000

REGION_ID_OFFSET = {
    'us-east': 14_000_000,
    'eu-west': 20_000_000,
    'asia-pac': 30_000_000
}

def get_next_id():
    base_id = redis.incr('url_counter')
    region_offset = REGION_ID_OFFSET[os.environ['REGION']]
    return base_id + region_offset
```

## Performance Optimization

### Database Optimization

#### Read Optimization

1. **Partition Key Design**
   - short_code as primary key
   - Enables direct node lookup
   - No scanning required

2. **Read Consistency**
   - Use ONE consistency (fastest)
   - Acceptable for URL lookup (idempotent)

```python
# Fast reads
result = session.execute(
    "SELECT long_url FROM url_shortener WHERE short_code = ?",
    [short_code],
    consistency_level=ConsistencyLevel.ONE
)
```

#### Write Optimization

1. **Batch Writes** (if applicable)
   - Group multiple writes
   - Reduces network overhead

2. **Async Writes**
   - Fire-and-forget for analytics
   - Don't block response

### Network Optimization

#### Connection Pooling

```python
# Reuse database connections
from cassandra.cluster import Cluster

cluster = Cluster(['node1', 'node2', 'node3'])
session = cluster.connect('url_shortener')
# Reuse session across requests
```

#### Keep-Alive Connections

```python
# Redis connection pool
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=redis_pool)
```

## Capacity Planning Summary

### Current Requirements

| Metric | Value |
|--------|-------|
| Write operations/sec | 1,160 |
| Read operations/sec | 11,600 |
| Storage (10 years) | 36.5 TB |
| Records (10 years) | 365 billion |

### Infrastructure Needs

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| API Instances | 13 | 15-20 |
| Cassandra Nodes | 3 | 5-7 |
| Redis Nodes | 3 | 3-6 |
| Load Balancers | 2 | 2 (active-passive) |

### Scaling Projections

**10x Growth**:
- API Instances: 150-200
- Cassandra Nodes: 15-20
- Cache capacity: Scale proportionally

**100x Growth**:
- Requires sharding strategy
- Multi-region mandatory
- More sophisticated caching

## Monitoring and Alerting

### Key Metrics

1. **Throughput**
   - Requests per second
   - Writes vs reads ratio

2. **Latency**
   - P50, P95, P99
   - Cache hit latency
   - Database query latency

3. **Availability**
   - Uptime percentage
   - Error rate
   - Failed requests

4. **Capacity**
   - Database size
   - Cache memory usage
   - Instance CPU/memory

### Alert Thresholds

```python
alerts = {
    'high_latency_p95': 200,  # ms
    'error_rate': 1,  # %
    'cache_hit_rate_low': 70,  # %
    'database_connections_high': 80,  # %
    'disk_usage': 85,  # %
}
```

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/scalability-patterns.pt-br.md)

---

**Related Documents**:
- [Architecture Design](architecture-design.md)
- [Performance Metrics](performance-metrics.md)

