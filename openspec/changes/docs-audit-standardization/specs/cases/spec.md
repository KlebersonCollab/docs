## ADDED Requirements

### Requirement: Case Documentation Standardization (Livelo and iFood)
Standardize case documentation in EN and PT-BR across structure, content, and cross-links.

#### Scenario: Case structure alignment
- **WHEN** reviewing case folders
- **THEN** ensure presence of README, HLA, guidelines, governance, use case(s), and ADRs
- **AND** ensure PT-BR mirrors EN under `pt-br/`

#### Scenario: Cross-linking between EN and PT-BR
- **WHEN** a doc has a localized counterpart
- **THEN** include links to both versions in the README and per-file headers
- **AND** verify that links resolve

#### Scenario: Diagram and template checks
- **WHEN** diagrams exist
- **THEN** ensure Mermaid/C4 is used and consistent
- **AND** documents follow the corresponding templates
