# Guia de Implementação - Padrão Template Method

## 🎯 Checklist de Implementação

### ✅ **Fase 1: Análise e Identificação**

- [ ] **Identificar duplicação**: Múltiplas classes com código similar
- [ ] **Mapear algoritmo comum**: Listar passos que são idênticos
- [ ] **Identificar variações**: Listar passos que são diferentes
- [ ] **Validar necessidade**: Confirmar que Template Method é a melhor solução
- [ ] **Planejar refatoração**: Definir estratégia de migração

### ✅ **Fase 2: Design da Classe Abstrata**

- [ ] **Criar classe abstrata**: Definir estrutura base
- [ ] **Implementar template method**: Método que define o esqueleto
- [ ] **Implementar métodos comuns**: Código compartilhado
- [ ] **Declarar métodos abstratos**: Passos que variam
- [ ] **Documentar comportamento**: Escrever documentação clara

### ✅ **Fase 3: Implementação da Classe Abstrata**

- [ ] **Implementar template method**: Lógica central do algoritmo
- [ ] **Implementar métodos comuns**: Funcionalidades compartilhadas
- [ ] **Declarar métodos abstratos**: Interface para personalização
- [ ] **Validar implementação**: Testes unitários
- [ ] **Documentar classe abstrata**: Comentários e exemplos

### ✅ **Fase 4: Implementação das Classes Concretas**

- [ ] **Implementar classes concretas**: Uma por tipo de variação
- [ ] **Implementar métodos abstratos**: Lógica específica de cada classe
- [ ] **Validar implementação**: Testes unitários para cada classe
- [ ] **Documentar classes concretas**: Comentários e exemplos de uso
- [ ] **Otimizar implementação**: Identificar melhorias se necessário

### ✅ **Fase 5: Integração e Testes**

- [ ] **Integrar sistema**: Conectar com sistema existente
- [ ] **Implementar testes**: Testes de integração
- [ ] **Testes de performance**: Verificar impacto na performance
- [ ] **Testes de regressão**: Validar que funcionalidades existentes não quebraram
- [ ] **Documentar uso**: Criar exemplos práticos

## 🛠️ Fases de Desenvolvimento

### **Fase 1: Análise e Identificação**

#### 1.1 Identificar Duplicação
```markdown
**Perguntas a fazer:**
- Existem múltiplas classes com código similar?
- O algoritmo é o mesmo, mas com pequenas variações?
- Há necessidade de manter a ordem de execução?
- A duplicação está causando problemas de manutenção?

**Sinais de que Template Method é necessário:**
- Múltiplas classes com algoritmos similares
- Duplicação de código entre classes
- Necessidade de controlar ordem de execução
- Manutenção complexa devido à duplicação
```

#### 1.2 Mapear Algoritmo Comum
```markdown
**Lista de passos comuns:**
- [ ] Passo 1: [Descrição e implementação]
- [ ] Passo 2: [Descrição e implementação]
- [ ] Passo 3: [Descrição e implementação]
- [ ] Passo 4: [Descrição e implementação]

**Lista de passos que variam:**
- [ ] Variação 1: [Descrição e diferenças]
- [ ] Variação 2: [Descrição e diferenças]
- [ ] Variação 3: [Descrição e diferenças]
```

#### 1.3 Validar Necessidade
```markdown
**Critérios de validação:**
- [ ] Múltiplas classes com algoritmos similares
- [ ] Duplicação de código é um problema
- [ ] Ordem de execução deve ser controlada
- [ ] Manutenção centralizada é desejada
- [ ] Extensibilidade é necessária

**Alternativas consideradas:**
- [ ] Strategy Pattern
- [ ] Command Pattern
- [ ] Chain of Responsibility
- [ ] Composition over Inheritance
```

### **Fase 2: Design da Classe Abstrata**

