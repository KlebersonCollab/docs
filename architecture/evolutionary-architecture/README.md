# 🧬 Evolutionary Architecture Guide

## 📋 Overview

Evolutionary Architecture represents a fundamental shift in how we approach software design. Instead of upfront, comprehensive architectural planning, we build architectures that evolve based on real data, context, and actual needs.

**Key Principle**: Architecture decisions should be guided by data and context, not assumptions or upfront design.

> "The current trend is towards evolutionary architecture - making architectural decisions guided by data and context, rather than upfront design."

---

## 🎯 Core Concepts

### What is Evolutionary Architecture?

Evolutionary Architecture is an approach that recognizes that:

1. **Architectures Must Evolve**: Software systems are not static; they change over time based on new requirements, user needs, and business constraints.

2. **Data-Driven Decisions**: Architectural decisions should be based on actual metrics and data, not speculation about future needs.

3. **Guided Change**: Use guidelines, metrics, and fitness functions to guide architectural evolution while maintaining architectural integrity.

4. **Automation**: Automate architectural decisions and validations whenever possible to reduce human error and ensure consistency.

5. **Minimize Required System**: Focus on what's truly required now, not what might be needed in the future (YAGNI principle).

### Traditional vs Evolutionary Approach

| Traditional Architecture | Evolutionary Architecture |
|-------------------------|--------------------------|
| Comprehensive upfront design | Incremental, guided evolution |
| Decisions based on assumptions | Decisions based on data |
| Fixed architecture | Architecture that adapts |
| Manual validation | Automated validation |
| "Big Design Up Front" | "Last Responsible Moment" |

---

## 🏗️ Fundamental Principles

### 1. Architecture Must Evolve Based on Actual Needs

**Key Point**: Architecture must evolve based on actual needs, not assumptions.

**Why This Matters**:
- Requirements change over time
- User needs become clearer with usage
- Business constraints evolve
- Technology landscape shifts

**How to Apply**:
- Start with minimal viable architecture
- Add complexity only when data shows it's needed
- Measure actual usage patterns
- Evolve based on real metrics

### 2. Use Guidelines and Metrics to Guide Evolution

**Key Point**: Use guidelines and metrics to guide evolution.

**What This Means**:
- Define architectural guidelines that support evolution
- Establish metrics to measure architectural health
- Create fitness functions to validate architectural constraints
- Monitor metrics continuously

**Implementation**:
- Document architectural guidelines (see [Guidelines Template](./guidelines-template.md))
- Define metrics for architectural decisions (see [Metrics Definition](./metrics-definition.md))
- Create automated checks for guidelines
- Review metrics regularly

### 3. Automate Architectural Decisions When Possible

**Key Point**: Automate architectural decisions when possible.

**Benefits**:
- Consistency across the system
- Reduced human error
- Faster feedback cycles
- Enforced architectural constraints

**Examples**:
- Automated dependency analysis
- Architectural tests (fitness functions)
- Code generation for common patterns
- Automated refactoring tools

See [Automation Strategies](./automation-strategies.md) for detailed approaches.

### 4. Focus on What's Truly Required

**Key Point**: Focus on what's truly required (minimize required system).

