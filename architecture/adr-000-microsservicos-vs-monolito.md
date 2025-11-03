# ADR-000: Microservices vs Monolith - Decision Framework

## Informações Básicas
- **ID do ADR**: ADR-000
- **Título**: Framework para Decisão entre Arquitetura de Microsserviços e Monolito
- **Status**: Accepted
- **Data**: 01/11/2025
- **Decisores**: Equipe de Arquitetura
- **Consultores**: Especialistas em Arquitetura Corporativa

## Resumo

### Decisão
Não existe uma fórmula única para escolher entre microsserviços e monolito. A decisão deve ser baseada em critérios de negócio, operação, custo e demanda funcional, não apenas em questões técnicas.

### Status
Accepted - Framework estabelecido para decisões arquiteturais futuras

### Contexto
Após anos de hype com microsserviços, o mercado atingiu maturidade e percebeu que:
- Microsserviços não são bala de prata
- Monolitos bem arquitetados podem ser adequados para muitos casos
- A decisão arquitetural é mais sobre negócio do que sobre tecnologia pura
- O tamanho dos componentes deve refletir o tamanho do domínio, não ser micro por ser micro

## Problema

### Situação Atual
- Muitas organizações adotaram microsserviços sem análise adequada de custo-benefício
- Decisões arquiteturais sendo tomadas baseadas apenas em hype e tendências
- Over-engineering comum: criando complexidade desnecessária
- Under-engineering também ocorre: monolito sem estrutura adequada
- Times pequenos tentando manter arquiteturas complexas de microsserviços

### Necessidade de Decisão
É necessário estabelecer um framework objetivo para tomar decisões arquiteturais que:
- Considere o contexto de negócio
- Avalie custos operacionais e de desenvolvimento
- Considere o tamanho e capacidade do time
- Analise demandas não-funcionais reais
- Evite decisões baseadas apenas em preferência técnica ou hype

### Restrições
- **Orçamento**: Limitações financeiras podem influenciar a decisão
- **Time disponível**: Número de desenvolvedores impacta capacidade operacional
- **Deadlines**: Prazos curtos podem exigir soluções mais simples
- **Legado**: Sistemas legados podem limitar opções
- **Vendor lock-in**: Dependência de fornecedores específicos

### Requisitos
- Decisão baseada em critérios objetivos e mensuráveis
- Documentação clara da justificativa arquitetural
- Possibilidade de evolução futura (refactoring, migração)
- Manutenibilidade a longo prazo
- Alinhamento com objetivos de negócio

## Alternativas Consideradas

### Alternativa 1: Sempre Microsserviços
**Descrição**: Adotar arquitetura de microsserviços para todos os projetos, independente do contexto.

**Prós**:
- Escalabilidade independente por domínio
- Times independentes podem trabalhar em paralelo
- Tecnologias heterogêneas possíveis
- Isolamento de falhas

**Contras**:
- Complexidade operacional alta
- Custo elevado de infraestrutura (múltiplos deploys, monitoramento)
- Difícil para times pequenos manter
- Overhead de comunicação entre serviços
- Mais difícil para testes locais
- Dependências cíclicas podem surgir

**Por que não foi escolhida**: Não considera o contexto real de negócio, tamanho do time, orçamento e complexidade do domínio. Leva a over-engineering em muitos casos.

### Alternativa 2: Sempre Monolito
**Descrição**: Manter sempre arquitetura monolítica, independente da escala e demanda.

**Prós**:
- Simplicidade operacional
- Custo menor de infraestrutura
- Fácil desenvolvimento e testes locais
- Deploy único
- Transações ACID mais simples

**Contras**:
- Escalabilidade limitada quando domínios têm demandas diferentes
- Times grandes podem conflitar
- Tecnologia única (lock-in tecnológico)
- Blast radius maior em falhas
- Dificuldade para evoluir partes independentes

**Por que não foi escolhida**: Pode ser under-engineering para sistemas que realmente precisam de escalabilidade independente ou times grandes trabalhando em paralelo.

### Alternativa 3: Framework Contextual (Escolhida)
**Descrição**: Decisão baseada em análise contextual usando critérios objetivos de negócio, operação, custo e demanda.

**Prós**:
- Decisão adequada ao contexto real
- Evita over-engineering e under-engineering
- Considera múltiplas variáveis (negócio, operação, custo)
- Permite evolução gradual
- Documentação clara da justificativa

**Contras**:
- Requer análise mais profunda
- Pode gerar debate sobre critérios
- Decisão pode mudar com o tempo (requer revisão)

**Por que foi escolhida**: É a abordagem mais pragmática e alinhada com objetivos reais de negócio, evitando extremos desnecessários.

## Decisão

