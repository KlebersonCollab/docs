# Critérios de Decisão Arquitetural

## Visão Geral

Este documento detalha os critérios objetivos para tomar decisões arquiteturais, especialmente sobre quando usar microsserviços vs monolito, e outras decisões arquiteturais importantes.

**Baseado em**: Insights extraídos de discussões técnicas e transcrições de podcasts sobre arquitetura de software.

---

## 📊 Framework de Decisão

### Matriz de Decisão Rápida

| Critério | Monolito Recomendado | Microsserviços Recomendado | Híbrido Recomendado |
|----------|---------------------|---------------------------|---------------------|
| **Tamanho do Time** | < 10 desenvolvedores | > 30 desenvolvedores | 10-30 desenvolvedores |
| **Domínios** | 1-2 domínios coesos | 3+ domínios distintos | 2-3 domínios com alguma sobreposição |
| **Escalabilidade** | Escala uniforme | Escalas independentes necessárias | Alguns componentes precisam escala independente |
| **Orçamento** | Limitado | Ampla disponibilidade | Médio |
| **Operação** | Time pequeno/limitado | Time DevOps robusto | Time DevOps médio |
| **Time-to-Market** | Crítico (rápido) | Flexível | Médio |
| **Volumetria** | Baixa-Média (< 100K req/dia) | Alta (> 1M req/dia) | Média-Alta (100K-1M req/dia) |

---

## 🎯 Critérios Detalhados

### 1. Contexto de Negócio

#### 1.1 Objetivos Estratégicos

**Perguntas a responder**:
- Qual o objetivo estratégico do produto/sistema?
- Qual a visão de longo prazo (1-3 anos)?
- Como a arquitetura suporta os objetivos de negócio?

**Monolito é melhor quando**:
- Produto MVP ou em fase inicial
- Objetivo é validar hipótese rapidamente
- Recursos limitados para investir em infraestrutura complexa

**Microsserviços é melhor quando**:
- Produto maduro com roadmap claro
- Objetivo é escalar para múltiplos mercados/regiões
- Diferentes domínios têm estratégias diferentes

#### 1.2 Volumetria Esperada

**Perguntas a responder**:
- Quantos usuários/transações são esperados?
- Qual o crescimento projetado?
- Há picos de tráfego previsíveis?

**Monolito é melhor quando**:
- < 100.000 requisições/dia
- Crescimento gradual e previsível
- Picos gerenciáveis com auto-scaling simples

**Microsserviços é melhor quando**:
- > 1.000.000 requisições/dia
- Crescimento exponencial esperado
- Picos significativos em componentes específicos

#### 1.3 Evolução Prevista

**Perguntas a responder**:
- Com que frequência o produto muda?
- Há múltiplos times trabalhando em paralelo?
- Mudanças afetam todo o sistema ou domínios específicos?

**Monolito é melhor quando**:
- Mudanças são frequentes mas coordenadas
- Time único ou pequeno
- Mudanças afetam o sistema como um todo

**Microsserviços é melhor quando**:
- Múltiplos times com prioridades diferentes
- Mudanças são independentes por domínio
- Ciclos de release diferentes por componente

#### 1.4 Prioridades

**Perguntas a responder**:
- Time-to-market é crítico?
- Qualidade vs velocidade: qual prioridade?
- Orçamento para investimento inicial?

**Monolito é melhor quando**:
- Time-to-market é crítico
- Orçamento limitado para infraestrutura
- Aceita trade-offs em escalabilidade futura

**Microsserviços é melhor quando**:
- Flexibilidade e escalabilidade são prioridades
- Orçamento permite investimento inicial maior
- Manutenibilidade a longo prazo é crítica

---

### 2. Operação e Time

#### 2.1 Tamanho do Time

**Perguntas a responder**:
- Quantos desenvolvedores vão trabalhar no sistema?
- Há capacidade para manter múltiplos serviços?
- Time é distribuído ou co-localizado?

