# Diretrizes de Engenharia: Plataforma de IA e Automação da Livelo

> **Versão em Inglês**: [Engineering Guidelines](../livelo-engineering-guidelines.md)

---

## Informações Básicas
- **ID da Diretriz**: EG-LIV-001
- **Projeto**: Stack de Automação e IA Livelo
- **Versão**: 1.0
- **Criação**: 30/10/2025
- **Atualização**: 30/10/2025
- **Autor**: GPT-5 Codex (com base em insights da liderança Livelo)
- **Aprovação**: *Pendente de validação pelo AI Board*

## Visão Geral

### Propósito
Definir guardrails unificados para squads que constroem agentes de IA e automações sobre Open WebUI + N8N + LiteLLM, garantindo governança, segurança e escala sem perder velocidade de entrega.

### Escopo
- Abrange agentes, automações e integrações orquestradas via N8N ou expostas no Open WebUI / Expert Livelo.
- Válida para engenheiros, especialistas em automação e colaboradores semi-técnicos autorizados.
- Aplica-se a experimentos em sandbox e a agentes em produção.

### Aplicabilidade
- Obrigatória para promover workflows de protótipo a produção.
- Recomendado aplicar desde a fase de descoberta para reduzir retrabalho.
- Documento exigido em aprovações do AI Board e revisões de segurança.

## Padrões de Código

### Convenções de Nomenclatura
- **Variáveis**: `lowerCamelCase` em TypeScript/JavaScript, `snake_case` em Python.
- **Funções**: formato `verboNome` (ex.: `calculateQuota`, `sanitize_prompt`).
- **Classes**: `PascalCase` em implementações TypeScript.
- **Constantes**: `UPPER_SNAKE_CASE` para valores imutáveis.
- **Arquivos**: nomes descritivos em kebab-case (ex.: `agent-budget-monitor.ts`).

### Estrutura de Código
- **Indentação**: 2 espaços (TS/JS), 4 espaços (Python).
- **Comprimento**: máximo 110 caracteres por linha.
- **Organização**: nodes customizados em `src/n8n/nodes/<dominio>`; utilitários compartilhados em `src/shared`.

### Comentários e Documentação
- **Comentários**: esclarecer regras de negócio, critérios de modelo e passos sensíveis.
- **Documentação de Funções**: registrar propósito, entradas, saídas e erros (JSDoc/docstring).
- **README**: cada repositório deve detalhar gatilhos, dependências, runbook e rollback.

## Arquitetura e Design

### Princípios Arquiteturais
- **Guardrail Primeiro**: orçamentos, escopo de acesso e plano de escalonamento definidos antes do go-live.
- **Observabilidade por Padrão**: tracing e logs de tokens desde a primeira versão.
- **Experimento Desacoplado**: protótipos permanecem em sandbox até aprovação formal.

### Padrões de Design
- **Orchestration Pattern**: usar N8N para coordenação de APIs, ramificações e retries.
- **Model Adapter Pattern**: encapsular chamadas em adaptadores LiteLLM com envelope padrão.
- **Audit Trail Pattern**: registrar metadados (inputs, outputs, modelo, tokens) para rastreabilidade.

### Estrutura de Projeto
```
project/
├── docs/
│   ├── architecture/
│   └── runbooks/
├── src/
│   ├── n8n/
│   ├── workers/
│   ├── shared/
│   └── tests/
├── helm/
├── .github/
└── README.md
```

## Boas Práticas de Desenvolvimento

### Versionamento
- **Branches**: GitFlow simplificado (feature → `develop` → `main`).
- **Commits**: Conventional Commits com referência ao ticket.
- **Tags**: marcar versões de workflows (ex.: `workflow-v1.4.0`).

### Testes
- **Unitários**: obrigatórios em nodes customizados (≥80% cobertura).
- **Integração**: simular chamadas de modelo com provedores mockados e checagem de orçamento.
- **E2E**: smoke tests para caminhos principal e de falha.
- **Cobertura**: mínimo 75% com foco em ramos e tratamento de erros.

