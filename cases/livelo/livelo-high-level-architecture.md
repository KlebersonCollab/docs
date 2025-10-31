# Livelo AI Platform - High-Level Architecture

## Overview
Livelo operates a company-wide AI and automation platform that combines conversational interfaces, low-code orchestration, and controlled model consumption. The platform enables three strategic pillars:

- **Customer-facing expert** delivering travel planning and points optimisation.
- **Internal AI agents** that streamline legal, engineering, and business workflows.
- **Automation centre of excellence** that accelerates back-office processes.

The architecture focuses on rapid experimentation with strict governance, allowing squads to prove value quickly while keeping scale, security, and compliance under control.

## Architectural Objectives
- **Performance**: Real-time or near-real-time responses for conversational agents (<2 seconds for standard prompts) with asynchronous handling for heavy automations.
- **Scalability**: Horizontal scaling through Kubernetes for N8N and Open WebUI pods; dynamic fan-out of agent workflows to accommodate demand spikes.
- **Availability**: Target 99.5% uptime for internal agents and 99.9% for the customer-facing expert using redundancy across clusters.
- **Security**: Isolated cloud account, VPN-only access, dedicated guardrails, and strict prompt sanitisation mitigate prompt-injection and data exfiltration risks.
- **Maintainability**: Modular workflows, declarative agent definitions, and automated linting keep automations understandable and easy to iterate.

## Architecture Diagram
```mermaid
graph TD
    subgraph Users
        U1[Livelo Employees]
        U2[Livelo Customers]
    end

    U1 -->|VPN| OWUI[Open WebUI]
    U2 --> EXPERT[Expert Livelo Chat]

    OWUI -->|Slash commands| N8N[N8N Orchestrator]
    EXPERT -->|REST/gRPC| N8N

    N8N --> RAG[RAG + Knowledge Sources]
    N8N --> BUD[LiteLLM Budget Manager]
    N8N -->|API| MODELS{Model Providers}
    MODELS --> OAI[OpenAI]
    MODELS --> GCP[Vertex AI]
    MODELS --> AWS[Amazon Bedrock]

    BUD -->|Pre-paid quotas| FIN[Financial Systems]

    subgraph Platform Runtime (Isolated Account)
        K8S[Kubernetes Cluster]
        OBS[Observability Stack]
    end

    N8N -.->|Deployments| K8S
    OWUI -.-> K8S
    N8N --> OBS
    BUD --> OBS

    SEC[Security Controls]:::security -.-> U1
    SEC -.-> OWUI
    SEC -.-> N8N

    classDef security fill:#fce5cd,stroke:#cc0000,stroke-width:1.5px;
```

## Main Components

### Open WebUI
- **Responsibility**: Provide a unified conversational interface for internal users with slash-command extensions for knowledge uploads.
- **Technology**: Open WebUI (self-hosted) deployed in Kubernetes; integrates with corporate SSO via VPN.
- **Interfaces**: Web sockets for chat, REST hooks to N8N, command hooks to RAG ingestion pipelines.
- **Dependencies**: N8N workflow endpoints, authentication gateway.

### Expert Livelo Chat
- **Responsibility**: Customer-facing conversational experience for points planning and travel itinerary optimisation.
- **Technology**: Web and mobile clients calling serverless adapters that route to N8N agents.
- **Interfaces**: REST APIs, streaming responses.
- **Dependencies**: N8N orchestration, agent catalogue, observability stack.

### N8N Orchestrator
- **Responsibility**: Central workflow engine for AI agents, automation routines, and multi-step integrations.
- **Technology**: N8N (open-source) running in Kubernetes with autoscaling pods.
- **Interfaces**: REST, webhooks, queue processors.
- **Dependencies**: LiteLLM, knowledge stores, Git repositories, third-party APIs.

### LiteLLM Budget Manager
- **Responsibility**: Token spend control with pre-paid balancing per area; prevents runaway costs and enforces accountability.
- **Technology**: LiteLLM with custom budget enforcement routines; integrated with corporate finance systems.
- **Interfaces**: REST for quota checks, event hooks for low-credit alerts.
- **Dependencies**: Finance ledger, notification services, monitoring stack.

### Model Providers Abstraction
- **Responsibility**: Route prompts to the best available model (OpenAI, Google Gemini, Anthropic Claude via Bedrock, etc.).
- **Technology**: LiteLLM adapters, N8N connectors, SDK-specific wrappers.
- **Interfaces**: Standardised prompt APIs, response normalisation layer.
- **Dependencies**: Provider credentials, latency dashboards, fallback strategies.

### Knowledge & RAG Layer
- **Responsibility**: Manage private corpora (PDFs, policies, process documents) ingested via slash commands and converted to embeddings.
- **Technology**: N8N pipelines, vector store (proprietary), access policies via LiteLLM.
- **Interfaces**: Document upload, retrieval API, search endpoints.
- **Dependencies**: Storage buckets, malware scanning, metadata catalogue.

### Observability Stack
- **Responsibility**: Provide tracing, logging, and metrics for each agent run, including token usage and success rate.
- **Technology**: Prometheus/Grafana, centralised logging, tracing plug-ins from Flowise/LLM frameworks.
- **Interfaces**: Metrics exporters, OpenTelemetry collectors, dashboards.
- **Dependencies**: Kubernetes, LiteLLM events, Git hooks.

### Security Controls
- **Responsibility**: Enforce VPN-only access, prompt sanitisation, guardrails against prompt injection, and segregated environments.
- **Technology**: Dedicated cloud account, IAM policies, WAF rules, secret rotation.
- **Interfaces**: IAM, network ACLs, policy enforcement points.
- **Dependencies**: Corporate identity provider, compliance tooling, security operations centre.

