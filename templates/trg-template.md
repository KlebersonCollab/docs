# Template: TRG (Technical Review Guide)

## 1. Informações Básicas
- **ID do TRG**: [TRG-XXX]
- **Nome do Projeto/Sistema**: [Nome do Projeto ou Sistema]
- **Versão**: [1.0]
- **Data de Criação**: [DD/MM/AAAA]
- **Última Atualização**: [DD/MM/AAAA]
- **Autor**: [Nome do Revisor Técnico]
- **Status**: [Rascunho/Em Revisão/Aprovado]

## 2. Visão Geral da Revisão

### Objetivo da Revisão
[Descrição do objetivo da revisão técnica e o que será avaliado]

### Escopo da Revisão
- **Componentes Incluídos**: [Lista dos componentes que serão revisados]
- **Componentes Excluídos**: [Lista dos componentes que NÃO serão revisados]
- **Período de Revisão**: [Data de início] - [Data de fim]

### Critérios de Revisão
- [Critério 1 de revisão]
- [Critério 2 de revisão]
- [Critério 3 de revisão]

## 3. Equipe de Revisão

### Revisores Técnicos
- **Revisor Principal**: [Nome e especialidade]
- **Revisor Secundário**: [Nome e especialidade]
- **Revisor de Segurança**: [Nome e especialidade]
- **Revisor de Performance**: [Nome e especialidade]

### Stakeholders
- **Product Owner**: [Nome]
- **Arquiteto**: [Nome]
- **Gerente de Projeto**: [Nome]
- **Desenvolvedor Líder**: [Nome]

## 4. Checklist de Revisão

### 4.1. Arquitetura e Design
- [ ] Arquitetura está alinhada com os requisitos
- [ ] Padrões arquiteturais foram seguidos
- [ ] Decisões arquiteturais estão documentadas (ADRs)
- [ ] Diagramas de arquitetura estão atualizados
- [ ] C4 Model está completo e atualizado

### 4.2. Código e Implementação
- [ ] Código segue os padrões estabelecidos
- [ ] Convenções de nomenclatura foram seguidas
- [ ] Comentários e documentação estão adequados
- [ ] Tratamento de erros está implementado
- [ ] Logs estão configurados adequadamente

### 4.3. Segurança
- [ ] Autenticação está implementada corretamente
- [ ] Autorização está configurada adequadamente
- [ ] Dados sensíveis estão protegidos
- [ ] Validação de entrada está implementada
- [ ] Headers de segurança estão configurados

### 4.4. Performance
- [ ] Consultas ao banco estão otimizadas
- [ ] Cache está implementado onde necessário
- [ ] Compressão está habilitada
- [ ] CDN está configurado adequadamente
- [ ] Métricas de performance estão sendo coletadas

### 4.5. Testes
- [ ] Testes unitários estão implementados
- [ ] Testes de integração estão funcionando
- [ ] Testes de performance foram executados
- [ ] Testes de segurança foram realizados
- [ ] Cobertura de testes está adequada

### 4.6. Documentação
- [ ] README está atualizado
- [ ] Documentação de API está completa
- [ ] Guias de instalação estão disponíveis
- [ ] Documentação de deploy está atualizada
- [ ] Troubleshooting está documentado

## 5. Análise Detalhada

### 5.1. Pontos Fortes
- [Ponto forte 1]: [Descrição e justificativa]
- [Ponto forte 2]: [Descrição e justificativa]
- [Ponto forte 3]: [Descrição e justificativa]

### 5.2. Pontos de Melhoria
- [Ponto de melhoria 1]: [Descrição e recomendação]
- [Ponto de melhoria 2]: [Descrição e recomendação]
- [Ponto de melhoria 3]: [Descrição e recomendação]

### 5.3. Riscos Identificados
- **Risco 1**: [Descrição do risco]
  - **Severidade**: [Alta/Média/Baixa]
  - **Probabilidade**: [Alta/Média/Baixa]
  - **Mitigação**: [Como mitigar o risco]
- **Risco 2**: [Descrição do risco]
  - **Severidade**: [Alta/Média/Baixa]
  - **Probabilidade**: [Alta/Média/Baixa]
  - **Mitigação**: [Como mitigar o risco]

### 5.4. Não Conformidades
- **NC-001**: [Descrição da não conformidade]
  - **Severidade**: [Crítica/Alta/Média/Baixa]
  - **Ação Corretiva**: [Ação necessária]
  - **Responsável**: [Nome do responsável]
  - **Prazo**: [Data limite]
