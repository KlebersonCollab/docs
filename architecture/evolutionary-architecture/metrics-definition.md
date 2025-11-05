# Metrics Definition Guide

## 📋 Overview

This guide explains how to define and use metrics for architectural decisions in evolutionary architecture. Metrics provide objective, quantifiable measures of architectural health and guide evolution decisions.

**Key Principle**: Architectural decisions should be based on actual metrics and data, not speculation.

---

## 🎯 Why Metrics Matter

### Data-Driven Decisions

Metrics enable:
- **Objective Evaluation**: Measure architectural health objectively
- **Trend Analysis**: Track evolution over time
- **Early Detection**: Identify issues before they become problems
- **Informed Decisions**: Base decisions on actual data, not assumptions

### Types of Architectural Metrics

1. **Structural Metrics**: Measure code structure and organization
2. **Quality Metrics**: Measure code quality and maintainability
3. **Performance Metrics**: Measure system performance
4. **Evolution Metrics**: Measure how easily the architecture can evolve
5. **Business Metrics**: Measure business value delivery

---

## 📊 Core Metrics Categories

### 1. Coupling Metrics

Coupling measures the interdependence between modules or components.

#### Afferent Coupling (Ca)
**Definition**: Number of modules that depend on a given module.

**Measurement**:
```typescript
// Example: Count incoming dependencies
function calculateAfferentCoupling(moduleName: string): number {
  const allFiles = getAllSourceFiles();
  return allFiles.filter(file => 
    file.imports.includes(moduleName)
  ).length;
}
```

**Target**: Lower is better, but some modules (like core domain) should have higher Ca.

#### Efferent Coupling (Ce)
**Definition**: Number of modules that a given module depends on.

**Measurement**:
```typescript
// Example: Count outgoing dependencies
function calculateEfferentCoupling(modulePath: string): number {
  const module = parseModule(modulePath);
  return module.imports.length;
}
```

**Target**: Lower is better. Modules with high Ce are tightly coupled.

#### Instability (I)
**Definition**: Ratio of efferent coupling to total coupling.

**Formula**: `I = Ce / (Ca + Ce)`

**Range**: 0 (stable) to 1 (unstable)

**Target**: 
- Stable modules (I ≈ 0): Core domain, shared utilities
- Unstable modules (I ≈ 1): UI components, infrastructure adapters

#### Abstractness (A)
**Definition**: Ratio of abstract elements (interfaces, abstract classes) to total elements.

**Formula**: `A = AbstractElements / TotalElements`

**Range**: 0 (concrete) to 1 (fully abstract)

#### Distance from Main Sequence (D)
**Definition**: Distance from the ideal relationship between abstractness and instability.

**Formula**: `D = |A + I - 1|`

**Target**: D should be close to 0 for well-designed modules.

### 2. Cohesion Metrics

Cohesion measures how well the elements within a module work together.

#### LCOM (Lack of Cohesion of Methods)
**Definition**: Measures how methods in a class are related.

**Calculation**:
1. For each method pair, check if they share instance variables
2. Count pairs that don't share variables
3. Subtract pairs that do share variables

**Target**: Lower LCOM is better. LCOM = 0 indicates perfect cohesion.

#### Functional Cohesion
**Definition**: Measures how well methods contribute to a single, well-defined purpose.

**Assessment**: Qualitative rather than quantitative.

**Target**: High functional cohesion - each module has one clear purpose.

### 3. Complexity Metrics

#### Cyclomatic Complexity
**Definition**: Measures the number of linearly independent paths through code.

**Calculation**: Based on decision points (if, while, for, case, etc.)

**Target**: 
- Low (1-10): Simple, testable
- Medium (11-20): Moderately complex
- High (21+): Needs refactoring

**Example**:
```go
// Low complexity (CC = 2)
func ProcessOrder(order Order) error {
    if order.IsEmpty() {
        return ErrEmptyOrder
    }
    return nil
}

// High complexity (CC = 8)
func ProcessOrder(order Order) error {
    if order.IsEmpty() {
        return ErrEmptyOrder
    }
    if order.Items.Count > 10 {
        // ... more nested conditions
    }
    // ... many more decision points
}
```

#### Cognitive Complexity
**Definition**: Measures how difficult code is to understand (considers nesting).

**Target**: Lower is better. Similar to cyclomatic complexity but more human-focused.

### 4. Dependency Metrics

#### Dependency Depth
**Definition**: Maximum depth of dependency chain.

**Target**: Keep dependency chains shallow (depth < 5).

#### Circular Dependency Detection
**Definition**: Detection of circular dependencies between modules.

**Target**: Zero circular dependencies.

**Example Check**:
```python
# Check for circular dependencies
def has_circular_dependency(modules: Dict[str, List[str]]) -> bool:
    """Detect circular dependencies using DFS."""
    visited = set()
    rec_stack = set()
    
    def has_cycle(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in modules.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    for module in modules:
        if module not in visited:
            if has_cycle(module):
                return True
    
    return False
```

### 5. Evolution Metrics

#### Change Velocity
**Definition**: How quickly can changes be made to the architecture.