### Performance
- **Otimização**: cache de RAG, tarefas assíncronas para cargas pesadas.
- **Profiling**: amostragem semanal de latência para agentes críticos.
- **Monitoramento**: métricas no Grafana; alertas para latência >2 s ou spike de tokens >30%.

## Segurança

### Princípios de Segurança
- **Autenticação**: VPN + SSO para usuários; tokens de curta duração para contas de serviço.
- **Autorização**: RBAC (Agent Owner, Reviewer, Observer) e budgets segregados.
- **Validação**: sanitizar prompts, remover metadados, validar JSON de saída.

### Práticas Seguras
- **Segredos**: armazenar no Secrets Manager; nunca versionar.
- **Tokens**: rotacionar credenciais trimestralmente; manter hashes para auditoria.
- **Dados Sensíveis**: mascarar antes de enviar ao LLM; usar vector store criptografado.

### Vulnerabilidades Comuns
- **Prompt Injection**: testes adversariais automatizados; listas de allow/deny.
- **Data Leakage**: pipelines de redação; DLP sobre uploads.
- **Supply Chain**: revisar dependências open-source; pinning de versões e SCA.

## Qualidade de Código

### Métricas
- **Complexidade Ciclomática**: <10 por função quando possível.
- **Duplicação**: <5% via reutilização de bibliotecas.
- **Índice de Manutenibilidade**: ≥75 no SonarQube.

### Ferramentas
- **Linter**: ESLint (TS) e Ruff (Python) com enforcement em CI.
- **SonarQube**: obrigatório em pull requests; bloqueio em issues críticas.
- **Code Review**: revisão por staff engineer ou steward para produção.

### Refatoração
- **Quando**: alertas do Sonar, findings do AI Board ou três ajustes consecutivos.
- **Como**: abrir ticket, criar testes de regressão, refatorar incrementalmente.
- **Testes**: executar suíte completa, incluindo rollback.

## Processo de Desenvolvimento

### Workflow
1. **Planejamento**: definir problema, budget, KPIs e dependências.
2. **Desenvolvimento**: construir em sandbox, seguir estratégia de branches, documentar.
3. **Testes**: rodar automações, dry-run em staging com dados sintéticos.
4. **Deploy**: promoção GitOps (Helm) com runbook e rollback anexados.

### Code Review
- **Critérios**: aderência às diretrizes, guardrails configurados, testes verdes, observabilidade ativa.
- **Processo**: reviewer clona branch, roda lint/testes, valida matriz de riscos.
- **Responsáveis**: autor documenta; reviewer avalia; steward assina.

### Deployment
- **Ambientes**: sandbox → staging → produção (conta isolada).
- **Pipeline**: GitHub Actions + ArgoCD com gates manuais.
- **Rollback**: manter chart anterior e snapshot do budget; rodar smoke test após rollback.

## Ferramentas e Tecnologias

### Obligatoriedade
- **IDE**: VS Code com extensão da plataforma.
- **Versionamento**: GitHub Enterprise.
- **CI/CD**: GitHub Actions + ArgoCD.

### Recomendado
- **Debug**: VS Code Remote Containers, `kubectl port-forward` para pods N8N.
- **Profiling**: Jaeger, coletores OpenTelemetry.
- **Monitoramento**: dashboards Grafana por agente.

### Configuração
- **Editor**: `.editorconfig` (espaços, encoding, newline).
- **Git**: commits assinados, hooks de pré-commit.
- **CI/CD**: segredos em cofres cifrados, variáveis por ambiente via sealed secrets.

## Documentação

### Técnica
- **API**: descrever gatilhos, entradas/saídas, rate limit e payloads exemplo.
- **Arquitetura**: atualizar diagramas a cada novo componente.
- **Deploy**: runbooks com health checks, rollback e contatos.

### Código
- **README**: visão geral, diagrama, pré-requisitos e instruções de deploy.
- **Comentários**: destacar regras críticas e integrações externas.
- **Changelog**: registrar data, autor, resumo e nível de risco.

