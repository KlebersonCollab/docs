# Design do Read Model

## 📋 Visão Geral

O Read Model é otimizado para queries. É tipicamente desnormalizado e eventualmente consistente.

**Princípio Fundamental**: Read Model = Projections. Otimize para performance de leitura, não consistência de escrita.

---

## 🎯 Princípios de Design

### 1. Otimização de Query

**Princípio**: Otimize para performance de leitura.

**Técnicas**:
- Desnormalização
- Agregações pré-computadas
- Queries indexadas
- Cache

### 2. Consistência Eventual

**Princípio**: Read models são eventualmente consistentes.

**Características**:
- Atualizados assincronamente
- Podem estar ligeiramente obsoletos
- Aceitável para a maioria das queries

### 3. Projeções

**Princípio**: Read models são projeções de eventos.

**Processo**:
- Eventos publicados do command model
- Event handlers atualizam read models
- Read models otimizados para queries

---

## 🏗️ Estrutura

### Padrão de Projeção

```
Domain Event → Event Handler → Atualização do Read Model
```

### Exemplo de Projeção

```typescript
class ProjecaoResumoPedido {
  async aoPedidoCriado(event: PedidoCriadoEvent): Promise<void> {
    const resumo: ResumoPedido = {
      id: event.pedidoId,
      clienteId: event.clienteId,
      total: this.calcularTotal(event.items),
      quantidadeItens: event.items.length,
      status: 'Pendente',
      criadoEm: event.timestamp
    };
    await this.readRepository.save(resumo);
  }
  
  async aoPedidoCancelado(event: PedidoCanceladoEvent): Promise<void> {
    await this.readRepository.update(event.pedidoId, {
      status: 'Cancelado'
    });
  }
}
```

### Query Handlers

```typescript
class ObterResumoPedidoQueryHandler {
  async handle(query: ObterResumoPedidoQuery): Promise<ResumoPedido> {
    return await this.readRepository.findById(query.pedidoId);
  }
}
```

---

## 📊 Estratégias de Otimização

### 1. Desnormalização

**Princípio**: Armazene dados em formato pronto para query.

**Exemplo**:
```typescript
// Read Model Desnormalizado
interface ResumoPedido {
  id: string;
  clienteId: string;
  nomeCliente: string;  // Desnormalizado de Cliente
  total: number;        // Pré-computado
  quantidadeItens: number;  // Pré-computado
  status: string;
}
```

### 2. Agregações Pré-computadas

**Princípio**: Calcule agregações durante projeção.

**Exemplo**:
```typescript
// Calcular total durante projeção
async aoPedidoCriado(event: PedidoCriadoEvent): Promise<void> {
  const total = event.items.reduce((soma, item) => 
    soma + (item.preco * item.quantidade), 0
  );
  // Armazenar total pré-computado
}
```

### 3. Cache

**Princípio**: Faça cache de read models frequentemente acessados.

**Exemplo**:
```typescript
class RepositorioResumoPedidoCacheado {
  async findById(id: string): Promise<ResumoPedido> {
    // Verificar cache primeiro
    const cached = await this.cache.get(id);
    if (cached) return cached;
    // Fallback para banco de dados
    const resumo = await this.db.findById(id);
    await this.cache.set(id, resumo);
    return resumo;
  }
}
```

---

## 🔄 Tratamento de Eventos

### Padrão Event Handler

```typescript
class ProjecaoReadModelPedido {
  async handle(event: DomainEvent): Promise<void> {
    switch (event.type) {
      case 'PedidoCriado':
        await this.aoPedidoCriado(event);
        break;
      case 'PedidoCancelado':
        await this.aoPedidoCancelado(event);
        break;
      // ... outros eventos
    }
  }
}
```

### Idempotência

**Princípio**: Event handlers devem ser idempotentes.

**Exemplo**:
```typescript
async aoPedidoCriado(event: PedidoCriadoEvent): Promise<void> {
  // Verificar se já foi processado
  const existente = await this.readRepository.findById(event.pedidoId);
  if (existente) return; // Já processado
  
  // Processar evento
  const resumo = this.criarResumo(event);
  await this.readRepository.save(resumo);
}
```

---

## 🔗 Documentação Relacionada

- [Guia de CQRS](./README.md) - Visão geral
- [Design do Command Model](./command-model-design.md) - Design do command model
- [Guia de Event-Driven Architecture](../../event-driven-architecture/README.md) - Tratamento de eventos

**Versão em Inglês**: [Read Model Design (EN)](../read-model-design.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

