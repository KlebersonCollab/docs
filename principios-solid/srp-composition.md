# Composição de Objetos e Facade Pattern no SRP

## Informações Básicas
- **ID do Documento**: SRP-004
- **Nome**: Composição de Objetos e Facade Pattern no SRP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

Este documento apresenta como usar composição de objetos e o padrão Facade para implementar o Princípio da Responsabilidade Única (SRP) corretamente, criando sistemas mais coesos e maintíveis.

## 1. Composição de Objetos

### 1.1. Conceito de Composição

#### Definição
**Composição** é o processo de combinar objetos para criar funcionalidades mais complexas, mantendo cada objeto com sua responsabilidade específica.

#### Benefícios
- **Reutilização**: Objetos podem ser combinados de diferentes formas
- **Flexibilidade**: Fácil alteração de implementações
- **Testabilidade**: Cada objeto pode ser testado isoladamente
- **Manutenibilidade**: Mudanças isoladas em objetos específicos

### 1.2. Exemplo Prático: Sistema de Pedidos

#### Problema Original
```typescript
// ❌ Classe com múltiplas responsabilidades
class OrderProcessorService {
  processOrder(order: Order): void {
    this.checkInventory(order);
    this.calculateTotal(order);
    this.processPayment(order);
  }
  
  private checkInventory(order: Order): void {
    // Lógica de inventário
  }
  
  private calculateTotal(order: Order): void {
    // Lógica de cálculo
  }
  
  private processPayment(order: Order): void {
    // Lógica de pagamento
  }
}
```

#### Solução com Composição
```typescript
// ✅ Classes com responsabilidades específicas
class InventoryChecker {
  check(order: Order): void {
    // Lógica específica para checar inventário
  }
}

class OrderCalculator {
  calculate(order: Order): void {
    // Lógica específica para calcular total
  }
}

class PaymentProcessor {
  process(order: Order): void {
    // Lógica específica para processar pagamento
  }
}

// ✅ Classe que compõe os objetos
class OrderProcessorService {
  constructor(
    private inventoryChecker: InventoryChecker,
    private orderCalculator: OrderCalculator,
    private paymentProcessor: PaymentProcessor
  ) {}
  
  processOrder(order: Order): void {
    this.inventoryChecker.check(order);
    this.orderCalculator.calculate(order);
    this.paymentProcessor.process(order);
  }
}
```

## 2. Padrão Facade

### 2.1. Conceito do Facade Pattern

#### Definição
**Facade Pattern** é um padrão estrutural que fornece uma interface simplificada para um subsistema complexo, escondendo a complexidade interna.

#### Benefícios
- **Interface simplificada**: Cliente não precisa conhecer detalhes internos
- **Encapsulamento**: Lógica complexa escondida
- **Flexibilidade**: Pode ser alterado internamente sem afetar cliente
- **Manutenibilidade**: Mudanças internas não afetam código cliente

### 2.2. Implementação do Facade

#### Exemplo: Facade para Processamento de Pedidos
```typescript
// ✅ Facade que simplifica a interface
class OrderProcessorFacade {
  constructor(
    private inventoryChecker: InventoryChecker,
    private orderCalculator: OrderCalculator,
    private paymentProcessor: PaymentProcessor
  ) {}
  
  processOrder(order: Order): void {
    // Orquestra o processo completo
    this.inventoryChecker.check(order);
    this.orderCalculator.calculate(order);
    this.paymentProcessor.process(order);
  }
}
```

#### Código Cliente Simplificado
```typescript
// ✅ Código cliente simplificado
class OrderCommand {
  execute(): void {
    const order = new Order("123", 100.0);
    
    // Criação das dependências
    const inventoryChecker = new InventoryChecker();
    const orderCalculator = new OrderCalculator();
    const paymentProcessor = new PaymentProcessor();
    
    // Criação do facade
    const orderProcessor = new OrderProcessorFacade(
      inventoryChecker,
      orderCalculator,
      paymentProcessor
    );
    
    // Processamento simplificado
    orderProcessor.processOrder(order);
  }
}
```

## 3. Injeção de Dependências

### 3.1. Conceito de Injeção de Dependências

#### Definição
**Injeção de Dependências** é um padrão onde as dependências de um objeto são fornecidas externamente, ao invés de serem criadas internamente.

#### Benefícios
- **Testabilidade**: Fácil criação de mocks
- **Flexibilidade**: Diferentes implementações podem ser injetadas
- **Manutenibilidade**: Dependências podem ser alteradas sem modificar código
- **Reutilização**: Objetos podem ser reutilizados em diferentes contextos

### 3.2. Implementação com Injeção de Dependências

