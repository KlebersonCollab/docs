# Guia de Implementação - Padrão Strategy

## 🎯 Checklist de Implementação

### ✅ **Fase 1: Análise e Planejamento**

- [ ] **Identificar o problema**: Múltiplas formas de executar uma tarefa
- [ ] **Mapear algoritmos**: Listar todas as variações possíveis
- [ ] **Definir interface**: Criar contrato comum para todas as estratégias
- [ ] **Validar necessidade**: Confirmar que Strategy é a melhor solução
- [ ] **Planejar testes**: Definir estratégia de testes para cada implementação

### ✅ **Fase 2: Design da Interface**

- [ ] **Criar interface Strategy**: Definir métodos comuns
- [ ] **Definir parâmetros**: Especificar entrada e saída
- [ ] **Documentar contrato**: Escrever documentação clara
- [ ] **Validar interface**: Revisar com stakeholders
- [ ] **Versionar interface**: Considerar compatibilidade futura

### ✅ **Fase 3: Implementação das Estratégias**

- [ ] **Implementar estratégias concretas**: Uma classe por algoritmo
- [ ] **Validar implementação**: Testes unitários para cada estratégia
- [ ] **Documentar estratégias**: Comentários e exemplos de uso
- [ ] **Otimizar performance**: Identificar gargalos se necessário
- [ ] **Tratar erros**: Implementar tratamento de exceções

### ✅ **Fase 4: Implementação do Contexto**

- [ ] **Criar classe Context**: Implementar gerenciador de estratégias
- [ ] **Implementar setter**: Método para trocar estratégias
- [ ] **Implementar executor**: Método que delega para a estratégia
- [ ] **Validar contexto**: Testes de integração
- [ ] **Documentar contexto**: Explicar responsabilidades

### ✅ **Fase 5: Integração e Testes**

- [ ] **Integrar com cliente**: Conectar com código existente
- [ ] **Implementar Factory**: Se necessário para criação de estratégias
- [ ] **Testes de integração**: Validar fluxo completo
- [ ] **Testes de performance**: Verificar impacto na performance
- [ ] **Documentar uso**: Criar exemplos práticos

## 🛠️ Fases de Desenvolvimento

### **Fase 1: Análise e Planejamento**

#### 1.1 Identificar o Problema
```markdown
**Perguntas a fazer:**
- Existem múltiplas formas de executar a mesma tarefa?
- Os algoritmos variam frequentemente?
- Há necessidade de trocar algoritmos em runtime?
- O código atual viola princípios SOLID?

**Sinais de que Strategy é necessário:**
- Muitos ifs/switch para diferentes comportamentos
- Violação do Open/Closed Principle
- Violação do Single Responsibility Principle
- Dificuldade para testar algoritmos isoladamente
```

#### 1.2 Mapear Algoritmos
```markdown
**Lista de algoritmos identificados:**
- [ ] Algoritmo A: [Descrição]
- [ ] Algoritmo B: [Descrição]
- [ ] Algoritmo C: [Descrição]
- [ ] Algoritmo D: [Descrição]

**Características comuns:**
- Entrada: [Tipo de dados]
- Saída: [Tipo de dados]
- Parâmetros: [Lista de parâmetros]
- Validações: [Regras de validação]
```

#### 1.3 Validar Necessidade
```markdown
**Critérios de validação:**
- [ ] Múltiplas implementações do mesmo conceito
- [ ] Necessidade de trocar implementação em runtime
- [ ] Violação de princípios SOLID
- [ ] Dificuldade de manutenção
- [ ] Necessidade de testes isolados

**Alternativas consideradas:**
- [ ] Factory Pattern
- [ ] Template Method
- [ ] Chain of Responsibility
- [ ] Command Pattern
```

### **Fase 2: Design da Interface**

#### 2.1 Criar Interface Strategy
```typescript
// Exemplo de interface bem definida
interface PaymentStrategy {
  // Método principal
  processPayment(amount: number, data: PaymentData): Promise<PaymentResult>;
  
  // Métodos de validação
  validatePaymentData(data: PaymentData): boolean;
  
  // Métodos de informação
  getMethodName(): string;
  getFeeRate(): number;
  getPriority(): number;
  
  // Métodos de configuração
  configure(options: StrategyOptions): void;
}
```