**Monolito é melhor quando**:
- < 10 desenvolvedores
- Time co-localizado ou pequeno
- Capacidade limitada para operação complexa

**Microsserviços é melhor quando**:
- > 30 desenvolvedores
- Múltiplos times distribuídos
- Capacidade de operação distribuída

#### 2.2 Especialização

**Perguntas a responder**:
- Time domina múltiplas tecnologias?
- Há especialistas por domínio?
- Capacidade de manter stack heterogêneo?

**Monolito é melhor quando**:
- Time focado em uma stack tecnológica
- Especialização em domínio único
- Homogeneidade tecnológica preferida

**Microsserviços é melhor quando**:
- Times especializados em diferentes tecnologias
- Diferentes domínios têm necessidades tecnológicas diferentes
- Capacidade de gerenciar múltiplas stacks

#### 2.3 Maturidade Operacional

**Perguntas a responder**:
- Time tem experiência com DevOps?
- Processos de deploy/monitoramento maduros?
- Cultura de observabilidade estabelecida?

**Monolito é melhor quando**:
- Maturidade operacional ainda em desenvolvimento
- Processos de deploy simples são suficientes
- Foco em desenvolvimento, não em operação

**Microsserviços é melhor quando**:
- Maturidade operacional alta (DevOps, SRE)
- Processos automatizados robustos
- Observabilidade como cultura

#### 2.4 Comunicação

**Perguntas a responder**:
- Qualidade da comunicação entre times?
- Há conflitos frequentes em merges/deploys?
- Times trabalham de forma independente?

**Monolito é melhor quando**:
- Comunicação excelente entre times
- Coordenação de deploys é viável
- Times trabalham de forma colaborativa

**Microsserviços é melhor quando**:
- Comunicação limitada entre times
- Dependências criam gargalos
- Times precisam trabalhar independentemente

---

### 3. Demanda Não-Funcional

#### 3.1 Escalabilidade

**Perguntas a responder**:
- Todos os componentes escalam igualmente?
- Há componentes com demandas muito diferentes?
- Escala horizontal é necessária?

**Monolito é melhor quando**:
- Escala uniforme é suficiente
- Auto-scaling simples resolve
- Componentes têm demandas similares

**Microsserviços é melhor quando**:
- Componentes precisam escalar independentemente
- Alguns componentes têm demanda muito maior
- Otimização de recursos por componente

#### 3.2 Disponibilidade

**Perguntas a responder**:
- Qual o SLA necessário?
- Falhas podem ser isoladas por domínio?
- Disaster recovery por componente?

**Monolito é melhor quando**:
- SLA 99.9% é suficiente
- Falhas afetam todo o sistema de qualquer forma
- Disaster recovery simples é adequado

**Microsserviços é melhor quando**:
- SLA > 99.99% necessário
- Isolamento de falhas crítico
- Disaster recovery granular necessário

#### 3.3 Performance

**Perguntas a responder**:
- Há requisitos de latência específicos?
- Alguns componentes precisam de otimização especial?
- Cache e otimizações podem ser compartilhadas?

**Monolito é melhor quando**:
- Performance uniforme é aceitável
- Otimizações podem ser compartilhadas
- Latência não é crítica

**Microsserviços é melhor quando**:
- Diferentes requisitos de performance por componente
- Otimizações específicas necessárias
- Latência crítica em alguns componentes

#### 3.4 Resiliência

**Perguntas a responder**:
- Falhas devem ser isoladas?
- Circuit breakers necessários?
- Retry e fallback por componente?

**Monolito é melhor quando**:
- Resiliência simples é suficiente
- Falhas afetam sistema como um todo
- Estratégias de retry uniformes

**Microsserviços é melhor quando**:
- Isolamento de falhas crítico
- Circuit breakers por componente
- Estratégias de fallback específicas

---

### 4. Custo

#### 4.1 Custo de Infraestrutura

