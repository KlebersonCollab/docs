# Violações de Pré-condições no Princípio da Substituição de Liskov

## Informações Básicas
- **ID do Documento**: LSP-003
- **Nome**: Violações de Pré-condições no LSP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

As violações de pré-condições no Princípio da Substituição de Liskov ocorrem quando uma subclasse endurece (torna mais restritivas) as condições necessárias para executar um método, impedindo que o código cliente use a subclasse onde usava a superclasse.

## O que são Pré-condições

### Definição
Pré-condições são condições que devem ser verdadeiras **antes** da execução de um método. Elas definem:
- **Validações de entrada**: Parâmetros que devem ser válidos
- **Estado do objeto**: Condições que o objeto deve atender
- **Recursos necessários**: Dependências que devem estar disponíveis

### Características
- **Não podem ser endurecidas**: Subclasses não podem exigir mais que a superclasse
- **Podem ser relaxadas**: Subclasses podem aceitar menos restrições
- **Devem ser consistentes**: Comportamento previsível em toda a hierarquia

## Exemplo Prático: Sistema Bancário

### Cenário
Um sistema bancário com diferentes tipos de contas, onde cada tipo tem regras específicas de depósito.

### Classe Base
```typescript
class BankAccount {
  protected balance: number = 0;
  
  /**
   * Deposita um valor na conta
   * @param amount Valor a ser depositado (deve ser positivo)
   * @throws Error se o valor for negativo ou zero
   */
  deposit(amount: number): void {
    // Pré-condição: valor deve ser positivo
    if (amount <= 0) {
      throw new Error('Valor do depósito deve ser positivo');
    }
    
    this.balance += amount;
  }
  
  getBalance(): number {
    return this.balance;
  }
}
```

### Implementação Correta (Respeitando LSP)

#### Conta Corrente
```typescript
class CheckingAccount extends BankAccount {
  deposit(amount: number): void {
    // ✅ Mantém a mesma pré-condição da superclasse
    if (amount <= 0) {
      throw new Error('Valor do depósito deve ser positivo');
    }
    
    this.balance += amount;
  }
}
```

### Implementação Problemática (Violando LSP)

#### Conta Poupança
```typescript
class SavingsAccount extends BankAccount {
  private readonly MINIMUM_DEPOSIT = 10;
  
  deposit(amount: number): void {
    // ❌ VIOLAÇÃO: Endureceu a pré-condição
    if (amount <= 0) {
      throw new Error('Valor do depósito deve ser positivo');
    }
    
    // ❌ VIOLAÇÃO: Adicionou nova restrição
    if (amount < this.MINIMUM_DEPOSIT) {
      throw new Error('Depósito mínimo é de R$ 10 para conta poupança');
    }
    
    this.balance += amount;
  }
}
```

## O Problema da Violação

### Código Cliente Afetado
```typescript
class BankingService {
  processDeposit(account: BankAccount, amount: number) {
    try {
      // Este código funcionava com BankAccount
      account.deposit(amount);
      console.log(`Depósito de R$ ${amount} realizado com sucesso`);
    } catch (error) {
      console.error('Erro no depósito:', error.message);
    }
  }
}
```

### Cenário de Falha
```typescript
// ✅ Funciona com conta genérica
const genericAccount = new BankAccount();
bankingService.processDeposit(genericAccount, 5); // Sucesso

// ❌ Falha com conta poupança (mesmo valor)
const savingsAccount = new SavingsAccount();
bankingService.processDeposit(savingsAccount, 5); // Erro: Depósito mínimo é de R$ 10
```

### Consequências da Violação

#### 1. Quebra de Substituibilidade
- **Código cliente quebrado**: Não consegue substituir superclasse por subclasse
- **Comportamento inesperado**: Mesmo valor funciona em uma classe, falha em outra
- **Perda de polimorfismo**: Código cliente precisa conhecer tipos específicos

