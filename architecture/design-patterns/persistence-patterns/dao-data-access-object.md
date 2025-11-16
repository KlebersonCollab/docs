# Data Access Object (DAO) Pattern

## 📋 Informações do Documento

- **Tipo**: Padrão de Persistência
- **Categoria**: Data Source Architectural Patterns
- **Versão**: 1.0
- **Data**: 2025-11-16
- **Fonte**: Patterns of Enterprise Application Architecture - Martin Fowler

## 🎯 Visão Geral

O padrão **Data Access Object (DAO)** encapsula o acesso a uma fonte de dados, abstraindo detalhes de implementação e fornecendo uma interface orientada a objetos para acessar dados. É um padrão fundamental para separar lógica de negócio de detalhes de persistência.

## 📖 Definição

> "Um objeto que atua como um Gateway para uma tabela do banco de dados. Uma instância trata todos os registros daquela tabela."

## 🔍 Características

### Estrutura
- Encapsula acesso a dados
- Abstrai detalhes de implementação
- Fornece interface orientada a objetos
- Pode trabalhar com múltiplas tabelas

### Responsabilidades
1. **Operações CRUD**
   - Create (criar)
   - Read (ler)
   - Update (atualizar)
   - Delete (deletar)

2. **Conversão de Dados**
   - De banco para objetos
   - De objetos para banco
   - Mapeamento de tipos

3. **Gerenciamento de Conexões**
   - Abrir/fechar conexões
   - Gerenciar transações
   - Tratar erros

## 💡 Quando Usar

### ✅ Situações Ideais

1. **Separação de Responsabilidades**
   - Isolar lógica de acesso a dados
   - Facilitar mudanças de implementação
   - Melhorar testabilidade

2. **Múltiplas Fontes de Dados**
   - Diferentes bancos de dados
   - APIs externas
   - Arquivos

3. **Testabilidade**
   - Fácil criar mocks
   - Isolar testes
   - Substituir implementação

4. **Flexibilidade**
   - Trocar implementação facilmente
   - Suportar diferentes estratégias
   - Adaptar a mudanças

### ❌ Quando Evitar

1. **Aplicações Muito Simples**
   - Operações CRUD básicas
   - Sem necessidade de abstração
   - Overhead desnecessário

2. **ORM Completo**
   - Já fornece abstração
   - DAO seria redundante
   - Use Repository ao invés

## 🏗️ Estrutura de Implementação

### Exemplo Básico

```typescript
// Interface do DAO
interface TicketDAO {
  save(ticket: TicketData): Promise<void>;
  findById(id: string): Promise<TicketData | null>;
  findByStatus(status: string): Promise<TicketData[]>;
  update(ticket: TicketData): Promise<void>;
  delete(id: string): Promise<void>;
}

// Implementação com PostgreSQL
class TicketDAOImpl implements TicketDAO {
  constructor(private connection: Pool) {}

  async save(ticket: TicketData): Promise<void> {
    const query = `
      INSERT INTO tickets (id, content, requester_id, agent_id, status, start_date)
      VALUES ($1, $2, $3, $4, $5, $6)
    `;
    
    await this.connection.query(query, [
      ticket.id,
      ticket.content,
      ticket.requesterId,
      ticket.agentId,
      ticket.status,
      ticket.startDate
    ]);
  }

  async findById(id: string): Promise<TicketData | null> {
    const query = 'SELECT * FROM tickets WHERE id = $1';
    const result = await this.connection.query(query, [id]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return this.mapRowToTicket(result.rows[0]);
  }

  async findByStatus(status: string): Promise<TicketData[]> {
    const query = 'SELECT * FROM tickets WHERE status = $1';
    const result = await this.connection.query(query, [status]);
    
    return result.rows.map(row => this.mapRowToTicket(row));
  }

  async update(ticket: TicketData): Promise<void> {
    const query = `
      UPDATE tickets 
      SET content = $2, requester_id = $3, agent_id = $4, 
          status = $5, start_date = $6, end_date = $7, duration = $8
      WHERE id = $1
    `;
    
    await this.connection.query(query, [
      ticket.id,
      ticket.content,
      ticket.requesterId,
      ticket.agentId,
      ticket.status,
      ticket.startDate,
      ticket.endDate,
      ticket.duration
    ]);
  }

  async delete(id: string): Promise<void> {
    const query = 'DELETE FROM tickets WHERE id = $1';
    await this.connection.query(query, [id]);
  }

  // Mapeamento de linha do banco para objeto
  private mapRowToTicket(row: any): TicketData {
    return {
      id: row.id,
      content: row.content,
      requesterId: row.requester_id, // snake_case → camelCase
      agentId: row.agent_id,
      status: row.status,
      startDate: row.start_date,
      endDate: row.end_date,
      duration: row.duration
    };
  }
}
```

