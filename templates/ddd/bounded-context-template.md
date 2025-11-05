# Bounded Context Documentation Template

## 📋 Overview

This template helps document a bounded context in Strategic DDD. Use this template to document each bounded context identified in your system.

---

## Bounded Context: [Context Name]

### Basic Information

**Name**: [Context Name]  
**Version**: [Version Number]  
**Last Updated**: [Date]  
**Owner**: [Team/Role]  
**Status**: [Active | In Development | Deprecated]

---

### Description

[Brief description of what this bounded context represents and its purpose]

**Example**:
> The Order Management bounded context is responsible for managing customer orders throughout their lifecycle, from creation to fulfillment. It handles order creation, validation, cancellation, and status tracking.

---

### Ubiquitous Language

**Key Terms**:

| Term | Definition | Example |
|------|------------|---------|
| [Term 1] | [Definition] | [Example usage] |
| [Term 2] | [Definition] | [Example usage] |
| [Term 3] | [Definition] | [Example usage] |

**Example**:
| Term | Definition | Example |
|------|------------|---------|
| Order | A customer's purchase request | "Order #12345 contains 3 items" |
| OrderItem | A single item in an order | "OrderItem: 2x Product A" |
| OrderStatus | Current state of the order | "OrderStatus: PENDING" |

---

### Domain Model

**Aggregates**:

- **[Aggregate Name]**
  - Description: [What this aggregate represents]
  - Commands: [List of commands this aggregate handles]
  - Events: [List of events this aggregate produces]
  - Invariants: [Business rules that must be maintained]

**Example**:
- **Order**
  - Description: Represents a customer order
  - Commands: CreateOrder, CancelOrder, UpdateOrder
  - Events: OrderCreated, OrderCancelled, OrderUpdated
  - Invariants: Order must have at least one item, Total must be positive

---

### Domain Events

**Events Produced**:

| Event | Description | Triggered By |
|-------|-------------|--------------|
| [Event 1] | [Description] | [Command/Aggregate] |
| [Event 2] | [Description] | [Command/Aggregate] |

**Example**:
| Event | Description | Triggered By |
|-------|-------------|--------------|
| OrderCreated | Order was created by customer | CreateOrder command |
| OrderCancelled | Order was cancelled | CancelOrder command |
| OrderValidated | Order passed validation | ValidateOrder command |

---

### Commands

**Commands Handled**:

| Command | Description | Handler | Produces Events |
|---------|-------------|---------|----------------|
| [Command 1] | [Description] | [Aggregate] | [Event 1, Event 2] |
| [Command 2] | [Description] | [Aggregate] | [Event 3] |

**Example**:
| Command | Description | Handler | Produces Events |
|---------|-------------|---------|----------------|
| CreateOrder | Create a new order | Order aggregate | OrderCreated |
| CancelOrder | Cancel an existing order | Order aggregate | OrderCancelled |
| ValidateOrder | Validate order business rules | Order aggregate | OrderValidated |

---

### Context Boundaries

**What's Inside**:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

**What's Outside**:
- [Not responsible for 1]
- [Not responsible for 2]
- [Not responsible for 3]

**Example**:
**What's Inside**:
- Order creation and management
- Order validation
- Order status tracking

**What's Outside**:
- Payment processing (Payment Processing context)
- Inventory management (Inventory Management context)
- Shipping coordination (Shipping context)

---

### Context Relationships

**Upstream Contexts** (dependencies):
- **[Context Name]**: [Relationship type and description]
  - Integration Pattern: [Pattern used]
  - Integration Technology: [Technology used]

**Downstream Contexts** (depend on this):
- **[Context Name]**: [Relationship type and description]
  - Integration Pattern: [Pattern used]
  - Integration Technology: [Technology used]

**Example**:
**Upstream Contexts**:
- **Product Catalog**: Customer-Supplier relationship
  - Integration Pattern: REST API
  - Integration Technology: HTTP/REST

**Downstream Contexts**:
- **Payment Processing**: Customer-Supplier relationship (we are upstream)
  - Integration Pattern: REST API
  - Integration Technology: HTTP/REST

---

### Subdomain Classification

**Classification**: [Core Domain | Supporting Subdomain | Generic Subdomain]

**Rationale**: [Why this classification]

**Investment Priority**: [High | Medium | Low]

**Build Strategy**: [Build In-House | Build or Outsource | Outsource/Integrate]

**Example**:
**Classification**: Supporting Subdomain

**Rationale**: Order management is important for operations but not a competitive differentiator. Common across e-commerce platforms.

**Investment Priority**: Medium

**Build Strategy**: Build In-House (medium complexity, supports core domain)

