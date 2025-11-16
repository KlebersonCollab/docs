# Domain Model Pattern

## 📋 Informações do Documento

- **Tipo**: Padrão de Persistência
- **Categoria**: Domain Logic Patterns
- **Versão**: 1.0
- **Data**: 2025-11-16
- **Fonte**: Patterns of Enterprise Application Architecture - Martin Fowler

## 🎯 Visão Geral

O padrão **Domain Model** incorpora tanto dados quanto comportamento em objetos de domínio, preservando invariâncias e centralizando regras de negócio. É a abordagem mais rica e poderosa para lidar com lógica de negócio complexa.

## 📖 Definição

> "Um objeto de domínio que incorpora tanto dados quanto comportamento, preservando invariâncias e centralizando regras de negócio."

## 🔍 Características

### Estrutura
- Objetos de domínio com comportamento
- Preservação de invariâncias
- Encapsulamento de regras de negócio
- Identidade e ciclo de vida gerenciados

### Princípios Fundamentais

1. **Encapsulamento**
   - Dados privados
   - Comportamento público
   - Invariâncias protegidas

2. **Identidade**
   - Cada entidade tem identidade única
   - Identidade persiste através do tempo
   - Identidade diferente de igualdade

3. **Ciclo de Vida**
   - Criação controlada
   - Modificação através de métodos
   - Persistência gerenciada

## 💡 Quando Usar

### ✅ Situações Ideais

1. **Regras de Negócio Complexas**
   - Múltiplas validações
   - Transições de estado complexas
   - Cálculos e transformações

2. **Preservação de Invariâncias**
   - Estados inválidos devem ser impossíveis
   - Regras de negócio críticas
   - Integridade de dados essencial

3. **Aplicações de Grande Porte**
   - Múltiplos desenvolvedores
   - Longa duração
   - Manutenção contínua

4. **Domain-Driven Design (DDD)**
   - Linguagem ubíqua
   - Agregados
   - Entidades e Value Objects

### ❌ Quando Evitar

1. **Lógica Muito Simples**
   - Operações CRUD básicas
   - Poucas regras de negócio
   - Aplicações pequenas

2. **Equipe Sem Experiência**
   - Falta de conhecimento em OOP
   - Sem experiência em DDD
   - Curva de aprendizado alta

3. **Performance Crítica**
   - Operações muito simples
   - Overhead de objetos inaceitável
   - Requisitos extremos de performance

## 🏗️ Estrutura de Implementação

### Exemplo Básico

```typescript
// Entidade de Domínio
class Ticket {
  private constructor(
    private readonly id: string,
    private content: string,
    private requesterId: string,
    private agentId: string | null,
    private status: TicketStatus,
    private startDate: Date,
    private endDate: Date | null,
    private duration: number | null
  ) {}

  // Factory Method - Porta de entrada controlada
  static create(content: string, requesterId: string): Ticket {
    return new Ticket(
      generateId(),
      content,
      requesterId,
      null,
      TicketStatus.OPEN,
      new Date(),
      null,
      null
    );
  }

  // Métodos de Domínio - Preservam Invariâncias
  assign(agentId: string): void {
    if (this.status !== TicketStatus.OPEN) {
      throw new Error('Can only assign open tickets');
    }
    
    this.agentId = agentId;
    this.status = TicketStatus.ASSIGNED;
  }

  close(): void {
    if (this.status === TicketStatus.OPEN) {
      throw new Error('Cannot close unassigned ticket');
    }
    
    if (this.status === TicketStatus.CLOSED) {
      throw new Error('Ticket is already closed');
    }

    this.endDate = new Date();
    this.duration = this.calculateDuration();
    this.status = TicketStatus.CLOSED;
  }

  private calculateDuration(): number {
    if (!this.endDate) {
      throw new Error('End date is required to calculate duration');
    }
    
    return Math.floor(
      (this.endDate.getTime() - this.startDate.getTime()) / 1000
    );
  }

  // Getters - Acesso controlado
  getId(): string {
    return this.id;
  }

  getStatus(): TicketStatus {
    return this.status;
  }

  getAgentId(): string | null {
    return this.agentId;
  }

  // Método para hidratação (restauração do banco)
  static restore(data: TicketData): Ticket {
    return new Ticket(
      data.id,
      data.content,
      data.requesterId,
      data.agentId,
      data.status,
      data.startDate,
      data.endDate,
      data.duration
    );
  }
}

enum TicketStatus {
  OPEN = 'OPEN',
  ASSIGNED = 'ASSIGNED',
  CLOSED = 'CLOSED'
}
```