- **NC-002**: [Descrição da não conformidade]
  - **Severidade**: [Crítica/Alta/Média/Baixa]
  - **Ação Corretiva**: [Ação necessária]
  - **Responsável**: [Nome do responsável]
  - **Prazo**: [Data limite]

## 6. Métricas e KPIs

### 6.1. Métricas de Qualidade
- **Cobertura de Testes**: [X]%
- **Complexidade Ciclomática**: [X]
- **Duplicação de Código**: [X]%
- **Débito Técnico**: [X] horas

### 6.2. Métricas de Performance
- **Tempo de Resposta**: [X]ms
- **Throughput**: [X] req/s
- **Uso de CPU**: [X]%
- **Uso de Memória**: [X]MB

### 6.3. Métricas de Segurança
- **Vulnerabilidades Críticas**: [X]
- **Vulnerabilidades Altas**: [X]
- **Vulnerabilidades Médias**: [X]
- **Vulnerabilidades Baixas**: [X]

## 7. Recomendações

### 7.1. Recomendações Imediatas
- [Recomendação 1]: [Descrição e justificativa]
- [Recomendação 2]: [Descrição e justificativa]
- [Recomendação 3]: [Descrição e justificativa]

### 7.2. Recomendações de Médio Prazo
- [Recomendação 1]: [Descrição e justificativa]
- [Recomendação 2]: [Descrição e justificativa]
- [Recomendação 3]: [Descrição e justificativa]

### 7.3. Recomendações de Longo Prazo
- [Recomendação 1]: [Descrição e justificativa]
- [Recomendação 2]: [Descrição e justificativa]
- [Recomendação 3]: [Descrição e justificativa]

## 8. Plano de Ação

### 8.1. Ações Imediatas (0-7 dias)
- **Ação 1**: [Descrição da ação]
  - **Responsável**: [Nome]
  - **Prazo**: [Data]
  - **Status**: [Pendente/Em Andamento/Concluído]
- **Ação 2**: [Descrição da ação]
  - **Responsável**: [Nome]
  - **Prazo**: [Data]
  - **Status**: [Pendente/Em Andamento/Concluído]

### 8.2. Ações de Curto Prazo (1-4 semanas)
- **Ação 1**: [Descrição da ação]
  - **Responsável**: [Nome]
  - **Prazo**: [Data]
  - **Status**: [Pendente/Em Andamento/Concluído]
- **Ação 2**: [Descrição da ação]
  - **Responsável**: [Nome]
  - **Prazo**: [Data]
  - **Status**: [Pendente/Em Andamento/Concluído]

### 8.3. Ações de Médio Prazo (1-3 meses)
- **Ação 1**: [Descrição da ação]
  - **Responsável**: [Nome]
  - **Prazo**: [Data]
  - **Status**: [Pendente/Em Andamento/Concluído]
- **Ação 2**: [Descrição da ação]
  - **Responsável**: [Nome]
  - **Prazo**: [Data]
  - **Status**: [Pendente/Em Andamento/Concluído]

## 9. Aprovações

### 9.1. Aprovação Técnica
- **Revisor Principal**: [Nome] - [Assinatura/Data]
- **Revisor de Segurança**: [Nome] - [Assinatura/Data]
- **Revisor de Performance**: [Nome] - [Assinatura/Data]

### 9.2. Aprovação de Negócio
- **Product Owner**: [Nome] - [Assinatura/Data]
- **Gerente de Projeto**: [Nome] - [Assinatura/Data]

### 9.3. Aprovação Final
- **Arquiteto**: [Nome] - [Assinatura/Data]
- **Desenvolvedor Líder**: [Nome] - [Assinatura/Data]

## 10. Próximos Passos

### 10.1. Ações Imediatas
- [Ação 1 que deve ser tomada imediatamente]
- [Ação 2 que deve ser tomada imediatamente]

### 10.2. Acompanhamento
- **Frequência**: [Semanal/Mensal/Trimestral]
- **Responsável**: [Nome do responsável pelo acompanhamento]
- **Métricas**: [Métricas que serão acompanhadas]

### 10.3. Próxima Revisão
- **Data Prevista**: [DD/MM/AAAA]
- **Escopo**: [O que será revisado na próxima vez]
- **Preparação**: [O que deve ser preparado]

---

**Referências**:
- [Link para ADRs relevantes]
- [Link para documentação de arquitetura]
- [Link para documentação de segurança]

**Histórico de Revisões**:
| Versão | Data | Autor | Descrição da Mudança |
|--------|------|-------|----------------------|
| 1.0    | DD/MM/AAAA | [Autor] | Criação inicial do TRG |
