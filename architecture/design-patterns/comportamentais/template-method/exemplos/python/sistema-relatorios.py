"""
Exemplo do Padrão Template Method - Sistema de Relatórios

Este exemplo demonstra como implementar o padrão Template Method para
eliminar duplicação de código em um sistema de geração de relatórios
que processa diferentes tipos de dados e gera relatórios em formatos diversos.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
import json
import csv
import xml.etree.ElementTree as ET


class ReportGenerator(ABC):
    """
    Classe abstrata que define o template method para geração de relatórios.
    Define o esqueleto do algoritmo e implementa métodos comuns.
    """
    
    def generate_report(self, data: List[Dict[str, Any]]) -> str:
        """
        Template Method - define o esqueleto do algoritmo
        Este método não pode ser sobrescrito pelas subclasses
        """
        print("🚀 Iniciando geração de relatório...")
        
        # 1. Validar dados
        validated_data = self.validate_data(data)
        print(f"✅ Dados validados: {len(validated_data)} registros")
        
        # 2. Processar dados
        processed_data = self.process_data(validated_data)
        print(f"🔍 Dados processados: {len(processed_data)} registros")
        
        # 3. Formatar dados
        formatted_data = self.format_data(processed_data)
        print(f"📝 Dados formatados: {len(formatted_data)} registros")
        
        # 4. Gerar relatório (implementação comum)
        report_content = self.generate_report_content(formatted_data)
        
        # 5. Salvar relatório (implementação comum)
        file_path = self.save_report(report_content)
        
        # 6. Enviar notificações (implementação comum)
        self.send_notifications(file_path, len(formatted_data))
        
        print("✅ Relatório gerado com sucesso!")
        return file_path
    
    @abstractmethod
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Método abstrato para validar dados
        Cada subclasse implementa sua própria lógica de validação
        """
        pass
    
    @abstractmethod
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Método abstrato para processar dados
        Cada subclasse implementa sua própria lógica de processamento
        """
        pass
    
    @abstractmethod
    def format_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Método abstrato para formatar dados
        Cada subclasse implementa sua própria lógica de formatação
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Método abstrato para obter extensão do arquivo
        Cada subclasse retorna sua extensão específica
        """
        pass
    
    @abstractmethod
    def get_report_type(self) -> str:
        """
        Método abstrato para obter tipo de relatório
        Cada subclasse retorna seu tipo específico
        """
        pass
    
    def generate_report_content(self, data: List[Dict[str, Any]]) -> str:
        """
        Método comum para gerar conteúdo do relatório
        Implementação compartilhada entre todas as subclasses
        """
        print("📊 Gerando conteúdo do relatório...")
        
        # Cabeçalho do relatório
        header = self._generate_header()
        
        # Corpo do relatório
        body = self._generate_body(data)
        
        # Rodapé do relatório
        footer = self._generate_footer()
        
        return f"{header}\n{body}\n{footer}"
    
    def save_report(self, content: str) -> str:
        """
        Método comum para salvar relatório
        Implementação compartilhada entre todas as subclasses
        """
        print("💾 Salvando relatório...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{self.get_report_type().lower()}_{timestamp}.{self.get_file_extension()}"
        filepath = f"reports/{filename}"
        
        # Simular salvamento do arquivo
        print(f"   📁 Arquivo salvo em: {filepath}")
        print(f"   📊 Tamanho do arquivo: {len(content)} caracteres")
        
        return filepath
    
    def send_notifications(self, file_path: str, record_count: int) -> None:
        """
        Método comum para enviar notificações
        Implementação compartilhada entre todas as subclasses
        """
        print("📧 Enviando notificações...")
        
        # Notificar por email
        self._send_email_notification(file_path, record_count)
        
        # Notificar por sistema interno
        self._send_internal_notification(file_path, record_count)
        
        # Notificar stakeholders
        self._notify_stakeholders(file_path, record_count)
    
    def _generate_header(self) -> str:
        """Gerar cabeçalho do relatório"""
        return f"""
========================================
RELATÓRIO {self.get_report_type().upper()}
========================================
Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Tipo de Relatório: {self.get_report_type()}
========================================
"""
    
    def _generate_body(self, data: List[Dict[str, Any]]) -> str:
        """Gerar corpo do relatório"""
        if not data:
            return "Nenhum dado encontrado para o relatório."
        
        body = f"Total de Registros: {len(data)}\n\n"
        
        # Mostrar primeiros 5 registros como exemplo
        for i, record in enumerate(data[:5]):
            body += f"Registro {i+1}:\n"
            for key, value in record.items():
                body += f"  {key}: {value}\n"
            body += "\n"
        
        if len(data) > 5:
            body += f"... e mais {len(data) - 5} registros\n"
        
        return body
    
    def _generate_footer(self) -> str:
        """Gerar rodapé do relatório"""
        return f"""
========================================
Relatório gerado automaticamente
Sistema de Relatórios v1.0
========================================
"""
    
    def _send_email_notification(self, file_path: str, record_count: int) -> None:
        """Enviar notificação por email"""
        print(f"   📧 Email enviado para: admin@empresa.com")
        print(f"   📧 Assunto: Relatório {self.get_report_type()} - {record_count} registros")
    
    def _send_internal_notification(self, file_path: str, record_count: int) -> None:
        """Enviar notificação interna"""
        print(f"   🔔 Notificação interna enviada")
        print(f"   🔔 Arquivo: {file_path}")
    
    def _notify_stakeholders(self, file_path: str, record_count: int) -> None:
        """Notificar stakeholders"""
        print(f"   👥 Stakeholders notificados")
        print(f"   👥 Relatório: {self.get_report_type()} com {record_count} registros")


class SalesReportGenerator(ReportGenerator):
    """Gerador de relatórios de vendas"""
    
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validar dados de vendas"""
        print("🔍 Validando dados de vendas...")
        
        validated_data = []
        for record in data:
            # Validar campos obrigatórios
            if 'vendedor' in record and 'valor' in record and 'data' in record:
                # Validar valor numérico
                try:
                    float(record['valor'])
                    validated_data.append(record)
                except ValueError:
                    print(f"⚠️ Valor inválido ignorado: {record}")
            else:
                print(f"⚠️ Registro incompleto ignorado: {record}")
        
        return validated_data
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processar dados de vendas"""
        print("⚙️ Processando dados de vendas...")
        
        processed_data = []
        for record in data:
            processed_record = {
                'vendedor': record['vendedor'].upper(),
                'valor': float(record['valor']),
                'data': record['data'],
                'comissao': float(record['valor']) * 0.05,  # 5% de comissão
                'status': 'PROCESSADO'
            }
            processed_data.append(processed_record)
        
        return processed_data
    
    def format_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formatar dados de vendas"""
        print("📝 Formatando dados de vendas...")
        
        formatted_data = []
        for record in data:
            formatted_record = {
                'Vendedor': record['vendedor'],
                'Valor da Venda': f"R$ {record['valor']:.2f}",
                'Data': record['data'],
                'Comissão': f"R$ {record['comissao']:.2f}",
                'Status': record['status']
            }
            formatted_data.append(formatted_record)
        
        return formatted_data
    
    def get_file_extension(self) -> str:
        return "txt"
    
    def get_report_type(self) -> str:
        return "VENDAS"


class InventoryReportGenerator(ReportGenerator):
    """Gerador de relatórios de estoque"""
    
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validar dados de estoque"""
        print("🔍 Validando dados de estoque...")
        
        validated_data = []
        for record in data:
            # Validar campos obrigatórios
            if 'produto' in record and 'quantidade' in record and 'preco' in record:
                # Validar quantidade e preço numéricos
                try:
                    int(record['quantidade'])
                    float(record['preco'])
                    validated_data.append(record)
                except ValueError:
                    print(f"⚠️ Dados numéricos inválidos ignorados: {record}")
            else:
                print(f"⚠️ Registro incompleto ignorado: {record}")
        
        return validated_data
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processar dados de estoque"""
        print("⚙️ Processando dados de estoque...")
        
        processed_data = []
        for record in data:
            quantidade = int(record['quantidade'])
            preco = float(record['preco'])
            
            processed_record = {
                'produto': record['produto'].upper(),
                'quantidade': quantidade,
                'preco': preco,
                'valor_total': quantidade * preco,
                'status_estoque': 'ALTO' if quantidade > 100 else 'BAIXO' if quantidade < 20 else 'NORMAL'
            }
            processed_data.append(processed_record)
        
        return processed_data
    
    def format_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formatar dados de estoque"""
        print("📝 Formatando dados de estoque...")
        
        formatted_data = []
        for record in data:
            formatted_record = {
                'Produto': record['produto'],
                'Quantidade': record['quantidade'],
                'Preço Unitário': f"R$ {record['preco']:.2f}",
                'Valor Total': f"R$ {record['valor_total']:.2f}",
                'Status do Estoque': record['status_estoque']
            }
            formatted_data.append(formatted_record)
        
        return formatted_data
    
    def get_file_extension(self) -> str:
        return "csv"
    
    def get_report_type(self) -> str:
        return "ESTOQUE"


class FinancialReportGenerator(ReportGenerator):
    """Gerador de relatórios financeiros"""
    
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validar dados financeiros"""
        print("🔍 Validando dados financeiros...")
        
        validated_data = []
        for record in data:
            # Validar campos obrigatórios
            if 'conta' in record and 'valor' in record and 'tipo' in record:
                # Validar valor numérico
                try:
                    float(record['valor'])
                    validated_data.append(record)
                except ValueError:
                    print(f"⚠️ Valor inválido ignorado: {record}")
            else:
                print(f"⚠️ Registro incompleto ignorado: {record}")
        
        return validated_data
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processar dados financeiros"""
        print("⚙️ Processando dados financeiros...")
        
        processed_data = []
        for record in data:
            valor = float(record['valor'])
            
            processed_record = {
                'conta': record['conta'].upper(),
                'valor': valor,
                'tipo': record['tipo'].upper(),
                'categoria': 'RECEITA' if valor > 0 else 'DESPESA',
                'status': 'PROCESSADO'
            }
            processed_data.append(processed_record)
        
        return processed_data
    
    def format_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formatar dados financeiros"""
        print("📝 Formatando dados financeiros...")
        
        formatted_data = []
        for record in data:
            formatted_record = {
                'Conta': record['conta'],
                'Valor': f"R$ {record['valor']:.2f}",
                'Tipo': record['tipo'],
                'Categoria': record['categoria'],
                'Status': record['status']
            }
            formatted_data.append(formatted_record)
        
        return formatted_data
    
    def get_file_extension(self) -> str:
        return "json"
    
    def get_report_type(self) -> str:
        return "FINANCEIRO"
    
    def save_report(self, content: str) -> str:
        """
        Sobrescrever método de salvamento para formato JSON
        """
        print("💾 Salvando relatório em formato JSON...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{self.get_report_type().lower()}_{timestamp}.{self.get_file_extension()}"
        filepath = f"reports/{filename}"
        
        # Simular salvamento em formato JSON
        print(f"   📁 Arquivo JSON salvo em: {filepath}")
        print(f"   📊 Tamanho do arquivo: {len(content)} caracteres")
        
        return filepath


class CustomerReportGenerator(ReportGenerator):
    """Gerador de relatórios de clientes"""
    
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validar dados de clientes"""
        print("🔍 Validando dados de clientes...")
        
        validated_data = []
        for record in data:
            # Validar campos obrigatórios
            if 'nome' in record and 'email' in record and 'telefone' in record:
                # Validar email
                if '@' in record['email']:
                    validated_data.append(record)
                else:
                    print(f"⚠️ Email inválido ignorado: {record}")
            else:
                print(f"⚠️ Registro incompleto ignorado: {record}")
        
        return validated_data
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processar dados de clientes"""
        print("⚙️ Processando dados de clientes...")
        
        processed_data = []
        for record in data:
            processed_record = {
                'nome': record['nome'].title(),
                'email': record['email'].lower(),
                'telefone': record['telefone'],
                'status': 'ATIVO',
                'data_cadastro': datetime.now().strftime('%Y-%m-%d')
            }
            processed_data.append(processed_record)
        
        return processed_data
    
    def format_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formatar dados de clientes"""
        print("📝 Formatando dados de clientes...")
        
        formatted_data = []
        for record in data:
            formatted_record = {
                'Nome': record['nome'],
                'Email': record['email'],
                'Telefone': record['telefone'],
                'Status': record['status'],
                'Data de Cadastro': record['data_cadastro']
            }
            formatted_data.append(formatted_record)
        
        return formatted_data
    
    def get_file_extension(self) -> str:
        return "xml"
    
    def get_report_type(self) -> str:
        return "CLIENTES"


# Exemplo de uso
def demonstrate_template_method():
    """Demonstra o padrão Template Method com sistema de relatórios"""
    print("=== Demonstração do Padrão Template Method - Sistema de Relatórios ===\n")
    
    # Dados de exemplo para vendas
    sales_data = [
        {'vendedor': 'João Silva', 'valor': '1500.00', 'data': '2024-01-15'},
        {'vendedor': 'Maria Santos', 'valor': '2300.50', 'data': '2024-01-16'},
        {'vendedor': 'Pedro Costa', 'valor': '800.75', 'data': '2024-01-17'}
    ]
    
    # Dados de exemplo para estoque
    inventory_data = [
        {'produto': 'Notebook', 'quantidade': '50', 'preco': '2500.00'},
        {'produto': 'Mouse', 'quantidade': '200', 'preco': '25.00'},
        {'produto': 'Teclado', 'quantidade': '15', 'preco': '150.00'}
    ]
    
    # Dados de exemplo para financeiro
    financial_data = [
        {'conta': 'Vendas', 'valor': '5000.00', 'tipo': 'receita'},
        {'conta': 'Salários', 'valor': '-3000.00', 'tipo': 'despesa'},
        {'conta': 'Aluguel', 'valor': '-800.00', 'tipo': 'despesa'}
    ]
    
    # Dados de exemplo para clientes
    customer_data = [
        {'nome': 'Ana Silva', 'email': 'ana@email.com', 'telefone': '11999999999'},
        {'nome': 'Carlos Santos', 'email': 'carlos@email.com', 'telefone': '11888888888'},
        {'nome': 'Lucia Costa', 'email': 'lucia@email.com', 'telefone': '11777777777'}
    ]
    
    # Gerar relatórios
    generators = [
        (SalesReportGenerator(), sales_data, "Vendas"),
        (InventoryReportGenerator(), inventory_data, "Estoque"),
        (FinancialReportGenerator(), financial_data, "Financeiro"),
        (CustomerReportGenerator(), customer_data, "Clientes")
    ]
    
    for generator, data, report_type in generators:
        print(f"--- Gerando Relatório de {report_type} ---")
        try:
            file_path = generator.generate_report(data)
            print(f"✅ Relatório de {report_type} gerado: {file_path}\n")
        except Exception as e:
            print(f"❌ Erro ao gerar relatório de {report_type}: {e}\n")


def demonstrate_extensibility():
    """Demonstra extensibilidade do padrão"""
    print("\n=== Demonstração de Extensibilidade ===\n")
    
    # Criar um novo tipo de gerador de relatórios
    class PerformanceReportGenerator(ReportGenerator):
        """Gerador de relatórios de performance"""
        
        def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            print("🔍 Validando dados de performance...")
            return data  # Validação simples para exemplo
        
        def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            print("⚙️ Processando dados de performance...")
            return data  # Processamento simples para exemplo
        
        def format_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            print("📝 Formatando dados de performance...")
            return data  # Formatação simples para exemplo
        
        def get_file_extension(self) -> str:
            return "txt"
        
        def get_report_type(self) -> str:
            return "PERFORMANCE"
    
    # Usar o novo gerador
    performance_data = [
        {'metrica': 'Uptime', 'valor': '99.9%'},
        {'metrica': 'Response Time', 'valor': '150ms'},
        {'metrica': 'Throughput', 'valor': '1000 req/s'}
    ]
    
    performance_generator = PerformanceReportGenerator()
    performance_generator.generate_report(performance_data)


def demonstrate_customization():
    """Demonstra personalização do padrão"""
    print("\n=== Demonstração de Personalização ===\n")
    
    # Gerador personalizado que sobrescreve métodos comuns
    class CustomReportGenerator(ReportGenerator):
        """Gerador de relatórios personalizado"""
        
        def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            print("🔍 Validando dados com lógica personalizada...")
            return data
        
        def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            print("⚙️ Processando dados com lógica personalizada...")
            return data
        
        def format_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            print("📝 Formatando dados com lógica personalizada...")
            return data
        
        def get_file_extension(self) -> str:
            return "txt"
        
        def get_report_type(self) -> str:
            return "CUSTOM"
        
        def send_notifications(self, file_path: str, record_count: int) -> None:
            """Sobrescrever método de notificação para personalização"""
            print("📧 Enviando notificações personalizadas...")
            print(f"   📧 Email personalizado enviado para: custom@empresa.com")
            print(f"   📧 Assunto personalizado: Relatório Custom - {record_count} registros")
            print(f"   🔔 Notificação personalizada enviada")
            print("✅ Notificações personalizadas enviadas com sucesso")
    
    # Usar o gerador personalizado
    custom_data = [
        {'campo1': 'valor1', 'campo2': 'valor2'},
        {'campo1': 'valor3', 'campo2': 'valor4'}
    ]
    
    custom_generator = CustomReportGenerator()
    custom_generator.generate_report(custom_data)


if __name__ == "__main__":
    demonstrate_template_method()
    demonstrate_extensibility()
    demonstrate_customization()
