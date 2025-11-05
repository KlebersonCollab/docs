# 🎯 Subdomain Classification Guide

## 📋 Overview

Subdomain classification is a critical strategic decision in DDD. It helps determine where to invest effort, what to build in-house, and what to outsource or integrate.

**Key Principle**: Not all subdomains are equal. Classify them to focus investment on what matters most.

---

## 🎯 Subdomain Types

### 1. Core Domain

**Definition**: The unique value proposition of your business. What makes you different from competitors.

**Characteristics**:
- ✅ **Unique**: Unique to your business
- ✅ **Competitive Advantage**: Differentiates you from competitors
- ✅ **High Complexity**: Complex business logic
- ✅ **Deep Expertise**: Requires deep domain expertise
- ✅ **High Value**: High business value

**Investment Priority**: **HIGHEST** - This is where you invest most effort.

**Build Strategy**: **Build In-House** - Requires custom development.

**Example**:
```
E-Commerce Platform:
- Core Domain: Product Recommendation Engine
  - Unique algorithm
  - Competitive advantage
  - Complex ML models
  - Build in-house

SaaS Application:
- Core Domain: Feature Flag Logic
  - Unique business rules
  - Competitive advantage
  - Complex targeting rules
  - Build in-house
```

---

### 2. Supporting Subdomain

**Definition**: Important but not differentiating. Supports the core domain but doesn't provide competitive advantage.

**Characteristics**:
- ⚠️ **Important**: Important for business operations
- ⚠️ **Not Unique**: Common across similar businesses
- ⚠️ **Medium Complexity**: Moderate complexity
- ⚠️ **Supporting Role**: Supports core domain

**Investment Priority**: **MEDIUM** - Important but not the focus.

**Build Strategy**: **Build or Outsource** - Can be built or outsourced depending on resources.

**Example**:
```
E-Commerce Platform:
- Supporting Subdomain: Order Management
  - Important for operations
  - Common across e-commerce
  - Medium complexity
  - Can be built or outsourced

SaaS Application:
- Supporting Subdomain: User Management
  - Important for operations
  - Common across SaaS
  - Medium complexity
  - Can be built or outsourced
```

---

### 3. Generic Subdomain

**Definition**: Common functionality found across industries. No competitive advantage.

**Characteristics**:
- ❌ **Common**: Common across industries
- ❌ **No Advantage**: No competitive advantage
- ❌ **Low Complexity**: Relatively simple
- ❌ **Commodity**: Available as commodity solutions

**Investment Priority**: **LOWEST** - Minimize investment.

**Build Strategy**: **Outsource or Integrate** - Use existing solutions.

**Example**:
```
E-Commerce Platform:
- Generic Subdomain: Payment Processing
  - Common across e-commerce
  - No competitive advantage
  - Use Stripe, PayPal, etc.
  - Outsource/integrate

SaaS Application:
- Generic Subdomain: Email Sending
  - Common across SaaS
  - No competitive advantage
  - Use SendGrid, Mailgun, etc.
  - Outsource/integrate
```

---

## 🔍 Classification Framework

### Decision Tree

```
Question 1: Is this unique to our business?
├─ No → Generic Subdomain (Outsource)
└─ Yes → Question 2: Is this our competitive advantage?
    ├─ No → Supporting Subdomain (Build or Outsource)
    └─ Yes → Core Domain (Build In-House)
```

### Classification Questions

**Question 1: Uniqueness**
- Is this functionality unique to our business?
- Do competitors have similar functionality?
- Is this a standard industry feature?

**Question 2: Competitive Advantage**
- Does this differentiate us from competitors?
- Is this a key differentiator?
- Would losing this hurt our competitive position?

**Question 3: Complexity**
- How complex is this functionality?
- Does it require deep domain expertise?
- Is it a commodity or custom solution?

**Question 4: Investment**
- How much should we invest here?
- What's the ROI?
- Where should we focus resources?

---

## 📊 Classification Matrix

| Criterion | Core Domain | Supporting Subdomain | Generic Subdomain |
|-----------|-------------|---------------------|-------------------|
| **Uniqueness** | Unique | Common | Very Common |
| **Competitive Advantage** | High | Low | None |
| **Complexity** | High | Medium | Low |
| **Expertise Required** | Deep | Moderate | Standard |
| **Investment Priority** | Highest | Medium | Lowest |
| **Build Strategy** | Build In-House | Build or Outsource | Outsource/Integrate |
| **Examples** | Recommendation engine, Feature flags | Order management, User management | Payment, Email, Logging |

---

## 🛠️ Classification Process

### Step 1: List All Subdomains

Identify all subdomains in your system:

```
E-Commerce Platform Subdomains:
- Product Catalog
- Product Recommendation
- Order Management
- Payment Processing
- Shipping & Logistics
- Customer Management
- Inventory Management
- Analytics
- Search
```

### Step 2: Classify Each Subdomain

Apply the decision framework to each subdomain:

```
Product Recommendation:
- Unique? Yes (unique algorithm)
- Competitive Advantage? Yes (key differentiator)
- → Core Domain

Order Management:
- Unique? No (common across e-commerce)
- Competitive Advantage? No
- → Supporting Subdomain

Payment Processing:
- Unique? No (very common)
- Competitive Advantage? No
- → Generic Subdomain
```