#### 2. Violação dos Princípios SOLID
- **SRP**: Classe cliente tem responsabilidade de conhecer implementações
- **OCP**: Não pode ser estendida sem modificação
- **LSP**: Substituições não funcionam
- **ISP**: Interface não está bem definida
- **DIP**: Depende de implementações concretas

#### 3. Código Frágil
```typescript
// ❌ Código cliente precisa de verificações específicas
class BankingService {
  processDeposit(account: BankAccount, amount: number) {
    // ❌ Precisa conhecer implementações específicas
    if (account instanceof SavingsAccount && amount < 10) {
      throw new Error('Valor insuficiente para conta poupança');
    }
    
    account.deposit(amount);
  }
}
```

## Soluções para Violações de Pré-condições

### Solução 1: Hierarquia Correta de Herança

#### Análise do Problema
O problema não é a implementação, mas a **hierarquia de herança incorreta**.

```typescript
// ❌ Hierarquia incorreta
BankAccount (genérica)
├── CheckingAccount (conta corrente)
└── SavingsAccount (conta poupança) // ❌ Não é uma conta genérica
```

#### Hierarquia Correta
```typescript
// ✅ Hierarquia correta
Account (interface genérica)
├── BasicAccount (conta básica)
├── CheckingAccount (conta corrente)
└── SavingsAccount (conta poupança) // ✅ Tipo específico
```

#### Implementação Corrigida
```typescript
// Interface base mais genérica
interface Account {
  deposit(amount: number): void;
  getBalance(): number;
}

// Conta básica (sem restrições especiais)
class BasicAccount implements Account {
  protected balance: number = 0;
  
  deposit(amount: number): void {
    if (amount <= 0) {
      throw new Error('Valor do depósito deve ser positivo');
    }
    this.balance += amount;
  }
  
  getBalance(): number {
    return this.balance;
  }
}

// Conta poupança (tipo específico)
class SavingsAccount implements Account {
  private balance: number = 0;
  private readonly MINIMUM_DEPOSIT = 10;
  
  deposit(amount: number): void {
    if (amount <= 0) {
      throw new Error('Valor do depósito deve ser positivo');
    }
    if (amount < this.MINIMUM_DEPOSIT) {
      throw new Error('Depósito mínimo é de R$ 10 para conta poupança');
    }
    this.balance += amount;
  }
  
  getBalance(): number {
    return this.balance;
  }
}
```

### Solução 2: Validação Prévia

#### Validador de Contas
```typescript
class AccountValidator {
  canDeposit(account: Account, amount: number): boolean {
    if (amount <= 0) return false;
    
    // Validações específicas por tipo
    if (account instanceof SavingsAccount) {
      return amount >= 10;
    }
    
    return true;
  }
}
```

#### Serviço com Validação
```typescript
class BankingService {
  private validator = new AccountValidator();
  
  processDeposit(account: Account, amount: number) {
    if (!this.validator.canDeposit(account, amount)) {
      throw new Error('Depósito não permitido para este tipo de conta');
    }
    
    account.deposit(amount);
  }
}
```

### Solução 3: Factory Pattern

#### Factory de Contas
```typescript
class AccountFactory {
  createAccount(type: 'basic' | 'checking' | 'savings'): Account {
    switch (type) {
      case 'basic':
        return new BasicAccount();
      case 'checking':
        return new CheckingAccount();
      case 'savings':
        return new SavingsAccount();
      default:
        throw new Error('Tipo de conta não suportado');
    }
  }
}
```

#### Serviço Especializado
```typescript
class BankingService {
  private factory = new AccountFactory();
  
  createAccount(type: 'basic' | 'checking' | 'savings'): Account {
    return this.factory.createAccount(type);
  }
  
  processDeposit(account: Account, amount: number) {
    // Validação baseada no tipo de conta
    this.validateDeposit(account, amount);
    account.deposit(amount);
  }
  
  private validateDeposit(account: Account, amount: number) {
    if (account instanceof SavingsAccount && amount < 10) {
      throw new Error('Depósito mínimo é de R$ 10 para conta poupança');
    }
  }
}
```

