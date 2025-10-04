# Violações de Invariância no Princípio da Substituição de Liskov

## Informações Básicas
- **ID do Documento**: LSP-004
- **Nome**: Violações de Invariância no LSP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

As violações de invariância no Princípio da Substituição de Liskov ocorrem quando uma subclasse altera regras de negócio fundamentais (invariantes) estabelecidas pela classe base, causando comportamentos inconsistentes e quebrando a substituibilidade.

## O que são Invariantes

### Definição
Invariantes são **propriedades que devem ser mantidas durante toda a vida do objeto**. Elas definem:
- **Regras de negócio fundamentais**: Condições que nunca devem ser violadas
- **Estado consistente**: Propriedades que devem permanecer verdadeiras
- **Comportamento previsível**: Garantias que o objeto deve cumprir

### Características
- **Imutáveis**: Não podem ser alteradas por subclasses
- **Fundamentais**: Representam a essência do objeto
- **Críticas**: Violá-las quebra a lógica de negócio

## Exemplo Prático: Sistema Bancário com Cheque Especial

### Cenário
Um sistema bancário onde contas não podem ter saldo negativo, mas contas correntes podem ter cheque especial.

### Classe Base
```typescript
class BankAccount {
  protected balance: number = 0;
  
  /**
   * Saca um valor da conta
   * @param amount Valor a ser sacado
   * @throws Error se o valor for maior que o saldo disponível
   */
  withdraw(amount: number): void {
    // Pré-condição: valor deve ser positivo
    if (amount <= 0) {
      throw new Error('Valor do saque deve ser positivo');
    }
    
    // ❌ INVARIANTE: Conta não pode ficar com saldo negativo
    if (amount > this.balance) {
      throw new Error('Saldo insuficiente');
    }
    
    this.balance -= amount;
  }
  
  getBalance(): number {
    return this.balance;
  }
}
```

### Implementação Problemática (Violando LSP)

#### Conta Corrente com Cheque Especial
```typescript
class CheckingAccount extends BankAccount {
  private overdraftLimit: number = 1000; // Limite do cheque especial
  
  withdraw(amount: number): void {
    // Pré-condição: valor deve ser positivo
    if (amount <= 0) {
      throw new Error('Valor do saque deve ser positivo');
    }
    
    // ❌ VIOLAÇÃO: Permite saldo negativo (quebra invariante)
    const availableBalance = this.balance + this.overdraftLimit;
    
    if (amount > availableBalance) {
      throw new Error('Saldo insuficiente e limite do cheque especial excedido');
    }
    
    this.balance -= amount; // ❌ Pode resultar em saldo negativo
  }
  
  getAvailableBalance(): number {
    return this.balance + this.overdraftLimit;
  }
}
```

## O Problema da Violação

### Código Cliente Afetado
```typescript
class BankingService {
  processWithdrawal(account: BankAccount, amount: number) {
    try {
      account.withdraw(amount);
      console.log(`Saque de R$ ${amount} realizado com sucesso`);
    } catch (error) {
      console.error('Erro no saque:', error.message);
    }
  }
  
  checkAccountStatus(account: BankAccount) {
    const balance = account.getBalance();
    
    // ❌ Este código assume que saldo negativo é impossível
    if (balance < 0) {
      console.error('ERRO: Conta com saldo negativo!');
      // Lógica de emergência para saldo negativo
    }
  }
}
```

### Cenário de Falha
```typescript
// ✅ Funciona com conta genérica
const genericAccount = new BankAccount();
genericAccount.deposit(100);
genericAccount.withdraw(50); // Saldo: 50
genericAccount.withdraw(60); // ❌ Erro: Saldo insuficiente

// ❌ Comportamento inesperado com conta corrente
const checkingAccount = new CheckingAccount();
checkingAccount.deposit(100);
checkingAccount.withdraw(50); // Saldo: 50
checkingAccount.withdraw(60); // ✅ Permite (saldo: -10)
// ❌ Quebra a invariante: saldo negativo é permitido
```

### Consequências da Violação

#### 1. Quebra de Invariantes Fundamentais
- **Regras de negócio violadas**: Saldo negativo não deveria ser possível
- **Comportamento inconsistente**: Diferentes tipos de conta se comportam diferentemente
- **Lógica de negócio quebrada**: Código cliente não pode confiar nas regras

#### 2. Violação dos Princípios SOLID
- **SRP**: Classe cliente tem responsabilidade de gerenciar diferentes comportamentos
- **OCP**: Não pode ser estendida sem modificar lógica existente
- **LSP**: Substituições não funcionam
- **ISP**: Interface não reflete a realidade do domínio
- **DIP**: Depende de implementações específicas

#### 3. Código Frágil e Inconsistente
```typescript
// ❌ Código cliente precisa gerenciar diferentes comportamentos
class BankingService {
  processWithdrawal(account: BankAccount, amount: number) {
    if (account instanceof CheckingAccount) {
      // Lógica específica para conta corrente
      const availableBalance = account.getAvailableBalance();
      if (amount > availableBalance) {
        throw new Error('Limite excedido');
      }
    } else {
      // Lógica para outras contas
      if (amount > account.getBalance()) {
        throw new Error('Saldo insuficiente');
      }
    }
    
    account.withdraw(amount);
  }
}
```

## Soluções para Violações de Invariância

### Solução 1: Hierarquia Correta de Herança

#### Análise do Problema
O problema não é a implementação, mas a **hierarquia de herança incorreta**.

```typescript
// ❌ Hierarquia incorreta
BankAccount (não pode ter saldo negativo)
└── CheckingAccount (pode ter saldo negativo) // ❌ Violação de invariante
```

