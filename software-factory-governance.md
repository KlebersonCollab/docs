# Governança e Fábrica de Software para LLMs e IAs

## 🎯 Objetivo

Este documento define como LLMs e IAs devem utilizar este projeto como uma **governança completa** e **fábrica de software**, garantindo que toda documentação gerada siga padrões consistentes e cubra todas as fases do ciclo de vida do software.

## 🔄 Ciclo de Vida Completo do Software

### Fase 1: Ideação e Planejamento
| Etapa | Documentação | Template | Quando Usar | Próximos Passos |
|-------|-------------|----------|-------------|-----------------|
| **Brainstorming** | Documento de Ideias | - | Capturar ideias iniciais | → PRD |
| **Definição de Requisitos** | PRD | `prd-template.md` | Definir produto e objetivos | → FRD, TRD |
| **Requisitos Funcionais** | FRD | `frd-template.md` | Detalhar funcionalidades | → User Stories, Use Cases |
| **Requisitos Técnicos** | TRD | `trd-template.md` | Especificar APIs e integrações | → ADR, System Design |

### Fase 2: Arquitetura e Design
| Etapa | Documentação | Template | Quando Usar | Próximos Passos |
|-------|-------------|----------|-------------|-----------------|
| **Arquitetura de Alto Nível** | High-Level Architecture | `high-level-architecture-template.md` | Visão geral da arquitetura | → ADR, C4 Model |
| **Decisões Arquiteturais** | ADR | `adr-template.md` | Registrar decisões importantes | → System Design |
| **Documentação Concisa** | Architecture Haikai | `architecture-hai-template.md` | Visão rápida da arquitetura | → C4 Model |
| **Documentação Detalhada** | C4 Model | `c4-model-template.md` | Arquitetura em níveis | → Engineering Guidelines |
| **Design do Sistema** | System Design | `system-design-template.md` | Design completo do sistema | → User Stories, Use Cases |
| **Padrões de Engenharia** | Engineering Guidelines | `engineering-guidelines-template.md` | Estabelecer padrões | → Desenvolvimento |

### Fase 3: Desenvolvimento
| Etapa | Documentação | Template | Quando Usar | Próximos Passos |
|-------|-------------|----------|-------------|-----------------|
| **User Stories** | User Story | `user-story-template.md` | Desenvolvimento ágil | → BDD, Test Cases |
| **Use Cases** | Use Case | `use-case-template.md` | Especificações técnicas | → Test Cases |
| **BDD** | BDD | `bdd-template.md` | Comportamento do sistema | → Test Cases |
| **Plano de Testes** | Test Plan | `test-plan-template.md` | Planejamento de testes | → Test Scripts |
| **Roteiro de Testes** | Test Script | `test-script-template.md` | Execução de testes | → Test Cases |
| **Casos de Teste** | Test Case | `test-case-template.md` | Testes específicos | → Execução |

### Fase 4: Entrega e Manutenção
| Etapa | Documentação | Template | Quando Usar | Próximos Passos |
|-------|-------------|----------|-------------|-----------------|
| **Revisão Técnica** | TRG | `trg-template.md` | Revisão final do produto | → Deploy |
| **Análise de Segurança** | Threat Model | `threat-model-template.md` | Avaliar riscos de segurança | → Data Governance |
| **Governança de Dados** | Data Governance | `data-governance-template.md` | Proteger e governar dados | → Manutenção |
| **Propostas de Mudança** | RFC | `rfc-template.md` | Propor melhorias | → ADR |

## 🤖 Instruções para LLMs e IAs

### 1. Análise do Contexto
Antes de gerar qualquer documentação, a IA deve:

1. **Identificar o Tipo de Projeto**: Web, Mobile, Desktop, API, etc.
2. **Determinar a Fase Atual**: Em qual fase do ciclo de vida o projeto está
3. **Identificar Stakeholders**: Quem são os envolvidos no projeto
4. **Analisar Requisitos**: Quais são os requisitos principais
5. **Verificar Dependências**: Quais documentos já existem

### 2. Seleção do Template
Com base na análise do contexto:

1. **Consultar a Tabela**: Usar a tabela do ciclo de vida para identificar o template correto
2. **Verificar Prerequisitos**: Garantir que os documentos anteriores foram criados
3. **Considerar Dependências**: Incluir links para documentos relacionados
4. **Adaptar ao Contexto**: Modificar o template conforme necessário

### 3. Preenchimento Estruturado
Ao preencher o template:

1. **Seguir a Estrutura**: Usar todas as seções obrigatórias do template
2. **Manter Consistência**: Usar terminologia consistente em todo o projeto
3. **Incluir Rastreabilidade**: Adicionar links para documentos relacionados
4. **Garantir Qualidade**: Seguir as boas práticas definidas nos templates

