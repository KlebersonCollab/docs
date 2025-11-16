# Repository Pattern

## 📋 Informações do Documento

- **Tipo**: Padrão de Persistência
- **Categoria**: Data Source Architectural Patterns
- **Versão**: 1.0
- **Data**: 2025-11-16
- **Fonte**: Patterns of Enterprise Application Architecture - Martin Fowler

## 🎯 Visão Geral

O padrão **Repository** fornece uma interface orientada a objetos para acessar objetos de domínio, abstraindo detalhes de persistência. É fundamental quando se trabalha com Domain Model, pois permite que a lógica de negócio trabalhe com objetos de domínio sem conhecer detalhes de como são persistidos.

## 📖 Definição

> "Mediante uma interface orientada a objetos, encapsula o conjunto de objetos persistidos em memória e as operações realizadas sobre eles, proporcionando uma perspectiva mais orientada a objetos da camada de persistência."

## 🔍 Características

### Estrutura
- Interface orientada a objetos
- Trabalha com objetos de domínio
- Abstrai detalhes de persistência
- Retorna entidades e agregados

### Princípios Fundamentais

1. **Abstração de Persistência**
   - Lógica de negócio não conhece detalhes
   - Pode trocar implementação
   - Facilita testes

2. **Orientado a Domínio**
   - Retorna objetos de domínio
   - Preserva invariâncias
   - Trabalha com agregados

3. **Interface Rica**
   - Métodos específicos do domínio
   - Não apenas CRUD genérico
   - Expressa intenção

## 💡 Quando Usar

### ✅ Situações Ideais

1. **Domain Model**
   - Trabalhando com objetos de domínio
   - Preservando invariâncias
   - Centralizando regras de negócio

2. **Testabilidade**
   - Fácil criar mocks
   - Testes de unidade isolados
   - Sem dependência de banco

3. **Múltiplas Fontes de Dados**
   - Diferentes bancos
   - APIs externas
   - Cache

4. **DDD (Domain-Driven Design)**
   - Agregados
   - Entidades
   - Value Objects

### ❌ Quando Evitar

1. **Aplicações Simples**
   - CRUD básico
   - Sem lógica de negócio complexa
   - Overhead desnecessário

2. **Sem Domain Model**
   - Apenas DTOs
   - Transaction Script
   - Use DAO ao invés

3. **Consultas Complexas**
   - Relatórios
   - Estatísticas
   - Use Query Objects ou DAO

## 🏗️ Estrutura de Implementação

### Exemplo Básico

```typescript
// Interface do Repository
interface TicketRepository {
  save(ticket: Ticket): Promise<void>;
  findById(id: string): Promise<Ticket | null>;
  findByStatus(status: TicketStatus): Promise<Ticket[]>;
  findByRequester(requesterId: string): Promise<Ticket[]>;
}

// Implementação do Repository
class TicketRepositoryImpl implements TicketRepository {
  constructor(private dao: TicketDAO) {}

  async save(ticket: Ticket): Promise<void> {
    const data = this.toData(ticket);
    await this.dao.save(data);
  }

  async findById(id: string): Promise<Ticket | null> {
    const data = await this.dao.findById(id);
    if (!data) {
      return null;
    }
    return Ticket.restore(data);
  }

  async findByStatus(status: TicketStatus): Promise<Ticket[]> {
    const dataList = await this.dao.findByStatus(status);
    return dataList.map(data => Ticket.restore(data));
  }

  async findByRequester(requesterId: string): Promise<Ticket[]> {
    const dataList = await this.dao.findByRequester(requesterId);
    return dataList.map(data => Ticket.restore(data));
  }

  // Conversão de domínio para persistência
  private toData(ticket: Ticket): TicketData {
    return {
      id: ticket.getId(),
      content: ticket.getContent(),
      requesterId: ticket.getRequesterId(),
      agentId: ticket.getAgentId(),
      status: ticket.getStatus(),
      startDate: ticket.getStartDate(),
      endDate: ticket.getEndDate(),
      duration: ticket.getDuration()
    };
  }
}
```

### Uso com Domain Model

