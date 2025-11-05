# 🎯 CQRS Guide

## 📋 Overview

Command Query Responsibility Segregation (CQRS) is a pattern that separates the command model (used for writes) from the read model (used for reads). This pattern naturally emerges from Domain-Driven Design.

**Key Principle**: CQRS naturally emerges from DDD. Command Model (Domain Model) for mutations, Read Model (projections) for queries.

> "CQRS naturally emerges from DDD. Command Model (Domain Model) for mutations, Read Model (projections) for queries." - From architecture insights

---

## 🎯 What is CQRS?

### Definition

**CQRS** separates:
- **Command Model**: Optimized for writes (mutations)
- **Read Model**: Optimized for reads (queries)

**Key Insight**: Different models for different purposes lead to better performance and simpler code.

### Command Model vs Read Model

**Command Model**:
- Domain model for business logic
- Handles commands (mutations)
- Enforces business rules
- Maintains consistency
- Uses transactional database

**Read Model**:
- Optimized projections for queries
- Handles queries (reads)
- Denormalized for performance
- Eventually consistent
- Uses read-optimized database

### CQRS and DDD Relationship

**Natural Emergence**:
- DDD identifies bounded contexts
- Bounded contexts have different read/write needs
- CQRS emerges naturally from these needs
- Command Model = Domain Model
- Read Model = Projections

---

## 🎯 When to Use CQRS

### ✅ Good Use Cases

**High Read/Write Ratio**:
- Many more reads than writes
- Read optimization needed
- Different read patterns

**Different Scaling Needs**:
- Reads need to scale differently
- Writes need different optimization
- Independent scaling requirements

**Complex Domain Models**:
- Complex business logic in writes
- Simple queries in reads
- Different models simplify code

**Event Sourcing**:
- Event sourcing naturally leads to CQRS
- Events are commands
- Projections are read models

### ❌ When NOT to Use CQRS

**Simple CRUD**:
- Basic CRUD operations
- Simple read/write patterns
- No performance issues

**Small Applications**:
- Small team
- Simple domain
- No scaling concerns

**High Consistency Required**:
- Immediate consistency needed
- Eventual consistency not acceptable
- Synchronous operations required

---

## 🏗️ Architecture Patterns

### Basic CQRS

```
┌─────────────┐     Commands     ┌──────────────┐
│   Client    │ ────────────────>│  Command     │
│             │                  │  Handler     │
│             │                  └──────────────┘
│             │                         │
│             │                         │ Write
│             │                         ▼
│             │                  ┌──────────────┐
│             │                  │  Write Model │
│             │                  │  (Domain)    │
│             │                  └──────────────┘
│             │                         │
│             │                         │ Events
│             │                         ▼
│             │                  ┌──────────────┐
│             │                  │   Read Model │
│             │<─────────────────│ (Projection) │
│             │     Queries      └──────────────┘
└─────────────┘
```

### CQRS with Event Sourcing

```
Commands → Command Handler → Domain Model → Events → Event Store
                                                         │
                                                         ▼
                                              Read Model (Projections)
```

---

## 📚 Code Examples

### TypeScript Example: Command Model

```typescript
// Command Model (Domain Model)
class Order {
  private items: OrderItem[] = [];
  private status: OrderStatus = OrderStatus.Pending;

  createOrder(customerId: string, items: OrderItem[]): void {
    if (items.length === 0) {
      throw new Error('Order must have at least one item');
    }
    this.items = items;
    this.status = OrderStatus.Pending;
    DomainEventPublisher.publish(new OrderCreatedEvent(this.id, customerId));
  }

  cancelOrder(): void {
    if (this.status === OrderStatus.Shipped) {
      throw new Error('Cannot cancel shipped order');
    }
    this.status = OrderStatus.Cancelled;
    DomainEventPublisher.publish(new OrderCancelledEvent(this.id));
  }
}

// Command Handler
class CreateOrderCommandHandler {
  async handle(command: CreateOrderCommand): Promise<void> {
    const order = new Order();
    order.createOrder(command.customerId, command.items);
    await this.orderRepository.save(order);
  }
}
```

### TypeScript Example: Read Model

```typescript
// Read Model (Projection)
interface OrderSummary {
  id: string;
  customerId: string;
  total: number;
  itemCount: number;
  status: string;
  createdAt: Date;
}

// Query Handler
class GetOrderSummaryQueryHandler {
  async handle(query: GetOrderSummaryQuery): Promise<OrderSummary> {
    return await this.readRepository.findById(query.orderId);
  }
}

// Projection (Event Handler)
class OrderProjection {
  async onOrderCreated(event: OrderCreatedEvent): Promise<void> {
    const summary: OrderSummary = {
      id: event.orderId,
      customerId: event.customerId,
      total: 0, // Calculated from items
      itemCount: event.items.length,
      status: 'Pending',
      createdAt: event.timestamp
    };
    await this.readRepository.save(summary);
  }
}
```

---

## 🔄 Event-Driven CQRS

### Event Flow

```
1. Command received
2. Command Handler processes command
3. Domain Model updates (write model)
4. Domain Events published
5. Event Handlers update read models (projections)
6. Read models available for queries
```

### Event Sourcing Integration

**Event Sourcing + CQRS**:
- Events are the source of truth
- Read models are projections from events
- Commands produce events
- Queries read from projections

---

## 📊 Decision Framework

### Should We Use CQRS?

| Criterion | Use CQRS | Don't Use CQRS |
|-----------|----------|----------------|
| Read/Write Ratio | High (10:1+) | Low (1:1) |
| Scaling Needs | Different | Same |
| Complexity | High domain complexity | Simple CRUD |
| Consistency | Eventual OK | Immediate required |
| Team Size | Medium-Large | Small |
| Performance | Read optimization needed | Not needed |

---

## 🚫 Anti-Patterns

### ❌ CQRS Everywhere

**Problem**: Applying CQRS to everything, even simple CRUD.

**Solution**: Use CQRS only where it adds value.

### ❌ Synchronous Projections

**Problem**: Synchronously updating read models, losing CQRS benefits.

**Solution**: Use async event-driven projections.

### ❌ Shared Database

**Problem**: Using same database for read and write models.

**Solution**: Separate databases or at least separate schemas.

---

## 🔗 Related Documentation

- [When to Use CQRS](./when-to-use.md) - Detailed decision guide
- [Command Model Design](./command-model-design.md) - Designing command models
- [Read Model Design](./read-model-design.md) - Designing read models
- [Strategic DDD Guide](../ddd/strategic-ddd/README.md) - CQRS emerges from DDD
- [Event-Driven Architecture Guide](../event-driven-architecture/README.md) - Event-driven integration

**Versão em Português**: [Guia de CQRS (PT-BR)](./pt-br/README.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

