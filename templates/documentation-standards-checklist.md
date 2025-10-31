# Documentation Standards Checklist

## 📋 Overview

This checklist ensures all new documentation follows project standards, including template conformance and bilingual cross-linking (EN/PT-BR).

## ✅ Pre-Creation Checklist

### 1. Template Selection
- [ ] Identify the document type (HLA, Use Case, ADR, Data Governance, Engineering Guidelines)
- [ ] Locate the corresponding template in `docs/templates/`
- [ ] Review the template structure before writing
- [ ] Confirm the document follows template sections

### 2. Language Policy
- [ ] Determine if the document needs both EN and PT-BR versions
- [ ] Create EN version first (root `cases/<case-name>/`)
- [ ] Create PT-BR version in `cases/<case-name>/pt-br/`
- [ ] Mirror structure between EN and PT-BR versions

### 3. Cross-Links Setup
- [ ] Add "Language Versions" section at the end of EN document
- [ ] Add header link to EN version at the top of PT-BR document
- [ ] Use relative paths: `./pt-br/document-name.pt-br.md` (EN → PT-BR)
- [ ] Use relative paths: `../document-name.md` (PT-BR → EN)

## 📝 During Creation Checklist

### 4. Template Conformance
- [ ] Include all required sections from template
- [ ] Use same heading levels as template
- [ ] Follow template naming conventions
- [ ] Include metadata (ID, Version, Date, Author)

### 5. Section Requirements

#### High-Level Architecture
- [ ] Overview/Visão Geral
- [ ] Architectural Objectives/Objetivos Arquiteturais
- [ ] Architecture Diagram/Diagrama
- [ ] Main Components/Componentes Principais

#### Use Case
- [ ] Basic Information/Informações Básicas
- [ ] Actors/Atores
- [ ] Preconditions/Pré-condições
- [ ] Flow/Fluxo (Main Flow)
- [ ] Alternate Flows/Fluxos Alternativos
- [ ] Exception Flows/Fluxos de Exceção

#### Data Governance
- [ ] Basic Information/Informações Básicas
- [ ] Data Classification/Classificação de Dados
- [ ] Data Policies/Políticas de Dados

#### Engineering Guidelines
- [ ] Basic Information/Informações Básicas
- [ ] Code Quality/Qualidade
- [ ] Testing/Testes

#### ADR
- [ ] Status
- [ ] Context
- [ ] Decision/Decisão
- [ ] Consequences/Consequências

### 6. Links and References
- [ ] Use relative paths for internal links
- [ ] Verify all links point to existing files
- [ ] Avoid absolute paths or external URLs when internal docs exist
- [ ] Test links before committing

### 7. Diagram Standards
- [ ] Use Mermaid for architecture diagrams
- [ ] Include diagram descriptions
- [ ] Ensure diagrams render correctly in markdown viewers
- [ ] Keep diagrams updated with document changes

## 🔍 Post-Creation Checklist

### 8. Cross-Link Verification
- [ ] EN document has link to PT-BR version
- [ ] PT-BR document has link to EN version
- [ ] Both links use correct relative paths
- [ ] Links are tested and working

### 9. Template Validation
- [ ] Run validation script: `python3 scripts/validar-template-conformance.py`
- [ ] Confirm document appears as "Conforme" in validation output
- [ ] Fix any missing sections identified by validator
- [ ] Re-run validation until 100% conformant

### 10. Link Validation
- [ ] Run link checker: `python3 scripts/verificar-links-reais.py`
- [ ] Fix any broken links reported
- [ ] Verify no new broken links introduced
- [ ] Update navigation indices if needed

### 11. Navigation Updates
- [ ] Add document to relevant README.md
- [ ] Update `docs/NAVIGATION.md` if it's a major document
- [ ] Update case README.md if applicable
- [ ] Ensure discoverability from main indices

## 📚 Quick Reference

### Cross-Link Format (EN Document)
```markdown
## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/document-name.pt-br.md)

---
```
*Note: Replace `document-name` with actual document name*

### Cross-Link Format (PT-BR Document)
```markdown
# Document Title (PT-BR)

> **Versão em Inglês**: [English Version](../document-name.md)

---
```
*Note: Replace `document-name` with actual document name*

### Required Sections by Type

| Document Type | Required Sections |
|--------------|------------------|
| **High-Level Architecture** | Overview, Architectural Objectives, Architecture Diagram, Main Components |
| **Use Case** | Basic Information, Actors, Preconditions, Flow, Alternate Flows, Exception Flows |
| **Data Governance** | Basic Information, Data Classification, Data Policies |
| **Engineering Guidelines** | Basic Information, Code Quality, Testing |
| **ADR** | Status, Context, Decision, Consequences |

## 🛠️ Tools

### Validation Commands
```bash
# Validate template conformance
cd docs && python3 scripts/validar-template-conformance.py

# Check for broken links
cd docs && python3 scripts/verificar-links-reais.py
```

### Template Locations
- High-Level Architecture: `docs/templates/high-level-architecture-template.md`
- Use Case: `docs/templates/use-case-template.md`
- Data Governance: `docs/templates/data-governance-template.md`
- Engineering Guidelines: `docs/templates/engineering-guidelines-template.md`
- ADR: `docs/templates/adr-template.md`

## 📖 Examples

### Example: Creating a New Case Document

1. **Create EN version**:
   ```bash
   docs/cases/new-case/
   ├── new-case-high-level-architecture.md
   └── pt-br/
       └── new-case-high-level-architecture.pt-br.md
   ```

2. **Add cross-links**:
   - EN: Add "Language Versions" section at end
   - PT-BR: Add link to EN at top

3. **Validate**:
   ```bash
   python3 scripts/validar-template-conformance.py
   python3 scripts/verificar-links-reais.py
   ```

4. **Update navigation**:
   - Add to `cases/new-case/README.md`
   - Update main navigation if needed

## ⚠️ Common Mistakes to Avoid

- ❌ Creating EN document without PT-BR version when needed
- ❌ Forgetting cross-links between EN and PT-BR
- ❌ Using absolute paths instead of relative paths
- ❌ Missing required template sections
- ❌ Not validating before committing
- ❌ Using inconsistent heading levels
- ❌ Creating documents outside appropriate directories

## ✅ Quality Gate

Before marking a document as complete, ensure:
1. ✅ Template conformance validated (100% pass rate)
2. ✅ All links verified (0 broken links)
3. ✅ Cross-links added (if bilingual required)
4. ✅ Navigation updated
5. ✅ Document follows naming conventions (kebab-case)

---

**Last Updated**: 2025-10-30  
**Maintainer**: Skynet Docs Team  
**Reference**: OpenSpec Change `docs-audit-standardization`

