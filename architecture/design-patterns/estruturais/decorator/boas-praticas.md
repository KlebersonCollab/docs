# Boas Práticas do Padrão Decorator

## Visão Geral

Este documento apresenta as melhores práticas para implementar e usar o padrão Decorator de forma eficaz, evitando armadilhas comuns e maximizando os benefícios do padrão.

## 1. Design e Arquitetura

### 1.1 Interface Consistente
**✅ FAÇA**: Mantenha a mesma interface entre o componente base e os decoradores

```typescript
// ✅ Bom: Interface consistente
interface DataProcessor {
  process(data: any): any;
  getMetadata(): object;
}

class BasicProcessor implements DataProcessor {
  process(data: any): any { /* ... */ }
  getMetadata(): object { /* ... */ }
}

class LoggingDecorator implements DataProcessor {
  process(data: any): any { /* ... */ }
  getMetadata(): object { /* ... */ }
}
```

**❌ EVITE**: Interfaces inconsistentes

```typescript
// ❌ Ruim: Interfaces diferentes
interface BasicProcessor {
  process(data: any): any;
}

interface LoggingDecorator {
  process(data: any): any;
  log(message: string): void; // Método extra quebra a consistência
}
```

### 1.2 Composição Simples
**✅ FAÇA**: Mantenha decoradores simples e focados

```typescript
// ✅ Bom: Decorador simples e focado
class ValidationDecorator {
  constructor(private processor: DataProcessor) {}
  
  process(data: any): any {
    this.validate(data);
    return this.processor.process(data);
  }
  
  private validate(data: any): void {
    // Lógica de validação simples
  }
}
```

**❌ EVITE**: Decoradores complexos com múltiplas responsabilidades

```typescript
// ❌ Ruim: Decorador com muitas responsabilidades
class ComplexDecorator {
  process(data: any): any {
    this.validate(data);
    this.log(data);
    this.compress(data);
    this.encrypt(data);
    this.cache(data);
    // ... muitas responsabilidades
  }
}
```

### 1.3 Hierarquia Clara
**✅ FAÇA**: Use classes abstratas para decoradores base

```typescript
// ✅ Bom: Hierarquia clara
abstract class DataProcessorDecorator implements DataProcessor {
  constructor(protected processor: DataProcessor) {}
  
  abstract process(data: any): any;
  
  getMetadata(): object {
    return this.processor.getMetadata();
  }
}
```

**❌ EVITE**: Herança desnecessária ou confusa

```typescript
// ❌ Ruim: Herança desnecessária
class LoggingDecorator extends ValidationDecorator {
  // Herda validação desnecessariamente
}
```

## 2. Implementação

### 2.1 Construtores Consistentes
**✅ FAÇA**: Use construtores consistentes

```typescript
// ✅ Bom: Construtor consistente
class EncryptionDecorator extends DataProcessorDecorator {
  constructor(
    processor: DataProcessor,
    private key: string
  ) {
    super(processor);
  }
}
```

**❌ EVITE**: Construtores inconsistentes

```typescript
// ❌ Ruim: Construtor inconsistente
class EncryptionDecorator {
  constructor(processor: DataProcessor) {
    this.processor = processor;
    this.key = "default"; // Hardcoded
  }
}
```

### 2.2 Delegação Adequada
**✅ FAÇA**: Delegue corretamente para o componente base

```typescript
// ✅ Bom: Delegação adequada
class LoggingDecorator extends DataProcessorDecorator {
  process(data: any): any {
    console.log("Entrada:", data);
    const result = this.processor.process(data);
    console.log("Saída:", result);
    return result;
  }
}
```

**❌ EVITE**: Não delegar ou delegar incorretamente

```typescript
// ❌ Ruim: Não delega
class LoggingDecorator {
  process(data: any): any {
    console.log("Entrada:", data);
    return data; // Não processa!
  }
}
```

### 2.3 Tratamento de Erros
**✅ FAÇA**: Trate erros adequadamente

```typescript
// ✅ Bom: Tratamento de erros
class RetryDecorator extends DataProcessorDecorator {
  process(data: any): any {
    for (let i = 0; i < this.maxRetries; i++) {
      try {
        return this.processor.process(data);
      } catch (error) {
        if (i === this.maxRetries - 1) throw error;
        this.wait(this.delay);
      }
    }
  }
}
```

**❌ EVITE**: Ignorar erros ou tratá-los inadequadamente

```typescript
// ❌ Ruim: Ignora erros
class RetryDecorator {
  process(data: any): any {
    return this.processor.process(data); // Sem tratamento de erro
  }
}
```

## 3. Nomenclatura

### 3.1 Nomes Descritivos
**✅ FAÇA**: Use nomes que descrevam a funcionalidade

```typescript
// ✅ Bom: Nomes descritivos
class CompressionDecorator { }
class EncryptionDecorator { }
class ValidationDecorator { }
class LoggingDecorator { }
```

