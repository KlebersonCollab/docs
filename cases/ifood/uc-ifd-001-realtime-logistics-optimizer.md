# Use Case: Real-time Logistics Optimizer

## Basic Information
- **ID**: UC-IFD-001
- **Name**: Real-time fleet orchestration (telemetry → clustering → routing)
- **Version**: 1.0
- **Created**: 2025-10-30
- **Updated**: 2025-10-30

## Description
Continuously assign riders to pickup and delivery tasks by consuming live telemetry, dynamically clustering orders under peak, and computing feasible multi-stop routes (TSP-like heuristics) that minimise lateness and idle time.

## Actors
- **Rider Device** (Primary): sends location/status via MQTT.
- **Logistics Orchestrator** (Primary): consumes telemetry, runs clustering and routing.
- **Dispatcher/Operator** (Secondary): monitors dashboards, triggers regional controls in incidents.
- **Customer** (Secondary): receives ETA updates.

## Preconditions
- Telemetry ingest operational (broker up; auth OK).
- Restaurants publishing readiness; orders available in queue.
- Sufficient riders online in target regions.

## Postconditions
- Orders assigned to riders; ETAs updated; metrics/logs recorded.
- In peaks, batching applied and backlogs reduced progressively.

## Flow

### Main Flow
1. Telemetry arrives (MQTT → bus) with rider coordinates/status.
2. Orchestrator updates rider state; merges with order queue by region.
3. Clustering engine groups orders spatially/temporally per region.
4. Routing engine computes candidate sequences (heuristics); selects lowest cost.
5. Assignments published to rider app; customer ETAs notified.

## Alternate Flows
- **AF1 – Regional Overload**: backlog > threshold → enable batching; degrade to simpler policies; rate-limit new regions first.
- **AF2 – Sparse Riders**: widen search radius; relax constraints; prioritise SLA-critical orders.

## Exception Flows
- **EX1 – Telemetry Outage**: fall back to last-known positions; shorten assignment horizon; alert SRE.
- **EX2 – Routing Timeout**: return best-so-far route within time budget; log for offline improvement.

## Business Rules
- Prioritise by SLA risk and prep readiness.
- Bound routing compute-time per region (e.g., < 500ms median).
- Cap batch size to avoid excessive detours.

## Non-functional Requirements
- **Performance**: assignment cycle P95 < 2s per region.
- **Scalability**: support 100k+ concurrent orders at national peak via partitioning.
- **Reliability**: graceful degradation; retry with jitter on publish failures.

## Dependencies
- Telemetry broker (MQTT), event bus, rider app, restaurant readiness feed, assignment API.

## Test Scenarios
1. Peak-load synthetic: validate backlog decay and SLA adherence with batching enabled.
2. Telemetry-loss drill: verify fallback to last-known and alerting.
3. Routing-stress: ensure time-bounded heuristic returns best-so-far.

## Implementation Notes
- Partition by city → region → neighbourhood to keep problems tractable.
- Persist anonymised prompt/response if LLM is used for ops insights; do not use LLMs in assignment loop.
- Keep kill-switches for regional pauses; pre-warm workers before expected peaks.

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/uc-ifd-001-realtime-logistics-optimizer.pt-br.md)

---
Status: Draft


