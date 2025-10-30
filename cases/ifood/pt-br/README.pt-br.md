# Pacote de Conhecimento do Case iFood (PT-BR)

## Propósito
Consolidar aprendizados da história do iFood em artefatos acionáveis alinhados aos templates: arquitetura, diretrizes de engenharia, governança de dados, casos de uso e decisões arquiteturais.

## Inventário de Documentos
- `ifood-high-level-architecture.pt-br.md`: Visão ponta a ponta da evolução da plataforma (monólito + Oracle → microsserviços + Postgres + cloud) e logística em tempo real (MQTT, clusterização, roteirização).
- `ifood-engineering-guidelines.pt-br.md`: Velocidade com guardrails, squads, incidentes, observabilidade e refatoração pragmática.
- `ifood-data-governance.pt-br.md`: Pilotos, ambidestria (labs vs core), contenção de risco e estratégias de rollout por percentual.
- `uc-ifd-001-realtime-logistics-optimizer.pt-br.md`: Orquestração de frota em tempo real: telemetria, clusterização e roteirização.
- `adr-001-database-modernization.pt-br.md`: Modernização Oracle → Postgres em microsserviços.
- `adr-002-mqtt-for-telemetry.pt-br.md`: Adoção de MQTT para telemetria leve de localização.

## Como Usar
1. Comece pela arquitetura para entender limites de componentes e evolução.
2. Aplique as diretrizes para equilibrar velocidade e escala.
3. Use a governança para pilotos seguros e mitigação de risco reputacional.
4. Reaproveite o caso de uso e os ADRs ao projetar logística em tempo real ou modernizações.

---

Mantenedor: Skynet Docs  
Atualização: 2025-10-30