## Architectural Patterns

### Pattern 1: Low-Code Orchestration for Agent Pipelines
- **Description**: Use N8N to model AI workflows graphically, enabling engineers and semi-technical staff to build automations.
- **Application**: Internal AI agents, customer expert, automation centre of excellence.
- **Benefits**: Fast iteration, shared knowledge, reusable workflows, lower barrier for non-developers with oversight.
- **Trade-offs**: Requires strong governance to avoid overloading the orchestrator; limited for high-throughput transactional workloads.

### Pattern 2: Multi-Cloud Model Routing with Budget Enforcement
- **Description**: Abstract model providers and couple each call with quota checks.
- **Application**: Every agent call passes through LiteLLM to deduct credits.
- **Benefits**: Cost transparency, easy switching between models, vendor diversification.
- **Trade-offs**: Additional latency for quota checks; requires financial reconciliation.

## Architectural Decisions

### Decision 1: Adopt N8N Instead of Fully Custom Microservices
- **Context**: Need for rapid prototyping and empowerment of non-traditional developers while keeping technical flexibility.
- **Decision**: Standardise on N8N across squads with Kubernetes scaling and shared governance policies.
- **Consequences**: Simplified onboarding, consistent tooling, ability to reuse connectors; must limit heavy transactional workloads.
- **Alternatives**: Custom Node/Go microservices (slower delivery), other low-code tools like Make/Zapier (insufficient governance, SaaS lock-in).

### Decision 2: Use LiteLLM with Pre-Paid Budgets per Agent Owner
- **Context**: Prevent cost overruns and empower business units to self-manage spend.
- **Decision**: Implement mandatory pre-paid quota per agent; trigger alerts when credits run low.
- **Consequences**: Zero risk of unexpected bills, clear accountability; requires finance workflows to approve top-ups.
- **Alternatives**: Centralised monthly caps (less granular), custom cost dashboards (reactive only).

### Decision 3: Operate the Platform in a Segregated Cloud Account with VPN Access
- **Context**: AI guardrails, need to contain experimentation risks, comply with security standards.
- **Decision**: Deploy Open WebUI, N8N, and LiteLLM inside a restricted account with no public internet egress except whitelisted providers.
- **Consequences**: Strong containment, easier audits; extra operational overhead for cross-account integrations.
- **Alternatives**: Shared corporate account (higher blast radius), SaaS hosting (less control, compliance risk).

## System Qualities

### Performance
- **Metrics**: Response latency (<2s average), token consumption per run, throughput per agent.
- **Strategies**: Autoscaling pods, caching RAG results, asynchronous job queues for heavy tasks.
- **Monitoring**: Prometheus dashboards, LiteLLM cost telemetry, alerting on slow workflows.

### Scalability
- **Strategies**: Horizontal pod autoscaling, stateless workflow executions, decoupled connectors.
- **Horizontal**: Scale N8N pods and worker queues for concurrency.
- **Vertical**: Temporary CPU/memory boosts for embedding jobs.

### Availability
- **SLA**: 99.5% internal, 99.9% external.
- **Strategies**: Multi-zone Kubernetes clusters, automated failover, backup orchestrator nodes.
- **Recovery**: Automated redeploy via GitOps, playbooks for restoring RAG stores and budgets.

### Security
- **Authentication**: VPN + SSO for employees; customer identity via Livelo accounts.
- **Authorization**: Role segmentation for agent owners, reviewers, and observers.
- **Cryptography**: TLS termination at ingress, encrypted storage for embeddings and secrets.

## Technology Stack

### Frontend
- **Framework**: Open WebUI with custom slash-command extensions.
- **Language**: TypeScript custom widgets, React for customer channels.
- **Tools**: Corporate design system integrations, accessibility validators.

### Backend
- **Framework**: N8N workflows, Python/TypeScript Function nodes, serverless adapters for Expert Livelo.
- **Language**: TypeScript, Python, Bash for automation scripts.
- **APIs**: REST, GraphQL (planned), webhook triggers.

### Database
- **Type**: Vector store for RAG, Postgres for operational metadata, object storage for documents.
- **Strategies**: Malware scanning on upload, metadata tagging for access control, versioning for knowledge sources.

### Infrastructure
- **Cloud**: AWS and GCP (model access + optional workloads); dedicated sandbox account for core runtime.
- **Containerisation**: Docker images for Open WebUI and N8N.
- **Orchestration**: Kubernetes with GitOps deployment pipelines.

## Architectural Risks

### Risk 1: Uncontrolled Workflow Growth Overloading N8N
- **Impact**: High – platform instability and degraded experience.
- **Probability**: Medium.
- **Mitigation**: AI board approvals, workflow linting, guardrail policies, workload classification (experiments vs production).

### Risk 2: Prompt Injection or Data Leakage via Conversational Agents
- **Impact**: Critical – potential legal/compliance breaches.
- **Probability**: Medium.
- **Mitigation**: Prompt sanitisation, sandboxed execution, separated knowledge stores, automated security testing, continuous red-team exercises.

### Risk 3: Model Vendor Dependency or Performance Regression
- **Impact**: Medium.
- **Probability**: Medium.
- **Mitigation**: Multi-cloud abstraction, continuous benchmarking, fallback models, on-call escalation when latency exceeds thresholds.

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/livelo-high-level-architecture.pt-br.md)

---

**Last Update**: 2025-10-30  
**Source**: Livelo interview on PPT Não Compila podcast.


