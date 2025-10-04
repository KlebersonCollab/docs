# Refatoração e Extração de Classes no SRP

## Informações Básicas
- **ID do Documento**: SRP-003
- **Nome**: Refatoração e Extração de Classes no SRP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

Este documento apresenta técnicas práticas para refatorar classes que violam o Princípio da Responsabilidade Única (SRP), mostrando como extrair responsabilidades e criar classes mais coesas e maintíveis.

## 1. Identificação de Responsabilidades

### 1.1. Análise de Motivos para Mudança

#### Pergunta-Chave
> "Quantos motivos esta classe tem para mudar?"

#### Exemplo de Análise
```typescript
// ❌ Classe com múltiplos motivos para mudança
class OrderProcessorService {
  processOrder(order: Order): void {
    this.checkInventory(order);      // Motivo 1: Lógica de inventário
    this.calculateTotal(order);      // Motivo 2: Lógica de cálculo
    this.processPayment(order);      // Motivo 3: Lógica de pagamento
  }
  
  private checkInventory(order: Order): void {
    // Se a lógica de inventário mudar, esta classe muda
  }
  
  private calculateTotal(order: Order): void {
    // Se a lógica de cálculo mudar, esta classe muda
  }
  
  private processPayment(order: Order): void {
    // Se a lógica de pagamento mudar, esta classe muda
  }
}
```

#### Identificação de Responsabilidades
- **Responsabilidade 1**: Verificação de inventário
- **Responsabilidade 2**: Cálculo de total
- **Responsabilidade 3**: Processamento de pagamento

### 1.2. Análise de Coesão

#### Métodos Relacionados
```typescript
// ❌ Métodos não relacionados em uma classe
class UserService {
  // Grupo 1: Gerenciamento de usuários
  createUser(user: User): void { }
  updateUser(user: User): void { }
  deleteUser(userId: string): void { }
  
  // Grupo 2: Envio de emails
  sendWelcomeEmail(user: User): void { }
  sendPasswordResetEmail(user: User): void { }
  
  // Grupo 3: Geração de relatórios
  generateUserReport(): void { }
  exportUserData(): void { }
  
  // Grupo 4: Logging
  logUserActivity(user: User, activity: string): void { }
}
```

#### Identificação de Grupos
- **Grupo 1**: Gerenciamento de usuários
- **Grupo 2**: Envio de emails
- **Grupo 3**: Geração de relatórios
- **Grupo 4**: Logging

## 2. Extração de Responsabilidades

### 2.1. Extração por Responsabilidade

#### Passo 1: Identificar Responsabilidades
```typescript
// ❌ Classe original com múltiplas responsabilidades
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

#### Passo 2: Extrair Responsabilidades
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

#### Passo 3: Refatorar Classe Original
```typescript
// ✅ Classe orquestradora
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

### 2.2. Extração por Contexto

#### Exemplo: Sistema de Usuários
```typescript
// ❌ Classe original com múltiplos contextos
class UserService {
  // Contexto 1: Gerenciamento de usuários
  createUser(user: User): void { }
  updateUser(user: User): void { }
  deleteUser(userId: string): void { }
  
  // Contexto 2: Envio de emails
  sendWelcomeEmail(user: User): void { }
  sendPasswordResetEmail(user: User): void { }
  
  // Contexto 3: Geração de relatórios
  generateUserReport(): void { }
  exportUserData(): void { }
  
  // Contexto 4: Logging
  logUserActivity(user: User, activity: string): void { }
}
```

#### Extração por Contexto
```typescript
// ✅ Contexto 1: Gerenciamento de usuários
class UserManager {
  createUser(user: User): void { }
  updateUser(user: User): void { }
  deleteUser(userId: string): void { }
}

// ✅ Contexto 2: Envio de emails
class UserEmailService {
  sendWelcomeEmail(user: User): void { }
  sendPasswordResetEmail(user: User): void { }
}

// ✅ Contexto 3: Geração de relatórios
class UserReportService {
  generateUserReport(): void { }
  exportUserData(): void { }
}

// ✅ Contexto 4: Logging
class UserActivityLogger {
  logUserActivity(user: User, activity: string): void { }
}
```

### 2.3. Extração por Abstração

#### Exemplo: Sistema de Dados
```typescript
// ❌ Classe original com múltiplas abstrações
class DataProcessor {
  // Abstração 1: Processamento
  processData(data: any): any { }
  transformData(data: any): any { }
  validateData(data: any): boolean { }
  
  // Abstração 2: Persistência
  saveData(data: any): void { }
  loadData(id: string): any { }
  
  // Abstração 3: Serialização
  serializeData(data: any): string { }
  deserializeData(json: string): any { }
  
  // Abstração 4: Cache
  getDataFromCache(key: string): any { }
  setDataInCache(key: string, data: any): void { }
}
```

#### Extração por Abstração
```typescript
// ✅ Abstração 1: Processamento
class DataProcessor {
  processData(data: any): any { }
  transformData(data: any): any { }
  validateData(data: any): boolean { }
}

// ✅ Abstração 2: Persistência
class DataRepository {
  saveData(data: any): void { }
  loadData(id: string): any { }
}

// ✅ Abstração 3: Serialização
class DataSerializer {
  serializeData(data: any): string { }
  deserializeData(json: string): any { }
}

// ✅ Abstração 4: Cache
class DataCache {
  getDataFromCache(key: string): any { }
  setDataInCache(key: string, data: any): void { }
}
```

