# Guia de Boas Práticas para o Princípio da Segregação de Interfaces

## Informações Básicas
- **ID do Documento**: ISP-005
- **Nome**: Boas Práticas para ISP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

Este guia apresenta as melhores práticas para implementar o Princípio da Segregação de Interfaces (ISP) corretamente, evitando violações comuns e criando sistemas mais robustos e maintíveis.

## 1. Design de Interfaces Corretas

### 1.1. Análise de Responsabilidades

#### Identificação de Responsabilidades
```typescript
// ✅ Identificar responsabilidades específicas
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
```

#### Implementações Específicas
```typescript
// ✅ Implementações que fazem sentido
class PixPayment implements PaymentMethod, QRCodeGenerable {
  pay(): void { /* implementação */ }
  generateQRCode(): void { /* implementação */ }
}

class BoletoPayment implements PaymentMethod, DocumentGenerable, EmailNotifiable {
  pay(): void { /* implementação */ }
  generateDocument(): void { /* implementação */ }
  sendEmail(): void { /* implementação */ }
}
```

### 1.2. Tamanho Adequado de Interfaces

#### Interfaces Pequenas e Focadas
```typescript
// ✅ Interface pequena e focada
interface EmailNotifiable {
  sendEmail(): void;
}

interface SMSNotifiable {
  sendSMS(): void;
}

interface PushNotifiable {
  sendPushNotification(): void;
}
```

#### Evitar Interfaces Infladas
```typescript
// ❌ Interface inflada
interface LargeInterface {
  method1(): void;
  method2(): void;
  method3(): void;
  method4(): void;
  method5(): void;
  method6(): void;
  method7(): void;
  method8(): void;
}
```

### 1.3. Métodos Relacionados

#### Agrupar Métodos que Fazem Sentido
```typescript
// ✅ Métodos relacionados agrupados
interface FileOperations {
  read(): string;
  write(content: string): void;
  delete(): void;
}

interface DataValidation {
  validate(data: any): boolean;
  sanitize(data: any): any;
}
```

## 2. Padrões de Segregação

### 2.1. Segregação por Responsabilidade

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

### 2.2. Segregação por Funcionalidade

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

### 2.3. Segregação por Domínio

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

## 3. Composição de Interfaces

### 3.1. Múltiplas Implementações

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

### 3.2. Injeção de Dependência

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

## 4. Padrões de Design Aplicados

### 4.1. Strategy Pattern

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

### 4.2. Adapter Pattern

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

## 5. Testes de Segregação

### 5.1. Testes de Interface

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

### 5.2. Testes de Composição

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

## 6. Detecção e Prevenção de Violações

### 6.1. Análise Estática

#### Regras de Lint
```typescript
// Configuração de lint para detectar violações
{
  "rules": {
    "no-empty-interface": "error",
    "no-unused-vars": "error",
    "prefer-interface-over-type": "error",
    "no-explicit-any": "error"
  }
}
```

#### Análise de Interfaces
```typescript
// ❌ Sinais de violação
interface LargeInterface {
  method1(): void;
  method2(): void;
  method3(): void;
  method4(): void;
  method5(): void;
  // Muitos métodos não relacionados
}
```

### 6.2. Métricas de Qualidade

#### Análise de Acoplamento
```typescript
class ISPAnalyzer {
  analyzeInterface(interfaceName: string): ISPMetrics {
    return {
      methodCount: this.countMethods(interfaceName),
      unusedMethods: this.findUnusedMethods(interfaceName),
      violationScore: this.calculateViolationScore(interfaceName)
    };
  }
  
  private countMethods(interfaceName: string): number {
    // Conta métodos na interface
    return this.sourceCode.match(/method/g)?.length || 0;
  }
  
  private findUnusedMethods(interfaceName: string): string[] {
    // Encontra métodos não utilizados
    return [];
  }
  
  private calculateViolationScore(interfaceName: string): number {
    // Calcula score de violação
    return 0;
  }
}
```

### 6.3. Testes de Segregação

#### Teste de Substituição
```typescript
// ✅ Teste que deve passar para todas as implementações
function testSubstitution(payment: PaymentMethod) {
  // Deve funcionar com qualquer implementação
  expect(() => payment.pay()).not.toThrow();
}
```

## 7. Refatoração de Código Problemático

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

### 7.2. Refatoração Passo a Passo

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

## 8. Monitoramento e Manutenção

### 8.1. Métricas de Qualidade

#### Dashboard de Métricas
```typescript
class ISPMetrics {
  calculateSegregationScore(interfaces: Interface[]): number {
    let score = 0;
    
    interfaces.forEach(interface_ => {
      // Testa se interface é específica
      const specificity = this.calculateSpecificity(interface_);
      score += specificity;
    });
    
    return score / interfaces.length;
  }
  
  calculateCouplingScore(classes: Class[]): number {
    let totalCoupling = 0;
    
    classes.forEach(cls => {
      const interfaceCount = this.countInterfaces(cls);
      const unusedMethods = this.countUnusedMethods(cls);
      totalCoupling += interfaceCount + unusedMethods;
    });
    
    return totalCoupling / classes.length;
  }
}
```

### 8.2. Alertas Automáticos

