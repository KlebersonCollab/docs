# Persistence Patterns - Padrões de Persistência

## 📋 Informações do Documento

- **Tipo**: Documentação de Padrões Arquiteturais
- **Categoria**: Design Patterns - Persistência
- **Versão**: 1.0
- **Data**: 2025-11-16
- **Autor**: Baseado em transcrição de live sobre Padrões de Persistência
- **Revisado por**: Equipe Skynet

## 🎯 Visão Geral

Os padrões de persistência são fundamentais para o desenvolvimento de aplicações que interagem com bancos de dados. Esta documentação explora os principais padrões utilizados para organizar a lógica de acesso a dados, desde abordagens simples até arquiteturas mais complexas que preservam a integridade do domínio.

## 📚 Padrões Documentados

### Padrões Principais (Completos)

### 1. Transaction Script
Padrão simples onde a lógica de negócio é organizada em procedimentos que manipulam dados diretamente.

- [Guia Completo](./transaction-script.md)
- [Exemplos Práticos](./exemplos/transaction-script/)

### 2. Domain Model
Padrão que incorpora dados e comportamento em objetos de domínio, preservando invariâncias e regras de negócio.

- [Guia Completo](./domain-model.md)
- [Exemplos Práticos](./exemplos/domain-model/)

### 3. Data Access Object (DAO)
Padrão que encapsula o acesso a uma fonte de dados, abstraindo detalhes de implementação.

- [Guia Completo](./dao-data-access-object.md)
- [Exemplos Práticos](./exemplos/dao/)

### 4. Table Gateway
Padrão que atua como um gateway para uma tabela do banco de dados, encapsulando operações sobre registros.

- [Guia Completo](./table-gateway.md)
- [Exemplos Práticos](./exemplos/table-gateway/)

### 5. Repository
Padrão que fornece uma interface orientada a objetos para acessar objetos de domínio, abstraindo detalhes de persistência.

- [Guia Completo](./repository.md)
- [Exemplos Práticos](./exemplos/repository/)

### 6. Active Record
Padrão onde um objeto encapsula uma linha de uma tabela ou view, incluindo acesso a dados e comportamento de domínio.

- [Guia Completo](./active-record.md)
- [Exemplos Práticos](./exemplos/active-record/)

### 7. Unit of Work
Padrão que mantém uma lista de objetos afetados por uma transação e coordena a escrita de mudanças.

- [Guia Completo](./unit-of-work.md)
- [Exemplos Práticos](./exemplos/unit-of-work/)

## 📊 Análise de Cobertura

Para verificar quais padrões estão documentados e quais ainda faltam, consulte:

- [Análise Completa de Cobertura](./ANALISE_COBERTURA.md)
- [Análise de Similaridade e Relevância](./ANALISE_SIMILARIDADE.md) - **Verifica se faz sentido documentar padrões adicionais**

### Status Atual
- ✅ **7 padrões principais** completamente documentados
- ⚠️ **3 padrões mencionados** na live (parcialmente cobertos)
- ❌ **~17 padrões adicionais** do livro de Martin Fowler (não documentados)

### Próximos Padrões a Documentar (Alta Prioridade)

**Baseado na análise de similaridade, os seguintes padrões FAZEM SENTIDO documentar separadamente:**

1. ✅ **DTO (Data Transfer Object)** - Padrão fundamental usado em todos os padrões
2. ✅ **Query Object** - Alternativa importante a Repository para consultas complexas
3. ✅ **Identity Map** - Otimização importante de performance
4. ✅ **Data Mapper** - Padrão fundamental do livro de Martin Fowler
5. ⚠️ **Lazy/Eager Loading** - Estratégias de carregamento (pode ser seção em Repository)

**Padrões que NÃO fazem sentido documentar separadamente:**
- ❌ Service Layer - Não é padrão de persistência (já coberto em DDD como Application Service)
- ❌ Row Data Gateway - Muito similar ao Table Gateway (integrar como seção)
- ❌ Padrões de mapeamento específicos - Integrar em Data Mapper quando criado
- ❌ Identity Field - Conceito básico já coberto
- ❌ Serialized LOB, Metadata Mapping - Casos muito específicos ou técnicos demais