### Uso com Service Layer

```typescript
// Service usando DAO
class TicketService {
  constructor(private ticketDao: TicketDAO) {}

  async createTicket(request: CreateTicketRequest): Promise<TicketDTO> {
    const ticket: TicketData = {
      id: generateId(),
      content: request.content,
      requesterId: request.requesterId,
      agentId: null,
      status: 'OPEN',
      startDate: new Date(),
      endDate: null,
      duration: null
    };

    await this.ticketDao.save(ticket);
    return this.toDTO(ticket);
  }

  async getTicket(id: string): Promise<TicketDTO> {
    const ticket = await this.ticketDao.findById(id);
    if (!ticket) {
      throw new Error('Ticket not found');
    }
    return this.toDTO(ticket);
  }

  private toDTO(ticket: TicketData): TicketDTO {
    return {
      id: ticket.id,
      content: ticket.content,
      status: ticket.status,
      // ... outros campos
    };
  }
}
```

## 🔄 DAO vs Repository

### DAO
```typescript
// DAO trabalha com estruturas de dados simples
interface TicketDAO {
  save(ticket: TicketData): Promise<void>;
  findById(id: string): Promise<TicketData | null>;
}

// Retorna DTO/Data
const ticketData = await ticketDao.findById(id);
// ticketData é uma estrutura simples, sem comportamento
```

### Repository
```typescript
// Repository trabalha com objetos de domínio
interface TicketRepository {
  save(ticket: Ticket): Promise<void>;
  findById(id: string): Promise<Ticket | null>;
}

// Retorna objeto de domínio
const ticket = await ticketRepository.findById(id);
// ticket é um objeto com comportamento
ticket.close(); // Método de domínio
```

### Diferença Principal
- **DAO**: Trabalha com **dados** (DTOs, Records, Structs)
- **Repository**: Trabalha com **objetos de domínio** (Entidades, Agregados)

## 🎯 DAO e Table Gateway

### Table Gateway
```typescript
// Table Gateway: uma instância para toda a tabela
class TicketTableGateway {
  findById(id: string): Promise<TicketData | null> { }
  findByStatus(status: string): Promise<TicketData[]> { }
  save(ticket: TicketData): Promise<void> { }
}

// Uso
const gateway = new TicketTableGateway();
const ticket = await gateway.findById('123');
```

### DAO
```typescript
// DAO: pode ter múltiplas instâncias, mais flexível
class TicketDAO {
  findById(id: string): Promise<TicketData | null> { }
  findByStatus(status: string): Promise<TicketData[]> { }
  save(ticket: TicketData): Promise<void> { }
}

// Uso similar, mas conceitualmente diferente
const dao = new TicketDAO();
const ticket = await dao.findById('123');
```

### Diferença
- **Table Gateway**: Conceito mais específico, uma instância por tabela
- **DAO**: Conceito mais geral, pode ter múltiplas implementações

## 🧪 Testes com DAO

