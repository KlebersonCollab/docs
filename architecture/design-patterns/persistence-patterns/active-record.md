# Active Record Pattern

## 📋 Informações do Documento

- **Tipo**: Padrão de Persistência
- **Categoria**: Domain Logic Patterns
- **Versão**: 1.0
- **Data**: 2025-11-16
- **Fonte**: Patterns of Enterprise Application Architecture - Martin Fowler

## 🎯 Visão Geral

O padrão **Active Record** é um objeto que encapsula uma linha de uma tabela ou view, incluindo acesso a dados e comportamento de domínio. É amplamente utilizado em frameworks como Rails, Laravel e Django, oferecendo uma abordagem simples e direta para persistência.

## 📖 Definição

> "Um objeto que encapsula uma linha de uma tabela ou view, incluindo acesso a dados e comportamento de domínio."

## 🔍 Características

### Estrutura
- Objeto representa uma linha da tabela
- Combina dados e comportamento
- Responsável por sua própria persistência
- Métodos estáticos para criação e busca

### Princípios Fundamentais

1. **Encapsulamento de Linha**
   - Cada instância = uma linha
   - Dados e comportamento juntos
   - Acesso direto a propriedades

2. **Auto-Persistência**
   - Objeto sabe como se salvar
   - Métodos `save()`, `update()`, `delete()`
   - Gerenciamento de estado

3. **Métodos Estáticos**
   - `create()` para criar
   - `find()` para buscar
   - `load()` para restaurar

## 💡 Quando Usar

### ✅ Situações Ideais

1. **Modelos de Domínio Simples**
   - Poucas regras de negócio
   - Operações CRUD básicas
   - Sem agregados complexos

2. **Frameworks que Suportam**
   - Rails (Ruby)
   - Laravel (PHP)
   - Django (Python)
   - ActiveRecord (Rails)

3. **Prototipagem Rápida**
   - Desenvolvimento rápido
   - MVPs
   - Validação de conceitos

4. **Aplicações Pequenas/Médias**
   - Equipes pequenas
   - Escopo limitado
   - Requisitos claros

### ❌ Quando Evitar

1. **Agregados Complexos**
   - Múltiplas tabelas relacionadas
   - Relacionamentos complexos
   - Lógica de negócio distribuída

2. **Regras de Negócio Complexas**
   - Múltiplas validações
   - Transições de estado complexas
   - Preservação de invariâncias crítica

3. **Necessidade de Testes de Unidade Isolados**
   - Testes sem banco de dados
   - Mocks complexos
   - Isolamento total

4. **Performance Crítica**
   - Operações muito simples
   - Overhead inaceitável
   - Requisitos extremos

## 🏗️ Estrutura de Implementação

### Exemplo Básico

