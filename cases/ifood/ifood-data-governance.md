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

## 3. Organisation
- **Data Steward (Tech)**: Platform/SRE lead (telemetry, observability, access).
- **Data Steward (Business)**: Product leads (order/logistics domain needs, rollout %).
- **Security Steward**: Security lead (secrets, IAM, incident management).
- **Privacy Officer**: Oversees PII redaction, retention and DSARs if applicable.

## 4. Data Classification
- **Operational**: orders, states, events → Internal; retention per business/legal needs.
- **Telemetry**: rider/device location/status → Confidential; short retention; redaction/anonymisation for analytics.
- **Financial**: payments/settlements → Internal/Confidential; longer retention obligations.
- **Observability**: metrics/logs/traces → Internal; PII redaction; rotation policies.

## 5. Policies
- **Quality**: schema versioning; contracts on events; automated validation.
- **Security**: secrets in vault, IAM roles; production access via break-glass with audit.
- **Privacy**: minimise PII in telemetry/logs; pseudonymise IDs for analytics.
- **Retention**: clear SLAs per data type (e.g., telemetry 30–90 days hot, longer cold only if justified).

## 6. Controls
- **Access**: VPN/SSO; role-based access; monthly access reviews.
- **Integrity**: checksums on event storage; schema registry; immutable logs.
- **Confidentiality**: TLS in transit; encrypted at rest; redaction pipelines.

## 7. Processes
- **Pilot Rollout**: 1–5% cohorts labelled beta; run A/B; collect outcomes; gated promotion.
- **Incident**: detect → contain (regional pause/rate-limit) → recover → post-mortem.
- **Change Management**: GitOps; approvals; traceable migrations.

## 8. Metrics & KPIs
- **Quality**: event schema conformance ≥99.5%, order state consistency ≥99.9%.
- **Security**: 0 critical secret exposures; time-to-rotate < 24h.
- **Privacy**: 0 unresolved PII leaks; DSAR SLA compliance 100%.
- **Ops**: telemetry freshness P95 < 5s; assignment time P95 < target.

## 9. Compliance
- Map operational data flows; DPIA for new telemetry uses.
- Maintain audit trails for deployments, access, and retention jobs.

## 10. Tooling
- Schema registry, lineage (via event catalog), DLP/redaction, SIEM, observability suite.

## 11. Implementation Plan
- Phase 1: define classifications/retention; deploy redaction.
- Phase 2: enforce IAM/least-privilege; automate access reviews.
- Phase 3: automate pilot gates; dashboards for telemetry/assignment KPIs.

---
Owner: Data Steward (Tech)