### Uso com Repository

```typescript
// Service Layer
class TicketService {
  constructor(private ticketRepository: TicketRepository) {}

  async createTicket(request: CreateTicketRequest): Promise<TicketDTO> {
    // Criar objeto de domínio
    const ticket = Ticket.create(request.content, request.requesterId);
    
    // Persistir através do repositório
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
    
    // Operação de domínio
    ticket.assign(agentId);
    
    // Persistir
    await this.ticketRepository.save(ticket);
  }

  async closeTicket(ticketId: string): Promise<void> {
    const ticket = await this.ticketRepository.findById(ticketId);
    if (!ticket) {
      throw new Error('Ticket not found');
    }
    
    ticket.close();
    await this.ticketRepository.save(ticket);
  }

  private toDTO(ticket: Ticket): TicketDTO {
    return {
      id: ticket.getId(),
      status: ticket.getStatus(),
      agentId: ticket.getAgentId(),
      // ... outros campos
    };
  }
}
```

## 🔄 Comparação com Transaction Script

### Transaction Script
```typescript
// Regras espalhadas em procedimentos
async function closeTicket(ticketId: string) {
  const ticket = await ticketDao.findById(ticketId);
  
  // Validação no procedimento
  if (ticket.status === 'OPEN') {
    throw new Error('Cannot close unassigned ticket');
  }
  
  // Cálculo no procedimento
  ticket.duration = calculateDuration(ticket.startDate, new Date());
  ticket.status = 'CLOSED';
  
  await ticketDao.update(ticket);
}
```

### Domain Model
```typescript
// Regras centralizadas no objeto
class Ticket {
  close(): void {
    // Validação encapsulada
    if (this.status === TicketStatus.OPEN) {
      throw new Error('Cannot close unassigned ticket');
    }
    
    // Cálculo encapsulado
    this.duration = this.calculateDuration();
    this.status = TicketStatus.CLOSED;
  }
}

// Uso simples e seguro
const ticket = await repository.findById(ticketId);
ticket.close(); // Invariâncias preservadas
await repository.save(ticket);
```

## 🛡️ Preservação de Invariâncias

### ❌ Sem Domain Model
```typescript
// Estados inválidos possíveis
ticket.status = 'CLOSED';
ticket.agentId = null; // Inválido! Ticket fechado sem agente
ticket.duration = -100; // Inválido! Duração negativa
```

### ✅ Com Domain Model
```typescript
// Estados inválidos impossíveis
class Ticket {
  private status: TicketStatus;
  private agentId: string | null;
  private duration: number | null;

  close(): void {
    // Validação obrigatória
    if (this.status === TicketStatus.OPEN) {
      throw new Error('Cannot close unassigned ticket');
    }
    
    // Cálculo automático
    this.duration = this.calculateDuration();
    this.status = TicketStatus.CLOSED;
    // agentId já está definido (invariância preservada)
  }
}
```

## 🧪 Testes com Domain Model

