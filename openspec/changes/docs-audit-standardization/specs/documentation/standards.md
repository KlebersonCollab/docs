# Global Documentation Standards

## Naming & Structure
- Filenames in kebab-case, `.md` extension.
- Place documents under the most specific domain folder (e.g., `docs/architecture/...`, `docs/templates/...`, `docs/processes/...`, `docs/cases/<case>`).
- Each folder has a `README.md` with local navigation.

## Language Policy
- Root docs in EN by default.
- PT-BR localizations mirror structure under `pt-br/` subfolder.
- Cross-link EN ⇄ PT-BR in README and document headers where applicable.

## Links & Diagrams
- Use relative links; verify targets.
- Prefer Mermaid/C4 for architecture diagrams.
- No absolute local paths; avoid bare URLs without context.

## Templates & Conformance
- Use templates from `docs/templates/` for HLA, governance, use case, ADR, processes, testing.
- Deviations must be justified in a short note at the end of the document.

## Navigation
- Update `docs/navigation` and section READMEs when adding/moving docs.
- Top-level indices must list cases and core domains.

## Versioning & Metadata
- Include header with: title (H1), document type/category, version, date, author, maintainer, next review.
- Record last update and next review at the bottom.

## Creative vs Technical
- Keep creative content grouped and referenced from navigation; avoid mixing into technical domains.
- Use clear labels to distinguish creative guides from technical specs.