## 3. Técnicas de Refatoração

### 3.1. Extract Method

#### Antes da Refatoração
```typescript
// ❌ Método longo com múltiplas responsabilidades
class OrderProcessor {
  processOrder(order: Order): void {
    // Verificação de inventário
    if (order.items.length === 0) {
      throw new Error('Pedido sem itens');
    }
    
    for (const item of order.items) {
      const stock = this.getStock(item.productId);
      if (stock < item.quantity) {
        throw new Error('Estoque insuficiente');
      }
    }
    
    // Cálculo de total
    let total = 0;
    for (const item of order.items) {
      total += item.price * item.quantity;
    }
    
    // Aplicação de impostos
    const tax = total * 0.1;
    total += tax;
    
    // Aplicação de desconto
    if (total > 100) {
      total *= 0.9;
    }
    
    // Processamento de pagamento
    const paymentResult = this.paymentGateway.processPayment(total);
    if (!paymentResult.success) {
      throw new Error('Pagamento falhou');
    }
    
    // Atualização de estoque
    for (const item of order.items) {
      this.updateStock(item.productId, item.quantity);
    }
  }
}
```

#### Depois da Refatoração
```typescript
// ✅ Métodos extraídos com responsabilidades específicas
class OrderProcessor {
  processOrder(order: Order): void {
    this.checkInventory(order);
    const total = this.calculateTotal(order);
    this.processPayment(order, total);
    this.updateInventory(order);
  }
  
  private checkInventory(order: Order): void {
    if (order.items.length === 0) {
      throw new Error('Pedido sem itens');
    }
    
    for (const item of order.items) {
      const stock = this.getStock(item.productId);
      if (stock < item.quantity) {
        throw new Error('Estoque insuficiente');
      }
    }
  }
  
  private calculateTotal(order: Order): number {
    let total = 0;
    for (const item of order.items) {
      total += item.price * item.quantity;
    }
    
    const tax = total * 0.1;
    total += tax;
    
    if (total > 100) {
      total *= 0.9;
    }
    
    return total;
  }
  
  private processPayment(order: Order, total: number): void {
    const paymentResult = this.paymentGateway.processPayment(total);
    if (!paymentResult.success) {
      throw new Error('Pagamento falhou');
    }
  }
  
  private updateInventory(order: Order): void {
    for (const item of order.items) {
      this.updateStock(item.productId, item.quantity);
    }
  }
}
```

### 3.2. Extract Class

#### Antes da Refatoração
```typescript
// ❌ Classe com múltiplas responsabilidades
class UserService {
  createUser(user: User): void {
    // Lógica de criação
  }
  
  updateUser(user: User): void {
    // Lógica de atualização
  }
  
  deleteUser(userId: string): void {
    // Lógica de exclusão
  }
  
  sendWelcomeEmail(user: User): void {
    // Lógica de email
  }
  
  sendPasswordResetEmail(user: User): void {
    // Lógica de email
  }
  
  generateUserReport(): void {
    // Lógica de relatório
  }
  
  exportUserData(): void {
    // Lógica de exportação
  }
  
  logUserActivity(user: User, activity: string): void {
    // Lógica de log
  }
}
```

#### Depois da Refatoração
```typescript
// ✅ Classes com responsabilidades específicas
class UserManager {
  createUser(user: User): void { }
  updateUser(user: User): void { }
  deleteUser(userId: string): void { }
}

class UserEmailService {
  sendWelcomeEmail(user: User): void { }
  sendPasswordResetEmail(user: User): void { }
}

class UserReportService {
  generateUserReport(): void { }
  exportUserData(): void { }
}

class UserActivityLogger {
  logUserActivity(user: User, activity: string): void { }
}
```

### 3.3. Move Method

#### Antes da Refatoração
```typescript
// ❌ Método em classe incorreta
class OrderService {
  processOrder(order: Order): void {
    // Lógica de processamento
  }
  
  calculateTax(order: Order): number {
    // Lógica de cálculo de imposto
    // Este método deveria estar em uma classe de cálculo
  }
}
```

#### Depois da Refatoração
```typescript
// ✅ Método movido para classe correta
class OrderService {
  processOrder(order: Order): void {
    // Lógica de processamento
  }
}

class TaxCalculator {
  calculateTax(order: Order): number {
    // Lógica de cálculo de imposto
  }
}
```

## 4. Padrões de Refatoração

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
```

### 4.3. Facade Pattern

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
    this.inventoryChecker.check(order);
    this.orderCalculator.calculate(order);
    this.paymentProcessor.process(order);
  }
}
```

## 5. Testes de Refatoração

### 5.1. Testes Unitários

#### Testes para Classes Extraídas
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

## 6. Benefícios da Refatoração

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

A refatoração para seguir o SRP é fundamental para criar sistemas bem arquitetados e maintíveis. Ela permite:

### Pontos-Chave
- **Identificação de responsabilidades**: Separar diferentes aspectos
- **Extração de classes**: Cada responsabilidade em sua própria classe
- **Composição de objetos**: Unir responsabilidades através de composição
- **Testes específicos**: Testes focados em uma responsabilidade

### Próximos Passos
- [Implementar composição](./srp-composition.md)
- [Aplicar boas práticas](./srp-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
