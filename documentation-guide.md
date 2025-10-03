# Guia de Documentação de Software

## Visão Geral

Este guia apresenta os principais tipos de documentação utilizados no desenvolvimento de software, baseado nas melhores práticas da indústria e metodologias ágeis.

## Tipos de Documentação

### 1. BDD (Behavior Driven Development)

#### Características
- **Foco**: No comportamento do sistema e comunicação entre equipes
- **Formato**: Linguagem Gherkin em português natural
- **Objetivo**: Especificar comportamento do sistema de forma compreensível

#### Quando Usar
- Desenvolvimento orientado a comportamento
- Quando é importante comunicação clara entre equipes
- Para automação de testes de aceitação
- Quando stakeholders não-técnicos precisam entender o sistema
- Para documentação viva e executável

#### Vantagens
- Linguagem natural compreensível por todos
- Documentação executável (pode ser automatizada)
- Foco no comportamento do sistema
- Facilita comunicação entre equipes
- Base sólida para testes automatizados

#### Estrutura Típica
- Especificação em linguagem Gherkin
- Cenários de sucesso, validação e exceção
- Palavras-chave obrigatórias (Dado, Quando, Então)
- Regras de negócio mapeadas
- Dados de teste e rastreabilidade

### 2. User Story (História do Usuário)

#### Características
- **Foco**: No usuário e suas necessidades
- **Formato**: "Como [papel], quero [funcionalidade], para que [benefício]"
- **Objetivo**: Descrever funcionalidades do ponto de vista do usuário final

#### Quando Usar
- Desenvolvimento ágil (Scrum, Kanban)
- Projetos orientados ao usuário
- Quando é importante entender o valor de negócio
- Para comunicação entre equipes multidisciplinares

#### Vantagens
- Fácil compreensão por stakeholders não-técnicos
- Foco no valor de negócio
- Facilita priorização de funcionalidades
- Promove colaboração entre equipes

#### Estrutura Típica
- Descrição da funcionalidade
- Papéis de usuários
- Critérios de aceite
- Cenários principais e alternativos
- Regras de negócio

### 3. Plano de Teste

#### Características
- **Foco**: No planejamento e estratégia de testes
- **Formato**: Documento estruturado com cronograma e recursos
- **Objetivo**: Planejar e organizar atividades de teste

#### Quando Usar
- Início de projetos de teste
- Quando é necessário planejamento detalhado
- Para definição de estratégia de teste
- Quando é importante documentar recursos e cronograma

#### Vantagens
- Planejamento estruturado de testes
- Definição clara de recursos necessários
- Cronograma detalhado de atividades
- Rastreabilidade de requisitos

#### Estrutura Típica
- Estratégia de teste e cronograma
- Funcionalidades e requisitos mapeados
- Recursos necessários e riscos
- Métricas de qualidade e relatórios

### 4. Roteiro de Teste

#### Características
- **Foco**: Em cenários específicos de teste
- **Formato**: Tabelas estruturadas com passos e resultados
- **Objetivo**: Executar testes de forma organizada

#### Quando Usar
- Execução de testes funcionais
- Quando é necessário documentar cenários
- Para testes de integração e sistema
- Quando é importante rastrear resultados

#### Vantagens
- Execução organizada de testes
- Documentação clara de cenários
- Rastreabilidade de resultados
- Facilita comunicação entre equipes

#### Estrutura Típica
- Cenários de sucesso, validação e exceção
- Casos de teste estruturados em tabelas
- Dados de teste e protótipos
- Execução e rastreabilidade

### 5. Caso de Teste

#### Características
- **Foco**: Em testes individuais específicos
- **Formato**: Documento detalhado com passos e evidências
- **Objetivo**: Executar e documentar testes específicos

#### Quando Usar
- Testes detalhados de funcionalidades
- Quando é necessário documentar evidências
- Para testes de aceitação
- Quando é importante rastrear defeitos

#### Vantagens
- Testes detalhados e específicos
- Documentação de evidências
- Rastreabilidade de defeitos
- Facilita análise de resultados

#### Estrutura Típica
- Passos detalhados e dados de entrada
- Resultados esperados e evidências
- Análise de resultados e defeitos
- Rastreabilidade e aprovações