### Step 3: Validate Classification

Review with domain experts and stakeholders:

- [ ] Does classification make sense?
- [ ] Are investment priorities correct?
- [ ] Are build strategies appropriate?
- [ ] Do stakeholders agree?

### Step 4: Document Decisions

Document classification with rationale:

```
Subdomain: Product Recommendation
Classification: Core Domain
Rationale:
- Unique ML algorithm provides competitive advantage
- High complexity requires deep expertise
- High investment priority
Build Strategy: Build in-house with ML team
```

---

## 💡 Outsourcing Strategies for Generic Subdomains

### Strategy 1: Third-Party Integration

**Use When**: Standard functionality available as service.

**Examples**:
- Payment: Stripe, PayPal
- Email: SendGrid, Mailgun
- SMS: Twilio
- Authentication: Auth0, Firebase Auth

**Benefits**:
- Fast implementation
- No maintenance
- Proven reliability
- Cost-effective

### Strategy 2: Open Source Solutions

**Use When**: Open source solution exists and fits needs.

**Examples**:
- Logging: ELK Stack
- Monitoring: Prometheus
- Message Queue: RabbitMQ, Kafka

**Benefits**:
- Free (or low cost)
- Customizable
- Community support
- Full control

**Considerations**:
- Maintenance required
- Expertise needed
- May need customization

### Strategy 3: SaaS Integration

**Use When**: SaaS solution provides needed functionality.

**Examples**:
- Analytics: Google Analytics, Mixpanel
- Error Tracking: Sentry
- Feature Flags: LaunchDarkly

**Benefits**:
- Managed service
- No infrastructure
- Regular updates
- Support included

---

## 🎯 Investment Strategy

### Core Domain Investment

**Allocation**: 60-80% of development effort

**Focus Areas**:
- Deep domain expertise
- Complex business logic
- Innovation and improvement
- Competitive advantage

**Teams**:
- Best developers
- Domain experts
- Innovation focus

### Supporting Subdomain Investment

**Allocation**: 15-30% of development effort

**Focus Areas**:
- Functional completeness
- Operational efficiency
- Integration with core domain

**Teams**:
- Standard development teams
- Good practices
- Efficiency focus

### Generic Subdomain Investment

**Allocation**: 5-10% of development effort

**Focus Areas**:
- Integration
- Configuration
- Minimal customization

**Teams**:
- Integration teams
- DevOps support
- Maintenance focus

---

## 📚 Examples

### Example 1: E-Commerce Platform

**Subdomain Classification**:

```
Core Domain (60% effort):
- Product Recommendation Engine
  - Unique ML algorithms
  - Competitive advantage
  - Build in-house

Supporting Subdomain (30% effort):
- Order Management
  - Important for operations
  - Build in-house (medium complexity)

Generic Subdomain (10% effort):
- Payment Processing
  - Integrate Stripe
  - Outsource

- Shipping & Logistics
  - Integrate FedEx API
  - Outsource
```

### Example 2: SaaS Application

**Subdomain Classification**:

```
Core Domain (70% effort):
- Feature Flag Logic
  - Unique targeting rules
  - Competitive advantage
  - Build in-house

Supporting Subdomain (20% effort):
- User Management
  - Important for operations
  - Build in-house (standard features)

Generic Subdomain (10% effort):
- Email Sending
  - Integrate SendGrid
  - Outsource

- Analytics
  - Integrate Mixpanel
  - Outsource
```

---

## 🚫 Anti-Patterns

### ❌ Building Generic Subdomains

**Problem**: Building payment processing, email sending, etc. in-house.

**Why It's Wrong**:
- No competitive advantage
- Wastes resources
- Better solutions exist
- Maintenance burden

**Solution**: Use existing solutions (Stripe, SendGrid, etc.).

### ❌ Outsourcing Core Domain

**Problem**: Outsourcing the unique value proposition.

**Why It's Wrong**:
- Loses competitive advantage
- Can't differentiate
- Dependent on vendors
- No control

**Solution**: Build core domain in-house.

### ❌ Equal Investment

**Problem**: Investing equally in all subdomains.

**Why It's Wrong**:
- Wastes resources on generic
- Under-invests in core
- No focus

**Solution**: Prioritize core domain, minimize generic.

---

## ✅ Validation Checklist

Before finalizing classification:

- [ ] All subdomains classified
- [ ] Classification rationale documented
- [ ] Investment priorities set
- [ ] Build strategies defined
- [ ] Outsourcing decisions made
- [ ] Stakeholders agree
- [ ] Investment allocation appropriate
- [ ] Resources allocated correctly

---

## 🔗 Related Documentation

- [Strategic DDD Guide](./README.md) - Overview of Strategic DDD
- [Bounded Context Identification](./bounded-context-identification.md) - Identifying contexts
- [Context Mapping Patterns](./context-mapping-patterns.md) - Context relationships
- [Evolutionary Architecture Guide](../evolutionary-architecture/README.md) - Evolution strategies

**Versão em Português**: [Guia de Classificação de Subdomínios (PT-BR)](./pt-br/subdomain-classification.md)

---

**Version**: 1.0  
**Last Updated**: 2025  
**Maintainer**: Skynet Documentation Team

