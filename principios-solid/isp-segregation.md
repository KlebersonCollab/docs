# Segregação de Interfaces: Soluções Práticas

## Informações Básicas
- **ID do Documento**: ISP-003
- **Nome**: Segregação de Interfaces - Soluções Práticas
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

Este documento apresenta soluções práticas para implementar a segregação de interfaces corretamente, baseado no exemplo do sistema de pagamentos da transcrição. Mostra como transformar interfaces infladas em interfaces coesas e bem definidas.

## 1. Análise do Problema Original

### Interface Inflada
```typescript
// ❌ Interface inflada com múltiplas responsabilidades
interface PaymentMethod {
  pay(): void;
  generateQRCode(): void;
  generateDocument(): void;
}
```

### Implementações Problemáticas
```typescript
// ❌ Implementações forçadas com código morto
class CreditCardPayment implements PaymentMethod {
  pay(): void {
    // Lógica de pagamento
  }
  
  generateQRCode(): void {
    throw new Error('Cartão não gera QR Code');
  }
  
  generateDocument(): void {
    throw new Error('Cartão não gera documento');
  }
}

class PixPayment implements PaymentMethod {
  pay(): void {
    // Lógica de pagamento
  }
  
  generateQRCode(): void {
    // Lógica de QR Code
  }
  
  generateDocument(): void {
    throw new Error('PIX não gera documento');
  }
}

class BoletoPayment implements PaymentMethod {
  pay(): void {
    // Lógica de pagamento
  }
  
  generateQRCode(): void {
    throw new Error('Boleto não gera QR Code');
  }
  
  generateDocument(): void {
    // Lógica de documento
  }
}
```

## 2. Solução: Segregação de Interfaces

### Passo 1: Identificar Responsabilidades

#### Análise das Responsabilidades
- **Pagamento**: Todos os métodos de pagamento precisam
- **Geração de QR Code**: Apenas PIX precisa
- **Geração de Documento**: Apenas Boleto precisa

#### Interfaces Segregadas
```typescript
// ✅ Interface base para pagamentos
interface PaymentMethod {
  pay(): void;
}

// ✅ Interface para geração de QR Code
interface QRCodeGenerable {
  generateQRCode(): void;
}

// ✅ Interface para geração de documentos
interface DocumentGenerable {
  generateDocument(): void;
}
```

### Passo 2: Implementações Específicas

#### Implementações Coesas
```typescript
// ✅ Implementação coesa - apenas pagamento
class CreditCardPayment implements PaymentMethod {
  pay(): void {
    // Apenas lógica de pagamento
  }
}

// ✅ Implementação com múltiplas responsabilidades específicas
class PixPayment implements PaymentMethod, QRCodeGenerable {
  pay(): void {
    // Lógica de pagamento
  }
  
  generateQRCode(): void {
    // Lógica de QR Code
  }
}

// ✅ Implementação com geração de documento
class BoletoPayment implements PaymentMethod, DocumentGenerable {
  pay(): void {
    // Lógica de pagamento
  }
  
  generateDocument(): void {
    // Lógica de documento
  }
}
```

### Passo 3: Código Cliente Específico

#### Serviços Especializados
```typescript
// ✅ Cliente que precisa apenas de pagamento
class PaymentProcessor {
  processPayment(method: PaymentMethod) {
    method.pay();
  }
}

// ✅ Cliente que precisa de QR Code
class QRCodeService {
  generateQRCode(generator: QRCodeGenerable) {
    generator.generateQRCode();
  }
}

// ✅ Cliente que precisa de documento
class DocumentService {
  generateDocument(generator: DocumentGenerable) {
    generator.generateDocument();
  }
}
```

## 3. Padrões de Segregação

### 3.1. Segregação por Responsabilidade

#### Exemplo: Sistema de Notificações
```typescript
// ✅ Interfaces segregadas por responsabilidade
interface EmailNotifiable {
  sendEmail(): void;
}

interface SMSNotifiable {
  sendSMS(): void;
}

interface PushNotifiable {
  sendPushNotification(): void;
}

// ✅ Implementações específicas
class User implements EmailNotifiable, SMSNotifiable {
  sendEmail(): void { /* implementação */ }
  sendSMS(): void { /* implementação */ }
}

class Admin implements EmailNotifiable, PushNotifiable {
  sendEmail(): void { /* implementação */ }
  sendPushNotification(): void { /* implementação */ }
}
```

### 3.2. Segregação por Funcionalidade

#### Exemplo: Sistema de Arquivos
```typescript
// ✅ Interfaces segregadas por funcionalidade
interface Readable {
  read(): string;
}

interface Writable {
  write(content: string): void;
}

interface Deletable {
  delete(): void;
}

interface Executable {
  execute(): void;
}

// ✅ Implementações específicas
class TextFile implements Readable, Writable, Deletable {
  read(): string { /* implementação */ }
  write(content: string): void { /* implementação */ }
  delete(): void { /* implementação */ }
}

class ScriptFile implements Readable, Writable, Deletable, Executable {
  read(): string { /* implementação */ }
  write(content: string): void { /* implementação */ }
  delete(): void { /* implementação */ }
  execute(): void { /* implementação */ }
}
```

