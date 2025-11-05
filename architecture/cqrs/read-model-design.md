# Read Model Design

## 📋 Overview

The Read Model is optimized for queries. It's typically denormalized and eventually consistent.

**Key Principle**: Read Model = Projections. Optimize for read performance, not write consistency.

---

## 🎯 Design Principles

### 1. Query Optimization

**Principle**: Optimize for read performance.

**Techniques**:
- Denormalization
- Pre-computed aggregations
- Indexed queries
- Caching

### 2. Eventual Consistency

**Principle**: Read models are eventually consistent.

**Characteristics**:
- Updated asynchronously
- May be slightly stale
- Acceptable for most queries

### 3. Projections

**Principle**: Read models are projections from events.

**Process**:
- Events published from command model
- Event handlers update read models
- Read models optimized for queries

---

## 🏗️ Structure

### Projection Pattern

```
Domain Event → Event Handler → Read Model Update
```

### Example Projection

```typescript
class OrderSummaryProjection {
  async onOrderCreated(event: OrderCreatedEvent): Promise<void> {
    const summary: OrderSummary = {
      id: event.orderId,
      customerId: event.customerId,
      total: this.calculateTotal(event.items),
      itemCount: event.items.length,
      status: 'Pending',
      createdAt: event.timestamp
    };
    await this.readRepository.save(summary);
  }
  
  async onOrderCancelled(event: OrderCancelledEvent): Promise<void> {
    await this.readRepository.update(event.orderId, {
      status: 'Cancelled'
    });
  }
}
```

### Query Handlers

```typescript
class GetOrderSummaryQueryHandler {
  async handle(query: GetOrderSummaryQuery): Promise<OrderSummary> {
    return await this.readRepository.findById(query.orderId);
  }
}
```

---

## 📊 Optimization Strategies

### 1. Denormalization

**Principle**: Store data in query-ready format.

**Example**:
```typescript
// Denormalized Read Model
interface OrderSummary {
  id: string;
  customerId: string;
  customerName: string;  // Denormalized from Customer
  total: number;          // Pre-computed
  itemCount: number;      // Pre-computed
  status: string;
}
```

### 2. Pre-computed Aggregations

**Principle**: Compute aggregations during projection.

**Example**:
```typescript
// Compute total during projection
async onOrderCreated(event: OrderCreatedEvent): Promise<void> {
  const total = event.items.reduce((sum, item) => 
    sum + (item.price * item.quantity), 0
  );
  // Store pre-computed total
}
```

### 3. Caching

**Principle**: Cache frequently accessed read models.

**Example**:
```typescript
class CachedOrderSummaryRepository {
  async findById(id: string): Promise<OrderSummary> {
    // Check cache first
    const cached = await this.cache.get(id);
    if (cached) return cached;
    // Fallback to database
    const summary = await this.db.findById(id);
    await this.cache.set(id, summary);
    return summary;
  }
}
```

---

## 🔄 Event Handling

### Event Handler Pattern

```typescript
class OrderReadModelProjection {
  async handle(event: DomainEvent): Promise<void> {
    switch (event.type) {
      case 'OrderCreated':
        await this.onOrderCreated(event);
        break;
      case 'OrderCancelled':
        await this.onOrderCancelled(event);
        break;
      // ... other events
    }
  }
}
```

### Idempotency

**Principle**: Event handlers must be idempotent.

**Example**:
```typescript
async onOrderCreated(event: OrderCreatedEvent): Promise<void> {
  // Check if already processed
  const existing = await this.readRepository.findById(event.orderId);
  if (existing) return; // Already processed
  
  // Process event
  const summary = this.createSummary(event);
  await this.readRepository.save(summary);
}
```

---

## 🔗 Related Documentation

- [CQRS Guide](./README.md) - Overview
- [Command Model Design](./command-model-design.md) - Command model design
- [Event-Driven Architecture Guide](../event-driven-architecture/README.md) - Event handling

**Versão em Português**: [Design do Read Model (PT-BR)](./pt-br/read-model-design.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

