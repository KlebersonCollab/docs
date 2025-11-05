# ⚡ Guia de Arquitetura Orientada a Eventos

## 📋 Visão Geral

Arquitetura Orientada a Eventos (Event-Driven Architecture) usa eventos para integrar sistemas distribuídos. Eventos permitem baixo acoplamento, escalabilidade e processamento assíncrono.

**Princípio Fundamental**: Comece com filas de mensagens simples (SQS) antes de event streaming complexo. Nem tudo deve ser orientado a eventos.

> "Eventos são essenciais para integração em sistemas distribuídos, mas nem todos os casos de uso precisam deles." - Dos insights de arquitetura

---

## 🎯 O que é Arquitetura Orientada a Eventos?

### Definição

**Arquitetura Orientada a Eventos** usa eventos para:
- Comunicar entre serviços
- Desacoplar componentes
- Permitir processamento assíncrono
- Suportar escalabilidade

### Conceitos Fundamentais

**Eventos**:
- Algo que aconteceu no passado
- Fatos imutáveis
- Publicados no event bus/fila
- Consumidos por subscribers

**Event Bus/Fila**:
- Message broker (RabbitMQ, Kafka, SQS)
- Roteia eventos para subscribers
- Lida com garantias de entrega
- Suporta padrões pub/sub

**Subscribers**:
- Serviços que consomem eventos
- Reagem a eventos
- Atualizam seu estado
- Publicam novos eventos

---

## 🎯 Quando Usar Eventos

### ✅ Boas Casos de Uso

**Baixo Acoplamento**:
- Serviços precisam ser desacoplados
- Evolução independente necessária
- Cronogramas de deploy diferentes

**Processamento Assíncrono**:
- Operações não bloqueantes
- Processamento em background
- Tarefas de longa duração

**Escalabilidade**:
- Processamento de alto volume
- Escala independente
- Distribuição de carga

**Event Sourcing**:
- Padrão event sourcing
- Trilha de auditoria necessária
- Debugging de viagem no tempo

### ❌ Quando NÃO Usar Eventos

**CRUD Simples**:
- Operações CRUD básicas
- Sem complexidade de integração
- Operações síncronas suficientes

**Consistência Imediata**:
- Consistência imediata necessária
- Operações síncronas necessárias
- Atualizações em tempo real necessárias

**Baixo Volume**:
- Baixo volume de eventos
- Integração simples
- Overhead não justificado

---

## 🏗️ Padrões Arquiteturais

### Básico Orientado a Eventos

```
Serviço A → Event Bus → Serviço B
           ↓
        Serviço C
```

### Event Sourcing

```
Commands → Domain Model → Events → Event Store
                                    ↓
                              Read Models (Projections)
```

---

## 📦 Design de Eventos

### Estrutura de Evento

**Padrão Envelope**:
```typescript
interface EventEnvelope {
  // Header
  id: string;
  type: string;
  timestamp: Date;
  source: string;
  version: string;
  
  // Trace
  traceId?: string;
  correlationId?: string;
  
  // Payload
  data: any;
}
```

### Nomenclatura de Eventos

**Convenção**: Passado, linguagem de domínio.

**Exemplos**:
- `OrderCreated`
- `PaymentProcessed`
- `ShipmentSent`
- `OrderCancelled`

---

## 🔄 Padrões de Eventos

### 1. Fila de Mensagens Simples

**Use Quando**: Processamento assíncrono simples, integração básica.

**Tecnologia**: SQS, RabbitMQ

### 2. Event Streaming

**Use Quando**: Alto volume, múltiplos consumidores, replay necessário.

**Tecnologia**: Kafka, Kinesis

### 3. Pub/Sub

**Use Quando**: Múltiplos subscribers, roteamento baseado em tópicos.

**Tecnologia**: Pub/Sub, SNS, RabbitMQ

---

## 🛡️ Padrões de Confiabilidade

### Estratégias de Retry

**Exponential Backoff**: Aumentar delay entre retries exponencialmente.

### Idempotência

**Princípio**: Handlers de eventos devem ser idempotentes.

**Padrão**: Verificar se já foi processado antes de processar.

### Dead Letter Queue

**Propósito**: Lidar com eventos que falharam.

---

## 📊 Framework de Decisão

### Devemos Usar Eventos?

| Critério | Usar Eventos | Não Usar Eventos |
|----------|--------------|------------------|
| Acoplamento | Baixo acoplamento necessário | Alto acoplamento OK |
| Consistência | Eventual OK | Imediata necessária |
| Volume | Alto volume | Baixo volume |
| Integração | Múltiplos serviços | Integração simples |
| Escalabilidade | Escala independente | Mesma escala |

---

## 🚫 Anti-Padrões

### ❌ Eventos em Tudo

**Problema**: Usar eventos para tudo, mesmo operações simples.

**Solução**: Use eventos apenas onde adicionam valor.

### ❌ Eventos Síncronos

**Problema**: Esperando processamento de eventos, perdendo benefícios assíncronos.

**Solução**: Verdadeiramente assíncrono, fire-and-forget quando possível.

---

## 🔗 Documentação Relacionada

- [Quando Usar Eventos](../when-to-use.md) - Guia de decisão
- [Padrões de Design de Eventos](../event-design-patterns.md) - Padrões de eventos
- [Guia de CQRS](../../cqrs/README.md) - CQRS com eventos
- [Guia de DDD Estratégico](../../ddd/strategic-ddd/README.md) - Integração de bounded context

**Versão em Inglês**: [Event-Driven Architecture Guide (EN)](../README.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

