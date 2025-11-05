# 🔍 Bounded Context Identification Guide

## 📋 Overview

Identifying bounded contexts is one of the most important activities in Strategic DDD. A bounded context defines the boundary within which a domain model is valid and where terminology has specific meanings.

**Key Principle**: Bounded contexts are discovered through domain exploration, not designed upfront.

---

## 🎯 What is a Bounded Context?

### Definition

A **Bounded Context** is:
- A boundary within which a domain model is valid
- A context where terms have specific, unambiguous meanings
- An area where the ubiquitous language is consistent
- A deployment unit (can be deployed independently)
- Owned by a team (or subset of a team)

### Characteristics

✅ **Has Clear Boundaries**:
- Clear scope of responsibility
- Defined interfaces with other contexts
- Independent deployment capability

✅ **Has Its Own Model**:
- Domain model specific to the context
- Entities, value objects, and services
- Business rules and invariants

✅ **Has Its Own Language**:
- Ubiquitous language within the context
- Terms have specific meanings
- Consistent terminology across the team

✅ **Can Be Implemented Independently**:
- Different technology stack if needed
- Different database if needed
- Different deployment schedule

---

## 🔍 Identification Techniques

### 1. Language Boundaries

**Principle**: Where terminology changes meaning, there's likely a boundary.

**Techniques**:
- **Terminology Mapping**: Map terms across the organization
- **Ambiguity Detection**: Identify where terms are ambiguous
- **Language Interviews**: Interview domain experts about terminology

**Example**:
```
In "Order Management" context:
- Order: A customer's purchase request
- Customer: Person placing the order
- Product: Item being ordered

In "Inventory Management" context:
- Order: A stock replenishment request
- Customer: Internal warehouse manager
- Product: SKU with stock levels

Same terms, different meanings → Different bounded contexts
```

### 2. Team Boundaries

**Principle**: Different teams often indicate different bounded contexts.

**Techniques**:
- **Team Structure Analysis**: Analyze team organization
- **Deployment Schedules**: Teams with different release cycles
- **Technology Choices**: Teams using different tech stacks

**Indicators**:
- Different teams own different parts
- Different deployment schedules
- Different technology stacks
- Different skill sets required

**Example**:
```
Team A: Payment Processing Team
- Uses Java, Spring Boot
- Deploys weekly
- Owns payment domain

Team B: Order Management Team
- Uses Node.js, Express
- Deploys daily
- Owns order domain

→ Two separate bounded contexts
```

### 3. Business Boundaries

**Principle**: Different business capabilities often indicate different contexts.

**Techniques**:
- **Capability Mapping**: Map business capabilities
- **Business Process Analysis**: Analyze business processes
- **Organizational Structure**: Analyze how business is organized

**Indicators**:
- Different business capabilities
- Different business rules
- Different business processes
- Different business metrics

**Example**:
```
Capability: Product Catalog
- Product information management
- Product search and discovery
- Product categorization

Capability: Order Fulfillment
- Order processing
- Inventory allocation
- Shipping coordination

→ Two separate bounded contexts
```

### 4. Data Boundaries

**Principle**: Different data ownership and consistency requirements indicate boundaries.

**Techniques**:
- **Data Ownership Analysis**: Who owns what data?
- **Consistency Requirements**: What are the consistency needs?
- **Data Access Patterns**: How is data accessed?

**Indicators**:
- Different data ownership
- Different consistency requirements
- Different data access patterns
- Different data models

**Example**:
```
Order Management:
- Owns: Order data, order history
- Consistency: Eventual consistency OK
- Access: Read-write, transactional

Product Catalog:
- Owns: Product data, product information
- Consistency: Strong consistency required
- Access: Read-heavy, cached

→ Different data models → Different contexts
```

---

## 🛠️ Practical Identification Process

### Step 1: Event Storming

**Purpose**: Discover domain events and identify boundaries.

**Process**:
1. Gather domain experts and developers
2. Identify domain events (orange sticky notes)
3. Group events by context
4. Identify boundaries between groups

**Output**: Initial bounded context candidates

### Step 2: Language Exploration

**Purpose**: Identify language boundaries and terminology differences.

**Process**:
1. Interview domain experts
2. Map terminology across the organization
3. Identify ambiguous terms
4. Document language differences

**Output**: Language boundary map

### Step 3: Team Analysis

**Purpose**: Understand team structure and identify team boundaries.

**Process**:
1. Map team organization
2. Identify team ownership
3. Analyze deployment schedules
4. Document team boundaries

