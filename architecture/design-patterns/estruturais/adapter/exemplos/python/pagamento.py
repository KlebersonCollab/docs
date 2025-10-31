#!/usr/bin/env python3
"""
Exemplo prático do Padrão Adapter em Python
Sistema de pagamentos com diferentes gateways
Baseado na transcrição do vídeo sobre padrão Adapter

Este exemplo demonstra como implementar o padrão Adapter
para integrar diferentes gateways de pagamento
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
import json


class PaymentAdapter(ABC):
    """Interface que define o contrato para processadores de pagamento"""
    
    @abstractmethod
    def process_payment(self, amount: float, card_data: Dict[str, str]) -> Dict[str, Any]:
        """Processa um pagamento"""
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Estorna um pagamento"""
        pass


class StripeAdapter(PaymentAdapter):
    """Adapter para o gateway Stripe"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        print(f"🔑 Stripe inicializado com API key: {api_key[:8]}...")
    
    def process_payment(self, amount: float, card_data: Dict[str, str]) -> Dict[str, Any]:
        print(f"💳 Processando pagamento via Stripe: R$ {amount:.2f}")
        
        # Simulação da API do Stripe
        transaction_id = f"stripe_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Validação específica do Stripe
        if not self._validate_stripe_card(card_data):
            raise ValueError("Dados do cartão inválidos para Stripe")
        
        # Processamento específico do Stripe
        result = {
            'transaction_id': transaction_id,
            'status': 'approved',
            'gateway': 'stripe',
            'amount': amount,
            'fee': amount * 0.029 + 0.30,  # Taxa do Stripe
            'processed_at': datetime.now().isoformat()
        }
        
        print(f"✅ Pagamento aprovado via Stripe: {transaction_id}")
        return result
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        print(f"🔄 Estornando pagamento via Stripe: {transaction_id}")
        
        # Simulação do estorno no Stripe
        refund_id = f"stripe_refund_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = {
            'refund_id': refund_id,
            'status': 'refunded',
            'gateway': 'stripe',
            'amount': amount,
            'refunded_at': datetime.now().isoformat()
        }
        
        print(f"✅ Estorno processado via Stripe: {refund_id}")
        return result
    
    def _validate_stripe_card(self, card_data: Dict[str, str]) -> bool:
        """Validação específica do Stripe"""
        required_fields = ['number', 'exp_month', 'exp_year', 'cvc']
        return all(field in card_data for field in required_fields)


class PayPalAdapter(PaymentAdapter):
    """Adapter para o gateway PayPal"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        print(f"🔑 PayPal inicializado com Client ID: {client_id[:8]}...")
    
    def process_payment(self, amount: float, card_data: Dict[str, str]) -> Dict[str, Any]:
        print(f"💳 Processando pagamento via PayPal: R$ {amount:.2f}")
        
        # Simulação da API do PayPal
        transaction_id = f"paypal_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Validação específica do PayPal
        if not self._validate_paypal_card(card_data):
            raise ValueError("Dados do cartão inválidos para PayPal")
        
        # Processamento específico do PayPal
        result = {
            'transaction_id': transaction_id,
            'status': 'approved',
            'gateway': 'paypal',
            'amount': amount,
            'fee': amount * 0.034 + 0.35,  # Taxa do PayPal
            'processed_at': datetime.now().isoformat()
        }
        
        print(f"✅ Pagamento aprovado via PayPal: {transaction_id}")
        return result
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        print(f"🔄 Estornando pagamento via PayPal: {transaction_id}")
        
        # Simulação do estorno no PayPal
        refund_id = f"paypal_refund_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = {
            'refund_id': refund_id,
            'status': 'refunded',
            'gateway': 'paypal',
            'amount': amount,
            'refunded_at': datetime.now().isoformat()
        }
        
        print(f"✅ Estorno processado via PayPal: {refund_id}")
        return result
    
    def _validate_paypal_card(self, card_data: Dict[str, str]) -> bool:
        """Validação específica do PayPal"""
        required_fields = ['card_number', 'expiry_date', 'cvv']
        return all(field in card_data for field in required_fields)


