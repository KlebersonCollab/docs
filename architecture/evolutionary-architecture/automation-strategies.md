# Automation Strategies for Evolutionary Architecture

## 📋 Overview

Automating architectural decisions and validations is crucial for evolutionary architecture. Automation ensures consistency, reduces human error, provides faster feedback, and enforces architectural constraints continuously.

**Key Principle**: Automate architectural decisions when possible.

---

## 🎯 Why Automate?

### Benefits

1. **Consistency**: Automated checks ensure rules are enforced uniformly
2. **Speed**: Automated validation provides instant feedback
3. **Reliability**: Reduces human error in validation
4. **Scalability**: Can check entire codebase quickly
5. **Documentation**: Automated checks serve as executable documentation

### When to Automate

✅ **Good Candidates for Automation**:
- Repeated checks (run on every commit)
- Objective rules (can be clearly defined)
- High-impact constraints (critical for architecture)
- Validation rules (can be checked automatically)

❌ **Not Suitable for Automation**:
- Subjective decisions (require human judgment)
- One-time assessments
- Complex business logic validation
- Design pattern application (can guide, but not enforce)

---

## 🔧 Automation Areas

### 1. Dependency Analysis

#### Automated Dependency Graphs

**Purpose**: Visualize and validate dependency structure.

**Tools**:
- TypeScript: `madge`, `dependency-cruiser`
- Go: `go mod graph`, custom tools
- Python: `pydeps`, `pipdeptree`

**Example** (TypeScript):
```typescript
// scripts/analyze-dependencies.ts
import { createMadge } from 'madge';

async function analyzeDependencies() {
  const madge = await createMadge('src/', {
    fileExtensions: ['ts', 'tsx'],
  });
  
  // Generate dependency graph
  await madge.image('docs/dependency-graph.svg');
  
  // Check for circular dependencies
  const circular = await madge.circular();
  if (circular.length > 0) {
    throw new Error(`Circular dependencies found: ${circular}`);
  }
  
  // Analyze dependencies
  const dependencies = await madge.obj();
  console.log('Dependency analysis:', dependencies);
}

analyzeDependencies().catch(console.error);
```

#### Layer Violation Detection

**Purpose**: Ensure architectural layers are respected.

**Example** (Go):
```go
// tools/check-layers.go
package main

import (
    "fmt"
    "go/ast"
    "go/parser"
    "go/token"
    "os"
    "path/filepath"
    "strings"
)

type LayerChecker struct {
    violations []string
}

func (c *LayerChecker) Check(path string) error {
    return filepath.Walk(path, func(filePath string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }
        
        if !strings.HasSuffix(filePath, ".go") {
            return nil
        }
        
        // Parse file
        fset := token.NewFileSet()
        f, err := parser.ParseFile(fset, filePath, nil, parser.ParseComments)
        if err != nil {
            return err
        }
        
        // Check if domain imports infrastructure
        if strings.Contains(filePath, "domain/") {
            ast.Inspect(f, func(n ast.Node) bool {
                imp, ok := n.(*ast.ImportSpec)
                if ok {
                    importPath := strings.Trim(imp.Path.Value, "\"")
                    if strings.Contains(importPath, "infrastructure") {
                        c.violations = append(c.violations, 
                            fmt.Sprintf("%s: domain imports infrastructure", filePath))
                    }
                }
                return true
            })
        }
        
        return nil
    })
}

func main() {
    checker := &LayerChecker{}
    if err := checker.Check("."); err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }
    
    if len(checker.violations) > 0 {
        fmt.Fprintf(os.Stderr, "Layer violations found:\n")
        for _, v := range checker.violations {
            fmt.Fprintf(os.Stderr, "  - %s\n", v)
        }
        os.Exit(1)
    }
    
    fmt.Println("✅ No layer violations found")
}
```

#### Circular Dependency Detection

**Purpose**: Detect and prevent circular dependencies.

