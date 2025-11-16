# Unit of Work Pattern

## 📋 Informações do Documento

- **Tipo**: Padrão de Persistência
- **Categoria**: Data Source Architectural Patterns
- **Versão**: 1.0
- **Data**: 2025-11-16
- **Fonte**: Patterns of Enterprise Application Architecture - Martin Fowler

## 🎯 Visão Geral

O padrão **Unit of Work** mantém uma lista de objetos afetados por uma transação de negócio e coordena a escrita de mudanças e a resolução de problemas de concorrência. É essencial quando você precisa coordenar múltiplas operações de persistência em uma única transação.

## 📖 Definição

> "Mantém uma lista de objetos afetados por uma transação de negócio e coordena a escrita de mudanças e a resolução de problemas de concorrência."

## 🔍 Características

### Estrutura
- Mantém lista de objetos modificados
- Coordena escrita de mudanças
- Gerencia transações
- Resolve problemas de concorrência

### Responsabilidades
1. **Rastreamento de Mudanças**
   - Objetos novos (new)
   - Objetos modificados (dirty)
   - Objetos deletados (removed)

2. **Coordenação de Transações**
   - Begin transaction
   - Commit changes
   - Rollback on error

3. **Resolução de Concorrência**
   - Detecção de conflitos
   - Estratégias de resolução
   - Lock management

## 💡 Quando Usar

### ✅ Situações Ideais

1. **Múltiplas Operações Coordenadas**
   - Salvar múltiplos objetos
   - Operações relacionadas
   - Transações complexas

2. **Problemas de Concorrência**
   - Múltiplos usuários
   - Operações simultâneas
   - Necessidade de locks

3. **Consistência de Dados**
   - Operações atômicas
   - Rollback em caso de erro
   - Integridade garantida

4. **Performance**
   - Batch operations
   - Reduzir round-trips
   - Otimizar escritas

### ❌ Quando Evitar

1. **Operações Simples**
   - Uma única operação
   - Sem necessidade de coordenação
   - Overhead desnecessário

2. **Sem Problemas de Concorrência**
   - Aplicações single-user
   - Sem necessidade de transações
   - Operações independentes

## 🏗️ Estrutura de Implementação

### Exemplo Básico

```typescript
// Unit of Work
class UnitOfWork {
  private newObjects: Ticket[] = [];
  private dirtyObjects: Ticket[] = [];
  private removedObjects: Ticket[] = [];
  private repository: TicketRepository;

  constructor(repository: TicketRepository) {
    this.repository = repository;
  }

  // Registrar objeto novo
  registerNew(ticket: Ticket): void {
    if (this.dirtyObjects.includes(ticket)) {
      throw new Error('Object is already registered as dirty');
    }
    if (this.removedObjects.includes(ticket)) {
      throw new Error('Object is already registered as removed');
    }
    if (this.newObjects.includes(ticket)) {
      throw new Error('Object is already registered as new');
    }
    this.newObjects.push(ticket);
  }

  // Registrar objeto modificado
  registerDirty(ticket: Ticket): void {
    if (this.removedObjects.includes(ticket)) {
      throw new Error('Object is already registered as removed');
    }
    if (!this.dirtyObjects.includes(ticket) && !this.newObjects.includes(ticket)) {
      this.dirtyObjects.push(ticket);
    }
  }

  // Registrar objeto removido
  registerRemoved(ticket: Ticket): void {
    if (this.newObjects.includes(ticket)) {
      this.newObjects = this.newObjects.filter(t => t !== ticket);
      return;
    }
    this.dirtyObjects = this.dirtyObjects.filter(t => t !== ticket);
    if (!this.removedObjects.includes(ticket)) {
      this.removedObjects.push(ticket);
    }
  }

  // Commitar todas as mudanças
  async commit(): Promise<void> {
    const connection = await getConnection();
    
    try {
      await connection.query('BEGIN');
      
      // Inserir novos objetos
      for (const ticket of this.newObjects) {
        await this.repository.insert(ticket, connection);
      }
      
      // Atualizar objetos modificados
      for (const ticket of this.dirtyObjects) {
        await this.repository.update(ticket, connection);
      }
      
      // Deletar objetos removidos
      for (const ticket of this.removedObjects) {
        await this.repository.delete(ticket.getId(), connection);
      }
      
      await connection.query('COMMIT');
      
      // Limpar após commit bem-sucedido
      this.clear();
    } catch (error) {
      await connection.query('ROLLBACK');
      throw error;
    } finally {
      connection.release();
    }
  }

  // Limpar rastreamento
  private clear(): void {
    this.newObjects = [];
    this.dirtyObjects = [];
    this.removedObjects = [];
  }
}
```

