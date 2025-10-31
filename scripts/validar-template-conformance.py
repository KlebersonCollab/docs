#!/usr/bin/env python3
"""
Script para validar conformidade de documentos com templates
Conforme requisito do OpenSpec: Template Conformance
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

DOCS_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = DOCS_ROOT / "templates"
CASES_DIR = DOCS_ROOT / "cases"

# Mapeamento de tipos de documentos para templates
TEMPLATE_MAPPING = {
    "high-level-architecture": "high-level-architecture-template.md",
    "data-governance": "data-governance-template.md",
    "engineering-guidelines": "engineering-guidelines-template.md",
    "use-case": "use-case-template.md",
    "adr": "adr-template.md",
}

# Seções obrigatórias para cada tipo de template
REQUIRED_SECTIONS = {
    "high-level-architecture": [
        r"#.*[Hh]igh.*[Ll]evel.*[Aa]rchitecture|#.*[Aa]rquitetura.*[Aa]lto.*[Nn]ível",
        r"##?\s*[Oo]verview|##?\s*[Vv]isão\s*[Gg]eral",
        r"##?\s*[Aa]rchitectural\s*[Oo]bjectives|##?\s*[Oo]bjetivos\s*[Aa]rquiteturais",
        r"##?\s*[Aa]rchitecture\s*[Dd]iagram|##?\s*[Dd]iagrama",
    ],
    "data-governance": [
        r"##?\s*.*[Bb]asic\s*[Ii]nformation|##?\s*.*[Ii]nformações\s*[Bb]ásicas",
        r"##?\s*.*[Dd]ata\s*[Cc]lassification|##?\s*.*[Cc]lassificação",
        r"##?\s*.*[Dd]ata\s*[Pp]olicies|##?\s*.*[Pp]olíticas",
    ],
    "engineering-guidelines": [
        r"##?\s*[Bb]asic\s*[Ii]nformation|##?\s*[Ii]nformações\s*[Bb]ásicas",
        r"##?\s*[Cc]ode\s*[Qq]uality|##?\s*[Qq]ualidade",
        r"##?\s*[Tt]esting|##?\s*[Tt]estes",
    ],
    "use-case": [
        r"##?\s*[Bb]asic\s*[Ii]nformation|##?\s*[Ii]nformações\s*[Bb]ásicas",
        r"##?\s*[Aa]ctors|##?\s*[Aa]tores",
        r"##?\s*[Pp]reconditions|##?\s*[Pp]ré.*[Cc]ondições",
        r"##?\s*[Ff]low|##?\s*[Ff]luxo",
    ],
    "adr": [
        r"##?\s*[Ss]tatus",
        r"##?\s*[Cc]ontext",
        r"##?\s*[Dd]ecision|##?\s*[Dd]ecisão",
        r"##?\s*[Cc]onsequences|##?\s*[Cc]onsequências",
    ],
}

def detect_document_type(file_path: Path) -> str:
    """Detecta o tipo de documento pelo nome do arquivo"""
    name_lower = file_path.name.lower()
    
    if "high-level-architecture" in name_lower or "arquitetura" in name_lower:
        return "high-level-architecture"
    elif "data-governance" in name_lower or "governança" in name_lower:
        return "data-governance"
    elif "engineering-guidelines" in name_lower or "diretrizes" in name_lower:
        return "engineering-guidelines"
    elif "uc-" in name_lower or "use-case" in name_lower or "caso-de-uso" in name_lower:
        return "use-case"
    elif "adr-" in name_lower:
        return "adr"
    
    return "unknown"

def validate_sections(content: str, doc_type: str) -> Tuple[bool, List[str]]:
    """Valida se o documento contém as seções obrigatórias"""
    if doc_type == "unknown":
        return True, []  # Skip validation for unknown types
    
    missing_sections = []
    required = REQUIRED_SECTIONS.get(doc_type, [])
    
    for pattern in required:
        if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            missing_sections.append(pattern)
    
    return len(missing_sections) == 0, missing_sections

def main():
    """Valida conformidade de documentos dos casos com templates"""
    print("🔍 Validando conformidade de templates...\n")
    
    results = []
    
    # Processar casos
    for case_dir in CASES_DIR.iterdir():
        if not case_dir.is_dir() or case_dir.name.startswith("."):
            continue
        
        print(f"📁 Processando caso: {case_dir.name}")
        
        # Processar arquivos .md (exceto README e pt-br)
        for md_file in case_dir.rglob("*.md"):
            if "README" in md_file.name or "pt-br" in str(md_file):
                continue
            
            doc_type = detect_document_type(md_file)
            if doc_type == "unknown":
                continue
            
            try:
                content = md_file.read_text(encoding="utf-8")
                is_valid, missing = validate_sections(content, doc_type)
                
                relative_path = md_file.relative_to(DOCS_ROOT)
                results.append({
                    "file": str(relative_path),
                    "type": doc_type,
                    "valid": is_valid,
                    "missing_sections": missing,
                })
                
                if is_valid:
                    print(f"  ✅ {md_file.name} - Conforme")
                else:
                    print(f"  ⚠️  {md_file.name} - Faltam {len(missing)} seções")
                    
            except Exception as e:
                print(f"  ❌ {md_file.name} - Erro: {e}")
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DE VALIDAÇÃO")
    print("="*60)
    
    total = len(results)
    valid = sum(1 for r in results if r["valid"])
    invalid = total - valid
    
    print(f"\nTotal de documentos validados: {total}")
    print(f"✅ Conformes: {valid}")
    print(f"⚠️  Não conformes: {invalid}")
    
    if invalid > 0:
        print("\n📋 Documentos não conformes:")
        for r in results:
            if not r["valid"]:
                print(f"\n  📄 {r['file']}")
                print(f"     Tipo: {r['type']}")
                print(f"     Seções faltantes: {len(r['missing_sections'])}")
                for pattern in r['missing_sections']:
                    print(f"       - {pattern}")
    
    print("\n" + "="*60)
    
    return 0 if invalid == 0 else 1

if __name__ == "__main__":
    exit(main())