**Related Concepts**:
- **YAGNI** (You Aren't Gonna Need It): Don't build features you don't need
- **Last Responsible Moment**: Delay decisions until you have enough information
- **Minimum Viable Architecture**: Start with the simplest architecture that works

**Anti-Pattern to Avoid**:
> "E se no futuro o cliente quiser adicionar PIX, boleto, PayPal ou criptomoeda? Melhor já estruturar tudo para suportar qualquer meio de pagamento."

This leads to over-engineering and unnecessary complexity.

---

## 🔬 Fitness Functions

### What are Fitness Functions?

Fitness functions are objective, quantifiable criteria that measure how well a system meets its architectural goals. They act as automated tests for architectural constraints.

**Characteristics**:
- **Objective**: Measurable, not subjective
- **Automated**: Can run in CI/CD pipelines
- **Continuous**: Monitored over time
- **Actionable**: Provide clear feedback

### Types of Fitness Functions

#### 1. Structural Fitness Functions
Measure structural aspects of the architecture:

- **Coupling metrics**: Measure dependencies between modules
- **Cyclomatic complexity**: Measure code complexity
- **Layer violations**: Detect violations of architectural layers
- **Code organization**: Verify package/module structure

**Example** (TypeScript):
```typescript
// Fitness function: No domain layer should import from infrastructure
describe('Architectural Constraints', () => {
  it('should not allow domain layer to import infrastructure', () => {
    const domainFiles = findFiles('src/domain/**/*.ts');
    const violations = domainFiles.filter(file => 
      file.content.includes('from "../infrastructure"')
    );
    expect(violations).toHaveLength(0);
  });
});
```

#### 2. Quality Fitness Functions
Measure code quality metrics:

- **Test coverage**: Minimum coverage thresholds
- **Performance benchmarks**: Response time, throughput
- **Security scans**: Vulnerability detection
- **Code smells**: Detect code quality issues

#### 3. Business Fitness Functions
Measure how well architecture supports business goals:

- **Deployment frequency**: How often can we deploy?
- **Lead time**: Time from commit to production
- **Mean time to recovery**: How quickly can we recover from failures?
- **Change failure rate**: Percentage of changes that fail

---

## 📊 Metrics for Evolutionary Architecture

### Key Metrics to Track

#### Architectural Metrics

1. **Coupling Metrics**
   - Number of dependencies between modules
   - Cyclic dependencies detection
   - Static coupling analysis
   - Dynamic coupling analysis

2. **Cohesion Metrics**
   - Module cohesion scores
   - Functional cohesion
   - Logical cohesion

3. **Complexity Metrics**
   - Cyclomatic complexity
   - Cognitive complexity
   - Architectural complexity

#### Evolution Metrics

1. **Change Velocity**
   - How quickly can we make changes?
   - Time to implement new features
   - Refactoring frequency

2. **Change Cost**
   - Cost of making architectural changes
   - Impact analysis of changes
   - Breaking change frequency

3. **Stability Metrics**
   - Rate of architectural changes
   - Deprecation patterns
   - Version compatibility

See [Metrics Definition Guide](./metrics-definition.md) for detailed metrics definitions and implementation.

---

## 🎨 Guidelines for Evolution

Architectural guidelines provide direction for how the architecture should evolve while maintaining integrity.

### Key Guidelines

1. **Modularity**: System should be decomposed into independent modules
2. **Loose Coupling**: Modules should have minimal dependencies
3. **High Cohesion**: Related functionality should be grouped together
4. **Clear Boundaries**: Well-defined boundaries between modules
5. **Testability**: Architecture should support testing
6. **Observability**: System behavior should be observable
7. **Security**: Security should be built-in, not added later

### Creating Guidelines

Use the [Guidelines Template](./guidelines-template.md) to document your architectural guidelines.

**Example Guideline**:
```markdown
## Guideline: Dependency Direction

**Rule**: Dependencies must point inward toward the domain layer.

**Rationale**: Domain should not depend on infrastructure or application layers.

**Validation**: Automated check in CI/CD pipeline.

**Examples**:
- ✅ `infrastructure -> application -> domain`
- ❌ `domain -> infrastructure`
```

---

## 🤖 Automation Strategies

Automating architectural decisions and validations is crucial for evolutionary architecture.

### Areas for Automation

1. **Dependency Analysis**
   - Automated dependency graphs
   - Circular dependency detection
   - Layer violation detection

2. **Architectural Testing**
   - Fitness functions in test suites
   - Automated architecture tests
   - Continuous validation

3. **Code Generation**
   - Template-based code generation
   - Scaffolding tools
   - Pattern enforcement

4. **Refactoring Support**
   - Automated refactoring tools
   - Refactoring patterns
   - Migration tools

See [Automation Strategies](./automation-strategies.md) for detailed approaches and examples.

---

## 📚 Code Examples

### TypeScript Example: Fitness Function

```typescript
// fitness-functions/architectural-tests.ts
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * Fitness Function: Verify no circular dependencies
 */
export async function testNoCircularDependencies(): Promise<void> {
  try {
    // Use madge to detect circular dependencies
    const { stdout } = await execAsync('madge --circular src/');
    
    if (stdout.trim()) {
      throw new Error(`Circular dependencies detected:\n${stdout}`);
    }
  } catch (error: any) {
    if (error.code === 'ENOENT') {
      console.warn('madge not installed, skipping circular dependency check');
      return;
    }
    throw error;
  }
}

/**
 * Fitness Function: Verify layer dependencies
 */
export function testLayerDependencies(files: string[]): void {
  const violations: string[] = [];
  
  files.forEach(file => {
    const content = readFileSync(file, 'utf-8');
    
    // Domain layer should not import from infrastructure
    if (file.includes('/domain/') && content.includes('from "../infrastructure"')) {
      violations.push(file);
    }
  });
  
  if (violations.length > 0) {
    throw new Error(
      `Layer dependency violations:\n${violations.join('\n')}`
    );
  }
}
```

### Go Example: Architectural Metrics

```go
// pkg/architecture/metrics.go
package architecture

import (
    "go/ast"
    "go/parser"
    "go/token"
    "os"
    "path/filepath"
)

// CouplingMetric measures coupling between packages
type CouplingMetric struct {
    Package     string
    Dependencies []string
    CouplingScore int
}

// AnalyzeCoupling analyzes coupling in a Go project
func AnalyzeCoupling(rootPath string) ([]CouplingMetric, error) {
    var metrics []CouplingMetric
    
    err := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }
        
        if !info.IsDir() || filepath.Ext(path) != "" {
            return nil
        }
        
        fset := token.NewFileSet()
        pkgs, err := parser.ParseDir(fset, path, nil, parser.ParseComments)
        if err != nil {
            return err
        }
        
        for pkgName, pkg := range pkgs {
            metric := CouplingMetric{
                Package: pkgName,
            }
            
            // Analyze imports to determine dependencies
            for _, file := range pkg.Files {
                ast.Inspect(file, func(n ast.Node) bool {
                    imp, ok := n.(*ast.ImportSpec)
                    if ok {
                        metric.Dependencies = append(metric.Dependencies, imp.Path.Value)
                    }
                    return true
                })
            }
            
            metric.CouplingScore = len(metric.Dependencies)
            metrics = append(metrics, metric)
        }
        
        return nil
    })
    
    return metrics, err
}
```

### Python Example: Automated Guideline Validation

```python
# tools/arch_validation.py
"""Architectural validation tools for evolutionary architecture."""

import ast
import os
from pathlib import Path
from typing import List, Dict, Set

class ArchitecturalValidator:
    """Validates architectural guidelines automatically."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.violations: List[Dict] = []
    
    def validate_dependency_direction(self) -> bool:
        """
        Validate that dependencies point inward (infrastructure -> domain).
        
        Returns:
            True if valid, False otherwise
        """
        domain_files = list(self.project_root.glob("**/domain/**/*.py"))
        
        for file_path in domain_files:
            with open(file_path) as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    # Check if domain is importing from infrastructure
                    if "infrastructure" in module or "application" in module:
                        self.violations.append({
                            "file": str(file_path),
                            "violation": f"Domain layer imports from {module}",
                            "rule": "dependency-direction"
                        })
        
        return len(self.violations) == 0
    
    def validate_layer_isolation(self) -> bool:
        """Validate that layers are properly isolated."""
        # Implementation for layer isolation checks
        pass
    
    def report(self) -> str:
        """Generate violation report."""
        if not self.violations:
            return "✅ No architectural violations found"
        
        report = "❌ Architectural Violations Found:\n\n"
        for violation in self.violations:
            report += f"  - {violation['file']}\n"
            report += f"    Rule: {violation['rule']}\n"
            report += f"    Issue: {violation['violation']}\n\n"
        
        return report

# Usage example
if __name__ == "__main__":
    validator = ArchitecturalValidator(Path("."))
    validator.validate_dependency_direction()
    print(validator.report())
```

---

## 🔄 Evolution Process

### Step-by-Step Evolution Process

1. **Measure Current State**
   - Collect architectural metrics
   - Identify pain points
   - Analyze current constraints

2. **Identify Evolution Needs**
   - Review metrics and feedback
   - Identify areas for improvement
   - Prioritize changes

3. **Design Evolution**
   - Create evolution plan
   - Define new guidelines if needed
   - Plan incremental changes

4. **Implement Changes**
   - Make incremental changes
   - Maintain fitness functions
   - Monitor metrics

5. **Validate Evolution**
   - Run fitness functions
   - Check metrics
   - Validate guidelines

6. **Document Changes**
   - Update documentation
   - Record ADRs if significant
   - Share learnings

### Incremental Evolution

**Key Principle**: Make small, incremental changes rather than big-bang refactorings.

**Benefits**:
- Lower risk
- Easier to validate
- Faster feedback
- Less disruption

**Example Evolution Path**:
```
Initial: Monolithic Application
  ↓
Step 1: Extract module to separate service
  ↓
Step 2: Add event-driven communication
  ↓
Step 3: Implement CQRS for read/write separation
  ↓
Step 4: Scale horizontally
```

---

## 🚨 Common Pitfalls

### 1. Over-Engineering Upfront

**Problem**: Building for hypothetical future needs.

**Solution**: Apply YAGNI principle. Build what you need now, evolve when needed.

### 2. Ignoring Metrics

**Problem**: Making architectural decisions without data.

**Solution**: Always collect and review metrics before making decisions.

### 3. Breaking Fitness Functions

**Problem**: Allowing violations of architectural constraints.

**Solution**: Fitness functions must be non-negotiable. Fix violations immediately.

### 4. Big-Bang Refactoring

**Problem**: Trying to evolve everything at once.

**Solution**: Make incremental changes. Evolve one aspect at a time.

### 5. Neglecting Documentation

**Problem**: Architecture evolves but documentation doesn't.

**Solution**: Keep documentation in sync with architecture. Update ADRs and guidelines.

---

## 🔗 Related Documentation

- [Guidelines Template](../../templates/evolutionary-architecture/guidelines-template.md) - Template for creating architectural guidelines
- [Metrics Definition](./metrics-definition.md) - Guide to defining metrics for architectural decisions
- [Automation Strategies](./automation-strategies.md) - Strategies for automating architectural decisions
- [Strategic DDD Guide](../ddd/strategic-ddd/README.md) - Strategic Domain-Driven Design (complements evolutionary architecture)
- [Technical Decision Making Process](../../processes/technical-decision-making/README.md) - Process for making architectural decisions
- [ADR Template](../../templates/adr-template.md) - Architecture Decision Record template

**Versão em Português**: [Guia de Arquitetura Evolutiva (PT-BR)](./pt-br/README.md)

---

## 📖 Recommended Reading

1. **Building Evolutionary Architectures** by Neal Ford, Rebecca Parsons, and Patrick Kua
   - Core book on evolutionary architecture concepts
   - Fitness functions and guided change

2. **Refactoring Databases** by Scott Ambler and Pramod Sadalage
   - Evolutionary database design

3. **Accelerate** by Nicole Forsgren, Jez Humble, and Gene Kim
   - Metrics for software delivery performance

---

## 🎯 Quick Reference

### When to Apply Evolutionary Architecture

✅ **Good Fit For**:
- Projects with changing requirements
- Systems that need to scale
- Teams comfortable with incremental changes
- When data-driven decisions are possible

❌ **Not Ideal For**:
- Systems with very strict constraints (regulatory, safety-critical)
- When upfront design is required by stakeholders
- Teams not ready for continuous evolution

### Key Takeaways

1. **Measure Everything**: Collect metrics on architectural health
2. **Automate Validation**: Use fitness functions to enforce constraints
3. **Evolve Incrementally**: Make small, validated changes
4. **Document Decisions**: Keep ADRs and guidelines updated
5. **Focus on Needs**: Build what you need, evolve when needed

---

**Last Updated**: 2025-01-20  
**Version**: 1.0  
**Maintainer**: Skynet Documentation Team  
**Status**: ✅ Active

---

**Related Guides**:
- [PT-BR Version](./pt-br/guia-arquitetura-evolutiva.md) 🇧🇷