**Measures**:
- Time to implement new features
- Time to refactor
- Deployment frequency

**Target**: High change velocity indicates evolvable architecture.

#### Change Cost
**Definition**: Cost of making architectural changes.

**Measures**:
- Number of files affected
- Test failures after changes
- Documentation updates needed

**Target**: Lower change cost indicates better evolvability.

#### Architectural Drift
**Definition**: Measure of how far architecture has drifted from intended design.

**Measures**:
- Number of guideline violations
- Fitness function failures
- Architectural debt

**Target**: Low architectural drift indicates well-maintained architecture.

---

## 📈 Defining Your Metrics

### Step 1: Identify What to Measure

Ask these questions:
1. What architectural concerns are most important?
2. What would indicate architectural health?
3. What metrics would guide evolution decisions?

### Step 2: Define Measurement Method

For each metric:
1. **Calculation Method**: How is it calculated?
2. **Collection**: How is data collected?
3. **Frequency**: How often is it measured?
4. **Tools**: What tools are used?

### Step 3: Set Targets

Define:
1. **Baseline**: Current value
2. **Target**: Desired value
3. **Threshold**: Alert/warning levels
4. **Trend**: Expected direction

### Step 4: Automate Collection

**Example**: Automated metrics collection

```typescript
// metrics/collector.ts
export class ArchitectureMetricsCollector {
  async collectAll(): Promise<MetricsReport> {
    return {
      coupling: await this.collectCoupling(),
      cohesion: await this.collectCohesion(),
      complexity: await this.collectComplexity(),
      dependencies: await this.collectDependencies(),
      evolution: await this.collectEvolution(),
    };
  }
  
  private async collectCoupling(): Promise<CouplingMetrics> {
    // Implement coupling metric collection
  }
  
  // ... other collection methods
}
```

### Step 5: Visualize and Monitor

Create dashboards showing:
- Current values
- Trends over time
- Target vs actual
- Alerts for thresholds

---

## 🛠️ Implementation Examples

### TypeScript: Coupling Metrics

```typescript
// metrics/coupling.ts
import { Project } from 'ts-morph';
import * as path from 'path';

export interface CouplingMetrics {
  afferentCoupling: number;
  efferentCoupling: number;
  instability: number;
}

export class CouplingAnalyzer {
  constructor(private project: Project) {}
  
  analyzeModule(modulePath: string): CouplingMetrics {
    const module = this.project.getSourceFile(modulePath);
    if (!module) {
      throw new Error(`Module not found: ${modulePath}`);
    }
    
    // Calculate efferent coupling
    const efferentCoupling = module.getImportDeclarations().length;
    
    // Calculate afferent coupling
    const allFiles = this.project.getSourceFiles();
    const afferentCoupling = allFiles.filter(file => {
      const imports = file.getImportDeclarations();
      return imports.some(imp => 
        imp.getModuleSpecifierValue().includes(modulePath)
      );
    }).length;
    
    // Calculate instability
    const totalCoupling = afferentCoupling + efferentCoupling;
    const instability = totalCoupling > 0 
      ? efferentCoupling / totalCoupling 
      : 0;
    
    return {
      afferentCoupling,
      efferentCoupling,
      instability,
    };
  }
}
```

### Go: Complexity Metrics

```go
// pkg/metrics/complexity.go
package metrics

import (
    "go/ast"
    "go/parser"
    "go/token"
)

// CyclomaticComplexity calculates cyclomatic complexity
func CyclomaticComplexity(funcDecl *ast.FuncDecl) int {
    complexity := 1 // Base complexity
    
    ast.Inspect(funcDecl, func(n ast.Node) bool {
        switch n.(type) {
        case *ast.IfStmt, *ast.ForStmt, *ast.RangeStmt,
             *ast.SwitchStmt, *ast.TypeSwitchStmt,
             *ast.SelectStmt, *ast.BinaryExpr:
            complexity++
        }
        return true
    })
    
    return complexity
}

// AnalyzeFunction analyzes complexity of a function
func AnalyzeFunction(filePath string, funcName string) (int, error) {
    fset := token.NewFileSet()
    f, err := parser.ParseFile(fset, filePath, nil, parser.ParseComments)
    if err != nil {
        return 0, err
    }
    
    for _, decl := range f.Decls {
        if fn, ok := decl.(*ast.FuncDecl); ok {
            if fn.Name.Name == funcName {
                return CyclomaticComplexity(fn), nil
            }
        }
    }
    
    return 0, fmt.Errorf("function %s not found", funcName)
}
```

### Python: Dependency Metrics

