# Padrão Decorator

## Visão Geral

O **Decorator** é um padrão de projeto estrutural que permite adicionar novos comportamentos a objetos dinamicamente, sem alterar sua estrutura original. É um dos padrões mais flexíveis e poderosos, utilizando o conceito de **composição recursiva**.

## Definição

O padrão Decorator permite estender funcionalidades de um objeto de forma dinâmica, envolvendo-o com objetos decoradores que adicionam comportamentos específicos, mantendo a interface original intacta.

## Nomes Alternativos

- **Decorator** (padrão)
- **Wrapper** (envoltório)
- **Envoltório** (tradução)

## Propósito

- Adicionar funcionalidades a objetos sem modificar suas classes
- Seguir o princípio **Open/Closed** (aberto para extensão, fechado para modificação)
- Permitir composição de funcionalidades de forma flexível
- Evitar a explosão de subclasses

## Princípios Relacionados

### Open/Closed Principle
- **Aberto para extensão**: Novos decoradores podem ser criados facilmente
- **Fechado para modificação**: A classe original não é alterada

### Single Responsibility Principle
- Cada decorador tem uma responsabilidade específica
- Funcionalidades são separadas em classes distintas

## Estrutura do Padrão

```
Component (Interface)
    ↓
ConcreteComponent (Implementação base)
    ↓
Decorator (Classe abstrata)
    ↓
ConcreteDecoratorA, ConcreteDecoratorB, etc.
```

## Analogia do Mundo Real

Imagine um personagem que precisa de diferentes equipamentos:

1. **Personagem base** (funcionalidade básica)
2. **Casaco** (decorador para proteção contra frio)
3. **Capa de chuva** (decorador para proteção contra chuva)
4. **Chapéu** (decorador para proteção contra sol)

Cada equipamento adiciona uma funcionalidade específica sem modificar o personagem original.

## Vantagens

- ✅ **Flexibilidade**: Funcionalidades podem ser adicionadas/removidas dinamicamente
- ✅ **Reutilização**: Decoradores podem ser reutilizados em diferentes contextos
- ✅ **Composição**: Múltiplos decoradores podem ser combinados
- ✅ **Ordem flexível**: Decoradores podem ser aplicados em qualquer ordem
- ✅ **Princípio Open/Closed**: Não modifica classes existentes

## Desvantagens

- ❌ **Complexidade**: Pode criar muitas classes pequenas
- ❌ **Debugging**: Pode ser difícil rastrear problemas em cadeias de decoradores
- ❌ **Performance**: Múltiplas camadas podem impactar performance
- ❌ **Ordem**: A ordem dos decoradores pode afetar o resultado

## Quando Usar

- Quando você precisa adicionar funcionalidades a objetos dinamicamente
- Quando herança não é uma opção adequada
- Quando você quer evitar a explosão de subclasses
- Quando funcionalidades precisam ser combinadas de forma flexível
- Quando você quer seguir o princípio Open/Closed

## Quando NÃO Usar

- Quando as funcionalidades são mutuamente exclusivas
- Quando a ordem dos decoradores é crítica e não pode ser alterada
- Quando você tem poucos decoradores e eles raramente mudam
- Quando performance é crítica e múltiplas camadas são problemáticas

## Exemplo Prático: Processador de Imagens

### Problema
Sistema de upload de imagens que precisa de diferentes processamentos:
- Processamento básico (validação, metadados)
- Adição de marca d'água
- Redimensionamento
- Aplicação de filtros

### Solução com Decorator

```typescript
// Interface base
interface ImageProcessor {
  process(imagePath: string): string;
}

// Implementação concreta
class BasicImageProcessor implements ImageProcessor {
  process(imagePath: string): string {
    // Validação básica, verificação de metadados
    console.log(`Processando imagem básica: ${imagePath}`);
    return `processed_${imagePath}`;
  }
}

// Decorator abstrato
abstract class ImageProcessorDecorator implements ImageProcessor {
  protected processor: ImageProcessor;

  constructor(processor: ImageProcessor) {
    this.processor = processor;
  }

  abstract process(imagePath: string): string;
}

// Decorador concreto - Marca d'água
class WatermarkDecorator extends ImageProcessorDecorator {
  private watermarkText: string;

  constructor(processor: ImageProcessor, watermarkText: string) {
    super(processor);
    this.watermarkText = watermarkText;
  }

  process(imagePath: string): string {
    // Primeiro processa a imagem base
    const processedPath = this.processor.process(imagePath);
    
    // Depois adiciona a marca d'água
    console.log(`Adicionando marca d'água: ${this.watermarkText}`);
    return `watermarked_${processedPath}`;
  }
}

// Decorador concreto - Redimensionamento
class ResizeDecorator extends ImageProcessorDecorator {
  private width: number;
  private height: number;

  constructor(processor: ImageProcessor, width: number, height: number) {
    super(processor);
    this.width = width;
    this.height = height;
  }