#### 2.1 Criar Classe Abstrata
```typescript
// Exemplo de classe abstrata bem estruturada
abstract class DataProcessor {
  // Template Method - define o esqueleto
  public process(data: any): ProcessResult {
    this.validateInput(data);
    const processedData = this.transformData(data);
    const result = this.analyzeData(processedData);
    this.saveResult(result);
    this.notifyStakeholders(result);
    return result;
  }
  
  // Métodos abstratos para personalização
  protected abstract validateInput(data: any): void;
  protected abstract transformData(data: any): any;
  protected abstract analyzeData(data: any): ProcessResult;
  
  // Métodos comuns implementados
  protected saveResult(result: ProcessResult): void {
    // Implementação comum
  }
  
  protected notifyStakeholders(result: ProcessResult): void {
    // Implementação comum
  }
}
```

#### 2.2 Implementar Template Method
```markdown
**Características do Template Method:**
- [ ] Método público e final
- [ ] Define ordem de execução
- [ ] Chama métodos abstratos e comuns
- [ ] Trata erros adequadamente
- [ ] Documenta comportamento
```

#### 2.3 Implementar Métodos Comuns
```markdown
**Funcionalidades comuns:**
- [ ] Validação de entrada
- [ ] Processamento de dados
- [ ] Salvamento de resultados
- [ ] Envio de notificações
- [ ] Logging e monitoramento
```

### **Fase 3: Implementação da Classe Abstrata**

#### 3.1 Implementar Template Method
```php
// Exemplo de implementação em PHP
abstract class DataMiner 
{
    /**
     * Template Method - define o esqueleto do algoritmo
     * Este método não pode ser sobrescrito pelas subclasses
     */
    final public function mine(): void 
    {
        try {
            // 1. Abrir arquivo
            $fileContent = $this->openFile();
            
            // 2. Extrair dados
            $rawData = $this->extractData($fileContent);
            
            // 3. Parsear dados
            $parsedData = $this->parseData($rawData);
            
            // 4. Analisar dados (implementação comum)
            $this->analyzeData($parsedData);
            
            // 5. Enviar relatório (implementação comum)
            $this->sendReport($parsedData);
            
        } catch (Exception $e) {
            $this->handleError($e);
        }
    }
    
    // Métodos abstratos para personalização
    abstract protected function openFile(): string;
    abstract protected function extractData(string $fileContent): array;
    abstract protected function parseData(array $rawData): array;
    
    // Implementações comuns
    protected function analyzeData(array $data): void 
    {
        // Lógica comum de análise
    }
    
    protected function sendReport(array $data): void 
    {
        // Lógica comum de envio
    }
    
    protected function handleError(Exception $e): void 
    {
        // Lógica comum de tratamento de erros
    }
}
```

#### 3.2 Implementar Métodos Comuns
```markdown
**Funcionalidades comuns implementadas:**
- [ ] Validação de dados
- [ ] Processamento de dados
- [ ] Análise de dados
- [ ] Salvamento de resultados
- [ ] Envio de notificações
- [ ] Tratamento de erros
- [ ] Logging e monitoramento
```

#### 3.3 Declarar Métodos Abstratos
```markdown
**Métodos abstratos definidos:**
- [ ] Método 1: [Descrição e assinatura]
- [ ] Método 2: [Descrição e assinatura]
- [ ] Método 3: [Descrição e assinatura]
- [ ] Método 4: [Descrição e assinatura]

**Documentação de cada método:**
- [ ] Propósito do método
- [ ] Parâmetros de entrada
- [ ] Valor de retorno
- [ ] Exceções possíveis
- [ ] Exemplos de uso
```

### **Fase 4: Implementação das Classes Concretas**

#### 4.1 Implementar Classes Concretas
```typescript
// Exemplo de implementação concreta
class SalesDataProcessor extends DataProcessor {
  protected validateInput(data: any): void {
    if (!data.sales || !Array.isArray(data.sales)) {
      throw new Error('Dados de vendas inválidos');
    }
  }
  
  protected transformData(data: any): any {
    return data.sales.map(sale => ({
      id: sale.id,
      amount: parseFloat(sale.amount),
      date: new Date(sale.date),
      customer: sale.customer
    }));
  }
  
  protected analyzeData(data: any): ProcessResult {
    const total = data.reduce((sum, sale) => sum + sale.amount, 0);
    const average = total / data.length;
    
    return {
      total,
      average,
      count: data.length,
      type: 'sales'
    };
  }
}
```