```typescript
// Service usando Repository
class TicketService {
  constructor(private ticketRepository: TicketRepository) {}

  async createTicket(request: CreateTicketRequest): Promise<TicketDTO> {
    // Criar objeto de domínio
    const ticket = Ticket.create(request.content, request.requesterId);
    
    // Persistir através do repository
    await this.ticketRepository.save(ticket);
    
    // Converter para DTO (fronteira da aplicação)
    return this.toDTO(ticket);
  }

  async assignTicket(ticketId: string, agentId: string): Promise<void> {
    // Restaurar objeto de domínio
    const ticket = await this.ticketRepository.findById(ticketId);
    if (!ticket) {
      throw new Error('Ticket not found');
    }
    
    // Operação de domínio (preserva invariâncias)
    ticket.assign(agentId);
    
    // Persistir
    await this.ticketRepository.save(ticket);
  }

  async closeTicket(ticketId: string): Promise<void> {
    const ticket = await this.ticketRepository.findById(ticketId);
    if (!ticket) {
      throw new Error('Ticket not found');
    }
    
    // Operação de domínio
    ticket.close();
    
    // Persistir
    await this.ticketRepository.save(ticket);
  }

  private toDTO(ticket: Ticket): TicketDTO {
    return {
      id: ticket.getId(),
      content: ticket.getContent(),
      status: ticket.getStatus(),
      agentId: ticket.getAgentId(),
      // ... outros campos
    };
  }
}
```

## 🔄 Repository vs DAO

### Repository
```typescript
// Repository trabalha com objetos de domínio
interface TicketRepository {
  save(ticket: Ticket): Promise<void>; // ✅ Objeto de domínio
  findById(id: string): Promise<Ticket | null>; // ✅ Retorna domínio
}

// Uso
const ticket = await repository.findById(id);
ticket.close(); // ✅ Método de domínio
await repository.save(ticket);
```

### DAO
```typescript
// DAO trabalha com dados simples
interface TicketDAO {
  save(ticket: TicketData): Promise<void>; // ✅ Dados simples
  findById(id: string): Promise<TicketData | null>; // ✅ Retorna dados
}

// Uso
const ticketData = await dao.findById(id);
// ticketData não tem comportamento
ticketData.status = 'CLOSED'; // ❌ Sem validação
await dao.update(ticketData);
```

### Diferença Principal
- **Repository**: Retorna **objetos de domínio** com comportamento
- **DAO**: Retorna **dados simples** sem comportamento

## 🎯 Repository e Agregados

### Agregados em DDD
```typescript
// Agregado: Ticket (raiz do agregado)
class Ticket {
  private id: string;
  private content: string;
  private comments: Comment[]; // Entidades dentro do agregado

  addComment(comment: Comment): void {
    // Regra de negócio: validar antes de adicionar
    if (this.status === TicketStatus.CLOSED) {
      throw new Error('Cannot add comment to closed ticket');
    }
    this.comments.push(comment);
  }
}

// Repository trabalha com agregados
interface TicketRepository {
  save(ticket: Ticket): Promise<void>; // Salva o agregado inteiro
  findById(id: string): Promise<Ticket | null>;
}
```

### Preservação de Invariâncias
```typescript
// Repository garante que operações respeitam agregados
class TicketRepositoryImpl {
  async save(ticket: Ticket): Promise<void> {
    // Salva ticket e todos os comentários
    // Garante consistência do agregado
    await this.dao.saveTicket(ticket);
    await this.dao.saveComments(ticket.getComments());
  }
}
```

## ⚠️ Armadilhas Comuns

### 1. Repository com Consultas Complexas
❌ **Evite:**
```typescript
// Repository não deve ter métodos de relatório
interface TicketRepository {
  getTicketsReport(status: string, start: Date, end: Date, agentId: string): Promise<Report>; // ❌
}
```

✅ **Prefira:**
```typescript
// Use Query Objects ou DAO para consultas
interface TicketQueryService {
  getTicketsReport(status: string, start: Date, end: Date, agentId: string): Promise<Report>; // ✅
}

// Repository apenas para operações de domínio
interface TicketRepository {
  save(ticket: Ticket): Promise<void>;
  findById(id: string): Promise<Ticket | null>;
}
```

### 2. Repository Permitindo Bypass de Regras
❌ **Evite:**
```typescript
// Repository não deve permitir atualizar status diretamente
interface TicketRepository {
  updateStatus(id: string, status: string): Promise<void>; // ❌
}
```

✅ **Prefira:**
```typescript
// Repository apenas salva objetos de domínio
interface TicketRepository {
  save(ticket: Ticket): Promise<void>; // ✅
}

// Operações de domínio no objeto
ticket.close(); // ✅ Valida regras
await repository.save(ticket);
```

### 3. Repository Retornando DTOs
❌ **Evite:**
```typescript
// Repository não deve retornar DTOs
interface TicketRepository {
  findById(id: string): Promise<TicketDTO>; // ❌
}
```

