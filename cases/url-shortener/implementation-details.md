# Implementation Details - URL Shortener

## Overview

This document details the implementation approach for generating unique short codes, avoiding collisions, and ensuring security.

## Short Code Generation

### Problem Statement

We need to generate a unique short code for each URL without:
- Hash collisions (same code for different URLs)
- Predictable patterns (security risk)
- Database lookups during generation (performance)

### Approach 1: Hash Functions (❌ Not Recommended)

#### Why Hash Functions Fail

1. **Wrong Base**
   - Hash functions (MD5, SHA1, CRC32) work with Base 16 (0-9, A-F)
   - This violates our requirement for Base 62
   - Results in longer short codes than necessary

2. **Collision Risk**
   - Different URLs can generate the same hash
   - Truncating hashes increases collision probability
   - Would require database lookups to verify uniqueness

3. **Performance Impact**
   - Every generation requires database check
   - Collisions increase exponentially over time (Birthday Paradox)
   - With 2.21 million URLs, collisions become likely

4. **Paradox of Birthday**
   - Even with 3.5 trillion possibilities
   - Collisions appear after ~2.21 million URLs
   - Given 100M URLs/day, collisions occur within minutes

#### Conclusion
Hash functions are **not suitable** for URL shortening due to collision risks and performance impact.

### Approach 2: Base 62 Conversion (✅ Recommended)

#### Concept

Convert a unique integer ID to Base 62 representation.

#### Base 62 Character Set

```
0-9  : 10 characters
a-z  : 26 characters
A-Z  : 26 characters
Total: 62 characters
```

**Mapping**:
- 0 → '0'
- 1 → '1'
- ...
- 9 → '9'
- 10 → 'A'
- 11 → 'B'
- ...
- 35 → 'Z'
- 36 → 'a'
- 37 → 'b'
- ...
- 61 → 'z'

#### Conversion Algorithm

**Example**: Convert 11,157 to Base 62

```
Step 1: 11,157 ÷ 62 = 179 remainder 59
Step 2: 179 ÷ 62 = 2 remainder 55
Step 3: 2 ÷ 62 = 0 remainder 2

Remainders (reverse order): 2, 55, 59

Mapping:
2  → '2'
55 → 'T'
59 → 'X'

Result: 11,157 in Base 62 = "2TX"
```

#### Implementation (Python)

```python
import base62

def encode_to_base62(decimal_number):
    """Convert decimal number to Base 62"""
    return base62.encode(decimal_number)

def decode_from_base62(base62_string):
    """Convert Base 62 string back to decimal"""
    return base62.decode(base62_string)

# Example
short_code = encode_to_base62(11157)  # Returns "2TX"
original_id = decode_from_base62("2TX")  # Returns 11157
```

#### Advantages

1. **Zero Collisions**: Each ID maps to exactly one Base 62 representation
2. **No Database Lookup**: Direct conversion, no verification needed
3. **Deterministic**: Same ID always produces same code
4. **Reversible**: Can decode short code back to original ID

#### Initial ID Value

**Security Consideration**: Starting from ID 1 makes codes predictable.

**Solution**: Start from a high initial value (e.g., 14 million)
- 62^4 = ~14.7 million combinations
- Starting at 14M ensures codes have at least 4 characters
- Prevents easy guessing of URLs

**Configuration**:
```python
INITIAL_ID = 14_000_000  # Start from 14 million
```

### Approach 3: Base 62 with ID Obfuscation (✅ Recommended for Production)

#### Problem with Sequential IDs

If IDs are sequential (1, 2, 3, 4...), the pattern becomes obvious:
- Easy to guess next URLs
- Security risk for private URLs
- Attackers can enumerate all URLs

#### Solution: HashID with Secret

Use a library like `hashids` to obfuscate the Base 62 encoding.

**Implementation**:
```python
from hashids import Hashids

# Create HashID instance with secret key
hashids = Hashids(
    salt='your-secret-key-here',
    min_length=4,
    alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
)

def encode_id_with_obfuscation(decimal_id):
    """Encode ID with obfuscation"""
    return hashids.encode(decimal_id)

def decode_id_from_obfuscation(obfuscated_code):
    """Decode obfuscated code back to ID"""
    decoded = hashids.decode(obfuscated_code)
    return decoded[0] if decoded else None

# Example
obfuscated = encode_id_with_obfuscation(11157)  # Returns "CJ0" (not "2TX")
original_id = decode_id_from_obfuscation("CJ0")  # Returns 11157
```

