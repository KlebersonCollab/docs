# Guide: Creating Bilingual Documentation (EN/PT-BR)

## 🎯 Purpose

This guide provides step-by-step instructions for creating and maintaining bilingual documentation with proper cross-linking between English and Portuguese (Brazil) versions.

## 📐 Structure

### Directory Organization

```
docs/cases/<case-name>/
├── document-name.md              # English version
├── pt-br/
│   └── document-name.pt-br.md    # Portuguese (Brazil) version
└── README.md
```

## 🔗 Cross-Linking Standards

### Standard 1: English Document Format

**Location**: At the end of the English document, before metadata footer.

**Format** (example - replace placeholders):
```markdown
## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/document-name.pt-br.md)

---
[Metadata: Last Update, Status, etc.]
```

**Example** (actual working link):
```markdown
## Language Versions
- **English**: This document
- **Português (Brasil)**: [Versão PT-BR](./pt-br/livelo-high-level-architecture.pt-br.md)

---
**Last Update**: 2025-10-30  
**Source**: Livelo interview on PPT Não Compila podcast.
```

### Standard 2: Portuguese Document Format

**Location**: Immediately after the title, before content begins.

**Format** (example - replace placeholders):
```markdown
# Document Title (PT-BR)

> **Versão em Inglês**: [English Version](../document-name.md)

---

[Content begins here]
```

**Example** (actual working link):
```markdown
# Plataforma de IA da Livelo - Arquitetura de Alto Nível (PT-BR)

> **Versão em Inglês**: [High-Level Architecture](../livelo-high-level-architecture.md)

---

## Visão Geral
[Content continues...]
```

## 📝 Step-by-Step: Creating Bilingual Documents

### Step 1: Create English Version

1. Create the English document in the case directory:
   ```bash
   docs/cases/<case-name>/document-name.md
   ```

2. Write content following the appropriate template

3. Add the "Language Versions" section at the end:
   ```markdown
   ## Language Versions
   - **English**: This document
   - **Português (Brasil)**: [Versão PT-BR](./pt-br/document-name.pt-br.md)
   ```

### Step 2: Create Portuguese Version

1. Create the PT-BR directory if it doesn't exist:
   ```bash
   mkdir -p docs/cases/<case-name>/pt-br
   ```

2. Create the Portuguese document:
   ```bash
   docs/cases/<case-name>/pt-br/document-name.pt-br.md
   ```

3. Add the English link at the top:
   ```markdown
   # Document Title (PT-BR)

   > **Versão em Inglês**: [English Version](../document-name.md)

   ---
   ```

4. Translate content maintaining same structure and heading levels

### Step 3: Verify Cross-Links

1. **From EN document**:
   - Click the PT-BR link
   - Verify it navigates to the correct Portuguese document

2. **From PT-BR document**:
   - Click the EN link
   - Verify it navigates to the correct English document

3. **Run link validation**:
   ```bash
   cd docs && python3 scripts/verificar-links-reais.py
   ```

## 🔍 Link Path Examples

### Correct Paths

#### EN → PT-BR (same directory level)
```markdown
<!-- Example path structure - replace with actual document names -->
<!-- From: docs/cases/livelo/livelo-hla.md -->
<!-- [Versão PT-BR](./pt-br/livelo-hla.pt-br.md) -->
```
*Note: This is an example. Use actual document paths in your files.*

#### PT-BR → EN (parent directory)
```markdown
<!-- Example path structure - replace with actual document names -->
<!-- From: docs/cases/livelo/pt-br/livelo-hla.pt-br.md -->
<!-- [English Version](../livelo-hla.md) -->
```
*Note: This is an example. Use actual document paths in your files.*

### Incorrect Paths (Avoid)

❌ **Absolute paths**:
```markdown
/docs/cases/livelo/pt-br/livelo-hla.pt-br.md
```

❌ **Incorrect relative paths**:
```markdown
pt-br/livelo-hla.pt-br.md  <!-- Missing ./ prefix -->
../livelo-hla.md           <!-- When already in pt-br subdirectory -->
```

## 📋 Checklist for Bilingual Documents

### Content Checklist
- [ ] English version created and complete
- [ ] Portuguese version created and complete
- [ ] Both versions follow same template structure
- [ ] Heading levels match between versions
- [ ] Metadata consistent between versions
- [ ] Content accurately translated

### Cross-Link Checklist
- [ ] EN document has "Language Versions" section
- [ ] PT-BR document has English link at top
- [ ] Links use correct relative paths
- [ ] Links tested and working
- [ ] No broken links reported by validator

### Validation Checklist
- [ ] Template conformance validated (both versions)
- [ ] Link checker passes (0 broken links)
- [ ] Navigation updated (both versions discoverable)