### Solução Escolhida
Adotar um framework de decisão contextual que avalia múltiplos critérios antes de escolher entre microsserviços, monolito ou abordagem híbrida. A decisão deve ser documentada em ADR específico para cada caso.

### Justificativa
1. **Não é sobre tamanho da aplicação, é sobre tamanho do domínio**: Se o domínio é único e coeso, um monolito pode ser adequado. Se há múltiplos domínios distintos com demandas diferentes, microsserviços podem fazer sentido.

2. **Decisões arquiteturais são menos técnicas do que parecem**: Variáveis de negócio, operação, custo e disponibilidade de profissionais são mais importantes que preferências técnicas puras.

3. **Evolução gradual é possível**: Começar com monolito bem estruturado permite evoluir para microsserviços quando necessário, se houver separação adequada de domínios.

4. **Custo operacional importa**: Manter múltiplos microsserviços requer mais operação do que um monolito. Para times pequenos ou orçamentos limitados, monolito pode ser mais viável.

### Critérios de Decisão

#### 1. Contexto de Negócio
- **Objetivos estratégicos**: Alinhamento com objetivos de longo prazo
- **Volumetria esperada**: Número de transações/usuários esperados
- **Evolução prevista**: Taxa de mudança e evolução do produto
- **Prioridades**: Time-to-market vs otimização

#### 2. Operação e Time
- **Tamanho do time**: Número de desenvolvedores disponíveis
- **Especialização**: Capacidade de manter múltiplas tecnologias
- **Maturidade operacional**: Capacidade de gerenciar complexidade
- **Comunicação**: Qualidade da comunicação entre times

#### 3. Demanda Não-Funcional
- **Escalabilidade**: Necessidade de escalar componentes independentemente
- **Disponibilidade**: SLAs e requisitos de uptime
- **Performance**: Requisitos de latência e throughput
- **Resiliência**: Tolerância a falhas

#### 4. Custo
- **Custo de infraestrutura**: Cloud, servidores, licenças
- **Custo operacional**: Manutenção, monitoramento, deploy
- **Custo de desenvolvimento**: Curva de aprendizado, ferramentas
- **ROI esperado**: Retorno sobre investimento em complexidade

#### 5. Domínio
- **Tamanho do domínio**: Um domínio ou múltiplos domínios distintos
- **Acoplamento**: Grau de acoplamento entre componentes
- **Coesão**: Coesão dos componentes dentro do domínio
- **Bounded Contexts**: Limites claros entre contextos

## Consequências

### Consequências Positivas
- **Decisões mais adequadas**: Arquitetura alinhada com realidade de negócio
- **Redução de over-engineering**: Evita complexidade desnecessária
- **Redução de under-engineering**: Garante estrutura adequada quando necessário
- **Documentação clara**: Justificativas arquiteturais bem documentadas
- **Evolução pragmática**: Permite evoluir conforme necessidade real
- **Custo otimizado**: Decisões consideram impacto financeiro

### Consequências Negativas
- **Requer análise**: Mais tempo para decisão inicial
- **Pode gerar debate**: Diferentes opiniões sobre critérios
- **Revisão periódica necessária**: Contexto muda, decisão pode precisar mudar
- **Sem fórmula mágica**: Requer experiência e julgamento técnico

### Mitigações
- **Template de análise**: Template para guiar análise de decisão arquitetural
- **Documentação obrigatória**: ADR obrigatório para decisões arquiteturais
- **Revisão periódica**: Revisar decisões a cada 6-12 meses ou em mudanças significativas
- **Consultoria interna**: Arquitetos experientes disponíveis para consulta
- **Casos de referência**: Biblioteca de decisões passadas para consulta

## Implementação

### Plano de Implementação
1. **Comunicação do Framework**: Apresentar framework para equipes de desenvolvimento
2. **Capacitação**: Treinar arquitetos e líderes técnicos no uso do framework
3. **Aplicação em Projetos Novos**: Usar framework em todos os novos projetos
4. **Revisão de Projetos Existentes**: Revisar decisões arquiteturais existentes
5. **Documentação de Casos**: Documentar casos de uso como referência

### Fases

#### Fase 1: Disseminação (Mês 1)
- Apresentação do framework para toda equipe técnica
- Publicação de documentação no projeto docs
- Treinamento de arquitetos

#### Fase 2: Aplicação (Meses 2-3)
- Aplicar framework em projetos novos
- Criar ADRs para decisões arquiteturais
- Documentar casos de uso

#### Fase 3: Consolidação (Mês 4+)
- Revisar decisões tomadas
- Refinar framework com lições aprendidas
- Manter biblioteca de referência atualizada

### Recursos Necessários
- **Tempo de arquitetos**: 2-4 horas por decisão arquitetural
- **Templates**: Template de ADR e checklist de decisão
- **Documentação**: Espaço no projeto docs para documentação
- **Treinamento**: Sessões de capacitação para equipes

