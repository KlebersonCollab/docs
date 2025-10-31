# ADR-001: Database Modernization – Oracle to Postgres Microservices

## Status
Accepted

## Context
Early iFood operations relied on a single Oracle instance hosted on-prem. As volume spiked, this created: cost pressure (per-core licensing), operational risk (single bottleneck), and scale barriers. The monolith’s growth aggravated DB hotspots.

## Decision
Adopt a strangler approach to carve out monolith hotspots into domain microservices backed by Postgres. Each service owns its schema; shared-nothing as default. Use caching for read-heavy paths.

## Consequences
- **Positive**: Reduced blast radius, improved agility, lower infra/license costs, domain-aligned schemas.
- **Negative**: Operational complexity (service sprawl), distributed transactions, eventual consistency.

## Alternatives Considered
- Scale-up Oracle cluster: limited agility; licensing cost; still central bottleneck.
- Sharded Oracle: complex + expensive; vendor lock-in.

## Implementation Notes
- Prioritise high-churn, high-load domains for first extractions.
- Introduce eventing to avoid tight coupling between services.
- Maintain dual-write only under strict, short-lived migration windows.

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/adr-001-database-modernization.pt-br.md)

---
Last Update: 2025-10-30