## 🎨 Formatting Standards

### Title Format

**English**:
```markdown
# Livelo AI Platform - High-Level Architecture
```

**Portuguese**:
```markdown
# Plataforma de IA da Livelo - Arquitetura de Alto Nível (PT-BR)
```

Note: Always include "(PT-BR)" suffix in Portuguese titles.

### Section Headings

Maintain same heading levels across both versions:

**English**:
```markdown
## Overview
## Architectural Objectives
### Component 1
```

**Portuguese**:
```markdown
## Visão Geral
## Objetivos Arquiteturais
### Componente 1
```

## 🔄 Updating Existing Documents

### When Updating English Version

1. Make changes to English document
2. Update "Last Update" date in metadata
3. Ensure cross-link to PT-BR is still correct
4. Update Portuguese version to match (if content changed)

### When Updating Portuguese Version

1. Make changes to Portuguese document
2. Update "Última Atualização" date in metadata
3. Ensure cross-link to EN is still correct
4. Verify English version if translation changes reflect source changes

### Maintaining Synchronization

- Keep structure synchronized between versions
- Update metadata dates independently (each version tracks its own updates)
- Maintain cross-links during refactoring
- Run validation after any structural changes

## 📚 Document Types Requiring Bilingual Support

### Always Bilingual
- High-Level Architecture documents
- Case study documentation
- Major project documentation

### Optional Bilingual
- Technical guides (if audience requires)
- ADRs (if team is bilingual)
- Engineering Guidelines (if team is bilingual)

### Typically English Only
- Internal technical documentation
- API references
- Configuration files

## 🛠️ Automation

### Script for Cross-Link Validation

You can create a script to validate all cross-links:

```bash
#!/bin/bash
# validate-cross-links.sh

for en_file in docs/cases/*/*.md; do
  if [[ "$en_file" != *"README.md" ]] && [[ "$en_file" != *"pt-br"* ]]; then
    case_name=$(dirname "$en_file" | xargs basename)
    doc_name=$(basename "$en_file" .md)
    pt_br_file="docs/cases/$case_name/pt-br/${doc_name}.pt-br.md"
    
    if [ -f "$pt_br_file" ]; then
      # Check if EN has link to PT-BR
      if ! grep -q "pt-br/${doc_name}.pt-br.md" "$en_file"; then
        echo "❌ Missing PT-BR link in: $en_file"
      fi
      
      # Check if PT-BR has link to EN
      if ! grep -q "../${doc_name}.md" "$pt_br_file"; then
        echo "❌ Missing EN link in: $pt_br_file"
      fi
    fi
  fi
done
```

## 📖 Examples

### Complete Example: Creating a New Case Document

1. **Structure**:
   ```
   docs/cases/new-case/
   ├── new-case-high-level-architecture.md
   ├── new-case-engineering-guidelines.md
   ├── new-case-data-governance.md
   ├── pt-br/
   │   ├── new-case-high-level-architecture.pt-br.md
   │   ├── new-case-engineering-guidelines.pt-br.md
   │   └── new-case-data-governance.pt-br.md
   └── README.md
   ```

2. **Each EN document ends with** (example - use actual filenames):
   ```markdown
   ## Language Versions
   - **English**: This document
   - **Português (Brasil)**: [Versão PT-BR](./pt-br/new-case-high-level-architecture.pt-br.md)
   
   ---
   Last Update: 2025-10-30
   ```
   *Replace with your actual document filename*

3. **Each PT-BR document starts with** (example - use actual filenames):
   ```markdown
   # New Case - Arquitetura de Alto Nível (PT-BR)
   
   > **Versão em Inglês**: [High-Level Architecture](../new-case-high-level-architecture.md)
   
   ---
   
   ## Visão Geral
   ```
   *Replace with your actual document filename*

## ⚠️ Common Pitfalls

1. **Incorrect Paths**: Always use relative paths, test them
2. **Missing Links**: Don't forget cross-links in either direction
3. **Structure Mismatch**: Keep heading levels and structure synchronized
4. **Outdated Links**: Update links when files are renamed or moved
5. **Case Sensitivity**: Be consistent with file naming (kebab-case)

## ✅ Quality Assurance

Before finalizing bilingual documents:

1. ✅ Both versions exist and are complete
2. ✅ Cross-links work in both directions
3. ✅ Structure matches between versions
4. ✅ Links validated (no broken links)
5. ✅ Navigation updated (both versions discoverable)
6. ✅ Metadata accurate and consistent

---

**Last Updated**: 2025-10-30  
**Maintainer**: Skynet Docs Team  
**Related**: [Documentation Standards Checklist](./documentation-standards-checklist.md)

