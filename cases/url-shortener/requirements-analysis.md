# Requirements Analysis - URL Shortener

## Overview

Before designing any architecture, it is critical to understand and establish requirements. This document outlines the functional and non-functional requirements for a URL shortener system.

## Functional Requirements

### 1. URL Shortening
**Description**: The system must be capable of shortening a long URL into a short URL.

**Endpoint**: `POST /api/v1/shorten`

**Request**:
```json
{
  "url": "https://example.com/very/long/url/with/many/parameters"
}
```

**Response**: `201 Created`
```json
{
  "shortUrl": "https://bit.ly/2tx"
}
```

### 2. URL Redirection
**Description**: When a short URL is accessed, the system must redirect the user to the original URL.

**Endpoint**: `GET /{shortCode}`

**Response**: `301 Moved Permanently` or `302 Found`
```
Location: https://example.com/very/long/url/with/many/parameters
```

## Non-Functional Requirements

### 1. Volume Capacity
- **Requirement**: System must support 100 million URLs generated per day
- **Breakdown**:
  - 100,000,000 URLs / 24 hours / 60 minutes / 60 seconds
  - **Write Operations**: ~1,160 requests per second
  - **Read Operations**: ~11,600 requests per second (10:1 ratio)

### 2. Short Code Length
- **Requirement**: Short code must be as short as possible
- **Constraint**: Only numbers 0-9, lowercase letters a-z, and uppercase letters A-Z are allowed (Base 62)
- **Calculation Result**: 7 characters minimum for 365 billion unique combinations

### 3. Character Set Restriction
- **Allowed**: 0-9, a-z, A-Z (62 characters total - Base 62)
- **Not Allowed**: Special characters that may cause issues in URLs

### 4. Read-Write Ratio
- **Requirement**: For each write operation, there will be 10 read operations
- **Rationale**: This is the average for most real-world applications
- **Impact**: Architecture must be optimized for read-heavy workloads

### 5. URL Storage Size
- **Average Length**: 100 bytes per URL stored in database
- **Purpose**: Used for capacity calculations

### 6. Data Retention
- **Requirement**: URLs must be stored for 10 years
- **Total Storage Calculation**:
  - 100 million URLs/day × 365 days × 10 years = 365 billion records
  - 365 billion × 100 bytes = 36.5 TB total storage

### 7. High Availability
- **Requirement**: System must operate in 24x7 high availability mode
- **Impact**: No single points of failure, redundancy required at all layers

## Calculations Summary

### Throughput
| Metric | Value |
|--------|-------|
| URLs per day | 100,000,000 |
| Write operations/sec | ~1,160 |
| Read operations/sec | ~11,600 |
| Read:Write ratio | 10:1 |

### Storage
| Metric | Value |
|--------|-------|
| Records over 10 years | 365 billion |
| Average URL size | 100 bytes |
| Total storage required | 36.5 TB |

### Short Code Specifications
| Metric | Value |
|--------|-------|
| Character set | Base 62 (0-9, a-z, A-Z) |
| Minimum length | 7 characters |
| Total combinations | 3.5 trillion |

## Key Questions for Interview Scenarios

When faced with a system design interview, ask these questions:

1. **Traffic Volume**
   - What is the daily traffic volume?
   - What are the peak traffic patterns?

2. **Operations Ratio**
   - What is the read:write ratio?
   - How do operations vary by time of day?

3. **Storage Requirements**
   - How long should data be retained?
   - What is the average size of stored data?

4. **Availability Requirements**
   - What is the acceptable downtime?
   - What are the SLAs?

5. **Security Requirements**
   - Are there privacy concerns?
   - Should short codes be predictable or obfuscated?

## Requirement-Driven Architecture

> **Critical Principle**: All architectural decisions must be based on requirements. Without clear requirements, any architecture will be based on guessing.

### Decision Tree

1. **High Volume** → Requires horizontal scaling, not vertical
2. **Read-Heavy** → Cache layer is essential
3. **Large Storage** → Database choice critical (Cassandra for horizontal scaling)
4. **High Availability** → Redundancy at all layers
5. **Unique Short Codes** → Requires careful algorithm selection

## Next Steps

After establishing requirements:
1. Calculate all necessary metrics (throughput, storage, etc.)
2. Choose appropriate technologies based on requirements
3. Design architecture patterns (caching, load balancing, etc.)
4. Plan for scalability and high availability

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/requirements-analysis.pt-br.md)

---

**Related Documents**:
- [Architecture Design](architecture-design.md)
- [Implementation Details](implementation-details.md)

