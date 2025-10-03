# Documentação de Reuniões - Ciclo de Vida do Software

## 🎯 Objetivo

Este documento define os tipos de reuniões necessárias ao longo do ciclo de vida do software, seus inputs, outputs e instruções claras para IAs gerarem as documentações necessárias baseadas nas transcrições das reuniões.

## 📋 Tipos de Reuniões por Fase

### Fase 1: Ideação e Planejamento

#### 1.1. Reunião de Brainstorming
**Objetivo**: Capturar ideias iniciais e definir conceito do produto
**Duração**: 2-4 horas
**Participantes**: Stakeholders, Product Owner, Equipe de Desenvolvimento

**Inputs**:
- Problema a ser resolvido
- Objetivos de negócio
- Restrições conhecidas
- Ideias iniciais

**Outputs Esperados**:
- Lista de ideias priorizadas
- Conceito inicial do produto
- Objetivos de alto nível

**Instruções para IA**:
- Extrair ideias principais da transcrição
- Identificar objetivos de negócio
- Listar restrições mencionadas
- Priorizar ideias por impacto/viabilidade
- Preparar para próxima reunião (PRD)

---

#### 1.2. Reunião de Definição de Requisitos (PRD)
**Objetivo**: Definir produto e objetivos de alto nível
**Duração**: 4-6 horas
**Participantes**: Product Owner, Stakeholders, Equipe de Desenvolvimento

**Inputs**:
- Resultados do Brainstorming
- Objetivos de negócio
- Público-alvo
- Restrições de negócio

**Outputs Esperados**:
- **PRD (Product Requirements Document)**
- Visão clara do produto
- Objetivos e métricas de sucesso
- Restrições e premissas

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Objetivo do produto
   - Público-alvo e personas
   - Requisitos funcionais de alto nível
   - Requisitos não funcionais
   - Restrições de negócio
   - Cronograma e recursos

2. **Gerar PRD** usando `prd-template.md`:
   - Preencher todas as seções obrigatórias
   - Incluir objetivos SMART
   - Definir métricas de sucesso
   - Listar restrições e premissas

3. **Próximos passos**:
   - Sugerir criação de FRD
   - Sugerir criação de TRD
   - Agendar reunião de arquitetura

---

#### 1.3. Reunião de Requisitos Funcionais (FRD)
**Objetivo**: Detalhar funcionalidades do sistema
**Duração**: 6-8 horas
**Participantes**: Product Owner, Analistas, Desenvolvedores, QA

**Inputs**:
- PRD aprovado
- Requisitos de negócio
- Casos de uso identificados

**Outputs Esperados**:
- **FRD (Functional Requirements Document)**
- Funcionalidades detalhadas
- Fluxos de processo
- Regras de negócio

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Funcionalidades principais
   - Fluxos de processo
   - Regras de negócio
   - Casos de uso
   - Pré-condições e pós-condições

2. **Gerar FRD** usando `frd-template.md`:
   - Detalhar cada funcionalidade
   - Mapear fluxos principais e alternativos
   - Documentar regras de negócio
   - Incluir critérios de aceite

3. **Próximos passos**:
   - Sugerir criação de TRD
   - Sugerir criação de User Stories
   - Agendar reunião de arquitetura

---

#### 1.4. Reunião de Requisitos Técnicos (TRD)
**Objetivo**: Especificar APIs e integrações técnicas
**Duração**: 4-6 horas
**Participantes**: Arquitetos, Desenvolvedores, DevOps, Integradores

**Inputs**:
- FRD aprovado
- Requisitos de integração
- Restrições técnicas

**Outputs Esperados**:
- **TRD (Technical Reference Document)**
- Especificações de APIs
- Contratos de integração
- Requisitos de infraestrutura

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - APIs necessárias
   - Integrações externas
   - Requisitos de performance
   - Restrições técnicas
   - Arquitetura de dados

2. **Gerar TRD** usando `trd-template.md`:
   - Documentar todas as APIs
   - Especificar contratos de dados
   - Definir requisitos de segurança
   - Incluir exemplos de uso

3. **Próximos passos**:
   - Sugerir criação de High-Level Architecture
   - Sugerir criação de ADRs
   - Agendar reunião de arquitetura

---

### Fase 2: Arquitetura e Design

#### 2.1. Reunião de Arquitetura de Alto Nível
**Objetivo**: Definir arquitetura geral do sistema
**Duração**: 6-8 horas
**Participantes**: Arquitetos, Desenvolvedores, DevOps, Product Owner

