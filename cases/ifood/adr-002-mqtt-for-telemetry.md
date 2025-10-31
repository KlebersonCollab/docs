# ADR-002: MQTT for Rider Telemetry Streaming

## Status
Accepted

## Context
HTTP for streaming rider coordinates/status incurred excessive overhead at scale; we needed lightweight, bi-directional, and reliable delivery to power real-time logistics.

## Decision
Adopt MQTT for rider/device telemetry ingestion. Use a managed/clustered broker; secure connections; topic strategy per region and rider.

## Consequences
- **Positive**: Lower network/CPU overhead, improved fan-in scalability, push semantics.
- **Negative**: New operational surface (broker); need for topic governance and backpressure strategies.

## Alternatives Considered
- Long-polling/HTTP streaming: heavier; less efficient under mobile conditions.
- WebSockets over HTTP: viable but heavier than MQTT for constrained devices.

## Implementation Notes
- Enforce TLS and auth; per-device credentials; short-lived tokens.
- Topic hierarchy: `/region/{id}/rider/{id}`; apply ACLs.
- Bridge MQTT → Kafka/Rabbit for downstream consumers.
- Backpressure: buffer with TTL; drop stale telemetry.

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/adr-002-mqtt-for-telemetry.pt-br.md)

---
Last Update: 2025-10-30


