#!/usr/bin/env python3
"""
Script para verificar links quebrados ignorando arquivos de relatório.
"""

import os
import re
from datetime import datetime

def find_markdown_files(root_dir):
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))
    return markdown_files

def is_report_file(filepath):
    """Verifica se o arquivo é um relatório que deve ser ignorado."""
    filename = os.path.basename(filepath)
    report_files = {
        'RELATORIO_LINKS_QUEBRADOS.md',
        'SUGESTOES_CORRECAO_LINKS.md',
        'RESUMO_CORRECAO_LINKS.md',
        'RESUMO_FINAL_CORRECAO_LINKS.md',
        'RESUMO_FINAL_CORRECAO_LINKS_COMPLETO.md'
    }
    
    # Ignora arquivos que contêm "RELATORIO" ou "RESUMO" ou "SUGESTOES"
    if any(keyword in filename.upper() for keyword in ['RELATORIO', 'RESUMO', 'SUGESTOES']):
        return True
    
    return filename in report_files

def check_links_in_file(filepath, root_dir):
    broken_links = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex para encontrar links Markdown: [texto do link](caminho/do/arquivo.md)
    # e links de imagem: ![alt text](caminho/da/imagem.png)
    # e links HTML: <a href="caminho/do/arquivo.md">
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)|\!\[.*?\]\((.*?)\)|<a href="(.*?)">')
    matches = link_pattern.finditer(content)

    for match in matches:
        link_path = None
        if match.group(1):
            link_path = match.group(1)
        elif match.group(2):
            link_path = match.group(2)
        elif match.group(3):
            link_path = match.group(3)

        if link_path and not link_path.startswith(('http://', 'https://', '#', 'mailto:')):
            # Remove âncoras de links internos (ex: #secao)
            link_path_without_anchor = link_path.split('#')[0]

            # Constrói o caminho absoluto para o link
            # Se o link começa com '/', é relativo à raiz do projeto docs
            if link_path_without_anchor.startswith('/'):
                abs_link_path = os.path.join(root_dir, link_path_without_anchor[1:])
            else:
                # Caso contrário, é relativo ao diretório do arquivo atual
                abs_link_path = os.path.join(os.path.dirname(filepath), link_path_without_anchor)

            # Normaliza o caminho para remover '..' e '.'
            abs_link_path = os.path.normpath(abs_link_path)

            if not os.path.exists(abs_link_path) and link_path_without_anchor:
                line_number = content.count('\n', 0, match.start()) + 1
                broken_links.append(f"- **Linha {line_number}**: Link quebrado: [{link_path}]({link_path})")
    return broken_links

def main():
    docs_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    markdown_files = find_markdown_files(docs_root)
    
    report_path = os.path.join(docs_root, 'RELATORIO_LINKS_REAIS.md')
    
    total_broken_links = 0
    files_with_problems = 0
    
    report_content = []
    report_content.append(f"# Relatório de Links Quebrados REAIS - Projeto Docs")
    report_content.append(f"**Data**: {datetime.now().strftime('%c')}")
    report_content.append(f"**Nota**: Ignorando arquivos de relatório para mostrar apenas links reais quebrados\n")
    
    broken_links_by_file = {}

    print("🔍 Verificando links REAIS na documentação (ignorando relatórios)...")

    for md_file in markdown_files:
        relative_filepath = os.path.relpath(md_file, docs_root)
        
        # Ignora arquivos de relatório
        if is_report_file(relative_filepath):
            print(f"⏭️  Ignorando arquivo de relatório: {relative_filepath}")
            continue
        
        broken = check_links_in_file(md_file, docs_root)
        if broken:
            files_with_problems += 1
            total_broken_links += len(broken)
            broken_links_by_file[relative_filepath] = broken
    
    report_content.append(f"## Resumo")
    report_content.append(f"- **Arquivos com problemas**: {files_with_problems}")
    report_content.append(f"- **Total de links quebrados**: {total_broken_links}\n")
    
    if broken_links_by_file:
        report_content.append(f"## Links Quebrados por Arquivo")
        for filename, links in broken_links_by_file.items():
            report_content.append(f"\n### {filename}\n")
            report_content.extend(links)
    else:
        report_content.append("## 🎉 Nenhum link quebrado encontrado!")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_content))

    print(f"📊 Relatório salvo em: {report_path}")
    print(f"📈 Total de arquivos com problemas: {files_with_problems}")
    print(f"🔗 Total de links quebrados: {total_broken_links}\n")

    if files_with_problems > 0:
        print("❌ Links quebrados encontrados:")
        for filename in broken_links_by_file.keys():
            print(f"  📄 {filename}: {len(broken_links_by_file[filename])} problemas")
    else:
        print("✅ Nenhum link quebrado encontrado. A documentação está impecável!")

if __name__ == "__main__":
    main()
