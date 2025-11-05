# Padrões de Design de Eventos

## 📋 Visão Geral

Este guia cobre padrões de design de eventos incluindo padrão envelope, estratégias de retry, idempotência e versionamento de eventos.

---

## 📦 Padrão Envelope

### Definição

**Padrão Envelope**: Envolver dados de evento em envelope com metadata.

**Estrutura**:
```typescript
interface EventEnvelope {
  // Header
  id: string;              // ID único do evento
  type: string;            // Tipo do evento
  timestamp: Date;         // Quando evento ocorreu
  source: string;          // Fonte do evento
  version: string;         // Versão do schema do evento
  
  // Trace
  traceId?: string;        // Distributed tracing
  correlationId?: string;  // Correlação de requisição
  
  // Payload
  data: any;               // Dados do evento
}
```

### Benefícios

- **Metadata**: Trace, correlação, versionamento
- **Padronização**: Estrutura de evento consistente
- **Evolução**: Tratamento de versão
- **Observabilidade**: Tracing e monitoramento

---

## 🔄 Estratégias de Retry

### Exponential Backoff

**Padrão**: Aumentar delay entre retries exponencialmente.

```typescript
async function processarEvento(event: Event, tentativa = 1): Promise<void> {
  try {
    await handleEvent(event);
  } catch (error) {
    if (tentativa < MAX_RETRIES) {
      const delay = Math.pow(2, tentativa) * 1000; // 2s, 4s, 8s, ...
      await delay(delay);
      return processarEvento(event, tentativa + 1);
    }
    // Enviar para dead letter queue
    await sendToDLQ(event, error);
  }
}
```

### Fixed Delay

**Padrão**: Delay fixo entre retries.

```typescript
async function processarEvento(event: Event, tentativa = 1): Promise<void> {
  try {
    await handleEvent(event);
  } catch (error) {
    if (tentativa < MAX_RETRIES) {
      await delay(5000); // 5 segundos
      return processarEvento(event, tentativa + 1);
    }
    await sendToDLQ(event, error);
  }
}
```

---

## 🛡️ Idempotência

### Princípio

**Idempotência**: Processar mesmo evento múltiplas vezes tem mesmo efeito que processar uma vez.

### Padrões

**Chave de Idempotência**:
```typescript
async function handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
  // Verificar se já foi processado
  const key = `order:${event.orderId}:${event.id}`;
  const processed = await idempotencyStore.get(key);
  if (processed) return; // Já processado
  
  // Processar evento
  await processOrder(event);
  
  // Marcar como processado
  await idempotencyStore.set(key, true);
}
```

**Verificação de Banco de Dados**:
```typescript
async function handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
  // Verificar se pedido já existe
  const existing = await orderRepository.findById(event.orderId);
  if (existing) return; // Já processado
  
  // Processar evento
  await orderRepository.save(createOrder(event));
}
```

---

## 📊 Versionamento de Eventos

### Estratégia

**Versão no Envelope**: Incluir versão no envelope do evento.

```typescript
interface EventEnvelope {
  version: string; // "1.0", "2.0"
  data: any;
}
```

**Tratamento de Versão**:
```typescript
async function handleEvent(event: EventEnvelope): Promise<void> {
  switch (event.version) {
    case '1.0':
      await handleV1(event.data);
      break;
    case '2.0':
      await handleV2(event.data);
      break;
    default:
      throw new Error(`Versão não suportada: ${event.version}`);
  }
}
```

---

## 🔗 Documentação Relacionada

- [Guia de Arquitetura Orientada a Eventos](./README.md) - Visão geral
- [Quando Usar Eventos](./when-to-use.md) - Guia de decisão

**Versão em Inglês**: [Event Design Patterns (EN)](../event-design-patterns.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