#### Hierarquia Correta
```typescript
// ✅ Hierarquia correta
Account (interface genérica)
├── BasicAccount (não pode ter saldo negativo)
└── CheckingAccount (pode ter saldo negativo) // ✅ Tipo específico
```

#### Implementação Corrigida
```typescript
// Interface base genérica
interface Account {
  withdraw(amount: number): void;
  getBalance(): number;
}

// Conta básica (sem cheque especial)
class BasicAccount implements Account {
  protected balance: number = 0;
  
  withdraw(amount: number): void {
    if (amount <= 0) {
      throw new Error('Valor do saque deve ser positivo');
    }
    
    if (amount > this.balance) {
      throw new Error('Saldo insuficiente');
    }
    
    this.balance -= amount;
  }
  
  getBalance(): number {
    return this.balance;
  }
}

// Conta corrente (com cheque especial)
class CheckingAccount implements Account {
  private balance: number = 0;
  private overdraftLimit: number = 1000;
  
  withdraw(amount: number): void {
    if (amount <= 0) {
      throw new Error('Valor do saque deve ser positivo');
    }
    
    const availableBalance = this.balance + this.overdraftLimit;
    if (amount > availableBalance) {
      throw new Error('Saldo insuficiente e limite do cheque especial excedido');
    }
    
    this.balance -= amount;
  }
  
  getBalance(): number {
    return this.balance;
  }
  
  getAvailableBalance(): number {
    return this.balance + this.overdraftLimit;
  }
}
```

### Solução 2: Composição com Delegation

#### Conta com Cheque Especial
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

### Solução 3: Strategy Pattern

#### Estratégias de Saque
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
```

## Padrões para Evitar Violações

### 1. Design por Contrato
```typescript
interface Account {
  /**
   * Saca um valor da conta
   * @param amount Valor a ser sacado
   * @pre amount > 0 (valor deve ser positivo)
   * @post balance = old.balance - amount
   * @invariant balance >= 0 (saldo nunca pode ser negativo)
   * @throws Error se amount <= 0 ou se saldo for insuficiente
   */
  withdraw(amount: number): void;
}
```

### 2. Testes de Invariantes
```typescript
describe('Account Invariants', () => {
  const accounts = [
    new BasicAccount(),
    new CheckingAccount() // ❌ Falhará se violar invariantes
  ];
  
  accounts.forEach(account => {
    it('should maintain non-negative balance', () => {
      // ✅ Todas devem manter saldo não-negativo
      account.deposit(100);
      account.withdraw(50);
      expect(account.getBalance()).toBeGreaterThanOrEqual(0);
    });
    
    it('should not allow overdraft', () => {
      // ✅ Todas devem impedir saque maior que saldo
      account.deposit(100);
      expect(() => account.withdraw(150)).toThrow();
    });
  });
});
```

### 3. Validação de Invariantes
```typescript
class InvariantValidator {
  validateAccount(account: Account): boolean {
    const balance = account.getBalance();
    
    // Invariante: saldo não pode ser negativo
    if (balance < 0) {
      return false;
    }
    
    return true;
  }
  
  validateWithdrawal(account: Account, amount: number): boolean {
    if (amount <= 0) return false;
    
    const balance = account.getBalance();
    return amount <= balance;
  }
}
```

## Detecção de Violações

### 1. Análise de Invariantes
```typescript
// ❌ Sinais de violação
class SubClass extends SuperClass {
  method(): void {
    // Altera regras fundamentais da superclasse
    this.balance -= amount; // Pode resultar em saldo negativo
  }
}
```

### 2. Testes de Substituição
```typescript
// ✅ Teste que deve passar para todas as implementações
function testInvariant(account: Account) {
  account.deposit(100);
  account.withdraw(50);
  
  // Invariante: saldo nunca pode ser negativo
  expect(account.getBalance()).toBeGreaterThanOrEqual(0);
}
```

### 3. Métricas de Consistência
- **Inconsistência**: Diferentes comportamentos para mesma operação
- **Fragilidade**: Mudanças quebram regras de negócio
- **Acoplamento**: Código cliente precisa gerenciar diferenças

## Boas Práticas

### 1. Análise de Domínio
- **Identifique invariantes**: Quais regras são fundamentais?
- **Separe responsabilidades**: Diferentes tipos = diferentes classes
- **Use composição**: Quando herança não for apropriada

### 2. Design de Hierarquias
```typescript
// ✅ Hierarquia baseada em comportamento
interface Account {
  withdraw(amount: number): void;
  getBalance(): number;
}

// ✅ Implementações específicas
class BasicAccount implements Account { /* sem cheque especial */ }
class CheckingAccount implements Account { /* com cheque especial */ }
```

### 3. Validação Contínua
```typescript
// ✅ Validação de invariantes em tempo de execução
class Account {
  private validateInvariants(): void {
    if (this.balance < 0) {
      throw new Error('Invariante violada: saldo negativo');
    }
  }
  
  withdraw(amount: number): void {
    // Lógica de saque
    this.balance -= amount;
    
    // Validação pós-operação
    this.validateInvariants();
  }
}
```

## Conclusão

As violações de invariância são as mais perigosas, pois quebram **regras de negócio fundamentais**. A solução é **redesenhar a hierarquia** para refletir a realidade do domínio.

### Pontos-Chave
- **Invariantes**: Regras fundamentais que nunca podem ser violadas
- **Hierarquia correta**: Baseada em comportamento, não em aparência
- **Composição**: Use quando herança não for apropriada
- **Validação**: Monitore invariantes em tempo de execução

### Próximos Passos
- [Aplicar boas práticas](./liskov-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