```typescript
// Active Record
class Ticket extends ActiveRecord {
  // Propriedades (representam colunas)
  public id: string;
  public content: string;
  public requesterId: string;
  public agentId: string | null;
  public status: string;
  public startDate: Date;
  public endDate: Date | null;
  public duration: number | null;

  // Método estático para criar
  static create(content: string, requesterId: string): Ticket {
    const ticket = new Ticket();
    ticket.id = generateId();
    ticket.content = content;
    ticket.requesterId = requesterId;
    ticket.agentId = null;
    ticket.status = 'OPEN';
    ticket.startDate = new Date();
    ticket.endDate = null;
    ticket.duration = null;
    return ticket;
  }

  // Método estático para carregar do banco
  static async load(id: string): Promise<Ticket | null> {
    const connection = await getConnection();
    const result = await connection.query(
      'SELECT * FROM tickets WHERE id = $1',
      [id]
    );

    if (result.rows.length === 0) {
      return null;
    }

    const ticket = new Ticket();
    ticket.hydrate(result.rows[0]);
    return ticket;
  }

  // Método de domínio
  assign(agentId: string): void {
    if (this.status !== 'OPEN') {
      throw new Error('Can only assign open tickets');
    }
    this.agentId = agentId;
    this.status = 'ASSIGNED';
  }

  // Método de domínio
  close(): void {
    if (this.status === 'OPEN') {
      throw new Error('Cannot close unassigned ticket');
    }

    this.endDate = new Date();
    this.duration = Math.floor(
      (this.endDate.getTime() - this.startDate.getTime()) / 1000
    );
    this.status = 'CLOSED';
  }

  // Persistência (herdado de ActiveRecord)
  async save(): Promise<void> {
    if (this.isNew()) {
      await this.insert();
    } else {
      await this.update();
    }
  }

  private async insert(): Promise<void> {
    const connection = await getConnection();
    await connection.query(
      `INSERT INTO tickets (id, content, requester_id, agent_id, status, start_date)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [
        this.id,
        this.content,
        this.requesterId,
        this.agentId,
        this.status,
        this.startDate
      ]
    );
  }

  private async update(): Promise<void> {
    const connection = await getConnection();
    await connection.query(
      `UPDATE tickets 
       SET content = $2, requester_id = $3, agent_id = $4, 
           status = $5, start_date = $6, end_date = $7, duration = $8
       WHERE id = $1`,
      [
        this.id,
        this.content,
        this.requesterId,
        this.agentId,
        this.status,
        this.startDate,
        this.endDate,
        this.duration
      ]
    );
  }

  // Hidratação (restauração do banco)
  private hydrate(row: any): void {
    this.id = row.id;
    this.content = row.content;
    this.requesterId = row.requester_id;
    this.agentId = row.agent_id;
    this.status = row.status;
    this.startDate = row.start_date;
    this.endDate = row.end_date;
    this.duration = row.duration;
  }

  private isNew(): boolean {
    // Lógica para determinar se é novo ou existente
    return !this.id || !this.existsInDatabase();
  }

  private async existsInDatabase(): Promise<boolean> {
    const connection = await getConnection();
    const result = await connection.query(
      'SELECT 1 FROM tickets WHERE id = $1',
      [this.id]
    );
    return result.rows.length > 0;
  }
}
```

### Uso

```typescript
// Criar novo ticket
const ticket = Ticket.create('Internet is slow', 'user-1');
await ticket.save();

// Carregar do banco
const ticket = await Ticket.load('ticket-123');
if (ticket) {
  ticket.assign('agent-1');
  await ticket.save();
}

// Operações de domínio
const ticket = await Ticket.load('ticket-123');
ticket.close();
await ticket.save();
```

## 🔄 Active Record vs Domain Model + Repository

### Active Record
```typescript
// Objeto responsável por si mesmo
class Ticket {
  public status: string;
  
  close(): void {
    this.status = 'CLOSED';
  }
  
  async save(): Promise<void> {
    // Salva a si mesmo
  }
}

// Uso
const ticket = await Ticket.load(id);
ticket.close();
await ticket.save();
```

### Domain Model + Repository
```typescript
// Objeto de domínio separado de persistência
class Ticket {
  private status: TicketStatus;
  
  close(): void {
    this.status = TicketStatus.CLOSED;
  }
}

// Repository gerencia persistência
class TicketRepository {
  async save(ticket: Ticket): Promise<void> {
    // Salva o objeto
  }
}

// Uso
const ticket = await repository.findById(id);
ticket.close();
await repository.save(ticket);
```

### Diferença Principal
- **Active Record**: Objeto **é responsável** por sua persistência
- **Domain Model + Repository**: Objeto de domínio **separado** de persistência

## ⚠️ Armadilhas Comuns

### 1. Quebra de Single Responsibility Principle
❌ **Problema:**
```typescript
// Active Record tem múltiplas responsabilidades
class Ticket {
  // Responsabilidade 1: Dados
  public content: string;
  
  // Responsabilidade 2: Comportamento de domínio
  close(): void { }
  
