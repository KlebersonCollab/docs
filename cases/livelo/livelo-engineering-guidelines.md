# Engineering Guidelines: Livelo AI & Automation Platform

## Basic Information
- **Guideline ID**: EG-LIV-001
- **Project Name**: Livelo AI Automation Stack
- **Version**: 1.0
- **Creation Date**: 2025-10-30
- **Last Update**: 2025-10-30
- **Author**: GPT-5 Codex (based on Livelo leadership insights)
- **Approved by**: *Pending AI Board validation*

## Overview

### Purpose
Provide consistent engineering guardrails for squads building AI agents and automations on top of the Livelo platform (Open WebUI + N8N + LiteLLM). The guidelines ensure that experiments remain governable, secure, and scalable while preserving rapid delivery.

### Scope
- Applies to all AI agents, automations, and integrations deployed through N8N or exposed via Open WebUI / Expert Livelo.
- Covers engineers, automation specialists, and semi-technical staff contributing workflows.
- Applies to both sandbox experiments and production-grade agents.

### Applicability
- Mandatory for any workflow promoted from prototype to production.
- Recommended for discovery experiments to avoid rework when scaling.
- Required artefact for AI Board approval and security review.

## Coding Standards

### Naming Conventions
- **Variables**: `lowerCamelCase` in TypeScript/JavaScript nodes, `snake_case` in Python nodes.
- **Functions**: `verbNoun` format (e.g., `calculateQuota`, `sanitize_prompt`).
- **Classes**: `PascalCase` when TypeScript classes are used in custom nodes.
- **Constants**: `UPPER_SNAKE_CASE` for immutable values (API keys, queue names).
- **Files**: descriptive kebab-case (e.g., `agent-budget-monitor.ts`).

### Code Structure
- **Indentation**: 2 spaces for TypeScript/JavaScript, 4 spaces for Python.
- **Line Length**: maximum 110 characters.
- **Organisation**: group N8N custom nodes under `src/n8n/nodes/<domain>` with shared utilities inside `src/shared`.

### Comments and Documentation
- **Code Comments**: explain non-obvious business logic, model selection criteria, or security-sensitive steps.
- **Function Docs**: include purpose, inputs, outputs, and error handling (JSDoc or Python docstring).
- **README**: each workflow repository requires a README outlining trigger, dependencies, runbook, and rollback instructions.

## Architecture & Design

### Architectural Principles
- **Guardrail First**: every workflow must define budget, access scope, and escalation plan before activation.
- **Observability by Default**: include tracing and token logging from the first iteration.
- **Decouple Experimentation**: prototypes remain in sandbox projects and must pass AI Board review before entering production.

### Design Patterns
- **Orchestrator Pattern**: use N8N to coordinate API calls, branching, and retries. Avoid embedding long business logic in single nodes.
- **Model Adapter Pattern**: route prompts via LiteLLM adapters with standard request/response envelopes.
- **Audit Trail Pattern**: store workflow metadata (inputs, outputs, model, token usage) for traceability and compliance.

### Project Structure
```
project/
├── docs/
│   ├── architecture/
│   └── runbooks/
├── src/
│   ├── n8n/
│   ├── workers/
│   ├── shared/
│   └── tests/
├── helm/
├── .github/
└── README.md
```

## Development Best Practices

