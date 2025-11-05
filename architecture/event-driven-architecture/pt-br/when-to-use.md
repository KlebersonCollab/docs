# Quando Usar Arquitetura Orientada a Eventos

## 📋 Visão Geral

Este guia ajuda você a decidir quando Arquitetura Orientada a Eventos é apropriada. Eventos adicionam complexidade, então use apenas quando benefícios superam custos.

---

## ✅ Use Eventos Quando

### 1. Baixo Acoplamento Necessário

**Cenário**: Serviços precisam ser desacoplados, evolução independente.

**Exemplo**:
- Serviço de pedidos não precisa saber sobre serviço de inventário
- Serviços podem evoluir independentemente
- Cronogramas de deploy diferentes

**Benefício**: Evolução independente, acoplamento reduzido.

### 2. Processamento Assíncrono

**Cenário**: Operações não bloqueantes, processamento em background.

**Exemplo**:
- Enviar notificações por email
- Atualizar analytics
- Gerar relatórios

**Benefício**: Não bloqueante, melhor performance.

### 3. Alto Volume

**Cenário**: Alto volume de eventos, múltiplos consumidores.

**Exemplo**:
- Rastreamento de atividade do usuário
- Dados de sensores IoT
- Eventos de analytics

**Benefício**: Escalabilidade, distribuição de carga.

### 4. Múltiplos Subscribers

**Cenário**: Múltiplos serviços precisam dos mesmos eventos.

**Exemplo**:
- OrderCreated → Inventory, Analytics, Notifications
- PaymentProcessed → Order, Accounting, Notifications

**Benefício**: Um publisher, múltiplos subscribers.

### 5. Event Sourcing

**Cenário**: Padrão event sourcing, trilha de auditoria necessária.

**Exemplo**:
- Transações financeiras
- Requisitos de conformidade
- Debugging de viagem no tempo

**Benefício**: Trilha de auditoria completa, capacidade de replay.

---

## ❌ Não Use Eventos Quando

### 1. CRUD Simples

**Cenário**: Operações CRUD básicas, sem complexidade.

**Problema**: Eventos adicionam complexidade desnecessária.

**Solução**: Use operações síncronas simples.

### 2. Consistência Imediata

**Cenário**: Consistência imediata necessária.

**Problema**: Eventos são eventualmente consistentes.

**Solução**: Use operações síncronas ou transações.

### 3. Baixo Volume

**Cenário**: Baixo volume de eventos, integração simples.

**Problema**: Overhead não justificado.

**Solução**: Use chamadas de API simples.

### 4. Operações Síncronas

**Cenário**: Precisa de resposta imediata, fluxo síncrono.

**Problema**: Eventos são assíncronos.

**Solução**: Use chamadas de API síncronas.

---

## 📊 Matriz de Decisão

| Critério | Peso | Usar Eventos | Não Usar Eventos |
|----------|------|--------------|-------------------|
| Acoplamento | 30% | Baixo acoplamento necessário | Alto acoplamento OK |
| Consistência | 25% | Eventual OK | Imediata necessária |
| Volume | 20% | Alto volume | Baixo volume |
| Subscribers | 15% | Múltiplos | Único |
| Integração | 10% | Complexa | Simples |

**Pontuação**: Se 3+ critérios favorecem eventos, considere usar.

---

## 💰 Análise Custo/Benefício

### Benefícios

**Desacoplamento**:
- Serviços independentes
- Evolução independente
- Dependências reduzidas

**Escalabilidade**:
- Escala independente
- Distribuição de carga
- Alto throughput

**Flexibilidade**:
- Fácil adicionar subscribers
- Fácil adicionar publishers
- Replay de eventos

### Custos

**Complexidade**:
- Lógica de tratamento de eventos
- Estratégias de retry
- Idempotência

**Consistência**:
- Consistência eventual
- Dados obsoletos possíveis
- Complexidade de ordenação

**Operacional**:
- Gerenciamento de message broker
- Monitoramento
- Debugging

---

## 🎯 Estratégia de Migração

### Comece Simples

1. **Comece com Fila Simples**
   - Use SQS ou RabbitMQ
   - Processamento assíncrono simples
   - Aprenda padrões

2. **Identifique Pontos Problemáticos**
   - Problemas de acoplamento?
   - Problemas de escala?
   - Complexidade de integração?

3. **Introduza Eventos Gradualmente**
   - Comece com uma integração
   - Adicione padrões orientados a eventos
   - Monitore resultados

4. **Expanda se Beneficial**
   - Adicione a outras integrações
   - Considere event streaming se necessário
   - Aprenda e itere

---

## 🔗 Documentação Relacionada

- [Guia de Arquitetura Orientada a Eventos](./README.md) - Visão geral
- [Padrões de Design de Eventos](./event-design-patterns.md) - Padrões de eventos

**Versão em Inglês**: [When to Use Event-Driven Architecture (EN)](../when-to-use.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

