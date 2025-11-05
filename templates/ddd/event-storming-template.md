# Event Storming Workshop Template

## 📋 Overview

Event Storming is a workshop technique for discovering domain events, identifying bounded contexts, and understanding the domain model through collaborative exploration.

**Duration**: 2-4 hours  
**Participants**: Domain experts, developers, product owners

---

## 🎯 Workshop Objectives

- [ ] Discover domain events
- [ ] Identify bounded contexts
- [ ] Understand business processes
- [ ] Map context relationships
- [ ] Identify aggregate boundaries

---

## 📦 Materials Needed

- Orange sticky notes (domain events)
- Blue sticky notes (commands)
- Yellow sticky notes (aggregates)
- Pink sticky notes (read models)
- Green sticky notes (policies/rules)
- Red sticky notes (hot spots/problems)
- Large whiteboard or wall space
- Markers

---

## 🗓️ Workshop Structure

### Phase 1: Domain Event Discovery (30-60 min)

**Process**:
1. Start with a business process or user journey
2. Identify events that happen in the domain
3. Write events on orange sticky notes
4. Place events in chronological order
5. Use past tense: "OrderCreated", "PaymentProcessed", "ShipmentSent"

**Questions to Ask**:
- What happens in this domain?
- What events occur?
- What are the business outcomes?
- What triggers these events?

**Output**: Timeline of domain events

---

### Phase 2: Command Discovery (30-60 min)

**Process**:
1. For each event, identify what causes it
2. Write commands on blue sticky notes
3. Place commands before their corresponding events
4. Use imperative form: "CreateOrder", "ProcessPayment", "SendShipment"

**Questions to Ask**:
- What causes this event?
- Who triggers this event?
- What action leads to this outcome?

**Output**: Commands mapped to events

---

### Phase 3: Aggregate Identification (30-60 min)

**Process**:
1. Group related events and commands
2. Identify aggregates (entities that handle commands and produce events)
3. Write aggregates on yellow sticky notes
4. Place aggregates above their events/commands

**Questions to Ask**:
- What entities handle these commands?
- What entities produce these events?
- What are the transaction boundaries?

**Output**: Aggregates identified

---

### Phase 4: Bounded Context Identification (30-60 min)

**Process**:
1. Look for boundaries in the event timeline
2. Identify where terminology changes
3. Identify where processes diverge
4. Draw boundaries around related events/commands/aggregates
5. Name each bounded context

**Questions to Ask**:
- Where does terminology change?
- Where do processes diverge?
- Where are there different teams?
- Where are there different data models?

**Output**: Bounded contexts identified

---

### Phase 5: Context Mapping (30-60 min)

**Process**:
1. Identify relationships between bounded contexts
2. Document integration patterns
3. Map dependencies
4. Identify integration points

**Questions to Ask**:
- How do contexts relate?
- What are the dependencies?
- How do contexts integrate?
- What integration patterns apply?

**Output**: Context map

---

### Phase 6: Hot Spots and Problems (30 min)

**Process**:
1. Identify areas of confusion
2. Mark unclear events or processes
3. Mark potential problems
4. Document questions and assumptions

**Questions to Ask**:
- What's unclear?
- What are the assumptions?
- What are the risks?
- What needs clarification?

**Output**: List of hot spots and questions

---

## 📝 Template: Domain Event

```
Event: [Event Name in Past Tense]
Description: [What happened]
Actor: [Who/what triggered it]
Context: [Bounded context]
Related Commands: [Commands that cause this event]
Related Events: [Events that follow this event]
```

**Example**:
```
Event: OrderCreated
Description: A customer placed an order
Actor: Customer
Context: Order Management
Related Commands: CreateOrder
Related Events: OrderValidated, PaymentInitiated
```

---

## 📝 Template: Command

```
Command: [Command Name in Imperative]
Description: [What action is requested]
Actor: [Who/what triggers it]
Context: [Bounded context]
Produces Events: [Events this command produces]
Aggregate: [Aggregate that handles this command]
```

**Example**:
```
Command: CreateOrder
Description: Customer requests to create an order
Actor: Customer
Context: Order Management
Produces Events: OrderCreated
Aggregate: Order
```

