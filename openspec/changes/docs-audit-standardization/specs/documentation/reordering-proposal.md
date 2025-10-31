# Reordering & Normalization Proposal

## Goals
- Coherent directory structure, clear separation of domains, consistent case placement, and discoverability via navigation.

## Proposed Moves (No-op until approved)
- Ensure all case documents live under `docs/cases/<case>` with PT-BR under `pt-br/`.
- Group creative-focused docs (estrutura-narrativa, personagens, conflitos, projeto, brainstorm) under a dedicated section (keep under root but referenced from `navigation/`; optionally consider `docs/creative/` in future phase).
- Consolidate architecture-related scattered docs under `docs/architecture/` (keep design patterns and scalability where they are; fix cross-links).

## Navigation Updates
- Update `docs/navigation/*` to surface: Cases (Livelo/iFood), Architecture, Templates, Processes, Creative (macro link), Governance, Testing, Monitoring.
- Ensure `README.md`, `GUIA_CENTRAL.md`, `INDICE_ORGANIZACIONAL.md`, `MAPA_NAVEGACAO.md` reflect final structure and provide cross-links.

## Rationale
- Reduces link breakage risk, improves discoverability, and aligns with global standards.

## Execution Plan
1. Confirm target locations for each misfiled item.
2. Move files and update links (batch per domain to minimize churn).
3. Update navigation and regenerate link report.