**Inputs**:
- PRD, FRD, TRD aprovados
- Requisitos não funcionais
- Restrições técnicas

**Outputs Esperados**:
- **High-Level Architecture**
- Visão geral da arquitetura
- Padrões arquiteturais
- Decisões técnicas

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Visão geral da arquitetura
   - Padrões arquiteturais escolhidos
   - Tecnologias selecionadas
   - Decisões técnicas
   - Requisitos não funcionais

2. **Gerar High-Level Architecture** usando `high-level-architecture-template.md`:
   - Documentar visão geral
   - Definir camadas da arquitetura
   - Especificar padrões utilizados
   - Incluir tecnologias e ferramentas

3. **Próximos passos**:
   - Sugerir criação de ADRs
   - Sugerir criação de Architecture Haikai
   - Agendar reunião de decisões arquiteturais

---

#### 2.2. Reunião de Decisões Arquiteturais (ADR)
**Objetivo**: Registrar decisões arquiteturais importantes
**Duração**: 4-6 horas
**Participantes**: Arquitetos, Desenvolvedores, Tech Leads

**Inputs**:
- High-Level Architecture
- Decisões técnicas pendentes
- Alternativas consideradas

**Outputs Esperados**:
- **ADR (Architectural Decision Record)**
- Decisões arquiteturais documentadas
- Justificativas e consequências
- Alternativas consideradas

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Decisões tomadas
   - Contexto de cada decisão
   - Alternativas consideradas
   - Justificativas
   - Consequências

2. **Gerar ADR** usando `adr-template.md`:
   - Documentar cada decisão
   - Incluir contexto e justificativa
   - Listar alternativas consideradas
   - Descrever consequências

3. **Próximos passos**:
   - Sugerir criação de Architecture Haikai
   - Sugerir criação de C4 Model
   - Agendar reunião de design detalhado

---

#### 2.3. Reunião de Documentação Arquitetural (Architecture Haikai)
**Objetivo**: Criar documentação concisa da arquitetura
**Duração**: 3-4 horas
**Participantes**: Arquitetos, Desenvolvedores, Stakeholders

**Inputs**:
- High-Level Architecture
- ADRs aprovados
- Requisitos funcionais e não funcionais

**Outputs Esperados**:
- **Architecture Haikai**
- Visão concisa da arquitetura
- Objetivos e restrições
- Decisões principais

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Objetivo do sistema
   - Requisitos funcionais principais
   - Restrições técnicas
   - Atributos de qualidade
   - Decisões arquiteturais

2. **Gerar Architecture Haikai** usando `architecture-hai-template.md`:
   - Documentar objetivo e escopo
   - Listar requisitos funcionais
   - Especificar restrições
   - Definir atributos de qualidade

3. **Próximos passos**:
   - Sugerir criação de C4 Model
   - Sugerir criação de System Design
   - Agendar reunião de design detalhado

---

#### 2.4. Reunião de Design Detalhado (C4 Model)
**Objetivo**: Criar documentação detalhada da arquitetura
**Duração**: 6-8 horas
**Participantes**: Arquitetos, Desenvolvedores, DevOps

**Inputs**:
- Architecture Haikai
- ADRs aprovados
- Requisitos técnicos

**Outputs Esperados**:
- **C4 Model**
- Arquitetura em quatro níveis
- Diagramas detalhados
- Especificações técnicas

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Contexto do sistema
   - Contêineres principais
   - Componentes internos
   - Estrutura de código
   - Tecnologias utilizadas

2. **Gerar C4 Model** usando `c4-model-template.md`:
   - Documentar contexto (nível 1)
   - Especificar contêineres (nível 2)
   - Detalhar componentes (nível 3)
   - Incluir estrutura de código (nível 4)

3. **Próximos passos**:
   - Sugerir criação de System Design
   - Sugerir criação de Engineering Guidelines
   - Agendar reunião de desenvolvimento

---

#### 2.5. Reunião de Design do Sistema (System Design)
**Objetivo**: Criar design completo do sistema
**Duração**: 8-10 horas
**Participantes**: Arquitetos, Desenvolvedores, DevOps, QA

**Inputs**:
- C4 Model aprovado
- Requisitos funcionais e não funcionais
- Decisões arquiteturais

**Outputs Esperados**:
- **System Design**
- Design completo do sistema
- Especificações técnicas
- Plano de implementação

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Visão geral do sistema
   - Componentes principais
   - Fluxos de dados
   - Requisitos não funcionais
   - Plano de implementação

