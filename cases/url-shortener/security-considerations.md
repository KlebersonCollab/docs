# Security Considerations - URL Shortener

## Overview

Security in URL shorteners involves preventing URL enumeration, protecting private URLs, and ensuring the system cannot be abused.

## Key Security Concerns

### 1. Predictable Short Codes

#### Problem

If short codes are generated sequentially from ID 1, they become predictable:
- Short code for ID 1: "1" (or "2TX" in base 62)
- Short code for ID 2: "2" (or next in sequence)
- Attackers can enumerate all URLs

#### Attack Scenario

```python
# Attacker can guess URLs
for i in range(1, 1000000):
    short_code = encode_base62(i)
    url = f"https://bit.ly/{short_code}"
    # Try to access URL
```

#### Solution: Start from High Initial Value

```python
INITIAL_ID = 14_000_000  # 62^4 = ~14.7M combinations

# Ensures:
# - Minimum 4 characters in short code
# - Cannot enumerate from start
# - Requires testing 14M+ combinations
```

**Calculation**:
- 62^4 = 14,776,336 combinations
- Starting at 14M ensures 4-character minimum
- Makes enumeration impractical

### 2. Sequential Pattern Detection

#### Problem

Even with high starting ID, sequential patterns are detectable:

```
ID: 14,000,000 → Code: "abc1"
ID: 14,000,001 → Code: "abc2"
ID: 14,000,002 → Code: "abc3"
```

Pattern becomes obvious after a few examples.

#### Solution: ID Obfuscation (HashID)

Use a library like `hashids` to shuffle the Base 62 encoding:

```python
from hashids import Hashids

hashids = Hashids(
    salt='secret-key-known-only-to-server',
    min_length=4,
    alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
)

# Sequential IDs produce non-sequential codes
hashids.encode(14000000)  # Returns: "CJ0"
hashids.encode(14000001)  # Returns: "X9K"
hashids.encode(14000002)  # Returns: "L2P"
```

#### How It Works

1. **Secret Key**: Server uses secret to shuffle alphabet
2. **Deterministic**: Same ID always produces same code
3. **Non-Reversible**: Without secret, cannot determine pattern
4. **Pattern Breaking**: Sequential IDs → Non-sequential codes

### 3. Secret Key Management

#### Requirements

- **Storage**: Environment variables or secret management service
- **Rotation**: Plan for key rotation strategy
- **Backup**: Secure backup (losing key breaks existing URLs)

```python
import os

SECRET_KEY = os.environ.get('URL_SHORTENER_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("Secret key must be set")
```

#### Key Rotation Strategy

**Challenge**: Changing secret breaks all existing URLs

**Solutions**:
1. **Multi-Secret Support**: Support multiple secrets (old + new)
2. **Migration Period**: Gradual transition with both secrets active
3. **Database Storage**: Store original ID, regenerate codes if needed

### 4. URL Validation and Filtering

#### Malicious URLs

Prevent abuse by validating URLs:

```python
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate URL before shortening"""
    try:
        result = urlparse(url)
        
        # Must have scheme
        if not result.scheme:
            return False
        
        # Must be HTTP/HTTPS
        if result.scheme not in ['http', 'https']:
            return False
        
        # Must have netloc (domain)
        if not result.netloc:
            return False
        
        # Block internal/localhost URLs
        if result.netloc in ['localhost', '127.0.0.1', '0.0.0.0']:
            return False
        
        # Check for malicious patterns
        malicious_patterns = [
            'javascript:',
            'data:',
            'vbscript:',
            'file:'
        ]
        
        if any(pattern in url.lower() for pattern in malicious_patterns):
            return False
        
        return True
    
    except Exception:
        return False
```

### 5. Rate Limiting

#### Protection Against Abuse

Implement rate limiting to prevent:
- DDoS attacks
- Automated URL generation
- Resource exhaustion

