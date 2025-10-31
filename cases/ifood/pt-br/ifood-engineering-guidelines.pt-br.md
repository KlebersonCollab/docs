# Diretrizes de Engenharia – Case iFood (PT-BR)

> **Versão em Inglês**: [Engineering Guidelines](../ifood-engineering-guidelines.md)

---

## Informações Básicas
- **ID**: EG-IFD-001
- **Projeto**: Plataforma iFood (Estudo de Caso)
- **Versão**: 1.0
- **Criação**: 2025-10-30
- **Atualização**: 2025-10-30
- **Aprovação**: (TBD)

## Propósito
Instituir práticas de engenharia orientadas à velocidade com guardrails para hiper-crescimento, refletindo lições do iFood.

## Escopo
Pedidos, restaurantes, pagamentos, logística e observabilidade; válido para protótipos, pilotos e produção.

## Aplicabilidade
- Obrigatório para mudanças rumo à produção.
- Recomendado na descoberta para reduzir retrabalho futuro.

## Padrões de Código
- **Nomes**: lowerCamelCase (TS/JS), snake_case (Python), PascalCase (classes), UPPER_SNAKE_CASE (consts).
- **Estrutura**: módulos pequenos; funções < 50 linhas quando possível; evitar objetos deus.
- **Docs**: JSDoc/docstrings; README por serviço com runbook/rollback.

## Arquitetura & Design
- **Strangler** na modernização do monólito.
- **Event-driven** para logística e efeitos.
- **Cache-first** em leituras pesadas (menus, disponibilidade).
- **Bulkheads/Timeouts** em integrações; retries com jitter.

## Workflow de Desenvolvimento
1. Planejar: problema, KPIs, guardrails (latência/erros/orçamento).
2. Construir: feature flags; dark launches; compatibilidade retroativa.
3. Testar: unit (≥80%), integração (mocks), e2e smoke.
4. Deploy: canary/blue-green via GitOps; rollback rápido.

## Versionamento
- Branches: feature/* → develop → main.
- Commits: Conventional Commits; vincular ticket.
- Tags: semver por serviço; imagens imutáveis.

## Observabilidade
- **Métricas**: P50/95/99, erro, lag de fila, frescor da telemetria, tempo de atribuição.
- **Logs**: JSON com IDs de correlação; redigir PII; sampling em pico.
- **Traces**: ponta a ponta em fluxos críticos.
- **Alertas**: baseados em SLO; runbooks; escalonamento claro.

## Segurança
- Segredos em cofre; zero em código.
- Menor privilégio para DB/mensageria.
- Auditoria de deploy e schema; 4-olhos para produção.

## Performance
- Orçamentos por endpoint; fail-fast em overload.
- Caches com TTL + eventos de invalidar.
- Pipelines assíncronos para compute/IO pesados (roteirização).

## Incidentes
- Canal de incidente; papéis (commander, comms, ops, scribe).
- Primeiro estabilizar (rate-limit/pausas regionais) e depois diagnosticar.
- Post-mortem em 48h; itens acompanhados.

## Refatoração
- Disparada por hotspots, incidentes frequentes ou dor de capacidade.
- Testes de regressão antes; migrar atrás de flag; remover legado após bake-in.

## Compliance & Risco
- Pilotos % com rótulo beta e kill-switch.
- Retenção por tipo de dado; revisões de acesso; DPIA quando houver PII.

---
Status: Rascunho


