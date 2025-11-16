# Design Patterns - Documentação

Esta seção contém documentação sobre padrões de projeto (Design Patterns) organizados por categoria e complexidade.

## Estrutura

```
design-patterns/
├── README.md                    # Este arquivo
├── estruturais/                 # Padrões Estruturais
│   ├── decorator/              # Padrão Decorator
│   ├── adapter/                # Padrão Adapter
│   └── facade/                 # Padrão Facade
├── criacionais/                # Padrões Criacionais
│   ├── factory/                # Padrão Factory
│   ├── singleton/              # Padrão Singleton
│   └── builder/                # Padrão Builder
├── comportamentais/            # Padrões Comportamentais
│   ├── observer/               # Padrão Observer
│   ├── strategy/               # Padrão Strategy
│   └── command/                # Padrão Command
├── persistence-patterns/       # Padrões de Persistência
│   ├── README.md               # Visão geral dos padrões
│   ├── transaction-script.md   # Transaction Script Pattern
│   ├── domain-model.md         # Domain Model Pattern
│   ├── dao-data-access-object.md # DAO Pattern
│   ├── table-gateway.md        # Table Gateway Pattern
│   ├── repository.md           # Repository Pattern
│   ├── active-record.md        # Active Record Pattern
│   └── unit-of-work.md         # Unit of Work Pattern
└── exemplos/                    # Exemplos práticos
    ├── java/                   # Exemplos em Java
    ├── python/                 # Exemplos em Python
    ├── typescript/             # Exemplos em TypeScript
    └── csharp/                 # Exemplos em C#
```

## Categorias de Padrões

### Padrões Estruturais
Padrões que lidam com a composição de classes e objetos para formar estruturas maiores e mais flexíveis.

### Padrões Criacionais
Padrões que lidam com a criação de objetos, fornecendo flexibilidade na criação e composição de objetos.

### Padrões Comportamentais
Padrões que se concentram na comunicação entre objetos e na distribuição de responsabilidades.

### Padrões de Persistência
Padrões que organizam a lógica de acesso a dados e persistência, desde abordagens simples até arquiteturas complexas que preservam a integridade do domínio.

**Documentação completa**: [Persistence Patterns](./persistence-patterns/README.md)

**Padrões disponíveis**:
- [Transaction Script](./persistence-patterns/transaction-script.md) - Organiza lógica em procedimentos
- [Domain Model](./persistence-patterns/domain-model.md) - Incorpora dados e comportamento
- [DAO (Data Access Object)](./persistence-patterns/dao-data-access-object.md) - Encapsula acesso a dados
- [Table Gateway](./persistence-patterns/table-gateway.md) - Gateway para tabela do banco
- [Repository](./persistence-patterns/repository.md) - Interface orientada a objetos para domínio
- [Active Record](./persistence-patterns/active-record.md) - Objeto que encapsula linha da tabela
- [Unit of Work](./persistence-patterns/unit-of-work.md) - Coordena transações e mudanças

## Princípios Fundamentais

- **Open/Closed Principle**: Classes devem estar abertas para extensão e fechadas para modificação
- **Single Responsibility Principle**: Uma classe deve ter apenas uma razão para mudar
- **Dependency Inversion Principle**: Dependa de abstrações, não de implementações concretas
- **Interface Segregation Principle**: Interfaces específicas são melhores que interfaces genéricas

## Como Usar Esta Documentação

1. **Navegue pela categoria** que melhor se adequa ao seu problema
2. **Leia a documentação** do padrão específico
3. **Analise os exemplos** de código fornecidos
4. **Implemente** seguindo as boas práticas documentadas
5. **Adapte** o padrão às necessidades específicas do seu projeto

## Contribuição

Para adicionar novos padrões ou melhorar a documentação existente:

1. Siga a estrutura de pastas estabelecida
2. Use os templates fornecidos
3. Inclua exemplos práticos e casos de uso
4. Documente prós e contras de cada padrão
5. Mantenha consistência na formatação

---

**Última atualização**: 2025-11-16
**Versão**: 2.0
**Autor**: Sistema de Documentação Skynet
**Nota**: Adicionada seção de Padrões de Persistência baseada em transcrição de live sobre o tema