#### 2.2 Definir Parâmetros
```markdown
**Entrada (Input):**
- Tipo: [Ex: PaymentData]
- Campos obrigatórios: [Lista]
- Campos opcionais: [Lista]
- Validações: [Regras]

**Saída (Output):**
- Tipo: [Ex: PaymentResult]
- Campos obrigatórios: [Lista]
- Campos opcionais: [Lista]
- Tratamento de erros: [Estratégia]
```

#### 2.3 Documentar Contrato
```markdown
**Documentação da interface:**
- [ ] Propósito de cada método
- [ ] Parâmetros e tipos
- [ ] Valores de retorno
- [ ] Exceções possíveis
- [ ] Exemplos de uso
- [ ] Casos de erro
```

### **Fase 3: Implementação das Estratégias**

#### 3.1 Implementar Estratégias Concretas
```php
// Exemplo de implementação em PHP
class CreditCardPayment implements PaymentStrategy 
{
    private const FEE_RATE = 0.029;
    private const METHOD_NAME = 'Cartão de Crédito';
    
    public function processPayment(float $amount, PaymentData $data): PaymentResult 
    {
        // Validação
        if (!$this->validatePaymentData($data)) {
            return PaymentResult::failed('Dados inválidos');
        }
        
        // Processamento
        $fee = $amount * self::FEE_RATE;
        $total = $amount + $fee;
        
        // Resultado
        return PaymentResult::success([
            'amount' => $amount,
            'fee' => $fee,
            'total' => $total,
            'transaction_id' => $this->generateTransactionId()
        ]);
    }
    
    public function validatePaymentData(PaymentData $data): bool 
    {
        return !empty($data->cardNumber) && 
               !empty($data->cvv) && 
               !empty($data->expiryDate);
    }
    
    public function getMethodName(): string 
    {
        return self::METHOD_NAME;
    }
    
    public function getFeeRate(): float 
    {
        return self::FEE_RATE;
    }
    
    public function getPriority(): int 
    {
        return 1;
    }
}
```

#### 3.2 Validar Implementação
```markdown
**Testes unitários para cada estratégia:**
- [ ] Teste de sucesso
- [ ] Teste de falha
- [ ] Teste de validação
- [ ] Teste de performance
- [ ] Teste de edge cases
```

#### 3.3 Documentar Estratégias
```markdown
**Documentação de cada estratégia:**
- [ ] Propósito da estratégia
- [ ] Algoritmo implementado
- [ ] Parâmetros específicos
- [ ] Validações específicas
- [ ] Exemplos de uso
- [ ] Limitações conhecidas
```

### **Fase 4: Implementação do Contexto**

#### 4.1 Criar Classe Context
```typescript
// Exemplo de contexto em TypeScript
class PaymentProcessor {
    private strategy: PaymentStrategy | null = null;
    
    public setStrategy(strategy: PaymentStrategy): PaymentProcessor {
        this.strategy = strategy;
        return this;
    }
    
    public async processPayment(amount: number, data: PaymentData): Promise<PaymentResult> {
        if (!this.strategy) {
            throw new Error('Estratégia de pagamento não definida');
        }
        
        return await this.strategy.processPayment(amount, data);
    }
    
    public getStrategyInfo(): StrategyInfo | null {
        if (!this.strategy) {
            return null;
        }
        
        return {
            method: this.strategy.getMethodName(),
            feeRate: this.strategy.getFeeRate(),
            priority: this.strategy.getPriority()
        };
    }
}
```

#### 4.2 Implementar Setter
```markdown
**Características do setter:**
- [ ] Validação da estratégia
- [ ] Configuração da estratégia
- [ ] Retorno do contexto (fluent interface)
- [ ] Tratamento de erros
- [ ] Logging de mudanças
```

