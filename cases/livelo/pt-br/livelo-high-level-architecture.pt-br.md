# Plataforma de IA da Livelo - Arquitetura de Alto Nível

## Visão Geral
A Livelo opera uma plataforma corporativa de IA e automação que combina interfaces conversacionais, orquestração low-code e controle rigoroso de consumo de modelos. A plataforma sustenta três pilares estratégicos:

- **Expert voltado ao cliente** que oferece planejamento de viagens e otimização de pontos.
- **Agentes de IA internos** que aceleram fluxos jurídicos, de engenharia e de negócio.
- **Centro de excelência em automação** que torna processos de backoffice mais eficientes.

A arquitetura prioriza experimentação rápida com governança rígida, permitindo provar valor rapidamente sem abrir mão de escala, segurança e conformidade.

## Objetivos Arquiteturais
- **Performance**: Respostas em tempo real ou quase real para agentes conversacionais (<2 segundos para prompts padrão) com tratamento assíncrono para rotinas mais pesadas.
- **Escalabilidade**: Escalonamento horizontal via Kubernetes para pods N8N e Open WebUI; fan-out dinâmico dos fluxos de agentes para absorver picos de demanda.
- **Disponibilidade**: Meta de 99,5% de uptime para agentes internos e 99,9% para o expert voltado ao cliente, com redundância entre clusters.
- **Segurança**: Conta isolada na nuvem, acesso exclusivo por VPN, guardrails dedicados e sanitização de prompts para mitigar injeção e vazamento de dados.
- **Manutenibilidade**: Workflows modulares, definições declarativas de agentes e linting automatizado facilitam evolução contínua e entendimento compartilhado.

## Componentes Principais

### Open WebUI
- **Responsabilidade**: Oferecer interface conversacional unificada para uso interno, com extensões de slash commands para upload de conhecimento.
- **Tecnologia**: Open WebUI autogerenciado em Kubernetes; integração com SSO corporativo via VPN.
- **Interfaces**: WebSockets para chat, hooks REST para o N8N, comandos para pipelines de ingestão RAG.
- **Dependências**: Endpoints de workflows N8N, gateway de autenticação.

### Expert Livelo Chat
- **Responsabilidade**: Experiência conversacional para clientes, entregando planejamento de pontos e itinerários.
- **Tecnologia**: Clientes web e mobile que chamam adaptadores serverless roteados para agentes no N8N.
- **Interfaces**: APIs REST e respostas em streaming.
- **Dependências**: Orquestração N8N, catálogo de agentes, stack de observabilidade.

### Orquestrador N8N
- **Responsabilidade**: Motor central de workflows para agentes de IA, rotinas de automação e integrações multietapas.
- **Tecnologia**: N8N open-source em Kubernetes com pods autoscaling.
- **Interfaces**: REST, webhooks e processadores de filas.
- **Dependências**: LiteLLM, repositórios de conhecimento, Git, APIs externas.

### Gestor de Orçamentos LiteLLM
- **Responsabilidade**: Controlar consumo de tokens com saldo pré-pago por área, prevenindo custos inesperados e reforçando accountability.
- **Tecnologia**: LiteLLM com rotinas personalizadas de budget; integração com sistemas financeiros corporativos.
- **Interfaces**: REST para checagens de quota, eventos para alertas de saldo baixo.
- **Dependências**: Contabilidade, serviços de notificação, observabilidade.

### Abstração de Provedores de Modelos
- **Responsabilidade**: Roteamento de prompts para o melhor modelo disponível (OpenAI, Google Gemini, Anthropic Claude via Bedrock, etc.).
- **Tecnologia**: Adaptadores LiteLLM, conectores N8N, wrappers específicos de SDK.
- **Interfaces**: APIs padronizadas de prompt e camada de normalização de respostas.
- **Dependências**: Credenciais de provedores, dashboards de latência, estratégias de fallback.

### Camada de Conhecimento e RAG
- **Responsabilidade**: Gerir corpora privados (PDFs, políticas, processos) ingeridos via slash commands e convertidos em embeddings.
- **Tecnologia**: Pipelines N8N, vector store dedicado, políticas de acesso via LiteLLM.
- **Interfaces**: Upload de documentos, API de retrieval, endpoints de busca.
- **Dependências**: Buckets de armazenamento, antivírus, catálogo de metadados.

### Stack de Observabilidade
- **Responsabilidade**: Fornecer tracing, logging e métricas por execução, incluindo uso de tokens e taxa de sucesso.
- **Tecnologia**: Prometheus/Grafana, logging centralizado, plug-ins de tracing.
- **Interfaces**: Exporters de métricas, coletores OpenTelemetry, dashboards.
- **Dependências**: Kubernetes, eventos do LiteLLM, hooks Git.

### Controles de Segurança
- **Responsabilidade**: Impor acesso exclusivamente por VPN, sanitização de prompts, guardrails contra injeção e ambientes segregados.
- **Tecnologia**: Conta dedicada, políticas IAM, regras WAF, rotação de segredos.
- **Interfaces**: IAM, ACLs de rede, pontos de aplicação de políticas.
- **Dependências**: IdP corporativo, ferramentas de compliance, SOC.

## Padrões Arquiteturais