```python
from redis import Redis
import time

redis_client = Redis()

def check_rate_limit(user_ip: str, limit: int = 100, window: int = 3600) -> bool:
    """Check if user exceeded rate limit"""
    key = f"rate_limit:{user_ip}"
    
    current = redis_client.incr(key)
    
    if current == 1:
        redis_client.expire(key, window)
    
    return current <= limit
```

**Configuration**:
- **Limit**: 100 URLs per hour per IP
- **Window**: 1 hour sliding window
- **Strict Mode**: Block after limit exceeded
- **Soft Mode**: Return slower responses

### 6. Private URL Protection

#### Requirement

Some URLs should be private and not discoverable.

#### Solutions

##### Option 1: Custom Short Codes
Allow users to specify their own codes (with validation):

```python
def create_custom_short_code(user_code: str) -> bool:
    """Allow user to create custom short code"""
    # Validate format
    if not re.match(r'^[a-zA-Z0-9]{4,7}$', user_code):
        return False
    
    # Check availability
    if code_exists(user_code):
        return False
    
    return True
```

##### Option 2: Authentication Required
Require authentication for URL creation:

```python
def shorten_url(long_url: str, user_id: int) -> str:
    """Create short URL with user association"""
    url_id = get_next_id()
    short_code = encode_with_obfuscation(url_id)
    
    # Store with user association
    store_url(short_code, long_url, user_id)
    
    return short_code
```

##### Option 3: Expiration and Access Control
Add expiration and access controls:

```python
def shorten_url_with_expiry(
    long_url: str,
    expires_in_days: int = None,
    password: str = None
) -> str:
    """Create URL with optional expiration and password"""
    short_code = create_short_code()
    
    metadata = {
        'long_url': long_url,
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(days=expires_in_days) if expires_in_days else None,
        'password': hash_password(password) if password else None
    }
    
    store_url(short_code, metadata)
    return short_code
```

### 7. HTTPS Enforcement

#### Requirement

All communications must be encrypted.

**Configuration**:
- Force HTTPS redirects
- HSTS headers
- SSL/TLS certificates

```python
# Middleware example
@app.before_request
def force_https():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return redirect(request.url.replace('http://', 'https://'), 301)
```

### 8. Input Sanitization

#### Prevent Injection Attacks

```python
def sanitize_url(url: str) -> str:
    """Sanitize URL input"""
    # Remove control characters
    url = ''.join(char for char in url if ord(char) >= 32)
    
    # Limit length
    if len(url) > 2048:
        raise ValueError("URL too long")
    
    # Validate encoding
    try:
        url.encode('utf-8')
    except UnicodeEncodeError:
        raise ValueError("Invalid URL encoding")
    
    return url
```

## Security Checklist

### Before Production

- [ ] Secret key stored securely (not in code)
- [ ] HTTPS enforced
- [ ] Rate limiting implemented
- [ ] URL validation active
- [ ] Input sanitization
- [ ] Monitoring and alerting
- [ ] Access logs enabled
- [ ] Security headers configured
- [ ] Regular security audits
- [ ] Incident response plan

### Ongoing

- [ ] Monitor for suspicious patterns
- [ ] Review access logs regularly
- [ ] Update dependencies
- [ ] Security patches applied
- [ ] Penetration testing
- [ ] Security training for team

## Security Best Practices Summary

1. **Start High**: Begin ID sequence from 14M+ to prevent enumeration
2. **Obfuscate**: Use HashID with secret key to break sequential patterns
3. **Validate**: Check all URLs before shortening
4. **Limit**: Implement rate limiting to prevent abuse
5. **Encrypt**: Enforce HTTPS everywhere
6. **Monitor**: Track and alert on suspicious activity
7. **Rotate**: Plan for secret key rotation
8. **Sanitize**: Clean all inputs

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/security-considerations.pt-br.md)

---

**Related Documents**:
- [Implementation Details](implementation-details.md)
- [Architecture Design](architecture-design.md)

