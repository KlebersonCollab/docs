# Use Case: AI Pull Request Reviewer

## Basic Information
- **Use Case ID**: UC-LIV-001
- **Name**: AI-augmented Pull Request Quality Review
- **Version**: 1.0
- **Creation Date**: 2025-10-30
- **Last Update**: 2025-10-30
- **Author**: GPT-5 Codex (based on Livelo engineering interview)

## Description
Automate pull request reviews in Git repositories by invoking an AI agent through N8N that analyses diffs, enforces coding standards, identifies security issues, and suggests corrections before human approval. The agent reduces review lead time and ensures guardrails for workflows built on the Livelo AI platform.

## Actors

### Primary Actors
- **Developer**: Submits pull requests for review and consumes AI feedback.
- **AI Reviewer Agent**: N8N workflow invoking LiteLLM with contextual prompts and repository knowledge.

### Secondary Actors
- **Reviewer (Human)**: Validates AI findings and approves or rejects pull requests.
- **Platform Steward**: Maintains guardrails, monitors agent performance, and updates prompts.

## Preconditions
- Repository configured with N8N webhook and GitHub/GitLab integration.
- LiteLLM budget available for the responsible squad.
- Coding standards and security policies documented in repository.

## Postconditions
- Pull request annotated with AI findings, severity, and suggested resolutions.
- Budget deduction recorded in LiteLLM ledger.
- Observability metrics updated (latency, token usage, accuracy feedback).

## Main Flow

### Step 1
**Actor Action**: Developer opens or updates a pull request.
**System Response**: Git platform triggers webhook to N8N with PR metadata and diff.

### Step 2
**Actor Action**: N8N orchestrator enriches context (coding standards, previous review history).
**System Response**: Workflow sanitises payload, checks LiteLLM quota, and prepares prompt.

### Step 3
**Actor Action**: AI Reviewer Agent sends prompt to selected LLM (e.g., Claude via Bedrock or Gemini via Vertex).
**System Response**: Model analyses diff, returns structured JSON with findings and confidence levels.

### Step 4
**Actor Action**: Workflow validates JSON schema, maps findings to repository guidelines.
**System Response**: Comments posted on pull request; summary appended to PR description.

### Step 5
**Actor Action**: Developer addresses issues and updates PR.
**System Response**: Workflow re-runs on update until findings are resolved or waived by human reviewer.

## Alternate Flows

### Alternate Flow A: Budget Exhausted
**Condition**: LiteLLM quota check fails.
**Steps**:
1. Workflow posts comment indicating budget exhaustion and assigns Agent Owner.
2. Finance alert triggered for quota top-up.
3. Human reviewer proceeds manually while top-up is processed.

### Alternate Flow B: Low Confidence Response
**Condition**: LLM confidence score < threshold (e.g., 0.6).
**Steps**:
1. Workflow requests re-evaluation using fallback model.
2. If still low, it flags reviewer with `needs-human-analysis` label.
3. Reviewer performs manual review and records outcome for feedback loop.

## Exception Flows

### Exception A: Prompt Injection Detected
**Condition**: Static analysis finds malicious instructions in diff or comments.
**Handling**:
1. Abort workflow and label PR as `security-alert`.
2. Notify security steward and platform steward.
3. Require manual security review before proceeding.

### Exception B: Schema Validation Failure
**Condition**: Model returns output that does not match expected schema.
**Handling**:
1. Log incident with payload snapshot (sanitised).
2. Retry once with stricter prompt.
3. If failure persists, escalate to human reviewer and record for prompt tuning.

## Business Rules

### Rule 1
**Description**: All production-bound repositories must enable AI review before human approval.
**Application**: Enforced via Git branch protection rules.

### Rule 2
**Description**: AI findings tagged as `critical` require human acknowledgement even after fix.
**Application**: Pull request cannot merge until reviewer confirms remediation.

### Rule 3
**Description**: LiteLLM budget threshold alerts trigger within 20% of remaining credits.
**Application**: Ensures squads top-up budgets before automated reviews halt.

## Prototypes & Mockups

### Main Screen
- PR interface displays AI summary comment plus inline annotations.
- Additional status badge indicates `AI Review: Passed/Changes Requested`.

### Secondary Screens
- Dashboard showing review counts, average turnaround time, token consumption (Grafana panel).
- LiteLLM quota view for squad owners.

## Non-functional Requirements

### Performance
- Response time target: <60 seconds per review for small/medium diffs.
- Concurrency: handle at least 20 simultaneous PR reviews without backlog.

### Security
- Run prompt sanitisation and diff escaping before sending to LLM.
- Restrict workflow to repository scope; deny access to secrets in diff.

### Usability
- Provide actionable comments with code snippets and recommended fixes.
- Allow developers to give thumbs-up/down feedback to improve prompts.

## Dependencies

### Related Use Cases
- [UC-LIV-002 – Planned] AI legal assistant for document drafting (shares budget module).
- [UC-LIV-003 – Planned] Automation COE workflows (shares N8N governance).

### System Modules
- **N8N Workflow**: orchestrates review logic.
- **LiteLLM Budget Service**: validates quota and logs consumption.
- **Observability Stack**: collects metrics and traces.

## Test Scenarios

### Test Scenario 1
**Objective**: Validate AI correctly flags insecure code.
**Input Data**: PR introducing SQL concatenation.
**Expected Result**: Comment identifies SQL injection risk with remediation advice.

### Test Scenario 2
**Objective**: Ensure workflow handles large diffs within timeout.
**Input Data**: PR modifying 500+ lines across multiple files.
**Expected Result**: Review completes within SLA or gracefully flags for human review.

## Implementation Notes

### Technical Considerations
- Use streaming responses when supported to reduce perceived latency.
- Store anonymised prompt/response pairs for continuous improvement.
- Provide configuration file per repository for rule weights and thresholds.

### Identified Risks
- **Risk**: False positives causing developer fatigue → Mitigation: collect feedback and adjust prompts weekly.
- **Risk**: Model drift reduces accuracy → Mitigation: schedule monthly benchmarking, fallback to alternative model when necessary.

### Estimates
- **Complexity**: Medium.
- **Effort**: ~3 engineer-weeks (initial implementation + staging hardening).
- **Priority**: High (directly impacts engineering productivity).

---

**Reviewed by**: *Pending*
**Approved by**: *Pending*
**Status**: Draft

