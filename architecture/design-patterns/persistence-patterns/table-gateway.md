# Table Gateway Pattern

## 📋 Informações do Documento

- **Tipo**: Padrão de Persistência
- **Categoria**: Data Source Architectural Patterns
- **Versão**: 1.0
- **Data**: 2025-11-16
- **Fonte**: Patterns of Enterprise Application Architecture - Martin Fowler

## 🎯 Visão Geral

O padrão **Table Gateway** atua como um gateway para uma tabela do banco de dados. Uma instância trata todos os registros daquela tabela, encapsulando operações SQL e fornecendo uma interface orientada a objetos para acessar dados.

## 📖 Definição

> "Um objeto que atua como um Gateway para uma tabela do banco de dados. Uma instância trata todos os registros daquela tabela."

## 🔍 Características

### Estrutura
- Uma instância por tabela
- Encapsula operações SQL
- Fornece interface orientada a objetos
- Trabalha com registros (rows)

### Responsabilidades
1. **Operações CRUD**
   - Create, Read, Update, Delete
   - Operações sobre a tabela inteira

2. **Conversão de Dados**
   - De banco (snake_case) para aplicação (camelCase)
   - Mapeamento de tipos
   - Conversão de datas

3. **Abstração SQL**
   - Esconde detalhes de SQL
   - Fornece interface simples
   - Facilita manutenção

## 💡 Quando Usar

### ✅ Situações Ideais

1. **Aplicações Simples**
   - CRUD básico
   - Poucas regras de negócio
   - Tabelas simples

2. **Rapidez de Desenvolvimento**
   - Prototipagem
   - MVPs
   - Projetos pequenos

3. **Equipes Pequenas**
   - Poucos desenvolvedores
   - Sem necessidade de abstrações complexas
   - Curva de aprendizado baixa

4. **Tabelas Independentes**
   - Sem relacionamentos complexos
   - Operações diretas
   - Pouca lógica de negócio

### ❌ Quando Evitar

1. **Lógica de Negócio Complexa**
   - Múltiplas validações
   - Transições de estado
   - Regras complexas

2. **Relacionamentos Complexos**
   - Múltiplas tabelas relacionadas
   - Joins complexos
   - Agregados

3. **Necessidade de Domain Model**
   - Preservar invariâncias
   - Objetos de domínio ricos
   - Use Repository

## 🏗️ Estrutura de Implementação

### Exemplo Básico

```typescript
// Table Gateway para tabela tickets
class TicketTableGateway {
  constructor(private connection: Pool) {}

  async findById(id: string): Promise<TicketRecord | null> {
    const query = 'SELECT * FROM tickets WHERE id = $1';
    const result = await this.connection.query(query, [id]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return this.mapRow(result.rows[0]);
  }

  async findByStatus(status: string): Promise<TicketRecord[]> {
    const query = 'SELECT * FROM tickets WHERE status = $1';
    const result = await this.connection.query(query, [status]);
    
    return result.rows.map(row => this.mapRow(row));
  }

  async insert(ticket: TicketRecord): Promise<void> {
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

  async update(ticket: TicketRecord): Promise<void> {
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
  private mapRow(row: any): TicketRecord {
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

// Record/Data Structure
interface TicketRecord {
  id: string;
  content: string;
  requesterId: string;
  agentId: string | null;
  status: string;
  startDate: Date;
  endDate: Date | null;
  duration: number | null;
}
```

### Uso com Service Layer

```typescript
// Service usando Table Gateway
class TicketService {
  constructor(private ticketGateway: TicketTableGateway) {}

  async createTicket(request: CreateTicketRequest): Promise<TicketDTO> {
    const ticket: TicketRecord = {
      id: generateId(),
      content: request.content,
      requesterId: request.requesterId,
      agentId: null,
      status: 'OPEN',
      startDate: new Date(),
      endDate: null,
      duration: null
    };

    await this.ticketGateway.insert(ticket);
    return this.toDTO(ticket);
  }

  async assignTicket(ticketId: string, agentId: string): Promise<void> {
    const ticket = await this.ticketGateway.findById(ticketId);
    if (!ticket) {
      throw new Error('Ticket not found');
    }

    // Validação no service
    if (ticket.status !== 'OPEN') {
      throw new Error('Can only assign open tickets');
    }

    ticket.agentId = agentId;
    ticket.status = 'ASSIGNED';

    await this.ticketGateway.update(ticket);
  }

  async closeTicket(ticketId: string): Promise<void> {
    const ticket = await this.ticketGateway.findById(ticketId);
    if (!ticket) {
      throw new Error('Ticket not found');
    }

    // Validação e lógica no service
    if (ticket.status === 'OPEN') {
      throw new Error('Cannot close unassigned ticket');
    }

    const endDate = new Date();
    const duration = Math.floor(
      (endDate.getTime() - ticket.startDate.getTime()) / 1000
    );

    ticket.status = 'CLOSED';
    ticket.endDate = endDate;
    ticket.duration = duration;

    await this.ticketGateway.update(ticket);
  }

  private toDTO(ticket: TicketRecord): TicketDTO {
    return {
      id: ticket.id,
      content: ticket.content,
      status: ticket.status,
      agentId: ticket.agentId,
      // ... outros campos
    };
  }
}
```

## 🔄 Table Gateway vs DAO

### Table Gateway
```typescript
// Table Gateway: uma instância para toda a tabela
class TicketTableGateway {
  findById(id: string): Promise<TicketRecord | null> { }
  findByStatus(status: string): Promise<TicketRecord[]> { }
  insert(ticket: TicketRecord): Promise<void> { }
  update(ticket: TicketRecord): Promise<void> { }
}

// Uso: uma instância
const gateway = new TicketTableGateway(connection);
const ticket = await gateway.findById('123');
```