**Perguntas a responder**:
- Orçamento para cloud/infraestrutura?
- Múltiplos ambientes necessários?
- Licenças e ferramentas adicionais?

**Monolito é melhor quando**:
- Orçamento limitado
- Infraestrutura simples é suficiente
- Minimizar custos operacionais

**Microsserviços é melhor quando**:
- Orçamento permite múltiplos ambientes
- ROI da escalabilidade justifica custo
- Otimização de custos por componente

#### 4.2 Custo Operacional

**Perguntas a responder**:
- Time de operação disponível?
- Monitoramento e observabilidade complexos?
- Múltiplos deploys e pipelines?

**Monolito é melhor quando**:
- Time de operação limitado
- Monitoramento simples é suficiente
- Deploy único é viável

**Microsserviços é melhor quando**:
- Time de operação robusto
- Observabilidade avançada disponível
- Pipelines automatizados maduros

#### 4.3 Custo de Desenvolvimento

**Perguntas a responder**:
- Curva de aprendizado aceitável?
- Ferramentas e frameworks disponíveis?
- Treinamento necessário?

**Monolito é melhor quando**:
- Stack conhecida pelo time
- Ferramentas familiares
- Minimizar curva de aprendizado

**Microsserviços é melhor quando**:
- Múltiplas tecnologias são vantagem
- Times especializados disponíveis
- Investimento em treinamento viável

#### 4.4 ROI Esperado

**Perguntas a responder**:
- Retorno justifica investimento em complexidade?
- Ganhos de produtividade esperados?
- Benefícios de negócio mensuráveis?

**Monolito é melhor quando**:
- ROI em complexidade não é claro
- Benefícios futuros incertos
- Foco em entrega rápida de valor

**Microsserviços é melhor quando**:
- ROI comprovado em escalabilidade
- Benefícios de negócio claros
- Investimento se paga em curto prazo

---

### 5. Domínio

#### 5.1 Tamanho do Domínio

**Perguntas a responder**:
- Quantos domínios distintos existem?
- Domínios são grandes ou pequenos?
- Há subdomínios claros?

**Monolito é melhor quando**:
- 1-2 domínios coesos
- Domínios pequenos ou médios
- Subdomínios interligados

**Microsserviços é melhor quando**:
- 3+ domínios distintos
- Domínios grandes e complexos
- Subdomínios bem definidos

#### 5.2 Acoplamento

**Perguntas a responder**:
- Componentes são fortemente acoplados?
- Dependências circulares?
- Interfaces bem definidas?

**Monolito é melhor quando**:
- Acoplamento alto é aceitável
- Dependências são normais
- Interfaces podem ser internas

**Microsserviços é melhor quando**:
- Acoplamento baixo necessário
- Dependências devem ser explícitas
- Interfaces públicas bem definidas

#### 5.3 Coesão

**Perguntas a responder**:
- Componentes dentro do domínio são coesos?
- Responsabilidades bem definidas?
- Boundaries claros?

**Monolito é melhor quando**:
- Alta coesão dentro do domínio
- Responsabilidades compartilhadas
- Boundaries podem ser internos

**Microsserviços é melhor quando**:
- Baixa coesão entre domínios
- Responsabilidades bem isoladas
- Boundaries explícitos necessários

#### 5.4 Bounded Contexts

**Perguntas a responder**:
- Bounded contexts bem definidos?
- Ubiquitous language por contexto?
- Modelos distintos por contexto?

**Monolito é melhor quando**:
- Bounded contexts compartilhados
- Linguagem ubíqua única
- Modelo unificado

**Microsserviços é melhor quando**:
- Bounded contexts distintos
- Linguagens ubíquas diferentes
- Modelos independentes

---

## 📋 Checklist de Decisão

Use este checklist para avaliar seu contexto antes de tomar uma decisão arquitetural:

### Contexto de Negócio
- [ ] Objetivos estratégicos claros e alinhados
- [ ] Volumetria projetada analisada
- [ ] Evolução prevista considerada
- [ ] Prioridades definidas

### Operação e Time
- [ ] Tamanho do time adequado para escolha
- [ ] Capacidade operacional avaliada
- [ ] Especialização do time considerada
- [ ] Comunicação entre times analisada

### Demanda Não-Funcional
- [ ] Requisitos de escalabilidade claros
- [ ] SLAs e disponibilidade definidos
- [ ] Performance e latência especificados
- [ ] Resiliência e isolamento avaliados

### Custo
- [ ] Orçamento disponível confirmado
- [ ] Custos operacionais estimados
- [ ] ROI projetado analisado
- [ ] Trade-offs financeiros aceitos

### Domínio
- [ ] Domínios identificados e delimitados
- [ ] Acoplamento e coesão analisados
- [ ] Bounded contexts definidos
- [ ] Boundaries claros estabelecidos

---

## 🎯 Tomada de Decisão

### Processo Recomendado

1. **Análise Contextual**: Responder todas as perguntas acima
2. **Documentação**: Documentar respostas e análise
3. **Avaliação Quantitativa**: Dar pesos e scores para cada critério
4. **Discussão**: Debater com time técnico e stakeholders
5. **Decisão**: Escolher baseado em evidências, não preferência
6. **ADR**: Documentar decisão em ADR (Architecture Decision Record)
7. **Revisão**: Revisar decisão periodicamente (6-12 meses)

### Pesos Sugeridos

Ajuste os pesos conforme sua organização:

| Critério | Peso | Justificativa |
|----------|------|---------------|
| **Contexto de Negócio** | 30% | Mais importante: alinha com objetivos |
| **Operação e Time** | 25% | Capacidade operacional é crítica |
| **Custo** | 20% | Viabilidade financeira essencial |
| **Demanda Não-Funcional** | 15% | Requisitos técnicos importantes |
| **Domínio** | 10% | Base técnica, mas não determinante sozinho |

### Scoring

Para cada critério, atribua:
- **1**: Fortemente favorece Monolito
- **2**: Levemente favorece Monolito
- **3**: Neutro / Híbrido adequado
- **4**: Levemente favorece Microsserviços
- **5**: Fortemente favorece Microsserviços

**Score Total**:
- **< 2.5**: Monolito recomendado
- **2.5 - 3.5**: Híbrido ou evolução gradual
- **> 3.5**: Microsserviços recomendado

---

## ⚠️ Armadilhas Comuns

### Over-Engineering
- ❌ **Erro**: Escolher microsserviços "porque é moderno"
- ✅ **Correto**: Escolher baseado em necessidade real de negócio

### Under-Engineering
- ❌ **Erro**: Monolito sem estrutura adequada
- ✅ **Correto**: Monolito bem arquitetado com separação de domínios

### Decisão por Hype
- ❌ **Erro**: Seguir tendências sem análise
- ✅ **Correto**: Analisar contexto antes de decidir

### Ignorar Custo
- ❌ **Erro**: Focar só em aspectos técnicos
- ✅ **Correto**: Considerar custo operacional e de desenvolvimento

### Ignorar Capacidade do Time
- ❌ **Erro**: Arquitetura além da capacidade do time
- ✅ **Correto**: Arquitetura adequada à capacidade disponível

---

## 📚 Referências

- [ADR-000: Framework de Decisão Microsserviços vs Monolito](./adr-000-microsservicos-vs-monolito.md)
- [Insights de Arquitetura Corporativa](./insights-arquitetura-corporativa.md)
- [Anti-padrões e Lições Aprendidas](./anti-padroes-licoes-aprendidas.md)
- Domain-Driven Design - Eric Evans
- Building Microservices - Sam Newman

---

**Última atualização**: 01/11/2025
**Mantenedor**: Equipe de Arquitetura Skynet