```python
# metrics/dependencies.py
"""Dependency analysis metrics."""

import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class DependencyAnalyzer:
    """Analyzes dependency metrics for a Python project."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.modules: Dict[str, Set[str]] = {}
    
    def analyze_dependencies(self) -> Dict[str, any]:
        """Analyze all dependency metrics."""
        self._collect_imports()
        
        return {
            "circular_dependencies": self._find_circular_dependencies(),
            "dependency_depth": self._calculate_max_depth(),
            "module_dependencies": self._count_dependencies_per_module(),
        }
    
    def _collect_imports(self) -> None:
        """Collect all imports from Python files."""
        for py_file in self.project_root.rglob("*.py"):
            if "test" in str(py_file):
                continue
            
            module_name = self._get_module_name(py_file)
            imports = self._extract_imports(py_file)
            self.modules[module_name] = imports
    
    def _get_module_name(self, file_path: Path) -> str:
        """Get module name from file path."""
        relative = file_path.relative_to(self.project_root)
        return str(relative).replace("/", ".").replace(".py", "")
    
    def _extract_imports(self, file_path: Path) -> Set[str]:
        """Extract import statements from a Python file."""
        with open(file_path) as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
        
        return imports
    
    def _find_circular_dependencies(self) -> List[Tuple[str, str]]:
        """Find circular dependencies using DFS."""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def has_cycle(node: str, path: List[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.modules.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(tuple(path[cycle_start:] + [neighbor]))
                    return True
            
            rec_stack.remove(node)
            path.pop()
            return False
        
        for module in self.modules:
            if module not in visited:
                has_cycle(module, [])
        
        return cycles
    
    def _calculate_max_depth(self) -> int:
        """Calculate maximum dependency depth."""
        max_depth = 0
        
        def calculate_depth(module: str, visited: Set[str], depth: int) -> int:
            if module in visited:
                return depth
            visited.add(module)
            
            current_max = depth
            for dep in self.modules.get(module, []):
                dep_depth = calculate_depth(dep, visited.copy(), depth + 1)
                current_max = max(current_max, dep_depth)
            
            return current_max
        
        for module in self.modules:
            depth = calculate_depth(module, set(), 0)
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _count_dependencies_per_module(self) -> Dict[str, int]:
        """Count dependencies per module."""
        return {
            module: len(deps)
            for module, deps in self.modules.items()
        }
```

---

## 📊 Metrics Dashboard

### Recommended Metrics Dashboard

Create a dashboard showing:

1. **Current Metrics**
   - All metrics with current values
   - Target values
   - Status (✅/⚠️/❌)

2. **Trends**
   - Metrics over time (graphs)
   - Improvement/degradation indicators

3. **Alerts**
   - Metrics exceeding thresholds
   - Rapid changes
   - Violations

### Example Dashboard Structure

```markdown
## Architecture Metrics Dashboard

### Coupling Metrics
| Module | Afferent | Efferent | Instability | Status |
|--------|----------|----------|-------------|--------|
| domain | 5 | 0 | 0.0 | ✅ |
| application | 3 | 2 | 0.4 | ✅ |
| infrastructure | 1 | 5 | 0.83 | ⚠️ |

### Complexity Metrics
| File | Cyclomatic | Cognitive | Status |
|------|------------|-----------|--------|
| OrderService.ts | 8 | 5 | ✅ |
| PaymentProcessor.ts | 15 | 12 | ✅ |
| OrderValidator.ts | 25 | 18 | ⚠️ |

### Dependency Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Max Depth | 4 | < 5 | ✅ |
| Circular Deps | 0 | 0 | ✅ |
| Avg Dependencies | 3.2 | < 5 | ✅ |
```

---

## 🎯 Using Metrics for Evolution

### Decision Framework

When metrics indicate issues:

1. **Identify Problem**: Which metric shows the problem?
2. **Analyze Root Cause**: Why is the metric at this level?
3. **Plan Evolution**: How can we improve this metric?
4. **Implement Change**: Make incremental changes
5. **Measure Impact**: Did the change improve the metric?

### Metric-Driven Refactoring

**Example**: High coupling detected

1. **Current State**: Module A has efferent coupling of 10
2. **Target**: Reduce to 5
3. **Plan**: Extract shared dependencies into a new module
4. **Implement**: Create module B, refactor A to use B
5. **Verify**: Measure coupling again (should be ~5)

---

## 📝 Best Practices

### Choose Meaningful Metrics

✅ **DO**:
- Focus on metrics that guide evolution
- Measure what matters for architectural health
- Combine multiple metrics for better insight

❌ **DON'T**:
- Measure everything (metric fatigue)
- Rely on single metrics in isolation
- Ignore metrics that don't fit expectations

### Automate Collection

- Collect metrics automatically
- Run in CI/CD pipeline
- Store historical data
- Generate reports regularly

### Review Regularly

- Review metrics weekly/monthly
- Identify trends
- Adjust targets based on learnings
- Remove metrics that no longer serve

### Act on Metrics

Metrics are useless if not acted upon:
- Set clear thresholds
- Create alerts for violations
- Make metrics visible to team
- Use metrics in decision-making

---

**Last Updated**: 2025-01-20  
**Version**: 1.0  
**Maintainer**: Skynet Documentation Team

---

**Related Documents**:
- [Evolutionary Architecture Guide](./README.md)
- [Guidelines Template](../../templates/evolutionary-architecture/guidelines-template.md)
- [Automation Strategies](./automation-strategies.md)

**Versão em Português**: [Guia de Definição de Métricas (PT-BR)](./pt-br/metrics-definition.md)

