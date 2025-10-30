# Plano de Governança de Dados: Stack de IA e Automação da Livelo

## 1. Informações Básicas
- **ID de Governança de Dados**: DG-LIV-001
- **Sistema**: Plataforma de IA & Automação Livelo
- **Versão**: 1.0
- **Criação**: 30/10/2025
- **Atualização**: 30/10/2025
- **Autor**: GPT-5 Codex (baseado na entrevista da liderança Livelo)
- **Status**: Rascunho

## 2. Visão Geral da Governança

### Objetivo
Garantir uso responsável, conforme e controlado de dados conversacionais e operacionais na plataforma N8N + Open WebUI + LiteLLM, definindo papéis, acesso, ciclo de vida e monitoramento.

### Escopo
- **Incluído**: Transcrições, logs de execução, corpora RAG (documentos/embeddings), transações de orçamento, métricas de observabilidade.
- **Excluído**: Dados transacionais legados de fidelidade, data lake de marketing (governado separadamente).
- **Período**: Desde 01/01/2024, com revisões trimestrais.

### Princípios
- **Isolamento por Design**: workloads de IA em conta segregada com egress controlado.
- **Accountability de Budget**: quotas pré-pagas por owner via LiteLLM.
- **Least Privilege**: acesso mínimo com VPN + SSO.
- **Auditabilidade**: rastrear prompts, outputs, modelos e gastos.

## 3. Estrutura Organizacional

### 3.1 Data Stewards
- **Principal**: Head de Arquitetura & Inovação (coordena roadmap, AI Board).
- **Negócio**: Product Leads do expert (alinhamento e consentimento).
- **Técnico**: Staff Engineer da plataforma (workflows, pipelines, acessos).
- **Segurança**: Líder de Segurança (sanitização, VPN, incidentes).

### 3.2 Data Owners
- **Dados Pessoais**: Chief Privacy Officer.
- **Dados Financeiros**: Diretor Financeiro.
- **Dados Operacionais**: Líder do COE de Automação.
- **Dados Estratégicos**: Diretor de Estratégia de IA.

### 3.3 Data Users
- **Negócio**: PMs e analistas jurídicos (dashboards read-only).
- **Técnicos**: Desenvolvedores e automadores (write controlado; ingestão RAG limitada).
- **Analíticos**: Cientistas de dados (datasets anonimizados).

## 4. Classificação de Dados

### 4.1 Dados Pessoais
- **Definição**: Conteúdos com identificadores de clientes ou colaboradores.
- **Exemplos**: Planos de viagem, resumos jurídicos.
- **Classificação**: Confidencial.
- **Retenção**: 180 dias; anonimização para analytics; deleção em 365 dias.
- **Acesso**: Revisores legais/compliance e serviços de anonimização.

### 4.2 Dados Financeiros
- **Definição**: Alocações, recargas e consumo LiteLLM.
- **Exemplos**: Livro de quotas, alertas financeiros.
- **Classificação**: Interno.
- **Retenção**: 3 anos.
- **Acesso**: Financeiro, stewards técnicos, auditores.

### 4.3 Dados Operacionais
- **Definição**: Definições de workflow, logs, métricas.
- **Exemplos**: Histórico N8N, séries Prometheus, traces de falha.
- **Classificação**: Interno.
- **Retenção**: 180 dias quente, 12 meses arquivado.
- **Acesso**: Engenharia de plataforma, plantão, observabilidade.

### 4.4 Dados Estratégicos
- **Definição**: Benchmarks de modelo, métricas de adoção, decisões do AI Board.
- **Exemplos**: Benchmarks de latência, dashboard de adoção, atas do board.
- **Classificação**: Confidencial.
- **Retenção**: 24 meses.
- **Acesso**: Liderança executiva e membros do board.

## 5. Políticas de Dados

### 5.1 Qualidade
- **Objetivo**: Manter bases de conhecimento atualizadas e métricas confiáveis.
- **Responsáveis**: Stewards validam ingestões; plataforma monitora sucesso dos workflows.
- **Métricas**: Atualização (<30 dias), taxa de sucesso (>98%), cobertura de anomalias.
- **Processo**: Revisões agendadas + linting automático.