#### 4.2 Validar Implementação
```markdown
**Testes unitários para cada classe:**
- [ ] Teste de criação
- [ ] Teste de validação
- [ ] Teste de transformação
- [ ] Teste de análise
- [ ] Teste de integração
- [ ] Teste de edge cases
```

#### 4.3 Documentar Classes Concretas
```markdown
**Documentação de cada classe:**
- [ ] Propósito da classe
- [ ] Funcionalidades específicas
- [ ] Parâmetros específicos
- [ ] Validações específicas
- [ ] Exemplos de uso
- [ ] Limitações conhecidas
```

### **Fase 5: Integração e Testes**

#### 5.1 Integrar Sistema
```markdown
**Integração com sistema existente:**
- [ ] Conectar com sistema existente
- [ ] Implementar inicialização
- [ ] Configurar dependências
- [ ] Atualizar testes existentes
- [ ] Documentar mudanças
```

#### 5.2 Implementar Testes
```typescript
// Exemplo de teste de integração
describe('DataProcessor Template Method', () => {
  let salesProcessor: SalesDataProcessor;
  let inventoryProcessor: InventoryDataProcessor;
  
  beforeEach(() => {
    salesProcessor = new SalesDataProcessor();
    inventoryProcessor = new InventoryDataProcessor();
  });
  
  it('should process sales data correctly', async () => {
    const salesData = {
      sales: [
        { id: 1, amount: '100.00', date: '2024-01-01', customer: 'John' },
        { id: 2, amount: '200.00', date: '2024-01-02', customer: 'Jane' }
      ]
    };
    
    const result = await salesProcessor.process(salesData);
    
    expect(result.total).toBe(300);
    expect(result.average).toBe(150);
    expect(result.count).toBe(2);
    expect(result.type).toBe('sales');
  });
  
  it('should process inventory data correctly', async () => {
    const inventoryData = {
      products: [
        { id: 1, name: 'Product A', quantity: 10, price: 25.00 },
        { id: 2, name: 'Product B', quantity: 5, price: 50.00 }
      ]
    };
    
    const result = await inventoryProcessor.process(inventoryData);
    
    expect(result.totalValue).toBe(500);
    expect(result.productCount).toBe(2);
    expect(result.type).toBe('inventory');
  });
});
```

#### 5.3 Testes de Performance
```markdown
**Testes de performance:**
- [ ] Tempo de execução
- [ ] Uso de memória
- [ ] Escalabilidade
- [ ] Concorrência
- [ ] Garbage collection
```

## 🎯 Boas Práticas

### **1. Design da Classe Abstrata**

#### ✅ **Faça**
```typescript
// Template method bem estruturado
abstract class DataProcessor {
  // Template method - define o esqueleto
  public process(data: any): ProcessResult {
    this.validateInput(data);
    const processedData = this.transformData(data);
    const result = this.analyzeData(processedData);
    this.saveResult(result);
    this.notifyStakeholders(result);
    return result;
  }
  
  // Métodos abstratos para personalização
  protected abstract validateInput(data: any): void;
  protected abstract transformData(data: any): any;
  protected abstract analyzeData(data: any): ProcessResult;
  
  // Métodos comuns implementados
  protected saveResult(result: ProcessResult): void {
    // Implementação comum
  }
  
  protected notifyStakeholders(result: ProcessResult): void {
    // Implementação comum
  }
}
```

#### ❌ **Evite**
```typescript
// Template method mal estruturado
abstract class DataProcessor {
  // Método muito genérico
  public process(data: any): any {
    // Lógica muito complexa
    // Sem separação clara de responsabilidades
    // Difícil de entender e manter
  }
  
  // Métodos abstratos muito genéricos
  abstract doSomething(data: any): any;
  abstract doSomethingElse(data: any): any;
}
```

### **2. Implementação das Classes Concretas**

