# Architecture Design - URL Shortener

## Overview

This document describes the complete system architecture for a scalable URL shortener, from initial simple design to production-ready distributed system.

## Evolution of Architecture

### Stage 1: Basic Architecture (❌ Insufficient)

```
┌──────────┐
│ Frontend │
└────┬─────┘
     │
┌────▼─────┐
│ Backend  │
│ Server   │
└────┬─────┘
     │
┌────▼─────┐
│Database  │
└──────────┘
```

**Problems**:
- Single server cannot handle 1,160 writes/sec and 11,600 reads/sec
- Single database is a single point of failure
- No redundancy (violates 24x7 availability requirement)

### Stage 2: Horizontal Scaling (✅ Better)

```
┌──────────┐
│ Frontend │
└────┬─────┘
     │
┌────▼─────────────┐
│ Load Balancer    │
└────┬─────────────┘
     │
┌────┼────┬────┬────┐
│    │    │    │    │
┌───▼──┐┌───▼──┐┌───▼──┐
│API-1 ││API-2 ││API-3 │
└───┬──┘└───┬──┘└───┬──┘
    │      │      │
    └──────┼──────┘
           │
    ┌──────▼──────┐
    │  Database   │
    │ (Cassandra) │
    └─────────────┘
```

**Improvements**:
- Multiple API instances for horizontal scaling
- Load balancer distributes traffic
- Still has database as potential bottleneck

### Stage 3: Complete Architecture (✅ Production-Ready)

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Mobile App   │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌─────────────────┐
         │ Load Balancer   │
         └─────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│ API-1 │        │ API-2 │        │ API-3 │
└───┬───┘        └───┬───┘        └───┬───┘
    │                │                │
    └────────────────┼────────────────┘
                     │
         ┌───────────┼───────────┐
         │          │           │
    ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
    │ Redis   │ │ Redis   │ │ Redis   │
    │ Cluster │ │ Cluster │ │ Cluster │
    │(Cache + │ │(Cache + │ │(Cache + │
    │ Counter)│ │ Counter)│ │ Counter)│
    └────┬────┘ └────┬────┘ └────┬────┘
         │          │           │
         └──────────┼───────────┘
                    │
         ┌──────────▼───────────┐
         │    Cassandra        │
         │    Cluster          │
         │  (Multiple Nodes)   │
         └─────────────────────┘
```

## Component Details

### 1. Load Balancer

**Purpose**: Distribute incoming requests across multiple backend instances

**Benefits**:
- High availability (if one instance fails, others continue)
- Increased throughput (parallel processing)
- Health checks and automatic failover

**Configuration**:
- Round-robin or least-connections algorithm
- Health checks every 30 seconds
- Sticky sessions not required (stateless API)

### 2. API Servers

**Scaling Strategy**: Horizontal (multiple instances)

**Requirements per Instance**:
- Stateless design (no session storage)
- Share-nothing architecture
- Consistent behavior across all instances

**Instance Count Calculation**:
```
Required capacity: 1,160 writes/sec + 11,600 reads/sec = 12,760 req/sec
Single instance capacity: ~1,000 req/sec
Minimum instances: 13 instances
Recommended: 15-20 instances (with 50% headroom)
```

### 3. Redis Cluster

**Dual Purpose**:
1. **ID Generation**: Atomic counter for unique IDs
2. **Cache Layer**: Store frequently accessed URLs

#### Redis for ID Generation

```python
# Atomic increment - no race conditions
next_id = redis_client.incr('url_counter')
```

**High Availability**:
- Redis Cluster (3-6 nodes minimum)
- Or Redis Sentinel for automatic failover
- Critical for system operation (without it, cannot create new URLs)

#### Redis for Caching

**Strategy**: Cache Most-Frequently-Used (MFU) URLs

```python
# Cache popular URLs for 1 hour
redis_client.setex(f"url:{short_code}", 3600, long_url)
```

**Benefits**:
- Reduces database load
- Faster response times (memory vs disk)
- Handles 11,600 reads/sec efficiently

**Cache Hit Ratio Target**: 80-90%

### 4. Cassandra Cluster

**Why Cassandra?**

1. **Horizontal Scalability**
   - Can scale to hundreds of nodes
   - Handles billions of records easily
   - Supports 36.5 TB storage requirement

2. **High Write Throughput**
   - Optimized for write-heavy workloads
   - Handles 1,160 writes/sec per node easily
   - Linear scaling with more nodes

3. **High Availability**
   - Built-in replication
   - No single point of failure
   - Automatic data distribution

4. **Low Latency Reads**
   - Columnar storage optimized for reads
   - Partition key (short_code) enables fast lookups

**Schema**:
```cql
CREATE TABLE url_shortener (
    short_code TEXT PRIMARY KEY,
    long_url TEXT,
    created_at TIMESTAMP
);
```

**Replication**:
- Replication factor: 3 (3 copies of each record)
- Allows 1-2 node failures without data loss

## Data Flow

### URL Shortening Flow

```
1. Client → Load Balancer
2. Load Balancer → API Server (selected)
3. API Server → Redis (INCR counter) → Get unique ID
4. API Server → Convert ID to Base 62 with obfuscation
5. API Server → Cassandra (Store: short_code → long_url)
6. API Server → Client (Return short URL)
```

**Performance**:
- Average latency: < 50ms
- Database writes: Only to Cassandra (no reads needed)
- Redis operations: Single INCR (atomic, fast)

### URL Redirection Flow

```
1. Client → Load Balancer
2. Load Balancer → API Server
3. API Server → Redis Cache (Check first)
   ├─ Cache Hit: Return URL immediately
   └─ Cache Miss: Continue to step 4