### Padrão 1: Orquestração Low-Code para Pipelines de Agentes
- **Descrição**: Modelar workflows de IA graficamente no N8N, permitindo colaboração de engenheiros e perfis semide técnicos.
- **Aplicação**: Agentes internos, expert ao cliente, centro de excelência.
- **Benefícios**: Iteração ágil, conhecimento compartilhado, conectores reutilizáveis, barreira reduzida.
- **Trade-offs**: Exige governança robusta para evitar sobrecarga do orquestrador; limitações para workloads transacionais intensas.

### Padrão 2: Roteamento Multi-cloud com Enforcement de Orçamento
- **Descrição**: Abstrair provedores de modelos e atrelar cada chamada a uma verificação de quota.
- **Aplicação**: Todas as invocações de agentes passam pelo LiteLLM.
- **Benefícios**: Transparência de custos, facilidade para trocar modelos, diversificação de fornecedores.
- **Trade-offs**: Latência adicional nas checagens; necessidade de conciliação financeira.

## Decisões Arquiteturais

### Decisão 1: Adotar N8N em vez de Microsserviços Sob Medida
- **Contexto**: Necessidade de prototipagem rápida e empoderamento de perfis não tradicionais.
- **Decisão**: Padronizar o N8N com Kubernetes e políticas compartilhadas.
- **Consequências**: Onboarding simplificado, tooling consistente, reutilização de conectores; workloads intensivos devem permanecer fora.
- **Alternativas**: Microsserviços dedicados (delivery mais lento), plataformas no-code SaaS (lock-in, governança limitada).

### Decisão 2: Usar LiteLLM com Orçamentos Pré-pagos por Agente
- **Contexto**: Evitar estouros de custo e estimular gestão descentralizada.
- **Decisão**: Orçamento obrigatório por agente e alertas de saldo baixo.
- **Consequências**: Zero risco de faturas inesperadas, accountability clara; precisa de processo de recarga junto ao financeiro.
- **Alternativas**: Tetos mensais centralizados (menos granular), dashboards reativos (sem bloqueio pró-ativo).

### Decisão 3: Operar em Conta Segregada com Acesso por VPN
- **Contexto**: Guardrails de IA, contenção de risco, compliance.
- **Decisão**: Hospedar Open WebUI, N8N e LiteLLM em conta restrita e sem egress público.
- **Consequências**: Contenção forte, auditorias facilitadas; mais esforço para integrações cross-account.
- **Alternativas**: Conta corporativa compartilhada (blast radius maior), SaaS gerenciado (menor controle, risco regulatório).

## Qualidades do Sistema

### Performance
- **Métricas**: Latência (<2 s), consumo de tokens por execução, throughput por agente.
- **Estratégias**: Autoscaling, cache de respostas RAG, filas assíncronas.
- **Monitoramento**: Dashboards Prometheus, telemetria do LiteLLM, alertas para workflows lentos.

### Escalabilidade
- **Estratégias**: Autoscaling horizontal, execuções stateless, conectores desacoplados.
- **Horizontal**: Escalar pods N8N e workers.
- **Vertical**: Ajustes temporários de CPU/memória em jobs de embedding.

### Disponibilidade
- **SLA**: 99,5% interno, 99,9% externo.
- **Estratégias**: Clusters multi-zona, failover automatizado, nós reserva.
- **Recuperação**: Redeploy GitOps, playbooks para restaurar RAG e budgets.

### Segurança
- **Autenticação**: VPN + SSO para funcionários; identidade Livelo para clientes.
- **Autorização**: Perfis segregados (owner, reviewer, observer).
- **Criptografia**: TLS na borda, dados e embeddings criptografados em repouso.

## Stack Tecnológica

### Frontend
- **Framework**: Open WebUI com extensões customizadas.
- **Linguagem**: TypeScript para widgets, React para canais do cliente.
- **Ferramentas**: Integrações com design system corporativo, validadores de acessibilidade.

### Backend
- **Framework**: Workflows N8N, nodes em Python/TypeScript, adaptadores serverless.
- **Linguagem**: TypeScript, Python, Bash.
- **APIs**: REST, GraphQL (planejado), webhooks.

### Banco de Dados
- **Tipo**: Vector store para RAG, Postgres para metadados operacionais, storage de objetos para documentos.
- **Estratégias**: Escaneamento de malware, tagging de metadados, versionamento.

### Infraestrutura
- **Cloud**: AWS e GCP (modelos e workloads); conta sandbox dedicada.
- **Containerização**: Docker para Open WebUI e N8N.
- **Orquestração**: Kubernetes com pipelines GitOps.

## Riscos Arquiteturais

### Risco 1: Crescimento Descontrolado de Workflows sobrecarrega o N8N
- **Impacto**: Alto.
- **Probabilidade**: Média.
- **Mitigação**: Aprovações do AI Board, linting, políticas de guardrail, classificação de workloads.

### Risco 2: Injeção de Prompt ou Vazamento de Dados
- **Impacto**: Crítico.
- **Probabilidade**: Média.
- **Mitigação**: Sanitização, execução sandbox, stores segregados, testes de segurança contínuos.

### Risco 3: Dependência de Fornecedor ou Regressão de Performance
- **Impacto**: Médio.
- **Probabilidade**: Média.
- **Mitigação**: Abstração multi-cloud, benchmarks contínuos, modelos de fallback, escalonamento de suporte.

---

**Última atualização**: 30/10/2025
**Fonte**: Entrevista da Livelo no podcast PPT Não Compila.

