# Princípio da Substituição de Liskov (LSP)

## Informações Básicas
- **ID do Documento**: LSP-001
- **Nome**: Princípio da Substituição de Liskov
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

O Princípio da Substituição de Liskov (LSP) é um dos cinco princípios SOLID da programação orientada a objetos, criado por Bárbara Liskov em 1987 e popularizado por Robert C. Martin (Uncle Bob) nos anos 2000.

### Definição Original

> "Seja q(x) uma propriedade que se pode provar do objeto x do tipo T. Então q(y) também é possível provar para o objeto y do tipo S sendo S um subtipo de T." - Bárbara Liskov (1987)

### Princípio Fundamental

**Classes filhas ou classes derivadas nunca devem infringir comportamentos e definições de tipo da classe base ou da interface que implementam.**

## Conceitos Centrais

### 1. Substituibilidade
- Objetos de uma superclasse devem ser substituíveis por objetos de suas subclasses
- O código cliente não deve quebrar ao fazer essa substituição
- O comportamento esperado deve ser mantido

### 2. Contratos e Interfaces
- Interfaces definem contratos que devem ser respeitados
- Implementações não podem violar esses contratos
- Comportamento deve ser consistente entre implementações

### 3. Polimorfismo Seguro
- O polimorfismo deve funcionar sem surpresas
- Código cliente deve ser agnóstico à implementação específica
- Substituições devem ser transparentes

## Três Níveis de Violação

O LSP pode ser violado em três níveis distintos:

### 1. Pós-condições
- **Definição**: Condições que devem ser verdadeiras após a execução de um método
- **Violação**: Retornar valores ou comportamentos inesperados
- **Impacto**: Código cliente recebe dados em formato diferente do esperado

### 2. Pré-condições
- **Definição**: Condições que devem ser verdadeiras antes da execução de um método
- **Violação**: Endurecer restrições em subclasses
- **Impacto**: Código cliente não consegue usar a subclasse onde usava a superclasse

### 3. Invariância
- **Definição**: Propriedades que devem ser mantidas durante toda a vida do objeto
- **Violação**: Alterar regras de negócio fundamentais
- **Impacto**: Comportamento inconsistente entre classes da mesma hierarquia

## Exemplo Conceitual

### O Problema do Pato
> "Se parece com um pato, faz barulho de pato, mas precisa de bateria para funcionar, então muito provavelmente não é um pato."

Este exemplo ilustra como uma abstração incorreta pode quebrar o LSP:
- **Aparência**: Implementa a interface corretamente
- **Comportamento**: Produz o som esperado
- **Dependências**: Requer recursos não esperados (bateria)

## Benefícios do LSP

### 1. Código Mais Robusto
- Substituições seguras entre implementações
- Menor acoplamento entre componentes
- Maior confiabilidade do sistema

### 2. Facilita Testes
- Mocks e stubs funcionam corretamente
- Testes de integração mais simples
- Isolamento de dependências

### 3. Melhora Manutenibilidade
- Mudanças em implementações não afetam clientes
- Extensibilidade sem quebrar código existente
- Refatoração mais segura

## Relação com Outros Princípios SOLID

### Single Responsibility Principle (SRP)
- LSP ajuda a manter responsabilidades bem definidas
- Evita que classes tenham múltiplas responsabilidades conflitantes

### Open/Closed Principle (OCP)
- LSP permite extensão sem modificação
- Novas implementações podem ser adicionadas sem quebrar código existente

### Interface Segregation Principle (ISP)
- LSP trabalha em conjunto com ISP
- Interfaces bem segregadas facilitam implementações que respeitam LSP

### Dependency Inversion Principle (DIP)
- LSP garante que abstrações funcionem corretamente
- Dependências de abstrações são mais seguras com LSP

## Sinais de Violação do LSP

### 1. Código Cliente com Conhecimento de Implementação
```typescript
// ❌ Violação do LSP
if (reportGenerator instanceof S3ReportGenerator) {
  // Lógica específica para S3
} else {
  // Lógica para outros tipos
}
```

### 2. Exceções Inesperadas
```typescript
// ❌ Violação do LSP
try {
  const result = account.deposit(5); // Funciona na superclasse
} catch (error) {
  // Falha na subclasse com mesmo valor
}
```

### 3. Comportamentos Inconsistentes
```typescript
// ❌ Violação do LSP
const localFile = csvGenerator.generate(); // Retorna caminho local
const cloudFile = s3Generator.generate(); // Retorna URL
// Código cliente precisa tratar diferentemente
```

## Boas Práticas

### 1. Design por Contrato
- Defina contratos claros e específicos
- Documente pré-condições e pós-condições
- Use interfaces bem definidas

### 2. Testes de Substituição
- Teste todas as implementações com o mesmo código cliente
- Verifique se comportamentos são consistentes
- Valide que exceções são as mesmas

### 3. Refatoração Cuidadosa
- Quando violar LSP, refatore a hierarquia
- Considere composição ao invés de herança
- Separe responsabilidades em interfaces diferentes

## Ferramentas e Técnicas

### 1. Análise Estática
- Use ferramentas que detectam violações de LSP
- Configure regras de qualidade de código
- Monitore métricas de acoplamento

### 2. Testes Automatizados
- Implemente testes de contrato
- Use property-based testing
- Valide substituições em testes de integração

### 3. Code Review
- Revise hierarquias de herança
- Verifique implementações de interfaces
- Valide contratos entre classes

## Conclusão

O Princípio da Substituição de Liskov é fundamental para criar sistemas robustos e maintíveis. Ele garante que o polimorfismo funcione corretamente e que o código cliente seja independente de implementações específicas.

### Pontos-Chave
- **Substituibilidade**: Objetos devem ser intercambiáveis
- **Contratos**: Interfaces devem ser respeitadas
- **Comportamento**: Consistência entre implementações
- **Testes**: Validação de substituições

### Próximos Passos
- [Estudar violações de pós-condições](./liskov-post-conditions.md)
- [Estudar violações de pré-condições](./liskov-pre-conditions.md)
- [Estudar violações de invariância](./liskov-invariants.md)
- [Aplicar boas práticas](./liskov-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
