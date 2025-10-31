# URL Shortener - System Design Case Study

## Overview

URL Shortener is a classic system design challenge that demonstrates the same architectural principles used in large-scale applications like YouTube, Instagram, Uber, and Netflix. Despite appearing simple, this system requires careful consideration of scalability, performance, and distributed systems concepts.

## Table of Contents

1. [Requirements Analysis](requirements-analysis.md)
2. [Architecture Design](architecture-design.md)
3. [Implementation Details](implementation-details.md)
4. [Scalability Patterns](scalability-patterns.md)
5. [Security Considerations](security-considerations.md)
6. [Performance Metrics](performance-metrics.md)

## Key Insights

### Critical Principle
> "Every architecture is made to meet very well-defined requirements. Without requirements, you cannot architect anything because anything you try to architect will be based on guessing. And we don't work with guessing."

### Core Concepts

1. **Requirements First**: Functional and non-functional requirements must be clearly defined before any architectural decisions
2. **Mathematical Foundation**: All architectural choices are based on calculations, estimates, and approximations
3. **No Perfect Solution**: Trade-offs are inherent in every architectural decision
4. **Status Code Impact**: Even HTTP status codes (301 vs 302) affect the entire system architecture

## Quick Reference

### Problem Statement
Given a long URL, create a short URL. When the short URL is requested, redirect the user to the original URL.

### Key Requirements
- **Functional**: URL shortening and redirection
- **Non-functional**: High volume, low latency, high availability

### Technology Stack
- **Database**: Cassandra (for horizontal scalability and high availability)
- **Cache**: Redis (for frequently accessed URLs and ID generation)
- **Load Balancer**: For horizontal scaling
- **Backend**: Multiple instances for high availability

## Related Documentation

- [Database Selection Guide](../architecture/database-selection-guide.md)
- [Cache Layer Patterns](../architecture/escalabilidade/05-cache-layer.md)
- [Load Balancing](../architecture/escalabilidade/03-load-balancing.md)

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/README.pt-br.md)

---

**Source**: Video transcription - System Design Interview
**Last Updated**: January 2025
**Maintainer**: Skynet Team