#### ✅ **Faça**
```typescript
// Implementação concreta bem estruturada
class SalesDataProcessor extends DataProcessor {
  protected validateInput(data: any): void {
    if (!data.sales || !Array.isArray(data.sales)) {
      throw new Error('Dados de vendas inválidos');
    }
    
    // Validações específicas para vendas
    data.sales.forEach(sale => {
      if (!sale.id || !sale.amount || !sale.date) {
        throw new Error('Venda incompleta encontrada');
      }
    });
  }
  
  protected transformData(data: any): any {
    return data.sales.map(sale => ({
      id: sale.id,
      amount: parseFloat(sale.amount),
      date: new Date(sale.date),
      customer: sale.customer
    }));
  }
  
  protected analyzeData(data: any): ProcessResult {
    const total = data.reduce((sum, sale) => sum + sale.amount, 0);
    const average = total / data.length;
    
    return {
      total,
      average,
      count: data.length,
      type: 'sales'
    };
  }
}
```

#### ❌ **Evite**
```typescript
// Implementação concreta mal estruturada
class SalesDataProcessor extends DataProcessor {
  protected validateInput(data: any): void {
    // Validação muito genérica
    if (!data) {
      throw new Error('Dados inválidos');
    }
  }
  
  protected transformData(data: any): any {
    // Transformação muito genérica
    return data;
  }
  
  protected analyzeData(data: any): ProcessResult {
    // Análise muito genérica
    return { type: 'sales' };
  }
}
```

### **3. Tratamento de Erros**

#### ✅ **Faça**
```typescript
// Tratamento de erros específico
abstract class DataProcessor {
  public process(data: any): ProcessResult {
    try {
      this.validateInput(data);
      const processedData = this.transformData(data);
      const result = this.analyzeData(processedData);
      this.saveResult(result);
      this.notifyStakeholders(result);
      return result;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }
  
  protected handleError(error: Error): void {
    console.error('Erro no processamento:', error.message);
    // Lógica comum de tratamento de erros
  }
}
```

#### ❌ **Evite**
```typescript
// Tratamento de erros genérico
abstract class DataProcessor {
  public process(data: any): ProcessResult {
    try {
      // Lógica do processamento
    } catch (error) {
      console.error('Erro:', error);
      throw error;
    }
  }
}
```

### **4. Testes**

#### ✅ **Faça**
```typescript
// Testes específicos para cada classe
describe('SalesDataProcessor', () => {
  let processor: SalesDataProcessor;
  
  beforeEach(() => {
    processor = new SalesDataProcessor();
  });
  
  it('should validate sales data correctly', () => {
    const validData = {
      sales: [
        { id: 1, amount: '100.00', date: '2024-01-01', customer: 'John' }
      ]
    };
    
    expect(() => processor.validateInput(validData)).not.toThrow();
  });
  
  it('should throw error for invalid sales data', () => {
    const invalidData = {
      sales: [
        { id: 1, amount: '100.00' } // Missing date and customer
      ]
    };
    
    expect(() => processor.validateInput(invalidData)).toThrow();
  });
});
```

#### ❌ **Evite**
```typescript
// Testes genéricos
describe('DataProcessor', () => {
  it('should work', () => {
    // Teste genérico que não testa nada específico
  });
});
```

## 🔧 Extensões Avançadas

### **1. Template Method com Hooks**

```typescript
// Template method com hooks para personalização
abstract class DataProcessor {
  public process(data: any): ProcessResult {
    this.beforeProcessing(data);
    
    this.validateInput(data);
    const processedData = this.transformData(data);
    const result = this.analyzeData(processedData);
    
    this.afterProcessing(result);
    
    this.saveResult(result);
    this.notifyStakeholders(result);
    
    return result;
  }
  
  // Hooks para personalização
  protected beforeProcessing(data: any): void {
    // Implementação padrão vazia
  }
  
  protected afterProcessing(result: ProcessResult): void {
    // Implementação padrão vazia
  }
  
  // Métodos abstratos obrigatórios
  protected abstract validateInput(data: any): void;
  protected abstract transformData(data: any): any;
  protected abstract analyzeData(data: any): ProcessResult;
}
```

### **2. Template Method com Strategy**

