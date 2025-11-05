# Template de Documentação de Bounded Context

## 📋 Visão Geral

Este template ajuda a documentar um bounded context em DDD Estratégico. Use este template para documentar cada bounded context identificado em seu sistema.

---

## Bounded Context: [Nome do Contexto]

### Informações Básicas

**Nome**: [Nome do Contexto]  
**Versão**: [Número da Versão]  
**Última Atualização**: [Data]  
**Proprietário**: [Equipe/Papel]  
**Status**: [Ativo | Em Desenvolvimento | Depreciado]

---

### Descrição

[Breve descrição do que este bounded context representa e seu propósito]

**Exemplo**:
> O bounded context de Gerenciamento de Pedidos é responsável por gerenciar pedidos de clientes ao longo de seu ciclo de vida, da criação ao atendimento. Ele lida com criação de pedidos, validação, cancelamento e rastreamento de status.

---

### Linguagem Ubíqua

**Termos-Chave**:

| Termo | Definição | Exemplo |
|-------|-----------|---------|
| [Termo 1] | [Definição] | [Uso do exemplo] |
| [Termo 2] | [Definição] | [Uso do exemplo] |
| [Termo 3] | [Definição] | [Uso do exemplo] |

**Exemplo**:
| Termo | Definição | Exemplo |
|-------|-----------|---------|
| Pedido | Solicitação de compra de um cliente | "Pedido #12345 contém 3 itens" |
| ItemPedido | Um único item em um pedido | "ItemPedido: 2x Produto A" |
| StatusPedido | Estado atual do pedido | "StatusPedido: PENDENTE" |

---

### Modelo de Domínio

**Agregados**:

- **[Nome do Agregado]**
  - Descrição: [O que este agregado representa]
  - Comandos: [Lista de comandos que este agregado lida]
  - Eventos: [Lista de eventos que este agregado produz]
  - Invariantes: [Regras de negócio que devem ser mantidas]

**Exemplo**:
- **Pedido**
  - Descrição: Representa um pedido de cliente
  - Comandos: CriarPedido, CancelarPedido, AtualizarPedido
  - Eventos: PedidoCriado, PedidoCancelado, PedidoAtualizado
  - Invariantes: Pedido deve ter pelo menos um item, Total deve ser positivo

---

### Eventos de Domínio

**Eventos Produzidos**:

| Evento | Descrição | Desencadeado Por |
|--------|-----------|------------------|
| [Evento 1] | [Descrição] | [Comando/Agregado] |
| [Evento 2] | [Descrição] | [Comando/Agregado] |

**Exemplo**:
| Evento | Descrição | Desencadeado Por |
|--------|-----------|------------------|
| PedidoCriado | Pedido foi criado pelo cliente | Comando CriarPedido |
| PedidoCancelado | Pedido foi cancelado | Comando CancelarPedido |
| PedidoValidado | Pedido passou na validação | Comando ValidarPedido |

---

### Comandos

**Comandos Tratados**:

| Comando | Descrição | Handler | Produz Eventos |
|---------|-----------|---------|----------------|
| [Comando 1] | [Descrição] | [Agregado] | [Evento 1, Evento 2] |
| [Comando 2] | [Descrição] | [Agregado] | [Evento 3] |

**Exemplo**:
| Comando | Descrição | Handler | Produz Eventos |
|---------|-----------|---------|----------------|
| CriarPedido | Criar um novo pedido | Agregado Pedido | PedidoCriado |
| CancelarPedido | Cancelar um pedido existente | Agregado Pedido | PedidoCancelado |
| ValidarPedido | Validar regras de negócio do pedido | Agregado Pedido | PedidoValidado |

---

### Limites do Contexto

**O que Está Dentro**:
- [Responsabilidade 1]
- [Responsabilidade 2]
- [Responsabilidade 3]

**O que Está Fora**:
- [Não responsável por 1]
- [Não responsável por 2]
- [Não responsável por 3]