**Example** (Python):
```python
# tools/detect_circular_deps.py
"""Detect circular dependencies in Python project."""

import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple

def detect_circular_dependencies(project_root: Path) -> List[Tuple[str, ...]]:
    """Detect circular dependencies using DFS."""
    modules = _collect_modules(project_root)
    cycles = []
    
    def has_cycle(node: str, path: List[str], visited: Set[str], rec_stack: Set[str]) -> bool:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in modules.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, path, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                # Found cycle
                cycle_start = path.index(neighbor)
                cycle = tuple(path[cycle_start:] + [neighbor])
                cycles.append(cycle)
                return True
        
        rec_stack.remove(node)
        path.pop()
        return False
    
    visited = set()
    for module in modules:
        if module not in visited:
            has_cycle(module, [], visited, set())
    
    return cycles

def _collect_modules(project_root: Path) -> Dict[str, Set[str]]:
    """Collect module imports."""
    modules = {}
    
    for py_file in project_root.rglob("*.py"):
        if "test" in str(py_file):
            continue
        
        module_name = _get_module_name(py_file, project_root)
        imports = _extract_imports(py_file)
        modules[module_name] = imports
    
    return modules

# ... (implementation details)

if __name__ == "__main__":
    project_root = Path(".")
    cycles = detect_circular_dependencies(project_root)
    
    if cycles:
        print("❌ Circular dependencies found:")
        for cycle in cycles:
            print(f"  {' -> '.join(cycle)}")
        exit(1)
    else:
        print("✅ No circular dependencies found")
```

### 2. Architectural Testing (Fitness Functions)

#### Automated Architecture Tests

**Purpose**: Validate architectural constraints continuously.

**Example** (TypeScript with Jest):
```typescript
// tests/architecture/constraints.test.ts
import { Project } from 'ts-morph';
import * as path from 'path';
import * as fs from 'fs';

describe('Architectural Constraints', () => {
  let project: Project;
  
  beforeAll(() => {
    project = new Project({
      tsConfigFilePath: 'tsconfig.json',
    });
  });
  
  describe('Layer Dependencies', () => {
    it('should not allow domain to import from infrastructure', () => {
      const domainFiles = project.getSourceFiles()
        .filter(f => f.getFilePath().includes('/domain/'));
      
      const violations: string[] = [];
      
      domainFiles.forEach(file => {
        const imports = file.getImportDeclarations();
        imports.forEach(imp => {
          const importPath = imp.getModuleSpecifierValue();
          if (importPath.includes('/infrastructure/') || 
              importPath.includes('/application/')) {
            violations.push(
              `${file.getFilePath()}: imports ${importPath}`
            );
          }
        });
      });
      
      expect(violations).toHaveLength(0);
    });
    
    it('should not allow application to import from infrastructure directly', () => {
      // Similar check for application layer
    });
  });
  
  describe('Dependency Rules', () => {
    it('should not have circular dependencies', async () => {
      // Check for circular dependencies
      const { exec } = require('child_process');
      const { promisify } = require('util');
      const execAsync = promisify(exec);
      
      try {
        const { stdout } = await execAsync('madge --circular src/');
        if (stdout.trim()) {
          throw new Error(`Circular dependencies:\n${stdout}`);
        }
      } catch (error: any) {
        if (error.stdout) {
          throw error;
        }
        // madge not installed, skip check
      }
    });
  });
  
  describe('Code Organization', () => {
    it('should have correct module structure', () => {
      const expectedStructure = [
        'src/domain/',
        'src/application/',
        'src/infrastructure/',
      ];
      
      expectedStructure.forEach(dir => {
        expect(fs.existsSync(dir)).toBe(true);
      });
    });
  });
});
```

#### Complexity Validation

**Purpose**: Ensure code complexity stays within limits.

**Example** (Go with golangci-lint):
```go
// .golangci.yml configuration
linters:
  enable:
    - gocyclo
    - gocognit

linters-settings:
  gocyclo:
    min-complexity: 15  # Fail if complexity > 15
  gocognit:
    min-complexity: 15  # Cognitive complexity limit

issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - gocyclo  # Allow higher complexity in tests
```

