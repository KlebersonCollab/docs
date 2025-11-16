# Transaction Script Pattern

## 📋 Informações do Documento

- **Tipo**: Padrão de Persistência
- **Categoria**: Domain Logic Patterns
- **Versão**: 1.0
- **Data**: 2025-11-16
- **Fonte**: Patterns of Enterprise Application Architecture - Martin Fowler

## 🎯 Visão Geral

O padrão **Transaction Script** organiza a lógica de negócio em procedimentos, onde cada procedimento lida com uma única requisição do sistema de apresentação. É uma abordagem simples e direta, ideal para lógica de negócio que não é muito complexa.

## 📖 Definição

> "Organiza a lógica de negócio em procedimentos, onde cada procedimento lida com uma única requisição do sistema de apresentação."

## 🔍 Características

### Estrutura
- Lógica de negócio em procedimentos/funções
- Cada procedimento trata uma transação completa
- Dados geralmente armazenados em estruturas simples (DTOs, Records)
- Acesso a dados através de DAOs ou Table Gateways

### Fluxo Típico
```
Request → Transaction Script → DAO/Table Gateway → Database
         ↑                                              ↓
         └──────────── Response ←──────────────────────┘
```

## 💡 Quando Usar

### ✅ Situações Ideais

1. **Lógica de Negócio Simples**
   - Poucas regras de negócio
   - Operações diretas e lineares
   - Sem complexidade de estado

2. **Aplicações Pequenas ou Médias**
   - Equipes pequenas
   - Escopo limitado
   - Requisitos claros

3. **Prototipagem Rápida**
   - Validação de conceitos
   - MVPs
   - Projetos de curto prazo

4. **Migração de Sistemas Legados**
   - Código procedural existente
   - Refatoração gradual
   - Manutenção de compatibilidade

### ❌ Quando Evitar

1. **Regras de Negócio Complexas**
   - Múltiplas transições de estado
   - Validações complexas
   - Lógica condicional extensa

2. **Necessidade de Preservar Invariâncias**
   - Estados inválidos devem ser impossíveis
   - Regras de negócio devem ser centralizadas
   - Integridade de dados crítica

3. **Aplicações de Grande Porte**
   - Múltiplos desenvolvedores
   - Longa duração do projeto
   - Manutenção a longo prazo

## 🏗️ Estrutura de Implementação

### Exemplo Básico

```typescript
// Transaction Script
class TicketService {
  constructor(
    private ticketDao: TicketDAO,
    private userDao: UserDAO
  ) {}

  async createTicket(request: CreateTicketRequest): Promise<TicketDTO> {
    // 1. Validar entrada
    if (!request.content || !request.requesterId) {
      throw new Error('Content and requesterId are required');
    }

    // 2. Buscar dados necessários
    const requester = await this.userDao.findById(request.requesterId);
    if (!requester) {
      throw new Error('Requester not found');
    }

    // 3. Aplicar regras de negócio
    const ticket: TicketDTO = {
      id: generateId(),
      content: request.content,
      requesterId: request.requesterId,
      status: 'OPEN',
      createdAt: new Date(),
      startDate: new Date()
    };

    // 4. Persistir
    await this.ticketDao.save(ticket);

    // 5. Retornar resultado
    return ticket;
  }

  async assignTicket(ticketId: string, agentId: string): Promise<void> {
    // 1. Buscar ticket
    const ticket = await this.ticketDao.findById(ticketId);
    if (!ticket) {
      throw new Error('Ticket not found');
    }

    // 2. Validar estado
    if (ticket.status !== 'OPEN') {
      throw new Error('Ticket must be open to assign');
    }

    // 3. Aplicar regras de negócio
    ticket.agentId = agentId;
    ticket.status = 'ASSIGNED';

    // 4. Persistir
    await this.ticketDao.update(ticket);
  }

  async closeTicket(ticketId: string): Promise<void> {
    // 1. Buscar ticket
    const ticket = await this.ticketDao.findById(ticketId);
    if (!ticket) {
      throw new Error('Ticket not found');
    }

    // 2. Validar estado
    if (ticket.status === 'OPEN') {
      throw new Error('Cannot close unassigned ticket');
    }

    // 3. Aplicar regras de negócio
    const endDate = new Date();
    const duration = Math.floor((endDate.getTime() - ticket.startDate.getTime()) / 1000);

    ticket.status = 'CLOSED';
    ticket.endDate = endDate;
    ticket.duration = duration;

    // 4. Persistir
    await this.ticketDao.update(ticket);
  }
}
```

## 🔄 Comparação com Domain Model