#### Sistema de Alertas
```typescript
class ISPAlertSystem {
  checkForViolations(codebase: Codebase): Alert[] {
    const alerts: Alert[] = [];
    
    // Verifica interfaces infladas
    const largeInterfaces = this.findLargeInterfaces(codebase);
    if (largeInterfaces.length > 0) {
      alerts.push({
        type: 'LARGE_INTERFACE',
        message: 'Interface com muitos métodos - possível violação do ISP',
        severity: 'HIGH',
        locations: largeInterfaces
      });
    }
    
    // Verifica implementações com exceções
    const exceptionImplementations = this.findExceptionImplementations(codebase);
    if (exceptionImplementations.length > 0) {
      alerts.push({
        type: 'EXCEPTION_IMPLEMENTATION',
        message: 'Implementações com exceções - possível violação do ISP',
        severity: 'MEDIUM',
        locations: exceptionImplementations
      });
    }
    
    return alerts;
  }
}
```

## 9. Ferramentas e Automação

### 9.1. Ferramentas de Análise

#### Análise Automática
```typescript
class ISPAnalyzer {
  analyzeCodebase(codebase: Codebase): AnalysisResult {
    return {
      violations: this.findViolations(codebase),
      suggestions: this.generateSuggestions(codebase),
      metrics: this.calculateMetrics(codebase),
      recommendations: this.generateRecommendations(codebase)
    };
  }
  
  private findViolations(codebase: Codebase): Violation[] {
    const violations: Violation[] = [];
    
    // Verifica interfaces infladas
    const largeInterfaces = this.findLargeInterfaces(codebase);
    violations.push(...largeInterfaces.map(interface_ => ({
      type: 'LARGE_INTERFACE',
      location: interface_.location,
      severity: 'HIGH',
      suggestion: 'Segregar interface em interfaces menores'
    })));
    
    return violations;
  }
}
```

### 9.2. Geração Automática de Testes

#### Gerador de Testes de Segregação
```typescript
class SegregationTestGenerator {
  generateTests(interfaceName: string, implementations: Class[]): TestSuite {
    const tests: Test[] = [];
    
    implementations.forEach(impl => {
      tests.push({
        name: `should implement ${interfaceName} correctly`,
        code: this.generateImplementationTest(interfaceName, impl),
        type: 'SEGREGATION'
      });
    });
    
    return {
      name: `${interfaceName} Segregation Tests`,
      tests: tests
    };
  }
  
  private generateImplementationTest(interfaceName: string, impl: Class): string {
    return `
      it('should implement ${interfaceName} correctly', () => {
        const instance = new ${impl.name}();
        
        // Deve implementar todos os métodos sem exceções
        expect(() => instance.method1()).not.toThrow();
        expect(() => instance.method2()).not.toThrow();
      });
    `;
  }
}
```

## 10. Checklist de Implementação

### 10.1. Checklist de Design

#### ✅ Análise de Responsabilidades
- [ ] Identificar responsabilidades específicas?
- [ ] Separar conceitos diferentes?
- [ ] Evitar generalizações desnecessárias?

#### ✅ Design de Interfaces
- [ ] Interfaces pequenas e focadas?
- [ ] Métodos relacionados agrupados?
- [ ] Tamanho adequado de interfaces?

#### ✅ Implementação
- [ ] Implementações fazem sentido?
- [ ] Eliminação de código morto?
- [ ] Substituições funcionam corretamente?

#### ✅ Testes
- [ ] Testes de segregação implementados?
- [ ] Testes de composição funcionam?
- [ ] Cobertura de testes adequada?

### 10.2. Checklist de Manutenção

#### ✅ Monitoramento
- [ ] Métricas de segregação monitoradas?
- [ ] Alertas de violação configurados?
- [ ] Análise estática configurada?
- [ ] Testes de regressão funcionando?

#### ✅ Refatoração
- [ ] Violações identificadas e corrigidas?
- [ ] Interfaces problemáticas refatoradas?
- [ ] Código cliente simplificado?
- [ ] Documentação atualizada?

## 11. Conclusão

### 11.1. Benefícios das Boas Práticas

#### Código Mais Robusto
- **Interfaces específicas**: Cada interface tem um propósito claro
- **Implementações coerentes**: Classes fazem apenas o que precisam
- **Maior confiabilidade**: Comportamento previsível

#### Facilita Manutenção
- **Mudanças isoladas**: Modificações em interfaces específicas
- **Extensibilidade**: Novas funcionalidades sem quebrar código existente
- **Testes mais simples**: Mocks e stubs mais fáceis

#### Melhora Qualidade
- **Código mais limpo**: Menos responsabilidades por classe
- **Arquitetura melhor**: Hierarquias bem desenhadas
- **Documentação clara**: Interfaces bem definidas

### 11.2. Próximos Passos

#### Implementação Imediata
1. **Audite código existente**: Identifique violações do ISP
2. **Implemente testes**: Crie testes de segregação
3. **Refatore gradualmente**: Corrija violações uma por vez
4. **Configure ferramentas**: Use análise estática e métricas

#### Melhoria Contínua
1. **Monitore métricas**: Acompanhe qualidade do código
2. **Treine equipe**: Ensine princípios e práticas
3. **Automatize verificações**: Use CI/CD para validação
4. **Documente padrões**: Crie guias e exemplos

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
