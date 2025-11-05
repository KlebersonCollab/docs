# When to Use CQRS

## 📋 Overview

This guide helps you decide when CQRS is appropriate and when it's not. CQRS adds complexity, so use it only when benefits outweigh costs.

---

## ✅ Use CQRS When

### 1. High Read/Write Ratio

**Scenario**: Many more reads than writes (10:1 or higher).

**Example**:
- Product catalog: 1000 reads per write
- Order history: 100 reads per write
- Analytics dashboards: 10000 reads per write

**Benefit**: Optimize read model separately from write model.

### 2. Different Scaling Needs

**Scenario**: Reads and writes need to scale independently.

**Example**:
- Writes: Low volume, high consistency
- Reads: High volume, can be eventually consistent

**Benefit**: Scale read and write models independently.

### 3. Complex Domain Models

**Scenario**: Complex business logic in writes, simple queries in reads.

**Example**:
- Write: Complex order validation, business rules
- Read: Simple order summary, list views

**Benefit**: Simplify models by separating concerns.

### 4. Event Sourcing

**Scenario**: Using event sourcing.

**Example**:
- Events are source of truth
- Read models are projections
- Need to rebuild projections

**Benefit**: CQRS is natural fit for event sourcing.

### 5. Different Data Models

**Scenario**: Read and write need different data structures.

**Example**:
- Write: Normalized relational model
- Read: Denormalized document model

**Benefit**: Optimize each model for its purpose.

---

## ❌ Don't Use CQRS When

### 1. Simple CRUD

**Scenario**: Basic CRUD operations, no complexity.

**Problem**: CQRS adds unnecessary complexity.

**Solution**: Use simple CRUD pattern.

### 2. Small Applications

**Scenario**: Small team, simple domain, no scaling concerns.

**Problem**: Overhead not justified.

**Solution**: Start simple, add CQRS when needed.

### 3. Immediate Consistency Required

**Scenario**: Reads must see latest writes immediately.

**Problem**: CQRS uses eventual consistency.

**Solution**: Use traditional approach or synchronous projections.

### 4. Low Read/Write Ratio

**Scenario**: Similar number of reads and writes.

**Problem**: Benefits don't justify complexity.

**Solution**: Use traditional approach.

---

## 📊 Decision Matrix

| Criterion | Weight | Use CQRS | Don't Use CQRS |
|-----------|--------|----------|----------------|
| Read/Write Ratio | 30% | High (10:1+) | Low (1:1) |
| Scaling Needs | 25% | Different | Same |
| Complexity | 20% | High | Low |
| Consistency | 15% | Eventual OK | Immediate |
| Team Size | 10% | Medium-Large | Small |

**Scoring**: If 3+ criteria favor CQRS, consider using it.

---

## 💰 Cost/Benefit Analysis

### Benefits

**Performance**:
- Read optimization (denormalized projections)
- Write optimization (simplified domain model)
- Independent scaling

**Simplicity**:
- Simpler models (separate concerns)
- Easier to understand
- Better testability

**Flexibility**:
- Independent evolution
- Different technologies
- Easy to add new read models

### Costs

**Complexity**:
- Two models to maintain
- Event synchronization
- Projection logic

**Consistency**:
- Eventual consistency
- Stale reads possible
- Synchronization complexity

**Development**:
- More code to write
- More tests to write
- More to understand

---

## 🎯 Migration Strategy

### Start Simple

1. **Begin with Traditional Approach**
   - Single model for reads and writes
   - Monitor performance and complexity

2. **Identify Pain Points**
   - Read performance issues?
   - Write complexity issues?
   - Scaling issues?

3. **Introduce CQRS Gradually**
   - Start with one bounded context
   - Add read model projections
   - Monitor results

4. **Expand if Beneficial**
   - Add to other contexts if needed
   - Learn and iterate

---

## 🔗 Related Documentation

- [CQRS Guide](./README.md) - Overview
- [Command Model Design](./command-model-design.md) - Designing command models
- [Read Model Design](./read-model-design.md) - Designing read models

**Versão em Português**: [Quando Usar CQRS (PT-BR)](./pt-br/when-to-use.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

