# 🎯 Guia de CQRS

## 📋 Visão Geral

Command Query Responsibility Segregation (CQRS) é um padrão que separa o modelo de comando (usado para writes) do modelo de leitura (usado para reads). Este padrão emerge naturalmente do Domain-Driven Design.

**Princípio Fundamental**: CQRS emerge naturalmente do DDD. Command Model (Domain Model) para mutações, Read Model (projections) para queries.

> "CQRS emerge naturalmente do DDD. Command Model (Domain Model) para mutações, Read Model (projections) para queries." - Dos insights de arquitetura

---

## 🎯 O que é CQRS?

### Definição

**CQRS** separa:
- **Command Model**: Otimizado para writes (mutações)
- **Read Model**: Otimizado para reads (queries)

**Insight Principal**: Modelos diferentes para propósitos diferentes levam a melhor performance e código mais simples.

### Command Model vs Read Model

**Command Model**:
- Modelo de domínio para lógica de negócio
- Processa comandos (mutações)
- Aplica regras de negócio
- Mantém consistência
- Usa banco de dados transacional

**Read Model**:
- Projeções otimizadas para queries
- Processa queries (reads)
- Desnormalizado para performance
- Eventualmente consistente
- Usa banco de dados otimizado para leitura

### Relacionamento CQRS e DDD

**Emergência Natural**:
- DDD identifica bounded contexts
- Bounded contexts têm necessidades diferentes de read/write
- CQRS emerge naturalmente dessas necessidades
- Command Model = Domain Model
- Read Model = Projections

---

## 🎯 Quando Usar CQRS

### ✅ Boas Casos de Uso

**Alta Razão Read/Write**:
- Muito mais reads do que writes
- Otimização de leitura necessária
- Padrões de leitura diferentes

**Necessidades de Escala Diferentes**:
- Reads precisam escalar diferentemente
- Writes precisam de otimização diferente
- Requisitos de escala independentes

**Modelos de Domínio Complexos**:
- Lógica de negócio complexa em writes
- Queries simples em reads
- Modelos diferentes simplificam código

### ❌ Quando NÃO Usar CQRS

**CRUD Simples**:
- Operações CRUD básicas
- Padrões simples de read/write
- Sem problemas de performance

**Aplicações Pequenas**:
- Equipe pequena
- Domínio simples
- Sem preocupações de escala

**Alta Consistência Necessária**:
- Consistência imediata necessária
- Consistência eventual não aceitável
- Operações síncronas necessárias

---

## 🏗️ Padrões Arquiteturais

### CQRS Básico

```
Cliente → Command Handler → Command Model (Write)
                              ↓
                           Events
                              ↓
                         Read Model (Projections) → Queries
```

### CQRS com Event Sourcing

```
Commands → Command Handler → Domain Model → Events → Event Store
                                                         ↓
                                              Read Model (Projections)
```

---

## 📊 Framework de Decisão

### Devemos Usar CQRS?

| Critério | Usar CQRS | Não Usar CQRS |
|----------|-----------|---------------|
| Razão Read/Write | Alta (10:1+) | Baixa (1:1) |
| Necessidades de Escala | Diferentes | Mesmas |
| Complexidade | Alta complexidade de domínio | CRUD simples |
| Consistência | Eventual OK | Imediata necessária |
| Tamanho da Equipe | Médio-Grande | Pequeno |
| Performance | Otimização de leitura necessária | Não necessária |

---

## 🚫 Anti-Padrões

### ❌ CQRS em Tudo

**Problema**: Aplicar CQRS a tudo, mesmo CRUD simples.

**Solução**: Use CQRS apenas onde adiciona valor.

### ❌ Projeções Síncronas

**Problema**: Atualizando read models sincronamente, perdendo benefícios do CQRS.

**Solução**: Use projeções assíncronas orientadas a eventos.

---

## 🔗 Documentação Relacionada

- [Quando Usar CQRS](../when-to-use.md) - Guia de decisão detalhado
- [Design do Command Model](../command-model-design.md) - Projetando command models
- [Design do Read Model](../read-model-design.md) - Projetando read models e projeções
- [Guia de DDD Estratégico](../../ddd/strategic-ddd/README.md) - CQRS emerge do DDD
- [Guia de Event-Driven Architecture](../../event-driven-architecture/README.md) - Integração orientada a eventos

**Versão em Inglês**: [CQRS Guide (EN)](../README.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

