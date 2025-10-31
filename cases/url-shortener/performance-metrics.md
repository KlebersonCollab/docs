# Performance Metrics - URL Shortener

## Overview

This document outlines the key performance metrics, calculations, and monitoring strategies for a URL shortener system.

## Required Performance Metrics

### Throughput Requirements

#### Write Operations
- **Target**: 1,160 writes/second
- **Peak**: Assume 2x = 2,320 writes/second
- **Calculation**:
  ```
  100,000,000 URLs/day ÷ 24 hours ÷ 60 minutes ÷ 60 seconds
  = ~1,160 writes/second
  ```

#### Read Operations
- **Target**: 11,600 reads/second
- **Peak**: Assume 2x = 23,200 reads/second
- **Calculation**:
  ```
  1,160 writes/sec × 10 (read:write ratio)
  = 11,600 reads/second
  ```

### Latency Requirements

#### URL Shortening (Write)
- **Target**: < 50ms (P95)
- **Breakdown**:
  - Redis INCR: ~1ms
  - Base 62 encoding: < 1ms
  - Cassandra write: ~10-20ms
  - Network overhead: ~5ms
  - **Total**: ~20-30ms average

#### URL Redirection (Read)
- **Cache Hit**: < 5ms (P95)
- **Cache Miss**: < 20ms (P95)
- **Breakdown** (Cache Miss):
  - Cache check: ~1ms
  - Cassandra query: ~10ms
  - Cache write: ~1ms
  - Network: ~5ms
  - **Total**: ~17ms average

### Availability Requirements

- **Target**: 99.9% uptime (24x7)
- **Allowed Downtime**: ~8.76 hours/year
- **Impact**: Requires redundancy at all layers

## Storage Calculations

### Total Records

```
100,000,000 URLs/day × 365 days/year × 10 years
= 365,000,000,000 records (365 billion)
```

### Total Storage

```
365 billion records × 100 bytes/record
= 36,500,000,000,000 bytes
= 36.5 TB
```

### Short Code Space

**Base 62 Calculation**:
```
62^1 = 62
62^2 = 3,844
62^3 = 238,328
62^4 = 14,776,336
62^5 = 916,132,832
62^6 = 56,800,235,584
62^7 = 3,521,614,606,208 (3.5 trillion)
```

**Minimum Required**: 7 characters for 365 billion unique codes

## Performance Benchmarks

### Component Benchmarks

#### Redis (ID Generation)
- **Operation**: INCR (atomic increment)
- **Latency**: ~1ms
- **Throughput**: 100,000+ ops/sec per node
- **Capacity**: Easily handles 1,160 writes/sec

#### Redis (Cache)
- **Operation**: GET/SET
- **Latency**: < 1ms
- **Throughput**: 100,000+ ops/sec per node
- **Capacity**: Easily handles 11,600 reads/sec (with multiple nodes)

#### Cassandra (Read)
- **Operation**: SELECT by partition key
- **Latency**: 10-15ms (P95)
- **Throughput**: ~10,000 reads/sec per node
- **With Cache**: Only 20% hit database = 2,320 reads/sec needed
- **Nodes Required**: 1 node (with 400% headroom)

#### Cassandra (Write)
- **Operation**: INSERT
- **Latency**: 10-20ms (P95)
- **Throughput**: ~5,000 writes/sec per node
- **Nodes Required**: 1 node (with 200% headroom)

### System-Wide Benchmarks

#### End-to-End Latency

**URL Shortening**:
```
Load Balancer: ~2ms
API Processing: ~1ms
Redis INCR: ~1ms
Encoding: <1ms
Cassandra Write: ~15ms
Response: ~5ms
─────────────────────
Total: ~25ms (P95: ~50ms)
```

**URL Redirection (Cache Hit)**:
```
Load Balancer: ~2ms
API Processing: ~1ms
Redis GET: <1ms
Response: ~2ms
─────────────────────
Total: ~5ms (P95: ~10ms)
```

**URL Redirection (Cache Miss)**:
```
Load Balancer: ~2ms
API Processing: ~1ms
Redis GET (miss): ~1ms
Cassandra Read: ~12ms
Redis SET: ~1ms
Response: ~3ms
─────────────────────
Total: ~20ms (P95: ~40ms)
```

## Cache Performance

### Cache Hit Rate Target

- **Goal**: 85-90% hit rate
- **Impact**: Reduces database load by 85-90%

### Cache Hit Rate Calculation

```
Total reads: 11,600/sec
Cache hits (85%): 9,860/sec
Cache misses (15%): 1,740/sec
Database queries: 1,740/sec (reduced from 11,600)
```

### Cache Strategy Impact

**Without Cache**:
- 11,600 database queries/sec
- Requires 2-3 Cassandra nodes
- Higher latency (15ms vs 5ms)

**With Cache (85% hit rate)**:
- 1,740 database queries/sec
- Requires 1 Cassandra node
- Lower latency (5ms for 85% of requests)

## Scalability Metrics

### Horizontal Scaling Capacity

#### API Servers
- **Single Instance Capacity**: ~1,000 req/sec
- **Required Capacity**: 12,760 req/sec
- **Minimum Instances**: 13
- **Recommended**: 15-20 (with 50% headroom)