#### 4.3 Implementar Executor
```markdown
**Características do executor:**
- [ ] Validação de estratégia definida
- [ ] Delegação para estratégia
- [ ] Tratamento de exceções
- [ ] Logging de execução
- [ ] Métricas de performance
```

### **Fase 5: Integração e Testes**

#### 5.1 Integrar com Cliente
```markdown
**Integração com código existente:**
- [ ] Refatorar código cliente
- [ ] Implementar Factory se necessário
- [ ] Configurar injeção de dependência
- [ ] Atualizar testes existentes
- [ ] Documentar mudanças
```

#### 5.2 Implementar Factory
```typescript
// Exemplo de Factory para Strategy
class PaymentStrategyFactory {
    private static strategies = new Map<string, () => PaymentStrategy>([
        ['credit_card', () => new CreditCardPayment()],
        ['pix', () => new PIXPayment()],
        ['boleto', () => new BoletoPayment()]
    ]);
    
    public static createStrategy(type: string): PaymentStrategy {
        const strategyFactory = this.strategies.get(type);
        if (!strategyFactory) {
            throw new Error(`Tipo de pagamento '${type}' não suportado`);
        }
        
        return strategyFactory();
    }
    
    public static getAvailableTypes(): string[] {
        return Array.from(this.strategies.keys());
    }
}
```

#### 5.3 Testes de Integração
```markdown
**Testes de integração:**
- [ ] Teste de fluxo completo
- [ ] Teste de troca de estratégias
- [ ] Teste de performance
- [ ] Teste de concorrência
- [ ] Teste de falhas
```

## 🎯 Boas Práticas

### **1. Design da Interface**

#### ✅ **Faça**
```typescript
// Interface clara e específica
interface PaymentStrategy {
  processPayment(amount: number, data: PaymentData): Promise<PaymentResult>;
  validatePaymentData(data: PaymentData): boolean;
  getMethodName(): string;
}
```

#### ❌ **Evite**
```typescript
// Interface muito genérica
interface Strategy {
  execute(data: any): any;
}
```

### **2. Implementação das Estratégias**

#### ✅ **Faça**
```php
// Estratégia focada e coesa
class CreditCardPayment implements PaymentStrategy 
{
    private const FEE_RATE = 0.029;
    
    public function processPayment(float $amount, PaymentData $data): PaymentResult 
    {
        // Implementação específica para cartão de crédito
    }
}
```

#### ❌ **Evite**
```php
// Estratégia com múltiplas responsabilidades
class PaymentProcessor 
{
    public function processCreditCard() { /* ... */ }
    public function processPIX() { /* ... */ }
    public function processBoleto() { /* ... */ }
}
```

### **3. Implementação do Contexto**

#### ✅ **Faça**
```typescript
// Contexto simples e claro
class PaymentProcessor {
    private strategy: PaymentStrategy | null = null;
    
    public setStrategy(strategy: PaymentStrategy): PaymentProcessor {
        this.strategy = strategy;
        return this;
    }
    
    public async processPayment(amount: number, data: PaymentData): Promise<PaymentResult> {
        if (!this.strategy) {
            throw new Error('Estratégia não definida');
        }
        
        return await this.strategy.processPayment(amount, data);
    }
}
```

#### ❌ **Evite**
```typescript
// Contexto com lógica complexa
class PaymentProcessor {
    public processPayment(type: string, amount: number, data: any): any {
        if (type === 'credit_card') {
            // Lógica específica aqui
        } else if (type === 'pix') {
            // Lógica específica aqui
        }
        // ...
    }
}
```

### **4. Tratamento de Erros**

#### ✅ **Faça**
```typescript
// Tratamento específico por estratégia
class CreditCardPayment implements PaymentStrategy {
    public async processPayment(amount: number, data: PaymentData): Promise<PaymentResult> {
        try {
            if (!this.validatePaymentData(data)) {
                return PaymentResult.failed('Dados do cartão inválidos');
            }
            
            // Processamento...
            return PaymentResult.success(result);
        } catch (error) {
            return PaymentResult.failed(`Erro no processamento: ${error.message}`);
        }
    }
}
```

