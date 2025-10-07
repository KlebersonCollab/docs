"""
Exemplo do Padrão Simple Factory - Sistema de Pagamento

Este exemplo demonstra como implementar o padrão Simple Factory para criar
diferentes tipos de processadores de pagamento (Stripe, PayPal, PagSeguro)
de forma centralizada e reutilizável.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Any, List
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
    STRIPE = "stripe"
    PAYPAL = "paypal"
    PAGSEGURO = "pagseguro"
    MERCADOPAGO = "mercadopago"


# Interface para processadores de pagamento
class PaymentProcessor(ABC):
    """Interface para processadores de pagamento"""
    
    @abstractmethod
    def process_payment(self, amount: Decimal, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa o pagamento"""
        pass
    
    @abstractmethod
    def get_processor_name(self) -> str:
        """Retorna o nome do processador"""
        pass
    
    @abstractmethod
    def get_fee_rate(self) -> Decimal:
        """Retorna a taxa de processamento"""
        pass
    
    @abstractmethod
    def get_supported_currencies(self) -> List[str]:
        """Retorna moedas suportadas"""
        pass


# Implementação concreta: Stripe
class StripeProcessor(PaymentProcessor):
    """Processador de pagamento Stripe"""
    
    def __init__(self):
        self.fee_rate = Decimal('0.029')  # 2.9%
        self.supported_currencies = ['USD', 'EUR', 'BRL']
    
    def process_payment(self, amount: Decimal, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento via Stripe"""
        print(f"💳 Processando pagamento via Stripe: ${amount}")
        print(f"📊 Taxa: {self.fee_rate * 100}%")
        
        # Simular processamento
        fee = amount * self.fee_rate
        total = amount + fee
        
        return {
            'status': PaymentStatus.APPROVED,
            'processor': self.get_processor_name(),
            'amount': amount,
            'fee': fee,
            'total': total,
            'transaction_id': f'stripe_{data.get("card_number", "****")[-4:]}',
            'currency': data.get('currency', 'USD')
        }
    
    def get_processor_name(self) -> str:
        return 'Stripe'
    
    def get_fee_rate(self) -> Decimal:
        return self.fee_rate
    
    def get_supported_currencies(self) -> List[str]:
        return self.supported_currencies


# Implementação concreta: PayPal
class PayPalProcessor(PaymentProcessor):
    """Processador de pagamento PayPal"""
    
    def __init__(self):
        self.fee_rate = Decimal('0.034')  # 3.4%
        self.supported_currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']
    
    def process_payment(self, amount: Decimal, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento via PayPal"""
        print(f"🅿️ Processando pagamento via PayPal: ${amount}")
        print(f"📊 Taxa: {self.fee_rate * 100}%")
        
        # Simular processamento
        fee = amount * self.fee_rate
        total = amount + fee
        
        return {
            'status': PaymentStatus.APPROVED,
            'processor': self.get_processor_name(),
            'amount': amount,
            'fee': fee,
            'total': total,
            'transaction_id': f'paypal_{data.get("email", "****")[-8:]}',
            'currency': data.get('currency', 'USD')
        }
    
    def get_processor_name(self) -> str:
        return 'PayPal'
    
    def get_fee_rate(self) -> Decimal:
        return self.fee_rate
    
    def get_supported_currencies(self) -> List[str]:
        return self.supported_currencies


# Implementação concreta: PagSeguro
class PagSeguroProcessor(PaymentProcessor):
    """Processador de pagamento PagSeguro"""
    
    def __init__(self):
        self.fee_rate = Decimal('0.039')  # 3.9%
        self.supported_currencies = ['BRL']
    
    def process_payment(self, amount: Decimal, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento via PagSeguro"""
        print(f"🇧🇷 Processando pagamento via PagSeguro: R$ {amount}")
        print(f"📊 Taxa: {self.fee_rate * 100}%")
        
        # Simular processamento
        fee = amount * self.fee_rate
        total = amount + fee
        
        return {
            'status': PaymentStatus.APPROVED,
            'processor': self.get_processor_name(),
            'amount': amount,
            'fee': fee,
            'total': total,
            'transaction_id': f'pagseguro_{data.get("cpf", "****")[-4:]}',
            'currency': 'BRL'
        }
    
    def get_processor_name(self) -> str:
        return 'PagSeguro'
    
    def get_fee_rate(self) -> Decimal:
        return self.fee_rate
    
    def get_supported_currencies(self) -> List[str]:
        return self.supported_currencies


# Implementação concreta: MercadoPago
class MercadoPagoProcessor(PaymentProcessor):
    """Processador de pagamento MercadoPago"""
    
    def __init__(self):
        self.fee_rate = Decimal('0.049')  # 4.9%
        self.supported_currencies = ['BRL', 'ARS', 'MXN', 'CLP', 'COP', 'UYU']
    
    def process_payment(self, amount: Decimal, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento via MercadoPago"""
        print(f"🛒 Processando pagamento via MercadoPago: R$ {amount}")
        print(f"📊 Taxa: {self.fee_rate * 100}%")
        
        # Simular processamento
        fee = amount * self.fee_rate
        total = amount + fee
        
        return {
            'status': PaymentStatus.APPROVED,
            'processor': self.get_processor_name(),
            'amount': amount,
            'fee': fee,
            'total': total,
            'transaction_id': f'mercadopago_{data.get("user_id", "****")[-4:]}',
            'currency': data.get('currency', 'BRL')
        }
    
    def get_processor_name(self) -> str:
        return 'MercadoPago'
    
    def get_fee_rate(self) -> Decimal:
        return self.fee_rate
    
    def get_supported_currencies(self) -> List[str]:
        return self.supported_currencies


# Simple Factory para criar processadores de pagamento
class PaymentProcessorFactory:
    """Factory para criar processadores de pagamento"""
    
    @staticmethod
    def create_processor(method: PaymentMethod) -> PaymentProcessor:
        """Cria um processador baseado no método de pagamento"""
        processors = {
            PaymentMethod.STRIPE: StripeProcessor,
            PaymentMethod.PAYPAL: PayPalProcessor,
            PaymentMethod.PAGSEGURO: PagSeguroProcessor,
            PaymentMethod.MERCADOPAGO: MercadoPagoProcessor
        }
        
        if method not in processors:
            raise ValueError(f"Método de pagamento '{method}' não suportado")
        
        return processors[method]()
    
    @staticmethod
    def get_supported_methods() -> List[PaymentMethod]:
        """Retorna lista de métodos suportados"""
        return list(PaymentMethod)
    
    @staticmethod
    def is_supported(method: PaymentMethod) -> bool:
        """Verifica se um método é suportado"""
        return method in PaymentMethod


# Serviço de pagamento que usa a Factory
class PaymentService:
    """Serviço de pagamento que demonstra o uso da Factory"""
    
    def __init__(self):
        self.factory = PaymentProcessorFactory()
    
    def process_payment(self, method: PaymentMethod, amount: Decimal, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa pagamento usando a Factory"""
        try:
            # Criar processador usando Factory
            processor = self.factory.create_processor(method)
            
            # Processar pagamento
            result = processor.process_payment(amount, data)
            
            return {
                'success': True,
                'data': result
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro interno: {str(e)}'
            }
    
    def get_processor_info(self, method: PaymentMethod) -> Dict[str, Any]:
        """Retorna informações sobre um processador"""
        try:
            processor = self.factory.create_processor(method)
            return {
                'name': processor.get_processor_name(),
                'fee_rate': float(processor.get_fee_rate() * 100),
                'supported_currencies': processor.get_supported_currencies()
            }
        except ValueError as e:
            return {'error': str(e)}


# Exemplo de uso
def demonstrate_payment_factory():
    """Demonstra o uso do padrão Simple Factory para pagamentos"""
    print("=== Demonstração do Padrão Simple Factory para Pagamentos ===\n")
    
    service = PaymentService()
    
    # Casos de teste
    test_cases = [
        {
            'method': PaymentMethod.STRIPE,
            'amount': Decimal('100.00'),
            'data': {
                'card_number': '4111111111111111',
                'currency': 'USD',
                'email': 'user@example.com'
            }
        },
        {
            'method': PaymentMethod.PAYPAL,
            'amount': Decimal('150.00'),
            'data': {
                'email': 'user@paypal.com',
                'currency': 'USD'
            }
        },
        {
            'method': PaymentMethod.PAGSEGURO,
            'amount': Decimal('200.00'),
            'data': {
                'cpf': '12345678901',
                'currency': 'BRL'
            }
        },
        {
            'method': PaymentMethod.MERCADOPAGO,
            'amount': Decimal('250.00'),
            'data': {
                'user_id': 'user123',
                'currency': 'BRL'
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"--- Teste {i}: {test_case['method'].value.upper()} ---")
        
        result = service.process_payment(
            test_case['method'],
            test_case['amount'],
            test_case['data']
        )
        
        if result['success']:
            data = result['data']
            print(f"✅ Status: {data['status'].value}")
            print(f"💳 Processador: {data['processor']}")
            print(f"💰 Valor: ${data['amount']}")
            print(f"💸 Taxa: ${data['fee']}")
            print(f"💵 Total: ${data['total']}")
            print(f"🆔 Transação: {data['transaction_id']}")
        else:
            print(f"❌ Erro: {result['error']}")
        
        print()


def demonstrate_processor_info():
    """Demonstra informações sobre os processadores"""
    print("=== Informações dos Processadores ===\n")
    
    service = PaymentService()
    
    for method in PaymentMethod:
        print(f"--- {method.value.upper()} ---")
        info = service.get_processor_info(method)
        
        if 'error' not in info:
            print(f"📊 Nome: {info['name']}")
            print(f"💸 Taxa: {info['fee_rate']}%")
            print(f"🌍 Moedas: {', '.join(info['supported_currencies'])}")
        else:
            print(f"❌ Erro: {info['error']}")
        
        print()


def demonstrate_flexibility():
    """Demonstra flexibilidade da Factory"""
    print("=== Demonstração de Flexibilidade ===\n")
    
    factory = PaymentProcessorFactory()
    
    print("Métodos de pagamento suportados:")
    for method in factory.get_supported_methods():
        print(f"- {method.value}")
    
    print(f"\nTotal de métodos: {len(factory.get_supported_methods())}")
    
    print("\nVerificações de suporte:")
    test_methods = [PaymentMethod.STRIPE, PaymentMethod.PAYPAL, PaymentMethod.PAGSEGURO]
    
    for method in test_methods:
        supported = factory.is_supported(method)
        status = "✅" if supported else "❌"
        print(f"{status} {method.value}: {'Suportado' if supported else 'Não suportado'}")


if __name__ == "__main__":
    demonstrate_payment_factory()
    print("\n" + "="*50 + "\n")
    demonstrate_processor_info()
    print("\n" + "="*50 + "\n")
    demonstrate_flexibility()