### 4. Validação de Qualidade
Antes de finalizar:

1. **Verificar Completude**: Todas as seções obrigatórias foram preenchidas
2. **Validar Links**: Todos os links para documentos relacionados funcionam
3. **Revisar Consistência**: Terminologia e formato consistentes
4. **Validar Rastreabilidade**: Links bidirecionais entre documentos

### 5. Geração de Links
Incluir links para:

1. **Documentos Anteriores**: Links para documentos da fase anterior
2. **Documentos Relacionados**: Links para documentos da mesma fase
3. **Próximos Passos**: Links para documentos da próxima fase
4. **Referências**: Links para documentação externa relevante

## 📋 Checklist para IAs

### Antes de Gerar Documentação
- [ ] Identifiquei o tipo de projeto
- [ ] Determinei a fase atual do ciclo de vida
- [ ] Identifiquei os stakeholders envolvidos
- [ ] Analisei os requisitos principais
- [ ] Verifiquei quais documentos já existem

### Durante a Geração
- [ ] Usei o template correto para a fase atual
- [ ] Preenchi todas as seções obrigatórias
- [ ] Mantive consistência terminológica
- [ ] Incluí links para documentos relacionados
- [ ] Segui as boas práticas do template

### Após a Geração
- [ ] Verifiquei a completude do documento
- [ ] Validei todos os links
- [ ] Revisei a consistência
- [ ] Confirmei a rastreabilidade
- [ ] Sugeri próximos passos

## 🔗 Exemplo de Fluxo Completo

### Cenário: Novo Sistema de E-commerce

#### 1. Análise do Contexto
- **Tipo**: Sistema web de e-commerce
- **Fase**: Ideação e Planejamento
- **Stakeholders**: Product Owner, Desenvolvedores, QA
- **Requisitos**: Catálogo, Carrinho, Checkout, Pagamento

#### 2. Seleção do Template
- **Template**: PRD (Product Requirements Document)
- **Justificativa**: Primeira fase, definição de produto
- **Prerequisitos**: Nenhum (documento inicial)

#### 3. Preenchimento Estruturado
- **Seções**: Objetivo, Requisitos, Público-alvo, etc.
- **Conteúdo**: Específico para e-commerce
- **Links**: Nenhum (documento inicial)

#### 4. Próximos Passos Sugeridos
- **FRD**: Detalhar funcionalidades
- **TRD**: Especificar APIs de pagamento
- **High-Level Architecture**: Definir arquitetura
- **ADR**: Registrar decisões arquiteturais

#### 5. Rastreabilidade
- **Documento Anterior**: Nenhum
- **Documentos Relacionados**: FRD, TRD, High-Level Architecture
- **Próxima Fase**: Arquitetura e Design

## 🎯 Benefícios da Governança

### Para Desenvolvedores
1. **Estrutura Clara**: Sabem exatamente o que documentar
2. **Padrões Consistentes**: Todos os documentos seguem o mesmo padrão
3. **Rastreabilidade**: Fácil navegação entre documentos
4. **Qualidade**: Templates promovem qualidade

### Para IAs e LLMs
1. **Instruções Claras**: Sabem exatamente o que fazer
2. **Templates Estruturados**: Não precisam "adivinhar" a estrutura
3. **Ciclo de Vida Completo**: Cobertura de todas as fases
4. **Governança**: Garantem consistência e qualidade

### Para o Projeto
1. **Documentação Completa**: Nenhuma fase fica sem documentação
2. **Qualidade Consistente**: Todos os documentos seguem padrões
3. **Rastreabilidade**: Fácil manutenção e evolução
4. **Governança**: Controle total sobre o processo

## 📚 Recursos Adicionais

### Templates Disponíveis
- [Lista completa de templates](README.md#documentos-disponíveis)
- [Guia de documentação](documentation-guide.md)
- [Exemplos práticos](bdd-example.md)

### Ferramentas Recomendadas
- **Draw.io**: Para diagramas C4 Model
- **Lucidchart**: Para diagramas arquiteturais
- **PlantUML**: Para diagramas de código
- **OWASP ZAP**: Para análise de segurança
- **SonarQube**: Para análise de qualidade

### Metodologias
- **Scrum**: Para desenvolvimento ágil
- **Waterfall**: Para projetos tradicionais
- **SAFe**: Para projetos em escala
- **DevOps**: Para integração contínua
- **SRE**: Para confiabilidade

---

**Criado por**: [Nome do Analista]
**Data**: [DD/MM/AAAA]
**Versão**: 1.0