2. **Gerar System Design** usando `system-design-template.md`:
   - Documentar visão geral
   - Especificar componentes
   - Descrever fluxos de dados
   - Incluir requisitos não funcionais

3. **Próximos passos**:
   - Sugerir criação de Engineering Guidelines
   - Sugerir criação de User Stories
   - Agendar reunião de desenvolvimento

---

#### 2.6. Reunião de Padrões de Engenharia (Engineering Guidelines)
**Objetivo**: Estabelecer padrões de desenvolvimento
**Duração**: 4-6 horas
**Participantes**: Tech Leads, Desenvolvedores, QA

**Inputs**:
- System Design aprovado
- Padrões de código
- Boas práticas

**Outputs Esperados**:
- **Engineering Guidelines**
- Padrões de código
- Boas práticas
- Processos de desenvolvimento

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Padrões de código
   - Convenções de nomenclatura
   - Boas práticas
   - Processos de desenvolvimento
   - Ferramentas utilizadas

2. **Gerar Engineering Guidelines** usando `engineering-guidelines-template.md`:
   - Documentar padrões de código
   - Especificar convenções
   - Incluir boas práticas
   - Definir processos

3. **Próximos passos**:
   - Sugerir criação de User Stories
   - Sugerir criação de Use Cases
   - Agendar reunião de desenvolvimento

---

### Fase 3: Desenvolvimento

#### 3.1. Reunião de User Stories (Sprint Planning)
**Objetivo**: Criar histórias de usuário para desenvolvimento
**Duração**: 4-6 horas
**Participantes**: Product Owner, Desenvolvedores, QA, Scrum Master

**Inputs**:
- FRD aprovado
- Requisitos funcionais
- Critérios de aceite

**Outputs Esperados**:
- **User Stories**
- Histórias de usuário priorizadas
- Critérios de aceite
- Estimativas de esforço

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Funcionalidades a serem desenvolvidas
   - Critérios de aceite
   - Prioridades
   - Estimativas de esforço
   - Dependências

2. **Gerar User Stories** usando `user-story-template.md`:
   - Criar histórias no formato "Como/Quero/Para que"
   - Incluir critérios de aceite
   - Definir cenários
   - Especificar regras de negócio

3. **Próximos passos**:
   - Sugerir criação de Use Cases
   - Sugerir criação de BDD
   - Agendar reunião de casos de uso

---

#### 3.2. Reunião de Use Cases
**Objetivo**: Detalhar casos de uso do sistema
**Duração**: 6-8 horas
**Participantes**: Analistas, Desenvolvedores, QA

**Inputs**:
- User Stories aprovadas
- Requisitos funcionais
- Fluxos de processo

**Outputs Esperados**:
- **Use Cases**
- Casos de uso detalhados
- Fluxos principais e alternativos
- Regras de negócio

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Casos de uso identificados
   - Atores envolvidos
   - Fluxos principais
   - Fluxos alternativos
   - Regras de negócio

2. **Gerar Use Cases** usando `use-case-template.md`:
   - Documentar cada caso de uso
   - Especificar atores
   - Descrever fluxos
   - Incluir regras de negócio

3. **Próximos passos**:
   - Sugerir criação de BDD
   - Sugerir criação de Test Plan
   - Agendar reunião de BDD

---

#### 3.3. Reunião de BDD (Behavior Driven Development)
**Objetivo**: Definir comportamento do sistema em linguagem natural
**Duração**: 4-6 horas
**Participantes**: Product Owner, Desenvolvedores, QA, Stakeholders

**Inputs**:
- User Stories aprovadas
- Use Cases aprovados
- Critérios de aceite

**Outputs Esperados**:
- **BDD (Behavior Driven Development)**
- Cenários em linguagem natural
- Critérios de aceite executáveis
- Regras de negócio mapeadas

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Cenários de comportamento
   - Critérios de aceite
   - Regras de negócio
   - Dados de teste
   - Fluxos de processo

2. **Gerar BDD** usando `bdd-template.md`:
   - Criar cenários em Gherkin
   - Mapear critérios de aceite
   - Documentar regras de negócio
   - Incluir dados de teste

3. **Próximos passos**:
   - Sugerir criação de Test Plan
   - Sugerir criação de Test Script
   - Agendar reunião de planejamento de testes

---

#### 3.4. Reunião de Planejamento de Testes (Test Plan)
**Objetivo**: Planejar atividades de teste
**Duração**: 4-6 horas
**Participantes**: QA, Desenvolvedores, Product Owner

**Inputs**:
- BDD aprovado
- Requisitos funcionais
- Critérios de aceite