**❌ EVITE**: Nomes genéricos ou confusos

```typescript
// ❌ Ruim: Nomes genéricos
class Decorator1 { }
class Wrapper { }
class Processor { }
```

### 3.2 Sufixos Consistentes
**✅ FAÇA**: Use sufixos consistentes

```typescript
// ✅ Bom: Sufixos consistentes
class DataProcessorDecorator { }
class ImageProcessorDecorator { }
class NotificationDecorator { }
```

**❌ EVITE**: Sufixos inconsistentes

```typescript
// ❌ Ruim: Sufixos inconsistentes
class DataProcessorDecorator { }
class ImageWrapper { }
class NotificationEnhancer { }
```

## 4. Documentação

### 4.1 Documentação Clara
**✅ FAÇA**: Documente o propósito e uso de cada decorador

```typescript
/**
 * Decorador que adiciona compressão aos dados processados
 * 
 * @param processor - Processador base
 * @param level - Nível de compressão (1-9)
 * @param algorithm - Algoritmo de compressão
 */
class CompressionDecorator extends DataProcessorDecorator {
  constructor(
    processor: DataProcessor,
    private level: number = 6,
    private algorithm: string = 'gzip'
  ) {
    super(processor);
  }
}
```

**❌ EVITE**: Documentação ausente ou confusa

```typescript
// ❌ Ruim: Sem documentação
class CompressionDecorator {
  constructor(processor: DataProcessor, level: number) {
    this.processor = processor;
    this.level = level;
  }
}
```

### 4.2 Exemplos de Uso
**✅ FAÇA**: Forneça exemplos de uso

```typescript
/**
 * Exemplo de uso:
 * 
 * const processor = new CompressionDecorator(
 *   new EncryptionDecorator(
 *     new BasicProcessor()
 *   ),
 *   9
 * );
 */
class CompressionDecorator { }
```

## 5. Testes

### 5.1 Testes Unitários
**✅ FAÇA**: Teste cada decorador isoladamente

```typescript
// ✅ Bom: Teste unitário
describe('CompressionDecorator', () => {
  it('should compress data', () => {
    const mockProcessor = jest.fn().mockReturnValue('processed');
    const decorator = new CompressionDecorator(mockProcessor, 9);
    
    const result = decorator.process('data');
    
    expect(mockProcessor).toHaveBeenCalledWith('data');
    expect(result).toContain('compressed');
  });
});
```

**❌ EVITE**: Testes complexos ou acoplados

```typescript
// ❌ Ruim: Teste acoplado
describe('ComplexTest', () => {
  it('should work with all decorators', () => {
    const processor = new CompressionDecorator(
      new EncryptionDecorator(
        new ValidationDecorator(
          new BasicProcessor()
        )
      )
    );
    // Teste muito complexo
  });
});
```

### 5.2 Testes de Integração
**✅ FAÇA**: Teste combinações de decoradores

```typescript
// ✅ Bom: Teste de integração
describe('Decorator Combinations', () => {
  it('should work with compression and encryption', () => {
    const processor = new CompressionDecorator(
      new EncryptionDecorator(
        new BasicProcessor()
      )
    );
    
    const result = processor.process('test data');
    expect(result).toBeDefined();
  });
});
```

## 6. Performance

### 6.1 Lazy Loading
**✅ FAÇA**: Use lazy loading quando apropriado

```typescript
// ✅ Bom: Lazy loading
class CacheDecorator extends DataProcessorDecorator {
  private cache: Map<string, any> = new Map();
  
  process(data: any): any {
    const key = this.generateKey(data);
    
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    
    const result = this.processor.process(data);
    this.cache.set(key, result);
    return result;
  }
}
```

**❌ EVITE**: Carregamento desnecessário

```typescript
// ❌ Ruim: Carregamento desnecessário
class CacheDecorator {
  private cache: Map<string, any> = new Map();
  private allData: any[] = []; // Carrega tudo na inicialização
  
  constructor(processor: DataProcessor) {
    this.processor = processor;
    this.loadAllData(); // Desnecessário
  }
}
```

### 6.2 Memória
**✅ FAÇA**: Gerencie memória adequadamente

```typescript
// ✅ Bom: Gerenciamento de memória
class CacheDecorator extends DataProcessorDecorator {
  private cache: Map<string, any> = new Map();
  private maxSize: number;
  
  constructor(processor: DataProcessor, maxSize: number = 100) {
    super(processor);
    this.maxSize = maxSize;
  }
  
  process(data: any): any {
    if (this.cache.size >= this.maxSize) {
      this.evictOldest();
    }
    // ... resto da implementação
  }
}
```

## 7. Configuração

### 7.1 Configuração Flexível
**✅ FAÇA**: Use configuração flexível

