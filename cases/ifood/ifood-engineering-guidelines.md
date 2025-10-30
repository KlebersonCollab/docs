# Engineering Guidelines – iFood Case

## Basic Information
- **Guideline ID**: EG-IFD-001
- **Project**: iFood Platform (Case Study)
- **Version**: 1.0
- **Created**: 2025-10-30
- **Updated**: 2025-10-30
- **Approved by**: (TBD)

## Purpose
Codify speed-first engineering practices with pragmatic guardrails suited for hyper-growth platforms, reflecting lessons learned in the iFood journey.

## Scope
Applies to order, restaurant, payment, logistics, and observability components; valid for prototypes, pilots, and production services.

## Applicability
- Mandatory for production-bound changes.
- Recommended during discovery to reduce future rework.

## Coding Standards
- **Naming**: lowerCamelCase (TS/JS), snake_case (Python), PascalCase (classes), UPPER_SNAKE_CASE (consts).
- **Structure**: small modules; functions under 50 lines where feasible; avoid god-objects.
- **Docs**: JSDoc/docstrings for public functions; README per service with runbook/rollback.

## Architecture & Design
- **Strangler Pattern** for modernization from monolith.
- **Event-Driven** logistics and order side effects.
- **Cache-First** on read-heavy paths (menus, availability).
- **Bulkheads & Timeouts** around external calls; retries with jitter.

## Development Workflow
1. Plan: define problem, KPIs, guardrails (budget/latency/errors).
2. Build: feature flags; dark launches; backwards compatibility by default.
3. Test: unit (≥80%), integration (mocks for providers), e2e smoke on happy/unhappy.
4. Deploy: canary/blue-green via GitOps; fast rollback available.

## Version Control
- Branches: feature/* → develop → main.
- Commits: Conventional Commits; link ticket.
- Tags: service semver; immutable images.

## Observability
- **Metrics**: latency P50/P95/P99, error rate, queue lag, telemetry freshness, rider assignment time.
- **Logs**: JSON with correlation IDs; redact PII; sampling under peak.
- **Traces**: end-to-end on critical flows (order create, rider assign).
- **Alerts**: SLO-based alerts; on-call runbooks; escalation paths.

## Security
- Secrets in vault; no secrets in code.
- Principle of least privilege for DB/message/internals.
- Audit deployment and schema changes; 4-eyes for prod.

## Performance
- Perf budgets per endpoint; fail-fast on overload.
- Caches with TTL + cache-busting events.
- Asynchronous pipelines for heavy compute (routing) and IO.

## Incident Response
- Incident channel, roles (commander, comms, ops, scribe).
- First action: stabilise (rate-limit/queue/pause specific regions), then diagnose.
- Post-mortem within 48h; action items tracked.

## Refactoring Policy
- Triggered by hotspots, frequent incidents, or capacity pain.
- Write regression tests first; migrate behind feature flag; remove legacy after bake-in.

## Compliance & Risk
- Pilot with % of users; label beta; explicit guardrails and kill-switch.
- Data retention per policy; access reviews; DPIA for new flows if PII involved.

---
Status: Draft