### Cronograma
- **Início**: 01/11/2025
- **Fim**: 01/03/2026 (consolidação contínua)
- **Milestones**:
  - Framework publicado (Semana 1)
  - Primeiro ADR usando framework (Semana 2)
  - 5 ADRs documentados (Mês 1)
  - Framework refinado com feedback (Mês 3)

## Monitoramento

### Métricas de Sucesso
- **Qualidade das decisões**: % de decisões que não precisaram ser revertidas
- **Satisfação das equipes**: Pesquisa de satisfação com decisões arquiteturais
- **Custo**: Redução de custos operacionais onde aplicável
- **Time-to-market**: Impacto em velocidade de entrega
- **Manutenibilidade**: Facilidade de manutenção percebida

### Indicadores de Problema
- **Decisões revertidas**: Alta taxa de reversão de decisões arquiteturais
- **Queixas de complexidade**: Equipes reclamando de complexidade desnecessária
- **Custos elevados**: Custos operacionais acima do esperado
- **Atrasos**: Atrasos em entregas relacionados a decisões arquiteturais

### Alertas
- **Alerta de over-engineering**: Quando complexidade não se justifica
- **Alerta de under-engineering**: Quando estrutura básica está faltando
- **Alerta de custo**: Quando custos operacionais excedem orçamento
- **Alerta de time**: Quando time não tem capacidade para manter arquitetura

## Revisão e Manutenção

### Frequência de Revisão
Esta decisão deve ser revisada:
- Semestralmente (revisão periódica)
- Quando contexto de negócio muda significativamente
- Quando novas tecnologias ou padrões emergem
- Após 5-10 decisões arquiteturais usando o framework

### Critérios de Revisão
- **Mudança de contexto**: Empresa cresceu ou mudou foco significativamente
- **Novas tecnologias**: Novas opções arquiteturais disponíveis
- **Lições aprendidas**: Padrões claros emergindo de decisões passadas
- **Feedback**: Equipes indicando problemas com framework

### Responsáveis pela Revisão
- **Arquiteto Principal**: Responsável por revisar e atualizar framework
- **CTO/Head of Engineering**: Aprova mudanças significativas
- **Arquitetos de Equipe**: Contribuem com feedback e casos de uso

## Dependências

### Dependências Internas
- **Arquitetura Corporativa**: Framework deve estar alinhado com arquitetura corporativa
- **Processos de Desenvolvimento**: Integração com processos ágeis e documentação
- **Governança**: Aprovação de governança de TI

### Dependências Externas
- **Tendências de Mercado**: Evolução de padrões e tecnologias
- **Capacitação**: Treinamento e educação contínua
- **Ferramentas**: Ferramentas de documentação e análise

### Impacto em Outras Decisões
- **ADR-001+**: Todas as decisões arquiteturais futuras devem usar este framework
- **Decisões de Tecnologia**: Framework influencia escolhas de stack tecnológico
- **Decisões de Infraestrutura**: Influencia escolhas de cloud e infraestrutura

## Documentação Relacionada

### Documentos Técnicos
- [Guia de Critérios de Decisão Arquitetural](../architecture/criterios-decisao-arquitetural.md)
- [Insights de Arquitetura Corporativa](../architecture/insights-arquitetura-corporativa.md)
- [Anti-padrões e Lições Aprendidas](../architecture/anti-padroes-licoes-aprendidas.md)

### Referências
- Transcrição do Podcast "PPT Não Compila" - Episódio sobre Microsserviços (2025)
- Gartner Hype Cycle - Maturidade de Tecnologias
- Domain-Driven Design - Eric Evans
- Building Microservices - Sam Newman

### Estudos de Caso
- [iFood - Migração Oracle para Postgres](../cases/ifood/adr-001-database-modernization.md)
- Casos de uso internos (a documentar)

## Histórico de Alterações

| Versão | Data | Autor | Alteração |
|--------|------|-------|-----------|
| 1.0 | 01/11/2025 | Equipe Skynet Docs | Criação inicial baseada em insights de transcrição |

## Aprovações

### Aprovação Técnica
- **Aprovador**: Arquitetura de Software
- **Data**: 01/11/2025
- **Status**: Aprovado
- **Comentários**: Framework estabelecido como padrão para decisões arquiteturais

### Aprovação de Arquitetura
- **Aprovador**: Equipe de Arquitetura Corporativa
- **Data**: 01/11/2025
- **Status**: Aprovado
- **Comentários**: Alinhado com arquitetura corporativa e objetivos de negócio

### Aprovação de Negócio
- **Aprovador**: [A definir]
- **Data**: [A definir]
- **Status**: Pendente
- **Comentários**: [A definir]

---

**Revisado por**: Equipe de Arquitetura Skynet
**Aprovado por**: [A definir]
**Status**: Accepted