```typescript
// ✅ Bom: Configuração flexível
class LoggingDecorator extends DataProcessorDecorator {
  constructor(
    processor: DataProcessor,
    private config: LoggingConfig = {}
  ) {
    super(processor);
  }
}

interface LoggingConfig {
  level?: 'debug' | 'info' | 'warn' | 'error';
  format?: 'json' | 'text';
  destination?: 'console' | 'file' | 'network';
}
```

**❌ EVITE**: Configuração hardcoded

```typescript
// ❌ Ruim: Configuração hardcoded
class LoggingDecorator extends DataProcessorDecorator {
  constructor(processor: DataProcessor) {
    super(processor);
    this.level = 'info'; // Hardcoded
    this.format = 'json'; // Hardcoded
  }
}
```

### 7.2 Validação de Configuração
**✅ FAÇA**: Valide configurações

```typescript
// ✅ Bom: Validação de configuração
class CompressionDecorator extends DataProcessorDecorator {
  constructor(
    processor: DataProcessor,
    private level: number = 6
  ) {
    super(processor);
    this.validateLevel(level);
  }
  
  private validateLevel(level: number): void {
    if (level < 1 || level > 9) {
      throw new Error('Compression level must be between 1 and 9');
    }
  }
}
```

## 8. Debugging

### 8.1 Logging Adequado
**✅ FAÇA**: Use logging para debugging

```typescript
// ✅ Bom: Logging para debugging
class LoggingDecorator extends DataProcessorDecorator {
  process(data: any): any {
    console.log(`[${this.constructor.name}] Processing:`, data);
    const start = Date.now();
    
    const result = this.processor.process(data);
    
    const duration = Date.now() - start;
    console.log(`[${this.constructor.name}] Completed in ${duration}ms`);
    
    return result;
  }
}
```

### 8.2 Identificação de Decoradores
**✅ FAÇA**: Identifique decoradores na cadeia

```typescript
// ✅ Bom: Identificação de decoradores
class DataProcessorDecorator {
  getDecoratorChain(): string[] {
    const chain = [this.constructor.name];
    if (this.processor instanceof DataProcessorDecorator) {
      chain.push(...this.processor.getDecoratorChain());
    }
    return chain;
  }
}
```

## 9. Ordem e Dependências

### 9.1 Documentar Dependências
**✅ FAÇA**: Documente dependências entre decoradores

```typescript
/**
 * EncryptionDecorator deve ser aplicado antes de CompressionDecorator
 * para evitar compressão de dados já criptografados
 */
class EncryptionDecorator extends DataProcessorDecorator {
  // ...
}
```

### 9.2 Validação de Ordem
**✅ FAÇA**: Valide ordem quando necessário

```typescript
// ✅ Bom: Validação de ordem
class CompressionDecorator extends DataProcessorDecorator {
  constructor(processor: DataProcessor) {
    super(processor);
    this.validateOrder();
  }
  
  private validateOrder(): void {
    if (this.processor instanceof EncryptionDecorator) {
      throw new Error('CompressionDecorator must come before EncryptionDecorator');
    }
  }
}
```

## 10. Refatoração

### 10.1 Extrair Decoradores
**✅ FAÇA**: Extraia decoradores quando apropriado

```typescript
// ✅ Bom: Extrair decorador
class RetryDecorator extends DataProcessorDecorator {
  constructor(
    processor: DataProcessor,
    private maxRetries: number = 3,
    private delay: number = 1000
  ) {
    super(processor);
  }
  
  process(data: any): any {
    for (let i = 0; i < this.maxRetries; i++) {
      try {
        return this.processor.process(data);
      } catch (error) {
        if (i === this.maxRetries - 1) throw error;
        this.wait(this.delay);
      }
    }
  }
  
  private wait(ms: number): void {
    // Implementação do wait
  }
}
```

### 10.2 Simplificar Decoradores
**✅ FAÇA**: Simplifique decoradores complexos

```typescript
// ✅ Bom: Decorador simples
class ValidationDecorator extends DataProcessorDecorator {
  process(data: any): any {
    this.validate(data);
    return this.processor.process(data);
  }
  
  private validate(data: any): void {
    if (!data) {
      throw new Error('Data cannot be null');
    }
  }
}
```

## Conclusão

Seguir essas boas práticas ajudará a criar implementações do padrão Decorator que são:

- **Manuteníveis**: Fáceis de entender e modificar
- **Testáveis**: Fáceis de testar isoladamente
- **Reutilizáveis**: Podem ser reutilizados em diferentes contextos
- **Performantes**: Eficientes em termos de recursos
- **Flexíveis**: Podem ser combinados de forma flexível

Lembre-se de que o padrão Decorator é uma ferramenta poderosa, mas deve ser usada com sabedoria. Nem sempre é a melhor solução para todos os problemas, mas quando aplicado corretamente, pode tornar o código muito mais flexível e manutenível.

---

**Última atualização**: 04/10/2025
**Versão**: 1.0

