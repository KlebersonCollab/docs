# Template de Workshop Event Storming

## 📋 Visão Geral

Event Storming é uma técnica de workshop para descobrir eventos de domínio, identificar bounded contexts e entender o modelo de domínio através de exploração colaborativa.

**Duração**: 2-4 horas  
**Participantes**: Especialistas de domínio, desenvolvedores, product owners

---

## 🎯 Objetivos do Workshop

- [ ] Descobrir eventos de domínio
- [ ] Identificar bounded contexts
- [ ] Entender processos de negócio
- [ ] Mapear relacionamentos de contexto
- [ ] Identificar limites de agregados

---

## 📦 Materiais Necessários

- Notas laranja (eventos de domínio)
- Notas azuis (comandos)
- Notas amarelas (agregados)
- Notas rosa (read models)
- Notas verdes (políticas/regras)
- Notas vermelhas (hot spots/problemas)
- Quadro branco grande ou espaço de parede
- Marcadores

---

## 🗓️ Estrutura do Workshop

### Fase 1: Descoberta de Eventos de Domínio (30-60 min)

**Processo**:
1. Comece com um processo de negócio ou jornada do usuário
2. Identifique eventos que acontecem no domínio
3. Escreva eventos em notas laranja
4. Coloque eventos em ordem cronológica
5. Use tempo passado: "PedidoCriado", "PagamentoProcessado", "EnvioEnviado"

**Perguntas a Fazer**:
- O que acontece neste domínio?
- Que eventos ocorrem?
- Quais são os resultados de negócio?
- O que desencadeia esses eventos?

**Saída**: Linha do tempo de eventos de domínio

---

### Fase 2: Descoberta de Comandos (30-60 min)

**Processo**:
1. Para cada evento, identifique o que o causa
2. Escreva comandos em notas azuis
3. Coloque comandos antes de seus eventos correspondentes
4. Use forma imperativa: "CriarPedido", "ProcessarPagamento", "EnviarEnvio"

**Perguntas a Fazer**:
- O que causa este evento?
- Quem desencadeia este evento?
- Que ação leva a este resultado?

**Saída**: Comandos mapeados para eventos

---

### Fase 3: Identificação de Agregados (30-60 min)

**Processo**:
1. Agrupe eventos e comandos relacionados
2. Identifique agregados (entidades que lidam com comandos e produzem eventos)
3. Escreva agregados em notas amarelas
4. Coloque agregados acima de seus eventos/comandos

**Perguntas a Fazer**:
- Quais entidades lidam com esses comandos?
- Quais entidades produzem esses eventos?
- Quais são os limites de transação?

**Saída**: Agregados identificados

---

### Fase 4: Identificação de Bounded Context (30-60 min)

**Processo**:
1. Procure limites na linha do tempo de eventos
2. Identifique onde a terminologia muda
3. Identifique onde processos divergem
4. Desenhe limites ao redor de eventos/comandos/agregados relacionados
5. Nomeie cada bounded context

**Perguntas a Fazer**:
- Onde a terminologia muda?
- Onde os processos divergem?
- Onde há equipes diferentes?
- Onde há modelos de dados diferentes?

**Saída**: Bounded contexts identificados

---

### Fase 5: Context Mapping (30-60 min)

**Processo**:
1. Identifique relacionamentos entre bounded contexts
2. Documente padrões de integração
3. Mapeie dependências
4. Identifique pontos de integração

**Perguntas a Fazer**:
- Como contextos se relacionam?
- Quais são as dependências?
- Como contextos se integram?
- Quais padrões de integração se aplicam?

**Saída**: Context map

---

### Fase 6: Hot Spots e Problemas (30 min)

**Processo**:
1. Identifique áreas de confusão
2. Marque eventos ou processos não claros
3. Marque problemas potenciais
4. Documente perguntas e suposições

**Perguntas a Fazer**:
- O que não está claro?
- Quais são as suposições?
- Quais são os riscos?
- O que precisa de esclarecimento?

**Saída**: Lista de hot spots e perguntas

---

## 📝 Template: Evento de Domínio

```
Evento: [Nome do Evento no Tempo Passado]
Descrição: [O que aconteceu]
Ator: [Quem/o que desencadeou]
Contexto: [Bounded context]
Comandos Relacionados: [Comandos que causam este evento]
Eventos Relacionados: [Eventos que seguem este evento]
```

**Exemplo**:
```
Evento: PedidoCriado
Descrição: Um cliente fez um pedido
Ator: Cliente
Contexto: Gerenciamento de Pedidos
Comandos Relacionados: CriarPedido
Eventos Relacionados: PedidoValidado, PagamentoIniciado
```

---

## 📝 Template: Comando

```
Comando: [Nome do Comando no Imperativo]
Descrição: [Que ação é solicitada]
Ator: [Quem/o que desencadeia]
Contexto: [Bounded context]
Produz Eventos: [Eventos que este comando produz]
Agregado: [Agregado que lida com este comando]
```