#### ❌ **Evite**
```typescript
// Tratamento genérico
class PaymentStrategy {
    public processPayment(amount: number, data: PaymentData): PaymentResult {
        try {
            // Processamento...
        } catch (error) {
            return PaymentResult.failed('Erro genérico');
        }
    }
}
```

### **5. Testes**

#### ✅ **Faça**
```typescript
// Testes específicos para cada estratégia
describe('CreditCardPayment', () => {
    it('should process payment successfully', async () => {
        const strategy = new CreditCardPayment();
        const result = await strategy.processPayment(100, validData);
        expect(result.success).toBe(true);
    });
    
    it('should fail with invalid data', async () => {
        const strategy = new CreditCardPayment();
        const result = await strategy.processPayment(100, invalidData);
        expect(result.success).toBe(false);
    });
});
```

#### ❌ **Evite**
```typescript
// Testes genéricos
describe('PaymentStrategy', () => {
    it('should work', () => {
        // Teste genérico que não testa nada específico
    });
});
```

## 🔧 Extensões Avançadas

### **1. Strategy com Factory**

```typescript
// Factory para criar estratégias
class PaymentStrategyFactory {
    private static strategies = new Map<string, () => PaymentStrategy>();
    
    public static registerStrategy(type: string, factory: () => PaymentStrategy): void {
        this.strategies.set(type, factory);
    }
    
    public static createStrategy(type: string): PaymentStrategy {
        const factory = this.strategies.get(type);
        if (!factory) {
            throw new Error(`Estratégia '${type}' não encontrada`);
        }
        
        return factory();
    }
}

// Registro de estratégias
PaymentStrategyFactory.registerStrategy('credit_card', () => new CreditCardPayment());
PaymentStrategyFactory.registerStrategy('pix', () => new PIXPayment());
```

### **2. Strategy com Registry**

```typescript
// Registry para gerenciar estratégias
class PaymentStrategyRegistry {
    private strategies = new Map<string, PaymentStrategy>();
    
    public registerStrategy(type: string, strategy: PaymentStrategy): void {
        this.strategies.set(type, strategy);
    }
    
    public getStrategy(type: string): PaymentStrategy | null {
        return this.strategies.get(type) || null;
    }
    
    public getAvailableTypes(): string[] {
        return Array.from(this.strategies.keys());
    }
}
```

### **3. Strategy com Builder**

```typescript
// Builder para configurar estratégias
class PaymentStrategyBuilder {
    private strategy: PaymentStrategy | null = null;
    private options: StrategyOptions = {};
    
    public setStrategy(strategy: PaymentStrategy): PaymentStrategyBuilder {
        this.strategy = strategy;
        return this;
    }
    
    public withOptions(options: StrategyOptions): PaymentStrategyBuilder {
        this.options = { ...this.options, ...options };
        return this;
    }
    
    public build(): PaymentStrategy {
        if (!this.strategy) {
            throw new Error('Estratégia não definida');
        }
        
        this.strategy.configure(this.options);
        return this.strategy;
    }
}
```

### **4. Strategy com Chain of Responsibility**

```typescript
// Chain of Responsibility com Strategy
abstract class PaymentHandler {
    protected nextHandler: PaymentHandler | null = null;
    
    public setNext(handler: PaymentHandler): PaymentHandler {
        this.nextHandler = handler;
        return handler;
    }
    
    public async handle(request: PaymentRequest): Promise<PaymentResult> {
        if (this.canHandle(request)) {
            return await this.process(request);
        }
        
        if (this.nextHandler) {
            return await this.nextHandler.handle(request);
        }
        
        return PaymentResult.failed('Nenhum handler disponível');
    }
    
    protected abstract canHandle(request: PaymentRequest): boolean;
    protected abstract process(request: PaymentRequest): Promise<PaymentResult>;
}
```

## 🚨 Armadilhas Comuns

### **1. Over-Engineering**

