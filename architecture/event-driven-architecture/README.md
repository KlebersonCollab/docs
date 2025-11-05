# ⚡ Event-Driven Architecture Guide

## 📋 Overview

Event-Driven Architecture (EDA) uses events to integrate distributed systems. Events enable loose coupling, scalability, and asynchronous processing.

**Key Principle**: Start with simple message queues (SQS) before complex event streaming. Not everything should be event-driven.

> "Events are essential for integration in distributed systems, but not all use cases need them." - From architecture insights

---

## 🎯 What is Event-Driven Architecture?

### Definition

**Event-Driven Architecture** uses events to:
- Communicate between services
- Decouple components
- Enable asynchronous processing
- Support scalability

### Core Concepts

**Events**:
- Something that happened in the past
- Immutable facts
- Published to event bus/queue
- Consumed by subscribers

**Event Bus/Queue**:
- Message broker (RabbitMQ, Kafka, SQS)
- Routes events to subscribers
- Handles delivery guarantees
- Supports pub/sub patterns

**Subscribers**:
- Services that consume events
- React to events
- Update their state
- Publish new events

---

## 🎯 When to Use Events

### ✅ Good Use Cases

**Loose Coupling**:
- Services need to be decoupled
- Independent evolution required
- Different deployment schedules

**Asynchronous Processing**:
- Non-blocking operations
- Background processing
- Long-running tasks

**Scalability**:
- High volume processing
- Independent scaling
- Load distribution

**Event Sourcing**:
- Event sourcing pattern
- Audit trail needed
- Time-travel debugging

### ❌ When NOT to Use Events

**Simple CRUD**:
- Basic CRUD operations
- No integration complexity
- Synchronous operations sufficient

**Immediate Consistency**:
- Immediate consistency required
- Synchronous operations needed
- Real-time updates required

**Low Volume**:
- Low event volume
- Simple integration
- Overhead not justified

---

## 🏗️ Architecture Patterns

### Basic Event-Driven

```
Service A → Event Bus → Service B
           ↓
        Service C
```

### Event Sourcing

```
Commands → Domain Model → Events → Event Store
                                    ↓
                              Read Models (Projections)
```

### CQRS with Events

```
Commands → Command Model → Events → Read Model Projections
```

---

## 📦 Event Design

### Event Structure

**Envelope Pattern**:
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

### Event Naming

**Convention**: Past tense, domain language.

**Examples**:
- `OrderCreated`
- `PaymentProcessed`
- `ShipmentSent`
- `OrderCancelled`

---

## 🔄 Event Patterns

### 1. Simple Message Queue

**Use When**: Simple async processing, basic integration.

**Technology**: SQS, RabbitMQ

**Example**:
```
Order Service → SQS → Inventory Service
```

### 2. Event Streaming

**Use When**: High volume, multiple consumers, replay needed.

**Technology**: Kafka, Kinesis

**Example**:
```
Order Service → Kafka → Multiple Consumers
```

### 3. Pub/Sub

**Use When**: Multiple subscribers, topic-based routing.

**Technology**: Pub/Sub, SNS, RabbitMQ

**Example**:
```
Order Service → Topic → Subscribers
```

---

## 🛡️ Reliability Patterns

### Retry Strategies

**Exponential Backoff**:
```typescript
async function processEvent(event: Event, retries = 3): Promise<void> {
  try {
    await handleEvent(event);
  } catch (error) {
    if (retries > 0) {
      await delay(Math.pow(2, 3 - retries) * 1000);
      return processEvent(event, retries - 1);
    }
    throw error;
  }
}
```

### Idempotency

**Principle**: Event handlers must be idempotent.

**Pattern**:
```typescript
async function handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
  // Check if already processed
  const existing = await repository.findById(event.orderId);
  if (existing) return; // Already processed
  
  // Process event
  await repository.save(createOrder(event));
}
```

### Dead Letter Queue

**Purpose**: Handle failed events.

**Pattern**:
```
Event → Handler (fails) → Retry → Still fails → Dead Letter Queue
```

---

## 📊 Decision Framework

### Should We Use Events?

| Criterion | Use Events | Don't Use Events |
|-----------|------------|------------------|
| Coupling | Loose coupling needed | Tight coupling OK |
| Consistency | Eventual OK | Immediate required |
| Volume | High volume | Low volume |
| Integration | Multiple services | Simple integration |
| Scalability | Independent scaling | Same scaling |

---

## 🚫 Anti-Patterns

### ❌ Events Everywhere

**Problem**: Using events for everything, even simple operations.

**Solution**: Use events only where they add value.

### ❌ Synchronous Events

**Problem**: Waiting for event processing, losing async benefits.

**Solution**: Truly async, fire-and-forget when possible.

### ❌ No Idempotency

**Problem**: Processing same event multiple times causes issues.

**Solution**: Make handlers idempotent.

---

## 🔗 Related Documentation

- [When to Use Events](./when-to-use.md) - Decision guide
- [Event Design Patterns](./event-design-patterns.md) - Event patterns
- [CQRS Guide](../cqrs/README.md) - CQRS with events
- [Strategic DDD Guide](../ddd/strategic-ddd/README.md) - Bounded context integration

**Versão em Português**: [Guia de Arquitetura Orientada a Eventos (PT-BR)](./pt-br/README.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

