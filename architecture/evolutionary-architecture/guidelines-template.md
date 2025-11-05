# Architectural Guidelines Template

## 📋 Overview

This template helps you document architectural guidelines that support evolutionary architecture. Guidelines provide direction for how the architecture should evolve while maintaining architectural integrity.

**Usage**: Copy this template and fill in the sections for each architectural guideline you want to establish.

---

## Guideline: [Guideline Name]

### Description

[Brief description of what this guideline enforces and why it exists]

**Example**:
> This guideline ensures that the domain layer remains independent of infrastructure concerns, enabling easier testing and evolution of both layers independently.

### Rationale

[Explain why this guideline is important for evolutionary architecture]

**Key Points**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

### Rule

[Clear statement of the rule or constraint]

**Format**: 
- ✅ **DO**: [What should be done]
- ❌ **DON'T**: [What should be avoided]

**Example**:
- ✅ **DO**: Domain entities should contain only business logic
- ❌ **DON'T**: Domain entities should not depend on infrastructure (databases, HTTP clients, etc.)

### Validation

[How this guideline is validated - automated checks, reviews, etc.]

**Automated Checks**:
- [ ] [Check 1]: [Description]
- [ ] [Check 2]: [Description]

**Manual Reviews**:
- [ ] [Review 1]: [Description]
- [ ] [Review 2]: [Description]

**Tools Used**:
- [Tool 1]: [Purpose]
- [Tool 2]: [Purpose]

### Examples

#### ✅ Good Example

[Show a code example that follows the guideline]

```typescript
// ✅ Good: Domain entity without infrastructure dependencies
export class Order {
  constructor(
    private id: OrderId,
    private items: OrderItem[],
    private total: Money
  ) {}
  
  addItem(item: OrderItem): void {
    // Business logic only
    if (this.items.length >= 10) {
      throw new Error('Maximum 10 items per order');
    }
    this.items.push(item);
    this.total = this.recalculateTotal();
  }
  
  private recalculateTotal(): Money {
    // Business logic only
    return this.items.reduce(
      (sum, item) => sum.add(item.price),
      Money.zero()
    );
  }
}
```

#### ❌ Bad Example

[Show a code example that violates the guideline]

```typescript
// ❌ Bad: Domain entity with infrastructure dependency
import { Database } from '../infrastructure/database';
import { EmailService } from '../infrastructure/email';

export class Order {
  constructor(
    private id: OrderId,
    private items: OrderItem[],
    private total: Money,
    private db: Database,  // ❌ Infrastructure dependency
    private emailService: EmailService  // ❌ Infrastructure dependency
  ) {}
  
  async addItem(item: OrderItem): Promise<void> {
    // Business logic mixed with infrastructure
    await this.db.save(item);  // ❌ Direct database access
    await this.emailService.send(/* ... */);  // ❌ Direct email sending
  }
}
```

### Fitness Function

[Optional: Automated fitness function that validates this guideline]

```typescript
// Example fitness function
describe('Architectural Guideline: Domain Independence', () => {
  it('should not allow domain layer to import infrastructure', () => {
    const domainFiles = findFiles('src/domain/**/*.ts');
    const violations = domainFiles.filter(file => {
      const content = readFileSync(file, 'utf-8');
      return content.includes('from "../infrastructure"') ||
             content.includes('from "../application"');
    });
    
    expect(violations).toHaveLength(0);
  });
});
```

### Evolution Strategy

[How this guideline might evolve over time]

**Current State**: [Describe current enforcement]

**Future Evolution**:
- [ ] [Evolution step 1]
- [ ] [Evolution step 2]

**Conditions for Change**:
- [Condition 1]: [What would trigger a change to this guideline]
- [Condition 2]: [Another trigger condition]

### Related Guidelines

[Links to related guidelines]

- [Guideline Name](./guideline-name.md)
- [Guideline Name](./guideline-name.md)

### Exceptions

[Document any exceptions to this guideline and why they exist]

| Exception | Reason | Duration |
|-----------|--------|----------|
| [Exception 1] | [Why it exists] | [Temporary/Permanent] |
| [Exception 2] | [Why it exists] | [Temporary/Permanent] |

### Metrics

[How to measure compliance with this guideline]

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| [Metric 1] | [Target value] | [Current value] | ✅/❌ |
| [Metric 2] | [Target value] | [Current value] | ✅/❌ |

---

## Guidelines Catalog Template

Use this section to maintain a catalog of all guidelines:

### Guidelines by Category

#### Dependency Management
- [Guideline: Dependency Direction](./guidelines/dependency-direction.md)
- [Guideline: Circular Dependency Prevention](./guidelines/no-circular-deps.md)

#### Layer Architecture
- [Guideline: Layer Isolation](./guidelines/layer-isolation.md)
- [Guideline: Dependency Inversion](./guidelines/dependency-inversion.md)

#### Code Quality
- [Guideline: Code Complexity Limits](./guidelines/complexity-limits.md)
- [Guideline: Test Coverage Requirements](./guidelines/test-coverage.md)

#### Performance
- [Guideline: Response Time Targets](./guidelines/response-time.md)
- [Guideline: Resource Usage Limits](./guidelines/resource-limits.md)

### Guidelines Review Schedule

| Guideline | Last Reviewed | Next Review | Owner |
|-----------|---------------|-------------|-------|
| [Guideline 1] | [Date] | [Date] | [Name] |
| [Guideline 2] | [Date] | [Date] | [Name] |

---

## 📝 Using This Template

### Step 1: Identify Need

Before creating a guideline, ask:
- Is this a recurring architectural issue?
- Would automated validation help?
- Does this support evolutionary architecture goals?

### Step 2: Draft Guideline

1. Copy the guideline template section
2. Fill in all sections
3. Add examples (good and bad)
4. Define validation approach

### Step 3: Review and Approve

1. Review with architecture team
2. Get stakeholder approval
3. Document any exceptions

### Step 4: Implement Validation

1. Create fitness functions
2. Add to CI/CD pipeline
3. Set up monitoring

### Step 5: Monitor and Evolve

1. Review compliance metrics regularly
2. Update guidelines as architecture evolves
3. Remove guidelines that no longer serve a purpose

---

## 🎯 Best Practices

### Keep Guidelines Focused

✅ **DO**:
- Keep each guideline focused on one concern
- Make guidelines specific and actionable
- Update guidelines as architecture evolves

❌ **DON'T**:
- Create overly broad guidelines
- Set guidelines that are hard to validate
- Keep outdated guidelines

### Validate Automatically

Whenever possible, create automated fitness functions to validate guidelines. This ensures:
- Consistent enforcement
- Early detection of violations
- Faster feedback cycles

### Document Exceptions

When exceptions are needed, document them clearly with:
- Reason for exception
- Duration (temporary or permanent)
- Review date for temporary exceptions

### Review Regularly

Guidelines should be reviewed regularly to ensure they:
- Still serve their purpose
- Align with current architecture
- Support evolutionary goals

---

**Template Version**: 1.0  
**Last Updated**: 2025-01-20  
**Maintainer**: Skynet Documentation Team

---

**Related Documents**:
- [Evolutionary Architecture Guide](./README.md)
- [Metrics Definition](./metrics-definition.md)
- [Automation Strategies](./automation-strategies.md)