### Mock para Testes
```typescript
// Mock do DAO
class MockTicketDAO implements TicketDAO {
  private tickets: Map<string, TicketData> = new Map();

  async save(ticket: TicketData): Promise<void> {
    this.tickets.set(ticket.id, ticket);
  }

  async findById(id: string): Promise<TicketData | null> {
    return this.tickets.get(id) || null;
  }

  async findByStatus(status: string): Promise<TicketData[]> {
    return Array.from(this.tickets.values())
      .filter(ticket => ticket.status === status);
  }

  async update(ticket: TicketData): Promise<void> {
    this.tickets.set(ticket.id, ticket);
  }

  async delete(id: string): Promise<void> {
    this.tickets.delete(id);
  }
}

// Teste usando mock
describe('TicketService', () => {
  it('should create a ticket', async () => {
    const mockDao = new MockTicketDAO();
    const service = new TicketService(mockDao);
    
    const ticket = await service.createTicket({
      content: 'Internet is slow',
      requesterId: 'user-1'
    });
    
    expect(ticket.id).toBeDefined();
    expect(ticket.status).toBe('OPEN');
  });
});
```

## ⚠️ Armadilhas Comuns

### 1. DAO com Lógica de Negócio
❌ **Evite:**
```typescript
class TicketDAO {
  async updateStatus(id: string, status: string): Promise<void> {
    // ❌ Lógica de negócio no DAO
    if (status === 'CLOSED') {
      const ticket = await this.findById(id);
      ticket.duration = calculateDuration(ticket.startDate, new Date());
    }
    await this.update(ticket);
  }
}
```

✅ **Prefira:**
```typescript
class TicketDAO {
  async update(ticket: TicketData): Promise<void> {
    // ✅ Apenas persistência
    const query = 'UPDATE tickets SET ... WHERE id = $1';
    await this.connection.query(query, [...]);
  }
}

// Lógica de negócio no Service ou Domain Model
class TicketService {
  async closeTicket(id: string): Promise<void> {
    const ticket = await this.dao.findById(id);
    ticket.duration = this.calculateDuration(ticket);
    ticket.status = 'CLOSED';
    await this.dao.update(ticket);
  }
}
```

### 2. DAO Retornando Objetos de Domínio
❌ **Evite:**
```typescript
// DAO não deve retornar objetos de domínio
class TicketDAO {
  async findById(id: string): Promise<Ticket> { // ❌
    // ...
  }
}
```

✅ **Prefira:**
```typescript
// DAO retorna dados simples
class TicketDAO {
  async findById(id: string): Promise<TicketData> { // ✅
    // ...
  }
}

// Repository converte para domínio
class TicketRepository {
  async findById(id: string): Promise<Ticket> {
    const data = await this.dao.findById(id);
    return Ticket.restore(data);
  }
}
```

## 📊 Vantagens e Desvantagens

### ✅ Vantagens

1. **Separação de Responsabilidades**
   - Lógica de acesso isolada
   - Fácil de manter
   - Mudanças localizadas

2. **Testabilidade**
   - Fácil criar mocks
   - Testes isolados
   - Sem dependência de banco

3. **Flexibilidade**
   - Trocar implementação
   - Suportar múltiplas fontes
   - Adaptar a mudanças

4. **Reutilização**
   - Compartilhar entre serviços
   - Evitar duplicação
   - Código centralizado

### ❌ Desvantagens

1. **Overhead**
   - Mais camadas
   - Mais código
   - Complexidade adicional

2. **Abstração Desnecessária**
   - Para casos simples
   - Pode ser over-engineering
   - Aumenta complexidade

## 🎓 Lições da Live

### Pontos-Chave
1. **DAO encapsula acesso a dados**: Abstrai detalhes de implementação
2. **Trabalha com dados simples**: DTOs, não objetos de domínio
3. **Facilita testes**: Fácil criar mocks
4. **Separa responsabilidades**: Lógica de negócio separada de persistência
5. **Pode ser usado com Repository**: DAO pode estar por trás do Repository

### Boas Práticas
1. **Mantenha DAO simples**: Apenas operações de dados
2. **Use interfaces**: Facilita testes e troca de implementação
3. **Faça mapeamento**: Converta entre banco e aplicação
4. **Trate erros**: Gerencie exceções de banco
5. **Documente**: Especialmente mapeamentos complexos

## 📚 Referências

- **Patterns of Enterprise Application Architecture** - Martin Fowler
  - Capítulo: Data Source Architectural Patterns
  - Páginas: 144-152

---

**Última atualização**: 2025-11-16
**Mantenedor**: Equipe Skynet
**Versão**: 1.0

