# Tasks: Docs Audit & Standardization

## Phase 1: Inventory & Standards
- [x] 1.1 Full inventory and classification across `docs/` (all subfolders and root files):
      - Folders: `analises/`, `architecture/`, `bpm-agil/`, `escalabilidade/`, `ferramentas/`, `governance/`, `meetings/`, `monitoring/`, `navigation/`, `principios-desenvolvimento/`, `principios-solid/`, `processes/`, `rules/`, `security/`, `templates/`, `testing/`, `cases/`
      - Root files: `ANALISE_FINAL_COMPLETA.md`, `architecture-hai-template.md`, `bancos-dados.md`, `bdd-example.md`, `best-practices`, `brainstorm-processo-criativo.md`, `c4-model-template.md`, `conflitos-template.md`, `criacao-conflitos.md`, `desenvolvimento-personagens.md`, `design-patterns`, `estrutura-narrativa-template.md`, `estrutura-narrativa.md`, `gestao-projetos.md`, `GUIA_CENTRAL.md`, `INDICE_ORGANIZACIONAL.md`, `LICENSE`, `MAPA_NAVEGACAO.md`, `NAVIGATION.md`, `ORGANIZACAO_COMPLETA.md`, `personagens-template.md`, `projeto-template.md`, `README.md`, `recursos-inspiracao.md`, `refinamento-roteiro.md`, `RELATORIO_LINKS_REAIS.md`, `software-criacao.md`
- [x] 1.2 Define global standards (naming, language policy EN root / PT-BR in `pt-br/`, structure, relative links, Mermaid/C4 usage)
- [x] 1.3 Link integrity pass plan: use `RELATORIO_LINKS_REAIS.md` to queue fixes (update paths, add missing targets, or adjust references)
- [x] 1.4 Reordering proposal: propose normalized tree (move misplaced docs to correct domains, split creative vs técnico, ensure cases under `docs/cases/*`)

## Phase 2: Domain Passes
- [x] 2.1 Cases – Livelo (EN/PT-BR) standardization and cross-links
- [x] 2.2 Cases – iFood (EN/PT-BR) standardization and cross-links
- [x] 2.3 Governance docs alignment (data/security/process)
- [x] 2.4 Architecture docs pass (HLA, mermaid/C4 consistency; consolidate patterns under `architecture/`)
- [x] 2.5 Testing/Observability docs pass (KPIs, SLOs; align with `templates/testing/*`)
- [x] 2.6 Creative docs grouping (estrutura narrativa, personagens, conflitos, projeto): confirm dedicated section and link from navigation indices

## Phase 3: Navigation & Validation
- [x] 3.1 Update navigation indices and READMEs to reflect final structure
- [x] 3.2 Cross-link verification (no dead links) and regenerate `RELATORIO_LINKS_REAIS.md`
- [x] 3.3 OpenSpec validation (scenarios format) and close-out
