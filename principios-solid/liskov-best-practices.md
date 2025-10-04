# Guia de Boas Práticas para o Princípio da Substituição de Liskov

## Informações Básicas
- **ID do Documento**: LSP-005
- **Nome**: Boas Práticas para LSP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

Este guia apresenta as melhores práticas para implementar o Princípio da Substituição de Liskov (LSP) corretamente, evitando violações comuns e criando sistemas mais robustos e maintíveis.

## 1. Design de Hierarquias Corretas

### 1.1. Análise de Relacionamentos

#### Pergunta-Chave: "É um" vs "Tem um"
```typescript
// ❌ Relacionamento incorreto
class SavingsAccount extends BankAccount {
  // SavingsAccount NÃO é um BankAccount genérico
  // É um tipo específico com regras próprias
}

// ✅ Relacionamento correto
class SavingsAccount implements Account {
  // SavingsAccount É um Account (interface genérica)
  // Implementa comportamento específico
}
```

#### Teste de Substituição
```typescript
// ✅ Teste que deve passar
function testSubstitution(account: Account) {
  // Deve funcionar com qualquer implementação
  account.deposit(100);
  account.withdraw(50);
  expect(account.getBalance()).toBe(50);
}
```

### 1.2. Hierarquias Baseadas em Comportamento

#### Estrutura Correta
```typescript
// ✅ Hierarquia baseada em comportamento
interface Account {
  deposit(amount: number): void;
  withdraw(amount: number): void;
  getBalance(): number;
}

// ✅ Implementações específicas
class BasicAccount implements Account {
  // Comportamento básico sem restrições especiais
}

class SavingsAccount implements Account {
  // Comportamento específico com restrições
}

class CheckingAccount implements Account {
  // Comportamento específico com cheque especial
}
```

## 2. Design por Contrato

### 2.1. Documentação Clara de Contratos

#### Interface Bem Documentada
```typescript
interface ReportGenerator {
  /**
   * Gera um relatório e retorna o caminho para acessá-lo
   * @param data Dados para gerar o relatório
   * @returns Caminho local do arquivo gerado
   * @pre data não pode ser null ou vazio
   * @post arquivo deve existir no sistema de arquivos
   * @throws Error se não conseguir gerar o relatório
   */
  generate(data: ReportData): string;
}
```

#### Implementação que Respeita o Contrato
```typescript
class CsvReportGenerator implements ReportGenerator {
  generate(data: ReportData): string {
    // ✅ Respeita pré-condições
    if (!data || data.length === 0) {
      throw new Error('Dados não podem ser vazios');
    }
    
    // ✅ Gera arquivo local
    const filePath = this.createLocalFile(data);
    
    // ✅ Respeita pós-condições
    if (!this.fileExists(filePath)) {
      throw new Error('Arquivo não foi criado');
    }
    
    return filePath;
  }
}
```

### 2.2. Validação de Contratos

#### Validador de Contratos
```typescript
class ContractValidator {
  validateReportGenerator(generator: ReportGenerator, data: ReportData): boolean {
    try {
      // Testa pré-condições
      if (!data || data.length === 0) {
        return false;
      }
      
      // Testa execução
      const result = generator.generate(data);
      
      // Testa pós-condições
      return typeof result === 'string' && result.length > 0;
    } catch (error) {
      return false;
    }
  }
}
```

## 3. Testes de Substituição

### 3.1. Testes Automatizados

#### Teste de Substituição Genérico
```typescript
describe('Account Substitution Tests', () => {
  const accountTypes = [
    () => new BasicAccount(),
    () => new SavingsAccount(),
    () => new CheckingAccount()
  ];
  
  accountTypes.forEach((createAccount, index) => {
    describe(`Account Type ${index + 1}`, () => {
      let account: Account;
      
      beforeEach(() => {
        account = createAccount();
      });
      
      it('should allow positive deposits', () => {
        expect(() => account.deposit(100)).not.toThrow();
        expect(account.getBalance()).toBe(100);
      });
      
      it('should reject negative deposits', () => {
        expect(() => account.deposit(-10)).toThrow();
      });
      
      it('should allow valid withdrawals', () => {
        account.deposit(100);
        expect(() => account.withdraw(50)).not.toThrow();
        expect(account.getBalance()).toBe(50);
      });
      
      it('should maintain balance consistency', () => {
        account.deposit(100);
        account.withdraw(30);
        account.deposit(20);
        expect(account.getBalance()).toBe(90);
      });
    });
  });
});
```