### Uso com Repository

```typescript
// Repository com suporte a Unit of Work
interface TicketRepository {
  insert(ticket: Ticket, connection?: Pool): Promise<void>;
  update(ticket: Ticket, connection?: Pool): Promise<void>;
  delete(id: string, connection?: Pool): Promise<void>;
}

// Service usando Unit of Work
class TicketService {
  constructor(
    private ticketRepository: TicketRepository,
    private userRepository: UserRepository
  ) {}

  async createTicketWithUser(request: CreateTicketRequest): Promise<void> {
    const uow = new UnitOfWork(this.ticketRepository);
    
    // Criar usuário se não existir
    let user = await this.userRepository.findByEmail(request.userEmail);
    if (!user) {
      user = User.create(request.userEmail, request.userName);
      uow.registerNew(user);
    }
    
    // Criar ticket
    const ticket = Ticket.create(request.content, user.getId());
    uow.registerNew(ticket);
    
    // Commitar tudo de uma vez
    await uow.commit();
  }

  async assignMultipleTickets(ticketIds: string[], agentId: string): Promise<void> {
    const uow = new UnitOfWork(this.ticketRepository);
    
    for (const ticketId of ticketIds) {
      const ticket = await this.ticketRepository.findById(ticketId);
      if (ticket) {
        ticket.assign(agentId);
        uow.registerDirty(ticket);
      }
    }
    
    await uow.commit();
  }
}
```

## 🔄 Unit of Work e Active Record

### Active Record com Unit of Work
```typescript
// Active Record pode usar Unit of Work
class Ticket extends ActiveRecord {
  private static uow: UnitOfWork | null = null;

  static beginTransaction(): UnitOfWork {
    Ticket.uow = new UnitOfWork();
    return Ticket.uow;
  }

  async save(): Promise<void> {
    if (Ticket.uow) {
      // Registrar no Unit of Work ao invés de salvar imediatamente
      Ticket.uow.registerDirty(this);
    } else {
      // Salvar imediatamente se não houver Unit of Work
      await this.insertOrUpdate();
    }
  }

  static async commit(): Promise<void> {
    if (Ticket.uow) {
      await Ticket.uow.commit();
      Ticket.uow = null;
    }
  }
}

// Uso
const uow = Ticket.beginTransaction();
const ticket1 = Ticket.create('Issue 1', 'user-1');
const ticket2 = Ticket.create('Issue 2', 'user-2');
await ticket1.save(); // Registra no UoW
await ticket2.save(); // Registra no UoW
await Ticket.commit(); // Salva tudo de uma vez
```

## ⚠️ Armadilhas Comuns

### 1. Não Limpar Após Commit
❌ **Evite:**
```typescript
async commit(): Promise<void> {
  // ... salvar objetos ...
  // ❌ Não limpa os arrays
}
```

✅ **Prefira:**
```typescript
async commit(): Promise<void> {
  // ... salvar objetos ...
  this.clear(); // ✅ Limpa após commit
}
```

### 2. Registrar Objeto Duplicado
❌ **Evite:**
```typescript
registerNew(ticket: Ticket): void {
  this.newObjects.push(ticket); // ❌ Pode adicionar duplicado
}
```