### Version Control
- **Branching**: GitFlow-light (feature branches, `develop`, `main`).
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`) with reference to Jira/Clubhouse ticket.
- **Tags**: release tags for production workflow versions (e.g., `workflow-v1.4.0`).

### Testing
- **Unit Tests**: mandatory for custom nodes and helper libraries (≥80% coverage).
- **Integration Tests**: simulate model calls with mocked providers and budget checks.
- **E2E Tests**: smoke tests for core workflows (happy path + failure scenarios).
- **Coverage**: maintain ≥75% overall with focus on decision branches and error handling.

### Performance
- **Optimisation**: cache RAG results for repeated queries; use asynchronous tasks for heavy generation.
- **Profiling**: perform latency sampling weekly for high-traffic agents (Expert Livelo, legal assistant).
- **Monitoring**: collect metrics via Prometheus and Grafana, alert on latency >2s or token spikes >30% daily baseline.

## Security

### Security Principles
- **Authentication**: VPN + SSO for employees; oauth tokens for service accounts.
- **Authorization**: role-based access (Agent Owner, Reviewer, Observer). Minimal privileges on LiteLLM budgets.
- **Validation**: sanitize prompts, strip file metadata, validate JSON outputs before downstream actions.

### Secure Practices
- **Secrets**: store in AWS Secrets Manager or GCP Secret Manager; never hard-code.
- **Tokens**: rotate provider keys quarterly; store hashed references for audit.
- **Sensitive Data**: mask personal data before sending to LLMs; use secure vector stores with encryption at rest.

### Common Vulnerabilities
- **Prompt Injection**: run automated adversarial tests; keep allow/deny lists within workflows.
- **Data Leakage**: enforce redaction pipelines; run DLP scanners on uploaded documents.
- **Supply Chain**: vet open-source nodes; pin versions and run SCA (Software Composition Analysis).

## Code Quality

### Quality Metrics
- **Cyclomatic Complexity**: <10 per function where feasible; refactor complex nodes.
- **Duplication**: reuse shared libraries; duplication threshold <5%.
- **Maintainability Index**: ≥75 in SonarQube for code modules.

### Analysis Tools
- **Linter**: ESLint (TS) and Ruff (Python) with CI enforcement.
- **SonarQube**: run on pull requests; block merges on critical issues.
- **Code Review**: mandatory review from staff engineer or platform steward for production workflows.

### Refactoring
- **When**: triggered by Sonar alerts, AI Board findings, or after three iterations of quick fixes.
- **How**: create tech debt ticket, write regression tests first, refactor incrementally.
- **Tests**: run full pipeline tests after refactor, including rollback scenarios.

## Development Process

### Workflow
1. **Planning**: define problem, budget quota, success KPIs; align with AI Board backlog.
2. **Development**: build in sandbox, follow branching, document dependencies.
3. **Testing**: execute automated suites, dry-run in staging with synthetic data.
4. **Deploy**: GitOps promotion via Helm; attach runbooks and rollback plan.

### Code Review
- **Criteria**: adherence to guidelines, guardrails configured, tests passing, observability hooks present.
- **Process**: reviewer clones branch, runs lint/tests, validates risk assessment.
- **Responsibilities**: author prepares documentation; reviewer validates compliance; platform steward signs off.

### Deployment
- **Environments**: sandbox ➜ staging ➜ production (isolated account).
- **Pipeline**: CI (lint/tests) → CD (GitOps ArgoCD/Flux) with manual gates.
- **Rollback**: maintain previous Helm chart version + snapshot of LiteLLM budgets; run smoke test post-rollback.

## Tools & Technologies

### Mandatory Tools
- **IDE**: VS Code with platform extension pack.
- **Version Control**: GitHub Enterprise.
- **CI/CD**: GitHub Actions + ArgoCD.

### Recommended Tools
- **Debugging**: VS Code Remote Containers, kubectl port-forward for N8N pods.
- **Profiling**: Jaeger tracing, OpenTelemetry collectors.
- **Monitoring**: Grafana dashboards per agent.

### Configurations
- **Editor**: enforce `.editorconfig` (spaces, encoding, newline at EOF).
- **Git**: enable commit signing, pre-commit hooks for linting.
- **CI/CD**: secrets stored in encrypted vaults, environment-specific variables via sealed secrets.

## Documentation

### Technical Documentation
- **API**: describe triggers, inputs, outputs, and rate limits in Markdown; include sample payloads.
- **Architecture**: update high-level and detailed diagrams when adding components.
- **Deploy**: maintain runbooks with health checks, rollback steps, and escalation contacts.

### Code Documentation
- **README**: include overview, architecture diagram, prerequisites, deployment instructions.
- **Comments**: highlight business rules and external dependencies within nodes.
- **Changelog**: track releases with date, author, summary, and risk level.

### Process Documentation
- **Onboarding**: provide quick start guide plus curated learning path for N8N and prompt engineering.
- **Troubleshooting**: maintain KB articles for common failure modes (budget exhausted, model timeout, prompt injection alert).
- **Incidents**: document root cause, mitigation, preventive actions after each incident.

## Observability & Monitoring

### Metrics
- **Performance**: latency, success rate, queue length, token usage per agent.
- **Errors**: workflow failures, provider API errors, budget denials.
- **Usage**: daily active users, prompt counts, automation throughput.

### Logs
- **Structure**: JSON logs with correlation IDs, model name, workflow version.
- **Levels**: `debug`, `info`, `warn`, `error`, `critical` with consistent semantics.
- **Retention**: 90 days online, 12 months cold storage for compliance.

### Alerts
- **Configuration**: Prometheus Alertmanager with thresholds agreed per agent criticality.
- **Escalation**: first on-call (platform engineer) → secondary (staff engineer) → AI Board if systemic.
- **Response**: follow runbook; update status channel every 30 minutes until resolution.

## Incidents & Troubleshooting

### Incident Process
1. **Detection**: automated alerts or user reports via helpdesk.
2. **Response**: acknowledge within 15 minutes; evaluate blast radius.
3. **Resolution**: implement fix or rollback; validate budget balances.
4. **Post-mortem**: complete template within 48 hours; share with AI Board.

### Troubleshooting
- **Debugging**: replay workflow with synthetic inputs; inspect queue states and model responses.
- **Logs**: search by correlation ID; review LiteLLM quota responses.
- **Metrics**: correlate token spikes with user adoption or model drift.

### Communication
- **Status**: post updates in #livelo-ai-operations channel; escalate to executives for P1 incidents.
- **Updates**: every 30 minutes for critical incidents, hourly for P2, daily summary for P3.
- **Stakeholders**: notify security, compliance, and affected product leads.

## Training & Development

### Onboarding
- **New Developers**: complete N8N academy modules, security training, and sandbox exercise.
- **Documentation**: deliver onboarding playbook + quick reference guides.
- **Mentoring**: assign staff engineer mentor for first two sprints.

### Continuous Development
- **Trainings**: monthly sessions on prompt engineering, cost optimisation, and threat modelling.
- **Certifications**: encourage AWS/GCP AI certifications; track completions.
- **Conferences**: share learnings from industry events (e.g., re:Invent, Google Cloud Next).

### Knowledge Management
- **Sharing**: bi-weekly community of practice; record sessions.
- **Documentation**: centralise assets in Confluence + Docs repository.
- **Review**: quarterly review of key workflows and guardrails.

## Compliance & Audit

### Compliance Requirements
- **LGPD**: classify data before ingestion; record legal basis for personal data usage.
- **SOX**: maintain evidence of change approvals and cost controls.
- **ISO 27001**: enforce access reviews and incident response compliance.

### Audit
- **Process**: maintain audit trail of workflow deployments and LiteLLM consumptions.
- **Documentation**: archive AI Board approvals, risk assessments, and post-mortems.
- **Evidence**: export budget logs, access reviews, and security scans quarterly.

### Security Approval
- **Policies**: adhere to corporate security policies; update risk register per workflow.
- **Training**: annual security refresh mandatory for all contributors.
- **Incidents**: report potential data leakage to security within 24 hours.

## Approvals

### Technical Approval
- **Name**: *To be assigned* (Platform Staff Engineer)
- **Date**: *Pending*
- **Notes**: Awaiting formal validation.

### Architecture Approval
- **Name**: *To be assigned* (Head of Architecture)
- **Date**: *Pending*
- **Notes**: To be reviewed in next AI Board session.

### Security Approval
- **Name**: *To be assigned* (Security Lead)
- **Date**: *Pending*
- **Notes**: Requires threat modelling report.

## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/livelo-engineering-guidelines.pt-br.md)

---

**Reviewed by**: *Pending*
**Status**: Draft