### Processo
- **Onboarding**: playbook + trilha de aprendizagem N8N e prompt engineering.
- **Troubleshooting**: KB para falhas recorrentes (budget, timeout, alerta de injeção).
- **Incidentes**: root cause, mitigação e prevenção documentadas.

## Observabilidade e Monitoramento

### Métricas
- **Performance**: latência, taxa de sucesso, tamanho de fila, uso de tokens.
- **Erros**: falhas de workflow, erros de API, bloqueios de orçamento.
- **Uso**: usuários ativos, quantidade de prompts, throughput.

### Logs
- **Estrutura**: JSON com IDs de correlação, modelo, versão do workflow.
- **Níveis**: `debug`, `info`, `warn`, `error`, `critical` com semântica consistente.
- **Retenção**: 90 dias on-line, 12 meses cold storage.

### Alertas
- **Configuração**: Alertmanager com thresholds por criticidade.
- **Escalonamento**: on-call primário → engineer secundário → AI Board em issues sistêmicas.
- **Resposta**: seguir runbook; atualizações a cada 30 min até resolver.

## Incidentes e Troubleshooting

### Processo de Incidentes
1. **Detecção**: alertas automáticos ou chamados.
2. **Resposta**: reconhecer em 15 minutos; avaliar impacto.
3. **Resolução**: aplicar fix/rollback; validar budgets.
4. **Post-mortem**: completar em 48 horas; compartilhar com AI Board.

### Troubleshooting
- **Debug**: reproduzir com inputs sintéticos; analisar filas e respostas.
- **Logs**: buscar por ID; revisar quotas no LiteLLM.
- **Métricas**: relacionar spikes de tokens com adoção ou drift.

### Comunicação
- **Status**: canal #livelo-ai-operations; escalonar executivos em incidentes P1.
- **Updates**: 30 min (P1), 1 h (P2), resumo diário (P3).
- **Stakeholders**: segurança, compliance e product leads afetados.

## Treinamento e Desenvolvimento

### Onboarding
- **Novos Engenheiros**: módulos N8N, treinamento de segurança, exercício sandbox.
- **Documentação**: playbook + quick reference.
- **Mentoria**: staff engineer acompanha duas sprints.

### Desenvolvimento Contínuo
- **Treinamentos**: sessões mensais (prompt, custo, threat modelling).
- **Certificações**: incentivar AWS/GCP AI; monitorar adesão.
- **Conferências**: disseminar aprendizados de eventos.

### Gestão de Conhecimento
- **Compartilhamento**: comunidade de prática quinzenal com gravação.
- **Documentação**: centralizar em Confluence + repositório Docs.
- **Revisão**: revisões trimestrais de workflows críticos.

## Compliance e Auditoria

### Requisitos
- **LGPD**: classificar dados antes da ingestão; registrar base legal.
- **SOX**: manter evidências de aprovações e controle de custos.
- **ISO 27001**: garantir revisões de acesso e resposta a incidentes.

### Auditoria
- **Processo**: trilha de auditoria de deploys e consumo LiteLLM.
- **Documentos**: guardar aprovações, avaliações de risco, post-mortems.
- **Evidências**: exportar logs de budget, revisões de acesso e scans trimestrais.

### Segurança
- **Políticas**: aderência às normas corporativas; atualizar risk register.
- **Treinamento**: reciclagem anual obrigatória.
- **Incidentes**: reportar violações em até 24 horas.

## Aprovações

### Técnica
- **Nome**: *A designar* (Staff Engineer da plataforma)
- **Data**: *Pendente*
- **Notas**: Aguardando validação.

### Arquitetura
- **Nome**: *A designar* (Head de Arquitetura)
- **Data**: *Pendente*
- **Notas**: Revisão na próxima sessão do AI Board.

### Segurança
- **Nome**: *A designar* (Líder de Segurança)
- **Data**: *Pendente*
- **Notas**: Requer relatório de threat modelling.

---

**Revisão**: *Pendente*
**Status**: Draft

