#!/usr/bin/env python3
"""
Script para verificar links quebrados na documentação do projeto docs.
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Dict, Tuple

class LinkChecker:
    def __init__(self, docs_root: str):
        self.docs_root = Path(docs_root)
        self.broken_links = []
        self.valid_files = set()
        self.scan_files()
    
    def scan_files(self):
        """Escaneia todos os arquivos markdown para criar índice de arquivos válidos."""
        for md_file in self.docs_root.rglob("*.md"):
            # Caminho relativo ao docs_root
            rel_path = md_file.relative_to(self.docs_root)
            self.valid_files.add(str(rel_path))
            # Também adiciona versão sem extensão
            self.valid_files.add(str(rel_path.with_suffix("")))
    
    def extract_links(self, content: str) -> List[Tuple[str, int]]:
        """Extrai links markdown do conteúdo."""
        # Padrão para links markdown [texto](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = []
        
        for match in re.finditer(link_pattern, content):
            link_text = match.group(1)
            link_url = match.group(2)
            line_number = content[:match.start()].count('\n') + 1
            links.append((link_text, link_url, line_number))
        
        return links
    
    def is_valid_link(self, link_url: str, current_file: str) -> bool:
        """Verifica se um link é válido."""
        # Ignora links externos
        if link_url.startswith(('http://', 'https://', 'mailto:', '#')):
            return True
        
        # Ignora links para seções (começam com #)
        if link_url.startswith('#'):
            return True
        
        # Remove fragmentos (#section)
        clean_url = link_url.split('#')[0]
        
        # Se é um caminho relativo
        if not clean_url.startswith('/'):
            # Caminho relativo ao arquivo atual
            current_dir = Path(current_file).parent
            target_path = current_dir / clean_url
        else:
            # Caminho absoluto
            target_path = self.docs_root / clean_url.lstrip('/')
        
        # Normaliza o caminho
        try:
            target_path = target_path.resolve()
            docs_path = self.docs_root.resolve()
            
            # Verifica se está dentro do docs_root
            if not str(target_path).startswith(str(docs_path)):
                return False
            
            # Verifica se o arquivo existe
            rel_path = target_path.relative_to(docs_path)
            
            # Tenta diferentes extensões
            possible_paths = [
                str(rel_path),
                str(rel_path) + '.md',
                str(rel_path) + '/README.md',
                str(rel_path) + '/index.md'
            ]
            
            for path in possible_paths:
                if path in self.valid_files:
                    return True
            
            return False
            
        except (ValueError, OSError):
            return False
    
    def check_file(self, file_path: str) -> List[Dict]:
        """Verifica links em um arquivo específico."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            issues.append({
                'file': file_path,
                'line': 0,
                'type': 'error',
                'message': f'Erro ao ler arquivo: {e}'
            })
            return issues
        
        links = self.extract_links(content)
        
        for link_text, link_url, line_number in links:
            if not self.is_valid_link(link_url, file_path):
                issues.append({
                    'file': file_path,
                    'line': line_number,
                    'type': 'broken_link',
                    'link_text': link_text,
                    'link_url': link_url,
                    'message': f'Link quebrado: [{link_text}]({link_url})'
                })
        
        return issues
    
    def check_all_files(self) -> Dict[str, List[Dict]]:
        """Verifica todos os arquivos markdown."""
        all_issues = {}
        
        for md_file in self.docs_root.rglob("*.md"):
            file_path = str(md_file)
            issues = self.check_file(file_path)
            
            if issues:
                all_issues[file_path] = issues
        
        return all_issues
    
    def generate_report(self, issues: Dict[str, List[Dict]]) -> str:
        """Gera relatório de links quebrados."""
        report = []
        report.append("# Relatório de Links Quebrados - Projeto Docs")
        report.append(f"**Data**: {os.popen('date').read().strip()}")
        report.append("")
        
        total_files = len(issues)
        total_issues = sum(len(file_issues) for file_issues in issues.values())
        
        report.append(f"## Resumo")
        report.append(f"- **Arquivos com problemas**: {total_files}")
        report.append(f"- **Total de links quebrados**: {total_issues}")
        report.append("")
        
        if total_issues == 0:
            report.append("✅ **Nenhum link quebrado encontrado!**")
            return "\n".join(report)
        
        report.append("## Links Quebrados por Arquivo")
        report.append("")
        
        for file_path, file_issues in issues.items():
            # Converte para caminho relativo
            rel_path = Path(file_path).relative_to(self.docs_root)
            report.append(f"### {rel_path}")
            report.append("")
            
            for issue in file_issues:
                if issue['type'] == 'broken_link':
                    report.append(f"- **Linha {issue['line']}**: {issue['message']}")
                else:
                    report.append(f"- **Erro**: {issue['message']}")
            
            report.append("")
        
        return "\n".join(report)

def main():
    docs_root = "/home/kleberson/Projetos/Skynet/docs"
    checker = LinkChecker(docs_root)
    
    print("🔍 Verificando links na documentação...")
    issues = checker.check_all_files()
    
    report = checker.generate_report(issues)
    
    # Salva o relatório
    report_file = Path(docs_root) / "RELATORIO_LINKS_QUEBRADOS.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📊 Relatório salvo em: {report_file}")
    print(f"📈 Total de arquivos com problemas: {len(issues)}")
    
    total_issues = sum(len(file_issues) for file_issues in issues.values())
    print(f"🔗 Total de links quebrados: {total_issues}")
    
    if total_issues > 0:
        print("\n❌ Links quebrados encontrados:")
        for file_path, file_issues in issues.items():
            rel_path = Path(file_path).relative_to(Path(docs_root))
            print(f"  📄 {rel_path}: {len(file_issues)} problemas")
    else:
        print("\n✅ Nenhum link quebrado encontrado!")

if __name__ == "__main__":
    main()