  // Responsabilidade 3: Persistência
  async save(): Promise<void> { }
}
```

✅ **Aceitável quando:**
- Modelo de domínio simples
- Operações básicas
- Framework suporta bem

### 2. Dificuldade em Testes de Unidade
❌ **Problema:**
```typescript
// Teste precisa de banco de dados
it('should close ticket', async () => {
  const ticket = await Ticket.load(id); // Precisa de banco
  ticket.close();
  await ticket.save(); // Precisa de banco
});
```

✅ **Solução:**
```typescript
// Usar mocks ou fakes
class FakeTicket extends Ticket {
  async save(): Promise<void> {
    // Mock implementation
  }
}
```

### 3. Relacionamentos Complexos
❌ **Problema:**
```typescript
// Active Record com relacionamentos complexos
class Ticket {
  public comments: Comment[]; // Como gerenciar?
  public attachments: Attachment[]; // Como salvar?
}
```

✅ **Solução:**
- Usar Repository para relacionamentos complexos
- Ou migrar para Domain Model + Repository

## 🧪 Testes com Active Record

### Teste de Integração
```typescript
describe('Ticket - Integration Tests', () => {
  it('should create and save ticket', async () => {
    const ticket = Ticket.create('Internet is slow', 'user-1');
    await ticket.save();
    
    const loaded = await Ticket.load(ticket.id);
    expect(loaded).not.toBeNull();
    expect(loaded.status).toBe('OPEN');
  });

  it('should assign and close ticket', async () => {
    const ticket = Ticket.create('Internet is slow', 'user-1');
    await ticket.save();
    
    ticket.assign('agent-1');
    await ticket.save();
    
    ticket.close();
    await ticket.save();
    
    const loaded = await Ticket.load(ticket.id);
    expect(loaded.status).toBe('CLOSED');
  });
});
```

### Limitações
- Testes dependem de banco de dados
- Mais lentos que testes de unidade
- Configuração mais complexa
- Dificuldade em isolar comportamentos

## 📊 Vantagens e Desvantagens

### ✅ Vantagens

1. **Simplicidade**
   - Fácil de entender
   - Curva de aprendizado baixa
   - Código direto

2. **Rapidez de Desenvolvimento**
   - Implementação rápida
   - Frameworks suportam bem
   - Ideal para MVPs

3. **Produtividade**
   - Menos código
   - Menos abstrações
   - Desenvolvimento ágil

4. **Familiaridade**
   - Padrão conhecido
   - Muitos exemplos
   - Comunidade grande

### ❌ Desvantagens

1. **Single Responsibility Principle**
   - Múltiplas responsabilidades
   - Dados + Comportamento + Persistência
   - Pode quebrar princípios SOLID

2. **Testabilidade**
   - Dificuldade em testes de unidade
   - Dependência de banco
   - Mocks complexos

3. **Agregados Complexos**
   - Dificuldade com relacionamentos
   - Lógica distribuída
   - Não ideal para DDD

4. **Manutenibilidade**
   - Código acoplado
   - Mudanças em múltiplos lugares
   - Difícil evoluir

## 🎓 Lições da Live

### Pontos-Chave
1. **Active Record combina responsabilidades**: Dados + Comportamento + Persistência
2. **Ideal para modelos simples**: Operações CRUD básicas
3. **Pode quebrar SRP**: Mas aceitável em casos simples
4. **Frameworks suportam bem**: Rails, Laravel, Django
5. **Evolua quando necessário**: Para Domain Model quando complexidade crescer

### Quando Migrar
- ✅ Agregados complexos
- ✅ Regras de negócio complexas
- ✅ Necessidade de testes de unidade isolados
- ✅ Preservação de invariâncias crítica
- ✅ Múltiplas tabelas relacionadas

## 📚 Referências

- **Patterns of Enterprise Application Architecture** - Martin Fowler
  - Capítulo: Domain Logic Patterns
  - Páginas: 160-180

- **Frameworks que Usam Active Record**
  - [Ruby on Rails](https://rubyonrails.org/)
  - [Laravel (Eloquent)](https://laravel.com/docs/eloquent)
  - [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/models/)

---

**Última atualização**: 2025-11-16
**Mantenedor**: Equipe Skynet
**Versão**: 1.0