4. API Server → Cassandra (Query by short_code)
5. API Server → Redis Cache (Store for future)
6. API Server → Client (301/302 redirect)
```

**Performance**:
- Cache Hit: < 5ms
- Cache Miss: < 20ms (Cassandra query)

## HTTP Status Codes Impact

### 301 vs 302 - Critical Architectural Decision

#### 301 Moved Permanently

**Behavior**:
- Browser caches redirect locally
- Subsequent requests go directly to destination (no server request)
- Reduces server load significantly

**Pros**:
- Minimal server load
- Faster for end users

**Cons**:
- Cannot track analytics (requests don't reach server)
- Cannot identify popular URLs for caching
- Cannot implement analytics dashboard

#### 302 Found (Temporary Redirect)

**Behavior**:
- Browser checks server on every request
- Server handles every redirect
- Full request path available

**Pros**:
- Can track all clicks
- Can identify popular URLs
- Enables analytics and caching strategy
- Can implement dashboards

**Cons**:
- Higher server load
- Every request hits backend

### Recommendation

**Use 302** for URL shortener because:
1. Enables analytics (critical feature)
2. Allows cache optimization (identify popular URLs)
3. Supports dashboard functionality
4. Cache layer can still reduce database load

**Note**: Status code choice fundamentally changes architecture. 301 makes cache layer unnecessary, but eliminates analytics capability.

## Capacity Planning

### Write Operations
- **Target**: 1,160 writes/sec
- **Peak**: Assume 2x average = 2,320 writes/sec
- **Cassandra**: Can handle ~5,000 writes/sec per node
- **Nodes Required**: 1 node (with 100% headroom) or 2 nodes (for redundancy)

### Read Operations
- **Target**: 11,600 reads/sec
- **Peak**: Assume 2x average = 23,200 reads/sec
- **Cache Hit Rate**: 85% = 19,720 cached, 3,480 DB queries/sec
- **Cassandra**: Can handle ~10,000 reads/sec per node
- **Nodes Required**: 1-2 nodes

### Total Nodes Required
- **Minimum**: 3 nodes (for replication factor 3)
- **Recommended**: 5-7 nodes (for performance and redundancy)

## High Availability Setup

### Multi-Region Deployment

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

**Benefits**:
- Geographic redundancy
- Lower latency (route to nearest region)
- Disaster recovery

## Monitoring and Metrics

### Key Metrics

1. **Throughput**
   - Writes/sec
   - Reads/sec
   - Cache hit rate

2. **Latency**
   - P50, P95, P99 response times
   - Cache latency vs database latency

3. **Availability**
   - Uptime percentage
   - Error rate
   - Failed requests

4. **Capacity**
   - Database size
   - Cache memory usage
   - Network bandwidth

## Next Steps

1. Implement caching strategy (identify popular URLs)
2. Set up monitoring and alerting
3. Plan for multi-region deployment
4. Design analytics dashboard
5. Implement rate limiting and security measures

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/architecture-design.pt-br.md)

---

**Related Documents**:
- [Scalability Patterns](scalability-patterns.md)
- [Performance Metrics](performance-metrics.md)

