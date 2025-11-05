# 🎯 Guia de Classificação de Subdomínios

## 📋 Visão Geral

A classificação de subdomínios é uma decisão estratégica crítica no DDD. Ajuda a determinar onde investir esforço, o que construir internamente e o que terceirizar ou integrar.

**Princípio Fundamental**: Nem todos os subdomínios são iguais. Classifique-os para focar investimento no que mais importa.

---

## 🎯 Tipos de Subdomínios

### 1. Core Domain

**Definição**: A proposta de valor única do seu negócio. O que te diferencia dos concorrentes.

**Características**:
- ✅ **Único**: Único para seu negócio
- ✅ **Vantagem Competitiva**: Te diferencia dos concorrentes
- ✅ **Alta Complexidade**: Lógica de negócio complexa
- ✅ **Expertise Profunda**: Requer expertise profunda do domínio
- ✅ **Alto Valor**: Alto valor de negócio

**Prioridade de Investimento**: **MAIOR** - É aqui que você investe mais esforço.

**Estratégia de Construção**: **Construir Internamente** - Requer desenvolvimento customizado.

---

### 2. Supporting Subdomain

**Definição**: Importante mas não diferenciador. Suporta o core domain mas não fornece vantagem competitiva.

**Características**:
- ⚠️ **Importante**: Importante para operações de negócio
- ⚠️ **Não Único**: Comum em negócios similares
- ⚠️ **Complexidade Média**: Complexidade moderada
- ⚠️ **Papel de Suporte**: Suporta core domain

**Prioridade de Investimento**: **MÉDIA** - Importante mas não o foco.

**Estratégia de Construção**: **Construir ou Terceirizar** - Pode ser construído ou terceirizado dependendo de recursos.

---

### 3. Generic Subdomain

**Definição**: Funcionalidade comum encontrada em vários setores. Sem vantagem competitiva.

**Características**:
- ❌ **Comum**: Comum em vários setores
- ❌ **Sem Vantagem**: Sem vantagem competitiva
- ❌ **Baixa Complexidade**: Relativamente simples
- ❌ **Commodity**: Disponível como soluções commodity

**Prioridade de Investimento**: **MENOR** - Minimize investimento.

**Estratégia de Construção**: **Terceirizar ou Integrar** - Use soluções existentes.

---

## 🔍 Framework de Classificação

### Árvore de Decisão

```
Pergunta 1: Isso é único para nosso negócio?
├─ Não → Generic Subdomain (Terceirizar)
└─ Sim → Pergunta 2: Isso é nossa vantagem competitiva?
    ├─ Não → Supporting Subdomain (Construir ou Terceirizar)
    └─ Sim → Core Domain (Construir Internamente)
```

---

## 📊 Matriz de Classificação

| Critério | Core Domain | Supporting Subdomain | Generic Subdomain |
|----------|-------------|---------------------|-------------------|
| **Unicidade** | Único | Comum | Muito Comum |
| **Vantagem Competitiva** | Alta | Baixa | Nenhuma |
| **Complexidade** | Alta | Média | Baixa |
| **Expertise Necessária** | Profunda | Moderada | Padrão |
| **Prioridade de Investimento** | Maior | Média | Menor |
| **Estratégia de Construção** | Construir Internamente | Construir ou Terceirizar | Terceirizar/Integrar |

---

## 💡 Estratégias de Terceirização para Generic Subdomains

### Estratégia 1: Integração Third-Party

**Use Quando**: Funcionalidade padrão disponível como serviço.

**Exemplos**:
- Pagamento: Stripe, PayPal
- Email: SendGrid, Mailgun
- SMS: Twilio
- Autenticação: Auth0, Firebase Auth

**Benefícios**:
- Implementação rápida
- Sem manutenção
- Confiabilidade comprovada
- Custo-efetivo

### Estratégia 2: Soluções Open Source

**Use Quando**: Solução open source existe e atende necessidades.

**Exemplos**:
- Logging: ELK Stack
- Monitoramento: Prometheus
- Message Queue: RabbitMQ, Kafka

---

## 🎯 Estratégia de Investimento

### Investimento em Core Domain

**Alocação**: 60-80% do esforço de desenvolvimento

**Áreas de Foco**:
- Expertise profunda do domínio
- Lógica de negócio complexa
- Inovação e melhoria
- Vantagem competitiva

### Investimento em Supporting Subdomain

**Alocação**: 15-30% do esforço de desenvolvimento

**Áreas de Foco**:
- Completude funcional
- Eficiência operacional
- Integração com core domain

### Investimento em Generic Subdomain

**Alocação**: 5-10% do esforço de desenvolvimento

**Áreas de Foco**:
- Integração
- Configuração
- Customização mínima

---

## 📚 Exemplos

### Exemplo 1: Plataforma E-Commerce

**Classificação de Subdomínios**:

```
Core Domain (60% esforço):
- Motor de Recomendação de Produtos
  - Algoritmo único
  - Vantagem competitiva
  - Construir internamente

Supporting Subdomain (30% esforço):
- Gerenciamento de Pedidos
  - Importante para operações
  - Construir internamente (complexidade média)

Generic Subdomain (10% esforço):
- Processamento de Pagamento
  - Integrar Stripe
  - Terceirizar

- Envio e Logística
  - Integrar API FedEx
  - Terceirizar
```

---

## 🚫 Anti-Padrões

### ❌ Construindo Generic Subdomains

**Problema**: Construir processamento de pagamento, envio de email, etc. internamente.

**Por que Está Errado**:
- Sem vantagem competitiva
- Desperdiça recursos
- Soluções melhores existem
- Fardo de manutenção

**Solução**: Use soluções existentes (Stripe, SendGrid, etc.).

### ❌ Terceirizando Core Domain

**Problema**: Terceirizar a proposta de valor única.

**Por que Está Errado**:
- Perde vantagem competitiva
- Não pode diferenciar
- Dependente de fornecedores
- Sem controle

**Solução**: Construa core domain internamente.

---

## 🔗 Documentação Relacionada

- [Guia de DDD Estratégico](./README.md) - Visão geral do DDD Estratégico
- [Identificação de Bounded Context](./bounded-context-identification.md) - Identificar contextos
- [Padrões de Context Mapping](./context-mapping-patterns.md) - Relacionamentos de contexto
- [Guia de Arquitetura Evolutiva](../../../evolutionary-architecture/README.md) - Estratégias de evolução

**Versão em Inglês**: [Subdomain Classification Guide (EN)](../subdomain-classification.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