**Example** (Python with radon):
```python
# scripts/check_complexity.py
"""Check code complexity using radon."""

from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor
from pathlib import Path

def check_complexity(file_path: Path, max_complexity: int = 15) -> bool:
    """Check if file complexity is within limits."""
    with open(file_path) as f:
        code = f.read()
    
    blocks = cc_visit(code)
    violations = []
    
    for block in blocks:
        if block.complexity > max_complexity:
            violations.append({
                'name': block.name,
                'complexity': block.complexity,
                'line': block.lineno,
            })
    
    if violations:
        print(f"❌ Complexity violations in {file_path}:")
        for v in violations:
            print(f"  {v['name']} (line {v['line']}): complexity {v['complexity']}")
        return False
    
    return True

if __name__ == "__main__":
    project_root = Path(".")
    all_good = True
    
    for py_file in project_root.rglob("*.py"):
        if "test" in str(py_file):
            continue
        if not check_complexity(py_file):
            all_good = False
    
    exit(0 if all_good else 1)
```

### 3. Code Generation

#### Template-Based Code Generation

**Purpose**: Generate boilerplate code following architectural patterns.

**Example** (TypeScript with Plop):
```javascript
// plopfile.js
module.exports = function(plop) {
  // Generator for domain entities
  plop.setGenerator('domain-entity', {
    description: 'Create a new domain entity',
    prompts: [{
      type: 'input',
      name: 'name',
      message: 'Entity name:',
    }],
    actions: [{
      type: 'add',
      path: 'src/domain/entities/{{pascalCase name}}.ts',
      templateFile: 'templates/domain-entity.hbs',
    }],
  });
  
  // Generator for use cases
  plop.setGenerator('use-case', {
    description: 'Create a new use case',
    prompts: [{
      type: 'input',
      name: 'name',
      message: 'Use case name:',
    }],
    actions: [{
      type: 'add',
      path: 'src/application/use-cases/{{pascalCase name}}UseCase.ts',
      templateFile: 'templates/use-case.hbs',
    }],
  });
};
```

**Template** (Handlebars):
```handlebars
// templates/domain-entity.hbs
export class {{pascalCase name}} {
  constructor(
    private readonly id: {{pascalCase name}}Id,
    // Add properties here
  ) {}
  
  // Add business logic methods here
}
```

#### Scaffolding Tools

**Purpose**: Generate project structure following architectural guidelines.

**Example** (Custom Go tool):
```go
// tools/scaffold.go
package main

import (
    "fmt"
    "os"
    "path/filepath"
    "text/template"
)

type ProjectStructure struct {
    Name string
    Modules []string
}

func scaffoldCleanArchitecture(projectName string) error {
    structure := ProjectStructure{
        Name: projectName,
        Modules: []string{"domain", "application", "infrastructure"},
    }
    
    for _, module := range structure.Modules {
        dirs := []string{
            filepath.Join("internal", module),
            filepath.Join("pkg", module),
        }
        
        for _, dir := range dirs {
            if err := os.MkdirAll(dir, 0755); err != nil {
                return err
            }
            
            // Create README
            readme := fmt.Sprintf("# %s\n\nThis module contains %s layer code.\n", 
                module, module)
            if err := os.WriteFile(
                filepath.Join(dir, "README.md"), 
                []byte(readme), 
                0644,
            ); err != nil {
                return err
            }
        }
    }
    
    return nil
}
```

### 4. Refactoring Support

#### Automated Refactoring Tools

**Purpose**: Support safe refactoring of architectural elements.

**Example** (TypeScript with ts-morph):
```typescript
// tools/refactor-dependency.ts
import { Project } from 'ts-morph';

async function refactorDependency(
  fromModule: string,
  toModule: string,
  oldImport: string,
  newImport: string
) {
  const project = new Project({
    tsConfigFilePath: 'tsconfig.json',
  });
  
  const files = project.getSourceFiles()
    .filter(f => f.getFilePath().includes(fromModule));
  
  files.forEach(file => {
    const imports = file.getImportDeclarations();
    imports.forEach(imp => {
      const importPath = imp.getModuleSpecifierValue();
      if (importPath === oldImport) {
        imp.setModuleSpecifier(newImport);
      }
    });
    
    file.saveSync();
  });
  
  await project.save();
}

// Usage
refactorDependency(
  'src/domain',
  'src/domain',
  '../infrastructure/database',
  '../infrastructure/repositories'
);
```