✅ **Prefira:**
```typescript
registerNew(ticket: Ticket): void {
  if (this.newObjects.includes(ticket)) {
    throw new Error('Object already registered');
  }
  this.newObjects.push(ticket); // ✅ Valida antes
}
```

### 3. Não Tratar Erros
❌ **Evite:**
```typescript
async commit(): Promise<void> {
  await connection.query('BEGIN');
  // ... operações ...
  await connection.query('COMMIT');
  // ❌ Não trata erros
}
```

✅ **Prefira:**
```typescript
async commit(): Promise<void> {
  try {
    await connection.query('BEGIN');
    // ... operações ...
    await connection.query('COMMIT');
  } catch (error) {
    await connection.query('ROLLBACK'); // ✅ Rollback em caso de erro
    throw error;
  }
}
```

## 🧪 Testes com Unit of Work

### Teste de Integração
```typescript
describe('UnitOfWork - Integration Tests', () => {
  it('should commit multiple operations atomically', async () => {
    const repository = new TicketRepositoryImpl(connection);
    const uow = new UnitOfWork(repository);
    
    const ticket1 = Ticket.create('Issue 1', 'user-1');
    const ticket2 = Ticket.create('Issue 2', 'user-2');
    
    uow.registerNew(ticket1);
    uow.registerNew(ticket2);
    
    await uow.commit();
    
    // Verificar que ambos foram salvos
    const loaded1 = await repository.findById(ticket1.getId());
    const loaded2 = await repository.findById(ticket2.getId());
    
    expect(loaded1).not.toBeNull();
    expect(loaded2).not.toBeNull();
  });

  it('should rollback on error', async () => {
    const repository = new TicketRepositoryImpl(connection);
    const uow = new UnitOfWork(repository);
    
    const ticket1 = Ticket.create('Issue 1', 'user-1');
    const ticket2 = Ticket.create('Issue 2', 'invalid-user'); // Vai causar erro
    
    uow.registerNew(ticket1);
    uow.registerNew(ticket2);
    
    await expect(uow.commit()).rejects.toThrow();
    
    // Verificar que nenhum foi salvo
    const loaded1 = await repository.findById(ticket1.getId());
    expect(loaded1).toBeNull();
  });
});
```

## 📊 Vantagens e Desvantagens

### ✅ Vantagens

1. **Coordenação de Transações**
   - Múltiplas operações atômicas
   - Rollback automático
   - Consistência garantida

2. **Performance**
   - Batch operations
   - Reduz round-trips
   - Otimiza escritas

3. **Resolução de Concorrência**
   - Detecção de conflitos
   - Estratégias de resolução
   - Lock management

4. **Simplicidade**
   - Interface simples
   - Fácil de usar
   - Abstração útil

### ❌ Desvantagens

1. **Complexidade**
   - Rastreamento de estado
   - Gerenciamento de memória
   - Overhead adicional

2. **Dificuldade em Testes**
   - Testes mais complexos
   - Dependência de banco
   - Mocks difíceis

3. **Overhead**
   - Mais código
   - Mais memória
   - Pode ser desnecessário

## 🎓 Lições da Live

### Pontos-Chave
1. **Unit of Work coordena transações**: Múltiplas operações em uma transação
2. **Rastreia mudanças**: Novos, modificados, removidos
3. **Commit atômico**: Tudo ou nada
4. **Resolve concorrência**: Detecta e resolve conflitos
5. **Pode usar com Active Record**: Mas geralmente usado com Repository

### Boas Práticas
1. **Sempre limpe após commit**: Evite vazamentos de memória
2. **Valide antes de registrar**: Evite duplicações
3. **Trate erros**: Sempre faça rollback em caso de erro
4. **Use com Repository**: Ideal para Domain Model
5. **Documente estratégias**: Especialmente resolução de conflitos

## 📚 Referências

- **Patterns of Enterprise Application Architecture** - Martin Fowler
  - Capítulo: Data Source Architectural Patterns
  - Páginas: 184-200

---

**Última atualização**: 2025-11-16
**Mantenedor**: Equipe Skynet
**Versão**: 1.0