## 🔄 Evolução dos Padrões

A transcrição da live demonstra uma evolução natural dos padrões, começando com código sem design definido e progredindo para arquiteturas mais sofisticadas:

```
Sem Design → Transaction Script → DAO → Domain Model + Repository → Active Record
```

### Versão 1: Sem Design
- Código misturado (HTTP + SQL + Lógica de Negócio)
- Alto acoplamento
- Difícil de testar
- Sem separação de responsabilidades

### Versão 2: Transaction Script + DAO
- Separação entre lógica de aplicação e acesso a dados
- Código de negócio em procedimentos
- DAO encapsula operações de banco
- Melhor testabilidade

### Versão 3: Domain Model + Repository
- Objetos de domínio com comportamento
- Preservação de invariâncias
- Repository abstrai persistência
- Testes de unidade viáveis

### Versão 4: Active Record
- Objeto responsável por si mesmo
- Combina dados e comportamento
- Simplifica operações básicas
- Pode quebrar Single Responsibility Principle

## 🎯 Quando Usar Cada Padrão

### Transaction Script
✅ **Use quando:**
- Lógica de negócio simples
- Poucas regras de negócio
- Aplicações pequenas ou médias
- Equipe pequena

❌ **Evite quando:**
- Regras de negócio complexas
- Múltiplas transições de estado
- Necessidade de preservar invariâncias

### Domain Model + Repository
✅ **Use quando:**
- Regras de negócio complexas
- Necessidade de preservar invariâncias
- Múltiplas transições de estado
- Aplicações de grande porte

❌ **Evite quando:**
- Lógica de negócio muito simples
- Aplicações pequenas
- Equipe sem experiência em DDD

### Active Record
✅ **Use quando:**
- Modelo de domínio simples
- Operações CRUD básicas
- Frameworks que suportam (Rails, Laravel)
- Prototipagem rápida

❌ **Evite quando:**
- Agregados complexos
- Múltiplas tabelas relacionadas
- Regras de negócio complexas
- Necessidade de testes de unidade isolados

## 🔗 Padrões Relacionados

### Unit of Work
Padrão que mantém uma lista de objetos afetados por uma transação e coordena a escrita, resolvendo problemas de concorrência.

- [Documentação](./unit-of-work.md)

### CQRS (Command Query Responsibility Segregation)
Separação entre modelos de escrita (comandos) e leitura (consultas), permitindo otimizações específicas para cada caso.

- [Documentação CQRS](../cqrs/README.md)

### DTO (Data Transfer Object)
Objetos simples usados para transferir dados entre camadas, especialmente nas fronteiras da aplicação.

- [Documentação](./dto-data-transfer-object.md)

## 📊 Comparação de Padrões

| Padrão | Complexidade | Testabilidade | Manutenibilidade | Performance |
|--------|--------------|---------------|------------------|-------------|
| Transaction Script | Baixa | Média | Baixa | Alta |
| DAO | Média | Média | Média | Alta |
| Domain Model + Repository | Alta | Alta | Alta | Média |
| Active Record | Média | Baixa | Média | Alta |

## 🧪 Testes e Padrões de Persistência

### Pirâmide de Testes

```
        ┌─────────────┐
        │   E2E Tests │  ← Testes End-to-End (menos)
        ├─────────────┤
        │ Integration │  ← Testes de Integração
        │    Tests    │
        ├─────────────┤
        │  Unit Tests │  ← Testes de Unidade (mais)
        └─────────────┘
```

### Testes de Integração
- Testam múltiplas camadas
- Podem acessar banco de dados
- Mais abrangentes (broad)
- Mais lentos

### Testes de Unidade
- Testam unidades isoladas
- Usam mocks/stubs/fakes
- Mais específicos (narrow)
- Mais rápidos