**Output**: Team boundary map

### Step 4: Business Capability Mapping

**Purpose**: Map business capabilities and identify boundaries.

**Process**:
1. List business capabilities
2. Map capabilities to contexts
3. Identify capability boundaries
4. Document business boundaries

**Output**: Business capability map

### Step 5: Data Analysis

**Purpose**: Understand data ownership and identify data boundaries.

**Process**:
1. Map data ownership
2. Analyze consistency requirements
3. Identify data access patterns
4. Document data boundaries

**Output**: Data boundary map

### Step 6: Synthesis

**Purpose**: Combine all insights to identify final bounded contexts.

**Process**:
1. Combine all boundary maps
2. Identify overlapping boundaries
3. Refine context boundaries
4. Document final bounded contexts

**Output**: Final bounded context map

---

## 📊 Decision Framework

### Should These Be Separate Contexts?

| Criterion | Same Context | Separate Contexts |
|-----------|--------------|-------------------|
| Terminology | Same terms, same meanings | Different terms or meanings |
| Team | Same team | Different teams |
| Deployment | Same schedule | Different schedules |
| Technology | Same stack | Different stacks |
| Business Rules | Same rules | Different rules |
| Data Model | Same model | Different models |
| Consistency | Same requirements | Different requirements |

**Rule of Thumb**: If 3+ criteria indicate separation, consider separate contexts.

---

## 🚫 Anti-Patterns

### ❌ Too Many Small Contexts

**Problem**: Over-granular contexts lead to:
- Excessive integration complexity
- Communication overhead
- Deployment complexity

**Solution**: Merge related contexts or reconsider boundaries.

### ❌ Too Few Large Contexts

**Problem**: Under-granular contexts lead to:
- Unclear boundaries
- Team conflicts
- Deployment bottlenecks

**Solution**: Split contexts based on clear boundaries.

### ❌ Technical Boundaries Only

**Problem**: Bounding by technology alone misses domain boundaries.

**Example**: 
```
❌ Wrong: "Microservice A" and "Microservice B"
✅ Right: "Order Management" and "Payment Processing"
```

**Solution**: Start with domain boundaries, then consider technical boundaries.

### ❌ Copying Other Organizations

**Problem**: Copying contexts from other organizations without understanding your domain.

**Solution**: Identify contexts based on your specific domain and organization.

---

## ✅ Validation Checklist

Before finalizing a bounded context, verify:

- [ ] Has clear business purpose
- [ ] Has consistent ubiquitous language
- [ ] Has clear boundaries
- [ ] Can be deployed independently
- [ ] Has clear ownership (team or role)
- [ ] Has defined interfaces with other contexts
- [ ] Has appropriate granularity (not too small, not too large)
- [ ] Aligns with business capabilities
- [ ] Makes sense to domain experts
- [ ] Can evolve independently

---

## 📚 Examples

### Example 1: E-Commerce Platform

**Identified Contexts**:
1. **Product Catalog**
   - Terminology: Product, Category, Brand
   - Team: Product Management Team
   - Data: Product information, images, descriptions

2. **Order Management**
   - Terminology: Order, OrderItem, OrderStatus
   - Team: Order Processing Team
   - Data: Order data, order history

3. **Payment Processing**
   - Terminology: Payment, Transaction, Refund
   - Team: Payment Team
   - Data: Payment transactions, payment methods

### Example 2: SaaS Application

**Identified Contexts**:
1. **User Management**
   - Terminology: User, Account, Role
   - Team: Platform Team
   - Data: User accounts, authentication

2. **Feature Flags**
   - Terminology: Feature, Flag, Target
   - Team: Product Team
   - Data: Feature flag configurations

3. **Billing**
   - Terminology: Subscription, Invoice, Payment
   - Team: Finance Team
   - Data: Billing data, invoices

---

## 🔗 Related Documentation

- [Strategic DDD Guide](./README.md) - Overview of Strategic DDD
- [Context Mapping Patterns](./context-mapping-patterns.md) - How contexts relate
- [Subdomain Classification](./subdomain-classification.md) - Classifying subdomains
- [Event Storming Template](../../../templates/ddd/event-storming-template.md) - Template for event storming
- [Bounded Context Template](../../../templates/ddd/bounded-context-template.md) - Template for documenting contexts

**Versão em Português**: [Guia de Identificação de Bounded Context (PT-BR)](./pt-br/bounded-context-identification.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

