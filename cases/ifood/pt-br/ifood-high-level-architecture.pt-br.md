# Plataforma iFood – Arquitetura de Alto Nível (PT-BR)

> **English version**: [High-Level Architecture](../ifood-high-level-architecture.md)

---

## Visão Geral
Evolução do iFood de uma operação analógica para uma plataforma tecnológica em grande escala:
- Núcleo inicial monolítico (Java) com Oracle on-prem.
- Modernização progressiva: microsserviços, Postgres, barramento de mensagens e nuvem.
- Subsistema de logística em tempo real com telemetria leve (MQTT), clusterização e roteirização (heurísticas tipo TSP) e práticas SRE resilientes.

## Objetivos Arquiteturais
- **Velocidade**: Lançar rápido, aprender com pilotos e iterar.
- **Escalabilidade**: Escala horizontal para pedidos e logística em picos (ex.: domingo à noite, Dia dos Namorados).
- **Disponibilidade**: Minimizar downtime com serviços resilientes, estratégias de rollout e playbooks de incidente.
- **Segurança**: Segredos fora do código, IAM e controle de mudanças em produção.
- **Operabilidade**: Observabilidade-first (métricas, logs, traces), on-call claro e resposta a incidentes objetiva.

## Diagrama
```mermaid
graph TD
  U[Clientes (Web/Mobile)] --> GW[API Gateway]
  GW --> ORD[Serviço de Pedidos]
  GW --> RST[Integração de Restaurantes]
  GW --> PAY[Adaptador de Pagamentos]
  GW --> LGX[Orquestrador de Logística]
  LGX --> TEL[Ingestão de Telemetria (MQTT)]
  TEL --> BUS[Barramento de Eventos (Kafka/Rabbit)]
  LGX --> CLU[Engine de Clusterização]
  LGX --> RTG[Engine de Roteirização]
  ORD --> DBP[(Postgres)]
  RST --> CCH[(Cache)]
  SUB[Sistemas (Promo, Catálogo, Usuário)] --> ORD
  OBS[Stack de Observabilidade] -->|Dashboards/Alertas| OPS[On-call/SRE]
  ORD --> OBS
  LGX --> OBS
  PAY --> OBS
```

## Componentes Principais
- **API Gateway**: Autenticação/autorização, rate limit e roteamento.
- **Serviço de Pedidos**: Jornada do pedido; monólito (Java)+Oracle → microsserviços+Postgres.
- **Integração de Restaurantes**: Menu, disponibilidade, push/ack; cache agressivo.
- **Pagamentos**: Abstração sobre adquirentes/antifraude; segredos externalizados.
- **Orquestrador de Logística**: Atribuição, batching e rotas dinâmicas.
- **Telemetria (MQTT)**: Ingestão leve de localização/status; menor overhead que HTTP.
- **Barramento de Eventos**: Desacoplamento, buffer e backpressure.
- **Clusterização & Roteirização**: Agrupamento espaço-temporal e heurísticas TSP; decomposição por cidade/região/bairro.
- **Observabilidade**: Prometheus, logs centralizados, OpenTelemetry e Alertmanager.

## Padrões
- **Strangler** para modernização do monólito.
- **Event-driven** na logística e efeitos de pedido.
- **Degradação graciosa** e backpressure em pico.
- **Pilotos percentuais** com rótulo beta para mitigar risco reputacional.

## Decisões-Chave
- Oracle → Postgres por domínio (reduzir gargalo/custo, aumentar agilidade).
- MQTT para telemetria por eficiência em rede/CPU.
- Particionar por cidade/região/bairro para manter roteirização viável.
- Logística cloud-native para aproveitar elasticidade.

## Qualidades
- **Performance**: Ciclos de atribuição sub-minuto; frescor da telemetria em segundos.
- **Escala**: Ingest/roteirização escaláveis horizontalmente.
- **Disponibilidade**: Blue/green ou canary; rollback rápido.
- **Segurança**: Cofre de segredos; menor privilégio; aprovação de mudança.

## Stack (indicativo)
- **Serviços**: Java/Node microsserviços.
- **Dados**: Postgres (OLTP), Redis, storage de objetos.
- **Mensageria**: Kafka/RabbitMQ; broker MQTT.
- **Infra**: Kubernetes (cloud), IaC, GitOps.
- **Obs**: Prometheus, Loki/ELK, Jaeger/Tempo, Alertmanager.

---
Atualização: 2025-10-30