---

## 📝 Template: Aggregate

```
Aggregate: [Aggregate Name]
Description: [What this aggregate represents]
Context: [Bounded context]
Handles Commands: [Commands this aggregate handles]
Produces Events: [Events this aggregate produces]
Invariants: [Business rules/invariants]
```

**Example**:
```
Aggregate: Order
Description: Represents a customer order
Context: Order Management
Handles Commands: CreateOrder, CancelOrder, UpdateOrder
Produces Events: OrderCreated, OrderCancelled, OrderUpdated
Invariants: Order must have at least one item, Total must be positive
```

---

## 📝 Template: Bounded Context

```
Bounded Context: [Context Name]
Description: [What this context represents]
Domain Events: [List of events in this context]
Aggregates: [List of aggregates in this context]
Ubiquitous Language: [Key terms in this context]
Related Contexts: [Other contexts this relates to]
```

**Example**:
```
Bounded Context: Order Management
Description: Manages customer orders
Domain Events: OrderCreated, OrderValidated, OrderCancelled
Aggregates: Order, OrderItem
Ubiquitous Language: Order, OrderItem, Customer, Total
Related Contexts: Payment Processing, Inventory Management
```

---

## 🎯 Workshop Output

After the workshop, document:

1. **Event Timeline**: Chronological list of events
2. **Commands**: List of commands and their events
3. **Aggregates**: List of aggregates and their responsibilities
4. **Bounded Contexts**: List of bounded contexts and their boundaries
5. **Context Map**: Map of relationships between contexts
6. **Hot Spots**: List of unclear areas and questions
7. **Next Steps**: Action items and follow-up

---

## 📊 Example: E-Commerce Order Process

### Event Timeline

```
1. OrderCreated
2. OrderValidated
3. PaymentInitiated
4. PaymentProcessed
5. InventoryReserved
6. ShipmentCreated
7. ShipmentSent
8. OrderFulfilled
```

### Commands

```
CreateOrder → OrderCreated
ValidateOrder → OrderValidated
InitiatePayment → PaymentInitiated
ProcessPayment → PaymentProcessed
ReserveInventory → InventoryReserved
CreateShipment → ShipmentCreated
SendShipment → ShipmentSent
FulfillOrder → OrderFulfilled
```

### Aggregates

```
Order (handles: CreateOrder, ValidateOrder, CancelOrder)
Payment (handles: InitiatePayment, ProcessPayment)
Inventory (handles: ReserveInventory, ReleaseInventory)
Shipment (handles: CreateShipment, SendShipment)
```

### Bounded Contexts

```
Order Management:
- Events: OrderCreated, OrderValidated, OrderCancelled
- Aggregates: Order

Payment Processing:
- Events: PaymentInitiated, PaymentProcessed, PaymentFailed
- Aggregates: Payment

Inventory Management:
- Events: InventoryReserved, InventoryReleased
- Aggregates: Inventory

Shipping:
- Events: ShipmentCreated, ShipmentSent
- Aggregates: Shipment
```

---

## ✅ Workshop Checklist

Before the workshop:
- [ ] Schedule workshop (2-4 hours)
- [ ] Invite participants (domain experts, developers)
- [ ] Prepare materials (sticky notes, markers, whiteboard)
- [ ] Define scope (which process/journey to explore)

During the workshop:
- [ ] Facilitate domain event discovery
- [ ] Identify commands and aggregates
- [ ] Map bounded contexts
- [ ] Document relationships
- [ ] Identify hot spots

After the workshop:
- [ ] Document findings
- [ ] Create bounded context map
- [ ] Create event timeline
- [ ] List action items
- [ ] Schedule follow-up if needed

---

## 🔗 Related Documentation

- [Strategic DDD Guide](../../architecture/ddd/strategic-ddd/README.md)
- [Bounded Context Identification](../../architecture/ddd/strategic-ddd/bounded-context-identification.md)
- [Context Mapping Patterns](../../architecture/ddd/strategic-ddd/context-mapping-patterns.md)

**Versão em Português**: [Template de Workshop Event Storming (PT-BR)](./pt-br/event-storming-template.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