### Teste de Unidade (Isolado)
```typescript
describe('Ticket - Unit Tests', () => {
  it('should create a new ticket with OPEN status', () => {
    const ticket = Ticket.create('Internet is slow', 'user-1');
    
    expect(ticket.getStatus()).toBe(TicketStatus.OPEN);
    expect(ticket.getAgentId()).toBeNull();
  });

  it('should assign ticket to agent', () => {
    const ticket = Ticket.create('Internet is slow', 'user-1');
    
    ticket.assign('agent-1');
    
    expect(ticket.getStatus()).toBe(TicketStatus.ASSIGNED);
    expect(ticket.getAgentId()).toBe('agent-1');
  });

  it('should not allow closing unassigned ticket', () => {
    const ticket = Ticket.create('Internet is slow', 'user-1');
    
    expect(() => ticket.close()).toThrow('Cannot close unassigned ticket');
  });

  it('should calculate duration when closing', () => {
    const ticket = Ticket.create('Internet is slow', 'user-1');
    ticket.assign('agent-1');
    
    // Simular passagem de tempo
    jest.useFakeTimers();
    jest.setSystemTime(new Date('2025-01-15T10:00:00Z'));
    const startTime = new Date();
    
    jest.setSystemTime(new Date('2025-01-15T11:30:00Z'));
    ticket.close();
    
    expect(ticket.getStatus()).toBe(TicketStatus.CLOSED);
    // Duração calculada automaticamente
  });
});
```

### Vantagens dos Testes de Unidade
- ✅ **Rápidos**: Não dependem de banco de dados
- ✅ **Isolados**: Testam apenas lógica de domínio
- ✅ **Determinísticos**: Sem dependências externas
- ✅ **Fáceis de escrever**: Objetos simples

## 🔗 Integração com Repository

### Repository Pattern
```typescript
interface TicketRepository {
  save(ticket: Ticket): Promise<void>;
  findById(id: string): Promise<Ticket | null>;
  findByStatus(status: TicketStatus): Promise<Ticket[]>;
}

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

  private toData(ticket: Ticket): TicketData {
    // Conversão de domínio para persistência
    return {
      id: ticket.getId(),
      status: ticket.getStatus(),
      // ... outros campos
    };
  }
}
```

## 📊 Vantagens e Desvantagens

### ✅ Vantagens

1. **Preservação de Invariâncias**
   - Estados inválidos impossíveis
   - Regras de negócio centralizadas
   - Integridade garantida

2. **Testabilidade**
   - Testes de unidade isolados
   - Sem dependências externas
   - Rápidos e determinísticos

3. **Manutenibilidade**
   - Código organizado
   - Responsabilidades claras
   - Fácil evoluir

4. **Expressividade**
   - Código legível
   - Linguagem ubíqua
   - Intenção clara

### ❌ Desvantagens

1. **Complexidade**
   - Curva de aprendizado
   - Mais abstrações
   - Overhead inicial

2. **Performance**
   - Mais objetos criados
   - Mais indireções
   - Pode ser mais lento (geralmente irrelevante)

3. **Overhead de Desenvolvimento**
   - Mais código inicial
   - Mais tempo de design
   - Requer experiência

## 🎓 Lições da Live

### Pontos-Chave
1. **Domain Model preserva invariâncias**: Estados inválidos são impossíveis
2. **Testes de unidade viáveis**: Não precisa de banco de dados
3. **Repository abstrai persistência**: Retorna objetos de domínio
4. **Evolução natural**: Comece simples, evolua quando necessário
5. **Performance não é problema**: Abstrações raramente causam problemas

### Quando Migrar para Domain Model
- ✅ Regras de negócio complexas
- ✅ Duplicação de validações
- ✅ Estados inválidos aparecendo
- ✅ Dificuldade em testar
- ✅ Necessidade de preservar invariâncias

## 📚 Referências

- **Patterns of Enterprise Application Architecture** - Martin Fowler
  - Capítulo: Domain Logic Patterns
  - Páginas: 116-135

- **Domain-Driven Design** - Eric Evans
  - Capítulo: Model-Driven Design
  - Capítulo: Building Blocks

---

**Última atualização**: 2025-11-16
**Mantenedor**: Equipe Skynet
**Versão**: 1.0