### 6. Use Case (Caso de Uso)

#### Características
- **Foco**: No sistema e suas funcionalidades
- **Formato**: Descrição detalhada de interações sistema-ator
- **Objetivo**: Especificar comportamento do sistema

#### Quando Usar
- Desenvolvimento tradicional (Waterfall)
- Sistemas complexos com múltiplas interações
- Quando é necessário detalhamento técnico
- Para especificações funcionais detalhadas

#### Vantagens
- Detalhamento completo das funcionalidades
- Cobertura de cenários alternativos e exceções
- Base sólida para desenvolvimento e testes
- Documentação técnica abrangente

#### Estrutura Típica
- Atores e pré-condições
- Fluxo principal
- Fluxos alternativos e de exceção
- Regras de negócio
- Protótipos e mockups

## Comparação: BDD vs User Story vs Use Case vs Templates de Teste

| Aspecto | BDD | User Story | Use Case | Plano de Teste | Roteiro de Teste | Caso de Teste |
|---------|-----|------------|----------|----------------|------------------|---------------|
| **Foco** | Comportamento do sistema | Usuário e valor de negócio | Sistema e funcionalidades | Planejamento de testes | Cenários de teste | Testes específicos |
| **Detalhamento** | Detalhado e executável | Alto nível | Detalhado | Estruturado | Detalhado | Muito detalhado |
| **Audiência** | Toda a equipe | Stakeholders, PO, equipe | Desenvolvedores, testadores | Gerentes, testadores | Testadores | Testadores |
| **Formato** | Linguagem Gherkin | Narrativo simples | Estruturado e técnico | Documento estruturado | Tabelas estruturadas | Documento detalhado |
| **Cenários** | Completos e executáveis | Básicos | Completos (principal, alternativo, exceção) | Estratégia geral | Cenários específicos | Testes individuais |
| **Manutenção** | Média | Fácil | Complexa | Média | Média | Alta |
| **Flexibilidade** | Média | Alta | Baixa | Baixa | Média | Baixa |
| **Automação** | Sim (testes) | Não | Não | Não | Parcial | Não |
| **Linguagem** | Natural (português) | Natural | Técnica | Técnica | Técnica | Técnica |

## Quando Usar Cada Tipo

### Use BDD quando:
- Desenvolvimento orientado a comportamento
- Comunicação clara entre equipes é essencial
- Automação de testes de aceitação é necessária
- Stakeholders não-técnicos precisam entender o sistema
- Documentação viva e executável é desejada
- Equipe trabalha com metodologias ágeis e BDD

### Use User Story quando:
- Trabalhando em metodologias ágeis
- O foco é no valor de negócio
- A equipe é multidisciplinar
- Há necessidade de comunicação simples
- O projeto tem requisitos em constante mudança

### Use Use Case quando:
- O sistema é complexo
- Há necessidade de especificação detalhada
- Múltiplos atores interagem com o sistema
- É importante documentar todos os cenários
- O projeto segue metodologia tradicional

### Use Plano de Teste quando:
- Início de projetos de teste
- Necessário planejamento detalhado
- Definição de estratégia de teste
- Documentação de recursos e cronograma

### Use Roteiro de Teste quando:
- Execução de testes funcionais
- Necessário documentar cenários
- Testes de integração e sistema
- Importante rastrear resultados

### Use Caso de Teste quando:
- Testes detalhados de funcionalidades
- Necessário documentar evidências
- Testes de aceitação
- Importante rastrear defeitos

## Boas Práticas

### Para BDD
1. **Linguagem natural**: Use português claro e compreensível
2. **Palavras-chave corretas**: Sempre use Dado, Quando, Então no início das frases
3. **Cenários completos**: Cubra sucesso, validação e exceção
4. **Regras de negócio**: Documente todas as regras aplicáveis
5. **Dados de teste**: Defina dados válidos e inválidos
6. **Rastreabilidade**: Mantenha links com User Stories e Use Cases
7. **Automação**: Implemente testes automatizados baseados nos cenários