#### How It Works

1. Uses secret key to shuffle Base 62 alphabet
2. Same ID always produces same obfuscated code (deterministic)
3. Without secret key, cannot reverse-engineer pattern
4. Same secret key = same shuffle pattern

#### Security Benefits

- **Pattern Breaking**: Sequential IDs produce non-sequential codes
- **Secret-Dependent**: Only with secret key can codes be decoded
- **Non-Predictable**: Cannot guess next URL without secret

## Database Schema

### Cassandra Table Structure

```cql
CREATE TABLE url_shortener (
    short_code TEXT PRIMARY KEY,
    long_url TEXT,
    created_at TIMESTAMP
) WITH CLUSTERING ORDER BY (created_at DESC);
```

**Why Cassandra?**
- Horizontal scalability
- Handles billions of records
- High write throughput
- Built-in replication for availability
- Low latency reads

### Redis for ID Generation

**Command**: `INCR counter`

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

def get_next_id():
    """Get next unique ID from Redis"""
    return redis_client.incr('url_counter')
```

**Configuration**:
```python
# Set initial value
redis_client.set('url_counter', 14_000_000)
```

**Why Redis?**
- Atomic increment operation (no race conditions)
- Extremely fast (in-memory)
- Supports clustering for high availability

**High Availability Setup**:
- Redis Cluster mode
- Or Redis Sentinel for automatic failover
- Ensures 24x7 availability

## Complete Flow

### URL Shortening Flow

```
1. Client sends POST /api/v1/shorten with long URL
2. Backend receives request
3. Get next ID from Redis (INCR operation)
4. Convert ID to Base 62 (with obfuscation if enabled)
5. Store in Cassandra: short_code → long_url
6. Return short URL to client
```

### URL Redirection Flow

```
1. Client requests GET /{shortCode}
2. Backend receives request
3. Check Redis cache first (for popular URLs)
4. If not in cache, query Cassandra
5. If found, cache in Redis and return redirect
6. Return 301 or 302 with Location header
```

## Code Example (Complete Service)

```python
import redis
from cassandra.cluster import Cluster
from hashids import Hashids
import base62

class URLShortenerService:
    def __init__(self):
        # Redis for ID generation
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )
        
        # Initialize counter if needed
        if not self.redis.exists('url_counter'):
            self.redis.set('url_counter', 14_000_000)
        
        # HashID for obfuscation
        self.hashids = Hashids(
            salt='your-secret-key',
            min_length=4,
            alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        )
        
        # Cassandra connection
        cluster = Cluster(['127.0.0.1'])
        self.session = cluster.connect('url_shortener')
    
    def shorten_url(self, long_url: str) -> str:
        """Shorten a URL"""
        # Get next unique ID
        url_id = self.redis.incr('url_counter')
        
        # Encode with obfuscation
        short_code = self.hashids.encode(url_id)
        
        # Store in database
        self.session.execute(
            "INSERT INTO url_shortener (short_code, long_url, created_at) VALUES (?, ?, ?)",
            [short_code, long_url, datetime.now()]
        )
        
        return f"https://bit.ly/{short_code}"
    
    def get_original_url(self, short_code: str) -> str:
        """Get original URL from short code"""
        # Check cache first
        cached_url = self.redis.get(f"url:{short_code}")
        if cached_url:
            return cached_url
        
        # Query database
        result = self.session.execute(
            "SELECT long_url FROM url_shortener WHERE short_code = ?",
            [short_code]
        )
        
        if result:
            long_url = result[0].long_url
            # Cache for 1 hour
            self.redis.setex(f"url:{short_code}", 3600, long_url)
            return long_url
        
        raise ValueError("Short code not found")
```

## Key Takeaways

1. **Avoid Hash Functions**: Use Base 62 conversion instead
2. **Start High**: Begin ID sequence from 14M+ for security
3. **Obfuscate**: Use HashID with secret key to prevent pattern detection
4. **No Database Checks**: Direct conversion eliminates collision checks
5. **Atomic Operations**: Redis INCR ensures unique IDs across instances

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/implementation-details.pt-br.md)

---

**Related Documents**:
- [Architecture Design](architecture-design.md)
- [Security Considerations](security-considerations.md)