### 3.3. Segregação por Domínio

#### Exemplo: Sistema de E-commerce
```typescript
// ✅ Interfaces segregadas por domínio
interface Product {
  getName(): string;
  getPrice(): number;
}

interface Shippable {
  calculateShipping(): number;
  getShippingAddress(): string;
}

interface Taxable {
  calculateTax(): number;
}

interface Discountable {
  applyDiscount(percentage: number): void;
}

// ✅ Implementações específicas
class PhysicalProduct implements Product, Shippable, Taxable {
  getName(): string { /* implementação */ }
  getPrice(): number { /* implementação */ }
  calculateShipping(): number { /* implementação */ }
  getShippingAddress(): string { /* implementação */ }
  calculateTax(): number { /* implementação */ }
}

class DigitalProduct implements Product, Taxable, Discountable {
  getName(): string { /* implementação */ }
  getPrice(): number { /* implementação */ }
  calculateTax(): number { /* implementação */ }
  applyDiscount(percentage: number): void { /* implementação */ }
}
```

## 4. Composição de Interfaces

### 4.1. Múltiplas Implementações

#### Exemplo: Sistema de Pagamentos Avançado
```typescript
// ✅ Interfaces específicas
interface PaymentMethod {
  pay(): void;
}

interface QRCodeGenerable {
  generateQRCode(): void;
}

interface DocumentGenerable {
  generateDocument(): void;
}

interface EmailNotifiable {
  sendEmail(): void;
}

interface Refundable {
  processRefund(): void;
}

// ✅ Implementações com múltiplas responsabilidades
class PixPayment implements PaymentMethod, QRCodeGenerable, Refundable {
  pay(): void { /* implementação */ }
  generateQRCode(): void { /* implementação */ }
  processRefund(): void { /* implementação */ }
}

class BoletoPayment implements PaymentMethod, DocumentGenerable, EmailNotifiable {
  pay(): void { /* implementação */ }
  generateDocument(): void { /* implementação */ }
  sendEmail(): void { /* implementação */ }
}

class CreditCardPayment implements PaymentMethod, Refundable {
  pay(): void { /* implementação */ }
  processRefund(): void { /* implementação */ }
}
```

### 4.2. Injeção de Dependência

#### Exemplo: Serviço de Pagamento Flexível
```typescript
// ✅ Serviço com injeção de dependência
class PaymentService {
  constructor(
    private paymentMethod: PaymentMethod,
    private qrCodeGenerator?: QRCodeGenerable,
    private documentGenerator?: DocumentGenerable,
    private emailNotifier?: EmailNotifiable
  ) {}
  
  processPayment() {
    // Processar pagamento
    this.paymentMethod.pay();
    
    // Gerar QR Code se disponível
    if (this.qrCodeGenerator) {
      this.qrCodeGenerator.generateQRCode();
    }
    
    // Gerar documento se disponível
    if (this.documentGenerator) {
      this.documentGenerator.generateDocument();
    }
    
    // Enviar email se disponível
    if (this.emailNotifier) {
      this.emailNotifier.sendEmail();
    }
  }
}
```

## 5. Padrões de Design Aplicados

### 5.1. Strategy Pattern

#### Exemplo: Processamento de Dados
```typescript
// ✅ Interfaces segregadas para Strategy Pattern
interface DataProcessor {
  process(data: any): any;
}

interface DataValidator {
  validate(data: any): boolean;
}

interface DataTransformer {
  transform(data: any): any;
}

interface DataPersister {
  save(data: any): void;
}

// ✅ Implementações específicas
class CSVProcessor implements DataProcessor, DataValidator {
  process(data: any): any { /* implementação */ }
  validate(data: any): boolean { /* implementação */ }
}

class JSONProcessor implements DataProcessor, DataTransformer, DataPersister {
  process(data: any): any { /* implementação */ }
  transform(data: any): any { /* implementação */ }
  save(data: any): void { /* implementação */ }
}
```

### 5.2. Adapter Pattern

#### Exemplo: Integração com APIs
```typescript
// ✅ Interfaces segregadas para Adapter Pattern
interface PaymentGateway {
  processPayment(amount: number): boolean;
}

interface QRCodeGenerator {
  generateQRCode(data: string): string;
}

interface DocumentGenerator {
  generateDocument(data: any): string;
}

// ✅ Implementações específicas
class StripeAdapter implements PaymentGateway {
  processPayment(amount: number): boolean { /* implementação */ }
}

class PayPalAdapter implements PaymentGateway {
  processPayment(amount: number): boolean { /* implementação */ }
}

class QRCodeService implements QRCodeGenerator {
  generateQRCode(data: string): string { /* implementação */ }
}

class PDFService implements DocumentGenerator {
  generateDocument(data: any): string { /* implementação */ }
}
```

