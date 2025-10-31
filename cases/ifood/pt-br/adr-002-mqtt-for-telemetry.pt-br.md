# ADR-002: MQTT para Streaming de Telemetria de Entregadores (PT-BR)

> **Versão em Inglês**: [ADR-002](../adr-002-mqtt-for-telemetry.md)

---

## Status
Aceita

## Contexto
HTTP para streaming de coordenadas/status gerava overhead em larga escala. Era necessário um protocolo leve, bidirecional e confiável para logística em tempo real.

## Decisão
Adotar MQTT para ingestão de telemetria. Broker gerenciado/clusterizado; conexões seguras; estratégia de tópicos por região e entregador.

## Consequências
- **Positivas**: Menor consumo de rede/CPU, melhor escalabilidade de fan-in, semântica de push.
- **Negativas**: Nova superfície operacional (broker); governança de tópicos e estratégias de backpressure.

## Alternativas Consideradas
- Long-polling/HTTP streaming: mais pesado em dispositivos móveis.
- WebSockets: viável, porém mais pesado que MQTT em dispositivos restritos.

## Notas de Implementação
- TLS e autenticação; credenciais por dispositivo; tokens de curta duração.
- Hierarquia de tópicos: `/region/{id}/rider/{id}` com ACLs.
- Ponte MQTT → Kafka/Rabbit para consumidores downstream.
- Backpressure: buffer com TTL e descarte de telemetria obsoleta.

---
Atualização: 2025-10-30