#### ❌ **Problema**
```typescript
// Strategy desnecessário para caso simples
interface SimpleStrategy {
    execute(): void;
}

class SimpleStrategyA implements SimpleStrategy {
    execute(): void {
        console.log('A');
    }
}

class SimpleStrategyB implements SimpleStrategy {
    execute(): void {
        console.log('B');
    }
}
```

#### ✅ **Solução**
```typescript
// Solução mais simples
function executeSimple(type: 'A' | 'B'): void {
    if (type === 'A') {
        console.log('A');
    } else {
        console.log('B');
    }
}
```

### **2. Interface Muito Genérica**

#### ❌ **Problema**
```typescript
// Interface muito genérica
interface Strategy {
    execute(data: any): any;
}
```

#### ✅ **Solução**
```typescript
// Interface específica
interface PaymentStrategy {
    processPayment(amount: number, data: PaymentData): Promise<PaymentResult>;
    validatePaymentData(data: PaymentData): boolean;
}
```

### **3. Contexto com Lógica Complexa**

#### ❌ **Problema**
```typescript
// Contexto com lógica complexa
class PaymentProcessor {
    public processPayment(type: string, amount: number, data: any): any {
        if (type === 'credit_card') {
            // Lógica complexa aqui
        } else if (type === 'pix') {
            // Lógica complexa aqui
        }
        // ...
    }
}
```

#### ✅ **Solução**
```typescript
// Contexto simples
class PaymentProcessor {
    private strategy: PaymentStrategy | null = null;
    
    public setStrategy(strategy: PaymentStrategy): void {
        this.strategy = strategy;
    }
    
    public async processPayment(amount: number, data: PaymentData): Promise<PaymentResult> {
        if (!this.strategy) {
            throw new Error('Estratégia não definida');
        }
        
        return await this.strategy.processPayment(amount, data);
    }
}
```

### **4. Falta de Validação**

#### ❌ **Problema**
```typescript
// Sem validação
class PaymentProcessor {
    public setStrategy(strategy: PaymentStrategy): void {
        this.strategy = strategy; // Sem validação
    }
}
```

#### ✅ **Solução**
```typescript
// Com validação
class PaymentProcessor {
    public setStrategy(strategy: PaymentStrategy): void {
        if (!strategy) {
            throw new Error('Estratégia não pode ser nula');
        }
        
        this.strategy = strategy;
    }
}
```

## 📊 Métricas e Monitoramento

### **Métricas de Performance**

```typescript
// Decorator para métricas
class MetricsPaymentStrategy implements PaymentStrategy {
    constructor(
        private strategy: PaymentStrategy,
        private metrics: MetricsCollector
    ) {}
    
    public async processPayment(amount: number, data: PaymentData): Promise<PaymentResult> {
        const startTime = Date.now();
        
        try {
            const result = await this.strategy.processPayment(amount, data);
            
            this.metrics.recordSuccess({
                strategy: this.strategy.getMethodName(),
                duration: Date.now() - startTime,
                amount: amount
            });
            
            return result;
        } catch (error) {
            this.metrics.recordError({
                strategy: this.strategy.getMethodName(),
                duration: Date.now() - startTime,
                error: error.message
            });
            
            throw error;
        }
    }
}
```

### **Métricas de Negócio**

```typescript
// Métricas de negócio
interface BusinessMetrics {
    totalTransactions: number;
    totalAmount: number;
    successRate: number;
    averageAmount: number;
    topStrategy: string;
}
```

### **Métricas Técnicas**

```typescript
// Métricas técnicas
interface TechnicalMetrics {
    responseTime: number;
    memoryUsage: number;
    cpuUsage: number;
    errorRate: number;
    throughput: number;
}
```

## 🎯 Conclusão

O padrão Strategy é uma ferramenta poderosa para resolver problemas de múltiplos algoritmos, mas deve ser usado com sabedoria. Seguindo este guia de implementação, você pode criar soluções flexíveis, testáveis e manuteníveis.

**Lembre-se:**
- Use Strategy quando houver múltiplas formas de executar uma tarefa
- Evite over-engineering para casos simples
- Mantenha interfaces específicas e claras
- Implemente testes para cada estratégia
- Monitore performance e métricas de negócio