#### Database Nodes
- **Write Capacity per Node**: ~5,000/sec
- **Required Writes**: 1,160/sec
- **Nodes Needed**: 1 (with 400% headroom)
- **Recommended**: 3 (for replication factor 3)

#### Cache Nodes
- **Capacity per Node**: 100,000+ ops/sec
- **Required Ops**: 11,600/sec
- **Nodes Needed**: 1 (with 800% headroom)
- **Recommended**: 3 (for high availability)

## Monitoring Metrics

### Key Performance Indicators (KPIs)

#### 1. Request Throughput
```python
metrics = {
    'writes_per_second': 1160,
    'reads_per_second': 11600,
    'total_requests_per_second': 12760
}
```

#### 2. Response Time
```python
latency_metrics = {
    'p50': 10,  # ms - Median
    'p95': 50,  # ms - 95th percentile
    'p99': 100,  # ms - 99th percentile
    'p999': 200  # ms - 99.9th percentile
}
```

#### 3. Cache Performance
```python
cache_metrics = {
    'hit_rate': 0.85,  # 85%
    'miss_rate': 0.15,  # 15%
    'cache_size': '10GB',
    'eviction_rate': 100  # per second
}
```

#### 4. Database Performance
```python
db_metrics = {
    'read_latency_p95': 15,  # ms
    'write_latency_p95': 20,  # ms
    'query_rate': 1740,  # per second (with cache)
    'connection_pool_usage': 0.6  # 60%
}
```

#### 5. Error Rates
```python
error_metrics = {
    'error_rate': 0.001,  # 0.1%
    'timeout_rate': 0.0001,  # 0.01%
    '4xx_errors': 0.0005,  # 0.05%
    '5xx_errors': 0.0005  # 0.05%
}
```

### Alert Thresholds

```python
alerts = {
    'high_latency_p95': {
        'threshold': 200,  # ms
        'action': 'Scale up API instances'
    },
    'low_cache_hit_rate': {
        'threshold': 0.70,  # 70%
        'action': 'Review cache strategy'
    },
    'high_error_rate': {
        'threshold': 0.01,  # 1%
        'action': 'Investigate errors'
    },
    'database_connection_pool_exhausted': {
        'threshold': 0.90,  # 90%
        'action': 'Increase pool size or scale DB'
    },
    'cpu_usage_high': {
        'threshold': 0.80,  # 80%
        'action': 'Scale horizontally'
    }
}
```

## Capacity Planning

### Current Capacity

| Component | Capacity | Utilization | Headroom |
|-----------|----------|-------------|----------|
| API Servers (15) | 15,000 req/sec | 12,760 (85%) | 15% |
| Cassandra (3) | 15,000 writes/sec | 1,160 (8%) | 92% |
| Cassandra Reads | 30,000 reads/sec | 1,740 (6%) | 94% |
| Redis (3) | 300,000 ops/sec | 11,600 (4%) | 96% |

### Growth Projections

#### 2x Growth
- **Writes**: 2,320/sec (still within capacity)
- **Reads**: 23,200/sec (cache handles most)
- **Action**: Scale API servers to 25-30 instances

#### 10x Growth
- **Writes**: 11,600/sec
- **Reads**: 116,000/sec
- **Action**: 
  - Scale API servers to 150-200 instances
  - Scale Cassandra to 5-7 nodes
  - Scale Redis cluster

#### 100x Growth
- **Requires**: Multi-region deployment
- **Requires**: Database sharding
- **Requires**: Advanced caching strategies

## Optimization Opportunities

### 1. Cache Warming

**Pre-populate cache with popular URLs**:
```python
def warm_cache():
    """Pre-populate cache with top 10,000 URLs"""
    popular_urls = get_top_urls(limit=10000)
    for url in popular_urls:
        redis.setex(f"url:{url.short_code}", 86400, url.long_url)
```

### 2. Read Replicas

**Use Cassandra read replicas**:
- Route read queries to nearest replica
- Reduces latency for global users

### 3. Connection Pooling

**Optimize database connections**:
```python
# Reuse connections
connection_pool_size = min_instances * 10
# Avoid connection overhead
```

### 4. Batch Operations

**Batch writes when possible**:
```python
# If batching multiple URLs
batch = []
for url in urls:
    batch.append(insert_statement)
session.execute_batch(batch)
```

## Performance Testing

### Load Testing Scenarios

#### 1. Baseline Test
- **Traffic**: 12,760 req/sec
- **Duration**: 1 hour
- **Goal**: Verify system handles expected load

#### 2. Peak Test
- **Traffic**: 25,520 req/sec (2x)
- **Duration**: 30 minutes
- **Goal**: Verify system handles traffic spikes

#### 3. Stress Test
- **Traffic**: Gradually increase until failure
- **Goal**: Find breaking point

#### 4. Endurance Test
- **Traffic**: 12,760 req/sec
- **Duration**: 24 hours
- **Goal**: Verify no memory leaks or degradation

### Tools

- **Apache JMeter**: Load testing
- **Gatling**: Performance testing
- **wrk**: HTTP benchmarking
- **Redis-benchmark**: Cache performance

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/performance-metrics.pt-br.md)

---

**Related Documents**:
- [Architecture Design](architecture-design.md)
- [Scalability Patterns](scalability-patterns.md)

