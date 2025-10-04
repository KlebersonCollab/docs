# Princípio da Responsabilidade Única (SRP)

## Informações Básicas
- **ID do Documento**: SRP-001
- **Nome**: Princípio da Responsabilidade Única
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

O Princípio da Responsabilidade Única (SRP) é o primeiro dos cinco princípios SOLID da programação orientada a objetos. É também o mais polêmico e mal compreendido de todos, pois existe uma crença errônea de que ele foi criado para gerar micro-arquivos ou classes espalhadas por todo o sistema, tornando-o extremamente granularizado.

### Definição Fundamental

> "Uma classe ou módulo deve ter apenas uma única responsabilidade e apenas um único motivo para mudar." - Robert C. Martin

### Princípio Central

**Uma classe deve ter apenas uma razão para mudar.** Este é o "pulo do gato" para identificar se uma classe está violando o SRP.

## Conceitos Centrais

### 1. Coesão e Coerência
- **Coesão**: A classe deve fazer apenas uma coisa bem feita
- **Coerência**: Todos os métodos e propriedades devem estar relacionados
- **Responsabilidade única**: Apenas um motivo para mudar

### 2. Análise de Motivos para Mudança
- **Pergunta-chave**: "Quantos motivos esta classe tem para mudar?"
- **Se mais de um**: A classe está violando o SRP
- **Se apenas um**: A classe está seguindo o SRP

### 3. Extração de Responsabilidades
- **Identificar responsabilidades**: Separar diferentes aspectos da classe
- **Criar classes específicas**: Cada responsabilidade em sua própria classe
- **Composição de objetos**: Unir as responsabilidades através de composição

## Exemplo Prático: Sistema de Pedidos

### Cenário Problemático

#### Classe com Múltiplas Responsabilidades
```typescript
class OrderProcessorService {
  processOrder(order: Order): void {
    this.checkInventory(order);
    this.calculateTotal(order);
    this.processPayment(order);
  }
  
  private checkInventory(order: Order): void {
    // Lógica para checar inventário
    // Conexão com banco de dados
    // Verificação de estoque
  }
  
  private calculateTotal(order: Order): void {
    // Lógica para calcular total
    // Aplicação de impostos
    // Aplicação de descontos
  }
  
  private processPayment(order: Order): void {
    // Lógica para processar pagamento
    // Integração com gateway de pagamento
  }
}
```

### Problemas Identificados

#### 1. Múltiplos Motivos para Mudança
- **Se a lógica de inventário mudar**: A classe precisa ser alterada
- **Se a lógica de cálculo mudar**: A classe precisa ser alterada
- **Se a lógica de pagamento mudar**: A classe precisa ser alterada

#### 2. Violação do SRP
- **Responsabilidades misturadas**: Inventário, cálculo e pagamento
- **Dificulta manutenção**: Mudanças em uma área afetam outras
- **Código duplicado**: Lógica não pode ser reutilizada

#### 3. Problemas de Reutilização
- **Lógica de inventário**: Pode ser necessária em relatórios
- **Lógica de cálculo**: Pode ser necessária em outros contextos
- **Lógica de pagamento**: Pode ser necessária em outros fluxos

## Solução: Extração de Responsabilidades

### Passo 1: Identificar Responsabilidades

#### Análise das Responsabilidades
- **Verificação de inventário**: Responsabilidade específica
- **Cálculo de total**: Responsabilidade específica
- **Processamento de pagamento**: Responsabilidade específica

#### Classes Específicas
```typescript
// ✅ Classe para verificar inventário
class InventoryChecker {
  check(order: Order): void {
    // Lógica específica para checar inventário
  }
}

// ✅ Classe para calcular total
class OrderCalculator {
  calculate(order: Order): void {
    // Lógica específica para calcular total
  }
}

// ✅ Classe para processar pagamento
class PaymentProcessor {
  process(order: Order): void {
    // Lógica específica para processar pagamento
  }
}
```

### Passo 2: Composição de Objetos