### Para User Stories
1. **Seja específico**: Evite ambiguidades na descrição
2. **Foque no valor**: Sempre explique o benefício para o usuário
3. **Critérios claros**: Defina critérios de aceite mensuráveis
4. **Tamanho adequado**: Stories devem ser completáveis em uma sprint
5. **Testabilidade**: Certifique-se de que podem ser testadas

### Para Use Cases
1. **Atores bem definidos**: Identifique todos os atores envolvidos
2. **Cenários completos**: Cubra fluxos principais, alternativos e exceções
3. **Regras de negócio**: Documente todas as regras aplicáveis
4. **Rastreabilidade**: Mantenha links com requisitos e testes
5. **Atualização**: Mantenha a documentação atualizada

### Para Planos de Teste
1. **Estratégia clara**: Defina estratégia de teste detalhada
2. **Recursos definidos**: Identifique recursos humanos e técnicos
3. **Cronograma realista**: Estabeleça prazos factíveis
4. **Riscos mapeados**: Identifique e mitigue riscos
5. **Métricas definidas**: Estabeleça métricas de qualidade

### Para Roteiros de Teste
1. **Cenários completos**: Cubra sucesso, validação e exceção
2. **Dados de teste**: Defina dados válidos e inválidos
3. **Passos claros**: Descreva passos de forma detalhada
4. **Resultados esperados**: Defina resultados claros
5. **Rastreabilidade**: Mantenha links com requisitos

### Para Casos de Teste
1. **Passos detalhados**: Descreva cada passo claramente
2. **Evidências**: Documente evidências de execução
3. **Análise de resultados**: Analise resultados obtidos
4. **Defeitos documentados**: Documente defeitos encontrados
5. **Rastreabilidade**: Mantenha links com requisitos e defeitos

## Ferramentas Recomendadas

### Para User Stories
- **Jira**: Gerenciamento de backlog e stories
- **Azure DevOps**: Work items e boards
- **Trello**: Organização simples de cards
- **Miro/Mural**: Workshops e refinamento

### Para Use Cases
- **Enterprise Architect**: Modelagem UML
- **Lucidchart**: Diagramas e fluxos
- **Confluence**: Documentação colaborativa
- **Draw.io**: Diagramas gratuitos

### Para BDD
- **Cucumber**: Automação de testes BDD
- **SpecFlow**: BDD para .NET
- **Behave**: BDD para Python
- **JBehave**: BDD para Java
- **Gauge**: Framework BDD multiplataforma

### Para Testes
- **TestRail**: Gerenciamento de casos de teste
- **Zephyr**: Execução de testes
- **Confluence**: Documentação de testes
- **Jira**: Rastreamento de defeitos
- **Selenium**: Automação de testes web

## Templates Disponíveis

1. **[BDD Template](bdd-template.md)**: Template estruturado para documentação BDD
2. **[User Story Template](user-story-template.md)**: Template completo para histórias de usuário
3. **[Use Case Template](use-case-template.md)**: Template detalhado para casos de uso
4. **[Plano de Teste Template](test-plan-template.md)**: Template para planejamento de testes
5. **[Roteiro de Teste Template](test-script-template.md)**: Template para roteiros de teste
6. **[Caso de Teste Template](test-case-template.md)**: Template para casos de teste individuais
7. **[Architecture Haikai Template](architecture-hai-template.md)**: Template para documentação arquitetural concisa
8. **[C4 Model Template](c4-model-template.md)**: Template para documentação em quatro níveis
9. **[TRG Template](trg-template.md)**: Template para revisão técnica
10. **[Threat Model Template](threat-model-template.md)**: Template para análise de segurança
11. **[Data Governance Template](data-governance-template.md)**: Template para governança de dados
12. **[High-Level Architecture Template](high-level-architecture-template.md)**: Template para arquitetura de alto nível

## Exemplos Práticos

### Exemplo de BDD
```gherkin
Funcionalidade: Cadastrar Anúncio
  Como anunciante
  Quero cadastrar um anúncio do meu serviço
  Para que clientes possam agendar a realização desse serviço

Cenário: Cadastro de anúncio com sucesso
  Dado que o anunciante esteja cadastrado no sistema
    E tenha realizado autenticação no sistema
  Quando o anunciante preencher os campos obrigatórios
    E clicar em salvar
  Então o sistema exibe uma mensagem de sucesso
    E o anúncio ficará disponível para agendamento
```