#### Exemplo: Sistema de Pagamentos
```typescript
// ✅ Interfaces para abstração
interface PaymentGateway {
  processPayment(amount: number): boolean;
}

interface EmailService {
  sendEmail(to: string, subject: string, body: string): void;
}

interface LogService {
  log(message: string): void;
}

// ✅ Implementações específicas
class StripePaymentGateway implements PaymentGateway {
  processPayment(amount: number): boolean {
    // Lógica específica do Stripe
    return true;
  }
}

class PayPalPaymentGateway implements PaymentGateway {
  processPayment(amount: number): boolean {
    // Lógica específica do PayPal
    return true;
  }
}

class SMTPEmailService implements EmailService {
  sendEmail(to: string, subject: string, body: string): void {
    // Lógica específica do SMTP
  }
}

class ConsoleLogService implements LogService {
  log(message: string): void {
    console.log(message);
  }
}

// ✅ Classe que usa injeção de dependências
class OrderProcessorService {
  constructor(
    private paymentGateway: PaymentGateway,
    private emailService: EmailService,
    private logService: LogService
  ) {}
  
  processOrder(order: Order): void {
    this.logService.log(`Processando pedido: ${order.id}`);
    
    const success = this.paymentGateway.processPayment(order.amount);
    
    if (success) {
      this.emailService.sendEmail(
        order.customerEmail,
        'Pedido processado',
        'Seu pedido foi processado com sucesso'
      );
    }
  }
}
```

### 3.3. Container de Injeção de Dependências

#### Exemplo: Configuração de Dependências
```typescript
// ✅ Container de injeção de dependências
class DIContainer {
  private services = new Map<string, any>();
  
  register<T>(name: string, factory: () => T): void {
    this.services.set(name, factory);
  }
  
  resolve<T>(name: string): T {
    const factory = this.services.get(name);
    if (!factory) {
      throw new Error(`Service ${name} not found`);
    }
    return factory();
  }
}

// ✅ Configuração das dependências
const container = new DIContainer();

container.register('PaymentGateway', () => new StripePaymentGateway());
container.register('EmailService', () => new SMTPEmailService());
container.register('LogService', () => new ConsoleLogService());

// ✅ Resolução das dependências
const paymentGateway = container.resolve<PaymentGateway>('PaymentGateway');
const emailService = container.resolve<EmailService>('EmailService');
const logService = container.resolve<LogService>('LogService');

const orderProcessor = new OrderProcessorService(
  paymentGateway,
  emailService,
  logService
);
```

## 4. Padrões de Composição

### 4.1. Strategy Pattern

#### Exemplo: Diferentes Estratégias de Cálculo
```typescript
// ✅ Interface para estratégias de cálculo
interface CalculationStrategy {
  calculate(order: Order): number;
}

// ✅ Estratégia para cálculo básico
class BasicCalculationStrategy implements CalculationStrategy {
  calculate(order: Order): number {
    let total = 0;
    for (const item of order.items) {
      total += item.price * item.quantity;
    }
    return total;
  }
}

// ✅ Estratégia para cálculo com impostos
class TaxCalculationStrategy implements CalculationStrategy {
  calculate(order: Order): number {
    let total = 0;
    for (const item of order.items) {
      total += item.price * item.quantity;
    }
    return total * 1.1; // 10% de imposto
  }
}

// ✅ Estratégia para cálculo com desconto
class DiscountCalculationStrategy implements CalculationStrategy {
  calculate(order: Order): number {
    let total = 0;
    for (const item of order.items) {
      total += item.price * item.quantity;
    }
    return total > 100 ? total * 0.9 : total;
  }
}

// ✅ Classe que usa estratégias
class OrderCalculator {
  constructor(private strategy: CalculationStrategy) {}
  
  calculate(order: Order): number {
    return this.strategy.calculate(order);
  }
}
```

### 4.2. Command Pattern

#### Exemplo: Comandos de Processamento
```typescript
// ✅ Interface para comandos
interface Command {
  execute(): void;
}

// ✅ Comando para verificar inventário
class CheckInventoryCommand implements Command {
  constructor(private order: Order, private inventoryChecker: InventoryChecker) {}
  
  execute(): void {
    this.inventoryChecker.check(this.order);
  }
}

// ✅ Comando para calcular total
class CalculateTotalCommand implements Command {
  constructor(private order: Order, private calculator: OrderCalculator) {}
  
  execute(): void {
    this.calculator.calculate(this.order);
  }
}

// ✅ Comando para processar pagamento
class ProcessPaymentCommand implements Command {
  constructor(private order: Order, private paymentProcessor: PaymentProcessor) {}
  
  execute(): void {
    this.paymentProcessor.process(this.order);
  }
}

// ✅ Classe que executa comandos
class OrderProcessorService {
  constructor(private commands: Command[]) {}
  
  processOrder(): void {
    for (const command of this.commands) {
      command.execute();
    }
  }
}
```

