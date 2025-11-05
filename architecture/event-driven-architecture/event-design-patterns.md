# Event Design Patterns

## 📋 Overview

This guide covers event design patterns including envelope pattern, retry strategies, idempotency, and event versioning.

---

## 📦 Envelope Pattern

### Definition

**Envelope Pattern**: Wrap event data in envelope with metadata.

**Structure**:
```typescript
interface EventEnvelope {
  // Header
  id: string;              // Unique event ID
  type: string;            // Event type
  timestamp: Date;         // When event occurred
  source: string;          // Event source
  version: string;         // Event schema version
  
  // Trace
  traceId?: string;        // Distributed tracing
  correlationId?: string;  // Request correlation
  
  // Payload
  data: any;               // Event data
}
```

### Benefits

- **Metadata**: Trace, correlation, versioning
- **Standardization**: Consistent event structure
- **Evolution**: Version handling
- **Observability**: Tracing and monitoring

---

## 🔄 Retry Strategies

### Exponential Backoff

**Pattern**: Increase delay between retries exponentially.

```typescript
async function processEvent(event: Event, attempt = 1): Promise<void> {
  try {
    await handleEvent(event);
  } catch (error) {
    if (attempt < MAX_RETRIES) {
      const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s, ...
      await delay(delay);
      return processEvent(event, attempt + 1);
    }
    // Send to dead letter queue
    await sendToDLQ(event, error);
  }
}
```

### Fixed Delay

**Pattern**: Fixed delay between retries.

```typescript
async function processEvent(event: Event, attempt = 1): Promise<void> {
  try {
    await handleEvent(event);
  } catch (error) {
    if (attempt < MAX_RETRIES) {
      await delay(5000); // 5 seconds
      return processEvent(event, attempt + 1);
    }
    await sendToDLQ(event, error);
  }
}
```

---

## 🛡️ Idempotency

### Principle

**Idempotency**: Processing same event multiple times has same effect as processing once.

### Patterns

**Idempotency Key**:
```typescript
async function handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
  // Check if already processed
  const key = `order:${event.orderId}:${event.id}`;
  const processed = await idempotencyStore.get(key);
  if (processed) return; // Already processed
  
  // Process event
  await processOrder(event);
  
  // Mark as processed
  await idempotencyStore.set(key, true);
}
```

**Database Check**:
```typescript
async function handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
  // Check if order already exists
  const existing = await orderRepository.findById(event.orderId);
  if (existing) return; // Already processed
  
  // Process event
  await orderRepository.save(createOrder(event));
}
```

---

## 📊 Event Versioning

### Strategy

**Version in Envelope**: Include version in event envelope.

```typescript
interface EventEnvelope {
  version: string; // "1.0", "2.0"
  data: any;
}
```

**Version Handling**:
```typescript
async function handleEvent(event: EventEnvelope): Promise<void> {
  switch (event.version) {
    case '1.0':
      await handleV1(event.data);
      break;
    case '2.0':
      await handleV2(event.data);
      break;
    default:
      throw new Error(`Unsupported version: ${event.version}`);
  }
}
```

---

## 🔗 Related Documentation

- [Event-Driven Architecture Guide](./README.md) - Overview
- [When to Use Events](./when-to-use.md) - Decision guide

**Versão em Português**: [Padrões de Design de Eventos (PT-BR)](./pt-br/event-design-patterns.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