```typescript
// Template method com strategy para algoritmos intercambiáveis
abstract class DataProcessor {
  protected strategy: ProcessingStrategy;
  
  public process(data: any): ProcessResult {
    this.validateInput(data);
    const processedData = this.transformData(data);
    const result = this.analyzeData(processedData);
    
    // Usar strategy para processamento específico
    const finalResult = this.strategy.process(result);
    
    this.saveResult(finalResult);
    this.notifyStakeholders(finalResult);
    
    return finalResult;
  }
  
  protected abstract validateInput(data: any): void;
  protected abstract transformData(data: any): any;
  protected abstract analyzeData(data: any): ProcessResult;
}

interface ProcessingStrategy {
  process(result: ProcessResult): ProcessResult;
}

class SalesProcessingStrategy implements ProcessingStrategy {
  process(result: ProcessResult): ProcessResult {
    // Lógica específica para vendas
    return result;
  }
}
```

### **3. Template Method com Observer**

```typescript
// Template method com observer para notificações
abstract class DataProcessor {
  private observers: ProcessorObserver[] = [];
  
  public process(data: any): ProcessResult {
    this.notifyObservers('processing_started', data);
    
    this.validateInput(data);
    const processedData = this.transformData(data);
    const result = this.analyzeData(processedData);
    
    this.notifyObservers('processing_completed', result);
    
    this.saveResult(result);
    this.notifyStakeholders(result);
    
    return result;
  }
  
  public addObserver(observer: ProcessorObserver): void {
    this.observers.push(observer);
  }
  
  private notifyObservers(event: string, data: any): void {
    this.observers.forEach(observer => observer.update(event, data));
  }
  
  protected abstract validateInput(data: any): void;
  protected abstract transformData(data: any): any;
  protected abstract analyzeData(data: any): ProcessResult;
}

interface ProcessorObserver {
  update(event: string, data: any): void;
}
```

### **4. Template Method com Factory**

```typescript
// Template method com factory para criação de objetos
abstract class DataProcessor {
  public process(data: any): ProcessResult {
    this.validateInput(data);
    const processedData = this.transformData(data);
    const result = this.analyzeData(processedData);
    
    // Usar factory para criar objetos específicos
    const report = this.createReport(result);
    
    this.saveResult(report);
    this.notifyStakeholders(report);
    
    return report;
  }
  
  protected abstract validateInput(data: any): void;
  protected abstract transformData(data: any): any;
  protected abstract analyzeData(data: any): ProcessResult;
  
  // Factory method para criação de relatórios
  protected abstract createReport(result: ProcessResult): Report;
}

abstract class Report {
  abstract generate(): string;
  abstract save(): void;
}
```

## 🚨 Armadilhas Comuns

### **1. Over-Engineering**

#### ❌ **Problema**
```typescript
// Template method desnecessário para caso simples
abstract class SimpleCalculator {
  public calculate(a: number, b: number): number {
    this.validateInput(a, b);
    const result = this.performCalculation(a, b);
    this.logResult(result);
    return result;
  }
  
  protected abstract performCalculation(a: number, b: number): number;
  
  protected validateInput(a: number, b: number): void {
    if (typeof a !== 'number' || typeof b !== 'number') {
      throw new Error('Invalid input');
    }
  }
  
  protected logResult(result: number): void {
    console.log('Result:', result);
  }
}
```

#### ✅ **Solução**
```typescript
// Solução mais simples para caso simples
class Calculator {
  public add(a: number, b: number): number {
    return a + b;
  }
  
  public subtract(a: number, b: number): number {
    return a - b;
  }
  
  public multiply(a: number, b: number): number {
    return a * b;
  }
  
  public divide(a: number, b: number): number {
    if (b === 0) {
      throw new Error('Division by zero');
    }
    return a / b;
  }
}
```

### **2. Hierarquia Muito Profunda**

#### ❌ **Problema**
```typescript
// Hierarquia muito profunda
abstract class BaseProcessor {
  public process(data: any): any {
    // Template method
  }
}

abstract class DataProcessor extends BaseProcessor {
  // Mais template methods
}

abstract class FileProcessor extends DataProcessor {
  // Mais template methods
}

class TextFileProcessor extends FileProcessor {
  // Implementação específica
}
```

