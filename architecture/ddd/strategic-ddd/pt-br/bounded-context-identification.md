# 🔍 Guia de Identificação de Bounded Context

## 📋 Visão Geral

Identificar bounded contexts é uma das atividades mais importantes no DDD Estratégico. Um bounded context define o limite dentro do qual um modelo de domínio é válido e onde a terminologia tem significados específicos.

**Princípio Fundamental**: Bounded contexts são descobertos através de exploração do domínio, não projetados antecipadamente.

---

## 🎯 O que é um Bounded Context?

### Definição

Um **Bounded Context** é:
- Um limite dentro do qual um modelo de domínio é válido
- Um contexto onde termos têm significados específicos e não ambíguos
- Uma área onde a linguagem ubíqua é consistente
- Uma unidade de deploy (pode ser implantada independentemente)
- Possuído por uma equipe (ou subconjunto de uma equipe)

### Características

✅ **Tem Limites Claros**:
- Escopo claro de responsabilidade
- Interfaces definidas com outros contextos
- Capacidade de deploy independente

✅ **Tem Seu Próprio Modelo**:
- Modelo de domínio específico para o contexto
- Entidades, value objects e serviços
- Regras de negócio e invariantes

✅ **Tem Sua Própria Linguagem**:
- Linguagem ubíqua dentro do contexto
- Termos têm significados específicos
- Terminologia consistente em toda a equipe

✅ **Pode Ser Implementado Independentemente**:
- Stack tecnológico diferente se necessário
- Banco de dados diferente se necessário
- Cronograma de deploy diferente

---

## 🔍 Técnicas de Identificação

### 1. Limites de Linguagem

**Princípio**: Onde a terminologia muda de significado, provavelmente há um limite.

**Técnicas**:
- **Mapeamento de Terminologia**: Mapear termos em toda a organização
- **Detecção de Ambiguidade**: Identificar onde termos são ambíguos
- **Entrevistas de Linguagem**: Entrevistar especialistas de domínio sobre terminologia

**Exemplo**:
```
No contexto "Gerenciamento de Pedidos":
- Pedido: Solicitação de compra de um cliente
- Cliente: Pessoa que faz o pedido
- Produto: Item sendo pedido

No contexto "Gerenciamento de Inventário":
- Pedido: Solicitação de reposição de estoque
- Cliente: Gerente de armazém interno
- Produto: SKU com níveis de estoque

Mesmos termos, significados diferentes → Bounded contexts diferentes
```

### 2. Limites de Equipe

**Princípio**: Equipes diferentes frequentemente indicam bounded contexts diferentes.

**Indicadores**:
- Equipes diferentes possuem partes diferentes
- Cronogramas de deploy diferentes
- Stacks tecnológicos diferentes
- Habilidades diferentes necessárias

### 3. Limites de Negócio

**Princípio**: Diferentes capacidades de negócio frequentemente indicam contextos diferentes.

**Indicadores**:
- Diferentes capacidades de negócio
- Diferentes regras de negócio
- Diferentes processos de negócio
- Diferentes métricas de negócio

### 4. Limites de Dados

**Princípio**: Propriedade de dados diferente e requisitos de consistência diferentes indicam limites.

**Indicadores**:
- Propriedade de dados diferente
- Requisitos de consistência diferentes
- Padrões de acesso a dados diferentes
- Modelos de dados diferentes

---

## 🛠️ Processo Prático de Identificação

### Passo 1: Event Storming

**Propósito**: Descobrir eventos de domínio e identificar limites.

**Processo**:
1. Reunir especialistas de domínio e desenvolvedores
2. Identificar eventos de domínio (notas laranja)
3. Agrupar eventos por contexto
4. Identificar limites entre grupos

### Passo 2: Exploração de Linguagem

**Propósito**: Identificar limites de linguagem e diferenças de terminologia.

**Processo**:
1. Entrevistar especialistas de domínio
2. Mapear terminologia em toda a organização
3. Identificar termos ambíguos
4. Documentar diferenças de linguagem

### Passo 3: Análise de Equipe

**Propósito**: Entender estrutura de equipe e identificar limites de equipe.

**Processo**:
1. Mapear organização de equipes
2. Identificar propriedade de equipes
3. Analisar cronogramas de deploy
4. Documentar limites de equipe

### Passo 4: Síntese

**Propósito**: Combinar todos os insights para identificar bounded contexts finais.

**Processo**:
1. Combinar todos os mapas de limites
2. Identificar limites sobrepostos
3. Refinar limites de contexto
4. Documentar bounded contexts finais

---

## 📊 Framework de Decisão

### Devem Estes Ser Contextos Separados?

| Critério | Mesmo Contexto | Contextos Separados |
|----------|---------------|---------------------|
| Terminologia | Mesmos termos, mesmos significados | Termos diferentes ou significados diferentes |
| Equipe | Mesma equipe | Equipes diferentes |
| Deploy | Mesmo cronograma | Cronogramas diferentes |
| Tecnologia | Mesma stack | Stacks diferentes |
| Regras de Negócio | Mesmas regras | Regras diferentes |
| Modelo de Dados | Mesmo modelo | Modelos diferentes |
| Consistência | Mesmos requisitos | Requisitos diferentes |

**Regra de Ouro**: Se 3+ critérios indicam separação, considere contextos separados.

---

## 🚫 Anti-Padrões

### ❌ Muitos Contextos Pequenos

**Problema**: Contextos muito granulares levam a:
- Complexidade excessiva de integração
- Overhead de comunicação
- Complexidade de deploy

**Solução**: Mesclar contextos relacionados ou reconsiderar limites.

### ❌ Poucos Contextos Grandes

**Problema**: Contextos sub-granulares levam a:
- Limites não claros
- Conflitos de equipe
- Gargalos de deploy

**Solução**: Dividir contextos com base em limites claros.

---

## ✅ Checklist de Validação

Antes de finalizar um bounded context, verifique:

- [ ] Tem propósito de negócio claro
- [ ] Tem linguagem ubíqua consistente
- [ ] Tem limites claros
- [ ] Pode ser implantado independentemente
- [ ] Tem propriedade clara (equipe ou papel)
- [ ] Tem interfaces definidas com outros contextos
- [ ] Tem granularidade apropriada (não muito pequeno, não muito grande)
- [ ] Alinha com capacidades de negócio
- [ ] Faz sentido para especialistas de domínio
- [ ] Pode evoluir independentemente

---

## 🔗 Documentação Relacionada

- [Guia de DDD Estratégico](./README.md) - Visão geral do DDD Estratégico
- [Padrões de Context Mapping](./context-mapping-patterns.md) - Como contextos se relacionam
- [Classificação de Subdomínios](./subdomain-classification.md) - Classificar subdomínios
- [Template de Event Storming](../../../../templates/ddd/event-storming-template.md) - Template para event storming
- [Template de Bounded Context](../../../../templates/ddd/bounded-context-template.md) - Template para documentar contextos

**Versão em Inglês**: [Bounded Context Identification Guide (EN)](../bounded-context-identification.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

