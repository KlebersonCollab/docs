# Caso de Uso: Revisor de Pull Request com IA

## Informações Básicas
- **ID**: UC-LIV-001
- **Nome**: Revisão de Qualidade em Pull Requests com IA
- **Versão**: 1.0
- **Criação**: 30/10/2025
- **Atualização**: 30/10/2025
- **Autor**: GPT-5 Codex (com base na entrevista com a engenharia Livelo)

## Descrição
Automatizar a revisão de pull requests invocando um agente de IA via N8N para analisar diffs, aplicar padrões de código, identificar problemas de segurança e sugerir correções antes da aprovação humana. O agente reduz o tempo de revisão e reforça os guardrails da plataforma de IA da Livelo.

## Atores

### Primários
- **Desenvolvedor**: abre/atualiza o PR e consome o feedback da IA.
- **Agente Revisor**: workflow N8N que chama o LiteLLM com prompts contextualizados e conhecimento do repositório.

### Secundários
- **Revisor Humano**: valida achados da IA e aprova ou rejeita o PR.
- **Steward da Plataforma**: mantém guardrails, monitora desempenho e ajusta prompts.

## Pré-condições
- Repositório configurado com webhook N8N e integração GitHub/GitLab.
- Budget LiteLLM disponível para a squad responsável.
- Padrões de código e políticas de segurança documentados.

## Pós-condições
- PR anotado com achados, severidade e sugestões da IA.
- Débito do orçamento registrado no ledger LiteLLM.
- Métricas de observabilidade atualizadas (latência, tokens, feedback).

## Fluxo Principal

### Passo 1
**Ação do Ator**: Desenvolvedor abre ou atualiza o PR.
**Resposta do Sistema**: Plataforma Git aciona webhook para o N8N com metadados e diff.

### Passo 2
**Ação do Ator**: N8N enriquece contexto (padrões, histórico).
**Resposta do Sistema**: Workflow sanitiza payload, checa budget e prepara prompt.

### Passo 3
**Ação do Ator**: Agente envia prompt ao LLM escolhido (Claude, Gemini, etc.).
**Resposta do Sistema**: Modelo retorna JSON estruturado com achados e confiança.

### Passo 4
**Ação do Ator**: Workflow valida schema e mapeia achados aos guias do repositório.
**Resposta do Sistema**: Comentários adicionados ao PR; resumo anexado à descrição.

### Passo 5
**Ação do Ator**: Desenvolvedor corrige e atualiza PR.
**Resposta do Sistema**: Workflow reexecuta até resolver achados ou reviewer dispensar.

## Fluxos Alternativos

### A: Orçamento Esgotado
**Condição**: Checagem de quota falha.
**Passos**:
1. Workflow comenta no PR e marca Agent Owner.
2. Alerta ao financeiro para recarga.
3. Revisor humano conduz revisão enquanto orçamento é restabelecido.

### B: Resposta com Baixa Confiança
**Condição**: Score < limiar (ex.: 0,6).
**Passos**:
1. Workflow tenta modelo fallback.
2. Persistindo baixa confiança, adiciona label `needs-human-analysis`.
3. Revisor humano avalia e registra outcome para feedback.

## Fluxos de Exceção

### A: Injeção de Prompt Detectada
**Condição**: Análise estática identifica instruções maliciosas.
**Tratamento**:
1. Abort ar workflow e aplicar label `security-alert`.
2. Notificar segurança e steward.
3. Exigir revisão de segurança manual.

### B: Falha de Validação de Schema
**Condição**: Resposta fora do schema esperado.
**Tratamento**:
1. Log com snapshot (sanitizado).
2. Retry com prompt mais restrito.
3. Persistindo falha, escalar para revisão humana e registrar para ajuste futuro.

## Regras de Negócio

### Regra 1
- **Descrição**: Repositórios rumo à produção devem habilitar revisão com IA antes da aprovação humana.
- **Aplicação**: Proteções de branch bloqueiam merge sem execução do agente.

### Regra 2
- **Descrição**: Achados `critical` requerem acknowledgment humano mesmo após correção.
- **Aplicação**: PR só é liberado após confirmação do revisor.

### Regra 3
- **Descrição**: Alertas de saldo LiteLLM disparam quando restar 20% de créditos.
- **Aplicação**: Garante recarga proativa e evita parada do agente.

## Protótipos / Mockups
- Tela principal exibe resumo e comentários da IA, além de badge `AI Review`.
- Painéis complementares mostram volume de revisões, tempo médio e consumo de tokens.

## Requisitos Não Funcionais

### Performance
- Tempo alvo: <60 s para diffs pequenos/médios.
- Concorrência: mínimo 20 PRs simultâneos sem backlog.

### Segurança
- Sanitização de prompts e escaping de diffs antes do LLM.
- Workflow restrito ao escopo do repositório; sem acesso a segredos.

### Usabilidade
- Comentários devem ser acionáveis, com snippets e sugestões claras.
- Permitir feedback (positivo/negativo) para melhorar prompts.

## Dependências
- **Workflows N8N** (orquestração).
- **Serviço LiteLLM** (budget e logging).
- **Stack de Observabilidade** (métricas e traces).

## Cenários de Teste

### Cenário 1
- **Objetivo**: Confirmar alerta de risco SQL injection.
- **Entrada**: PR com concatenação insegura.
- **Resultado Esperado**: Comentário apontando vulnerabilidade e correção.

### Cenário 2
- **Objetivo**: Verificar comportamento em diffs grandes.
- **Entrada**: PR com >500 linhas alteradas.
- **Resultado Esperado**: Execução dentro do SLA ou sinalização para revisão humana.

## Notas de Implementação

### Considerações Técnicas
- Utilizar streaming quando disponível para reduzir latência aparente.
- Armazenar prompts/respostas anonimizados para melhoria contínua.
- Permitir configuração por repositório (pesos, limiares).

### Riscos
- **Falsos Positivos** → Mitigação: coletar feedback e ajustar prompts semanalmente.
- **Drift de Modelo** → Mitigação: benchmarking mensal e fallback automático.

### Estimativas
- **Complexidade**: Média.
- **Esforço**: ~3 semanas de engenharia (implementação + staging).
- **Prioridade**: Alta (impacto direto em produtividade).

---

**Revisão**: *Pendente*
**Aprovação**: *Pendente*
**Status**: Draft

