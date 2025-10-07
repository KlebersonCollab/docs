"""
Exemplo do Padrão Strategy - Sistema de Pagamento

Este exemplo demonstra como implementar o padrão Strategy para processar
diferentes tipos de pagamento (Cartão, PIX, Boleto) de forma flexível e
respeitando os princípios SOLID.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Any
from enum import Enum


class PaymentStatus(Enum):
    """Status possíveis de um pagamento"""
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class PaymentMethod(Enum):
    """Métodos de pagamento disponíveis"""
    CREDIT_CARD = "credit_card"
    PIX = "pix"
    BOLETO = "boleto"
    DEBIT_CARD = "debit_card"


# Interface da estratégia
class PaymentStrategy(ABC):
    """Interface para estratégias de pagamento"""
    
    @abstractmethod
    def process_payment(self, amount: Decimal, **kwargs) -> Dict[str, Any]:
        """Processa o pagamento"""
        pass
    
    @abstractmethod
    def get_method_name(self) -> str:
        """Retorna o nome do método de pagamento"""
        pass
    
    @abstractmethod
    def get_fee_rate(self) -> Decimal:
        """Retorna a taxa de processamento"""
        pass
    
    @abstractmethod
    def validate_payment_data(self, **kwargs) -> bool:
        """Valida os dados do pagamento"""
        pass


# Estratégia concreta: Cartão de Crédito
class CreditCardPayment(PaymentStrategy):
    """Estratégia para pagamento com cartão de crédito"""
    
    def __init__(self):
        self.fee_rate = Decimal('0.029')  # 2.9%
        self.method_name = "Cartão de Crédito"
    
    def process_payment(self, amount: Decimal, **kwargs) -> Dict[str, Any]:
        """Processa pagamento com cartão de crédito"""
        if not self.validate_payment_data(**kwargs):
            return {
                'status': PaymentStatus.REJECTED,
                'message': 'Dados do cartão inválidos',
                'transaction_id': None
            }
        
        # Simular processamento
        fee = amount * self.fee_rate
        total = amount + fee
        
        return {
            'status': PaymentStatus.APPROVED,
            'message': 'Pagamento aprovado',
            'transaction_id': f'CC_{kwargs.get("card_number", "****")[-4:]}',
            'amount': amount,
            'fee': fee,
            'total': total,
            'method': self.method_name
        }
    
    def get_method_name(self) -> str:
        return self.method_name
    
    def get_fee_rate(self) -> Decimal:
        return self.fee_rate
    
    def validate_payment_data(self, **kwargs) -> bool:
        """Valida dados do cartão"""
        required_fields = ['card_number', 'cvv', 'expiry_date', 'holder_name']
        return all(field in kwargs for field in required_fields)


# Estratégia concreta: PIX
class PIXPayment(PaymentStrategy):
    """Estratégia para pagamento via PIX"""
    
    def __init__(self):
        self.fee_rate = Decimal('0.005')  # 0.5%
        self.method_name = "PIX"
    
    def process_payment(self, amount: Decimal, **kwargs) -> Dict[str, Any]:
        """Processa pagamento via PIX"""
        if not self.validate_payment_data(**kwargs):
            return {
                'status': PaymentStatus.REJECTED,
                'message': 'Chave PIX inválida',
                'transaction_id': None
            }
        
        # Simular processamento
        fee = amount * self.fee_rate
        total = amount + fee
        
        return {
            'status': PaymentStatus.APPROVED,
            'message': 'PIX processado com sucesso',
            'transaction_id': f'PIX_{kwargs.get("pix_key", "****")[-8:]}',
            'amount': amount,
            'fee': fee,
            'total': total,
            'method': self.method_name
        }
    
    def get_method_name(self) -> str:
        return self.method_name
    
    def get_fee_rate(self) -> Decimal:
        return self.fee_rate
    
    def validate_payment_data(self, **kwargs) -> bool:
        """Valida chave PIX"""
        return 'pix_key' in kwargs and len(kwargs['pix_key']) >= 10


# Estratégia concreta: Boleto
class BoletoPayment(PaymentStrategy):
    """Estratégia para pagamento via boleto"""
    
    def __init__(self):
        self.fee_rate = Decimal('0.015')  # 1.5%
        self.method_name = "Boleto Bancário"
    
    def process_payment(self, amount: Decimal, **kwargs) -> Dict[str, Any]:
        """Processa pagamento via boleto"""
        if not self.validate_payment_data(**kwargs):
            return {
                'status': PaymentStatus.REJECTED,
                'message': 'Dados do boleto inválidos',
                'transaction_id': None
            }
        
        # Simular processamento
        fee = amount * self.fee_rate
        total = amount + fee
        
        return {
            'status': PaymentStatus.PENDING,
            'message': 'Boleto gerado com sucesso',
            'transaction_id': f'BOL_{kwargs.get("cpf", "****")[-4:]}',
            'amount': amount,
            'fee': fee,
            'total': total,
            'method': self.method_name,
            'boleto_code': f'23791{kwargs.get("cpf", "00000000000")}'
        }
    
    def get_method_name(self) -> str:
        return self.method_name
    
    def get_fee_rate(self) -> Decimal:
        return self.fee_rate
    
    def validate_payment_data(self, **kwargs) -> bool:
        """Valida dados do boleto"""
        return 'cpf' in kwargs and len(kwargs['cpf']) == 11


# Estratégia concreta: Cartão de Débito
class DebitCardPayment(PaymentStrategy):
    """Estratégia para pagamento com cartão de débito"""
    
    def __init__(self):
        self.fee_rate = Decimal('0.019')  # 1.9%
        self.method_name = "Cartão de Débito"
    
    def process_payment(self, amount: Decimal, **kwargs) -> Dict[str, Any]:
        """Processa pagamento com cartão de débito"""
        if not self.validate_payment_data(**kwargs):
            return {
                'status': PaymentStatus.REJECTED,
                'message': 'Dados do cartão inválidos',
                'transaction_id': None
            }
        
        # Simular processamento
        fee = amount * self.fee_rate
        total = amount + fee
        
        return {
            'status': PaymentStatus.APPROVED,
            'message': 'Pagamento aprovado',
            'transaction_id': f'DC_{kwargs.get("card_number", "****")[-4:]}',
            'amount': amount,
            'fee': fee,
            'total': total,
            'method': self.method_name
        }
    
    def get_method_name(self) -> str:
        return self.method_name
    
    def get_fee_rate(self) -> Decimal:
        return self.fee_rate
    
    def validate_payment_data(self, **kwargs) -> bool:
        """Valida dados do cartão"""
        required_fields = ['card_number', 'cvv', 'expiry_date', 'holder_name']
        return all(field in kwargs for field in required_fields)


# Contexto - Processador de Pagamentos
class PaymentProcessor:
    """Contexto que utiliza as estratégias de pagamento"""
    
    def __init__(self):
        self._strategy: PaymentStrategy = None
    
    def set_payment_strategy(self, strategy: PaymentStrategy) -> 'PaymentProcessor':
        """Define a estratégia de pagamento"""
        self._strategy = strategy
        return self
    
    def process_payment(self, amount: Decimal, **kwargs) -> Dict[str, Any]:
        """Processa o pagamento usando a estratégia definida"""
        if self._strategy is None:
            raise ValueError("Estratégia de pagamento não definida")
        
        return self._strategy.process_payment(amount, **kwargs)
    
    def get_payment_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o método de pagamento"""
        if self._strategy is None:
            raise ValueError("Estratégia de pagamento não definida")
        
        return {
            'method': self._strategy.get_method_name(),
            'fee_rate': float(self._strategy.get_fee_rate() * 100)
        }