**Exemplo**:
**O que Está Dentro**:
- Criação e gerenciamento de pedidos
- Validação de pedidos
- Rastreamento de status de pedidos

**O que Está Fora**:
- Processamento de pagamento (contexto Processamento de Pagamento)
- Gerenciamento de inventário (contexto Gerenciamento de Inventário)
- Coordenação de envio (contexto Envio)

---

### Relacionamentos de Contexto

**Contextos Upstream** (dependências):
- **[Nome do Contexto]**: [Tipo de relacionamento e descrição]
  - Padrão de Integração: [Padrão usado]
  - Tecnologia de Integração: [Tecnologia usada]

**Contextos Downstream** (dependem deste):
- **[Nome do Contexto]**: [Tipo de relacionamento e descrição]
  - Padrão de Integração: [Padrão usado]
  - Tecnologia de Integração: [Tecnologia usada]

**Exemplo**:
**Contextos Upstream**:
- **Catálogo de Produtos**: Relacionamento Customer-Supplier
  - Padrão de Integração: REST API
  - Tecnologia de Integração: HTTP/REST

**Contextos Downstream**:
- **Processamento de Pagamento**: Relacionamento Customer-Supplier (somos upstream)
  - Padrão de Integração: REST API
  - Tecnologia de Integração: HTTP/REST

---

### Classificação de Subdomínio

**Classificação**: [Core Domain | Supporting Subdomain | Generic Subdomain]

**Racionalização**: [Por que esta classificação]

**Prioridade de Investimento**: [Alta | Média | Baixa]

**Estratégia de Construção**: [Construir Internamente | Construir ou Terceirizar | Terceirizar/Integrar]

**Exemplo**:
**Classificação**: Supporting Subdomain

**Racionalização**: Gerenciamento de pedidos é importante para operações mas não é um diferenciador competitivo. Comum em plataformas de e-commerce.

**Prioridade de Investimento**: Média

**Estratégia de Construção**: Construir Internamente (complexidade média, suporta core domain)

---

### Detalhes de Implementação

**Stack Tecnológico**:
- Linguagem: [Linguagem de programação]
- Framework: [Framework]
- Banco de Dados: [Banco de dados]
- Outros: [Outras tecnologias]

**Deploy**:
- Unidade de Deploy: [Monolito | Microsserviço | Módulo]
- Frequência de Deploy: [Frequência]
- Equipe de Deploy: [Equipe]

**Exemplo**:
**Stack Tecnológico**:
- Linguagem: TypeScript
- Framework: Express.js
- Banco de Dados: PostgreSQL
- Outros: Redis para cache

**Deploy**:
- Unidade de Deploy: Microsserviço
- Frequência de Deploy: Diária
- Equipe de Deploy: Equipe de Gerenciamento de Pedidos

---

### Pontos de Integração

**APIs Expostas**:
- [Endpoint de API 1]: [Descrição]
- [Endpoint de API 2]: [Descrição]

**Eventos Publicados**:
- [Evento 1]: [Descrição, subscribers]
- [Evento 2]: [Descrição, subscribers]

**Eventos Assinados**:
- [Evento 1]: [Contexto de origem, handler]
- [Evento 2]: [Contexto de origem, handler]

**Exemplo**:
**APIs Expostas**:
- `POST /pedidos`: Criar um novo pedido
- `GET /pedidos/{id}`: Obter detalhes do pedido
- `PATCH /pedidos/{id}/cancelar`: Cancelar um pedido

**Eventos Publicados**:
- `PedidoCriado`: Publicado quando pedido é criado (subscribers: Processamento de Pagamento, Gerenciamento de Inventário)
- `PedidoCancelado`: Publicado quando pedido é cancelado (subscribers: Processamento de Pagamento, Gerenciamento de Inventário)

**Eventos Assinados**:
- `PagamentoProcessado`: Do contexto Processamento de Pagamento (handler: AtualizarStatusPedido)
- `InventarioReservado`: Do contexto Gerenciamento de Inventário (handler: ConfirmarPedido)