class PagSeguroAdapter(PaymentAdapter):
    """Adapter para o gateway PagSeguro (Brasil)"""
    
    def __init__(self, email: str, token: str):
        self.email = email
        self.token = token
        print(f"🔑 PagSeguro inicializado com email: {email}")
    
    def process_payment(self, amount: float, card_data: Dict[str, str]) -> Dict[str, Any]:
        print(f"💳 Processando pagamento via PagSeguro: R$ {amount:.2f}")
        
        # Simulação da API do PagSeguro
        transaction_id = f"pagseguro_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Validação específica do PagSeguro
        if not self._validate_pagseguro_card(card_data):
            raise ValueError("Dados do cartão inválidos para PagSeguro")
        
        # Processamento específico do PagSeguro
        result = {
            'transaction_id': transaction_id,
            'status': 'approved',
            'gateway': 'pagseguro',
            'amount': amount,
            'fee': amount * 0.0399 + 0.40,  # Taxa do PagSeguro
            'processed_at': datetime.now().isoformat()
        }
        
        print(f"✅ Pagamento aprovado via PagSeguro: {transaction_id}")
        return result
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        print(f"🔄 Estornando pagamento via PagSeguro: {transaction_id}")
        
        # Simulação do estorno no PagSeguro
        refund_id = f"pagseguro_refund_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = {
            'refund_id': refund_id,
            'status': 'refunded',
            'gateway': 'pagseguro',
            'amount': amount,
            'refunded_at': datetime.now().isoformat()
        }
        
        print(f"✅ Estorno processado via PagSeguro: {refund_id}")
        return result
    
    def _validate_pagseguro_card(self, card_data: Dict[str, str]) -> bool:
        """Validação específica do PagSeguro"""
        required_fields = ['numero', 'mes', 'ano', 'codigo_seguranca']
        return all(field in card_data for field in required_fields)