  process(imagePath: string): string {
    // Primeiro processa a imagem base
    const processedPath = this.processor.process(imagePath);
    
    // Depois redimensiona
    console.log(`Redimensionando para ${this.width}x${this.height}`);
    return `resized_${processedPath}`;
  }
}

// Uso do padrão
function main() {
  // Processamento básico
  let processor: ImageProcessor = new BasicImageProcessor();
  
  // Adicionando marca d'água
  processor = new WatermarkDecorator(processor, "Minha Empresa");
  
  // Adicionando redimensionamento
  processor = new ResizeDecorator(processor, 800, 600);
  
  // Processando a imagem
  const result = processor.process("image.jpg");
  console.log(`Resultado: ${result}`);
  // Output: Resultado: resized_watermarked_processed_image.jpg
}
```

## Composição Recursiva

O conceito de **composição recursiva** é fundamental no padrão Decorator:

1. **Objeto base** é envolvido pelo primeiro decorador
2. **Resultado** é envolvido pelo segundo decorador
3. **Processo continua** até todos os decoradores serem aplicados
4. **Execução** acontece de dentro para fora (recursivamente)

### Fluxo de Execução

```
ResizeDecorator.process()
  └── WatermarkDecorator.process()
      └── BasicImageProcessor.process()
          └── [Processamento básico]
      └── [Adiciona marca d'água]
  └── [Redimensiona]
```

## Flexibilidade de Ordem

Uma das grandes vantagens do Decorator é a flexibilidade na ordem dos decoradores:

```typescript
// Ordem 1: Marca d'água → Redimensionamento
let processor1 = new ResizeDecorator(
  new WatermarkDecorator(
    new BasicImageProcessor(), 
    "Empresa"
  ), 
  800, 600
);

// Ordem 2: Redimensionamento → Marca d'água
let processor2 = new WatermarkDecorator(
  new ResizeDecorator(
    new BasicImageProcessor(), 
    800, 600
  ), 
  "Empresa"
);
```

## Casos de Uso Comuns

### 1. Streams de Dados
- Compressão
- Criptografia
- Buffering
- Logging

### 2. Interface Gráfica
- Bordas
- Scrollbars
- Tooltips
- Animações

### 3. Middleware Web
- Autenticação
- Logging
- Caching
- Rate limiting

### 4. Processamento de Arquivos
- Validação
- Transformação
- Compressão
- Criptografia

## Implementação em Diferentes Linguagens

### Java
```java
// Interface
public interface Coffee {
    String getDescription();
    double getCost();
}

// Implementação base
public class SimpleCoffee implements Coffee {
    public String getDescription() {
        return "Simple coffee";
    }
    
    public double getCost() {
        return 1.0;
    }
}

// Decorator abstrato
public abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;
    
    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }
}

// Decorador concreto
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }
    
    public String getDescription() {
        return coffee.getDescription() + ", milk";
    }
    
    public double getCost() {
        return coffee.getCost() + 0.5;
    }
}
```

### Python
```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def get_description(self):
        pass
    
    @abstractmethod
    def get_cost(self):
        pass

class SimpleCoffee(Coffee):
    def get_description(self):
        return "Simple coffee"
    
    def get_cost(self):
        return 1.0

class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self.coffee = coffee

class MilkDecorator(CoffeeDecorator):
    def get_description(self):
        return self.coffee.get_description() + ", milk"
    
    def get_cost(self):
        return self.coffee.get_cost() + 0.5
```

## Boas Práticas

### 1. Interface Consistente
- Mantenha a mesma interface entre o componente base e os decoradores
- Use interfaces ou classes abstratas para garantir consistência

### 2. Composição Simples
- Evite decoradores muito complexos
- Mantenha cada decorador focado em uma responsabilidade

### 3. Documentação Clara
- Documente a ordem esperada dos decoradores quando relevante
- Explique as dependências entre decoradores

### 4. Testes
- Teste cada decorador individualmente
- Teste combinações de decoradores
- Teste diferentes ordens quando aplicável

### 5. Performance
- Considere o impacto de múltiplas camadas
- Use lazy loading quando apropriado
- Monitore o uso de memória

## Padrões Relacionados

### Adapter
- Ambos envolvem objetos
- Adapter muda a interface, Decorator mantém a interface

### Composite
- Ambos usam composição
- Composite representa hierarquias, Decorator adiciona funcionalidades

### Strategy
- Ambos permitem mudança de comportamento
- Strategy troca algoritmos, Decorator adiciona funcionalidades

## Conclusão

O padrão Decorator é uma ferramenta poderosa para adicionar funcionalidades de forma flexível e dinâmica. Sua principal vantagem é a capacidade de combinar funcionalidades sem modificar código existente, seguindo o princípio Open/Closed.

Quando usado corretamente, o Decorator pode tornar o código mais modular, testável e flexível, permitindo que novas funcionalidades sejam adicionadas sem quebrar o sistema existente.

---

**Referências:**
- Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four)
- Head First Design Patterns
- Clean Code - Robert C. Martin

**Última atualização**: 04/10/2025
**Versão**: 1.0