**Outputs Esperados**:
- **Test Plan**
- Estratégia de teste
- Recursos necessários
- Cronograma de testes

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Estratégia de teste
   - Tipos de teste necessários
   - Recursos disponíveis
   - Cronograma
   - Critérios de entrada e saída

2. **Gerar Test Plan** usando `test-plan-template.md`:
   - Definir estratégia de teste
   - Especificar tipos de teste
   - Listar recursos necessários
   - Criar cronograma

3. **Próximos passos**:
   - Sugerir criação de Test Script
   - Sugerir criação de Test Case
   - Agendar reunião de roteiros de teste

---

#### 3.5. Reunião de Roteiros de Teste (Test Script)
**Objetivo**: Criar roteiros de execução de testes
**Duração**: 4-6 horas
**Participantes**: QA, Desenvolvedores

**Inputs**:
- Test Plan aprovado
- Cenários de teste
- Critérios de aceite

**Outputs Esperados**:
- **Test Script**
- Roteiros de execução
- Cenários de teste
- Dados de teste

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Cenários de teste
   - Passos de execução
   - Dados de teste
   - Critérios de aceite
   - Pré-condições

2. **Gerar Test Script** usando `test-script-template.md`:
   - Criar roteiros de execução
   - Especificar passos
   - Incluir dados de teste
   - Definir critérios de aceite

3. **Próximos passos**:
   - Sugerir criação de Test Case
   - Sugerir execução de testes
   - Agendar reunião de casos de teste

---

#### 3.6. Reunião de Casos de Teste (Test Case)
**Objetivo**: Criar casos de teste específicos
**Duração**: 6-8 horas
**Participantes**: QA, Desenvolvedores

**Inputs**:
- Test Script aprovado
- Cenários de teste
- Critérios de aceite

**Outputs Esperados**:
- **Test Case**
- Casos de teste específicos
- Passos detalhados
- Dados de teste

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Casos de teste específicos
   - Passos detalhados
   - Dados de entrada
   - Resultados esperados
   - Critérios de aceite

2. **Gerar Test Case** usando `test-case-template.md`:
   - Criar casos específicos
   - Detalhar passos
   - Especificar dados
   - Definir resultados esperados

3. **Próximos passos**:
   - Sugerir execução de testes
   - Sugerir criação de TRG
   - Agendar reunião de revisão técnica

---

### Fase 4: Entrega e Manutenção

#### 4.1. Reunião de Revisão Técnica (TRG)
**Objetivo**: Revisar qualidade técnica do produto
**Duração**: 6-8 horas
**Participantes**: Arquitetos, Desenvolvedores, QA, DevOps

**Inputs**:
- Código implementado
- Testes executados
- Documentação técnica

**Outputs Esperados**:
- **TRG (Technical Review Guide)**
- Análise de qualidade
- Pontos de melhoria
- Plano de ação

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Pontos fortes identificados
   - Pontos de melhoria
   - Riscos identificados
   - Não conformidades
   - Recomendações

2. **Gerar TRG** usando `trg-template.md`:
   - Documentar análise de qualidade
   - Listar pontos de melhoria
   - Identificar riscos
   - Criar plano de ação

3. **Próximos passos**:
   - Sugerir criação de Threat Model
   - Sugerir criação de Data Governance
   - Agendar reunião de segurança

---

#### 4.2. Reunião de Análise de Segurança (Threat Model)
**Objetivo**: Avaliar riscos de segurança do sistema
**Duração**: 6-8 horas
**Participantes**: Especialistas em Segurança, Arquitetos, Desenvolvedores

**Inputs**:
- Arquitetura do sistema
- Requisitos de segurança
- Regulamentações aplicáveis

**Outputs Esperados**:
- **Threat Model**
- Análise de ameaças
- Controles de segurança
- Plano de mitigação

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Ameaças identificadas
   - Vulnerabilidades
   - Controles de segurança
   - Riscos de segurança
   - Plano de mitigação

2. **Gerar Threat Model** usando `threat-model-template.md`:
   - Documentar ameaças
   - Especificar vulnerabilidades
   - Listar controles
   - Criar plano de mitigação

3. **Próximos passos**:
   - Sugerir criação de Data Governance
   - Sugerir implementação de controles
   - Agendar reunião de governança de dados

---

#### 4.3. Reunião de Governança de Dados (Data Governance)
**Objetivo**: Estabelecer governança e proteção de dados
**Duração**: 6-8 horas
**Participantes**: Especialistas em Dados, Compliance, Arquitetos