### Exemplo de User Story
```
Como anunciante
Quero publicar um anúncio do meu serviço
Para que clientes possam agendar a realização desse serviço

Critérios de aceite:
- O anúncio pode ser gratuito ou pago
- O anúncio pode ser por dia, hora ou semana
- Clientes podem agendar o serviço
```

### Exemplo de Use Case
```
Caso de Uso: Cadastrar Anúncio
Ator Principal: Anunciante
Pré-condição: Usuário deve estar logado

Fluxo Principal:
1. Usuário acessa a tela de criação de anúncio
2. Sistema exibe formulário de cadastro
3. Usuário preenche dados do anúncio
4. Sistema valida os dados
5. Sistema salva o anúncio
6. Sistema exibe confirmação
```

## 7. Architecture Haikai

### Características
- **Foco**: Documentação arquitetural concisa e prática
- **Escopo**: Visão geral do sistema com foco em objetivos
- **Audiência**: Arquitetos, desenvolvedores, stakeholders
- **Formato**: Documento estruturado com diagramas simples

### Quando Usar
- Projetos que precisam de documentação concisa
- Necessidade de visão geral rápida do sistema
- Comunicação com stakeholders não técnicos
- Documentação inicial de arquitetura

### Vantagens
- Documentação concisa e fácil de entender
- Foco nos objetivos e requisitos principais
- Facilita comunicação com stakeholders
- Documenta decisões arquiteturais importantes

### Estrutura Típica
1. **Objetivo**: Propósito principal do sistema
2. **Requisitos**: Funcionais e restrições
3. **Atributos de Qualidade**: Performance, segurança, etc.
4. **Decisões**: Decisões arquiteturais principais
5. **Integrações**: Sistemas externos e APIs
6. **Cronograma**: Fases de implementação
7. **Recursos**: Humanos, técnicos e financeiros

## 8. C4 Model

### Características
- **Foco**: Documentação em quatro níveis de abstração
- **Escopo**: Contexto, Contêineres, Componentes e Código
- **Audiência**: Arquitetos, desenvolvedores, stakeholders
- **Formato**: Documento estruturado com diagramas em níveis

### Quando Usar
- Projetos complexos com múltiplos níveis
- Necessidade de documentação detalhada
- Comunicação entre equipes técnicas
- Documentação de arquitetura de software

### Vantagens
- Documentação estruturada em níveis
- Facilita comunicação entre equipes
- Documenta arquitetura de forma clara
- Ajuda no planejamento de desenvolvimento

### Estrutura Típica
1. **Context**: Visão geral do sistema
2. **Container**: Contêineres e tecnologias
3. **Component**: Componentes internos
4. **Code**: Estrutura de código e classes
5. **Tecnologias**: Stack tecnológico
6. **Segurança**: Considerações de segurança
7. **Performance**: Requisitos de performance
8. **Deploy**: Estratégia de implantação

## Conclusão

A escolha entre BDD, User Story, Use Case, Templates de Teste e Templates Arquiteturais depende do contexto do projeto, metodologia utilizada e necessidades da equipe. Todos têm seu lugar no desenvolvimento de software e podem ser complementares:

- **BDD** é ideal para comunicação clara e automação de testes
- **User Story** é perfeita para metodologias ágeis e foco no valor de negócio
- **Use Case** é adequado para especificações técnicas detalhadas
- **Plano de Teste** é essencial para planejamento de atividades de teste
- **Roteiro de Teste** é ideal para execução organizada de testes
- **Caso de Teste** é adequado para testes detalhados e específicos
- **Architecture Haikai** é ideal para documentação concisa de arquitetura
- **C4 Model** é adequado para documentação detalhada em níveis
- **TRG** é ideal para revisão técnica e qualidade
- **Threat Model** é adequado para análise de segurança
- **Data Governance** é ideal para governança e proteção de dados
- **High-Level Architecture** é adequado para arquitetura de alto nível

O importante é manter a documentação atualizada, clara e útil para todos os envolvidos no projeto.

---

**Criado por**: [Nome do Analista]
**Data**: [DD/MM/AAAA]
**Versão**: 1.0
