# Proposal: Docs Audit & Standardization

## Why
Ensure all documentation and guides are consistent, current, and discoverable, following the project’s governance, templates, and navigation rules. This is a documentation-only effort: no code changes expected.

## Scope
Covers the entire `docs/` tree, including but not limited to:
- Directories: `analises/`, `architecture/`, `bpm-agil/`, `escalabilidade/`, `ferramentas/`, `governance/`, `meetings/`, `monitoring/`, `navigation/`, `principios-desenvolvimento/`, `principios-solid/`, `processes/`, `rules/`, `security/`, `templates/`, `testing/`, `cases/`
- Root files: `ANALISE_FINAL_COMPLETA.md`, `architecture-hai-template.md`, `bancos-dados.md`, `bdd-example.md`, `best-practices`, `brainstorm-processo-criativo.md`, `c4-model-template.md`, `conflitos-template.md`, `criacao-conflitos.md`, `desenvolvimento-personagens.md`, `design-patterns`, `estrutura-narrativa-template.md`, `estrutura-narrativa.md`, `gestao-projetos.md`, `GUIA_CENTRAL.md`, `INDICE_ORGANIZACIONAL.md`, `LICENSE`, `MAPA_NAVEGACAO.md`, `NAVIGATION.md`, `ORGANIZACAO_COMPLETA.md`, `personagens-template.md`, `projeto-template.md`, `README.md`, `recursos-inspiracao.md`, `refinamento-roteiro.md`, `RELATORIO_LINKS_REAIS.md`, `software-criacao.md`

## What Changes
- ADDED organization-wide documentation standards (naming, language, structure, links, diagrams).
- ADDED full inventory and classification across all docs sections (see Scope).
- ADDED link integrity remediation based on `RELATORIO_LINKS_REAIS.md` (fix references, add missing targets, or adjust paths).
- ADDED reordering/normalization proposal to ensure coherent structure (cases under `docs/cases/*`, technical vs. criativo grouping) and apply changes.
- ADDED review and update pass for cases (Livelo, iFood) in EN and PT-BR with cross-links.
- ADDED governance, architecture, testing/observability documentation consolidation.
- UPDATED navigation and indices across docs.

## Deliverables
- Global Standards document (embedded in OpenSpec specs) and applied across repository.
- Updated and validated links (no dead links) with refreshed report.
- Reordered documentation where needed (with rationale) and updated navigation.
- Standardized case folders (EN/PT-BR) with cross-links.
- Conformance report against templates for key documents (HLA, governance, use case, ADR).

## Impact
- Affected areas: `docs/`, `docs/cases/*`, `docs/navigation/`, `docs/templates/`.
- Breaking changes: None (documentation-only).
- Dependencies: OpenSpec compliance (scenarios format), existing templates.

## Metrics of Success
- 100% documents conform to templates/standards.
- Navigation index updated and valid.
- Cross-links verified (no dead links).
- `RELATORIO_LINKS_REAIS.md` re-run shows 0 broken links.

## Timeline
- Phase 1 (Inventory/Standards/Plan): 3 days
- Phase 2 (Domain Passes & Remediation): 4 days
- Phase 3 (Navigation/Validation/Close-out): 2 days
