# Governança de Dados – Case iFood (PT-BR)

> **Versão em Inglês**: [Data Governance](../ifood-data-governance.md)

---

## 1. Informações Básicas
- **ID**: DG-IFD-001
- **Projeto**: Plataforma iFood (Estudo de Caso)
- **Versão**: 1.0
- **Criação**: 2025-10-30
- **Atualização**: 2025-10-30
- **Status**: Rascunho

## 2. Visão de Governança
- **Objetivo**: Habilitar experimentação rápida (pilotos) com contenção de risco operacional e reputacional.
- **Escopo (Incluído)**: Dados operacionais (pedidos/restaurantes/pagamentos), telemetria de logística (localização/status), observabilidade.
- **Escopo (Excluído)**: Backoffice não operacional (governado fora deste plano).
- **Princípios**: Piloto-first, contenção de risco, menor privilégio, auditabilidade, privacy-by-design.

## 3. Organização
- **Steward Técnico**: Plataforma/SRE (telemetria, observabilidade, acessos).
- **Steward de Negócio**: Produtos (regras de domínio, percentuais de rollout).
- **Segurança**: Líder de Segurança (segredos, IAM, incidentes).
- **Privacidade**: DPO/PO (PII: redação, retenção, DSARs).

## 4. Classificação
- **Operacional**: pedidos/estados/eventos → Interno; retenção conforme negócio/lei.
- **Telemetria**: localização/status de entregadores → Confidencial; retenção curta; anonimização p/ analytics.
- **Financeiro**: pagamentos/liquidações → Interno/Confidencial; retenções mais longas.
- **Observabilidade**: métricas/logs/traces → Interno; PII sempre redigida.

## 5. Políticas
- **Qualidade**: versionar esquemas; contratos de eventos; validação automatizada.
- **Segurança**: segredos em cofre; IAM por função; acesso de produção via break-glass auditado.
- **Privacidade**: minimizar PII em telemetria/logs; pseudonimização para analytics.
- **Retenção**: SLAs por tipo (ex.: telemetria 30–90 dias quente; frio apenas se justificado).

## 6. Controles
- **Acesso**: VPN/SSO; RBAC; revisão mensal de acessos.
- **Integridade**: checksums; registry de schema; logs imutáveis.
- **Confidencialidade**: TLS; criptografia em repouso; pipelines de redação.

## 7. Processos
- **Pilotos**: coortes 1–5% rotuladas beta; A/B; promoção com gates.
- **Incidentes**: detectar → conter (pausas regionais/rate-limit) → recuperar → post-mortem.
- **Mudança**: GitOps; aprovações; migrações rastreáveis.

## 8. Métricas
- **Qualidade**: conformidade de schema ≥99,5%; consistência de estados ≥99,9%.
- **Segurança**: 0 exposições críticas; rotação < 24h.
- **Privacidade**: 0 vazamentos PII abertos; DSAR 100% no SLA.
- **Operação**: frescor de telemetria P95 < 5s; atribuição P95 dentro da meta.

## 9. Conformidade
- Mapear fluxos; DPIA para novas utilizações de telemetria.
- Trilhas de auditoria de deploy, acesso e rotinas de retenção.

## 10. Ferramentas
- Registry/lineage de eventos, DLP/redação, SIEM, suite de observabilidade.

## 11. Plano
- Fase 1: classificação/retensão; redação automatizada.
- Fase 2: IAM/least-privilege; revisões de acesso automáticas.
- Fase 3: gates de piloto; dashboards de telemetria/atribuição.

---
Responsável: Steward Técnico