---

## 🔄 CI/CD Integration

### Pre-commit Hooks

**Purpose**: Catch architectural violations before code is committed.

**Example** (Git hooks):
```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running architectural checks..."

# Run dependency analysis
npm run check:dependencies || exit 1

# Run layer checks
npm run check:layers || exit 1

# Run complexity checks
npm run check:complexity || exit 1

echo "✅ All architectural checks passed"
```

### CI Pipeline Integration

**Purpose**: Validate architecture in CI pipeline.

**Example** (GitHub Actions):
```yaml
# .github/workflows/architecture-checks.yml
name: Architecture Checks

on: [push, pull_request]

jobs:
  architectural-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Check dependencies
        run: npm run check:dependencies
      
      - name: Check layer violations
        run: npm run check:layers
      
      - name: Run architecture tests
        run: npm run test:architecture
      
      - name: Check complexity
        run: npm run check:complexity
      
      - name: Generate dependency graph
        run: npm run analyze:dependencies
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dependency-graph
          path: docs/dependency-graph.svg
```

### Continuous Monitoring

**Purpose**: Monitor architectural metrics over time.

**Example** (Metrics collection script):
```typescript
// scripts/collect-metrics.ts
import { ArchitectureMetricsCollector } from './metrics/collector';

async function collectAndReport() {
  const collector = new ArchitectureMetricsCollector();
  const metrics = await collector.collectAll();
  
  // Save metrics to file
  const fs = require('fs');
  fs.writeFileSync(
    'metrics/latest.json',
    JSON.stringify(metrics, null, 2)
  );
  
  // Compare with previous metrics
  const previous = JSON.parse(
    fs.readFileSync('metrics/previous.json', 'utf-8')
  );
  
  // Generate report
  const report = generateReport(metrics, previous);
  console.log(report);
  
  // Update previous metrics
  fs.copyFileSync('metrics/latest.json', 'metrics/previous.json');
}

collectAndReport();
```

---

## 🎯 Best Practices

### Start Small

✅ **DO**:
- Begin with high-impact, easy-to-automate checks
- Add more automation gradually
- Focus on critical architectural constraints

❌ **DON'T**:
- Try to automate everything at once
- Automate subjective decisions
- Ignore false positives

### Keep Automation Maintainable

- Write clear, readable automation code
- Document what each check does
- Make it easy to update rules
- Handle edge cases gracefully

### Provide Clear Feedback

- Show exactly what violated rules
- Provide suggestions for fixes
- Link to documentation
- Make errors actionable

### Review and Update

- Review automation rules regularly
- Update as architecture evolves
- Remove obsolete checks
- Improve based on feedback

---

## 🛠️ Tool Recommendations

### TypeScript/JavaScript

- **madge**: Dependency analysis
- **dependency-cruiser**: Advanced dependency analysis
- **ts-morph**: TypeScript AST manipulation
- **Plop**: Code generation
- **ESLint**: Custom architectural rules

### Go

- **golangci-lint**: Comprehensive linting
- **go mod graph**: Dependency analysis
- **go-tools**: Static analysis
- **gocyclo**: Complexity analysis

### Python

- **pydeps**: Dependency analysis
- **radon**: Complexity analysis
- **mypy**: Type checking
- **pylint/flake8**: Code quality

### General

- **ArchiUnit** (Java): Architecture unit testing
- **Structure101**: Architecture analysis
- **SonarQube**: Code quality and architecture
- **CodeClimate**: Automated code review

---

**Last Updated**: 2025-01-20  
**Version**: 1.0  
**Maintainer**: Skynet Documentation Team

---

**Related Documents**:
- [Evolutionary Architecture Guide](./README.md)
- [Guidelines Template](../../templates/evolutionary-architecture/guidelines-template.md)
- [Metrics Definition](./metrics-definition.md)

**Versão em Português**: [Estratégias de Automação (PT-BR)](./pt-br/automation-strategies.md)

