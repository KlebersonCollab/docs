# Data Governance – iFood Case

## 1. Basic Information
- **ID**: DG-IFD-001
- **Project**: iFood Platform (Case Study)
- **Version**: 1.0
- **Created**: 2025-10-30
- **Updated**: 2025-10-30
- **Status**: Draft

## 2. Governance Overview
- **Objective**: Enable safe, fast experimentation (pilot-first) while containing reputational and operational risk.
- **Scope (Included)**: Order/restaurant/payment operational data, logistics telemetry (location/status), observability data.
- **Scope (Excluded)**: Non-operational back-office systems managed under separate governance.
- **Principles**: Pilot-first, risk containment, least-privilege, auditability, privacy-by-design.

## 3. Data Classification

### 3.1 Operational Data
- **Definition**: Order state, events, restaurant and payment operational data.
- **Examples**: Order lifecycle events, restaurant availability, payment transactions.
- **Classification**: Internal.
- **Retention**: Per business/legal requirements.
- **Access**: Authorized platform and product teams.

### 3.2 Telemetry Data
- **Definition**: Rider/device location and status information.
- **Examples**: Real-time GPS coordinates, rider status updates, device telemetry.
- **Classification**: Confidential.
- **Retention**: Short retention (30–90 days hot), longer cold only if justified.
- **Access**: Restricted to logistics and operations teams; redaction/anonymisation for analytics.

### 3.3 Financial Data
- **Definition**: Payment transactions and settlement information.
- **Examples**: Payment records, settlement transactions, financial logs.
- **Classification**: Internal/Confidential.
- **Retention**: Longer retention obligations (per regulatory requirements).
- **Access**: Finance and payment teams, auditors.

### 3.4 Observability Data
- **Definition**: Metrics, logs, and traces for system monitoring.
- **Examples**: Application logs, performance metrics, distributed traces.
- **Classification**: Internal.
- **Retention**: Rotation policies; PII redaction required.
- **Access**: Platform, SRE, and observability teams.

## 4. Data Policies

### 4.1 Quality Policy
- **Objective**: Ensure data quality through schema validation and consistency.
- **Responsibilities**: Platform team maintains schema registry; product teams validate events.
- **Controls**: Schema versioning; contracts on events; automated validation.

### 4.2 Security Policy
- **Objective**: Protect data through access controls and encryption.
- **Responsibilities**: Security lead manages secrets, IAM roles; platform team enforces policies.
- **Controls**: Secrets in vault, IAM roles; production access via break-glass with audit.

### 4.3 Privacy Policy
- **Objective**: Minimise PII exposure and comply with data protection regulations.
- **Responsibilities**: Privacy officer oversees PII handling; platform team implements redaction.
- **Controls**: Minimise PII in telemetry/logs; pseudonymise IDs for analytics.

### 4.4 Retention Policy
- **Objective**: Define clear retention SLAs per data type.
- **Responsibilities**: Data stewards define retention; platform team implements deletion.
- **Controls**: Clear SLAs per data type (e.g., telemetry 30–90 days hot, longer cold only if justified).

## 5. Organisation
- **Data Steward (Tech)**: Platform/SRE lead (telemetry, observability, access).
- **Data Steward (Business)**: Product leads (order/logistics domain needs, rollout %).
- **Security Steward**: Security lead (secrets, IAM, incident management).
- **Privacy Officer**: Oversees PII redaction, retention and DSARs if applicable.

## 6. Controls
- **Access**: VPN/SSO; role-based access; monthly access reviews.
- **Integrity**: checksums on event storage; schema registry; immutable logs.
- **Confidentiality**: TLS in transit; encrypted at rest; redaction pipelines.

## 7. Data Policies

*Note: Detailed policies are defined in section 4. This section provides a summary.*

## 8. Processes
- **Pilot Rollout**: 1–5% cohorts labelled beta; run A/B; collect outcomes; gated promotion.
- **Incident**: detect → contain (regional pause/rate-limit) → recover → post-mortem.
- **Change Management**: GitOps; approvals; traceable migrations.

## 9. Metrics & KPIs
- **Quality**: event schema conformance ≥99.5%, order state consistency ≥99.9%.
- **Security**: 0 critical secret exposures; time-to-rotate < 24h.
- **Privacy**: 0 unresolved PII leaks; DSAR SLA compliance 100%.
- **Ops**: telemetry freshness P95 < 5s; assignment time P95 < target.

## 10. Compliance
- Map operational data flows; DPIA for new telemetry uses.
- Maintain audit trails for deployments, access, and retention jobs.

## 11. Tooling
- Schema registry, lineage (via event catalog), DLP/redaction, SIEM, observability suite.

## 12. Implementation Plan
- Phase 1: define classifications/retention; deploy redaction.
- Phase 2: enforce IAM/least-privilege; automate access reviews.
- Phase 3: automate pilot gates; dashboards for telemetry/assignment KPIs.

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/ifood-data-governance.pt-br.md)

---
Owner: Data Steward (Tech)


