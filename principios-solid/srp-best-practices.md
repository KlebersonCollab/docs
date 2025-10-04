# Guia de Boas Práticas para o Princípio da Responsabilidade Única

## Informações Básicas
- **ID do Documento**: SRP-005
- **Nome**: Boas Práticas para SRP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

Este guia apresenta as melhores práticas para implementar o Princípio da Responsabilidade Única (SRP) corretamente, evitando violações comuns e criando sistemas mais robustos e maintíveis.

## 1. Análise de Responsabilidades

### 1.1. Identificação de Responsabilidades

#### Pergunta-Chave
> "Quantos motivos esta classe tem para mudar?"

#### Exemplo de Análise
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
  createUser(): void { }
  updateUser(): void { }
  deleteUser(): void { }
  
  // Grupo 2: Envio de emails
  sendWelcomeEmail(): void { }
  sendPasswordResetEmail(): void { }
  
  // Grupo 3: Geração de relatórios
  generateUserReport(): void { }
  exportUserData(): void { }
}
```

#### Identificação de Grupos
- **Grupo 1**: Gerenciamento de usuários
- **Grupo 2**: Envio de emails
- **Grupo 3**: Geração de relatórios

## 2. Design de Classes

### 2.1. Classes com Responsabilidade Única

#### Exemplo Correto
```typescript
// ✅ Classe com responsabilidade única
class UserManager {
  createUser(user: User): void {
    // Apenas lógica de criação de usuário
  }
  
  updateUser(user: User): void {
    // Apenas lógica de atualização de usuário
  }
  
  deleteUser(userId: string): void {
    // Apenas lógica de exclusão de usuário
  }
}
```

#### Exemplo Incorreto
```typescript
// ❌ Classe com múltiplas responsabilidades
class UserService {
  createUser(user: User): void { }
  updateUser(user: User): void { }
  deleteUser(userId: string): void { }
  sendWelcomeEmail(user: User): void { }
  sendPasswordResetEmail(user: User): void { }
  generateUserReport(): void { }
  exportUserData(): void { }
  logUserActivity(user: User, activity: string): void { }
}
```

### 2.2. Tamanho Adequado de Classes

#### Classes Pequenas e Focadas
```typescript
// ✅ Classe pequena e focada
class EmailValidator {
  validate(email: string): boolean {
    // Apenas validação de email
  }
}

// ✅ Classe pequena e focada
class PasswordValidator {
  validate(password: string): boolean {
    // Apenas validação de senha
  }
}
```

#### Evitar Classes Grandes
```typescript
// ❌ Classe grande com muitas responsabilidades
class UserService {
  createUser(): void { }
  updateUser(): void { }
  deleteUser(): void { }
  validateEmail(): void { }
  validatePassword(): void { }
  sendWelcomeEmail(): void { }
  sendPasswordResetEmail(): void { }
  generateUserReport(): void { }
  exportUserData(): void { }
  logUserActivity(): void { }
  checkUserPermissions(): void { }
  updateUserPreferences(): void { }
  // ... muitos outros métodos
}
```

## 3. Extração de Responsabilidades

### 3.1. Extração por Responsabilidade

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

#### Passo 3: Composição de Objetos
```typescript
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

### 3.2. Extração por Contexto

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

## 4. Composição de Objetos

### 4.1. Injeção de Dependências

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

### 4.2. Facade Pattern

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

## 5. Padrões de Design Aplicados

### 5.1. Strategy Pattern

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

### 5.2. Command Pattern

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

### 5.3. Observer Pattern

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

## 6. Testes com SRP

### 6.1. Testes Unitários

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

### 6.2. Testes de Integração

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

### 6.3. Testes com Mocks

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

## 7. Detecção de Violações

### 7.1. Análise de Motivos para Mudança
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

### 7.2. Análise de Coesão
```typescript
// ❌ Baixa coesão - métodos não relacionados
class UserService {
  createUser(): void { }
  sendEmail(): void { }
  logActivity(): void { }
  generateReport(): void { }
}
```

### 7.3. Análise de Acoplamento
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

## 8. Ferramentas e Automação

### 8.1. Análise Estática

#### Regras de Lint
```typescript
// Configuração de lint para detectar violações
{
  "rules": {
    "max-lines-per-function": ["error", 50],
    "max-lines": ["error", 300],
    "max-params": ["error", 4],
    "complexity": ["error", 10]
  }
}
```

#### Análise de Métricas
```typescript
class SRPAnalyzer {
  analyzeClass(className: string): SRPMetrics {
    return {
      methodCount: this.countMethods(className),
      responsibilityCount: this.countResponsibilities(className),
      couplingScore: this.calculateCouplingScore(className),
      cohesionScore: this.calculateCohesionScore(className)
    };
  }
}
```

### 8.2. Testes Automatizados

#### Testes de Responsabilidade
```typescript
describe('SRP Compliance', () => {
  it('should have single responsibility', () => {
    const class_ = new UserManager();
    
    // Testa se a classe tem apenas uma responsabilidade
    expect(class_.getResponsibilities()).toHaveLength(1);
  });
});
```

## 9. Checklist de Implementação

### 9.1. Checklist de Design

#### ✅ Análise de Responsabilidades
- [ ] Identificar responsabilidades específicas?
- [ ] Separar conceitos diferentes?
- [ ] Evitar generalizações desnecessárias?

#### ✅ Design de Classes
- [ ] Classes pequenas e focadas?
- [ ] Métodos relacionados agrupados?
- [ ] Tamanho adequado de classes?

#### ✅ Implementação
- [ ] Responsabilidade única por classe?
- [ ] Eliminação de código duplicado?
- [ ] Substituições funcionam corretamente?

#### ✅ Testes
- [ ] Testes unitários implementados?
- [ ] Testes de integração funcionam?
- [ ] Cobertura de testes adequada?

### 9.2. Checklist de Manutenção

#### ✅ Monitoramento
- [ ] Métricas de responsabilidade monitoradas?
- [ ] Alertas de violação configurados?
- [ ] Análise estática configurada?
- [ ] Testes de regressão funcionando?

#### ✅ Refatoração
- [ ] Violações identificadas e corrigidas?
- [ ] Classes problemáticas refatoradas?
- [ ] Código cliente simplificado?
- [ ] Documentação atualizada?

## 10. Conclusão

### 10.1. Benefícios das Boas Práticas

#### Código Mais Robusto
- **Responsabilidade única**: Cada classe tem um propósito específico
- **Manutenibilidade**: Mudanças isoladas em responsabilidades específicas
- **Testabilidade**: Testes focados em uma responsabilidade

#### Facilita Manutenção
- **Mudanças isoladas**: Alterações em uma responsabilidade não afetam outras
- **Código mais limpo**: Classes menores e mais focadas
- **Facilita testes**: Testes mais específicos e simples

#### Melhora Qualidade
- **Código mais limpo**: Menos responsabilidades por classe
- **Arquitetura melhor**: Hierarquias bem desenhadas
- **Documentação clara**: Classes bem definidas

### 10.2. Próximos Passos

#### Implementação Imediata
1. **Audite código existente**: Identifique violações do SRP
2. **Implemente testes**: Crie testes de responsabilidade
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