### Domain Model e Testabilidade
Com Domain Model, é possível criar testes de unidade que não dependem de banco de dados:

```typescript
// Teste de unidade - não precisa de banco
it('should assign ticket to agent', () => {
  const ticket = Ticket.create('content', 'requesterId');
  ticket.assign('agentId');
  expect(ticket.agentId).toBe('agentId');
  expect(ticket.status).toBe('ASSIGNED');
});
```

## ⚠️ Armadilhas Comuns

### 1. Misturar Responsabilidades
❌ **Evite:**
```typescript
// HTTP + SQL + Lógica de Negócio misturados
app.post('/tickets', async (req, res) => {
  const connection = await pool.connect();
  const result = await connection.query(
    'INSERT INTO tickets (content, status) VALUES ($1, $2)',
    [req.body.content, 'OPEN']
  );
  // Lógica de negócio aqui...
});
```

✅ **Prefira:**
```typescript
// Separação de responsabilidades
app.post('/tickets', async (req, res) => {
  const ticket = await ticketService.create(req.body);
  res.json(ticket);
});
```

### 2. Ignorar Invariâncias do Domínio
❌ **Evite:**
```typescript
// Permite estados inválidos
ticket.status = 'CLOSED';
ticket.agentId = null; // Inválido: ticket fechado sem agente
```

✅ **Prefira:**
```typescript
// Preserva invariâncias
ticket.close(); // Método que valida regras antes de fechar
```

### 3. Usar Repository para Consultas Complexas
❌ **Evite:**
```typescript
// Repository sobrecarregado com consultas de relatório
repository.findByStatusAndDateRangeAndAgent(status, start, end, agentId);
```

✅ **Prefira:**
```typescript
// Use DAO ou Query Objects para consultas
queryService.getTicketsReport(status, start, end, agentId);
```

## 📖 Referências

### Livros
- **Patterns of Enterprise Application Architecture** - Martin Fowler
- **Domain-Driven Design** - Eric Evans
- **Implementing Domain-Driven Design** - Vaughn Vernon

### Artigos e Recursos
- [Martin Fowler's Blog](https://martinfowler.com/)
- [Integration Test - Martin Fowler](https://martinfowler.com/bliki/IntegrationTest.html)
- [REST Thesis - Roy Fielding](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)

## 🎓 Aprendizados da Live

### Pontos-Chave
1. **Design é sobre responsabilidades**: Mudar design significa mudar atribuição de responsabilidades
2. **Testes guiam o design**: Testes ajudam a identificar problemas de design
3. **Performance não é o problema**: Abstrações não causam problemas de performance significativos
4. **Contexto importa**: Escolha o padrão baseado no contexto do projeto
5. **Evolução é natural**: Comece simples e evolua conforme necessário

### Lições sobre Performance
- Gargalos raramente estão nas abstrações
- Problemas reais: `SELECT *`, normalização ruim, falta de índices
- Medir antes de otimizar
- 99% dos sistemas não precisam se preocupar com performance de abstrações

## 📝 Checklist de Implementação

### Antes de Escolher um Padrão
- [ ] Analisar complexidade do domínio
- [ ] Avaliar tamanho da equipe
- [ ] Considerar experiência da equipe
- [ ] Verificar requisitos de performance
- [ ] Identificar necessidade de testes

### Durante a Implementação
- [ ] Separar responsabilidades claramente
- [ ] Escrever testes primeiro (TDD)
- [ ] Documentar decisões arquiteturais
- [ ] Revisar código regularmente
- [ ] Refatorar quando necessário

### Após a Implementação
- [ ] Validar com testes
- [ ] Medir performance
- [ ] Coletar feedback da equipe
- [ ] Documentar lições aprendidas
- [ ] Planejar evolução futura

---

**Última atualização**: 2025-11-16
**Mantenedor**: Equipe Skynet
**Versão**: 1.0
**Próxima revisão**: 2026-02-16

