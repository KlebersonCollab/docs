# Quando Usar CQRS

## 📋 Visão Geral

Este guia ajuda você a decidir quando CQRS é apropriado e quando não é. CQRS adiciona complexidade, então use apenas quando benefícios superam custos.

---

## ✅ Use CQRS Quando

### 1. Alta Razão Read/Write

**Cenário**: Muito mais reads do que writes (10:1 ou maior).

**Exemplo**:
- Catálogo de produtos: 1000 reads por write
- Histórico de pedidos: 100 reads por write
- Dashboards de analytics: 10000 reads por write

**Benefício**: Otimizar read model separadamente do write model.

### 2. Necessidades de Escala Diferentes

**Cenário**: Reads e writes precisam escalar independentemente.

**Exemplo**:
- Writes: Baixo volume, alta consistência
- Reads: Alto volume, podem ser eventualmente consistentes

**Benefício**: Escalar read e write models independentemente.

### 3. Modelos de Domínio Complexos

**Cenário**: Lógica de negócio complexa em writes, queries simples em reads.

**Exemplo**:
- Write: Validação complexa de pedido, regras de negócio
- Read: Resumo simples de pedido, visualizações de lista

**Benefício**: Simplificar modelos separando preocupações.

### 4. Event Sourcing

**Cenário**: Usando event sourcing.

**Exemplo**:
- Eventos são fonte da verdade
- Read models são projeções
- Necessidade de reconstruir projeções

**Benefício**: CQRS é ajuste natural para event sourcing.

### 5. Modelos de Dados Diferentes

**Cenário**: Read e write precisam de estruturas de dados diferentes.

**Exemplo**:
- Write: Modelo relacional normalizado
- Read: Modelo de documento desnormalizado

**Benefício**: Otimizar cada modelo para seu propósito.

---

## ❌ Não Use CQRS Quando

### 1. CRUD Simples

**Cenário**: Operações CRUD básicas, sem complexidade.

**Problema**: CQRS adiciona complexidade desnecessária.

**Solução**: Use padrão CRUD simples.

### 2. Aplicações Pequenas

**Cenário**: Equipe pequena, domínio simples, sem preocupações de escala.

**Problema**: Overhead não justificado.

**Solução**: Comece simples, adicione CQRS quando necessário.

### 3. Consistência Imediata Necessária

**Cenário**: Reads devem ver writes mais recentes imediatamente.

**Problema**: CQRS usa consistência eventual.

**Solução**: Use abordagem tradicional ou projeções síncronas.

### 4. Baixa Razão Read/Write

**Cenário**: Número similar de reads e writes.

**Problema**: Benefícios não justificam complexidade.

**Solução**: Use abordagem tradicional.

---

## 📊 Matriz de Decisão

| Critério | Peso | Usar CQRS | Não Usar CQRS |
|----------|------|-----------|---------------|
| Razão Read/Write | 30% | Alta (10:1+) | Baixa (1:1) |
| Necessidades de Escala | 25% | Diferentes | Mesmas |
| Complexidade | 20% | Alta | Baixa |
| Consistência | 15% | Eventual OK | Imediata |
| Tamanho da Equipe | 10% | Médio-Grande | Pequeno |

**Pontuação**: Se 3+ critérios favorecem CQRS, considere usar.

---

## 💰 Análise Custo/Benefício

### Benefícios

**Performance**:
- Otimização de leitura (projeções desnormalizadas)
- Otimização de escrita (modelo de domínio simplificado)
- Escala independente

**Simplicidade**:
- Modelos mais simples (separar preocupações)
- Mais fácil de entender
- Melhor testabilidade

**Flexibilidade**:
- Evolução independente
- Tecnologias diferentes
- Fácil adicionar novos read models

### Custos

**Complexidade**:
- Dois modelos para manter
- Sincronização de eventos
- Lógica de projeção

**Consistência**:
- Consistência eventual
- Reads obsoletos possíveis
- Complexidade de sincronização

**Desenvolvimento**:
- Mais código para escrever
- Mais testes para escrever
- Mais para entender

---

## 🎯 Estratégia de Migração

### Comece Simples

1. **Comece com Abordagem Tradicional**
   - Modelo único para reads e writes
   - Monitore performance e complexidade

2. **Identifique Pontos Problemáticos**
   - Problemas de performance de leitura?
   - Problemas de complexidade de escrita?
   - Problemas de escala?

3. **Introduza CQRS Gradualmente**
   - Comece com um bounded context
   - Adicione projeções de read model
   - Monitore resultados

4. **Expanda se Beneficial**
   - Adicione a outros contextos se necessário
   - Aprenda e itere

---

## 🔗 Documentação Relacionada

- [Guia de CQRS](./README.md) - Visão geral
- [Design do Command Model](./command-model-design.md) - Projetando command models
- [Design do Read Model](./read-model-design.md) - Projetando read models

**Versão em Inglês**: [When to Use CQRS (EN)](../when-to-use.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