**Exemplo**:
```
Comando: CriarPedido
Descrição: Cliente solicita criar um pedido
Ator: Cliente
Contexto: Gerenciamento de Pedidos
Produz Eventos: PedidoCriado
Agregado: Pedido
```

---

## 📝 Template: Agregado

```
Agregado: [Nome do Agregado]
Descrição: [O que este agregado representa]
Contexto: [Bounded context]
Lida com Comandos: [Comandos que este agregado lida]
Produz Eventos: [Eventos que este agregado produz]
Invariantes: [Regras de negócio/invariantes]
```

**Exemplo**:
```
Agregado: Pedido
Descrição: Representa um pedido de cliente
Contexto: Gerenciamento de Pedidos
Lida com Comandos: CriarPedido, CancelarPedido, AtualizarPedido
Produz Eventos: PedidoCriado, PedidoCancelado, PedidoAtualizado
Invariantes: Pedido deve ter pelo menos um item, Total deve ser positivo
```

---

## 📝 Template: Bounded Context

```
Bounded Context: [Nome do Contexto]
Descrição: [O que este contexto representa]
Eventos de Domínio: [Lista de eventos neste contexto]
Agregados: [Lista de agregados neste contexto]
Linguagem Ubíqua: [Termos-chave neste contexto]
Contextos Relacionados: [Outros contextos que este se relaciona]
```

**Exemplo**:
```
Bounded Context: Gerenciamento de Pedidos
Descrição: Gerencia pedidos de clientes
Eventos de Domínio: PedidoCriado, PedidoValidado, PedidoCancelado
Agregados: Pedido, ItemPedido
Linguagem Ubíqua: Pedido, ItemPedido, Cliente, Total
Contextos Relacionados: Processamento de Pagamento, Gerenciamento de Inventário
```

---

## 🎯 Saída do Workshop

Após o workshop, documente:

1. **Linha do Tempo de Eventos**: Lista cronológica de eventos
2. **Comandos**: Lista de comandos e seus eventos
3. **Agregados**: Lista de agregados e suas responsabilidades
4. **Bounded Contexts**: Lista de bounded contexts e seus limites
5. **Context Map**: Mapa de relacionamentos entre contextos
6. **Hot Spots**: Lista de áreas não claras e perguntas
7. **Próximos Passos**: Itens de ação e follow-up

---

## 📊 Exemplo: Processo de Pedido E-Commerce

### Linha do Tempo de Eventos

```
1. PedidoCriado
2. PedidoValidado
3. PagamentoIniciado
4. PagamentoProcessado
5. InventarioReservado
6. EnvioCriado
7. EnvioEnviado
8. PedidoAtendido
```

### Comandos

```
CriarPedido → PedidoCriado
ValidarPedido → PedidoValidado
IniciarPagamento → PagamentoIniciado
ProcessarPagamento → PagamentoProcessado
ReservarInventario → InventarioReservado
CriarEnvio → EnvioCriado
EnviarEnvio → EnvioEnviado
AtenderPedido → PedidoAtendido
```

### Agregados

```
Pedido (lida com: CriarPedido, ValidarPedido, CancelarPedido)
Pagamento (lida com: IniciarPagamento, ProcessarPagamento)
Inventario (lida com: ReservarInventario, LiberarInventario)
Envio (lida com: CriarEnvio, EnviarEnvio)
```

### Bounded Contexts

```
Gerenciamento de Pedidos:
- Eventos: PedidoCriado, PedidoValidado, PedidoCancelado
- Agregados: Pedido

Processamento de Pagamento:
- Eventos: PagamentoIniciado, PagamentoProcessado, PagamentoFalhou
- Agregados: Pagamento

Gerenciamento de Inventário:
- Eventos: InventarioReservado, InventarioLiberado
- Agregados: Inventario

Envio:
- Eventos: EnvioCriado, EnvioEnviado
- Agregados: Envio
```

---

## ✅ Checklist do Workshop

Antes do workshop:
- [ ] Agendar workshop (2-4 horas)
- [ ] Convidar participantes (especialistas de domínio, desenvolvedores)
- [ ] Preparar materiais (notas adesivas, marcadores, quadro branco)
- [ ] Definir escopo (qual processo/jornada explorar)

Durante o workshop:
- [ ] Facilitar descoberta de eventos de domínio
- [ ] Identificar comandos e agregados
- [ ] Mapear bounded contexts
- [ ] Documentar relacionamentos
- [ ] Identificar hot spots

Após o workshop:
- [ ] Documentar achados
- [ ] Criar mapa de bounded context
- [ ] Criar linha do tempo de eventos
- [ ] Listar itens de ação
- [ ] Agendar follow-up se necessário

---

## 🔗 Documentação Relacionada

- [Guia de DDD Estratégico](../../architecture/ddd/strategic-ddd/pt-br/README.md)
- [Identificação de Bounded Context](../../architecture/ddd/strategic-ddd/pt-br/bounded-context-identification.md)
- [Padrões de Context Mapping](../../architecture/ddd/strategic-ddd/pt-br/context-mapping-patterns.md)

**Versão em Inglês**: [Event Storming Workshop Template (EN)](../event-storming-template.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