✅ **Prefira:**
```typescript
// Repository retorna objetos de domínio
interface TicketRepository {
  findById(id: string): Promise<Ticket>; // ✅
}

// Conversão para DTO na camada de aplicação
const ticket = await repository.findById(id);
const dto = toDTO(ticket);
```

## 🧪 Testes com Repository

### Mock do Repository
```typescript
// Mock do Repository
class MockTicketRepository implements TicketRepository {
  private tickets: Map<string, Ticket> = new Map();

  async save(ticket: Ticket): Promise<void> {
    this.tickets.set(ticket.getId(), ticket);
  }

  async findById(id: string): Promise<Ticket | null> {
    return this.tickets.get(id) || null;
  }

  async findByStatus(status: TicketStatus): Promise<Ticket[]> {
    return Array.from(this.tickets.values())
      .filter(ticket => ticket.getStatus() === status);
  }

  async findByRequester(requesterId: string): Promise<Ticket[]> {
    return Array.from(this.tickets.values())
      .filter(ticket => ticket.getRequesterId() === requesterId);
  }
}

// Teste usando mock
describe('TicketService', () => {
  it('should assign ticket to agent', async () => {
    const mockRepository = new MockTicketRepository();
    const service = new TicketService(mockRepository);
    
    // Criar ticket
    const ticket = Ticket.create('Internet is slow', 'user-1');
    await mockRepository.save(ticket);
    
    // Atribuir
    await service.assignTicket(ticket.getId(), 'agent-1');
    
    // Verificar
    const updated = await mockRepository.findById(ticket.getId());
    expect(updated.getStatus()).toBe(TicketStatus.ASSIGNED);
    expect(updated.getAgentId()).toBe('agent-1');
  });
});
```

## 🔗 Repository e Unit of Work

### Unit of Work Pattern
```typescript
// Unit of Work coordena múltiplas operações
class UnitOfWork {
  private tickets: Ticket[] = [];

  registerNew(ticket: Ticket): void {
    this.tickets.push(ticket);
  }

  async commit(): Promise<void> {
    // Salva todos os tickets de uma vez
    for (const ticket of this.tickets) {
      await this.repository.save(ticket);
    }
    this.tickets = [];
  }
}

// Uso
const uow = new UnitOfWork();
uow.registerNew(ticket1);
uow.registerNew(ticket2);
await uow.commit(); // Transação única
```

## 📊 Vantagens e Desvantagens

### ✅ Vantagens

1. **Abstração de Persistência**
   - Lógica de negócio isolada
   - Fácil trocar implementação
   - Testabilidade

2. **Preservação de Invariâncias**
   - Trabalha com objetos de domínio
   - Regras centralizadas
   - Estados inválidos impossíveis

3. **Testabilidade**
   - Fácil criar mocks
   - Testes isolados
   - Sem dependência de banco

4. **Expressividade**
   - Interface rica
   - Métodos específicos
   - Intenção clara

### ❌ Desvantagens

1. **Complexidade**
   - Mais abstrações
   - Mais código
   - Curva de aprendizado

2. **Overhead**
   - Conversões de dados
   - Mais camadas
   - Pode ser desnecessário

3. **Consultas Complexas**
   - Não ideal para relatórios
   - Pode precisar de DAO adicional
   - Overhead para consultas simples

## 🎓 Lições da Live

### Pontos-Chave
1. **Repository trabalha com domínio**: Retorna objetos de domínio, não dados
2. **Preserva invariâncias**: Operações passam pelo objeto de domínio
3. **Não para consultas complexas**: Use DAO ou Query Objects
4. **Pode usar DAO por trás**: Repository pode delegar para DAO
5. **Facilita testes**: Fácil criar mocks

### Boas Práticas
1. **Mantenha interface rica**: Métodos específicos do domínio
2. **Não permita bypass**: Todas as operações passam pelo domínio
3. **Use para agregados**: Trabalhe com raízes de agregados
4. **Separe consultas**: Use Query Objects para relatórios
5. **Documente**: Especialmente conversões complexas

## 📚 Referências

- **Patterns of Enterprise Application Architecture** - Martin Fowler
  - Capítulo: Data Source Architectural Patterns
  - Páginas: 323-334

- **Domain-Driven Design** - Eric Evans
  - Capítulo: Repositories

---

**Última atualização**: 2025-11-16
**Mantenedor**: Equipe Skynet
**Versão**: 1.0