---

### Implementation Details

**Technology Stack**:
- Language: [Programming language]
- Framework: [Framework]
- Database: [Database]
- Other: [Other technologies]

**Deployment**:
- Deployment Unit: [Monolith | Microservice | Module]
- Deployment Frequency: [Frequency]
- Deployment Team: [Team]

**Example**:
**Technology Stack**:
- Language: TypeScript
- Framework: Express.js
- Database: PostgreSQL
- Other: Redis for caching

**Deployment**:
- Deployment Unit: Microservice
- Deployment Frequency: Daily
- Deployment Team: Order Management Team

---

### Integration Points

**APIs Exposed**:
- [API Endpoint 1]: [Description]
- [API Endpoint 2]: [Description]

**Events Published**:
- [Event 1]: [Description, subscribers]
- [Event 2]: [Description, subscribers]

**Events Subscribed**:
- [Event 1]: [Source context, handler]
- [Event 2]: [Source context, handler]

**Example**:
**APIs Exposed**:
- `POST /orders`: Create a new order
- `GET /orders/{id}`: Get order details
- `PATCH /orders/{id}/cancel`: Cancel an order

**Events Published**:
- `OrderCreated`: Published when order is created (subscribers: Payment Processing, Inventory Management)
- `OrderCancelled`: Published when order is cancelled (subscribers: Payment Processing, Inventory Management)

**Events Subscribed**:
- `PaymentProcessed`: From Payment Processing context (handler: UpdateOrderStatus)
- `InventoryReserved`: From Inventory Management context (handler: ConfirmOrder)

---

### Business Rules

**Key Business Rules**:
1. [Business rule 1]
2. [Business rule 2]
3. [Business rule 3]

**Example**:
1. Order must have at least one item
2. Order total must be positive
3. Order cannot be cancelled after shipping
4. Order must be validated before payment

---

### Evolution Strategy

**Current State**: [Current state description]

**Planned Evolution**:
- [Evolution 1]: [Description, timeline]
- [Evolution 2]: [Description, timeline]

**Migration Strategy**: [How to evolve without breaking changes]

**Example**:
**Current State**: Monolithic module, shared database

**Planned Evolution**:
- Extract to microservice: Q2 2025
- Separate database: Q2 2025
- Event-driven integration: Q3 2025

**Migration Strategy**: Gradual extraction using strangler fig pattern

---

### Metrics and Monitoring

**Key Metrics**:
- [Metric 1]: [Description, target]
- [Metric 2]: [Description, target]

**Monitoring**:
- [What to monitor]
- [Alerts configured]

**Example**:
**Key Metrics**:
- Order creation rate: Target: < 100ms p95
- Order validation success rate: Target: > 99%
- Order cancellation rate: Target: < 5%

**Monitoring**:
- API response times
- Event processing latency
- Error rates

---

### Team and Ownership

**Team**: [Team name]

**Roles**:
- [Role 1]: [Responsibility]
- [Role 2]: [Responsibility]

**On-Call**: [On-call rotation or contact]

**Example**:
**Team**: Order Management Team

**Roles**:
- Backend Developers: Order management logic
- Product Owner: Order feature requirements
- QA: Order testing

**On-Call**: Rotation with Payment Processing team

---

### Documentation

**Related Documentation**:
- [Link to related docs]
- [Link to API documentation]
- [Link to architecture diagrams]

**Examples**:
- [Order Management Architecture Diagram](./diagrams/order-management-architecture.md)
- [Order API Documentation](./api/order-api.md)
- [Order Domain Model](./domain/order-domain-model.md)

---

### Notes and Decisions

**Key Decisions**:
- [Decision 1]: [Rationale, date]
- [Decision 2]: [Rationale, date]

**Trade-offs**:
- [Trade-off 1]: [What was chosen, what was given up]

**Example**:
**Key Decisions**:
- Chose microservice over monolith: Better scalability, team autonomy (2024-01-15)
- Chose event-driven over synchronous: Better decoupling, scalability (2024-02-01)

**Trade-offs**:
- Microservice: Better scalability but increased operational complexity
- Event-driven: Better decoupling but eventual consistency

---

## 🔗 Related Documentation

- [Strategic DDD Guide](../../architecture/ddd/strategic-ddd/README.md)
- [Bounded Context Identification](../../architecture/ddd/strategic-ddd/bounded-context-identification.md)
- [Context Mapping Patterns](../../architecture/ddd/strategic-ddd/context-mapping-patterns.md)
- [Event Storming Template](./event-storming-template.md)

**Versão em Português**: [Template de Documentação de Bounded Context (PT-BR)](./pt-br/bounded-context-template.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