### 5.2 Segurança
- **Objetivo**: Evitar vazamentos via interações de IA.
- **Responsáveis**: Security steward (VPN, WAF, sanitização de prompt).
- **Controles**: Validação de entrada, filtros de saída, acesso tokenizado, zero trust.
- **Processo**: Pentests trimestrais, monitoramento contínuo.

### 5.3 Privacidade
- **Objetivo**: Garantir aderência a LGPD/GDPR.
- **Responsáveis**: Escritório de privacidade para consentimento; stewards de negócio para anonimização.
- **Controles**: Minimização, flags de consentimento, fluxos de deleção, DPIA.
- **Processo**: Auditoria mensal de transcrições; deleção automatizada com revisão humana.

### 5.4 Retenção
- **Objetivo**: Definir tempos de guarda equilibrando compliance e analytics.
- **Responsáveis**: Data owners definem; plataforma implementa.
- **Períodos**: Pessoais (180/365), Financeiros (3 anos), Operacionais (180+12m), Estratégicos (24m).
- **Processo**: Jobs agendados com logs de auditoria; alertas para violações.

## 6. Controles

### 6.1 Acesso
- **Autenticação**: VPN + SSO; tokens de curta duração.
- **Autorização**: Roles por persona; stores RAG segmentados.
- **Auditoria**: Revisão mensal de acessos.
- **Recertificação**: Trimestral com revogação de inativos.

### 6.2 Integridade
- **Validação**: Schemas em uploads, antivírus.
- **Verificação**: Checksums de embeddings, conciliação de metadados.
- **Backup**: Snapshots diários de vector stores e bancos operacionais.
- **Recuperação**: DR com RTO de 4 horas.

### 6.3 Confidencialidade
- **Criptografia**: TLS em trânsito, KMS em repouso.
- **Mascaramento**: Redação automática antes do envio ao LLM.
- **Anonimização**: Tokenização para analytics.
- **Pseudonimização**: Tokens únicos para depuração segura.

## 7. Processos

### 7.1 Aprovação de Acesso
1. Solicitação via catálogo com justificativa e duração.
2. Análise do data steward.
3. Aprovação pelo data owner e revisão de segurança.
4. Implementação pelo time de plataforma.
5. Monitoramento semanal e expiração automática.

### 7.2 Qualidade de Dados
1. Identificação por alertas ou feedback.
2. Análise do steward técnico.
3. Correção (knowledge base/workflow/ingestão).
4. Validação com regressões.
5. Monitoramento contínuo e escalonamento ao AI Board se recorrente.

### 7.3 Incidentes
1. Detecção (segurança, DLP ou usuário).
2. Análise pelo time de resposta.
3. Contenção, revogação de acessos, notificação.
4. Recuperação com restauração de dados limpos.
5. Lições aprendidas e atualização de controles.

## 8. Métricas e KPIs

### 8.1 Qualidade
- **Completude**: ≥95% dos metadados obrigatórios.
- **Acurácia**: ≥97% em auditorias de respostas.
- **Consistência**: <2% de respostas conflitantes/mês.
- **Validade**: 100% de compliance de schema.

### 8.2 Segurança
- **Incidentes**: ≤1 por trimestre.
- **Violações de Acesso**: 0 críticas.
- **Tempo de Resposta**: <30 minutos para alertas severos.
- **Taxa de Resolução**: ≥95% dentro do SLA.

### 8.3 Conformidade
- **LGPD**: ≥98% com base legal registrada.
- **Auditorias**: 100% aprovadas.
- **Não Conformidades**: ≤2 leves por ciclo.
- **Retenção**: 0 violações pendentes/mês.

## 9. Conformidade

### 9.1 LGPD
- **Status**: Amplamente aderente.
- **Requisitos**: Consentimento, minimização, atendimento a direitos.
- **Gaps**: Automação de DSAR em andamento.
- **Plano**: Concluir automação até Q1/2026; ampliar anonimização.

