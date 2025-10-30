# iFood Platform – High-Level Architecture

## Overview
iFood evolved from an analog operation to a technology platform supporting large-scale food delivery. The journey included:
- Initial monolithic core (Java) with a legacy Oracle database hosted on-prem.
- Progressive modernization: microservices, Postgres, message buses, and cloud.
- A real-time logistics subsystem for fleet orchestration using lightweight telemetry (MQTT), clustering and routing (TSP-like heuristics), and resilient SRE practices.

## Architectural Objectives
- **Speed-to-Value**: Ship fast; learn from pilots; iterate continuously.
- **Scalability**: Horizontal scale for order processing and real-time logistics at peak (e.g., Sunday evening, Valentine’s Day).
- **Availability**: Minimise downtime via resilient services, rollout strategies, and incident playbooks.
- **Security**: Secrets off-code, IAM, least-privilege, and controlled production change.
- **Operability**: Observability-first (metrics, logs, traces), clear on-call, and blunt incident response.

## Architecture Diagram
```mermaid
graph TD
  U[Customers (Web/Mobile)] --> GW[API Gateway]
  GW --> ORD[Order Service]
  GW --> RST[Restaurant Integration]
  GW --> PAY[Payment Adapter]
  GW --> LGX[Logistics Orchestrator]
  LGX --> TEL[Telemetry Ingest (MQTT)]
  TEL --> BUS[Event Bus (Kafka/Rabbit)]
  LGX --> CLU[Clustering Engine]
  LGX --> RTG[Routing Engine]
  ORD --> DBP[(Postgres)]
  RST --> CCH[(Cache)]
  SUB[Sub-systems (Promo, Catalog, User)] --> ORD
  OBS[Observability Stack] -->|Dashboards/Alerts| OPS[On-call/SRE]
  ORD --> OBS
  LGX --> OBS
  PAY --> OBS
```

## Main Components

### API Gateway
- **Responsibility**: Entry point, authn/z, rate limiting, routing.
- **Technology**: Managed gateway or envoy/nginx-based.

### Order Service (Evolution)
- **Responsibility**: Order lifecycle and state machine.
- **Tech Journey**: Monolith (Java) + Oracle → Microservices + Postgres.
- **Notes**: Legacy split driven by hotspots; database offloading during hyper-growth.

### Restaurant Integration
- **Responsibility**: Menu, availability, order push/ack to partners.
- **Tech**: REST/webhooks; aggressive caching to reduce load.

### Payment Adapter
- **Responsibility**: Abstraction over acquirers/anti-fraud.
- **Notes**: Externalised secrets, tokenisation.

### Logistics Orchestrator
- **Responsibility**: Assign riders, batch pickups, dynamic routing under peak.
- **Tech**: Event-driven; consumes telemetry; applies clustering and routing heuristics.

### Telemetry Ingest (MQTT)
- **Responsibility**: Lightweight ingestion of rider locations and status.
- **Rationale**: Reduced overhead vs HTTP; supports large fan-in.

### Event Bus
- **Responsibility**: Decouple producers/consumers; buffering; backpressure.
- **Tech**: Kafka/RabbitMQ depending on semantics.

### Clustering & Routing Engines
- **Responsibility**: Spatial-temporal clustering; TSP heuristics for batching.
- **Notes**: Problem decomposition: per-city → per-region → per-neighbourhood.

### Observability Stack
- **Responsibility**: Metrics (Prometheus), logs (centralised), traces (OpenTelemetry), alerting (Alertmanager).
- **SRE**: Correlation IDs, red/black dashboards, incident channels.

## Architectural Patterns
- **Strangler Modernization**: Carve out hotspots of the monolith into microservices.
- **Event-Driven Logistics**: Telemetry → bus → orchestrator → routing decisions.
- **Backpressure & Degradation**: Prefer degraded service vs meltdown (e.g., cancel-and-recover strategies under extreme backlog).
- **Pilot-First Rollouts**: Percentage-based enablement and explicit “beta” labels to reduce reputational risk.

## Key Architectural Decisions (Extract)
- Move from Oracle to Postgres microservices to eliminate single high-cost/low-agility DB bottleneck.
- Adopt MQTT for device telemetry to lower network and CPU overheads at large scale.
- Use city/region/neighbourhood partitioning to make routing computationally tractable.
- Run cloud-native logistics to exploit elasticity; reduce on-prem single-point risks.

## System Qualities
- **Performance**: Sub-minute assignment loops; telemetry up to seconds-level freshness.
- **Scalability**: Horizontal scaling of ingest and routing workers.
- **Availability**: Blue/green or canary for critical paths; rollback-first mindset.
- **Security**: Secrets management; least-privilege; production change approval.

## Technology Stack (indicative)
- **Services**: Java/Node microservices.
- **Datastores**: Postgres (OLTP), cache (Redis), object storage.
- **Messaging**: Kafka/RabbitMQ; MQTT broker.
- **Infra**: Kubernetes (cloud); IaC; GitOps.
- **Obs**: Prometheus, Loki/ELK, Jaeger/Tempo, Alertmanager.

---
Last Update: 2025-10-30