#### Classe Orquestradora
```typescript
// ✅ Classe que orquestra o processo
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

### Passo 3: Injeção de Dependências

#### Código Cliente
```typescript
// ✅ Código cliente com injeção de dependências
class OrderCommand {
  execute(): void {
    const order = new Order("123", 100.0);
    
    const inventoryChecker = new InventoryChecker();
    const orderCalculator = new OrderCalculator();
    const paymentProcessor = new PaymentProcessor();
    
    const orderProcessor = new OrderProcessorService(
      inventoryChecker,
      orderCalculator,
      paymentProcessor
    );
    
    orderProcessor.processOrder(order);
  }
}
```

## Padrão Facade

### Implementação do Facade Pattern

#### Classe Facade
```typescript
// ✅ Facade que simplifica a interface
class OrderProcessorService {
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

#### Benefícios do Facade
- **Interface simplificada**: Cliente não precisa conhecer detalhes
- **Encapsulamento**: Lógica complexa escondida
- **Flexibilidade**: Pode ser alterado internamente sem afetar cliente

## Relação com Outros Princípios SOLID

### Open/Closed Principle (OCP)
- **Extensibilidade**: Novas funcionalidades sem modificar código existente
- **Fechado para modificação**: Classes estáveis
- **Aberto para extensão**: Novas implementações possíveis

### Liskov Substitution Principle (LSP)
- **Substituições seguras**: Implementações podem ser trocadas
- **Polimorfismo funcional**: Código cliente funciona com qualquer implementação
- **Comportamento consistente**: Todas as implementações seguem o mesmo contrato

### Interface Segregation Principle (ISP)
- **Interfaces específicas**: Cada interface tem uma responsabilidade
- **Implementações coerentes**: Classes fazem apenas o que precisam
- **Eliminação de código morto**: Sem implementações desnecessárias

### Dependency Inversion Principle (DIP)
- **Dependência de abstrações**: Interfaces ao invés de implementações
- **Inversão de controle**: Dependências injetadas
- **Testabilidade**: Fácil criação de mocks e stubs

## Sinais de Violação do SRP

### 1. Múltiplos Motivos para Mudança
```typescript
// ❌ Classe com múltiplas responsabilidades
class UserService {
  createUser(user: User): void { /* lógica de criação */ }
  sendEmail(user: User): void { /* lógica de email */ }
  logActivity(user: User): void { /* lógica de log */ }
  generateReport(user: User): void { /* lógica de relatório */ }
}
```

### 2. Classes com Muitos Métodos
```typescript
// ❌ Classe com muitas responsabilidades
class DataProcessor {
  validateData(data: any): boolean { /* validação */ }
  transformData(data: any): any { /* transformação */ }
  saveData(data: any): void { /* persistência */ }
  sendNotification(data: any): void { /* notificação */ }
  generateReport(data: any): void { /* relatório */ }
}
```

### 3. Dependências Múltiplas
```typescript
// ❌ Classe com muitas dependências
class OrderService {
  constructor(
    private userRepository: UserRepository,
    private productRepository: ProductRepository,
    private paymentService: PaymentService,
    private emailService: EmailService,
    private logService: LogService,
    private reportService: ReportService
  ) {}
}
```

## Benefícios do SRP

### 1. Manutenibilidade
- **Mudanças isoladas**: Alterações em uma responsabilidade não afetam outras
- **Código mais limpo**: Classes menores e mais focadas
- **Facilita testes**: Testes mais específicos e simples

### 2. Reutilização
- **Classes específicas**: Podem ser reutilizadas em diferentes contextos
- **Composição flexível**: Diferentes combinações de responsabilidades
- **Eliminação de duplicação**: Lógica centralizada em classes específicas

### 3. Testabilidade
- **Mocks específicos**: Fácil criação de mocks para cada responsabilidade
- **Testes unitários**: Testes focados em uma responsabilidade
- **Isolamento**: Testes não dependem de outras responsabilidades

### 4. Extensibilidade
- **Novas funcionalidades**: Sem modificar código existente
- **Composição**: Diferentes combinações de responsabilidades
- **Flexibilidade**: Fácil alteração de implementações

## Padrões de Design Aplicados

### 1. Facade Pattern
```typescript
// ✅ Facade que simplifica interface complexa
class OrderProcessorService {
  constructor(
    private inventoryChecker: InventoryChecker,
    private orderCalculator: OrderCalculator,
    private paymentProcessor: PaymentProcessor
  ) {}
  
  processOrder(order: Order): void {
    // Orquestra processo complexo
  }
}
```

### 2. Strategy Pattern
```typescript
// ✅ Estratégias específicas para cada responsabilidade
interface InventoryStrategy {
  check(order: Order): void;
}

interface CalculationStrategy {
  calculate(order: Order): void;
}

interface PaymentStrategy {
  process(order: Order): void;
}
```

### 3. Dependency Injection
```typescript
// ✅ Injeção de dependências
class OrderProcessorService {
  constructor(
    private inventoryChecker: InventoryStrategy,
    private orderCalculator: CalculationStrategy,
    private paymentProcessor: PaymentStrategy
  ) {}
}
```

## Detecção de Violações

### 1. Análise de Motivos para Mudança
```typescript
// ❌ Múltiplos motivos para mudança
class OrderService {
  // Motivo 1: Lógica de inventário mudou
  checkInventory(): void { }
  
  // Motivo 2: Lógica de cálculo mudou
  calculateTotal(): void { }
  
  // Motivo 3: Lógica de pagamento mudou
  processPayment(): void { }
}
```

### 2. Análise de Coesão
```typescript
// ❌ Baixa coesão - métodos não relacionados
class UserService {
  createUser(): void { }
  sendEmail(): void { }
  logActivity(): void { }
  generateReport(): void { }
}
```

### 3. Análise de Acoplamento
```typescript
// ❌ Alto acoplamento - muitas dependências
class OrderService {
  constructor(
    private userRepo: UserRepository,
    private productRepo: ProductRepository,
    private paymentService: PaymentService,
    private emailService: EmailService,
    private logService: LogService,
    private reportService: ReportService
  ) {}
}
```

## Boas Práticas

### 1. Análise de Responsabilidades
- **Identificar responsabilidades**: Separar diferentes aspectos
- **Uma responsabilidade por classe**: Cada classe tem um propósito
- **Coesão alta**: Métodos relacionados agrupados

### 2. Design de Classes
- **Classes pequenas**: Fáceis de entender e manter
- **Métodos relacionados**: Agrupar funcionalidades similares
- **Responsabilidade única**: Apenas um motivo para mudar

### 3. Composição de Objetos
- **Composição ao invés de herança**: Preferir composição
- **Injeção de dependências**: Dependências externas
- **Interfaces bem definidas**: Contratos claros

## Conclusão

O Princípio da Responsabilidade Única é fundamental para criar sistemas bem arquitetados e maintíveis. Ele não é sobre criar micro-classes, mas sobre **coesão e coerência**.

### Pontos-Chave
- **Uma responsabilidade**: Cada classe tem um propósito específico
- **Um motivo para mudar**: Facilita manutenção e evolução
- **Composição de objetos**: Unir responsabilidades através de composição
- **Coesão alta**: Métodos relacionados agrupados

### Próximos Passos
- [Estudar violações comuns](./srp-violations.md)
- [Aplicar refatoração](./srp-refactoring.md)
- [Implementar composição](./srp-composition.md)
- [Aplicar boas práticas](./srp-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