### 9.2 GDPR
- **Status**: Parcial para clientes internacionais.
- **Requisitos**: Residência de dados, consentimento explícito.
- **Gaps**: Estratégia de residência em avaliação.
- **Plano**: Estudar hospedagem na UE; formalizar contratos.

### 9.3 Outros
- **SOX**: Logs de budget revisados trimestralmente pelo financeiro.
- **PCI DSS**: Não aplicável.
- **ISO 27001**: Controles mapeados; evidências em repositório.

## 10. Ferramentas

### Governança
- **Catálogo**: Confluence + Docs com tagging.
- **Lineage**: Metadados do N8N + histórico Git.
- **Qualidade**: Linting, scripts QA, observabilidade.
- **Segurança**: IAM, security groups, gateway VPN.

### Monitoramento
- **Dados**: Prometheus e painéis Grafana.
- **Acesso**: CloudTrail/Audit Logs + SIEM.
- **Compliance**: Checadores de retenção, alertas de budget.
- **Performance**: Traces Jaeger, analytics de tokens.

### Analytics
- **Data Analytics**: Workspace SQL com datasets anonimizados.
- **BI**: Looker/Tableau.
- **ML**: Scripts LiteLLM, notebooks Python.
- **Data Science**: JupyterHub em ambiente seguro.

## 11. Treinamento

### Stewards
- **Conteúdo**: Framework, exercícios de incidente, ferramentas de retenção.
- **Frequência**: Trimestral.
- **Responsável**: Data steward principal.
- **Certificação**: Recertificação anual.

### Usuários
- **Conteúdo**: Uso seguro de Open WebUI/N8N, privacidade.
- **Frequência**: Onboarding + reciclagem semestral.
- **Responsável**: Time de enablement.
- **Certificação**: Quiz + exercício prático.

### Segurança
- **Conteúdo**: Injeção de prompt, prevenção de vazamento, reporte de incidentes.
- **Frequência**: Anual obrigatória.
- **Responsável**: Security steward.
- **Certificação**: Registro em LMS.

## 12. Plano de Implementação

### Fase 1 – Preparação (0-1 mês)
- **Atividade**: Inventário e classificação.
- **Responsável**: Steward técnico.
- **Prazo**: 30/11/2025.
- **Entregas**: Documento de inventário, matriz de acesso.

### Fase 2 – Implementação (1-3 meses)
- **Atividade**: Deploy de rotinas de retenção e revisão de acesso.
- **Responsável**: Engenharia de plataforma.
- **Prazo**: 31/01/2026.
- **Entregas**: Jobs agendados, dashboards, alertas.

### Fase 3 – Operação (3-6 meses)
- **Atividade**: Cerimônias de governança, auditorias, evolução de guardrails.
- **Responsável**: AI Board + stewards.
- **Prazo**: Contínuo; primeira revisão 31/03/2026.
- **Entregas**: Relatório trimestral, métricas de incidentes, status de compliance.

## 13. Aprovações

### Técnica
- **Data Steward**: *Pendente*
- **Arquiteto de Dados**: *Pendente*
- **CISO**: *Pendente*

### Negócio
- **Data Owner**: *Pendente*
- **Gerente de Projeto**: *Pendente*

### Final
- **Diretor de TI**: *Pendente*
- **Compliance Officer**: *Pendente*

## 14. Próximos Passos

### Ações Imediatas
- Agendar primeira revisão de governança com AI Board.
- Priorização da automação DSAR.

### Acompanhamento
- **Frequência**: Trimestral.
- **Responsável**: Data steward principal.
- **Métricas**: Taxa de compliance, variação de custos, aderência de retenção.

### Próxima Revisão
- **Data**: 15/01/2026.
- **Escopo**: Avaliar automação de retenção e gaps LGPD.
- **Preparação**: Evidências de auditoria e sumário de incidentes.

---

**Referências**:
- Arquitetura de Alto Nível Livelo (versão PT-BR).
- Políticas corporativas de segurança.
- Documentação LiteLLM.

| Versão | Data       | Autor       | Descrição |
|--------|------------|-------------|-----------|
| 1.0    | 30/10/2025 | GPT-5 Codex | Criação   |