## 6. Testes de Segregação

### 6.1. Testes de Interface

#### Exemplo: Testes de Pagamento
```typescript
describe('Payment Interface Segregation', () => {
  describe('PaymentMethod', () => {
    it('should process payment', () => {
      const payment = new CreditCardPayment();
      expect(() => payment.pay()).not.toThrow();
    });
  });
  
  describe('QRCodeGenerable', () => {
    it('should generate QR code', () => {
      const generator = new PixPayment();
      expect(() => generator.generateQRCode()).not.toThrow();
    });
  });
  
  describe('DocumentGenerable', () => {
    it('should generate document', () => {
      const generator = new BoletoPayment();
      expect(() => generator.generateDocument()).not.toThrow();
    });
  });
});
```

### 6.2. Testes de Composição

#### Exemplo: Testes de Serviço
```typescript
describe('Payment Service Composition', () => {
  it('should work with PIX payment', () => {
    const pixPayment = new PixPayment();
    const service = new PaymentService(pixPayment, pixPayment);
    
    expect(() => service.processPayment()).not.toThrow();
  });
  
  it('should work with Boleto payment', () => {
    const boletoPayment = new BoletoPayment();
    const service = new PaymentService(boletoPayment, undefined, boletoPayment);
    
    expect(() => service.processPayment()).not.toThrow();
  });
});
```

## 7. Refatoração Passo a Passo

### 7.1. Identificação de Violações

#### Análise de Interface
```typescript
// ❌ Interface problemática
interface LargeInterface {
  method1(): void;
  method2(): void;
  method3(): void;
  method4(): void;
  method5(): void;
}
```

#### Análise de Implementações
```typescript
// ❌ Implementações com código morto
class Implementation1 implements LargeInterface {
  method1(): void { /* implementação */ }
  method2(): void { /* implementação */ }
  method3(): void { throw new Error('Não implementado'); }
  method4(): void { throw new Error('Não implementado'); }
  method5(): void { throw new Error('Não implementado'); }
}
```

### 7.2. Segregação Gradual

#### Passo 1: Identificar Responsabilidades
```typescript
// ✅ Identificar responsabilidades
interface Responsibility1 {
  method1(): void;
  method2(): void;
}

interface Responsibility2 {
  method3(): void;
  method4(): void;
}

interface Responsibility3 {
  method5(): void;
}
```

#### Passo 2: Implementações Específicas
```typescript
// ✅ Implementações específicas
class Implementation1 implements Responsibility1 {
  method1(): void { /* implementação */ }
  method2(): void { /* implementação */ }
}

class Implementation2 implements Responsibility1, Responsibility2 {
  method1(): void { /* implementação */ }
  method2(): void { /* implementação */ }
  method3(): void { /* implementação */ }
  method4(): void { /* implementação */ }
}
```

#### Passo 3: Código Cliente Atualizado
```typescript
// ✅ Código cliente atualizado
class Client {
  processResponsibility1(processor: Responsibility1) {
    processor.method1();
    processor.method2();
  }
  
  processResponsibility2(processor: Responsibility2) {
    processor.method3();
    processor.method4();
  }
}
```

## 8. Benefícios da Segregação

### 8.1. Melhoria na Coesão
- **Classes mais coerentes**: Fazem apenas uma coisa bem feita
- **Responsabilidade única**: Cada interface tem uma responsabilidade
- **Código mais limpo**: Menos responsabilidades por classe

### 8.2. Redução do Acoplamento
- **Dependências mínimas**: Classes dependem apenas do que precisam
- **Facilita testes**: Mocks e stubs mais simples
- **Manutenção mais fácil**: Mudanças isoladas em interfaces específicas

### 8.3. Melhoria na Reutilização
- **Classes enxutas**: Mais fáceis de reutilizar
- **Interfaces específicas**: Podem ser combinadas conforme necessário
- **Flexibilidade**: Diferentes combinações de interfaces

### 8.4. Facilita Manutenção
- **Ciclo de vida saudável**: Software mais fácil de manter
- **Extensibilidade**: Novas funcionalidades sem quebrar código existente
- **Redução de custos**: Menos tempo gasto em manutenção

## 9. Conclusão

A segregação de interfaces é fundamental para criar sistemas bem arquitetados e maintíveis. Ela permite:

### Pontos-Chave
- **Interfaces enxutas**: Uma responsabilidade por interface
- **Implementações coerentes**: Classes fazem apenas o que precisam
- **Composição flexível**: Múltiplas interfaces podem ser combinadas
- **Manutenção facilitada**: Mudanças isoladas em interfaces específicas

### Próximos Passos
- [Entender abstração correta](isp-abstraction.md)
- [Implementar boas práticas](isp-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
