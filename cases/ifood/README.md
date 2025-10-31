# iFood Case Knowledge Pack

## Purpose
Consolidate learnings from the iFood founding story/interview into actionable, reusable documentation aligned with our docs templates: architecture, engineering guidelines, data governance, use cases, and architectural decisions.

## Document Inventory
- `ifood-high-level-architecture.md`: End-to-end view of the early-to-scale iFood platform, from monolith + Oracle to microservices + Postgres + cloud, and the logistics real-time stack (MQTT, clustering, routing).
- `ifood-engineering-guidelines.md`: Speed-first development with guardrails, squads, incident handling, observability, and pragmatic refactoring through hyper-growth.
- `ifood-data-governance.md`: Experimentation (labs), pilot rollouts, risk containment, compliance aspects, and rollout percentage strategies.
- `uc-ifd-001-realtime-logistics-optimizer.md`: Core use case of real-time fleet orchestration: telemetry ingestion, clustering, routing (TSP heuristics), peak strategies.
- `adr-001-database-modernization.md`: Legacy Oracle to microservices + Postgres modernization.
- `adr-002-mqtt-for-telemetry.md`: Adopting MQTT for lightweight real-time location streaming.

## How to Use
1. Start with the high-level architecture to understand platform evolution and component boundaries.
2. Apply engineering guidelines to balance speed and scale under hyper-growth.
3. Use data-governance practices to run safe pilots and contain reputational risk.
4. Leverage the use case and ADRs when designing real-time logistics or modernizing legacy cores.

---

Maintainer: Skynet Docs Team  
Last Update: 2025-10-30