---

### Regras de Negócio

**Regras de Negócio Principais**:
1. [Regra de negócio 1]
2. [Regra de negócio 2]
3. [Regra de negócio 3]

**Exemplo**:
1. Pedido deve ter pelo menos um item
2. Total do pedido deve ser positivo
3. Pedido não pode ser cancelado após envio
4. Pedido deve ser validado antes do pagamento

---

### Estratégia de Evolução

**Estado Atual**: [Descrição do estado atual]

**Evolução Planejada**:
- [Evolução 1]: [Descrição, timeline]
- [Evolução 2]: [Descrição, timeline]

**Estratégia de Migração**: [Como evoluir sem breaking changes]

**Exemplo**:
**Estado Atual**: Módulo monolítico, banco de dados compartilhado

**Evolução Planejada**:
- Extrair para microsserviço: Q2 2025
- Banco de dados separado: Q2 2025
- Integração orientada a eventos: Q3 2025

**Estratégia de Migração**: Extração gradual usando padrão strangler fig

---

### Métricas e Monitoramento

**Métricas Principais**:
- [Métrica 1]: [Descrição, meta]
- [Métrica 2]: [Descrição, meta]

**Monitoramento**:
- [O que monitorar]
- [Alertas configurados]

**Exemplo**:
**Métricas Principais**:
- Taxa de criação de pedidos: Meta: < 100ms p95
- Taxa de sucesso de validação de pedidos: Meta: > 99%
- Taxa de cancelamento de pedidos: Meta: < 5%

**Monitoramento**:
- Tempos de resposta de API
- Latência de processamento de eventos
- Taxas de erro

---

### Equipe e Propriedade

**Equipe**: [Nome da equipe]

**Papéis**:
- [Papel 1]: [Responsabilidade]
- [Papel 2]: [Responsabilidade]

**On-Call**: [Rotação de on-call ou contato]

**Exemplo**:
**Equipe**: Equipe de Gerenciamento de Pedidos

**Papéis**:
- Desenvolvedores Backend: Lógica de gerenciamento de pedidos
- Product Owner: Requisitos de funcionalidades de pedidos
- QA: Testes de pedidos

**On-Call**: Rotação com equipe de Processamento de Pagamento

---

### Documentação

**Documentação Relacionada**:
- [Link para documentação relacionada]
- [Link para documentação de API]
- [Link para diagramas de arquitetura]

**Exemplos**:
- [Diagrama de Arquitetura de Gerenciamento de Pedidos](./diagrams/order-management-architecture.md)
- [Documentação de API de Pedidos](./api/order-api.md)
- [Modelo de Domínio de Pedidos](./domain/order-domain-model.md)

---

### Notas e Decisões

**Decisões Principais**:
- [Decisão 1]: [Racionalização, data]
- [Decisão 2]: [Racionalização, data]

**Trade-offs**:
- [Trade-off 1]: [O que foi escolhido, o que foi sacrificado]

**Exemplo**:
**Decisões Principais**:
- Escolheu microsserviço sobre monolito: Melhor escalabilidade, autonomia da equipe (2024-01-15)
- Escolheu orientado a eventos sobre síncrono: Melhor desacoplamento, escalabilidade (2024-02-01)

**Trade-offs**:
- Microsserviço: Melhor escalabilidade mas complexidade operacional aumentada
- Orientado a eventos: Melhor desacoplamento mas consistência eventual

---

## 🔗 Documentação Relacionada

- [Guia de DDD Estratégico](../../architecture/ddd/strategic-ddd/pt-br/README.md)
- [Identificação de Bounded Context](../../architecture/ddd/strategic-ddd/pt-br/bounded-context-identification.md)
- [Padrões de Context Mapping](../../architecture/ddd/strategic-ddd/pt-br/context-mapping-patterns.md)
- [Template de Event Storming](./event-storming-template.md)

**Versão em Inglês**: [Bounded Context Documentation Template (EN)](../bounded-context-template.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