### 4.3. Observer Pattern

#### Exemplo: Notificações de Pedidos
```typescript
// ✅ Interface para observadores
interface OrderObserver {
  update(order: Order): void;
}

// ✅ Observador para email
class EmailNotificationObserver implements OrderObserver {
  constructor(private emailService: EmailService) {}
  
  update(order: Order): void {
    this.emailService.sendEmail(
      order.customerEmail,
      'Pedido processado',
      'Seu pedido foi processado com sucesso'
    );
  }
}

// ✅ Observador para log
class LogObserver implements OrderObserver {
  constructor(private logService: LogService) {}
  
  update(order: Order): void {
    this.logService.log(`Pedido ${order.id} processado`);
  }
}

// ✅ Classe que notifica observadores
class OrderProcessorService {
  private observers: OrderObserver[] = [];
  
  addObserver(observer: OrderObserver): void {
    this.observers.push(observer);
  }
  
  processOrder(order: Order): void {
    // Lógica de processamento
    
    // Notifica observadores
    for (const observer of this.observers) {
      observer.update(order);
    }
  }
}
```

## 5. Testes com Composição

### 5.1. Testes Unitários

#### Testes para Classes Específicas
```typescript
describe('InventoryChecker', () => {
  it('should check inventory successfully', () => {
    const checker = new InventoryChecker();
    const order = new Order();
    
    expect(() => checker.check(order)).not.toThrow();
  });
});

describe('OrderCalculator', () => {
  it('should calculate total correctly', () => {
    const calculator = new OrderCalculator();
    const order = new Order();
    
    const total = calculator.calculate(order);
    expect(total).toBeGreaterThan(0);
  });
});

describe('PaymentProcessor', () => {
  it('should process payment successfully', () => {
    const processor = new PaymentProcessor();
    const order = new Order();
    
    expect(() => processor.process(order)).not.toThrow();
  });
});
```

### 5.2. Testes de Integração

#### Testes para Facade
```typescript
describe('OrderProcessorFacade', () => {
  it('should process order successfully', () => {
    const facade = new OrderProcessorFacade(
      new InventoryChecker(),
      new OrderCalculator(),
      new PaymentProcessor()
    );
    
    const order = new Order();
    expect(() => facade.processOrder(order)).not.toThrow();
  });
});
```

### 5.3. Testes com Mocks

#### Testes com Dependências Mockadas
```typescript
describe('OrderProcessorService', () => {
  it('should process order with mocked dependencies', () => {
    const mockInventoryChecker = {
      check: jest.fn()
    };
    
    const mockOrderCalculator = {
      calculate: jest.fn()
    };
    
    const mockPaymentProcessor = {
      process: jest.fn()
    };
    
    const service = new OrderProcessorService(
      mockInventoryChecker,
      mockOrderCalculator,
      mockPaymentProcessor
    );
    
    const order = new Order();
    service.processOrder(order);
    
    expect(mockInventoryChecker.check).toHaveBeenCalledWith(order);
    expect(mockOrderCalculator.calculate).toHaveBeenCalledWith(order);
    expect(mockPaymentProcessor.process).toHaveBeenCalledWith(order);
  });
});
```

## 6. Benefícios da Composição

### 6.1. Manutenibilidade
- **Mudanças isoladas**: Alterações em uma responsabilidade não afetam outras
- **Código mais limpo**: Classes menores e mais focadas
- **Facilita testes**: Testes mais específicos e simples

### 6.2. Reutilização
- **Classes específicas**: Podem ser reutilizadas em diferentes contextos
- **Composição flexível**: Diferentes combinações de responsabilidades
- **Eliminação de duplicação**: Lógica centralizada em classes específicas

### 6.3. Testabilidade
- **Mocks específicos**: Fácil criação de mocks para cada responsabilidade
- **Testes unitários**: Testes focados em uma responsabilidade
- **Isolamento**: Testes não dependem de outras responsabilidades

### 6.4. Extensibilidade
- **Novas funcionalidades**: Sem modificar código existente
- **Composição**: Diferentes combinações de responsabilidades
- **Flexibilidade**: Fácil alteração de implementações

## 7. Conclusão

A composição de objetos e o padrão Facade são fundamentais para implementar o SRP corretamente. Eles permitem:

### Pontos-Chave
- **Composição de objetos**: Combina responsabilidades específicas
- **Facade Pattern**: Simplifica interfaces complexas
- **Injeção de dependências**: Facilita testes e manutenção
- **Padrões de design**: Strategy, Command, Observer

### Próximos Passos
- [Aplicar boas práticas](./srp-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