**Inputs**:
- Requisitos de conformidade
- Regulamentações (LGPD, GDPR)
- Dados do sistema

**Outputs Esperados**:
- **Data Governance**
- Políticas de dados
- Controles de proteção
- Plano de conformidade

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Políticas de dados
   - Controles de proteção
   - Requisitos de conformidade
   - Estrutura organizacional
   - Processos de governança

2. **Gerar Data Governance** usando `data-governance-template.md`:
   - Documentar políticas
   - Especificar controles
   - Definir estrutura organizacional
   - Criar processos de governança

3. **Próximos passos**:
   - Sugerir criação de RFC
   - Sugerir implementação de controles
   - Agendar reunião de propostas de mudança

---

#### 4.4. Reunião de Propostas de Mudança (RFC)
**Objetivo**: Propor melhorias e mudanças no sistema
**Duração**: 4-6 horas
**Participantes**: Arquitetos, Desenvolvedores, Product Owner

**Inputs**:
- Feedback do sistema
- Melhorias identificadas
- Novos requisitos

**Outputs Esperados**:
- **RFC (Request for Comments)**
- Propostas de mudança
- Análise de impacto
- Plano de implementação

**Instruções para IA**:
1. **Analisar transcrição** para extrair:
   - Propostas de mudança
   - Justificativas
   - Análise de impacto
   - Alternativas consideradas
   - Plano de implementação

2. **Gerar RFC** usando `rfc-template.md`:
   - Documentar propostas
   - Incluir justificativas
   - Analisar impacto
   - Listar alternativas

3. **Próximos passos**:
   - Sugerir criação de ADR
   - Sugerir implementação
   - Agendar reunião de decisões arquiteturais

---

## 🔄 Fluxo Completo de Reuniões

### Sequência Recomendada
```
1. Brainstorming → 2. PRD → 3. FRD → 4. TRD → 5. High-Level Architecture → 
6. ADR → 7. Architecture Haikai → 8. C4 Model → 9. System Design → 
10. Engineering Guidelines → 11. User Stories → 12. Use Cases → 
13. BDD → 14. Test Plan → 15. Test Script → 16. Test Case → 
17. TRG → 18. Threat Model → 19. Data Governance → 20. RFC
```

### Dependências entre Reuniões
- **Reuniões 1-4**: Podem ser executadas em paralelo
- **Reuniões 5-10**: Sequenciais, dependem das anteriores
- **Reuniões 11-16**: Podem ser executadas em paralelo
- **Reuniões 17-20**: Sequenciais, dependem das anteriores

## 🤖 Instruções Gerais para IAs

### Antes de Cada Reunião
1. **Identificar o Tipo**: Determinar qual tipo de reunião está sendo realizada
2. **Verificar Inputs**: Confirmar que os inputs necessários estão disponíveis
3. **Preparar Template**: Ter o template correto pronto para uso

### Durante a Análise da Transcrição
1. **Extrair Informações**: Identificar todas as informações relevantes
2. **Organizar Dados**: Estruturar as informações de forma lógica
3. **Identificar Dependências**: Verificar links com outros documentos

### Após Gerar a Documentação
1. **Validar Completude**: Verificar se todas as seções foram preenchidas
2. **Incluir Links**: Adicionar links para documentos relacionados
3. **Sugerir Próximos Passos**: Indicar quais reuniões devem ser realizadas a seguir

### Checklist de Qualidade
- [ ] Todas as seções obrigatórias foram preenchidas
- [ ] Links para documentos relacionados foram incluídos
- [ ] Próximos passos foram sugeridos
- [ ] Qualidade da documentação foi validada
- [ ] Consistência terminológica foi mantida

## 📚 Recursos Adicionais

### Templates Disponíveis
- [Lista completa de templates](README.md#documentos-disponíveis)
- [Guia de documentação](documentation-guide.md)
- [Governança e fábrica de software](software-factory-governance.md)

### Ferramentas Recomendadas
- **Transcrição**: Otter.ai, Rev.com, Google Meet
- **Análise**: ChatGPT, Claude, Gemini
- **Documentação**: Notion, Confluence, GitBook
- **Colaboração**: Miro, Figma, Draw.io

### Metodologias
- **Scrum**: Para desenvolvimento ágil
- **Waterfall**: Para projetos tradicionais
- **SAFe**: Para projetos em escala
- **DevOps**: Para integração contínua

---

**Criado por**: [Nome do Analista]
**Data**: [DD/MM/AAAA]
**Versão**: 1.0