### Transaction Script
```typescript
// Lógica de negócio espalhada em procedimentos
async function closeTicket(ticketId: string) {
  const ticket = await ticketDao.findById(ticketId);
  
  // Regras de negócio no procedimento
  if (ticket.status === 'OPEN') {
    throw new Error('Cannot close unassigned ticket');
  }
  
  ticket.status = 'CLOSED';
  ticket.endDate = new Date();
  ticket.duration = calculateDuration(ticket.startDate, ticket.endDate);
  
  await ticketDao.update(ticket);
}
```

### Domain Model
```typescript
// Lógica de negócio no objeto de domínio
class Ticket {
  close(): void {
    if (this.status === 'OPEN') {
      throw new Error('Cannot close unassigned ticket');
    }
    
    this.status = 'CLOSED';
    this.endDate = new Date();
    this.duration = this.calculateDuration();
  }
  
  private calculateDuration(): number {
    return Math.floor(
      (this.endDate.getTime() - this.startDate.getTime()) / 1000
    );
  }
}

// Uso
const ticket = await ticketRepository.findById(ticketId);
ticket.close();
await ticketRepository.save(ticket);
```

## ⚖️ Vantagens e Desvantagens

### ✅ Vantagens

1. **Simplicidade**
   - Fácil de entender
   - Curva de aprendizado baixa
   - Código direto

2. **Performance**
   - Menos overhead
   - Menos objetos criados
   - Acesso direto a dados

3. **Rapidez de Desenvolvimento**
   - Implementação rápida
   - Poucas abstrações
   - Ideal para MVPs

4. **Compatibilidade**
   - Funciona bem com código procedural
   - Fácil migração de sistemas legados
   - Integração simples

### ❌ Desvantagens

1. **Duplicação de Código**
   - Regras de negócio repetidas
   - Validações espalhadas
   - Difícil manter consistência

2. **Falta de Encapsulamento**
   - Estados inválidos possíveis
   - Regras podem ser ignoradas
   - Sem proteção de invariâncias

3. **Testabilidade Limitada**
   - Difícil isolar lógica
   - Dependências de banco de dados
   - Testes mais complexos

4. **Manutenibilidade**
   - Mudanças em múltiplos lugares
   - Código acoplado
   - Difícil evoluir

## 🧪 Testes com Transaction Script

### Teste de Integração
```typescript
describe('TicketService - Integration Tests', () => {
  it('should create a new ticket', async () => {
    // Setup
    const ticketDao = new TicketDAO(connection);
    const userDao = new UserDAO(connection);
    const service = new TicketService(ticketDao, userDao);
    
    // Execute
    const ticket = await service.createTicket({
      content: 'Internet is slow',
      requesterId: 'user-1'
    });
    
    // Assert
    expect(ticket.id).toBeDefined();
    expect(ticket.status).toBe('OPEN');
    expect(ticket.content).toBe('Internet is slow');
  });
});
```

### Limitações
- Testes dependem de banco de dados
- Mais lentos que testes de unidade
- Configuração mais complexa
- Dificuldade em isolar comportamentos

## 🔄 Migração para Domain Model

### Sinais de que Precisa Migrar

1. **Duplicação de Regras**
   ```typescript
   // Mesma validação em múltiplos lugares
   if (ticket.status === 'OPEN') {
     throw new Error('Cannot close unassigned ticket');
   }
   ```

2. **Estados Inválidos**
   ```typescript
   // Possível criar estado inválido
   ticket.status = 'CLOSED';
   ticket.agentId = null; // Inválido!
   ```

3. **Lógica Complexa**
   ```typescript
   // Múltiplas condições e validações
   if (ticket.status === 'OPEN' && !ticket.agentId && ...) {
     // Lógica complexa
   }
   ```

### Estratégia de Migração

1. **Identificar Procedimentos Complexos**
2. **Extrair Regras de Negócio**
3. **Criar Objetos de Domínio**
4. **Migrar Gradualmente**
5. **Manter Compatibilidade**

## 📚 Referências

- **Patterns of Enterprise Application Architecture** - Martin Fowler
  - Capítulo: Domain Logic Patterns
  - Página: 110-120

## 🎓 Lições Aprendidas

### Da Live
1. Transaction Script é um bom ponto de partida
2. Não é necessário começar com Domain Model
3. Evolua conforme a complexidade cresce
4. Testes ajudam a identificar quando migrar
5. Simplicidade tem valor

### Boas Práticas
1. **Mantenha procedimentos pequenos**
2. **Extraia validações comuns**
3. **Use DTOs para transferência de dados**
4. **Documente regras de negócio**
5. **Planeje migração futura**

---

**Última atualização**: 2025-11-16
**Mantenedor**: Equipe Skynet
**Versão**: 1.0

