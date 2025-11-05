# Design do Command Model

## 📋 Visão Geral

O Command Model é o modelo de domínio otimizado para lidar com comandos (mutações). Aplica regras de negócio e mantém consistência.

**Princípio Fundamental**: Command Model = Domain Model. É a fonte autoritativa para lógica de negócio.

---

## 🎯 Princípios de Design

### 1. Domain-Driven Design

**Princípio**: Command Model segue princípios DDD.

**Características**:
- Modelo de domínio rico
- Lógica de negócio no domínio
- Entidades e value objects
- Eventos de domínio

### 2. Aplicação de Regras de Negócio

**Princípio**: Todas as regras de negócio aplicadas no Command Model.

**Exemplos**:
- Regras de validação
- Invariantes
- Restrições de negócio
- Regras de workflow

### 3. Consistência

**Princípio**: Command Model mantém consistência transacional.

**Características**:
- Transações ACID
- Consistência imediata
- Garantias de consistência forte

---

## 🏗️ Estrutura

### Aggregate Root

**Padrão**: Command Model organizado em torno de aggregates.

**Exemplo**:
```typescript
class Pedido {
  private items: ItemPedido[] = [];
  private status: StatusPedido;
  
  criarPedido(clienteId: string, items: ItemPedido[]): void {
    // Regras de negócio
    if (items.length === 0) {
      throw new Error('Pedido deve ter itens');
    }
    // Mudanças de estado
    this.items = items;
    this.status = StatusPedido.Pendente;
    // Eventos de domínio
    DomainEventPublisher.publish(new PedidoCriadoEvent(this.id));
  }
}
```

### Command Handlers

**Padrão**: Comandos processados por command handlers.

**Exemplo**:
```typescript
class CriarPedidoCommandHandler {
  async handle(command: CriarPedidoCommand): Promise<void> {
    const pedido = new Pedido();
    pedido.criarPedido(command.clienteId, command.items);
    await this.pedidoRepository.save(pedido);
  }
}
```

---

## 📚 Padrões

### Padrão Command

**Estrutura**:
```
Command → Command Handler → Domain Model → Events
```

### Validação

**Onde**: No modelo de domínio ou command handler.

**Exemplo**:
```typescript
class Pedido {
  criarPedido(clienteId: string, items: ItemPedido[]): void {
    // Validação
    if (!clienteId) throw new Error('ID do cliente necessário');
    if (items.length === 0) throw new Error('Itens necessários');
    // Lógica de negócio
    this.items = items;
  }
}
```

### Eventos de Domínio

**Propósito**: Notificar outras partes do sistema sobre mudanças.

**Exemplo**:
```typescript
class Pedido {
  cancelarPedido(): void {
    if (this.status === StatusPedido.Enviado) {
      throw new Error('Não pode cancelar pedido enviado');
    }
    this.status = StatusPedido.Cancelado;
    DomainEventPublisher.publish(new PedidoCanceladoEvent(this.id));
  }
}
```

---

## 🔗 Documentação Relacionada

- [Guia de CQRS](./README.md) - Visão geral
- [Design do Read Model](./read-model-design.md) - Design do read model
- [Guia de DDD Estratégico](../../ddd/strategic-ddd/README.md) - Modelagem de domínio

**Versão em Inglês**: [Command Model Design (EN)](../command-model-design.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

