## ADDED Requirements

### Requirement: Global Documentation Standards
Define and enforce global documentation standards covering naming, language, structure, links, and diagrams.

#### Scenario: Naming and file structure
- **WHEN** authors create or update docs
- **THEN** files follow kebab-case names and live in the appropriate directories (e.g., `docs/cases/<case>`)
- **AND** README files outline local navigation

#### Scenario: Language and dual-version policy
- **WHEN** content is Markdown in root docs
- **THEN** English is used
- **AND** PT-BR versions reside under `pt-br/` with mirrored structure

#### Scenario: Links and code references
- **WHEN** adding links
- **THEN** use relative links and verify targets
- **AND** use Mermaid/C4 for diagrams where applicable

#### Scenario: Cross-references for cases
- **WHEN** a case has EN and PT-BR versions
- **THEN** include cross-links in README and file headers
- **AND** ensure both versions are discoverable from navigation indices

### Requirement: Link Integrity Remediation
Fix all broken links reported in `RELATORIO_LINKS_REAIS.md` and ensure future stability.

#### Scenario: Link report remediation
- **WHEN** a broken link is reported
- **THEN** update the target path or adjust the reference to a valid location
- **AND** if a target document is missing, create it or update the source to a valid alternative
- **AND** rerun the link report to confirm zero broken links

### Requirement: Reordering and Normalization
Ensure the documentation tree is coherent and predictable.

#### Scenario: Reordering misfiled documents
- **WHEN** a document is identified in an inconsistent location
- **THEN** move it to the appropriate domain folder (e.g., cases → `docs/cases`, creative vs técnico separation)
- **AND** update navigation indices and references accordingly

### Requirement: Navigation and Indices
Ensure discoverability across docs via updated indices and READMEs.

#### Scenario: Navigation index updated
- **WHEN** new docs are added or reorganized
- **THEN** `docs/navigation` and relevant `README.md` files are updated
- **AND** top-level index lists all cases and core areas

### Requirement: Template Conformance
Ensure documents align to repository templates.

#### Scenario: Template adherence checked
- **WHEN** reviewing a doc
- **THEN** it is validated against the matching template (e.g., HLA, governance, use case, ADR)
- **AND** deviations are corrected or justified