### 3.2. Property-Based Testing

#### Teste de Propriedades
```typescript
import { property, forAll, integer, boolean } from 'fast-check';

describe('Account Properties', () => {
  it('should maintain balance consistency', () => {
    forAll(integer(0, 1000), integer(0, 1000), (initialBalance, amount) => {
      const account = new BasicAccount();
      account.deposit(initialBalance);
      
      if (amount <= initialBalance) {
        account.withdraw(amount);
        expect(account.getBalance()).toBe(initialBalance - amount);
      } else {
        expect(() => account.withdraw(amount)).toThrow();
      }
    });
  });
});
```

## 4. Padrões de Design Apropriados

### 4.1. Strategy Pattern

#### Estratégias de Comportamento
```typescript
interface WithdrawalStrategy {
  canWithdraw(balance: number, amount: number): boolean;
  getAvailableBalance(balance: number): number;
}

class BasicWithdrawalStrategy implements WithdrawalStrategy {
  canWithdraw(balance: number, amount: number): boolean {
    return amount <= balance;
  }
  
  getAvailableBalance(balance: number): number {
    return balance;
  }
}

class OverdraftWithdrawalStrategy implements WithdrawalStrategy {
  constructor(private overdraftLimit: number) {}
  
  canWithdraw(balance: number, amount: number): boolean {
    return amount <= (balance + this.overdraftLimit);
  }
  
  getAvailableBalance(balance: number): number {
    return balance + this.overdraftLimit;
  }
}
```

#### Conta com Estratégia
```typescript
class Account {
  protected balance: number = 0;
  private withdrawalStrategy: WithdrawalStrategy;
  
  constructor(withdrawalStrategy: WithdrawalStrategy) {
    this.withdrawalStrategy = withdrawalStrategy;
  }
  
  withdraw(amount: number): void {
    if (amount <= 0) {
      throw new Error('Valor do saque deve ser positivo');
    }
    
    if (!this.withdrawalStrategy.canWithdraw(this.balance, amount)) {
      throw new Error('Saldo insuficiente');
    }
    
    this.balance -= amount;
  }
  
  getBalance(): number {
    return this.balance;
  }
  
  getAvailableBalance(): number {
    return this.withdrawalStrategy.getAvailableBalance(this.balance);
  }
}
```

### 4.2. Composition over Inheritance

#### Composição com Delegation
```typescript
class CheckingAccount {
  private basicAccount: BasicAccount;
  private overdraftLimit: number = 1000;
  
  constructor() {
    this.basicAccount = new BasicAccount();
  }
  
  withdraw(amount: number): void {
    if (amount <= 0) {
      throw new Error('Valor do saque deve ser positivo');
    }
    
    const availableBalance = this.basicAccount.getBalance() + this.overdraftLimit;
    if (amount > availableBalance) {
      throw new Error('Saldo insuficiente e limite do cheque especial excedido');
    }
    
    // Delega para a conta básica
    this.basicAccount.withdraw(amount);
  }
  
  getBalance(): number {
    return this.basicAccount.getBalance();
  }
  
  getAvailableBalance(): number {
    return this.basicAccount.getBalance() + this.overdraftLimit;
  }
}
```

## 5. Detecção e Prevenção de Violações

### 5.1. Análise Estática

#### Regras de Lint
```typescript
// ❌ Padrões que indicam violação
if (obj instanceof SpecificClass) {
  // Lógica específica
}

// ❌ Verificações de tipo em código cliente
if (obj.constructor.name === 'SpecificClass') {
  // Lógica específica
}
```

#### Configuração de ESLint
```json
{
  "rules": {
    "no-instanceof": "error",
    "no-constructor-name": "error",
    "prefer-interface-over-type": "error"
  }
}
```

### 5.2. Métricas de Qualidade

#### Métricas de Acoplamento
```typescript
class CouplingAnalyzer {
  analyzeClass(className: string): CouplingMetrics {
    return {
      instanceofChecks: this.countInstanceOfChecks(className),
      typeChecks: this.countTypeChecks(className),
      couplingScore: this.calculateCouplingScore(className)
    };
  }
  
  private countInstanceOfChecks(className: string): number {
    // Conta verificações instanceof
    return this.sourceCode.match(/instanceof/g)?.length || 0;
  }
}
```

