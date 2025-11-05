# 🎯 Guia de DDD Estratégico

## 📋 Visão Geral

O DDD Estratégico é a base do Domain-Driven Design. Foca no entendimento e modelagem do domínio de negócio em nível estratégico, identificando bounded contexts, mapeando relacionamentos entre contextos e classificando subdomínios.

**Princípio Fundamental**: DDD Estratégico deve vir primeiro, antes dos padrões táticos. Entender os limites e relacionamentos do domínio é mais importante que implementar padrões táticos complexos.

> "DDD Estratégico é quase sempre aplicável. É óbvio hoje, mas não era quando foi criado." - Dos insights de arquitetura

---

## 🎯 Por que DDD Estratégico Primeiro?

### A Base Estratégica

O DDD Estratégico fornece:

1. **Entendimento do Domínio**: Entendimento profundo do domínio de negócio e seus limites
2. **Limites de Contexto**: Limites claros entre diferentes partes do sistema
3. **Mapeamento de Relacionamentos**: Entendimento de como diferentes contextos se relacionam e interagem
4. **Classificação de Subdomínios**: Identificação do que é core, supporting ou generic
5. **Decisões Estratégicas**: Tomar decisões informadas sobre onde investir esforço

### Estratégico vs Tático

**DDD Estratégico** (Fazer Primeiro):
- Identificação de Bounded Context
- Context Mapping
- Classificação de subdomínios
- Modelagem de domínio em nível estratégico

**DDD Tático** (Aplicar Quando Necessário):
- Aggregates, Entities, Value Objects
- Domain Services
- Padrões Repository
- Modelagem de lógica de negócio complexa

**Insight Principal**: Um bounded context pode usar Transaction Script, enquanto outro usa Domain Model. A escolha depende da complexidade, não de dogmas.

---

## 🏛️ Conceitos Fundamentais

### 1. Bounded Context

Um **Bounded Context** é um limite dentro do qual um modelo de domínio particular é válido. Define o contexto em que termos têm significados específicos.

**Características**:
- Tem seu próprio modelo de domínio
- Tem sua própria linguagem ubíqua
- Tem limites claros
- Pode ser implementado independentemente

**Exemplo**:
```
Contexto de Gerenciamento de Pedidos
- Pedido: Um pedido feito por um cliente
- Cliente: A pessoa que faz o pedido
- Pagamento: Processamento de pagamento para o pedido

Contexto de Gerenciamento de Inventário
- Produto: Um item físico em estoque
- Estoque: Quantidade disponível
- Armazém: Localização de armazenamento

Nota: "Pedido" significa coisas diferentes em cada contexto!
```

### 2. Context Mapping

**Context Mapping** é o processo de identificar e documentar relacionamentos entre bounded contexts.

**Padrões Comuns**:
- **Shared Kernel**: Código compartilhado entre contextos
- **Customer-Supplier**: Um contexto depende de outro
- **Conformist**: Um contexto se conforma ao modelo de outro
- **Anti-Corruption Layer**: Camada de tradução entre contextos
- **Separate Ways**: Contextos independentes sem dependências
- **Partnership**: Relacionamento colaborativo entre contextos

Veja [Padrões de Context Mapping](../context-mapping-patterns.md) para padrões detalhados.

### 3. Classificação de Subdomínios

**Subdomínios** são partes do domínio de negócio. São classificados como:

1. **Core Domain**: A proposta de valor única do negócio
   - Maior prioridade de investimento
   - Construído internamente
   - Requer expertise profunda do domínio

2. **Supporting Subdomain**: Importante mas não diferenciador
   - Construído internamente ou terceirizado
   - Suporta core domain
   - Prioridade de investimento média

3. **Generic Subdomain**: Funcionalidade comum, não única
   - Deve ser terceirizado/integrado
   - Baixa prioridade de investimento
   - Use soluções existentes quando possível

Veja [Classificação de Subdomínios](../subdomain-classification.md) para orientação detalhada.

---

## 🔍 Identificação de Bounded Context

### Técnicas para Identificar Bounded Contexts

1. **Limites de Linguagem**
   - Onde a terminologia muda de significado
   - Onde diferentes equipes usam termos diferentes
   - Onde conceitos são ambíguos

2. **Limites de Equipe**
   - Equipes diferentes trabalhando em partes diferentes
   - Cronogramas de deploy diferentes
   - Tecnologias diferentes

3. **Limites de Negócio**
   - Diferentes capacidades de negócio
   - Diferentes regras de negócio
   - Diferentes processos de negócio

4. **Limites de Dados**
   - Propriedade de dados diferente
   - Requisitos de consistência diferentes
   - Padrões de acesso a dados diferentes

Veja [Identificação de Bounded Context](../bounded-context-identification.md) para técnicas detalhadas.

---

## 🗺️ Context Mapping

O Context Mapping ajuda a visualizar e entender relacionamentos entre bounded contexts.

### Processo de Mapeamento

1. **Identificar Contextos**: Listar todos os bounded contexts
2. **Identificar Relacionamentos**: Determinar como contextos se relacionam
3. **Documentar Padrões**: Documentar o padrão de relacionamento
4. **Planejar Integração**: Planejar como contextos se integrarão
5. **Monitorar Evolução**: Atualizar mapa conforme contextos evoluem

Veja [Padrões de Context Mapping](../context-mapping-patterns.md) para padrões detalhados e estratégias de integração.

---

## 🎯 Classificação de Subdomínios

### Framework de Classificação

**Core Domain**:
- ✅ Único para seu negócio
- ✅ Vantagem competitiva
- ✅ Alta complexidade
- ✅ Requer expertise profunda

**Supporting Subdomain**:
- ⚠️ Importante mas não único
- ⚠️ Suporta core domain
- ⚠️ Complexidade média
- ⚠️ Pode ser construído ou terceirizado

**Generic Subdomain**:
- ❌ Comum em vários setores
- ❌ Sem vantagem competitiva
- ❌ Baixa complexidade
- ❌ Deve ser terceirizado

Veja [Classificação de Subdomínios](../subdomain-classification.md) para framework de decisão detalhado e exemplos.

---

## 📚 Exemplos Práticos

### Exemplo 1: Plataforma E-Commerce

**Bounded Contexts**:
- Catálogo de Produtos
- Gerenciamento de Pedidos
- Processamento de Pagamento
- Envio e Logística
- Gerenciamento de Clientes

**Classificação de Subdomínios**:
- **Core**: Catálogo de Produtos (descoberta única de produtos)
- **Supporting**: Gerenciamento de Pedidos, Gerenciamento de Clientes
- **Generic**: Processamento de Pagamento (Stripe), Envio (API FedEx)

---

## 🔗 Documentação Relacionada

- [Identificação de Bounded Context](../bounded-context-identification.md) - Técnicas para identificar contextos
- [Padrões de Context Mapping](../context-mapping-patterns.md) - Padrões detalhados de context mapping
- [Classificação de Subdomínios](../subdomain-classification.md) - Framework de classificação e exemplos
- [Template de Event Storming](../../../../templates/ddd/event-storming-template.md) - Template para workshops de event storming
- [Template de Bounded Context](../../../../templates/ddd/bounded-context-template.md) - Template para documentar bounded contexts
- [Guia de Arquitetura Evolutiva](../../evolutionary-architecture/README.md) - Como DDD estratégico suporta evolução
- [Guia de CQRS](../../cqrs/README.md) - Como CQRS emerge do DDD

**Versão em Inglês**: [Strategic DDD Guide (EN)](../README.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

