# Inventory – Docs Audit

## Top-level (docs/)
- README.md
- AGENTS.md (+ backup)
- NAVIGATION.md / MAPA_NAVEGACAO.md / INDICE_ORGANIZACIONAL.md / GUIA_CENTRAL.md
- RELATORIO_LINKS_REAIS.md
- Folders: architecture/, governance/, templates/, processes/, testing/, monitoring/, security/, navigation/, meetings/, cases/, principios-*, escalabilidade/, analises/, bpm-agil/, ferramentas/, scripts/

## Cases (docs/cases/)
- livelo/ (EN + pt-br/) – OK
- ifood/ (EN + pt-br/) – OK

## Architecture (docs/architecture/)
- c4-model-template.md
- architecture-hai-template.md
- design-patterns references (mixed locations)

## Governance (docs/governance/)
- (To scan for alignment with data/security templates)

## Templates (docs/templates/)
- HLA, governance, ADR, use case, processes, testing, etc. – authoritative

## Navigation (docs/navigation/)
- (To align with cases and core areas)

## Gaps / Candidates for Standardization
- Dual-language policy: ensure EN at root, PT-BR mirrors under `pt-br/`
- Cross-linking between EN/PT-BR in cases (add links in READMEs and headers)
- Consistent diagram usage (Mermaid/C4) across architecture docs
- Governance docs to align with data/security/process templates
- Navigation indices to list both cases and core domains
- Validate links in RELATORIO_LINKS_REAIS.md and update

## Next Actions
- Define global standards doc (naming, language, structure, links, diagrams)
- Run conformance pass on cases (Livelo/iFood)
- Governance pass (data/security/process)
- Architecture pass (HLA + diagrams)
- Testing/observability pass (KPIs/SLOs)
- Update navigation indices and READMEs