# Factory para criar estratégias
class PaymentStrategyFactory:
    """Factory para criar estratégias de pagamento"""
    
    @staticmethod
    def create_strategy(method: PaymentMethod) -> PaymentStrategy:
        """Cria uma estratégia baseada no método de pagamento"""
        strategies = {
            PaymentMethod.CREDIT_CARD: CreditCardPayment,
            PaymentMethod.PIX: PIXPayment,
            PaymentMethod.BOLETO: BoletoPayment,
            PaymentMethod.DEBIT_CARD: DebitCardPayment
        }
        
        if method not in strategies:
            raise ValueError(f"Método de pagamento '{method}' não suportado")
        
        return strategies[method]()
    
    @staticmethod
    def get_available_methods() -> list:
        """Retorna lista de métodos disponíveis"""
        return [method.value for method in PaymentMethod]


# Exemplo de uso
def demonstrate_payment_strategy():
    """Demonstra o uso do padrão Strategy para pagamentos"""
    print("=== Demonstração do Padrão Strategy para Pagamentos ===\n")
    
    # Criar processador
    processor = PaymentProcessor()
    
    # Dados de teste
    amount = Decimal('100.00')
    
    # Casos de teste
    test_cases = [
        {
            'method': PaymentMethod.CREDIT_CARD,
            'data': {
                'card_number': '4111111111111111',
                'cvv': '123',
                'expiry_date': '12/25',
                'holder_name': 'João Silva'
            }
        },
        {
            'method': PaymentMethod.PIX,
            'data': {
                'pix_key': 'joao.silva@email.com'
            }
        },
        {
            'method': PaymentMethod.BOLETO,
            'data': {
                'cpf': '12345678901'
            }
        },
        {
            'method': PaymentMethod.DEBIT_CARD,
            'data': {
                'card_number': '5555555555554444',
                'cvv': '456',
                'expiry_date': '06/26',
                'holder_name': 'Maria Santos'
            }
        }
    ]
    
    for case in test_cases:
        print(f"--- Processando {case['method'].value.upper()} ---")
        
        try:
            # Criar estratégia
            strategy = PaymentStrategyFactory.create_strategy(case['method'])
            
            # Configurar processador
            processor.set_payment_strategy(strategy)
            
            # Processar pagamento
            result = processor.process_payment(amount, **case['data'])
            
            # Exibir resultado
            print(f"✅ Status: {result['status'].value}")
            print(f"📝 Mensagem: {result['message']}")
            print(f"🆔 Transação: {result['transaction_id']}")
            print(f"💰 Valor: R$ {result['amount']:.2f}")
            print(f"💸 Taxa: R$ {result['fee']:.2f}")
            print(f"💵 Total: R$ {result['total']:.2f}")
            print(f"📊 Método: {result['method']}")
            
            if 'boleto_code' in result:
                print(f"📄 Código do Boleto: {result['boleto_code']}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        print()


def demonstrate_flexibility():
    """Demonstra a flexibilidade do padrão Strategy"""
    print("=== Demonstração de Flexibilidade ===\n")
    
    processor = PaymentProcessor()
    amount = Decimal('50.00')
    
    print(f"Valor base: R$ {amount:.2f}\n")
    
    # Testar todos os métodos
    for method in PaymentMethod:
        try:
            strategy = PaymentStrategyFactory.create_strategy(method)
            processor.set_payment_strategy(strategy)
            
            info = processor.get_payment_info()
            print(f"{info['method']}: Taxa de {info['fee_rate']:.1f}%")
            
        except Exception as e:
            print(f"Erro com {method.value}: {e}")


if __name__ == "__main__":
    demonstrate_payment_strategy()
    print("\n" + "="*50 + "\n")
    demonstrate_flexibility()