### 5.3. Testes de Integração

#### Teste de Substituição em Produção
```typescript
describe('Production Substitution Tests', () => {
  it('should work with any report generator', () => {
    const generators = [
      new CsvReportGenerator(),
      new PdfReportGenerator(),
      new S3ReportGenerator()
    ];
    
    generators.forEach(generator => {
      const processor = new ReportProcessor();
      
      // Deve funcionar com qualquer gerador
      expect(() => processor.processReport(generator)).not.toThrow();
    });
  });
});
```

## 6. Refatoração de Código Problemático

### 6.1. Identificação de Violações

#### Sinais de Violação
```typescript
// ❌ Código que indica violação
class ReportProcessor {
  processReport(generator: ReportGenerator) {
    const result = generator.generate();
    
    // ❌ Verificação específica de implementação
    if (generator instanceof S3ReportGenerator) {
      // Lógica específica para S3
      this.downloadFromS3(result);
    } else {
      // Lógica para arquivos locais
      this.processLocalFile(result);
    }
  }
}
```

### 6.2. Refatoração Passo a Passo

#### Passo 1: Identificar o Problema
```typescript
// Identificar que S3ReportGenerator retorna URL, não caminho local
class S3ReportGenerator implements ReportGenerator {
  generate(): string {
    // ❌ Retorna URL, não caminho local
    return this.uploadToS3();
  }
}
```

#### Passo 2: Segregar Interfaces
```typescript
// ✅ Interfaces segregadas
interface LocalReportGenerator {
  generate(): string; // Caminho local
}

interface CloudReportGenerator {
  generate(): string; // URL ou identificador
}
```

#### Passo 3: Implementações Específicas
```typescript
// ✅ Implementações específicas
class CsvReportGenerator implements LocalReportGenerator {
  generate(): string {
    return this.saveLocally();
  }
}

class S3ReportGenerator implements CloudReportGenerator {
  generate(): string {
    return this.uploadToS3();
  }
}
```

#### Passo 4: Processadores Específicos
```typescript
// ✅ Processadores específicos
class LocalReportProcessor {
  processReport(generator: LocalReportGenerator) {
    const filePath = generator.generate();
    this.processLocalFile(filePath);
  }
}

class CloudReportProcessor {
  processReport(generator: CloudReportGenerator) {
    const url = generator.generate();
    this.processCloudFile(url);
  }
}
```

## 7. Monitoramento e Manutenção

### 7.1. Métricas de Qualidade

#### Dashboard de Métricas
```typescript
class LSPMetrics {
  calculateSubstitutionScore(classes: Class[]): number {
    let score = 0;
    
    classes.forEach(cls => {
      // Testa substituição com outras classes
      const substitutionTests = this.runSubstitutionTests(cls);
      score += substitutionTests.passed / substitutionTests.total;
    });
    
    return score / classes.length;
  }
  
  calculateCouplingScore(classes: Class[]): number {
    let totalCoupling = 0;
    
    classes.forEach(cls => {
      const instanceofChecks = this.countInstanceOfChecks(cls);
      const typeChecks = this.countTypeChecks(cls);
      totalCoupling += instanceofChecks + typeChecks;
    });
    
    return totalCoupling / classes.length;
  }
}
```

### 7.2. Alertas Automáticos

#### Sistema de Alertas
```typescript
class LSPAlertSystem {
  checkForViolations(codebase: Codebase): Alert[] {
    const alerts: Alert[] = [];
    
    // Verifica verificações instanceof
    const instanceofChecks = this.findInstanceOfChecks(codebase);
    if (instanceOfChecks.length > 0) {
      alerts.push({
        type: 'LSP_VIOLATION',
        message: 'Código cliente usa instanceof - possível violação do LSP',
        severity: 'HIGH',
        locations: instanceofChecks
      });
    }
    
    // Verifica testes de substituição
    const substitutionTests = this.findSubstitutionTests(codebase);
    if (substitutionTests.length === 0) {
      alerts.push({
        type: 'MISSING_TESTS',
        message: 'Faltam testes de substituição',
        severity: 'MEDIUM',
        locations: []
      });
    }
    
    return alerts;
  }
}
```

## 8. Ferramentas e Automação