## Padrões para Evitar Violações

### 1. Design por Contrato
```typescript
interface Account {
  /**
   * Deposita um valor na conta
   * @param amount Valor a ser depositado
   * @pre amount > 0 (valor deve ser positivo)
   * @post balance = old.balance + amount
   * @throws Error se amount <= 0
   */
  deposit(amount: number): void;
}
```

### 2. Testes de Substituição
```typescript
describe('Account Substitution', () => {
  const accounts = [
    new BasicAccount(),
    new CheckingAccount(),
    new SavingsAccount() // ❌ Falhará se violar pré-condições
  ];
  
  accounts.forEach(account => {
    it('should accept positive amounts', () => {
      // ✅ Todas devem aceitar valores positivos
      expect(() => account.deposit(1)).not.toThrow();
    });
    
    it('should reject negative amounts', () => {
      // ✅ Todas devem rejeitar valores negativos
      expect(() => account.deposit(-1)).toThrow();
    });
  });
});
```

### 3. Validação de Pré-condições
```typescript
class PreConditionValidator {
  validateDeposit(account: Account, amount: number): void {
    if (amount <= 0) {
      throw new Error('Valor deve ser positivo');
    }
    
    // Validações específicas por tipo
    if (account instanceof SavingsAccount && amount < 10) {
      throw new Error('Depósito mínimo é de R$ 10 para conta poupança');
    }
  }
}
```

## Detecção de Violações

### 1. Análise de Hierarquia
```typescript
// ❌ Sinais de violação
class SubClass extends SuperClass {
  method(param: Type): ReturnType {
    // Verificações adicionais que não existiam na superclasse
    if (additionalCondition) {
      throw new Error('Nova restrição');
    }
    
    super.method(param);
  }
}
```

### 2. Testes de Substituição
```typescript
// ✅ Teste que deve passar para todas as implementações
function testSubstitution(account: Account) {
  // Deve funcionar com qualquer implementação
  account.deposit(1);
  expect(account.getBalance()).toBeGreaterThan(0);
}
```

### 3. Métricas de Acoplamento
- **Alto acoplamento**: Muitas verificações `instanceof`
- **Baixa coesão**: Lógica específica espalhada
- **Fragilidade**: Mudanças quebram código cliente

## Boas Práticas

### 1. Análise de Herança
- **Pergunta-chave**: "É um" vs "Tem um"
- **SavingsAccount é um BankAccount?** ❌ Não, é um tipo específico
- **SavingsAccount tem um BankAccount?** ✅ Sim, pode usar composição

### 2. Composição vs Herança
```typescript
// ✅ Composição ao invés de herança
class SavingsAccount {
  private account: BankAccount;
  private readonly MINIMUM_DEPOSIT = 10;
  
  deposit(amount: number): void {
    if (amount < this.MINIMUM_DEPOSIT) {
      throw new Error('Depósito mínimo é de R$ 10');
    }
    
    this.account.deposit(amount);
  }
}
```

### 3. Interfaces Específicas
```typescript
interface SavingsAccount {
  deposit(amount: number): void; // Com restrições específicas
  getBalance(): number;
}

interface BasicAccount {
  deposit(amount: number): void; // Sem restrições especiais
  getBalance(): number;
}
```

## Conclusão

As violações de pré-condições são frequentemente causadas por **hierarquias de herança incorretas**. A solução não é ajustar o código, mas **redesenhar a hierarquia** para refletir a realidade do domínio.

### Pontos-Chave
- **Herança correta**: "É um" deve ser verdadeiro
- **Pré-condições**: Não podem ser endurecidas em subclasses
- **Substituibilidade**: Código cliente deve funcionar com qualquer implementação
- **Composição**: Use quando herança não for apropriada

### Próximos Passos
- [Estudar violações de invariância](./liskov-invariants.md)
- [Aplicar boas práticas](./liskov-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