#### ✅ **Solução**
```typescript
// Hierarquia mais simples
abstract class DataProcessor {
  public process(data: any): any {
    // Template method
  }
}

class TextFileProcessor extends DataProcessor {
  // Implementação específica
}

class ImageFileProcessor extends DataProcessor {
  // Implementação específica
}
```

### **3. Métodos Abstratos Muito Genéricos**

#### ❌ **Problema**
```typescript
// Métodos abstratos muito genéricos
abstract class DataProcessor {
  public process(data: any): any {
    this.doStep1(data);
    this.doStep2(data);
    this.doStep3(data);
  }
  
  protected abstract doStep1(data: any): any;
  protected abstract doStep2(data: any): any;
  protected abstract doStep3(data: any): any;
}
```

#### ✅ **Solução**
```typescript
// Métodos abstratos específicos
abstract class DataProcessor {
  public process(data: any): ProcessResult {
    this.validateInput(data);
    const processedData = this.transformData(data);
    const result = this.analyzeData(processedData);
    this.saveResult(result);
    return result;
  }
  
  protected abstract validateInput(data: any): void;
  protected abstract transformData(data: any): any;
  protected abstract analyzeData(data: any): ProcessResult;
}
```

### **4. Falta de Documentação**

#### ❌ **Problema**
```typescript
// Falta de documentação
abstract class DataProcessor {
  public process(data: any): any {
    // Lógica sem documentação
  }
  
  protected abstract validateInput(data: any): void;
  protected abstract transformData(data: any): any;
  protected abstract analyzeData(data: any): any;
}
```

#### ✅ **Solução**
```typescript
// Documentação clara
abstract class DataProcessor {
  /**
   * Template method que define o esqueleto do algoritmo de processamento
   * @param data Dados de entrada para processamento
   * @returns Resultado do processamento
   */
  public process(data: any): ProcessResult {
    this.validateInput(data);
    const processedData = this.transformData(data);
    const result = this.analyzeData(processedData);
    this.saveResult(result);
    return result;
  }
  
  /**
   * Valida os dados de entrada
   * @param data Dados a serem validados
   * @throws Error se os dados forem inválidos
   */
  protected abstract validateInput(data: any): void;
  
  /**
   * Transforma os dados para o formato necessário
   * @param data Dados a serem transformados
   * @returns Dados transformados
   */
  protected abstract transformData(data: any): any;
  
  /**
   * Analisa os dados e gera o resultado
   * @param data Dados a serem analisados
   * @returns Resultado da análise
   */
  protected abstract analyzeData(data: any): ProcessResult;
}
```

## 📊 Métricas e Monitoramento

### **Métricas de Performance**

```typescript
// Decorator para métricas
class MetricsDataProcessor extends DataProcessor {
  constructor(private processor: DataProcessor) {
    super();
  }
  
  public process(data: any): ProcessResult {
    const startTime = Date.now();
    
    try {
      const result = this.processor.process(data);
      
      this.recordMetrics({
        processor: this.processor.constructor.name,
        duration: Date.now() - startTime,
        success: true
      });
      
      return result;
    } catch (error) {
      this.recordMetrics({
        processor: this.processor.constructor.name,
        duration: Date.now() - startTime,
        success: false,
        error: error.message
      });
      
      throw error;
    }
  }
  
  private recordMetrics(metrics: any): void {
    // Registrar métricas
  }
}
```

### **Métricas de Negócio**

```typescript
// Métricas de negócio
interface BusinessMetrics {
  totalProcessed: number;
  successRate: number;
  averageProcessingTime: number;
  errorRate: number;
}
```

### **Métricas Técnicas**

```typescript
// Métricas técnicas
interface TechnicalMetrics {
  classCount: number;
  methodCount: number;
  complexity: number;
  maintainability: number;
}
```

## 🎯 Conclusão

O padrão Template Method é uma solução elegante para eliminar duplicação de código quando múltiplas classes seguem o mesmo algoritmo com pequenas variações. É especialmente útil em sistemas legados onde a duplicação já existe e precisa ser refatorada.

**Lembre-se:**
- Use Template Method quando múltiplas classes têm algoritmos similares
- Evite over-engineering para casos simples
- Implemente tratamento de erros adequado
- Monitore performance e métricas
- Considere extensões avançadas quando necessário