class PaymentProcessor:
    """Cliente do padrão Adapter - Processa pagamentos usando qualquer gateway"""
    
    def __init__(self, payment_adapter: PaymentAdapter):
        self.payment_adapter = payment_adapter
        self.transactions = []
    
    def process_payment(self, amount: float, card_data: Dict[str, str]) -> Dict[str, Any]:
        """Processa um pagamento usando o adapter configurado"""
        print(f"🔄 Iniciando processamento de pagamento...")
        
        try:
            result = self.payment_adapter.process_payment(amount, card_data)
            self.transactions.append(result)
            
            print(f"💰 Pagamento processado com sucesso!")
            print(f"📊 Taxa cobrada: R$ {result['fee']:.2f}")
            print(f"🆔 ID da transação: {result['transaction_id']}\n")
            
            return result
            
        except Exception as e:
            print(f"❌ Erro ao processar pagamento: {e}")
            raise
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Estorna um pagamento usando o adapter configurado"""
        print(f"🔄 Iniciando estorno de pagamento...")
        
        try:
            result = self.payment_adapter.refund_payment(transaction_id, amount)
            
            print(f"💰 Estorno processado com sucesso!")
            print(f"🆔 ID do estorno: {result['refund_id']}\n")
            
            return result
            
        except Exception as e:
            print(f"❌ Erro ao estornar pagamento: {e}")
            raise
    
    def get_transactions(self) -> list:
        """Retorna histórico de transações"""
        return self.transactions


def demonstrar_pagamentos_stripe():
    """Demonstra processamento de pagamentos com Stripe"""
    print("=== DEMONSTRAÇÃO COM STRIPE ===")
    
    # Configurar adapter do Stripe
    stripe_adapter = StripeAdapter("sk_test_123456789")
    processor = PaymentProcessor(stripe_adapter)
    
    # Dados do cartão para Stripe
    card_data = {
        'number': '4242424242424242',
        'exp_month': '12',
        'exp_year': '2025',
        'cvc': '123'
    }
    
    # Processar pagamento
    result = processor.process_payment(150.00, card_data)
    
    # Estornar pagamento
    processor.refund_payment(result['transaction_id'], 50.00)
    
    return processor


def demonstrar_pagamentos_paypal():
    """Demonstra processamento de pagamentos com PayPal"""
    print("=== DEMONSTRAÇÃO COM PAYPAL ===")
    
    # Configurar adapter do PayPal
    paypal_adapter = PayPalAdapter("client_id_123", "client_secret_456")
    processor = PaymentProcessor(paypal_adapter)
    
    # Dados do cartão para PayPal
    card_data = {
        'card_number': '4111111111111111',
        'expiry_date': '12/25',
        'cvv': '123'
    }
    
    # Processar pagamento
    result = processor.process_payment(200.00, card_data)
    
    # Estornar pagamento
    processor.refund_payment(result['transaction_id'], 100.00)
    
    return processor


def demonstrar_pagamentos_pagseguro():
    """Demonstra processamento de pagamentos com PagSeguro"""
    print("=== DEMONSTRAÇÃO COM PAGSEGURO ===")
    
    # Configurar adapter do PagSeguro
    pagseguro_adapter = PagSeguroAdapter("vendedor@empresa.com", "token_123")
    processor = PaymentProcessor(pagseguro_adapter)
    
    # Dados do cartão para PagSeguro
    card_data = {
        'numero': '4111111111111111',
        'mes': '12',
        'ano': '25',
        'codigo_seguranca': '123'
    }
    
    # Processar pagamento
    result = processor.process_payment(300.00, card_data)
    
    # Estornar pagamento
    processor.refund_payment(result['transaction_id'], 150.00)
    
    return processor


def demonstrar_flexibilidade():
    """Demonstra flexibilidade do padrão Adapter"""
    print("=== DEMONSTRAÇÃO DE FLEXIBILIDADE ===")
    
    # Configuração dinâmica de gateways
    gateways = {
        'stripe': StripeAdapter("sk_test_123456789"),
        'paypal': PayPalAdapter("client_id_123", "client_secret_456"),
        'pagseguro': PagSeguroAdapter("vendedor@empresa.com", "token_123")
    }
    
    # Selecionar gateway dinamicamente
    selected_gateway = gateways['stripe']  # Pode vir de configuração
    processor = PaymentProcessor(selected_gateway)
    
    # Dados do cartão
    card_data = {
        'number': '4242424242424242',
        'exp_month': '12',
        'exp_year': '2025',
        'cvc': '123'
    }
    
    # Processar pagamento
    result = processor.process_payment(500.00, card_data)
    
    print(f"✅ Gateway configurado dinamicamente: {result['gateway']}")
    print(f"✅ Fácil troca de implementação sem modificar código!")
    
    return processor


def demonstrar_comparacao_taxas():
    """Demonstra comparação de taxas entre gateways"""
    print("=== COMPARAÇÃO DE TAXAS ===")
    
    amount = 1000.00
    
    # Testar com diferentes gateways
    gateways = [
        ("Stripe", StripeAdapter("sk_test_123456789")),
        ("PayPal", PayPalAdapter("client_id_123", "client_secret_456")),
        ("PagSeguro", PagSeguroAdapter("vendedor@empresa.com", "token_123"))
    ]
    
    card_data = {
        'number': '4242424242424242',
        'exp_month': '12',
        'exp_year': '2025',
        'cvc': '123'
    }
    
    print(f"💰 Comparando taxas para pagamento de R$ {amount:.2f}:\n")
    
    for gateway_name, adapter in gateways:
        processor = PaymentProcessor(adapter)
        
        try:
            result = processor.process_payment(amount, card_data)
            fee = result['fee']
            fee_percentage = (fee / amount) * 100
            
            print(f"🔹 {gateway_name}:")
            print(f"   Taxa: R$ {fee:.2f} ({fee_percentage:.2f}%)")
            print(f"   Valor líquido: R$ {amount - fee:.2f}\n")
            
        except Exception as e:
            print(f"❌ Erro com {gateway_name}: {e}\n")


def main():
    """Função principal que executa todas as demonstrações"""
    print("🎯 DEMONSTRAÇÃO DO PADRÃO ADAPTER EM PYTHON")
    print("Sistema de Pagamentos com Múltiplos Gateways\n")
    
    # Demonstrações
    demonstrar_pagamentos_stripe()
    demonstrar_pagamentos_paypal()
    demonstrar_pagamentos_pagseguro()
    demonstrar_flexibilidade()
    demonstrar_comparacao_taxas()
    
    print("=== DEMONSTRAÇÃO CONCLUÍDA ===")
    print("✅ O padrão Adapter permite integrar diferentes gateways!")
    print("✅ Cada gateway mantém sua interface específica!")
    print("✅ O código cliente permanece inalterado!")
    print("✅ Fácil troca de gateways via configuração!")


if __name__ == "__main__":
    main()