### 8.1. Ferramentas de Análise

#### Análise Automática
```typescript
class LSPAnalyzer {
  analyzeCodebase(codebase: Codebase): AnalysisResult {
    return {
      violations: this.findViolations(codebase),
      suggestions: this.generateSuggestions(codebase),
      metrics: this.calculateMetrics(codebase),
      recommendations: this.generateRecommendations(codebase)
    };
  }
  
  private findViolations(codebase: Codebase): Violation[] {
    const violations: Violation[] = [];
    
    // Verifica verificações instanceof
    const instanceofChecks = this.findInstanceOfChecks(codebase);
    violations.push(...instanceOfChecks.map(check => ({
      type: 'INSTANCEOF_CHECK',
      location: check.location,
      severity: 'HIGH',
      suggestion: 'Use interfaces ou strategy pattern'
    })));
    
    return violations;
  }
}
```

### 8.2. Geração Automática de Testes

#### Gerador de Testes de Substituição
```typescript
class SubstitutionTestGenerator {
  generateTests(interfaceName: string, implementations: Class[]): TestSuite {
    const tests: Test[] = [];
    
    implementations.forEach(impl => {
      tests.push({
        name: `should substitute ${impl.name} for ${interfaceName}`,
        code: this.generateSubstitutionTest(interfaceName, impl),
        type: 'SUBSTITUTION'
      });
    });
    
    return {
      name: `${interfaceName} Substitution Tests`,
      tests: tests
    };
  }
  
  private generateSubstitutionTest(interfaceName: string, impl: Class): string {
    return `
      it('should substitute ${impl.name} for ${interfaceName}', () => {
        const instance = new ${impl.name}();
        const client = new Client();
        
        // Deve funcionar com qualquer implementação
        expect(() => client.use(${interfaceName})).not.toThrow();
      });
    `;
  }
}
```

## 9. Checklist de Implementação

### 9.1. Checklist de Design

#### ✅ Análise de Hierarquia
- [ ] Relacionamento "é um" é verdadeiro?
- [ ] Comportamento é consistente entre implementações?
- [ ] Interfaces são bem definidas?
- [ ] Contratos são claros e documentados?

#### ✅ Implementação
- [ ] Pré-condições não são endurecidas?
- [ ] Pós-condições são consistentes?
- [ ] Invariantes são mantidas?
- [ ] Substituições funcionam corretamente?

#### ✅ Testes
- [ ] Testes de substituição implementados?
- [ ] Testes de contrato implementados?
- [ ] Testes de integração funcionam?
- [ ] Cobertura de testes adequada?

### 9.2. Checklist de Manutenção

#### ✅ Monitoramento
- [ ] Métricas de acoplamento monitoradas?
- [ ] Alertas de violação configurados?
- [ ] Análise estática configurada?
- [ ] Testes de regressão funcionando?

#### ✅ Refatoração
- [ ] Violações identificadas e corrigidas?
- [ ] Hierarquias problemáticas refatoradas?
- [ ] Código cliente simplificado?
- [ ] Documentação atualizada?

## 10. Conclusão

### 10.1. Benefícios das Boas Práticas

#### Código Mais Robusto
- **Substituições seguras**: Objetos podem ser intercambiados
- **Menor acoplamento**: Código cliente independente de implementações
- **Maior confiabilidade**: Comportamento previsível

#### Facilita Manutenção
- **Extensibilidade**: Novas implementações sem quebrar código existente
- **Refatoração segura**: Mudanças isoladas em implementações
- **Testes mais simples**: Mocks e stubs funcionam corretamente

#### Melhora Qualidade
- **Código mais limpo**: Menos verificações de tipo
- **Arquitetura melhor**: Hierarquias bem desenhadas
- **Documentação clara**: Contratos bem definidos

### 10.2. Próximos Passos

#### Implementação Imediata
1. **Audite código existente**: Identifique violações do LSP
2. **Implemente testes**: Crie testes de substituição
3. **Refatore gradualmente**: Corrija violações uma por vez
4. **Configure ferramentas**: Use análise estática e métricas

#### Melhoria Contínua
1. **Monitore métricas**: Acompanhe qualidade do código
2. **Treine equipe**: Ensine princípios e práticas
3. **Automatize verificações**: Use CI/CD para validação
4. **Documente padrões**: Crie guias e exemplos

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