### DAO
```typescript
// DAO: conceito mais geral, pode ter múltiplas instâncias
class TicketDAO {
  findById(id: string): Promise<TicketData | null> { }
  findByStatus(status: string): Promise<TicketData[]> { }
  save(ticket: TicketData): Promise<void> { }
}

// Uso similar, mas conceitualmente diferente
const dao = new TicketDAO(connection);
const ticket = await dao.findById('123');
```

### Diferença Principal
- **Table Gateway**: Conceito mais específico, uma instância por tabela
- **DAO**: Conceito mais geral, pode ter múltiplas implementações

## ⚠️ Armadilhas Comuns

### 1. Table Gateway com Lógica de Negócio
❌ **Evite:**
```typescript
class TicketTableGateway {
  async updateStatus(id: string, status: string): Promise<void> {
    // ❌ Lógica de negócio no gateway
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
class TicketTableGateway {
  async update(ticket: TicketRecord): Promise<void> {
    // ✅ Apenas persistência
    const query = 'UPDATE tickets SET ... WHERE id = $1';
    await this.connection.query(query, [...]);
  }
}

// Lógica de negócio no Service
class TicketService {
  async closeTicket(id: string): Promise<void> {
    const ticket = await this.gateway.findById(id);
    ticket.duration = this.calculateDuration(ticket);
    ticket.status = 'CLOSED';
    await this.gateway.update(ticket);
  }
}
```

### 2. Table Gateway para Múltiplas Tabelas
❌ **Evite:**
```typescript
// Gateway não deve gerenciar múltiplas tabelas
class TicketTableGateway {
  async findWithComments(id: string): Promise<TicketWithComments> {
    // ❌ Mistura tickets e comments
  }
}
```

✅ **Prefira:**
```typescript
// Gateways separados
class TicketTableGateway {
  async findById(id: string): Promise<TicketRecord | null> { }
}

class CommentTableGateway {
  async findByTicketId(ticketId: string): Promise<CommentRecord[]> { }
}

// Service orquestra
class TicketService {
  async getTicketWithComments(id: string) {
    const ticket = await this.ticketGateway.findById(id);
    const comments = await this.commentGateway.findByTicketId(id);
    return { ticket, comments };
  }
}
```

## 🧪 Testes com Table Gateway

### Mock para Testes
```typescript
// Mock do Table Gateway
class MockTicketTableGateway {
  private tickets: Map<string, TicketRecord> = new Map();

  async findById(id: string): Promise<TicketRecord | null> {
    return this.tickets.get(id) || null;
  }

  async findByStatus(status: string): Promise<TicketRecord[]> {
    return Array.from(this.tickets.values())
      .filter(ticket => ticket.status === status);
  }

  async insert(ticket: TicketRecord): Promise<void> {
    this.tickets.set(ticket.id, ticket);
  }

  async update(ticket: TicketRecord): Promise<void> {
    this.tickets.set(ticket.id, ticket);
  }

  async delete(id: string): Promise<void> {
    this.tickets.delete(id);
  }
}

// Teste usando mock
describe('TicketService', () => {
  it('should create a ticket', async () => {
    const mockGateway = new MockTicketTableGateway();
    const service = new TicketService(mockGateway);
    
    const ticket = await service.createTicket({
      content: 'Internet is slow',
      requesterId: 'user-1'
    });
    
    expect(ticket.id).toBeDefined();
    expect(ticket.status).toBe('OPEN');
  });
});
```

## 📊 Vantagens e Desvantagens

### ✅ Vantagens

1. **Simplicidade**
   - Fácil de entender
   - Curva de aprendizado baixa
   - Código direto

2. **Rapidez de Desenvolvimento**
   - Implementação rápida
   - Poucas abstrações
   - Ideal para MVPs

3. **Abstração SQL**
   - Esconde detalhes de SQL
   - Facilita manutenção
   - Interface simples

4. **Testabilidade**
   - Fácil criar mocks
   - Testes isolados
   - Sem dependência de banco

### ❌ Desvantagens

1. **Lógica de Negócio Espalhada**
   - Validações no service
   - Regras podem ser ignoradas
   - Sem preservação de invariâncias

2. **Duplicação de Código**
   - Validações repetidas
   - Lógica espalhada
   - Difícil manter consistência

3. **Limitações para Domínios Complexos**
   - Não preserva invariâncias
   - Estados inválidos possíveis
   - Não ideal para DDD

## 🎓 Lições da Live

### Pontos-Chave
1. **Table Gateway encapsula tabela**: Uma instância para toda a tabela
2. **Trabalha com registros**: Dados simples, não objetos de domínio
3. **Abstrai SQL**: Esconde detalhes de implementação
4. **Ideal para casos simples**: CRUD básico, poucas regras
5. **Pode evoluir para Repository**: Quando precisar de Domain Model

### Boas Práticas
1. **Mantenha gateway simples**: Apenas operações de dados
2. **Faça mapeamento**: Converta entre banco e aplicação
3. **Separe lógica de negócio**: No service, não no gateway
4. **Use interfaces**: Facilita testes e troca de implementação
5. **Documente mapeamentos**: Especialmente conversões complexas

## 📚 Referências

- **Patterns of Enterprise Application Architecture** - Martin Fowler
  - Capítulo: Data Source Architectural Patterns
  - Páginas: 144-152

---

**Última atualização**: 2025-11-16
**Mantenedor**: Equipe Skynet
**Versão**: 1.0

